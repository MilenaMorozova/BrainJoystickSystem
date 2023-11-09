from enums.status_enum import StatusEnum


class State:
    status = StatusEnum.STARTED

    @classmethod
    def is_stopped(cls) -> bool:
        return cls.status == StatusEnum.STOPPED

    @classmethod
    def is_paused(cls) -> bool:
        return cls.status == StatusEnum.PAUSED

    @classmethod
    def is_started(cls) -> bool:
        return cls.status == StatusEnum.STARTED

    @classmethod
    def is_player_answer(cls) -> bool:
        return cls.status == StatusEnum.PLAYER_ANSWER

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def on_click_play(self):
        pass

    def on_click_reset(self):
        pass
