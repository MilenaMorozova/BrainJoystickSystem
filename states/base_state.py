from enums.status_enum import StatusEnum


class BaseState:
    status = StatusEnum.RUN

    @classmethod
    def is_stop(cls) -> bool:
        return cls.status == StatusEnum.STOP

    @classmethod
    def is_pause(cls) -> bool:
        return cls.status == StatusEnum.PAUSE

    @classmethod
    def is_run(cls) -> bool:
        return cls.status == StatusEnum.RUN

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
