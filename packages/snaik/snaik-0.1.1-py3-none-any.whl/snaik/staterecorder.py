from __future__ import annotations

import json
import typing as t
from pathlib import Path

from pyqtgraph.functions import imageToArray
from qtextras import bindInteractorOptions as bind
from qtpy import QtCore, QtGui, QtWidgets

from snaik.snake import SnakeData
from snaik.utils import BoardStateEncoder, value_converter_json_hook


class DummyWriter:
    def close(self):
        pass

    def append_data(self, *args, **kwargs):
        pass


_save_file_type = dict(
    type="file", value="", acceptMode="AcceptSave", fileMode="AnyFile"
)


class StateRecorder:
    def __init__(
        self,
        scene_items: QtWidgets.QGraphicsItem | list[QtWidgets.QGraphicsItem],
        json_path: str | Path | None = None,
        frames_path: str | Path | None = None,
        gif_path: str | Path | None = None,
        gif_update_ms: int = 150,
        initial_board_state: dict | None = None,
    ):
        self.json_path = self.frames_path = self.gif_path = None
        self.gif_writer = DummyWriter()
        self.board_state_hook: t.Callable | None = (
            value_converter_json_hook(initial_board_state)
            if initial_board_state
            else None
        )

        self.json_states = []
        if self.frames_path:
            self.frames_path.mkdir(exist_ok=True)
        self.scene_items = (
            scene_items if isinstance(scene_items, list) else [scene_items]
        )
        self.gif_update_ms = gif_update_ms

        try:
            import imageio
        except ImportError:
            imageio = None
        self.imageio = imageio

        self.update_properties(
            json_path=json_path, frames_path=frames_path, gif_path=gif_path
        )

    def tick(self, board_state: dict):
        self.json_states.append(board_state)
        screenshot = None
        if self.frames_path:
            screenshot = self.get_board_screenshot()
            screenshot.save(
                self.frames_path.joinpath(f"{len(self.json_states):04d}.png").as_posix()
            )
        if self.json_path:
            with open(self.json_path, "w") as f:
                json.dump(self.json_states, f, cls=BoardStateEncoder)

        if self.gif_path:
            screenshot = screenshot or self.get_board_screenshot()
            # Can't chain operators since life cycle is important
            qimg = screenshot.toImage()
            np_img_bgra_wh = imageToArray(qimg)
            np_img_rgb_wh = np_img_bgra_wh[..., [2, 1, 0]]
            np_img_rgb = np_img_rgb_wh.transpose(1, 0, 2)
            self.gif_writer.append_data(np_img_rgb)

        return board_state

    def get_board_screenshot(self):
        total_size = QtCore.QSize(0, 0)
        for item in self.scene_items:
            size = item.scene().views()[0].size()
            total_size.setHeight(total_size.height() + size.height())
            total_size.setWidth(max(total_size.width(), size.width()))
        pixmap = QtGui.QPixmap(total_size)
        painter = QtGui.QPainter(pixmap)
        y_offset = 0
        # Y-axis is flipped in Qt, so we need to render from the bottom up
        for item in reversed(self.scene_items):
            view = item.scene().views()[0]
            cur_size = view.size()
            x_offset = (total_size.width() - cur_size.width()) // 2
            tgt_rect = QtCore.QRect(
                x_offset, y_offset, cur_size.width(), cur_size.height()
            )
            view.render(painter, target=tgt_rect)
            y_offset += cur_size.height()
            # When grabbing, artifacts appear on the board. As a workaround,
            # force a redraw of the board after grabbing.
            item.scene().update()
        painter.end()

        QtWidgets.QApplication.processEvents()
        return pixmap

    def restart(self, board_state: dict):
        self.json_states.clear()
        if self.gif_path:
            self.gif_writer.close()
        self._restart_writer()
        self.tick(board_state)

        return board_state

    def _restart_writer(self):
        self.gif_writer.close()
        self.gif_writer = DummyWriter()
        if self.gif_path and not self.imageio:
            raise ImportError("imageio is required to export gifs")
        elif self.gif_path:
            self.gif_writer = self.imageio.get_writer(
                self.gif_path, mode="I", duration=self.gif_update_ms / 1000
            )

    @bind(
        json_path=dict(**_save_file_type, nameFilter="*.json"),
        frames_path=dict(type="file", value="", fileMode="Directory"),
        gif_path=dict(**_save_file_type, nameFilter="*.gif"),
    )
    def update_properties(self, *, json_path="", frames_path="", gif_path=""):
        self.json_path = Path(json_path) if json_path else None
        self.frames_path = Path(frames_path) if frames_path else None
        self.gif_path = Path(gif_path) if gif_path else None
        self._restart_writer()

        if self.json_path and self.json_path.exists():
            self.json_states = self.read_json_file(self.json_path)

    def read_json_file(self, path: str | Path):
        def hook(obj: dict):
            obj = SnakeData.json_hook(obj)
            if self.board_state_hook:
                return self.board_state_hook(obj)
            return obj

        with open(path, "r") as f:
            return json.load(f, object_hook=hook)
