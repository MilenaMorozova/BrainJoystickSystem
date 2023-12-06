from PyQt6.QtWidgets import QWidget

from widgets.base.base_button import BaseButton


class PlayButton(BaseButton):
    title = "Начать"

    def __init__(self, parent: QWidget):
        super().__init__(parent)

    def click_handler(self):
        self._store.game.state.on_click_play()
