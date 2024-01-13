from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

from services.game_store import OnChangeSelectedQuestionSignalArgs
from services.service_locator import ServiceLocator
from widgets.presenter.buttons.right_answer_button import RightAnswerButton
from widgets.presenter.buttons.wrong_answer_button import WrongAnswerButton


class PlayerAnswerPresenterWidget(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.main_layout = QVBoxLayout(self)

        self.right_answer_button = RightAnswerButton(self)
        self.wrong_answer_button = WrongAnswerButton(self)
        self.answer_label = QLabel(self)

        self.main_layout.addWidget(self.right_answer_button)
        self.main_layout.addWidget(self.wrong_answer_button)
        self.main_layout.addWidget(self.answer_label)

        ServiceLocator.get().game.on_change_selected_question.connect(self.on_change_selected_question)

    def on_change_selected_question(self, args: OnChangeSelectedQuestionSignalArgs):
        self.answer_label.setText(args.question.answer)
