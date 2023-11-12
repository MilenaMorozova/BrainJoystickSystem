from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel

from enums.status_enum import StatusEnum
from player import OnChangeNameSignalArgs
from helpers.timer import OnTickSignalArgs
from stores.game_store import OnChangeStateSignalArgs, OnChangeActivePlayerSignalArgs
from stores.store import Store

STYLE = """
    color: #FFFFFF;
    font-size: 64px;
"""


class CentralWidget(QLabel):
    def __init__(self):
        super().__init__()

        self.setStyleSheet(STYLE)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        store = Store.get()
        self.game = store.game
        self.question_timer = store.question_timer

        self.game.on_change_state.connect(self._change_status_handler)
        self.question_timer.on_tick.connect(self._on_question_timer_tick)

        self.setText("Нажмите начать")

    def _change_status_handler(self, args: OnChangeStateSignalArgs):
        match args.new_state.status:
            case StatusEnum.PAUSE:
                self.setText("Пауза")
            case StatusEnum.PLAYER_ANSWER:
                self.game.active_player.on_change_name.connect(self._on_change_active_player_name_handler)
                self.game.on_change_active_player.connect(self._unsubscribe_on_change_active_player)
                self.setText(self.game.active_player.name)
            case StatusEnum.STOP:
                self.setText("Нажмите начать")
            case StatusEnum.RUN:
                self.setText(str(int(self.question_timer.get_rest())))

    def _unsubscribe_on_change_active_player(self, args: OnChangeActivePlayerSignalArgs):
        args.old_player.on_change_name.disconnect(self._on_change_active_player_name_handler)
        self.game.on_change_active_player.disconnect(self._unsubscribe_on_change_active_player)

    def _on_question_timer_tick(self, args: OnTickSignalArgs):
        self.setText(str(int(args.rest)))

    def _on_change_active_player_name_handler(self, args: OnChangeNameSignalArgs):
        self.setText(args.new_name)
