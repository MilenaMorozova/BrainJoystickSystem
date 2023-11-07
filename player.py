from dataclasses import dataclass

from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtGui import QColor

from helpers.signals import SignalArgs


@dataclass
class OnChangeNameSignalArgs(SignalArgs):
    old_name: str
    new_name: str


class Player:
    class Signals(QObject):
        on_change_name = pyqtSignal(OnChangeNameSignalArgs)

    def __init__(self, name: str, joystick_id: int, color: QColor):
        self.color = color
        self.joystick_id = joystick_id
        self.__name = name
        self.signals = self.Signals()

    @property
    def name(self) -> str:
        return self.__name

    @property
    def on_change_name(self) -> pyqtSignal:
        return self.signals.on_change_name

    @name.setter
    def name(self, value: str):
        old_name = self.__name
        self.__name = value
        self.on_change_name.emit(
            OnChangeNameSignalArgs(sender=self, old_name=old_name, new_name=value)
        )
