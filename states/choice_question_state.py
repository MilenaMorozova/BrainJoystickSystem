from animations.select_question_animation import SelectQuestionAnimation
from animations.start_round_animation import StartRoundAnimation
from enums.status_enum import StatusEnum
from packs.question import Question
from states.state_with_service_locator import StateWithServiceLocator


class ChoiceQuestionState(StateWithServiceLocator):
    status = StatusEnum.CHOICE_QUESTION

    def __init__(self):
        super().__init__()
        self._select_question_animation = None

    def on_enter(self):
        current_round = self.locator.game.round
        if not current_round or current_round.is_all_question_is_answered():
            self.locator.game.round_number += 1
            self._start_round_animation = StartRoundAnimation()
            self._set_next_state_after_animation(StatusEnum.CHOICE_QUESTION, self._start_round_animation)

    def select_question(self, question: Question):
        self.locator.game.selected_question = question
        self.locator.question_timer.reset()
        self.locator.game.players_who_answered.clear()

        self._select_question_animation = SelectQuestionAnimation(question)
        self._set_next_state_after_animation(StatusEnum.QUESTION, self._select_question_animation)
