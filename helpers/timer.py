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


@dataclass
class OnChangeRunStatusSignalArgs(SignalArgs):
    is_running: bool


class Timer(QObject):
    TICK_TIME = 100

    on_tick = pyqtSignal(OnTickSignalArgs)
    on_end = pyqtSignal(OnEndSignalArgs)
    on_change_run_status = pyqtSignal(OnChangeRunStatusSignalArgs)

    def __init__(self, time: float = 10):
        super().__init__()
        self.max_time = time
        self._rest_of_time = time
        self._start_time = None
        self._timer = QTimer()
        self._timer.timeout.connect(self._tick)

    def get_rest(self) -> float:
        if self._start_time:
            return self._rest_of_time - (datetime.now() - self._start_time).total_seconds()

        return self._rest_of_time

    def set_max_time(self, time: float):
        self._stop()
        self.max_time = time

    def start(self):
        if self._start_time is not None:
            return

        self._start_time = datetime.now()
        self._timer.start(self.TICK_TIME)
        self.on_change_run_status.emit(OnChangeRunStatusSignalArgs(self, True))

    def pause(self):
        if self._start_time is not None:
            self._rest_of_time = self.get_rest()
            self._stop()

    def reset(self):
        self._stop()
        self._rest_of_time = self.max_time

    def _stop(self):
        if self._start_time is None:
            return

        self._timer.stop()
        self._start_time = None
        self.on_change_run_status.emit(OnChangeRunStatusSignalArgs(self, False))

    def _tick(self):
        current_rest = self.get_rest()
        self.on_tick.emit(OnTickSignalArgs(sender=self, rest=current_rest))

        if current_rest <= 0:
            self._timer.stop()
            self.on_end.emit(OnEndSignalArgs(sender=self))
