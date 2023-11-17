from dataclasses import dataclass
from typing import Optional

from PyQt6.QtCore import QObject, QAbstractAnimation

from helpers.signal import Signal
from helpers.signals import SignalArgs


@dataclass
class OnEndAnimationSignalArgs(SignalArgs):
    pass


class Animation(QObject):
    def __init__(self):
        super().__init__()
        self.on_end = Signal()
        self.main_animation: Optional[QAbstractAnimation] = None

    def start(self):
        self.main_animation.finished.connect(self._emit_on_end)
        self.main_animation.start()

    def _emit_on_end(self):
        self.on_end.emit(OnEndAnimationSignalArgs(self))
