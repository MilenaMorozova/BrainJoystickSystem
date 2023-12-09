from PyQt6.QtWidgets import QWidget, QFileDialog

from widgets.base.base_button import BaseButton


class SelectPackButton(BaseButton):
    title = "Выбрать пакет"

    def __init__(self, parent: QWidget):
        super().__init__(parent)

    def click_handler(self):
        path, _ = QFileDialog.getOpenFileName(self, caption="Выбор пакета", filter="SiGame пакеты (*.siq)")
        if path:
            self._store.game.state.load_pack_async(path)
