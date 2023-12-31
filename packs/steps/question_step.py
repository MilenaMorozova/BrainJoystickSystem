from packs.loader import Loader


class QuestionStep:
    def __init__(self, content: str, loader: Loader):
        self.content = content
        self.loader = loader

    def get_result(self):
        raise NotImplemented()

    def get_filename(self) -> str:
        if not self.content.startswith('@'):
            raise AttributeError("content don't starting with ad")
        return self.content[1:]  # delete symbol ad

    def __str__(self):
        return self.content

    def __repr__(self):
        return str(self)

    def __eq__(self, other) -> bool:
        if not isinstance(other, QuestionStep):
            return False

        return self.content == other.content
