import typing

from PyQt6 import QtGui
from PyQt6.QtCore import QSize, pyqtSignal
from PyQt6.QtWidgets import QWidget

from helpers.signals import OnResizeSignalArgs
from widgets.presenter.play_button import PlayButton
from widgets.presenter.select_pack_button import SelectPackButton


class PresenterWindow(QWidget):
    on_resize = pyqtSignal(OnResizeSignalArgs)

    def __init__(self):
        super().__init__()
        # TODO: Solve problem with size of window
        self.setMinimumSize(QSize(640, 480))

        self.setWindowTitle("Окно ведущего")

        self.play_button = PlayButton(self)
        self.play_button.move(20, 20)

        self.select_pack_button = SelectPackButton(self)
        self.select_pack_button.move(20, 20)

    def resizeEvent(self, a0: typing.Optional[QtGui.QResizeEvent]) -> None:
        self.on_resize.emit(OnResizeSignalArgs(sender=self))
