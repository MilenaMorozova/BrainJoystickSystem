from PyQt6.QtCore import QPropertyAnimation, QSize, QParallelAnimationGroup, QPoint
from PyQt6.QtWidgets import QPushButton, QSizePolicy

from widgets.select_question_widget import SELECT_QUESTION_GRID_CELL_CSS, BIG_QUESTION_MARGIN

ANSWER_TO_QUESTION_WIDGET_CSS = SELECT_QUESTION_GRID_CELL_CSS + f"""
    margin: {BIG_QUESTION_MARGIN[0]};
"""


class AnswerToQuestionWidget(QPushButton):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.setStyleSheet(ANSWER_TO_QUESTION_WIDGET_CSS)

    def get_expand_animation(self) -> QParallelAnimationGroup:
        duration = 300
        start_size = self.size() - QSize(self.size().width(), 0)
        start_pos = QPoint(self.size().width() // 2, 0)

        expand = QPropertyAnimation(self, b'size', self)
        expand.setStartValue(start_size)
        expand.setEndValue(self.size())
        expand.setDuration(duration)

        moving = QPropertyAnimation(self, b'pos', self)
        moving.setStartValue(start_pos)
        moving.setEndValue(QPoint())
        moving.setDuration(duration)

        animation_group = QParallelAnimationGroup(self)
        animation_group.addAnimation(expand)
        animation_group.addAnimation(moving)

        return animation_group
