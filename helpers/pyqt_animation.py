from PyQt6.QtCore import QSequentialAnimationGroup, pyqtSignal, QPauseAnimation


class SequentialAnimationGroupWithStarted(QSequentialAnimationGroup):
    started = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.start_animation = QPauseAnimation()
        self.start_animation.setDuration(0)
        self.start_animation.finished.connect(lambda: self.started.emit())
        self.addAnimation(self.start_animation)
