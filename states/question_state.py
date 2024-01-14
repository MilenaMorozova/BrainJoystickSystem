from animations.show_answer_animation import ShowAnswerAnimation
from enums.joystick_button_enum import JoystickButton
from enums.status_enum import StatusEnum
from helpers.timer import OnEndSignalArgs
from services.joystick_input import OnPlayerClickSignalArgs
from states.state_with_service_locator import StateWithServiceLocator


class QuestionState(StateWithServiceLocator):
    status = StatusEnum.QUESTION

    def on_enter(self):
        self.locator.question_timer.start()
        self.locator.input.on_player_click.connect(self._on_player_click_handler)
        self.locator.question_timer.on_end.connect(self._on_timer_end)

    def on_exit(self):
        self.locator.question_timer.pause()
        self.locator.input.on_player_click.disconnect(self._on_player_click_handler)
        self.locator.question_timer.on_end.disconnect(self._on_timer_end)

    def _on_timer_end(self, args: OnEndSignalArgs):
        question = self.locator.game.selected_question
        question.is_answered = True
        self.show_answer_animation = ShowAnswerAnimation(question)
        self._set_next_state_after_animation(StatusEnum.CHOICE_QUESTION, self.show_answer_animation)

    def _on_player_click_handler(self, args: OnPlayerClickSignalArgs):
        if (
                args.key == JoystickButton.A
                and self.locator.game.active_player is None
                and args.player not in self.locator.game.players_who_answered
        ):
            self.locator.game.active_player = args.player
            self._set_next_state(StatusEnum.PLAYER_ANSWER)
