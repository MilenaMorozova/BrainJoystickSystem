from typing import Optional

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QLabel

from player import Player
from question_timer import QuestionTimer
from state import State, StatusEnum


class ActivePlayerWidget(QLabel):
    on_player_click = pyqtSignal(Player)

    def __init__(self):
        super().__init__()

        self.__active_player: Optional[Player] = None
        self.setStyleSheet("background-color: #000000; color: #FFFFFF;")
        self.on_player_click.connect(self.player_click)

        self.__state = State.get_state()
        self.__state.on_change_status.connect(self.change_status_handler)

        self.timer = QuestionTimer(on_tick=self.on_tick)
        self.setText("Нажмите начать")

    def change_status_handler(self, status: StatusEnum):
        if status != StatusEnum.PAUSED:
            self.active_player = None
        else:
            if self.active_player is None:
                self.setText("Пауза")

        if status == StatusEnum.STOPPED:
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

    def on_tick(self, rest_of_question_time: float):
        self.setText(str(int(rest_of_question_time)))
