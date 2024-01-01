from enums.status_enum import StatusEnum


class BaseState:
    status: StatusEnum

    def on_enter(self):
        pass

    def on_exit(self):
        pass
