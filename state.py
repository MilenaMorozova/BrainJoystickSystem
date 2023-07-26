from enum import IntEnum

from PyQt6.QtCore import pyqtSignal, QObject


class StatusEnum(IntEnum):
    STOPPED = 0
    PAUSED = 1
    STARTED = 2


class State(QObject):
    __instance = None
    on_change_status = pyqtSignal(StatusEnum)

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

        self.__status = value
        self.on_change_status.emit(value)

    @staticmethod
    def get_state() -> 'State':
        if State.__instance is None:
            State.__instance = State()
        return State.__instance
