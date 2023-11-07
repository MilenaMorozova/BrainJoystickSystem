from dataclasses import dataclass
from enum import IntEnum

from PyQt6.QtCore import QObject, pyqtSignal

from helpers.signals import SignalArgs


class StatusEnum(IntEnum):
    STOPPED = 0
    PAUSED = 1
    STARTED = 2


@dataclass
class OnChangeStatusSignalArgs(SignalArgs):
    new_status: StatusEnum
    old_status: StatusEnum


class State(QObject):
    __instance = None
    on_change_status = pyqtSignal(OnChangeStatusSignalArgs)

    def __init__(self):
        super().__init__()
        self.__status = StatusEnum.STOPPED

    @property
    def status(self) -> StatusEnum:
        return self.__status

    @status.setter
    def status(self, value: StatusEnum):
        if self.__status == value:
            return

        old_status = self.__status
        self.__status = value
        self.on_change_status.emit(
            OnChangeStatusSignalArgs(sender=self, old_status=old_status, new_status=value)
        )

    @staticmethod
    def get_state() -> 'State':
        if State.__instance is None:
            State.__instance = State()
        return State.__instance
