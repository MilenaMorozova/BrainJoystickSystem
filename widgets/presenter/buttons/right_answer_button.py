from PyQt6.QtWidgets import QWidget

from widgets.base.base_button import BaseButton


class RightAnswerButton(BaseButton):
    title = "Правильный ответ"

    def __init__(self, parent: QWidget):
        super().__init__(parent)

    def click_handler(self):
        self._locator.game.state.right_answer()
