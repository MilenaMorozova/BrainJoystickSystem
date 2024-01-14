from animations.animation import Animation
from packs.question import Question


class ShowAnswerAnimation(Animation):
    def __init__(self, question: Question):
        super().__init__()
        self.question = question

        self.answer_animation = self.main_window.answer_to_question_widget.get_show_answer_animation(self.question)
        self.answer_animation.finished.connect(self.on_end_show_answer_animation)

    def on_end_show_answer_animation(self):
        self.main_window.answer_to_question_widget.hide()
        self.main_window.select_question_widget.show()
        self._emit_on_end()

    def start(self):
        self.main_window.answer_to_question_widget.hide_all()
        self.answer_animation.start()
