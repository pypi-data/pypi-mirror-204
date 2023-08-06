from __future__ import annotations

import json
import random
import subprocess
import sys
import typing as t

import numpy as np
from qtpy import QtCore, QtWidgets

from snaik.utils import (
    Action,
    BoardStateEncoder,
    Command,
    Direction,
    NonBlockingReader,
    is_in_bounds,
    np_isin2d,
)

if t.TYPE_CHECKING:
    from snaik.snake import SnakeData


class KeyboardBrain(QtCore.QObject):
    filter_bound = False

    def __init__(self, nsew_keys=("Up", "Down", "Right", "Left")):
        """
        Controls a snake using keys on the keyboard.

        Parameters
        ----------
        nsew_keys
            Keys to use for changing direction, can be any standard keyboard key, i.e.,
            "Up", "A", "Left", etc. Order should match which key should be pressed to
            go north, south, east, and west, respectively.
        """
        super().__init__(None)
        Key = QtCore.Qt.Key
        nsew_keys = [k.upper() if len(k) == 1 else k for k in nsew_keys]
        qt_keys = [getattr(Key, f"Key_{key}") for key in nsew_keys]
        self.key_map = dict(zip(qt_keys, Direction))
        self.current_direction: Direction | None = None
        key_str = "".join(nsew_keys)
        self.__name__ = f"Keys `{key_str}`"

    def eventFilter(self, _obj: QtCore.QObject, event: QtCore.QEvent) -> bool:
        if event.type() != QtCore.QEvent.KeyPress:
            return False
        key = event.key()
        if key not in self.key_map:
            return False
        self.current_direction = self.key_map[key]
        return False

    # Don't worry about "unused variable" warnings since the signature should match
    def __call__(self, snake_id: int, board_state: dict):  # noqa
        if self.current_direction is None:
            return Action(Command.NOOP)
        return Action(Command.TURN, direction=self.current_direction)

    def restart(self, board_state: dict = None):
        self.current_direction = None
        return board_state


def random_brain(snake_id: int, board_state: dict):
    """
    Tells the snake to take a random action that hopefully won't immediately
    result in death

    Parameters
    ----------
    snake_id
        The id of the snake using this algorithm
    board_state
        The current state of the board

    Returns
    -------
    action
        The action to take
    """
    grid_size = board_state["grid_size"]
    data: SnakeData = board_state["snake_data"]
    head = data.get_head_points(snake_id)

    directions = np.array(list(Direction), dtype=object)
    coords = (
        np.array(
            [
                np.array([0, 1]),
                np.array([0, -1]),
                np.array([1, 0]),
                np.array([-1, 0]),
            ]
        )
        + head
    )
    living = data.get_living_subset()
    other_ids = set(living) - {snake_id}
    disallowed_positions = living.get_points(exclude_tails=True)
    # Filter invalid next directions
    mask = is_in_bounds(coords, grid_size) & ~np_isin2d(coords, disallowed_positions)
    if not np.any(mask):
        # Nothing can be done, all positions are invalid
        return Action(Command.NOOP)
    not_recommended = np_isin2d(
        coords, living.get_potential_future_head_points(other_ids)
    )
    ideal = directions[mask & ~not_recommended]
    if len(ideal) > 0:
        return Action(Command.TURN, direction=random.choice(ideal))
    # If there are no ideal directions, pick a suboptimal one
    return Action(Command.TURN, direction=random.choice(directions[mask]))


