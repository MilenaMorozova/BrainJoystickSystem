from PyQt6.QtWidgets import QPushButton

from state import State, StatusEnum, OnChangeStatusSignalArgs

BUTTON_CSS  = """
    min-width: 200px;
    max-width: 200px;
    min-height: 80px;
    max-height: 80px;
    font-size: 26px;
    border-radius: 35px;
    color: white;
    background-color: #0097F5;
"""


class ButtonsPanel:

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.__state = State.get_state()
        self.__state.on_change_status.connect(self._change_status_handler)

        self.play_button = QPushButton("Начать", parent)
        self.play_button.setStyleSheet(BUTTON_CSS)
        self.play_button.move(20, 20)
        self.play_button.clicked.connect(self.__click_to_start_pause_button)

        self.reset_button = QPushButton("Сбросить", parent)
        self.reset_button.setStyleSheet(BUTTON_CSS)
        self.reset_button.clicked.connect(self.__on_click_reset_button)

        parent.on_resize.connect(lambda args: self.update())
        self.update()

    def _change_status_handler(self, args: OnChangeStatusSignalArgs):
        match args.new_status:
            case StatusEnum.STOPPED:
                self.play_button.setText("Начать")
            case StatusEnum.STARTED:
                self.play_button.setText("Пауза")
            case StatusEnum.PAUSED:
                self.play_button.setText("Продолжить")

    def __click_to_start_pause_button(self):
        match self.__state.status:
            case StatusEnum.STOPPED:
                self.__state.status = StatusEnum.STARTED
            case StatusEnum.STARTED:
                self.__state.status = StatusEnum.PAUSED
            case StatusEnum.PAUSED:
                self.__state.status = StatusEnum.STARTED

    def __on_click_reset_button(self):
        self.__state.status = StatusEnum.STOPPED

    def update(self):
        self.reset_button.move(self.parent.width() - 220, 20)

