import typing

from PyQt6 import QtGui
from PyQt6.QtCore import QPropertyAnimation, QSize, pyqtProperty
from PyQt6.QtWidgets import QPushButton, QGridLayout, QWidget, QSizePolicy

from packs.parser import Parser
from packs.question import Question


SELECT_QUESTION_GRID_CELL_CSS = """
    font-size: 26px;
    /* border-radius: 35px; */
    color: white;
    background-color: #0097F5;
"""


class SelectQuestionGridCell(QPushButton):
    def __init__(self, text: str):
        super().__init__(text)
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.setStyleSheet(SELECT_QUESTION_GRID_CELL_CSS)


class QuestionButton(SelectQuestionGridCell):
    def __init__(self, question: Question):
        super().__init__(str(question.price))


parser = Parser(r'C:\Users\masht\Downloads\Ночные посиделки №47.siq')
parser.load()
pack = parser.get_pack()


class SelectQuestionWidget(QWidget):
    def __init__(self):
        super().__init__()
        # TODO swap to store.game.pack
        self.pack = pack
        r = self.pack.rounds[0]

        self.grid_widget = QWidget(self)
        self.grid = QGridLayout(self.grid_widget)

        for y, theme in enumerate(r.themes):
            theme_name_button = SelectQuestionGridCell(theme.name)
            self.grid.addWidget(theme_name_button, y, 0, 1, 3)
            for x, question in enumerate(theme.questions, 3):
                question_button = QuestionButton(question)
                self.grid.addWidget(question_button, y, x)

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
