from typing import Optional

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QLabel

from player import Player
from question_timer import QuestionTimer
from state import State, StatusEnum

STYLE = """
    color: #FFFFFF;
    font-size: 64px;
"""


class ActivePlayerWidget(QLabel):
    on_player_click = pyqtSignal(Player)

    def __init__(self):
        super().__init__()

        self.__active_player: Optional[Player] = None

        self.setStyleSheet(STYLE)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

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
        if self.__active_player is not None:
            self.__active_player.signals.on_change_name.disconnect(self.change_active_player_name)
        self.__active_player = player
        if player is not None:
            player.signals.on_change_name.connect(self.change_active_player_name)
            self.setText(player.name)
            self.__state.status = StatusEnum.PAUSED

    def player_click(self, player: Player):
        if self.active_player is None:
            if self.__state.status == StatusEnum.STARTED:
                self.active_player = player

    def on_tick(self, rest_of_question_time: float):
        self.setText(str(int(rest_of_question_time)))

    def change_active_player_name(self, old_name: str, new_name: str):
        self.setText(new_name)
