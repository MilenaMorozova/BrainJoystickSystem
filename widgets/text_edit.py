from PyQt6.QtWidgets import QLineEdit


STYLE = """
    background-color: white;
    font-size: 20px;
    border: none;
"""


class TextEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(STYLE)
