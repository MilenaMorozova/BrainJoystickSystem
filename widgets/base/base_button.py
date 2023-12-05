from typing import Union

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QPushButton, QWidget

from helpers.signal import Signal
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


class BaseButton(QPushButton):
    title = ""

    def __init__(self, parent: QWidget):
        super().__init__(self.title, parent)
        self.setStyleSheet(BUTTON_CSS)
        self.clicked.connect(self.click_handler)

        self._store = Store.get()
        self._update_on(self._store.game.on_change_state)
        self.update_visibility()

    def click_handler(self):
        raise NotImplementedError

    def change_state_handler(self, args: OnChangeStateSignalArgs):
        self.update_visibility()

    def is_visible(self) -> bool:
        return True

    def update_visibility(self):
        if self.is_visible():
            self.show()
        else:
            self.hide()

    def _update_on(self, signal: Union[pyqtSignal, Signal]):
        signal.connect(self.change_state_handler)
