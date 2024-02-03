import typing

from PyQt6 import QtGui
from PyQt6.QtCore import QPropertyAnimation, QSize, pyqtProperty, QParallelAnimationGroup, QPoint
from PyQt6.QtWidgets import QPushButton, QGridLayout, QWidget, QSizePolicy, QGraphicsOpacityEffect

from enums.status_enum import StatusEnum
from packs.question import Question
from packs.theme import Theme
from services.service_locator import ServiceLocator

SELECT_QUESTION_GRID_CELL_CSS = """
    font-size: 26px;
    /* border-radius: 35px; */
    color: white;
    background-color: #0097F5;
"""

BIG_QUESTION_MARGIN = (10, 10)


class SelectQuestionGridCell(QPushButton):
    def __init__(self, text: str):
        super().__init__(text)
        self.locator = ServiceLocator.get()
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.setStyleSheet(SELECT_QUESTION_GRID_CELL_CSS)

    def get_growing_animation(self) -> QParallelAnimationGroup:
        duration = 1000
        shift = (BIG_QUESTION_MARGIN[0] // 2, BIG_QUESTION_MARGIN[1] // 2)

        growing = QPropertyAnimation(self, b'size', self)
        growing.setEndValue(self.parent().size() - QSize(*BIG_QUESTION_MARGIN))
        growing.setDuration(duration)

        moving = QPropertyAnimation(self, b'pos', self)
        moving.setEndValue(self.parent().pos() + QPoint(*shift))
        moving.setDuration(duration)

        animation_group = QParallelAnimationGroup(self)
        animation_group.addAnimation(growing)
        animation_group.addAnimation(moving)

        return animation_group

    def get_collapse_animation(self) -> QParallelAnimationGroup:
        duration = 300
        end_size = self.size() - QSize(self.width(), 0)
        shift = QPoint(self.width() // 2, 0)

        collapse = QPropertyAnimation(self, b'size', self)
        collapse.setEndValue(end_size)
        collapse.setDuration(duration)

        moving = QPropertyAnimation(self, b'pos', self)
        moving.setEndValue(self.pos() + shift)
        moving.setDuration(duration)

        animation_group = QParallelAnimationGroup(self)
        animation_group.addAnimation(collapse)
        animation_group.addAnimation(moving)

        return animation_group


class QuestionButton(SelectQuestionGridCell):
    def __init__(self, question: Question):
        super().__init__(str(question.price))
        self.question = question
        self.clicked.connect(self.click_handler)

    def click_handler(self):
        if self.locator.game.state.status == StatusEnum.CHOICE_QUESTION and not self.question.is_answered:
            self.locator.game.state.select_question(self.question)

    def mark_as_answered(self):
        self.setText("")


class FinalQuestionButton(SelectQuestionGridCell):
    def __init__(self, theme: Theme):
        super().__init__(theme.name)
        self.theme = theme
        self.clicked.connect(self.click_handler)
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)
        self.is_clicked = False

    def click_handler(self):
        if self.locator.game.state.status == StatusEnum.CHOICE_QUESTION:
            self.mark_as_answered()

    def mark_as_answered(self):
        self.opacity_effect.setOpacity(0)
        self.is_clicked = True
        self.theme.questions[0].is_answered = True


class SelectQuestionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.game_store = ServiceLocator.get().game

        self.grid_widget = QWidget(self)
        self.grid = QGridLayout(self.grid_widget)
        self.questions_widgets: list[QuestionButton] = []
        self.final_questions_widgets: list[FinalQuestionButton] = []

        self.game_store.on_change_round_number.connect(self.update_questions)

    def resizeEvent(self, a0: typing.Optional[QtGui.QResizeEvent]) -> None:
        self.grid_size = self.size()

    @pyqtProperty(QSize)
    def grid_size(self) -> QSize:
        return self.grid_widget.size()

    @grid_size.setter
    def grid_size(self, value: QSize):
        self.grid_widget.setFixedSize(value)
        self.grid_widget.move(
            int(self.width() / 2 - value.width() / 2),
            int(self.height() / 2 - value.height() / 2)
        )

    def get_growing_animation(self) -> QPropertyAnimation:
        grid_growing = QPropertyAnimation(self, b'grid_size', self)
        grid_growing.setStartValue(QSize())
        grid_growing.setEndValue(self.size())
        grid_growing.setDuration(3000)
        return grid_growing

    def show_round_questions(self):
        self.questions_widgets = []
        for y, theme in enumerate(self.game_store.round.themes):
            theme_name_button = SelectQuestionGridCell(theme.name)
            self.grid.addWidget(theme_name_button, y, 0, 1, 3)
            for x, question in enumerate(theme.questions, 3):
                question_button = QuestionButton(question)
                self.grid.addWidget(question_button, y, x)
                self.questions_widgets.append(question_button)

    def show_final_round_questions(self):
        def check_questions():
            not_deleted_themes = [w.theme for w in self.final_questions_widgets if not w.is_clicked]
            if len(not_deleted_themes) == 1:
                last_theme = not_deleted_themes[0]
                self.game_store.state.select_question(last_theme.questions[0])

        self.final_questions_widgets = []
        for y, theme in enumerate(self.game_store.round.themes):
            theme_button = FinalQuestionButton(theme)
            theme_button.clicked.connect(check_questions)
            self.grid.addWidget(theme_button, y, 0, 1, 3)
            self.final_questions_widgets.append(theme_button)

        check_questions()

    def update_questions(self, *args, **kwargs):
        if self.game_store.round.is_final:
            self.show_final_round_questions()
        else:
            self.show_round_questions()

    def get_cell_by_question(self, question: Question) -> SelectQuestionGridCell:
        if self.game_store.round.is_final:
            for widget in self.final_questions_widgets:
                if widget.theme.questions[0] is question:
                    return widget
        else:
            for widget in self.questions_widgets:
                if widget.question is question:
                    return widget
