import typing

from PyQt6 import QtGui
from PyQt6.QtCore import QSize, pyqtSignal
from PyQt6.QtWidgets import QWidget

from helpers.signals import OnResizeSignalArgs
from widgets.presenter.lobby_presenter_widget import LobbyPresenterWidget


class PresenterWindow(QWidget):
    on_resize = pyqtSignal(OnResizeSignalArgs)

    def __init__(self):
        super().__init__()
        # TODO: Solve problem with size of window
        self.setMinimumSize(QSize(640, 480))

        self.setWindowTitle("Окно ведущего")

        self.lobby_presenter_widget = LobbyPresenterWidget(self)

    def resizeEvent(self, a0: typing.Optional[QtGui.QResizeEvent]) -> None:
        self.on_resize.emit(OnResizeSignalArgs(sender=self))
