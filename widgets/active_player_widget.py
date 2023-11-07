from dataclasses import dataclass
from typing import Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QLabel

from helpers.signals import SignalArgs
from player import Player, OnChangeNameSignalArgs
from question_timer import QuestionTimer
from state import State, StatusEnum, OnChangeStatusSignalArgs

STYLE = """
    color: #FFFFFF;
    font-size: 64px;
"""


@dataclass
class OnPlayerClickSignalArgs(SignalArgs):
    player: Player


class ActivePlayerWidget(QLabel):
    # pyqtSignal(OnPlayerClickSignalArgs)
    on_player_click = pyqtSignal(object)

    def __init__(self):
        super().__init__()

        self.__active_player: Optional[Player] = None

        self.setStyleSheet(STYLE)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.on_player_click.connect(self._on_player_click_handler)

        self.__state = State.get_state()
        self.__state.on_change_status.connect(self._change_status_handler)

        self.timer = QuestionTimer(on_tick=self.on_tick)
        self.setText("Нажмите начать")

    def _change_status_handler(self, args: OnChangeStatusSignalArgs):
        if args.new_status != StatusEnum.PAUSED:
            self.active_player = None
        else:
            if self.active_player is None:
                self.setText("Пауза")

        if args.new_status == StatusEnum.STOPPED:
            self.setText("Нажмите начать")

    @property
    def active_player(self) -> Optional[Player]:
        return self.__active_player

    @active_player.setter
    def active_player(self, player: Optional[Player]):
        if self.__active_player is not None:
            self.__active_player.signals.on_change_name.disconnect(self._on_change_active_player_name_handler)
        self.__active_player = player
        if player is not None:
            player.signals.on_change_name.connect(self._on_change_active_player_name_handler)
            self.setText(player.name)
            self.__state.status = StatusEnum.PAUSED

    def _on_player_click_handler(self, args: OnPlayerClickSignalArgs):
        if self.active_player is None:
            if self.__state.status == StatusEnum.STARTED:
                self.active_player = args.player

    def on_tick(self, rest_of_question_time: float):
        self.setText(str(int(rest_of_question_time)))

    def _on_change_active_player_name_handler(self, args: OnChangeNameSignalArgs):
        self.setText(args.new_name)
