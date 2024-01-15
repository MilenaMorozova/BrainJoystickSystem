from animations.animation import Animation


class GameOverAnimation(Animation):
    def __init__(self):
        super().__init__()
        self.text_growing = self.main_window.game_over_widget.get_text_growing_animation()
        self.text_growing.finished.connect(self._emit_on_end)

    def start(self):
        self.main_window.select_question_widget.hide()
        self.main_window.game_over_widget.update_text()
        self.main_window.game_over_widget.show()

        self.text_growing.start()
