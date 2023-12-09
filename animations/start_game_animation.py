from animations.animation import Animation


class StartGameAnimation(Animation):
    def __init__(self):
        super().__init__()
        self.grid_growing = None
        self.text_reduction = None

    def start_grid_growing_animation(self):
        self.main_window.lobby_central_widget.hide()
        self.main_window.select_question_widget.show()

        self.grid_growing = self.main_window.select_question_widget.get_growing_animation()
        self.grid_growing.finished.connect(self._emit_on_end)
        self.grid_growing.start()

    def start(self):
        self.text_reduction = self.main_window.lobby_central_widget.get_text_reduction_animation()
        self.text_reduction.finished.connect(self.start_grid_growing_animation)
        self.text_reduction.start()
