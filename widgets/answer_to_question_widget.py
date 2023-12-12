from typing import List, Optional

from PyQt6.QtCore import QPropertyAnimation, QSize, QParallelAnimationGroup, QPoint, QSequentialAnimationGroup, \
    QPauseAnimation, Qt
from PyQt6.QtWidgets import QPushButton, QSizePolicy, QLabel, QVBoxLayout

from helpers.pyqt_animation import SequentialAnimationGroupWithStarted
from packs.question import Question
from packs.steps.audio_step import AudioStep
from packs.steps.image_step import ImageStep
from packs.steps.question_step import QuestionStep
from packs.steps.text_step import TextStep
from packs.steps.video_step import VideoStep
from widgets.select_question_widget import SELECT_QUESTION_GRID_CELL_CSS, BIG_QUESTION_MARGIN

ANSWER_TO_QUESTION_WIDGET_CSS = SELECT_QUESTION_GRID_CELL_CSS + f"""
    margin: {BIG_QUESTION_MARGIN[0]};
"""


class AnswerToQuestionWidget(QPushButton):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.setStyleSheet(ANSWER_TO_QUESTION_WIDGET_CSS)

        self.vbox_layout = QVBoxLayout(self)

        self.text_label = QLabel("TEXT", self)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.content_label = QLabel("IMAGE", self)
        self.content_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.vbox_layout.addWidget(self.text_label)
        self.vbox_layout.addWidget(self.content_label, 1)

        self.text_label.hide()
        self.content_label.hide()
        
    def get_expand_animation(self) -> QParallelAnimationGroup:
        duration = 300
        start_size = self.size() - QSize(self.size().width(), 0)
        start_pos = QPoint(self.size().width() // 2, 0)

        expand = QPropertyAnimation(self, b'size', self)
        expand.setStartValue(start_size)
        expand.setEndValue(self.size())
        expand.setDuration(duration)

        moving = QPropertyAnimation(self, b'pos', self)
        moving.setStartValue(start_pos)
        moving.setEndValue(QPoint())
        moving.setDuration(duration)

        animation_group = QParallelAnimationGroup(self)
        animation_group.addAnimation(expand)
        animation_group.addAnimation(moving)

        return animation_group

    def get_text_step_animation(self, step: TextStep) -> SequentialAnimationGroupWithStarted:
        def on_start():
            self.text_label.setText(step.get_result())
            self.text_label.show()

        animation_group = SequentialAnimationGroupWithStarted()
        animation_group.started.connect(on_start)

        pause_animation = QPauseAnimation(self)
        pause_animation.setDuration(5000)
        animation_group.addAnimation(pause_animation)

        return animation_group

    def get_image_step_animation(self, step: ImageStep) -> SequentialAnimationGroupWithStarted:
        # TODO: create another animation for image step
        def on_start():
            self.content_label.setText(f'Image {step.content}')
            self.content_label.show()

        animation_group = SequentialAnimationGroupWithStarted()
        animation_group.started.connect(on_start)

        pause_animation = QPauseAnimation(self)
        pause_animation.setDuration(5000)
        animation_group.addAnimation(pause_animation)

        return animation_group

    def get_video_step_animation(self, step: VideoStep) -> SequentialAnimationGroupWithStarted:
        # TODO: create another animation for step
        def on_start():
            self.content_label.setText(f'Video {step.content}')
            self.content_label.show()

        animation_group = SequentialAnimationGroupWithStarted()
        animation_group.started.connect(on_start)

        pause_animation = QPauseAnimation(self)
        pause_animation.setDuration(5000)
        animation_group.addAnimation(pause_animation)

        return animation_group

    def get_audio_step_animation(self, step: AudioStep) -> SequentialAnimationGroupWithStarted:
        # TODO: create another animation for step
        def on_start():
            self.content_label.setText(f'Audio {step.content}')
            self.content_label.show()

        animation_group = SequentialAnimationGroupWithStarted()
        animation_group.started.connect(on_start)

        pause_animation = QPauseAnimation(self)
        pause_animation.setDuration(5000)
        animation_group.addAnimation(pause_animation)

        return animation_group

    def get_show_question_animation(self, question: Question) -> QSequentialAnimationGroup:
        animation_group = QSequentialAnimationGroup(self)

        for i, step in enumerate(question.steps_before):
            step_animation = None

            if isinstance(step, TextStep):
                step_animation = self.get_text_step_animation(step)
            elif isinstance(step, ImageStep):
                step_animation = self.get_image_step_animation(step)
            elif isinstance(step, VideoStep):
                step_animation = self.get_video_step_animation(step)
            elif isinstance(step, AudioStep):
                step_animation = self.get_audio_step_animation(step)

            if step_animation:
                animation_group.addAnimation(step_animation)
            else:
                print(f"New type of steps -> {step}")

        return animation_group
