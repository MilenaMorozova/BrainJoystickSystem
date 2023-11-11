from dataclasses import dataclass

from PyQt6.QtCore import pyqtSignal, QObject

from enums.joystick_button_enum import JoystickButton
from helpers.signals import SignalArgs

from joystick_controller import JoystickDownEvent, JoystickController
from player import Player
from stores.player_store import PlayerStore


@dataclass
class OnPlayerClickSignalArgs(SignalArgs):
    player: Player
    key: JoystickButton


@dataclass
class OnNotPlayerClickSignalArgs(SignalArgs):
    key: JoystickButton
    joystick_id: int


class JoystickInput(QObject):
    on_player_click = pyqtSignal(OnPlayerClickSignalArgs)
    on_not_player_click = pyqtSignal(OnNotPlayerClickSignalArgs)

    def __init__(self, player_store: PlayerStore):
        super().__init__()
        self._players = player_store
        self._joystick_controller = JoystickController(self.key_joystick_event)
        self._joystick_controller.start()

    def key_joystick_event(self, key: JoystickDownEvent) -> None:
        # start button - connect joystick
        player = self._players.get_player_by_joystick_id(key.joystick_id)
        if player:
            self.on_player_click.emit(
                OnPlayerClickSignalArgs(sender=self, player=player, key=key.button_id)
            )
        else:
            self.on_not_player_click.emit(
                OnNotPlayerClickSignalArgs(sender=self, key=key.button_id, joystick_id=key.joystick_id)
            )
