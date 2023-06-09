import sys
from datetime import datetime
from typing import Optional, List

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from linetimer import linetimer, CodeTimer

from multitracker.config import PROFILE_CODE
from multitracker.core.dataset_manager import DatasetManager
from multitracker.qt.my_main_window import Ui_MainWindow


class VideoPlayer(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Load static UI file
        # uic.loadUi('resource/qt-ui/app.ui', self)
        self.dataset_manager: Optional[DatasetManager] = None
        self.reinitialize()
        self.open_video_action.triggered.connect(self.open_video_folder)

    def connect_slot_and_signals(self):
        """ Enable media buttons once media is loaded. """
        self.videoPlayPauseButton.pressed.connect(self.toggle_play_video)
        self.videoPrevButton.pressed.connect(lambda: self.move_video_pos(frame_delta=-1))
        self.videoNextButton.pressed.connect(lambda: self.move_video_pos(frame_delta=1))

    def disconnect_slot_and_signals(self):
        """ Disable media buttons once media is loaded. """
        self.videoPlayPauseButton.disconnect()
        self.videoPrevButton.disconnect()
        self.videoNextButton.disconnect()

    def reinitialize(self, video_files_path: Optional[List[str]] = None):
        self.video_files_path = video_files_path
        self.pixmap = None
        self.current_frame_num = 0  # Move to dataset manager
        self.is_video_paused = True
        self.video_play_timer = QTimer()
        self.video_play_timer.timeout.connect(self.play_next_frame)  # execute `display_time`
        self.video_play_timer.setInterval(100)  # ToDo Set fps using video file.

        if self.dataset_manager is not None:
            pass  # Ask to save.
        if video_files_path is None:
            self.dataset_manager = None
            return

        self.video_files_path = list(filter(lambda video_file: "internal" not in video_file, self.video_files_path))
        self.dataset_manager = DatasetManager(self.video_files_path)
        self.connect_slot_and_signals()

    def open_video_folder(self):
        video_files_path, _ = QFileDialog.getOpenFileNames(self, 'Select Videos', "", "Video Files (*.avi *.mp4 *.mpg)")
        if video_files_path:
            self.reinitialize(video_files_path)
            self.update_frame(frame_num=0)  # Set the first frame

    def toggle_play_video(self):
        self.is_video_paused = not self.is_video_paused
        if self.is_video_paused:
            self.video_play_timer.stop()
        else:
            self.video_play_timer.start()

    def move_video_pos(self, frame_delta: int):
        if self.is_video_paused:  # There is no utility in moving video by one frame if it is not paused.
            self.update_frame(self.current_frame_num + frame_delta)
        else:
            self.statusbar.showMessage("To view frame by frame, first pause the video.", msecs=10000)

    def play_next_frame(self):
        self.update_frame(self.current_frame_num + 1)

    @linetimer('Update Frame', silent=PROFILE_CODE)
    def update_frame(self, frame_num: int):
        print(str(datetime.now()))
        self.current_frame_num = frame_num
        with CodeTimer('Get Data', unit='ms', silent=PROFILE_CODE):
            frame = self.dataset_manager.get_data(frame_num=frame_num)
        if frame is None:
            self.video_play_timer.stop()
            self.current_frame_num = 0

        with CodeTimer('Render frame', unit='ms', silent=PROFILE_CODE):
            image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format.Format_BGR888)
            self.pixmap = QPixmap.fromImage(image)
        self.update()

    def paintEvent(self, event):
        if self.pixmap is not None:
            self.video_label.setPixmap(
                self.pixmap.scaled(self.video_label.width(), self.video_label.height(),
                                   Qt.AspectRatioMode.KeepAspectRatio,
                                   transformMode=Qt.TransformationMode.SmoothTransformation)
            )


def main():
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
