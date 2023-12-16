from states.pause_state import PauseState
from states.run_state import RunState


def test_pause_on_enter(qtbot, mocked_locator):
    state = PauseState()
    mocked_locator.question_timer.start()

    state.on_enter()
    first_time = mocked_locator.question_timer.get_rest()
    qtbot.wait(200)
    second_time = mocked_locator.question_timer.get_rest()

    assert first_time == second_time, "Timer not paused"


def test_click_to_play(mocked_locator):
    pause_state = PauseState()
    mocked_locator.game.state = pause_state
    pause_state.on_click_play()
    assert isinstance(mocked_locator.game.state, RunState)
