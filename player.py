from dataclasses import dataclass

from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtGui import QColor

from helpers.signals import SignalArgs


@dataclass
class OnChangeNameSignalArgs(SignalArgs):
    old_name: str
    new_name: str


@dataclass
class OnChangeScoreSignalArgs(SignalArgs):
    old_score: int
    new_score: int


class Player(QObject):
    on_change_name = pyqtSignal(OnChangeNameSignalArgs)
    on_change_score = pyqtSignal(OnChangeScoreSignalArgs)

    def __init__(self, name: str, joystick_id: int, color: QColor):
        super().__init__()
        self.color = color
        self.joystick_id = joystick_id
        self._name = name
        self._score = 0

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        old_name = self._name
        self._name = value
        self.on_change_name.emit(
            OnChangeNameSignalArgs(sender=self, old_name=old_name, new_name=value)
        )

    @property
    def score(self) -> int:
        return self._score

    @score.setter
    def score(self, value: int):
        old_score = self._score
        self._score = value
        self.on_change_score.emit(
            OnChangeScoreSignalArgs(sender=self, old_score=old_score, new_score=value)
        )