from dataclasses import dataclass
from datetime import datetime

from PyQt6.QtCore import QTimer, QObject, pyqtSignal

from helpers.signals import SignalArgs


@dataclass
class OnTickSignalArgs(SignalArgs):
    rest: float


@dataclass
class OnEndSignalArgs(SignalArgs):
    pass


class Timer(QObject):
    TICK_TIME = 100

    on_tick = pyqtSignal(OnTickSignalArgs)
    on_end = pyqtSignal(OnEndSignalArgs)

    def __init__(self, time: float = 10):
        super().__init__()
        self._max_time = time
        self._rest_of_question_time = time
        self._start_time = None
        self._timer = QTimer()
        self._timer.timeout.connect(self._tick)

    def get_rest(self) -> float:
        return self._rest_of_question_time - (datetime.now() - self._start_time).total_seconds()

    def set_max_time(self, time: float):
        self._timer.stop()
        self._max_time = time
        self._rest_of_question_time = time

    def start(self):
        self._start_time = datetime.now()
        self._timer.start(self.TICK_TIME)

    def pause(self):
        if self._start_time is not None:
            self._rest_of_question_time = self.get_rest()
            self._timer.stop()

    def reset(self):
        self._timer.stop()
        self._rest_of_question_time = self._max_time

    def _tick(self):
        current_rest = self.get_rest()
        self.on_tick.emit(OnTickSignalArgs(sender=self, rest=current_rest))

        if current_rest <= 0:
            self._timer.stop()
            self.on_end.emit(OnEndSignalArgs(sender=self))
