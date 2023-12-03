from enum import IntEnum


class StatusEnum(IntEnum):
    LOBBY = 0
    PAUSE = 1
    RUN = 2
    PLAYER_ANSWER = 3
    ANIMATION = 4
    CHOICE_QUESTION = 5
