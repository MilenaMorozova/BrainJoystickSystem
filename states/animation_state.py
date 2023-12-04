from enums.status_enum import StatusEnum
from states.state_with_store import StateWithStore


class AnimationState(StateWithStore):
    status = StatusEnum.ANIMATION

    def __init__(self):
        super().__init__()
