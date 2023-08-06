from __future__ import annotations

import logging
import random
import typing as t

import numpy as np
import pyqtgraph as pg
from qtpy import QtWidgets

from snaik.brain import get_brain
from snaik.utils import (
    Action,
    ChildItemGroup,
    Command,
    Direction,
    ScatterItem,
    Status,
    np_isin2d,
)

_direction_distance_map = {
    Direction.NORTH: [0, 1],
    Direction.SOUTH: [0, -1],
    Direction.EAST: [1, 0],
    Direction.WEST: [-1, 0],
}
_id_color_map = {num: pg.intColor(num) for num in range(100)}
_FOOD_VALUE = 20
BrainType = t.Optional[t.Union[t.Callable[[int, dict], Action], str]]


class SnakeData(dict):
    def __init__(self, snake_info: dict | t.Iterable[dict]):
        if not isinstance(snake_info, dict):
            init_data = {info["id"]: info for info in snake_info}
        else:
            init_data = snake_info
        super().__init__(init_data)

    def get_points(
        self, *, exclude_ids: int | list[int] = None, exclude_tails=False, stack=True
    ) -> np.ndarray:
        if exclude_ids is None:
            exclude_ids = []
        elif np.isscalar(exclude_ids):
            exclude_ids = [exclude_ids]
        all_pts = []
        for id_, info in self.items():
            if id_ in exclude_ids:
                continue
            pts = info["points"]
            if exclude_tails and (len(pts) - 1) not in info["food_indexes"]:
                pts = pts[:-1]
            all_pts.append(pts)
        if stack:
            return (
                np.vstack(all_pts) if len(all_pts) else np.zeros((0, 2), dtype=np.int32)
            )
        longest_snake = max((len(p) for p in all_pts), default=0)
        padded = np.full((len(all_pts), longest_snake, 2), -1, dtype=np.int32)
        for i, p in enumerate(all_pts):
            padded[i, : len(p)] = p
        return padded

    def get_head_points(self, snake_ids: int | t.Iterable[int] = None) -> np.ndarray:
        if snake_ids is None:
            snake_ids = list(self.keys())
        if isinstance(snake_ids, int):
            return self[snake_ids]["points"][Snake.HEAD]
        if not len(snake_ids):
            return np.zeros((0, 2), dtype=np.int32)
        pts = np.array([self[snake_id]["points"][Snake.HEAD] for snake_id in snake_ids])
        return np.vstack(pts)

    def get_potential_future_head_points(
        self, snake_ids: int | t.Iterable[int] = None
    ) -> np.ndarray:
        heads = np.atleast_2d(self.get_head_points(snake_ids))
        if not len(heads):
            return heads
        directions = np.array(list(_direction_distance_map.values()))
        futures = np.vstack([head + directions for head in heads])
        return np.unique(futures, axis=0)

    def get_living_subset(self):
        return SnakeData(
            {id_: info for id_, info in self.items() if info["status"] != Status.DEAD}
        )

    @classmethod
    def json_hook(cls, data: dict):
        subkeys = {"id", "points"}
        if len(subkeys & set(data)) == len(subkeys):
            # Inner snake hook, convert points to numpy array
            data["points"] = np.asarray(data["points"], dtype=np.int32)

        if "snake_data" in data:
            # Outer snake hook, convert str id keys into ints
            data["snake_data"] = {
                int(id_): info for id_, info in data["snake_data"].items()
            }
        return data


