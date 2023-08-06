from __future__ import annotations

import typing as t
from pathlib import Path

import numpy as np
import pyqtgraph as pg
import qtextras as qte
from qdarktheme import load_stylesheet
from qtpy import QtCore, QtGui, QtWidgets

from snaik.game import Game
from snaik.utils import LogMode

bind = qte.bindInteractorOptions


class Grid(QtWidgets.QGraphicsItem):
    def __init__(self, n_x_cells: int, n_y_cells: int):
        super().__init__()
        self.n_x_cells, self.n_y_cells = n_x_cells, n_y_cells
        self.pen = pg.mkPen("#eee", width=3)
        # Slightly offset so points appear centered
        self.setPos(-0.5, -0.5)

    def paint(self, painter, option, widget=None):
        painter.setPen(self.pen)
        rect = self.boundingRect()
        cell_width = rect.width() / self.n_x_cells
        cell_height = rect.height() / self.n_y_cells
        for ii in range(self.n_x_cells):
            for jj in range(self.n_y_cells):
                to_draw = QtCore.QRectF(
                    ii * cell_width, jj * cell_height, cell_width, cell_height
                )
                painter.drawRect(to_draw)

    def boundingRect(self):
        return QtCore.QRectF(0, 0, self.n_x_cells, self.n_y_cells)


