from PyQt6.QtCore import Qt, pyqtProperty, QPropertyAnimation
from PyQt6.QtWidgets import QLabel

from enums.status_enum import StatusEnum
from player import OnChangeNameSignalArgs
from helpers.timer import OnTickSignalArgs
from stores.game_store import OnChangeStateSignalArgs, OnChangeActivePlayerSignalArgs
from stores.store import Store

STYLE = """
    color: #FFFFFF;
    font-size: {font_size}px;
"""


class LobbyCentralWidget(QLabel):
    def __init__(self):
        super().__init__()
        self._font_size = 64
        self._update_style()

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        store = Store.get()
        self.game = store.game
        self.question_timer = store.question_timer

        self.game.on_change_state.connect(self._change_status_handler)
        self.question_timer.on_tick.connect(self._on_question_timer_tick)

        self.setText("Нажмите start для подключения")

    def _update_style(self):
        self.setStyleSheet(STYLE.format(font_size=self._font_size))

    def _change_status_handler(self, args: OnChangeStateSignalArgs):
        # TODO delete this logic
        match args.new_state.status:
            case StatusEnum.PAUSE:
                self.setText("Пауза")
            case StatusEnum.PLAYER_ANSWER:
                self.game.active_player.on_change_name.connect(self._on_change_active_player_name_handler)
                self.game.on_change_active_player.connect(self._unsubscribe_on_change_active_player)
                self.setText(self.game.active_player.name)
            case StatusEnum.LOBBY:
                self.setText("Нажмите start для подключения")
            case StatusEnum.RUN:
                self.setText(str(int(self.question_timer.get_rest())))
            case StatusEnum.CHOICE_QUESTION:
                self.setText("Выбор вопроса")

    def _unsubscribe_on_change_active_player(self, args: OnChangeActivePlayerSignalArgs):
        args.old_player.on_change_name.disconnect(self._on_change_active_player_name_handler)
        self.game.on_change_active_player.disconnect(self._unsubscribe_on_change_active_player)

    def _on_question_timer_tick(self, args: OnTickSignalArgs):
        self.setText(str(int(args.rest)))

    def _on_change_active_player_name_handler(self, args: OnChangeNameSignalArgs):
        self.setText(args.new_name)

    @pyqtProperty(int)
    def font_size(self) -> int:
        return self._font_size

    @font_size.setter
    def font_size(self, value: int):
        self._font_size = value
        self._update_style()

    def get_text_reduction_animation(self) -> QPropertyAnimation:
        text_reduction = QPropertyAnimation(self, b'font_size', self)
        text_reduction.setEndValue(0)
        text_reduction.setDuration(1000)
        return text_reduction