class Snake(ScatterItem):
    HEAD = 0
    TAIL = -1
    BODY = slice(1, None)
    INVALID_POSITION = -2

    def __init__(
        self,
        id: int,
        brain: BrainType = None,
        direction: Direction | None = None,
        color: str = None,
    ):
        super().__init__()
        self.id = id
        self._brain: BrainType = None

        self._score = 0

        self._direction = direction or random.choice(list(Direction))
        self._status = Status.ALIVE
        self._food_indexes: list[int] = []

        self.set_brain(brain)

        if color is None:
            color = _id_color_map[id]
        else:
            color = pg.mkColor(color)

        line_pen = pg.mkPen(
            width=self._points.opts["size"] / 3,
            cosmetic=False,
            color=color,
        )
        self.line_plot = pg.PlotCurveItem(
            pen=line_pen, pxMode=self._points.opts["pxMode"]
        )
        self.line_plot.setZValue(-1)
        self.line_plot.setParentItem(self)

        # Style properties
        self._spot_size = self._points.opts["size"]
        self._food_size = self._spot_size * 1.5
        self.primary_color = color

    def __str__(self):
        if self._brain is None:
            brain_name = "brainless"
        elif hasattr(self._brain, "__name__"):
            brain_name = self._brain.__name__
        else:
            brain_name = type(self._brain).__name__
        return f"Snake #{self.id} ({brain_name}): {self.get_score()} points"

    def get_html_string(self):
        normal_str = str(self)
        if self._status == Status.DEAD:
            normal_str = f"<s>{normal_str}</s>"
        return normal_str

    def get_state(self):
        return {
            "id": self.id,
            "score": self.get_score(),
            "status": self.get_status(),
            "direction": self._direction,
            "food_indexes": self._food_indexes.copy(),
            "points": self.get_xy_points().astype(np.int32),
        }

    def set_state(self, state: dict):
        expected_keys = set(self.get_state())
        got_keys = set(state).union({"id"})
        if missing := expected_keys.difference(got_keys):
            raise ValueError(f"Missing keys in state: `{missing}`")
        if extra := got_keys.difference(expected_keys):
            raise ValueError(f"Unexpected keys in state: `{extra}`")

        self._score = state["score"]
        self.set_status(state["status"])
        self.turn(state["direction"])
        self._set_xy_points(state["points"])
        self._food_indexes = state["food_indexes"]
        self._update_point_sizes()

    def get_next_action(self, state: dict) -> Action:
        if self._brain is None:
            return Action()
        return self._brain(self.id, state)

    def perform_action(self, action: Action):
        """
        Take the given action.
        """
        command, kwargs = action.get_command(return_kwargs=True)
        func = getattr(self, command.lower())
        func(**kwargs)

    def turn(self, direction: Direction = None):
        if direction is None:
            return
        if direction not in list(Direction):
            raise ValueError(f"Invalid direction: `{direction}`")
        self._direction = direction

    def noop(self):
        pass

    def move_in_direction(self):
        distance = _direction_distance_map[self._direction]
        self.move(*distance)

    def move(self, x_distance: int, y_distance: int):
        distance = np.clip([x_distance, y_distance], -1, 1)
        # if np.abs(distance).sum() != 1:
        #     raise ValueError("Must move exactly one cell in either x or y direction")
        points = self.get_xy_points()
        food_point = np.zeros_like(points, shape=(0, 2))
        growth_point = len(points) - 1
        if growth_point >= 0 and growth_point in self._food_indexes:
            # Food is at the tail, time to grow
            food_point = points[growth_point].copy()
            self._food_indexes.remove(growth_point)
        points = np.roll(points, 1, axis=0)
        points[self.HEAD] = points[self.HEAD + 1] + distance
        points = np.vstack([points, food_point])
        self._set_xy_points(points)
        self.increment_food_indexes()
        self._increment_score(-1)

    def add_food_index(self, index: int | None = None):
        if index is None:
            index = self.HEAD
        if index == self.HEAD:
            # Just ate some food, score some points
            self._increment_score(_FOOD_VALUE)
        n_points = len(self.get_xy_points())
        if index < -1 or index >= n_points:
            raise ValueError(f"Invalid food index: {index}")
        self._food_indexes.append(index)
        self._update_point_sizes()

    def _update_point_sizes(self):
        n_points = len(self.get_xy_points())
        if not len(self._food_indexes):
            self._points.setSize(self._spot_size)
        else:
            sizes = np.array([self._spot_size] * n_points)
            sizes[self._food_indexes] = self._food_size
            self._points.setSize(sizes)

    def get_food_points(self):
        points = self.get_xy_points()
        return points[self._food_indexes]

    def get_status(self):
        return self._status

    def get_score(self):
        return self._score

    def _increment_score(self, increment: int):
        if increment == 0:
            return
        self._score += increment

    def set_status(self, status: Status):
        self._status = status
        opacity = 1.0 if status != Status.DEAD else 0.175
        self.setOpacity(opacity)

    def is_alive(self):
        return self._status in [Status.ALIVE, Status.WINNER]

    def is_winner(self):
        return self._status == Status.WINNER

    def increment_food_indexes(self):
        for ii in range(len(self._food_indexes)):
            self._food_indexes[ii] += 1
            if self._food_indexes[ii] >= len(self.get_xy_points()):
                raise ValueError("Food index out of bounds")
        self._update_point_sizes()

    def restart_brain(self, board_state: dict):
        if hasattr(self._brain, "restart"):
            self._brain.restart(board_state)

    def set_brain(self, brain: BrainType):
        if isinstance(brain, str):
            brain = get_brain(brain)
        self._brain = brain

    def set_initial_positions(self, board_size: tuple, num_segments=3, margin=3):
        """
        Create the initial positions for the snake based on its direction.
        """
        self._score = num_segments * _FOOD_VALUE
        x_array = np.arange(num_segments)
        y_array = np.zeros_like(x_array)
        if self._direction in [Direction.NORTH, Direction.EAST]:
            x_array = x_array[::-1]
        if self._direction in [Direction.NORTH, Direction.SOUTH]:
            x_array, y_array = y_array, x_array

        # Subtract 1 since positions are zero-indexed
        x_size, y_size = board_size[0] - 1, board_size[1] - 1
        if self._direction == Direction.NORTH:
            offset = [x_size - margin, margin]
        elif self._direction == Direction.SOUTH:
            offset = [margin, y_size - margin - num_segments]
        elif self._direction == Direction.EAST:
            offset = [margin, margin]
        elif self._direction == Direction.WEST:
            offset = [x_size - margin - num_segments, y_size - margin]
        else:
            raise ValueError(f"Invalid direction: `{self._direction}`")

        points = np.column_stack([x_array, y_array]) + np.array(offset)
        self._set_xy_points(points)
        self._food_indexes.clear()

    def _set_xy_points(self, points: np.ndarray):
        brushes = [pg.mkBrush(self.primary_color.lighter())] * len(points)
        brushes[self.HEAD] = pg.mkBrush(self.primary_color.darker(120))
        self._points.setData(*points.T, brush=brushes)
        self.line_plot.setData(*points.T)


