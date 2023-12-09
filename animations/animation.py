from dataclasses import dataclass

from PyQt6.QtCore import QObject

from helpers.signal import Signal
from helpers.signals import SignalArgs
from widgets.main_window import MainWindow


@dataclass
class OnEndAnimationSignalArgs(SignalArgs):
    pass


class Animation(QObject):
    def __init__(self):
        super().__init__()
        self.on_end = Signal()
        self.main_window = MainWindow.get()

    def start(self):
        raise NotImplemented

    def _emit_on_end(self):
        self.on_end.emit(OnEndAnimationSignalArgs(self))
