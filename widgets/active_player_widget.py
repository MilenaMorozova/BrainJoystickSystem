from typing import Optional

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QLabel

from player import Player
from state import State, StatusEnum


class ActivePlayerWidget(QLabel):
    on_player_click = pyqtSignal(Player)

    def __init__(self):
        super().__init__()
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

    @property
    def active_player(self) -> Optional[Player]:
        return self.__active_player

    @active_player.setter
    def active_player(self, player: Optional[Player]):
        self.__active_player = player
        if player is None:
            self.setText("Ждём кликов")
        else:
            self.setText(player.name)
            self.__state.status = StatusEnum.PAUSED

    def player_click(self, player: Player):
        if self.active_player is None:
            if self.__state.status == StatusEnum.STARTED:
                self.active_player = player
