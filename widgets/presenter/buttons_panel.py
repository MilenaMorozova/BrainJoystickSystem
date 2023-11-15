from PyQt6.QtWidgets import QPushButton

from enums.status_enum import StatusEnum
from stores.game_store import OnChangeStateSignalArgs
from stores.store import Store

BUTTON_CSS = """
    min-width: 200px;
    max-width: 200px;
    min-height: 80px;
    max-height: 80px;
    font-size: 26px;
    border-radius: 35px;
    color: white;
    background-color: #0097F5;
"""


class ButtonsPanel:

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self._game = Store.get().game
        self._game.on_change_state.connect(self._change_status_handler)

        self.play_button = QPushButton("Начать", parent)
        self.play_button.setStyleSheet(BUTTON_CSS)
        self.play_button.move(20, 20)
        self.play_button.clicked.connect(self._on_click_play_handler)

        self.reset_button = QPushButton("Сбросить", parent)
        self.reset_button.setStyleSheet(BUTTON_CSS)
        self.reset_button.clicked.connect(self. _on_click_reset_handler)

        parent.on_resize.connect(lambda args: self.update())
        self.update()

    def _change_status_handler(self, args: OnChangeStateSignalArgs):
        match args.new_state.status:
            case StatusEnum.LOBBY:
                self.play_button.setText("Начать")
            case StatusEnum.RUN:
                self.play_button.setText("Пауза")
            case StatusEnum.PAUSE:
                self.play_button.setText("Продолжить")

    def update(self):
        self.reset_button.move(self.parent.width() - 220, 20)

    def _on_click_play_handler(self):
        self._game.state.on_click_play()

    def _on_click_reset_handler(self):
        self._game.state.on_click_reset()
