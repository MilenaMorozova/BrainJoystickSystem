from dataclasses import dataclass
from typing import Optional

from PyQt6.QtCore import pyqtSignal, QObject

from enums.joystick_button_enum import JoystickButton
from helpers.signals import SignalArgs

from services.joystick_event_handler import JoystickDownEvent, JoystickEventHandler
from player import Player
from services.player_store import PlayerStore


@dataclass
class OnPlayerClickSignalArgs(SignalArgs):
    player: Player
    key: JoystickButton


@dataclass
class OnUnknownPlayerClickSignalArgs(SignalArgs):
    key: JoystickButton
    joystick_id: int


class JoystickInput(QObject):
    on_player_click = pyqtSignal(OnPlayerClickSignalArgs)
    on_unknown_player_click = pyqtSignal(OnUnknownPlayerClickSignalArgs)

    def __init__(self, player_store: PlayerStore):
        super().__init__()
        self._players = player_store
        self._joystick_event_handler: Optional[JoystickEventHandler] = None

    def key_joystick_event(self, key: JoystickDownEvent) -> None:
        player = self._players.get_player_by_joystick_id(key.joystick_id)
        if player:
            self.on_player_click.emit(
                OnPlayerClickSignalArgs(sender=self, player=player, key=key.button_id)
            )
        else:
            self.on_unknown_player_click.emit(
                OnUnknownPlayerClickSignalArgs(sender=self, key=key.button_id, joystick_id=key.joystick_id)
            )

    def start(self):
        self._joystick_event_handler = JoystickEventHandler(self.key_joystick_event)
        self._joystick_event_handler.start()
