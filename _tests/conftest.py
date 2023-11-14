import pytest

from states.state_with_store import init_all_states
from stores.store import Store


@pytest.fixture(scope='session', autouse=True)
def init_all_states_fixture():
    init_all_states()


@pytest.fixture()
def mocked_store():
    mock = Store()
    Store._instance = mock

    return mock
