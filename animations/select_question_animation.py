from animations.animation import Animation
from packs.question import Question


class SelectQuestionAnimation(Animation):
    def __init__(self, question: Question):
        super().__init__()
        self.question = question
        self.selected_question_collapse_animation = None
        self.expand_animation = None
        self.question_animation = None

        self.selected_question_cell = self.main_window.select_question_widget.get_cell_by_question(self.question)
        self.selected_question_growing_animation = self.selected_question_cell.get_growing_animation()

    def start_show_question_animation(self):
        self.question_animation = self.main_window.answer_to_question_widget.get_show_question_animation(self.question)
        self.question_animation.finished.connect(self._emit_on_end)
        self.question_animation.start()

    def start_expand_animation(self):
        self.selected_question_cell.mark_as_answered()
        self.main_window.select_question_widget.hide()
        self.main_window.answer_to_question_widget.show()
        self.main_window.answer_to_question_widget.hide_all()

        self.expand_animation = self.main_window.answer_to_question_widget.get_expand_animation()
        self.expand_animation.finished.connect(self.start_show_question_animation)
        self.expand_animation.start()

    def start_collapse_animation(self):
        self.selected_question_collapse_animation = self.selected_question_cell.get_collapse_animation()
        self.selected_question_collapse_animation.finished.connect(self.start_expand_animation)
        self.selected_question_collapse_animation.start()

    def start(self):
        self.selected_question_cell.raise_()
        self.selected_question_growing_animation.finished.connect(self.start_collapse_animation)
        self.selected_question_growing_animation.start()
