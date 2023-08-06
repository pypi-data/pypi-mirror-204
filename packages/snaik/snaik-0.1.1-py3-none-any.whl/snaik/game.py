from __future__ import annotations

import typing as t
from pathlib import Path

import pyqtgraph as pg
from pyqtgraph.functions import eq as pg_eq
from qtextras import (
    ParameterEditor,
    RunOptions,
    bindInteractorOptions as bind,
    parameterDialog,
)
from qtpy import QtCore

from snaik.food import Food
from snaik.leaderboard import LeaderboardWidget
from snaik.snake import BrainType, SnakeManager
from snaik.staterecorder import StateRecorder
from snaik.utils import ChildItemGroup


class TickProtocol(t.Protocol):
    def tick(self, board_state: dict) -> dict:
        ...

    def restart(self, board_state: dict) -> dict:
        ...


class Game(ChildItemGroup):
    def __init__(
        self,
        snake_brains: t.Sequence[BrainType] = ("greedy",),
        n_food_points: int | None = None,
        grid_size: tuple[int, int] = (10, 10),
        json_path: str | Path | None = None,
        frames_path: str | Path | None = None,
        gif_path: str | Path | None = None,
    ):
        super().__init__()
        self.snake_manager = SnakeManager(snake_brains, grid_size)
        self.snake_manager.setParentItem(self)

        self._game_over = False
        self._last_board_state: dict | None = None

        self.grid_size = grid_size
        self._priority_tick_map: dict[int, TickProtocol] = {}

        self.food = Food(n_points=n_food_points)
        self.food.restart(self.get_board_state())
        self.food.setParentItem(self)

        self.leaderboard = LeaderboardWidget(self.snake_manager)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.tick)

        self.recorder = StateRecorder(
            [self, self.leaderboard],
            json_path,
            frames_path,
            gif_path,
            initial_board_state=self.get_board_state(),
        )

        self.register_tick_callback(self.snake_manager)
        self.register_tick_callback(self.food)
        self.register_tick_callback(self.leaderboard)
        self.register_tick_callback(self.recorder)

    @bind(brains=dict(title="Brain List", type="text", value=""))
    def set_snake_brains(self, brains: str | list[BrainType]):
        if isinstance(brains, str):
            if not brains:
                return
            brains = brains.splitlines()

        self.snake_manager.set_snakes(brains)
        self.restart()

    def tick(self):
        state = self.get_board_state()
        if self._game_over or self.maybe_end_game(state):
            self.pause()
            return
        for priority in sorted(self._priority_tick_map):
            ticker = self._priority_tick_map[priority]
            state = ticker.tick(state)
        return state

    def playback_history_gui(self):
        states = self.recorder.json_states

        def set_tick_number(tick_number: int = len(states) - 1):
            self.set_board_state(states[tick_number])

        param = ParameterEditor.defaultInteractor(
            set_tick_number,
            tick_number=dict(limits=(0, len(states) - 1)),
            runOptions=RunOptions.ON_CHANGING,
        )
        parameterDialog(param)
        # Reset state after dialog closes
        if states:
            self.set_board_state(states[-1])

    def maybe_end_game(self, new_board_state):
        snake_won = any(s.is_winner() for s in self.snake_manager)
        if snake_won or pg_eq(new_board_state, self._last_board_state):
            self._game_over = True
            return True
        self._last_board_state = new_board_state
        return False

    def register_tick_callback(
        self, callback: TickProtocol, priority: int | None = None
    ):
        if priority in self._priority_tick_map:
            raise ValueError(f"Priority {priority} already registered")
        if priority is None:
            priority = max(self._priority_tick_map.keys(), default=-1) + 1
        self._priority_tick_map[priority] = callback
        return priority

    def get_board_state(self):
        return dict(
            snake_data=self.snake_manager.get_snake_data(),
            food=self.food.get_xy_points(),
            grid_size=self.grid_size,
        )

    def restart(self):
        self.timer.stop()
        board_state = self.get_board_state()
        board_state.pop("snake_data")
        for priority in sorted(self._priority_tick_map):
            ticker = self._priority_tick_map[priority]
            board_state = ticker.restart(board_state)
        self._game_over = False

    def set_board_state(self, board_state: dict):
        """
        Similar to ``restart``, but disables the state recorder and forces
        snakes to update from the state rather than set state properties. This
        is useful for restoring a previous game state, which ``restart`` cannot
        do.
        """
        self.timer.stop()
        for priority in sorted(self._priority_tick_map):
            ticker = self._priority_tick_map[priority]
            if ticker is self.recorder:
                continue
            board_state = ticker.restart(board_state)
        self._game_over = False

    def pause(self):
        self.timer.stop()

    def run(self, interval_ms: int = 150):
        self.timer.start(interval_ms)

    def run_full_game(self, abort_on_error=False, **exporter_kwargs):
        self.restart()
        defaults = dict(
            json_path=self.recorder.json_path,
            frames_path=self.recorder.frames_path,
            gif_path=self.recorder.gif_path,
        )
        for kk in set(defaults).intersection(exporter_kwargs):
            defaults[kk] = exporter_kwargs.pop(kk)
        self.recorder.update_properties(**defaults)

        tick = self.tick
        if abort_on_error:

            def tick():
                try:
                    self.tick()
                except:
                    self._game_over = True
                    pg.mkQApp().exit(1)
                    pg.exit()
                    raise

        while not self._game_over:
            tick()
