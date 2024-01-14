from animations.show_answer_animation import ShowAnswerAnimation
from enums.status_enum import StatusEnum
from states.state_with_service_locator import StateWithServiceLocator


class PlayerAnswerState(StateWithServiceLocator):
    status = StatusEnum.PLAYER_ANSWER

    def __init__(self):
        super().__init__()
        self.question = self.locator.game.selected_question
        self.player = self.locator.game.active_player
        self.show_answer_animation = None

    def on_enter(self):
        self.locator.question_timer.pause()

    def right_answer(self):
        self.question.is_answered = True
        self.player.score += self.question.price
        self.locator.game.active_player = None
        self.show_answer_animation = ShowAnswerAnimation(self.question)
        self._set_next_state_after_animation(StatusEnum.CHOICE_QUESTION, self.show_answer_animation)

    def wrong_answer(self):
        self.player.score -= self.question.price
        self.locator.game.active_player = None
        self._set_next_state(StatusEnum.QUESTION)
