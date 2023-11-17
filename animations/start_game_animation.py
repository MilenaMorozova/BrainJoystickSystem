from PyQt6.QtCore import QPropertyAnimation

from animations.animation import Animation


class StartGameAnimation(Animation):
    def __init__(self):
        # TODO: Create norm animation
        super().__init__()
        self._value = 0
        self.main_animation = QPropertyAnimation(self, b'_value')
        self.main_animation.setDuration(1500)
