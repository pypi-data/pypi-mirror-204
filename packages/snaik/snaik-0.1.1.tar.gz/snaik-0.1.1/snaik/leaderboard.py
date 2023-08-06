from __future__ import annotations

import typing as t

import pyqtgraph as pg
from qtpy import QtCore, QtWidgets

from snaik.snake import Snake


class LeaderboardItem(pg.LegendItem):
    def __init__(self, snakes: t.Sequence[Snake]):
        super().__init__(labelTextColor="#000", brush="k")
        self.setFlag(self.GraphicsItemFlag.ItemIgnoresTransformations, False)
        self.snakes = snakes

    def refresh(self, board_state: dict = None):
        self.clear()
        all_scores = [snake.get_score() for snake in self.snakes]
        min_score = min(all_scores)
        score_ptp = max(all_scores) - min_score
        base_font_size = 12
        z_values = sorted([snake.zValue() for snake in self.snakes])
        # Negative id in key means 0 is sorted first
        for snake in reversed(
            sorted(self.snakes, key=lambda s: (s.is_alive(), s.get_score(), -s.id))
        ):
            # Make sure high-scoring snakes are always on top
            snake.setZValue(z_values.pop())

            if score_ptp > 0:
                font_size = (
                    base_font_size + (snake.get_score() - min_score) / score_ptp * 7
                )
            else:
                font_size = base_font_size
            color = snake.primary_color
            html = snake.get_html_string()
            self.addItem(pg.ScatterPlotItem(pen=None, brush=color), html)
            label: pg.LabelItem = self.items[-1][1]
            label.setText(label.text, color=color, size=f"{font_size}pt")
        self.updateSize()
        return board_state


class LeaderboardWidget(QtWidgets.QGraphicsView):
    def __init__(self, snakes: t.Sequence[Snake]):
        super().__init__()
        leaderboard_item = LeaderboardItem(snakes)
        leaderboard_item.refresh()
        scene = QtWidgets.QGraphicsScene()
        scene.addItem(leaderboard_item)
        self.setScene(scene)
        self.setBackgroundBrush(pg.mkBrush("#000"))
        self.leaderboard_item = leaderboard_item

        self.horizontalScrollBar().setStyleSheet("QScrollBar { height: 0px; }")
        self.verticalScrollBar().setStyleSheet("QScrollBar { width: 0px; }")
        self.restart()

    def resizeEvent(self, event):
        to_return = super().resizeEvent(event)
        self.fitInView(self.leaderboard_item, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.update()
        return to_return

    def tick(self, board_state: dict = None):
        self.leaderboard_item.refresh()
        self.fitInView(self.leaderboard_item, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.update()
        return board_state

    def restart(self, board_state: dict = None):
        out = self.tick(board_state)
        fixed_height = max(75, 40 * len(self.leaderboard_item.snakes))
        self.setFixedHeight(fixed_height)
        return out
