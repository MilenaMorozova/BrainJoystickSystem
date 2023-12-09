import typing

from PyQt6 import QtGui
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout

from helpers.signals import OnResizeSignalArgs
from widgets.lobby_central_widget import LobbyCentralWidget
from widgets.players_container import PlayersContainer
from widgets.select_question_widget import SelectQuestionWidget

MAIN_STYLE = """
    background-color: #272D2D;
"""


class MainWindow(QMainWindow):
    _instance = None
    on_resize = pyqtSignal(OnResizeSignalArgs)

    def __init__(self):
        super().__init__()
        # TODO: Solve problem with size of window
        self.setMinimumSize(840, 680)

        self.setWindowTitle("Брейн ринг система")
        self.main_widget = QWidget()

        self.lobby_central_widget = LobbyCentralWidget()
        self.select_question_widget = SelectQuestionWidget()
        self.select_question_widget.hide()

        self.players_container = PlayersContainer()

        self.main_container = QVBoxLayout()
        self.main_container.setContentsMargins(0, 0, 0, 0)
        self.main_container.setSpacing(0)

        self.main_container.addWidget(self.select_question_widget, 1)
        self.main_container.addWidget(self.lobby_central_widget, 1)
        self.main_container.addLayout(self.players_container)

        self.main_widget.setLayout(self.main_container)
        self.setCentralWidget(self.main_widget)

        self.setStyleSheet(MAIN_STYLE)

        MainWindow._instance = self

    def resizeEvent(self, a0: typing.Optional[QtGui.QResizeEvent]) -> None:
        self.on_resize.emit(OnResizeSignalArgs(sender=self))

    @staticmethod
    def get() -> 'MainWindow':
        return MainWindow._instance
