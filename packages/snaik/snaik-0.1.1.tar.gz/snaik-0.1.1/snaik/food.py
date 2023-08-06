from __future__ import annotations

import numpy as np

from snaik.snake import SnakeData
from snaik.utils import ScatterItem, np_isin2d


class Food(ScatterItem):
    def __init__(self, n_points: int | None = None):
        super().__init__()
        self._points.setBrush("#42aff6")
        self._n_points = n_points

    def fill_positions(self, board_state: dict):
        """
        Simple implementation to randomly pick a food coordinate on the board that
        doesn't collide with a snake
        """

        existing_points = board_state["food"]
        data: SnakeData = board_state["snake_data"]
        grid_size = board_state["grid_size"]

        n_points = self._n_points
        if n_points is None:
            n_points = len(data.get_living_subset())

        # Remove existing points that collide with snakes
        snake_points = data.get_points()
        existing_points = existing_points[~np_isin2d(existing_points, snake_points)][
            :n_points
        ]
        n_posistions_needed = n_points - len(existing_points)

        collision_points = data.get_points()
        collision_points = np.row_stack((collision_points, existing_points)).astype(int)
        collision_points = collision_points[(collision_points >= 0).all(axis=1)]

        board_positions = np.mgrid[0 : grid_size[0], 0 : grid_size[1]].reshape(2, -1).T
        del_idxs = np.ravel_multi_index(collision_points.T, dims=grid_size, mode="clip")
        board_positions = np.delete(board_positions, del_idxs, axis=0)

        if not len(board_positions):
            # Snake has filled the board, so no new food can be added
            return
        new_points = board_positions[
            np.random.choice(len(board_positions), n_posistions_needed, replace=False)
        ]
        new_points = np.row_stack((existing_points, new_points))
        # Last `self._n_points` will contain both existing and new points, so self's
        # new value can be set to that
        self._points.setData(*new_points.T)

    def remove_positions(self, indexes: list[int]):
        existing_points = self.get_xy_points()
        new_points = np.delete(existing_points, indexes, axis=0)
        self._points.setData(*new_points.T)

    def tick(self, board_state: dict):
        out_state = board_state.copy()
        self.fill_positions(board_state)
        out_state["food"] = self.get_xy_points()
        return out_state

    def restart(self, board_state: dict):
        self.fill_positions(board_state)
        board_state["food"] = self.get_xy_points()
        return board_state
