from enums.status_enum import StatusEnum
from states.state_with_store import StateWithStore


class ChoiceQuestionState(StateWithStore):
    status = StatusEnum.CHOICE_QUESTION