class GreedyBrain:
    INVALID = -1

    def find_next_direction(
        self,
        disallowed_coordinates: np.ndarray,
        unpleasant_coordinates: np.ndarray,
        start: np.ndarray,
        ends: np.ndarray,
        grid_size: tuple[int, int],
    ):
        """
        Finds the shortest path between two points on a grid, given a list of coordinates
        that cannot be visited

        Parameters
        ----------
        disallowed_coordinates
            Nx2 array of coordinates that cannot be visited
        unpleasant_coordinates
            Nx2 array of coordinates that are technically reachable, but are
            undesirable to visit (i.e, might cause a collision one step in the future)
        start
            The starting coordinate
        ends
            Nx2 array of potential ending coordinates
        grid_size
            The size of the grid

        Returns
        -------
        action: Action
            The next action to take to get closer to an end point
        """
        # Initialize the grid
        grid = np.empty(grid_size, dtype=np.int32)
        queue = [start]
        directions = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])

        start_idx = tuple(start)
        grid = self.initialize_grid(
            grid, start_idx, disallowed_coordinates, unpleasant_coordinates, ends
        )

        current_previous_map: dict[tuple[int, int], tuple[int, int] | None] = {
            start_idx: None
        }

        # For now, simply don't consider end locations that are unpreferred
        ends = ends[~np_isin2d(ends, unpleasant_coordinates)]

        reached_ends = []
        while queue:
            current = queue.pop(0)

            # Check if we've reached the end
            if np_isin2d(current, ends):
                reached_ends.append(tuple(current))
                if len(reached_ends) == len(ends):
                    break

            for direction in directions:
                next_coord = current + direction
                next_idx = tuple(next_coord)
                current_idx = tuple(current)

                # Check if the next coordinate is valid
                if np.any(next_coord < 0) or np.any(next_coord >= grid_size):
                    continue
                if grid[next_idx] == self.INVALID:
                    # invalid location
                    continue

                new_distance = self.get_score(grid, current_idx)
                if new_distance < grid[next_idx]:
                    grid[next_idx] = new_distance
                    current_previous_map[next_idx] = current_idx
                    # Add the next coordinate to the queue
                    queue.append(next_coord)
        # If no path exists, panic and do nothing
        if not reached_ends:
            return Action(Command.NOOP)

        # Otherwise, walk back to the right direction to take
        best_score, best_end = np.inf, None
        for end in reached_ends:
            if grid[end] < best_score:
                best_score = grid[end]
                best_end = end

        current = tuple(best_end)
        while current_previous_map.get(current, start_idx) != start_idx:
            current = current_previous_map[current]
        distance = current[0] - start[0], current[1] - start[1]
        direction = {
            (0, 1): Direction.NORTH,
            (0, -1): Direction.SOUTH,
            (1, 0): Direction.EAST,
            (-1, 0): Direction.WEST,
        }[distance]
        return Action(Command.TURN, direction=direction)

    def get_score(
        self,
        grid: np.ndarray,
        current_index: t.Sequence[int],
    ):
        # Set the next coordinate to the current coordinate's distance + 1
        return grid[current_index] + 1

    def initialize_grid(
        self,
        grid: np.ndarray,
        start: np.ndarray,
        disallowed_coordinates: np.ndarray,
        unpleasant_coordinates: np.ndarray,
        ends: np.ndarray,
    ):
        grid[:] = np.iinfo(np.int32).max
        grid[disallowed_coordinates[:, 0], disallowed_coordinates[:, 1]] = self.INVALID
        # TODO: Allow traversal across unpleasant locations, since they are
        #   technically reachable any may provide favorable outcomes. For now,
        #   exhaustive searches are not friendly in Python so just don't consider
        #   them. The logic for their traversal is already implemented, just need
        #   to speed up calculation if exhaustive searching is enabled.
        grid[unpleasant_coordinates[:, 0], unpleasant_coordinates[:, 1]] = self.INVALID
        grid[tuple(start)] = 0
        return grid

    def __call__(self, snake_id: int, board_state: dict):
        """
        Tells the snake to always eat the closest food while avoiding death conditions
        (self intersections, other snakes, and walls)

        Parameters
        ----------
        snake_id
            The id of the snake using this algorithm
        board_state
            The current state of the board

        Returns
        -------
        action
            The action to take
        """
        food = board_state["food"]
        living: SnakeData = board_state["snake_data"].get_living_subset()
        disallowed_positions = living.get_points(exclude_tails=True)
        # Remove sentinel values and invalid positions
        disallowed_positions = disallowed_positions[
            is_in_bounds(disallowed_positions, board_state["grid_size"])
        ]
        other_ids = set(living) - {snake_id}
        # Don't go within one space of the other snake's head to preemptively avoid
        # future collisions
        unrecommended_positions = living.get_potential_future_head_points(other_ids)
        self_futures = living.get_potential_future_head_points(snake_id)
        unrecommended_positions = unrecommended_positions[
            is_in_bounds(unrecommended_positions, board_state["grid_size"])
            & np_isin2d(unrecommended_positions, self_futures)
        ]

        action = self.find_next_direction(
            disallowed_positions,
            unrecommended_positions,
            living.get_head_points(snake_id),
            food,
            board_state["grid_size"],
        )
        if action.get_command() == Command.NOOP:
            # If there's no valid direction to take, try to turn in a random direction
            action = random_brain(snake_id, board_state)
        return action


class ExternalBrain:
    def __init__(self, command_name: str, *args: str):
        self.__name__ = command_name
        self.subprocess = subprocess.Popen(
            [command_name, *args], stdin=subprocess.PIPE, stdout=subprocess.PIPE
        )
        self.reader = NonBlockingReader(self.subprocess.stdout)

    def restart(self, board_state: dict):
        if self.subprocess.poll() is None:
            self.subprocess.kill()
        self.subprocess = subprocess.Popen(
            self.__name__, stdin=subprocess.PIPE, stdout=subprocess.PIPE
        )
        self.subprocess.stdin.write(
            json.dumps(board_state, cls=BoardStateEncoder).encode()
        )
        self.subprocess.stdin.flush()
        self.subprocess.stdout.flush()
        self.reader = NonBlockingReader(self.subprocess.stdout)

    def __call__(self, snake_id: int, board_state: dict):
        board_state = board_state.copy()
        board_state["snake_id"] = snake_id
        encoded = json.dumps(board_state, cls=BoardStateEncoder).encode() + b"\n"
        self.subprocess.stdin.write(encoded)
        self.subprocess.stdin.flush()
        response = self.reader.readline(timeout=0.5)
        if response is None:
            return Action(Command.DIE)
        return Action(**json.loads(response.decode()))


def get_keyboard_brain(nsew_keys=("Up", "Down", "Right", "Left")):
    instance = QtWidgets.QApplication.instance()
    if instance is None:
        instance = QtWidgets.QApplication(sys.argv)
        # Alternatively can raise error
        # raise RuntimeError("No QApplication instance found")
    brain = KeyboardBrain(nsew_keys)
    instance.installEventFilter(brain)
    return brain


def get_external_brain(brain_name: str):
    try:
        return ExternalBrain(*brain_name.split(" "))
    except FileNotFoundError:
        raise ValueError(
            f"Brain `{brain_name}` not found, must be one of: "
            f"{brain_name_factory_map.keys()} or a valid executable"
        )


brain_name_factory_map = {
    "greedy": GreedyBrain,
    "random": lambda: random_brain,
    "keyboard": get_keyboard_brain,
}


def get_brain(brain_args: str):
    brain_key = brain_args.split()[0]
    if brain_key in brain_name_factory_map:
        string_kwargs = brain_args[len(brain_key) + 1 :]
        kwargs = eval(f"dict({string_kwargs})")
        return brain_name_factory_map[brain_key](**kwargs)
    else:
        return get_external_brain(brain_args)
