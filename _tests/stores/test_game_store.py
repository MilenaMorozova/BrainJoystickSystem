from unittest.mock import MagicMock


def test_state_setter_call_on_enter(mocked_store):
    state_mock = MagicMock()
    mocked_store.game.state = state_mock

    assert state_mock.on_enter.call_count == 1


def test_state_setter_call_on_exit(mocked_store):
    state_mock = MagicMock()
    state_mock2 = MagicMock()
    mocked_store.game.state = state_mock
    mocked_store.game.state = state_mock2

    assert state_mock.on_exit.call_count == 1
