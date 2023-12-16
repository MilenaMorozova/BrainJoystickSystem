from enums.status_enum import StatusEnum
from states.state_with_service_locator import StateWithServiceLocator
from widgets.main_window import MainWindow


class PlayerAnswerState(StateWithServiceLocator):
    status = StatusEnum.PLAYER_ANSWER

    def __init__(self):
        super().__init__()
        self.question = self.locator.game.selected_question
        self.player = self.locator.game.active_player

    def on_enter(self):
        self.locator.question_timer.pause()

    def right_answer(self):
        self.player.score += self.question.price
        self.locator.game.answered_questions.append(self.question)
        self.locator.game.active_player = None
        self._set_next_state(StatusEnum.CHOICE_QUESTION)
        # TODO swap to show answer animation
        MainWindow.get().answer_to_question_widget.hide()
        MainWindow.get().select_question_widget.show()

    def wrong_answer(self):
        self.player.score -= self.question.price
        self.locator.game.active_player = None
        self._set_next_state(StatusEnum.QUESTION)
