from PyQt6.QtWidgets import QWidget

from widgets.base.base_button import BaseButton


class WrongAnswerButton(BaseButton):
    title = "Неправильный ответ"

    def __init__(self, parent: QWidget):
        super().__init__(parent)

    def click_handler(self):
        self._locator.game.state.wrong_answer()
