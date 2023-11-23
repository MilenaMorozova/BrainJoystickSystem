from typing import Iterator, Union, Optional
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from packs.loader import Loader
from packs.pack import Pack
from packs.question import Question
from packs.round import Round
from packs.steps.audio_step import AudioStep
from packs.steps.image_step import ImageStep
from packs.steps.text_step import TextStep
from packs.steps.video_step import VideoStep
from packs.theme import Theme


class Parser:
    NAMESPACE = 'http://vladimirkhil.com/ygpackage3.0.xsd'
    TYPE2STEP = {
        None: TextStep,
        'say': TextStep,
        'image': ImageStep,
        'video': VideoStep,
        'voice': AudioStep,
    }

    def __init__(self, path: str):
        self.path = path
        self.loader = Loader(self.path)
        self.content: str = ''
        self.tree: Optional[Element] = None

    def load(self):
        self.loader.load()
        self.content = self.loader.get_content()
        self.tree = ElementTree.fromstring(self.content)

    def iter(self, root: Element, tag: str) -> Iterator[Element]:
        return root.iter('{' + self.NAMESPACE + '}' + tag)

    def find(self, root: Element, tag: str) -> Element:
        return next(root.iter('{' + self.NAMESPACE + '}' + tag))

    def get_pack(self) -> Pack:
        tags = ' '.join([i.text for i in self.iter(self.tree, 'tag')])
        rounds = [self._parse_round(i) for i in self.iter(self.tree, 'round')]

        return Pack(
            name=self.tree.get('name'),
            version=self.tree.get('version', '3'),
            restriction=self.tree.get('restriction', ''),
            created=self.tree.get('date', ''),
            tags=tags,
            rounds=rounds,
        )

    def _parse_round(self, item: Element) -> Round:
        themes = [self._parse_theme(i) for i in self.iter(item, 'theme')]
        return Round(
            name=item.get('name'),
            themes=themes,
            is_final=item.get('type') == 'final'
        )

    def _parse_theme(self, item: Element) -> Theme:
        questions = [self._parse_question(i) for i in self.iter(item, 'question')]
        return Theme(
            name=item.get('name'),
            questions=questions,
        )

    def _parse_question(self, item: Element) -> Question:
        before = []
        after = []
        marked = False
        for atom in self.iter(item, 'atom'):
            atom_type = atom.get('type')
            if atom_type == 'marker':
                marked = True
            else:
                step = self.TYPE2STEP[atom_type](atom.text, self.loader)
                if marked:
                    after.append(step)
                else:
                    before.append(step)

        return Question(
            steps_before=before,
            steps_after=after,
            answer=self.find(item, 'answer').text,
            price=item.get('price', 0)
        )
