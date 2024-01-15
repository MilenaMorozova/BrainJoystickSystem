from PyQt6.QtCore import QPropertyAnimation, Qt, pyqtProperty
from PyQt6.QtWidgets import QLabel

from services.service_locator import ServiceLocator

STYLE = """
    color: #FFFFFF;
    font-size: {font_size}px;
"""


class GameOverWidget(QLabel):
    def __init__(self):
        super().__init__()
        self._font_size = 64
        self._update_style()

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText("TEXT")

        self.player_store = ServiceLocator.get().player

    def _update_style(self):
        self.setStyleSheet(STYLE.format(font_size=self._font_size))

    @pyqtProperty(int)
    def font_size(self) -> int:
        return self._font_size

    @font_size.setter
    def font_size(self, value: int):
        self._font_size = value
        self._update_style()

    def get_text_growing_animation(self) -> QPropertyAnimation:
        text_growing = QPropertyAnimation(self, b'font_size', self)
        text_growing.setStartValue(0)
        text_growing.setEndValue(self._font_size)
        text_growing.setDuration(1000)
        return text_growing

    def update_text(self):
        leader = self.player_store.get_score_leader()
        if leader:
            self.setText(f"Победил {leader.name}!")
        else:
            self.setText("Победителя нет!")
