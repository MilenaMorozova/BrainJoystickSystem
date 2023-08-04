from PyQt6.QtCore import QObject, pyqtSignal


class Player:
    class Signals(QObject):
        on_change_name = pyqtSignal(str, str)

    def __init__(self, name: str, joystick_id: int):
        self.joystick_id = joystick_id
        self.__name = name
        self.signals = self.Signals()

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        old_name = self.__name
        self.__name = value
        self.signals.on_change_name.emit(old_name, value)
