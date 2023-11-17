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

    def _change_status_handler(self, args: OnChangeStateSignalArgs):
        match args.new_state.status:
            case StatusEnum.LOBBY:
                self.play_button.setText("Начать")
                self.play_button.show()
            case StatusEnum.WAIT_ANIMATION:
                self.play_button.hide()
            case StatusEnum.CHOICE_QUESTION:
                self.play_button.hide()
            case _:
                raise Exception(f"Unhandled case status = {args.new_state.status.name}")

    def _on_click_play_handler(self):
        self._game.state.on_click_play()
