from typing import List

import pytest
from PyQt6.QtGui import QColor

from helpers.colors import COLORS
from helpers.player_generator import PlayerGenerator
from player import Player
from services.player_store import PlayerStore


class PlayerStoreMock(PlayerStore):
    def __init__(self, used_colors: List[QColor] = None, count_players: int = 0):
        super().__init__()
        self.count_players = count_players
        self.used_colors = [] if used_colors is None else used_colors

    def get_used_colors(self) -> List[QColor]:
        return self.used_colors

    def get_count_of_players(self) -> int:
        return self.count_players


@pytest.mark.parametrize(
    "used,available",
    [
        ([[], COLORS]),
        ([COLORS[:-1], COLORS[-1:]]),
        (COLORS, COLORS)
    ],
    ids=[
            "empty colors",
            "any color is used",
            "all colors is used"
        ]
)
def test_get_new_color(used: List[QColor], available: List[QColor]):
    player_store_mock = PlayerStoreMock(used_colors=used)
    generator = PlayerGenerator(player_store_mock)
    new_color = generator.get_new_color()
    assert new_color in available


def test_get_new_player():
    player_store_mock = PlayerStoreMock(count_players=3, used_colors=COLORS[:-1])
    generator = PlayerGenerator(player_store_mock)
    joystick_id = 1234

    player = generator.get_new_player(joystick_id)
    assert isinstance(player, Player)
    assert player.name == "Имя 4"
    assert player.joystick_id == joystick_id
    assert player.color == COLORS[-1]
