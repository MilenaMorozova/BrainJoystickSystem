from unittest.mock import MagicMock

from packs.pack import Pack
from packs.parser import Parser
from packs.question import Question
from packs.round import Round
from packs.steps.image_step import ImageStep
from packs.steps.text_step import TextStep
from packs.steps.video_step import VideoStep
from packs.theme import Theme

TEST_PACK = Pack(
    name='test_name',
    version='4',
    created='01.01.2023',
    restriction='18+',
    tags='tag1 tag2',
    rounds=[
        Round(
            name='round1',
            themes=[
                Theme(
                    name='theme1',
                    questions=[
                        Question(
                            steps_before=[
                                TextStep('text1', None),
                                ImageStep('path1', None)
                            ],
                            steps_after=[ImageStep('path2', None)],
                            answer='answer1',
                            price=100
                        )
                    ]
                )
            ]
        ),
        Round(
            name='round2',
            themes=[
                Theme(
                    name='theme2',
                    questions=[
                        Question(
                            steps_before=[
                                TextStep('text2', None),
                                VideoStep('path3', None)
                            ],
                            steps_after=[],
                            answer='answer2',
                            price=0
                        )
                    ]
                )
            ]
        )
    ]
)


def test_get_pack(test_file_content):
    loader_mock = MagicMock(get_content=lambda: test_file_content)
    parser = Parser('path')
    parser.loader = loader_mock
    parser.load()
    pack = parser.get_pack()

    assert pack == TEST_PACK
