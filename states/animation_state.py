from enums.status_enum import StatusEnum
from states.state_with_service_locator import StateWithServiceLocator


class AnimationState(StateWithServiceLocator):
    status = StatusEnum.ANIMATION

    def __init__(self):
        super().__init__()
