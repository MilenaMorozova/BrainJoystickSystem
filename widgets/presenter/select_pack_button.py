from threading import Thread

from PyQt6.QtWidgets import QWidget, QFileDialog

from enums.status_enum import StatusEnum
from packs.parser import Parser
from widgets.base.base_button import BaseButton


class SelectPackButton(BaseButton):
    title = "Выбрать пакет"

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._update_on(self._store.game.on_change_pack)

    def load_pack_async(self, path: str):
        def func():
            parser = Parser(path)
            parser.load()
            self._store.game.pack = parser.get_pack()

        thread = Thread(target=func)
        thread.start()

    def click_handler(self):
        path, _ = QFileDialog.getOpenFileName(self, caption="Выбор пакета", filter="SiGame пакеты (*.siq)")
        if path:
            self.load_pack_async(path)

    def is_visible(self) -> bool:
        return (self._store.game.state.status == StatusEnum.LOBBY and
                self._store.game.pack is None)
