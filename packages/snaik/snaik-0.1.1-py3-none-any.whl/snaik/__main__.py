import logging
import os
import sys
from pathlib import Path

import pyqtgraph as pg
from qtextras import makeCli
from qtpy import QtCore

from snaik import __version__
from snaik.window import SnaikWindow


def main(
    grid_size=(12, 12),
    snake_brains: str = "keyboard",
    n_food_points: int = None,
    json_path="",
    frames_path="",
    gif_path="",
    headless=False,
):
    """
    Run a game of Snaik.

    Parameters
    ----------
    grid_size
        The size of the game board in (x, y) coordinates.
    snake_brains
        The brains to use for the snakes. Options are ``greedy``, ``keyboard``,
        ``random``, or an external command (e.g., ``python my_snake_brain.py``).
        Specify multiple brains by separating each option with a semicolon. For
        example:

            - to play an arrow key-controlled snake against a greedy snake, use
              ``--snake_brains keyboard;greedy``.
            - Note that a ``keyboard`` snake can also be passed ``nsew_keys=WSDA``
              to use the w, s, d, and a keys (or any other combination) instead of the
              arrow keys (in north, south, east, and west order).
              So, you could play against another human through using:
              ``--snake_brains "keyboard; keyboard nsew_keys='wsda'"
            - Note that arbitrary external programs can also be used if they accept
              JSON strings over stdin and output a JSON string of the next snake
              move over stdout. For example, you could play against a neural network
              by using ``--snake_brains "python my_neural_net.py; keyboard"`` (assuming
              that ``my_neural_net.py`` is a Python script that looks forever over stdin
              for a JSON string of the game state and outputs a JSON string of the next
              snake move). Or, you could compile a C++ application into
              "my_c_app.exe" and pass ``--snake_brains "my_c_app.exe; keyboard"``.
              Programs should be terminated on receiving a SIGINT (Ctrl+C) or SIGTERM.
    n_food_points
        The number of food points to spawn. If None, the number of food points will be
        equal to the number of snakes. In this case, as snakes die, less food will be
        spawned.
    json_path
        The path to save the game state as a JSON file.
    frames_path
        The path to save each frame of the game as a PNG file.
    gif_path
        The path to save the game as a GIF file.
    headless
        If True, the game will be run without a GUI. This is useful for running
        experiments. It is recommended to use the `--json-path` option to save the
        game state if ``headless`` is True.
    """
    snake_brains = snake_brains.split(";")
    kwargs = locals()
    logging.basicConfig(level=logging.INFO)
    if kwargs.pop("headless", False):
        os.environ["QT_QPA_PLATFORM"] = "offscreen"
        font_path = Path(__file__).resolve().parent / "resources"
        os.environ.setdefault("QT_QPA_FONTDIR", font_path.as_posix())
        app = pg.mkQApp()

        single_shot = QtCore.QTimer()
        single_shot.setSingleShot(True)

        def run():
            win.game.run_full_game(abort_on_error=True, **kwargs)
            app.exit(0)

        single_shot.timeout.connect(run)
        single_shot.start(0)

    app = pg.mkQApp()
    win = SnaikWindow(**kwargs)
    win.show()
    pg.exec()


def main_cli(**kwargs):
    if "--version" in sys.argv:
        print(__version__)
        return
    kwargs = vars(makeCli(main).parse_args())
    main(**kwargs)


if __name__ == "__main__":
    main_cli()
