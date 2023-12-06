from threading import Thread

from PyQt6.QtWidgets import QWidget, QFileDialog

from packs.parser import Parser
from widgets.base.base_button import BaseButton


class SelectPackButton(BaseButton):
    title = "Выбрать пакет"

    def __init__(self, parent: QWidget):
        super().__init__(parent)

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
