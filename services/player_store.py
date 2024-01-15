from dataclasses import dataclass
from typing import List, Optional, Set

from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtGui import QColor

from helpers.colors import COLORS
from helpers.signals import SignalArgs
from player import Player


@dataclass
class OnAddPlayerSignalArgs(SignalArgs):
    player: Player


@dataclass
class OnRemovePlayerSignalArgs(SignalArgs):
    player: Player


class PlayerStore(QObject):
    on_add_player = pyqtSignal(OnAddPlayerSignalArgs)
    on_remove_player = pyqtSignal(OnRemovePlayerSignalArgs)

    def __init__(self):
        super().__init__()
        self._players: List[Player] = []

    def color_is_used(self, color: QColor) -> bool:
        return any([i.color == color for i in self._players])

    def get_used_colors(self) -> List[QColor]:
        return list(filter(self.color_is_used, COLORS))

    def add_player(self, player: Player):
        self._players.append(player)
        self.on_add_player.emit(OnAddPlayerSignalArgs(sender=self, player=player))

    def remove_player(self, player: Player):
        self._players.remove(player)
        self.on_remove_player.emit(OnRemovePlayerSignalArgs(sender=self, player=player))

    def get_player_by_joystick_id(self, joystick_id: int) -> Optional[Player]:
        result = [i for i in self._players if i.joystick_id == joystick_id]
        match len(result):
            case 0:
                return None
            case 1:
                return result[0]
            case _:
                raise Exception(f"Multiple players with a joystick <{joystick_id}>")

    def get_count_of_players(self) -> int:
        return len(self._players)

    def get_score_leader(self) -> Optional[Player]:
        if self._players:
            return max(self._players, key=lambda x: x.score)
