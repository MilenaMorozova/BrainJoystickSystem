from PyQt6.QtWidgets import QPushButton, QWidget

from services.service_locator import ServiceLocator

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

        self._locator = ServiceLocator.get()

    def click_handler(self):
        raise NotImplementedError
