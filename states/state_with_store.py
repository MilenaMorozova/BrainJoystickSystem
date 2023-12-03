from typing import Dict, Type, Optional

from animations.animation import Animation, OnEndAnimationSignalArgs
from enums.status_enum import StatusEnum
from states.base_state import BaseState
from stores.store import Store


_STATES: Dict[StatusEnum, Type[BaseState]] = {}


class StateWithStore(BaseState):
    def __init__(self):
        self.store = Store.get()
        self.__status_after_animation: Optional[StatusEnum] = None

    @staticmethod
    def _get_state_type(status: StatusEnum) -> Type[BaseState]:
        global _STATES
        if status in _STATES:
            return _STATES[status]
        else:
            raise Exception(f"Status = {status.name} not registered, pls add new Status to {init_all_states.__name__}")

    def _set_next_state(self, status: StatusEnum):
        state_type = self._get_state_type(status)
        self.store.game.state = state_type()

    def _set_next_state_after_animation(self, status: StatusEnum, animation: Animation):
        self._set_next_state(StatusEnum.ANIMATION)
        self.__status_after_animation = status
        animation.on_end.connect(self.on_end_animation)
        animation.start()

    def on_end_animation(self, args: OnEndAnimationSignalArgs):
        args.sender.on_end.disconnect(self.on_end_animation)
        self._set_next_state(self.__status_after_animation)
        self.__status_after_animation = None


def init_all_states():
    from states.pause_state import PauseState
    from states.player_answer_state import PlayerAnswerState
    from states.run_state import RunState
    from states.lobby_state import LobbyState
    from states.animation_state import AnimationState
    from states.choice_question_state import ChoiceQuestionState
    global _STATES

    _STATES = {
        StatusEnum.PAUSE: PauseState,
        StatusEnum.PLAYER_ANSWER: PlayerAnswerState,
        StatusEnum.RUN: RunState,
        StatusEnum.LOBBY: LobbyState,
        StatusEnum.ANIMATION: AnimationState,
        StatusEnum.CHOICE_QUESTION: ChoiceQuestionState,
    }
