from unittest.mock import MagicMock

from enums.status_enum import StatusEnum
from states.lobby_state import LobbyState
from states.player_answer_state import PlayerAnswerState


class TestSetNextState:
    def test_that_state_changing(self, mocked_store):
        mocked_store.game.state = LobbyState()
        mocked_store.game.state._set_next_state(StatusEnum.PLAYER_ANSWER)

        assert isinstance(mocked_store.game.state, PlayerAnswerState)

    def test_call_on_enter(self, mocked_store, mocked_status):
        mocked_store.game.state = LobbyState()
        mocked_store.game.state._set_next_state(mocked_status)

        assert mocked_store.game.state.on_enter.called

    def test_call_on_exit(self, mocked_store):
        old_state = LobbyState()
        old_state.on_exit = MagicMock()
        mocked_store.game.state = old_state
        mocked_store.game.state._set_next_state(StatusEnum.PLAYER_ANSWER)

        assert old_state.on_exit.called
