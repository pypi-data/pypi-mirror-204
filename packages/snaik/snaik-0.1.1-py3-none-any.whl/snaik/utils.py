from __future__ import annotations

import itertools
import json
import typing as t
from enum import Enum
from queue import Empty, Queue
from threading import Thread

import numpy as np
import pyqtgraph as pg
from qtpy import QtWidgets


class StringEnum(str, Enum):
    def __contains__(self, __key: str) -> bool:
        return __key in list(self)


class Command(StringEnum):
    TURN = "TURN"
    NOOP = "NOOP"
    DIE = "DIE"


class Action(dict):
    def __init__(self, command: Command = Command.NOOP, **kwargs):
        if command not in list(Command):
            raise ValueError(
                f"Invalid command {command}. Must be one of {list(Command)}"
            )
        super().__init__(**kwargs)
        self["command"] = command

    def get_command(self, return_kwargs=False):
        if not return_kwargs:
            return self["command"]
        copied = self.copy()
        command = copied.pop("command")
        return command, copied


class Direction(StringEnum):
    NORTH = "NORTH"
    SOUTH = "SOUTH"
    EAST = "EAST"
    WEST = "WEST"

    @classmethod
    def cycle(cls) -> t.Generator[t.Self]:
        yield from itertools.cycle(cls)


class Status(StringEnum):
    ALIVE = "ALIVE"
    DEAD = "DEAD"
    WINNER = "WINNER"


class LogMode(StringEnum):
    GUI = "GUI"
    TERM = "TERM"
    NONE = "NONE"


class ChildItemGroup(QtWidgets.QGraphicsItem):
    # False positive signature mismatch
    def paint(self, painter, option, widget=None):  # noqa
        pass

    def boundingRect(self):
        return self.childrenBoundingRect()


class ScatterItem(ChildItemGroup):
    def __init__(self):
        super().__init__(None)

        self._points = pg.ScatterPlotItem(pxMode=False, size=0.5, pen=None)
        self._points.setParentItem(self)

    def get_xy_points(self):
        return np.column_stack(self._points.getData()).astype(np.int32)


def np_isin2d(arr1: np.ndarray, arr2: np.ndarray) -> np.ndarray:
    """
    Check if each row of arr1 is in arr2

    Parameters
    ----------
    arr1
        2d array
    arr2
        2d array

    Returns
    -------
    isin
        1d array of bools
    """
    if arr1.ndim == 1:
        return np.all(arr1 == arr2, axis=-1).any(axis=-1)
    return np.all(arr1[:, None, :] == arr2[None, :, :], axis=-1).any(axis=-1)


def is_in_bounds(points: np.ndarray, grid_size: tuple[int, int]):
    """
    Check if each point is in bounds

    Parameters
    ----------
    points
        Nx2 array of points or a single (2,) point
    grid_size
        The size of the grid

    Returns
    -------
    is_in_bounds
        1d array of bools
    """
    return np.all(points >= 0, axis=1) & np.all(points < grid_size, axis=1)


class NonBlockingReader:
    def __init__(self, pipe):
        self.pipe = pipe
        self.queue = Queue()
        self.thread = Thread(target=self.enqueue_output, args=(pipe, self.queue))
        self.thread.daemon = True
        self.thread.start()

    @staticmethod
    def enqueue_output(out, queue):
        for line in iter(out.readline, b""):
            queue.put(line)
        out.close()

    def readline(self, timeout=None):
        try:
            return self.queue.get(block=timeout is not None, timeout=timeout)
        except Empty:
            return None


class BoardStateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def value_converter_json_hook(reference_obj: dict):
    """
    JSON decoder hook that converts values to the correct type
    """

    def inner(obj: dict):
        for kk in set(reference_obj).intersection(obj):
            ref_val = reference_obj[kk]
            obj_val = obj[kk]
            if isinstance(ref_val, np.ndarray):
                obj[kk] = np.asarray(obj_val, dtype=ref_val.dtype)
            elif not isinstance(obj_val, type(ref_val)):
                obj[kk] = type(ref_val)(obj_val)
        return obj

    return inner


def svg_to_png(file: str, output: str = None):
    """Helper to convert logo to pyinstaller-accepted png"""
    from qtpy import QtGui

    pg.mkQApp()
    if output is None:
        output = file.replace(".svg", ".jpg")
    pixmap = QtGui.QPixmap(file)
    return pixmap.save(output)
