from unittest.mock import MagicMock

from enums.joystick_button_enum import JoystickButton
from joystick_input import OnPlayerClickSignalArgs
from states.pause_state import PauseState
from states.player_answer_state import PlayerAnswerState
from states.run_state import RunState


def test_start_timer_on_enter(qtbot, mocked_store):
    state = RunState()
    mocked_store.question_timer.start()

    state.on_enter()
    first_time = mocked_store.question_timer.get_rest()
    qtbot.wait(200)
    second_time = mocked_store.question_timer.get_rest()

    assert first_time != second_time, "Timer is paused"


def test_click_to_play(mocked_store):
    pause_state = RunState()
    mocked_store.game.state = pause_state
    pause_state.on_click_play()
    assert isinstance(mocked_store.game.state, PauseState)


def test_player_click_a(mocked_store):
    pause_state = RunState()
    mocked_store.game.state = pause_state
    pause_state.on_enter()

    mock_player = MagicMock()

    mocked_store.input.on_player_click.emit(OnPlayerClickSignalArgs(
        sender=mocked_store.input,
        player=mock_player,
        key=JoystickButton.A
    ))

    assert isinstance(mocked_store.game.state, PlayerAnswerState)
    assert mocked_store.game.active_player == mock_player
