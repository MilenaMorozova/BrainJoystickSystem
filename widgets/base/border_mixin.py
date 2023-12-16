from typing import Optional

from PyQt6.QtCore import QPoint, pyqtProperty, QLine, QPropertyAnimation
from PyQt6.QtGui import QPainter, QPen, QColor


class BorderMixin:
    def __init__(self):
        self.margin = (0, 0)
        self.border_width = 10
        self._part = 1
        self._enable_border = False
        self._right_line: Optional[QLine] = None
        self._bottom_line: Optional[QLine] = None
        self._left_line: Optional[QLine] = None
        self._top_line: Optional[QLine] = None
        self._timer_animation = QPropertyAnimation(self, b'part_of_border')
        self._timer_animation.setEndValue(0)

    @pyqtProperty(float)
    def part_of_border(self) -> float:
        return self._part

    @part_of_border.setter
    def part_of_border(self, value: float):
        self._part = value
        if self._enable_border:
            self.update()

    def shift(self, x: bool, y: bool) -> QPoint:
        x_sign = 1 if x else -1
        y_sign = 1 if y else -1
        return QPoint(self.margin[0] * x_sign, self.margin[1] * y_sign) + \
            QPoint(self.border_width * -x_sign, self.border_width * -y_sign) / 2

    @property
    def top_left(self) -> QPoint:
        return self.pos() + self.shift(True, True)

    @property
    def top_right(self) -> QPoint:
        return self.pos() + QPoint(self.width(), 0) + self.shift(False, True)

    @property
    def bottom_left(self) -> QPoint:
        return self.pos() + QPoint(0, self.height()) + self.shift(True, False)

    @property
    def bottom_right(self) -> QPoint:
        return self.pos() + QPoint(self.width(), self.height()) + self.shift(False, False)

    def set_enable_border(self, value: bool):
        self._enable_border = value
        self.update()

    def draw_line(self, painter: QPainter, start: QPoint, end: QPoint, part: float = 1):
        if part == 0:
            return None

        if part != 1:
            vec = end - start
            end = start + vec*part

        return painter.drawLine(start, end)

    def get_part_of_interval(self, value: float, start: float, end: float) -> float:
        if value >= end:
            return 1
        elif value <= start:
            return 0

        return (value - start) / (end - start)

    def clean_border(self):
        if self._top_line:
            self._top_line.clear()
        if self._left_line:
            self._left_line.clear()
        if self._bottom_line:
            self._bottom_line.clear()
        if self._right_line:
            self._right_line.clear()

    def draw_border(self):
        self.clean_border()
        painter = QPainter(self)

        pen = QPen(QColor(255, 255, 255, 255))
        pen.setWidth(self.border_width)
        painter.setPen(pen)

        # top
        top_part = self.get_part_of_interval(self._part, 0, 0.25)
        self._top_line = self.draw_line(painter, self.top_right, self.top_left, top_part)
        # left
        left_part = self.get_part_of_interval(self._part, .25, 0.50)
        self._left_line = self.draw_line(painter, self.top_left, self.bottom_left, left_part)
        # bottom
        bottom_part = self.get_part_of_interval(self._part, 0.50, 0.75)
        self._bottom_line = self.draw_line(painter, self.bottom_left, self.bottom_right, bottom_part)
        # right
        right_part = self.get_part_of_interval(self._part, .75, 1)
        self._right_line = self.draw_line(painter, self.bottom_right, self.top_right, right_part)

        painter.end()

    def update_border(self):
        if self._enable_border:
            self.draw_border()
        else:
            self.clean_border()

    def start_border_animation(self, part: float, msec: int):
        self._timer_animation.setStartValue(part)
        self._timer_animation.setDuration(msec)
        self._timer_animation.start()

    def stop_border_animation(self):
        self._timer_animation.stop()
