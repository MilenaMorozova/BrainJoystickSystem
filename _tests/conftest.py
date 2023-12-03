import pytest
from pathlib import Path

from settings import TEST_RESOURCES_PATH
from states.state_with_store import init_all_states
from stores.store import Store


@pytest.fixture(scope='session', autouse=True)
def init_all_states_fixture():
    init_all_states()


@pytest.fixture()
def mocked_store() -> Store:
    mock = Store()
    Store._instance = mock

    return mock


def _get_filepath(request) -> str:
    filename = request.node.nodeid.replace('_tests/', '').replace('/', '__').replace('::', '__').replace('.py', '')
    mask = f'{filename}.*'
    files = [str(f) for f in Path(TEST_RESOURCES_PATH).glob(mask)]
    if len(files) == 0:
        raise RuntimeError(f"Not found file for test {request.node.nodeid}")
    elif len(files) > 1:
        raise RuntimeError(f"For test {request.node.nodeid} found more than 1 file")

    return files[0]


@pytest.fixture()
def test_filepath(request) -> str:
    return _get_filepath(request)


@pytest.fixture()
def test_file_content(request) -> bytes:
    with open(_get_filepath(request), 'rb') as file:
        return file.read()