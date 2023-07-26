from PyQt6.QtWidgets import QHBoxLayout, QPushButton

from state import State, StatusEnum


class ButtonsPanel(QHBoxLayout):

    def __init__(self):
        super().__init__()

        self.__state = State.get_state()
        self.__state.on_change_status.connect(self.handle_change_status)

        self.play_button = QPushButton("Начать")
        self.play_button.setFixedWidth(100)
        self.play_button.clicked.connect(self.__click_to_start_pause_button)
        self.addWidget(self.play_button)

    def handle_change_status(self, status: StatusEnum):
        match status:
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
