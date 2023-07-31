from datetime import datetime
from typing import Optional

from PyQt6.QtCore import pyqtSignal, QTimer
from PyQt6.QtWidgets import QLabel

from player import Player
from state import State, StatusEnum


class ActivePlayerWidget(QLabel):
    on_player_click = pyqtSignal(Player)
    TICK_TIME = 100
    TIMER_TIME = 60  # secs

    def __init__(self):
        super().__init__()
        self.start_time = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.rest_of_question_time = ActivePlayerWidget.TIMER_TIME

        self.__active_player: Optional[Player] = None
        self.setText("Ждём кликов")
        self.setStyleSheet("background-color: #000000; color: #FFFFFF;")
        self.on_player_click.connect(self.player_click)

        self.__state = State.get_state()
        self.__state.on_change_status.connect(self.change_status_handler)

    def change_status_handler(self, status: StatusEnum):
        if status != StatusEnum.PAUSED:
            self.active_player = None
        else:
            if self.active_player is None:
                self.setText("Пауза")

        if status == StatusEnum.STARTED:
            self.start_time = datetime.now()
            self.timer.start(self.TICK_TIME)

        if status == StatusEnum.PAUSED:
            self.rest_of_question_time = self.get_current_rest_of_question_time()
            self.timer.stop()

        if status == StatusEnum.STOPPED:
            self.rest_of_question_time = ActivePlayerWidget.TIMER_TIME
            self.timer.stop()
            self.setText("Нажмите начать")

    @property
    def active_player(self) -> Optional[Player]:
        return self.__active_player

    @active_player.setter
    def active_player(self, player: Optional[Player]):
        self.__active_player = player
        if player is not None:
            self.setText(player.name)
            self.__state.status = StatusEnum.PAUSED

    def player_click(self, player: Player):
        if self.active_player is None:
            if self.__state.status == StatusEnum.STARTED:
                self.active_player = player

    def tick(self):
        self.setText(str(int(self.get_current_rest_of_question_time())))

    def get_current_rest_of_question_time(self) -> float:
        return self.rest_of_question_time - (datetime.now() - self.start_time).total_seconds()
