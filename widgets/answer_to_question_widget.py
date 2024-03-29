from typing import Optional, List

from PyQt6.QtCore import QPropertyAnimation, QSize, QParallelAnimationGroup, QPoint, QSequentialAnimationGroup, \
    QPauseAnimation, Qt
from PyQt6.QtGui import QPaintEvent, QPixmap
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import QPushButton, QSizePolicy, QLabel, QVBoxLayout

from helpers.media_player import MediaPlayer
from helpers.pyqt_animation import SequentialAnimationGroupWithStarted
from helpers.timer import OnChangeRunStatusSignalArgs
from packs.question import Question
from packs.steps.audio_step import AudioStep
from packs.steps.image_step import ImageStep
from packs.steps.question_step import QuestionStep
from packs.steps.text_step import TextStep
from packs.steps.video_step import VideoStep
from services.service_locator import ServiceLocator
from widgets.base.border_mixin import BorderMixin
from widgets.select_question_widget import SELECT_QUESTION_GRID_CELL_CSS, BIG_QUESTION_MARGIN

ANSWER_TO_QUESTION_WIDGET_CSS = SELECT_QUESTION_GRID_CELL_CSS + f"""
    margin: {BIG_QUESTION_MARGIN[0]};
"""


class AnswerToQuestionWidget(QPushButton, BorderMixin):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.setStyleSheet(ANSWER_TO_QUESTION_WIDGET_CSS)

        self.margin = BIG_QUESTION_MARGIN

        self.vbox_layout = QVBoxLayout(self)

        self.text_label = QLabel("TEXT", self)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.video_widget = QVideoWidget()

        self.content_label = QLabel("IMAGE", self)
        self.content_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_label.setScaledContents(True)

        self.vbox_layout.addWidget(self.text_label)
        self.vbox_layout.addWidget(self.content_label, 1)
        self.vbox_layout.addWidget(self.video_widget, 1)

        self.text_label.hide()
        self.content_label.hide()
        self.video_widget.hide()

        self.timer = ServiceLocator.get().question_timer

        self.timer.on_change_run_status.connect(self.on_change_run_status_handler)

    def show_content_label(self):
        self.video_widget.hide()
        self.content_label.show()

    def show_video_widget(self):
        self.content_label.hide()
        self.video_widget.show()

    def hide_all(self):
        self.content_label.hide()
        self.video_widget.hide()
        self.text_label.hide()

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

    def get_text_animation(self, text: str) -> SequentialAnimationGroupWithStarted:
        def on_start():
            self.text_label.setText(text)
            self.text_label.show()

        animation_group = SequentialAnimationGroupWithStarted()
        animation_group.started.connect(on_start)

        pause_animation = QPauseAnimation(self)
        pause_animation.setDuration(2000)
        animation_group.addAnimation(pause_animation)

        return animation_group

    def get_text_step_animation(self, step: TextStep) -> SequentialAnimationGroupWithStarted:
        return self.get_text_animation(step.get_result())

    def get_image_step_animation(self, step: ImageStep) -> SequentialAnimationGroupWithStarted:
        def on_start():
            image = step.get_result()
            pixmap = QPixmap()
            pixmap.loadFromData(image)
            self.content_label.setPixmap(pixmap)
            self.show_content_label()

        animation_group = SequentialAnimationGroupWithStarted()
        animation_group.started.connect(on_start)

        pause_animation = QPauseAnimation(self)
        pause_animation.setDuration(2000)
        animation_group.addAnimation(pause_animation)

        return animation_group

    def get_video_step_animation(self, step: VideoStep) -> SequentialAnimationGroupWithStarted:
        def on_start():
            self.show_video_widget()
            media_player.play()

        media_player = MediaPlayer(self.video_widget)
        media_player.set_content(step.get_result())

        animation_group = SequentialAnimationGroupWithStarted()
        animation_group.started.connect(on_start)

        pause_animation = QPauseAnimation(self)
        pause_animation.setDuration(media_player.get_duration())
        animation_group.addAnimation(pause_animation)

        return animation_group

    def get_audio_step_animation(self, step: AudioStep) -> SequentialAnimationGroupWithStarted:
        def on_start():
            pixmap = QPixmap('resources/audio_step_image.png')
            pixmap.setMask(pixmap.createHeuristicMask())  # enable background opacity
            self.content_label.setPixmap(pixmap)
            self.show_content_label()

            media_player.play()

        media_player = MediaPlayer()
        media_player.set_content(step.get_result())

        animation_group = SequentialAnimationGroupWithStarted()
        animation_group.started.connect(on_start)

        pause_animation = QPauseAnimation(self)
        pause_animation.setDuration(media_player.get_duration())
        animation_group.addAnimation(pause_animation)

        return animation_group

    def _get_animation_for_steps(self, steps: List[QuestionStep]) -> QSequentialAnimationGroup:
        animation_group = QSequentialAnimationGroup(self)

        for i, step in enumerate(steps):
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

    def get_show_question_animation(self, question: Question) -> QSequentialAnimationGroup:
        return self._get_animation_for_steps(question.steps_before)

    def get_show_answer_animation(self, question: Question) -> QSequentialAnimationGroup:
        animation_group = self._get_animation_for_steps(question.steps_after)

        if question.answer:
            text_answer_animation = self.get_text_animation(question.answer)
            animation_group.addAnimation(text_answer_animation)

        return animation_group

    def on_change_run_status_handler(self, args: OnChangeRunStatusSignalArgs):
        self.set_enable_border(args.is_running)
        if args.is_running:
            part = self.timer.get_rest() / self.timer.max_time
            self.start_border_animation(part, int(self.timer.get_rest() * 1000))
        else:
            self.stop_border_animation()

    def paintEvent(self, a0: Optional[QPaintEvent]) -> None:
        super().paintEvent(a0)
        self.update_border()
