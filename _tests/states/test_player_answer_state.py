from states.player_answer_state import PlayerAnswerState


def test_pause_on_enter(qtbot, mocked_locator):
    state = PlayerAnswerState()
    mocked_locator.question_timer.start()

    state.on_enter()
    first_time = mocked_locator.question_timer.get_rest()
    qtbot.wait(200)
    second_time = mocked_locator.question_timer.get_rest()

    assert first_time == second_time, "Timer not paused"
