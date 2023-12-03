from packs.loader import Loader


def test_get_content(test_filepath):
    loader = Loader(test_filepath)
    loader.load()
    content = loader.get_content()

    assert str(content, 'utf-8-sig') == 'test content'
