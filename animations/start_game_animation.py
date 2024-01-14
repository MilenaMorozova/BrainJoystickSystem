from animations.animation import Animation


class StartGameAnimation(Animation):
    def __init__(self):
        super().__init__()
        self.text_reduction = self.main_window.lobby_central_widget.get_text_reduction_animation()
        self.text_reduction.finished.connect(self.on_end_text_reduction_animation)

    def on_end_text_reduction_animation(self):
        self.main_window.lobby_central_widget.hide()
        self.main_window.select_question_widget.show()
        self._emit_on_end()

    def start(self):
        self.text_reduction.start()
