from animations.select_question_animation import SelectQuestionAnimation
from enums.status_enum import StatusEnum
from packs.question import Question
from states.state_with_service_locator import StateWithServiceLocator


class ChoiceQuestionState(StateWithServiceLocator):
    status = StatusEnum.CHOICE_QUESTION

    def __init__(self):
        super().__init__()
        self._select_question_animation = None

    def select_question(self, question: Question):
        self._select_question_animation = SelectQuestionAnimation(question)
        self._set_next_state_after_animation(StatusEnum.QUESTION, self._select_question_animation)
