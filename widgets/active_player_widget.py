from typing import Optional

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QLabel

from player import Player


class ActivePlayerWidget(QLabel):
    on_player_click = pyqtSignal(Player)

    def __init__(self):
        super().__init__()
        self.__active_player: Optional[Player] = None
        self.setText("Ждём кликов")
        self.setStyleSheet("background-color: #000000; color: #FFFFFF;")
        self.on_player_click.connect(self.player_click)

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

    def player_click(self, player: Player):
        if self.active_player is None:
            self.active_player = player