class SnakeManager(ChildItemGroup):
    def __init__(
        self,
        brains: t.Sequence[BrainType],
        grid_size: tuple[int, int] | None = None,
        parent: QtWidgets.QGraphicsItem | None = None,
    ):
        super().__init__(parent)
        self._snakes: list[Snake] = []
        self.grid_size = grid_size
        self.death_condition_log_map: dict[t.Callable, str] = {}

        self.set_snakes(brains)

        self.register_death_condition(
            self.get_wall_collisions, "Snakes {ids} collided with the wall"
        )
        self.register_death_condition(
            self.get_other_snake_collisions, "Snakes {ids} ran into another snake"
        )
        self.register_death_condition(
            self.get_self_collisions, "Snakes {ids} ran into themselves"
        )
        self.register_death_condition(
            self.get_starved_snakes, "Snakes {ids} starved to death"
        )

    def set_snakes(self, snakes_or_brains: t.Sequence[Snake | BrainType]):
        snakes = []
        directions = Direction.cycle()
        for ii, ctor in enumerate(snakes_or_brains):
            if isinstance(ctor, Snake):
                snake = ctor
                snake.id = ii
            else:
                snake = Snake(ii, ctor, next(directions))
            snakes.append(snake)

        # Wait to perform snake replacement until here just in case there were
        # any errors in the above code
        for snake in self:
            snake.setParentItem(None)
        for snake in snakes:
            snake.setParentItem(self)
        self._snakes = snakes
        self.restart()

    def __iter__(self) -> t.Iterator[Snake]:
        return iter(self._snakes)

    def __getitem__(self, item) -> Snake:
        return self._snakes[item]

    def __len__(self) -> int:
        return len(self._snakes)

    def get_snake_data(self):
        return SnakeData(map(Snake.get_state, self))

    def get_wall_collisions(self, data: SnakeData) -> np.ndarray:
        """
        Return ids of snakes that collided with the wall
        """
        living = data.get_living_subset()
        ids = np.array(list(living))
        heads = living.get_head_points()
        return ids[(heads == -1).any(axis=1) | (heads == self.grid_size).any(axis=1)]

    def get_other_snake_collisions(self, data: SnakeData) -> list[int]:
        dead_ids = []
        if len(data) == 1:
            # No other snakes to collide with
            return dead_ids
        living = data.get_living_subset()
        ids = np.array(list(living))
        for ii, check_head in zip(ids, living.get_head_points()):
            if np.any((check_head < 0) | (check_head >= self.grid_size)):
                # Snake is already dead or hit a wall, not another snake
                continue
            other_snakes = living.get_points(exclude_ids=ii)
            if np_isin2d(check_head, other_snakes):
                # Self's head hit any segment from any other snake
                dead_ids.append(ii)
        return dead_ids

    def get_self_collisions(self, data: SnakeData) -> np.ndarray:
        living = data.get_living_subset()
        ids = np.array(list(living))
        # .all() says both x and y collided at once, .any() says head collided with
        # any segment
        self_collisions = [
            np_isin2d(coords[Snake.HEAD], coords[Snake.BODY])
            for coords in living.get_points(stack=False)
        ]
        # self_collisions is n_snakes x n_segments-1
        return ids[self_collisions]

    def get_starved_snakes(self, data: SnakeData) -> np.ndarray:
        living = data.get_living_subset()
        return np.array([id_ for id_, info in living.items() if info["score"] == 0])

    def register_death_condition(
        self, condition: t.Callable[[SnakeData], t.Sequence[int]], log_format: str
    ):
        self.death_condition_log_map[condition] = log_format

    def move_snakes(self, board_state: dict):
        for snake in filter(Snake.is_alive, self):
            action = snake.get_next_action(board_state)
            snake.perform_action(action)
            if action.get_command() != Command.DIE:
                snake.move_in_direction()
            else:
                logging.getLogger(__name__).info(
                    f"Snake {snake.id} died of brainfreeze"
                )

    def feed_snakes(self, board_state: dict):
        food_points = board_state["food"]
        data: SnakeData = board_state["snake_data"]
        living = data.get_living_subset()
        ids = np.array(list(living))

        if not len(living):
            # No snakes left to feed
            return np.array([], dtype=np.int32)

        living_points = living.get_points(stack=False)
        # n_snakes x n_food array indicating whether a snake was fed and which food it
        # ate. In theory, if two snakes ate the same food, they would have already died
        # from self-collision, so we don't need to worry about that scenario
        collision_mask = np.all(
            living_points[:, Snake.HEAD, :][:, None, :] == food_points[None, :, :],
            axis=2,
        )
        indexes = np.nonzero(collision_mask)
        fed_snakes = ids[np.unique(indexes[0])]
        eaten_food_idxs = np.unique(indexes[1])
        if len(fed_snakes):
            logging.getLogger(__name__).info(f"Snakes {fed_snakes} ate food")
            for snake_id in fed_snakes:
                self[snake_id].add_food_index(Snake.HEAD)

        return eaten_food_idxs

    def kill_invalid_snakes(self, board_state: dict):
        all_dead_ids = []
        for condition, message in self.death_condition_log_map.items():
            dead_ids = condition(board_state["snake_data"])
            if len(dead_ids):
                logging.getLogger(__name__).info(message.format(ids=dead_ids))
                all_dead_ids.extend(dead_ids)
        for snake_id in all_dead_ids:
            self[snake_id].set_status(Status.DEAD)
            board_state["snake_data"][snake_id]["status"] = Status.DEAD
        return board_state

    def check_for_winner(self, board_state: dict):
        data: SnakeData = board_state["snake_data"]
        living = data.get_living_subset()

        if len(data) > 1 and len(living) == 1:
            winner = next(iter(living))
            data[winner]["status"] = Status.WINNER
            self[winner].set_status(Status.WINNER)
            logging.getLogger(__name__).info(f"Snake {winner} won!")

        return board_state

    def tick(self, board_state: dict):
        out_state = board_state.copy()
        self.move_snakes(board_state)
        # Update with new snake positions
        out_state["snake_data"] = self.get_snake_data()
        out_state = self.kill_invalid_snakes(out_state)
        out_state = self.check_for_winner(out_state)
        eaten_food_idxs = self.feed_snakes(out_state)
        out_state["food"] = np.delete(board_state["food"], eaten_food_idxs, axis=0)
        return out_state

    def restart(self, board_state: dict | None = None):
        if board_state is None:
            board_state = {}
        snake_data: SnakeData = board_state.get("snake_data", {})
        for ii, snake in enumerate(self):
            if state := snake_data.get(ii):
                snake.set_state(state)
            else:
                self.initialize_snake(ii)
            snake.restart_brain(board_state)
        if board_state:
            board_state["snake_data"] = self.get_snake_data()
        return board_state

    def initialize_snake(self, snake_id: int):
        snake = self[snake_id]
        direction = list(Direction)[snake_id % len(Direction)]
        snake.turn(direction)
        snake.set_initial_positions(self.grid_size, margin=snake_id // 3 * 2)
        snake.set_status(Status.ALIVE)
        return snake

    def get_leaderboard_html(self):
        to_print = sorted(self, key=Snake.get_score, reverse=True)
        return "\n".join(str(snake) for snake in to_print)
