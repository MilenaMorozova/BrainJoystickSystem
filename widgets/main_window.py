import typing

from PyQt6 import QtGui
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout

from helpers.signals import OnResizeSignalArgs
from widgets.central_widget import CentralWidget
from widgets.players_container import PlayersContainer


MAIN_STYLE = """
    background-color: #272D2D;
"""


class MainWindow(QMainWindow):
    on_resize = pyqtSignal(OnResizeSignalArgs)

    def __init__(self):
        super().__init__()
        # TODO: Solve problem with size of window
        self.setFixedSize(840, 680)

        self.setWindowTitle("Брейн ринг система")
        main_widget = QWidget()

        self._active_player_widget = CentralWidget()

        self.players_container = PlayersContainer()

        main_container = QVBoxLayout()
        main_container.setContentsMargins(0, 0, 0, 0)
        main_container.setSpacing(0)
        main_container.addWidget(self._active_player_widget)
        main_container.addLayout(self.players_container)
        main_widget.setLayout(main_container)
        self.setCentralWidget(main_widget)

        self.setStyleSheet(MAIN_STYLE)

    def resizeEvent(self, a0: typing.Optional[QtGui.QResizeEvent]) -> None:
        self.on_resize.emit(OnResizeSignalArgs(sender=self))
