from animations.animation import Animation


class StartRoundAnimation(Animation):
    def __init__(self):
        super().__init__()
        self.grid_growing = self.main_window.select_question_widget.get_growing_animation()
        self.grid_growing.finished.connect(self._emit_on_end)

    def start(self):
        self.grid_growing.start()
