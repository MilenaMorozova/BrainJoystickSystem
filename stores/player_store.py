import random
from dataclasses import dataclass
from typing import List, Optional

from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtGui import QColor

from helpers.signals import SignalArgs
from player import Player


COLORS = [
    QColor('#F1495C'),  # pink
    QColor('#F69A39'),  # orange
    QColor('#F9DE27'),  # yellow
    QColor('#75BC6A'),  # green
    QColor('#5891F6'),  # blue
    QColor('#BA75DA'),  # purple
]


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

    def _get_new_color(self) -> QColor:
        def color_is_free(color: QColor) -> bool:
            return not any([i.color == color for i in self._players])

        pos_colors = list(filter(color_is_free, COLORS))
        if not pos_colors:
            pos_colors = COLORS
        return random.choice(pos_colors)

    def create_player(self, joystick_id: int):
        new_player = Player(f"Имя {len(self._players) + 1}", joystick_id, self._get_new_color())
        self._players.append(new_player)
        self.on_add_player.emit(OnAddPlayerSignalArgs(sender=self, player=new_player))

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
                raise Exception(f"Multiple players with a joystick №{joystick_id}")
