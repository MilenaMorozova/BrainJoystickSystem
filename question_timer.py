from datetime import datetime
from typing import Callable

from PyQt6.QtCore import QTimer

from state import State, StatusEnum


class QuestionTimer:
    TICK_TIME = 100
    TIMER_TIME = 10  # secs

    def __init__(self, on_tick: Callable[[float], None]):
        self.start_time = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.rest_of_question_time = QuestionTimer.TIMER_TIME

        self.__state = State.get_state()
        self.__state.on_change_status.connect(self.change_status_handler)

        self.on_tick = on_tick

    def change_status_handler(self, status: StatusEnum):
        if status == StatusEnum.STARTED:
            self.start_time = datetime.now()
            self.timer.start(self.TICK_TIME)

        if status == StatusEnum.PAUSED:
            self.rest_of_question_time = self.get_current_rest_of_question_time()
            self.timer.stop()

        if status == StatusEnum.STOPPED:
            self.rest_of_question_time = QuestionTimer.TIMER_TIME
            self.timer.stop()

    def tick(self):
        current_rest_of_question_time = self.get_current_rest_of_question_time()
        self.on_tick(current_rest_of_question_time)

        if current_rest_of_question_time <= 0:
            self.__state.status = StatusEnum.STOPPED

    def get_current_rest_of_question_time(self) -> float:
        return self.rest_of_question_time - (datetime.now() - self.start_time).total_seconds()
