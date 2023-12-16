import random

from PyQt6.QtGui import QColor

from helpers.colors import COLORS
from player import Player
from services.player_store import PlayerStore


class PlayerGenerator:
    def __init__(self, player_store: PlayerStore):
        self._player_store = player_store

    def get_new_color(self) -> QColor:
        used_colors = self._player_store.get_used_colors()
        available_colors = [i for i in COLORS if i not in used_colors]
        if not available_colors:
            available_colors = COLORS

        return random.choice(available_colors)

    def get_new_player(self, joystick_id: int) -> Player:
        return Player(
            f"Имя {self._player_store.get_count_of_players() + 1}",
            joystick_id,
            self.get_new_color()
        )
