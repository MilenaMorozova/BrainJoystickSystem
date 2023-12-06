from dataclasses import dataclass
from typing import Optional

from PyQt6.QtCore import QObject, pyqtSignal

from helpers.signals import SignalArgs
from packs.pack import Pack
from player import Player
from states.base_state import BaseState


@dataclass
class OnChangeActivePlayerSignalArgs(SignalArgs):
    old_player: Optional[Player]
    new_player: Optional[Player]


@dataclass
class OnChangeStateSignalArgs(SignalArgs):
    new_state: BaseState
    old_state: BaseState


@dataclass
class OnChangePackSignalArgs(SignalArgs):
    new: Optional[Pack]
    old: Optional[Pack]


class GameStore(QObject):
    on_change_active_player = pyqtSignal(OnChangeActivePlayerSignalArgs)
    on_change_state = pyqtSignal(OnChangeStateSignalArgs)
    on_change_pack = pyqtSignal(OnChangePackSignalArgs)

    def __init__(self):
        super().__init__()
        self._active_player: Optional[Player] = None
        self._state: Optional[BaseState] = None
        self._pack: Optional[Pack] = None

    @property
    def active_player(self) -> Optional[Player]:
        return self._active_player

    @active_player.setter
    def active_player(self, value: Optional[Player]):
        if self._active_player == value:
            return

        old_active_player = self._active_player
        self._active_player = value
        self.on_change_active_player.emit(
            OnChangeActivePlayerSignalArgs(
                sender=self,
                old_player=old_active_player,
                new_player=value
            ))

    @property
    def state(self) -> BaseState:
        return self._state

    @state.setter
    def state(self, value: BaseState):
        if self._state == value:
            return

        old_state = self._state
        self._state = value
        if old_state:
            old_state.on_exit()
        value.on_enter()
        self.on_change_state.emit(
            OnChangeStateSignalArgs(sender=self, old_state=old_state, new_state=value)
        )

    @property
    def pack(self) -> Optional[Pack]:
        return self._pack

    @pack.setter
    def pack(self, value: Optional[Pack]):
        old_pack = self._pack
        self._pack = value
        self.on_change_pack.emit(
            OnChangePackSignalArgs(sender=self, old=old_pack, new=value)
        )
