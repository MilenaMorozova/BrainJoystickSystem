from PyQt6.QtWidgets import QWidget

from enums.status_enum import StatusEnum
from widgets.base.base_button import BaseButton


class PlayButton(BaseButton):
    title = "Начать"

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._update_on(self._store.game.on_change_pack)

    def click_handler(self):
        self._store.game.state.on_click_play()

    def is_visible(self) -> bool:
        return (self._store.game.state.status == StatusEnum.LOBBY and
                self._store.game.pack is not None)