class BoardWidget(pg.GraphicsView):
    def __init__(self, parent=None, *, grid_size: tuple[int, int] = (12, 12), **kwargs):
        super().__init__(parent)
        # Clean up unparented top window that spawns in super class
        self.viewbox = pg.ViewBox(
            defaultPadding=0.0125,
            enableMenu=False,
            lockAspect=True,
            enableMouse=False,
        )
        self.grid = Grid(*grid_size)
        path_kwargs = dict(
            json_path=kwargs.pop("json_path", ""),
            frames_path=kwargs.pop("frames_path", ""),
            gif_path=kwargs.pop("gif_path", ""),
        )
        self.game = game = Game(**kwargs, grid_size=grid_size)

        self.tools_editor = qte.ParameterEditor(name="Tools")
        interactive = self.tools_editor.registerFunction(
            game.recorder.update_properties,
            name="Recorder Properties",
            runOptions=qte.RunOptions.ON_CHANGED,
            **path_kwargs,
        )
        # Make sure parameters update when the function is called
        setattr(game.recorder, "update_properties", interactive)
        interactive()
        if game.recorder.json_states:
            game.set_board_state(game.recorder.json_states[-1])

        # fmt: off
        names_funcs_shortcuts = [
            ("Set Brains",       self.set_brains_gui,       "Ctrl+B"),
            (None,               game.run,                  "Ctrl+R"),
            (None,               game.pause,                "Ctrl+P"),
            (None,               game.restart,              "Ctrl+Shift+R"),
            (None,               game.tick,                 "Ctrl+T"),
            ("Playback History", game.playback_history_gui, "Ctrl+H"),
            ("Dev Console",      self.dev_console_gui,      "Ctrl+`"),
        ]
        # fmt: on

        for name, func, shortuct in names_funcs_shortcuts:
            if not name:
                name = self.tools_editor.defaultInteractor.titleFormat(func.__name__)
            kwargs = dict(name=name)
            if shortuct:
                kwargs["name"] = f"{name} ({shortuct})"
                kwargs["runActionTemplate"] = dict(shortcut=shortuct)
            registered = self.tools_editor.registerFunction(func, **kwargs)
            # Hide the function to reduce clutter if it can be run just from the
            # menu bar
            self.tools_editor.rootParameter.child(registered.__name__).hide()

        self.menu = self.tools_editor.createActionsFromFunctions(
            stealShortcuts=False, keepUpdated=False
        )

        # Special case: register "run" again but on property change. This allows
        # it to appear in the tools editor where the user can adjust the tick rate,
        # but also allows it to be run from the menu bar with a shortcut
        self.tools_editor.registerFunction(
            self.update_tick_rate,
            runOptions=qte.RunOptions.ON_CHANGED,
            tick_rate_ms=dict(title="Tick Rate (ms)"),
            nest=False,
        )
        self.tools_editor.registerFunction(
            self.set_theme, runOptions=qte.RunOptions.ON_CHANGED, nest=False
        )
        self.set_theme()

        self.setup_gui()
        self.setMinimumSize(500, 500)
        self.tools_editor.setMinimumWidth(300)

    def update_tick_rate(self, tick_rate_ms=150):
        interactive = [
            interactive
            for interactive in self.tools_editor.nameFunctionMap.values()
            if interactive.function == self.game.run
        ][0]
        interactive.parameters["interval_ms"].setValue(tick_rate_ms)
        if self.game.timer.isActive():
            interactive()

    def set_brains_gui(self):
        parameter = qte.ParameterEditor.defaultInteractor(self.game.set_snake_brains)
        qte.parameterDialog(parameter)

    def setup_gui(self):
        self.setCentralItem(self.viewbox)

        self.viewbox.addItem(self.grid)
        self.viewbox.addItem(self.game)

    def dev_console_gui(self):
        # Return type is denoted `QWidget`, but the board's usage is inside a
        # `QMainWindow`. Cast to avoid ide errors
        top_window = t.cast(SnaikWindow, self.window())
        qte.safeSpawnDevConsole(top_window, game=self.game, board=self)

    @bind(theme=dict(type="list", limits=["dark", "light"]))
    def set_theme(self, theme="dark"):
        if theme in ["dark", "light"]:
            app = QtWidgets.QApplication.instance()
            app.setStyleSheet(load_stylesheet(theme))
        else:
            raise ValueError(f"Invalid theme: {theme}")

        background_map = dict(dark="k", light="w")
        background = background_map.pop(theme)
        other = pg.mkColor(background_map.popitem()[1])
        color = pg.mkColor(background)
        brush = pg.mkBrush(background)

        self.grid.pen.setColor(other)
        self.grid.update()
        self.game.leaderboard.leaderboard_item.setBrush(brush)
        self.game.leaderboard.setBackgroundBrush(brush)
        self.viewbox.setBackgroundColor(color)

    def update_grid_size(self, grid_size: tuple[int, int], pixel_to_grid_ratio=40):
        self.grid.n_x_cells, self.grid.n_y_cells = grid_size

        game = self.game
        game.grid_size = grid_size
        game.snake_manager.grid_size = grid_size
        game.food.remove_positions(np.r_[: len(game.food.get_xy_points())])
        game.restart()
        min_size = (np.array(grid_size) / pixel_to_grid_ratio).astype(int)
        self.setMinimumSize(*min_size)
        self.update()
        self.viewbox.autoRange()


class SnaikWindow(QtWidgets.QMainWindow):
    def __init__(self, log_mode: LogMode | list[LogMode] = LogMode.GUI, **kwargs):
        super().__init__()
        resources_dir = Path(__file__).resolve().parent / "resources"
        self.setWindowIcon(QtGui.QIcon(str(resources_dir / "logo.svg")))
        self.setWindowTitle("snAIk")
        board = self.board = BoardWidget(parent=self, **kwargs)
        qte.EasyWidget.buildMainWindow(
            [
                board,
                [board.game.leaderboard, board.tools_editor],
            ],
            window=self,
            layout="H",
            useSplitter=True,
        )
        menu = self.menuBar()
        for action in self.board.menu.actions():
            menu.addAction(action)
        self.game = board.game
        splitter: QtWidgets.QSplitter = self.easyChild.widget_  # noqa
        for ii in range(2):
            splitter.setCollapsible(ii, False)

        self.logger = qte.AppLogger.getAppLogger(__name__)
        if log_mode == LogMode.GUI or LogMode.GUI in log_mode:
            self.logger.registerExceptions(self)
