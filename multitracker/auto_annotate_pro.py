import logging
import sys
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QProgressDialog
from linetimer import linetimer, CodeTimer
from typing import Optional, List

from multitracker.config import PROFILE_CODE
from multitracker.core.dataset_manager import DatasetManager
from multitracker.core.io.multi_video_manager import MultiVideoManager

from multitracker.core.tracker.multi_tracker import MultiVideoTracker
from multitracker.qt.my_main_window import Ui_MainWindow


class VideoPlayer(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.dataset_manager: Optional[DatasetManager] = None
        self.reinitialize()
        self.open_video_action.triggered.connect(self.open_video_folder)

    def connect_slot_and_signals(self):
        if self.dataset_manager is None:
            logging.warning("No dataset manager but various buttons are being enabled.")

        """ Enable media buttons once media is loaded. """
        self.video_play_pause_button.pressed.connect(self.toggle_play_video)
        self.video_prev_button.pressed.connect(lambda: self.move_video_pos(frame_delta=-1))
        self.video_next_button.pressed.connect(lambda: self.move_video_pos(frame_delta=1))

        """ Enable tracking option """
        self.run_tracking_model_button.pressed.connect(self.run_tracking)
        self.merge_tracks_button.pressed.connect(self.merge_tracks)

        """ Enable buttons """
        for button in [
            self.video_play_pause_button, self.video_prev_button, self.video_next_button,
            self.run_tracking_model_button, self.merge_tracks_button
        ]:
            button.setEnabled(True)

    def reinitialize(self, video_files: Optional[List[str]] = None):
        self.video_files = video_files
        self.pixmap = None
        self.current_frame_num = 0  # Move to dataset manager
        self.is_video_paused = True
        self.video_play_timer = QTimer()
        self.video_play_timer.timeout.connect(self.play_next_frame)  # execute `display_time`
        self.video_play_timer.setInterval(100)  # ToDo Set fps using video file.

        if self.dataset_manager is not None:
            pass  # Ask to save.
        if video_files is None:
            self.dataset_manager = None
            return

        self.video_files = list(filter(lambda video_file: "internal" not in video_file, self.video_files))
        self.dataset_manager = DatasetManager(self.video_files)
        self.connect_slot_and_signals()

    def open_video_folder(self):
        video_files, _ = QFileDialog.getOpenFileNames(self, 'Select Videos', "", "Video Files (*.avi *.mp4 *.mpg)")
        if video_files:
            self.reinitialize(video_files)
            self.update_frame(frame_num=0)  # Set the first frame to show video files are loaded.

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

    def run_tracking(self):
        # Pause the video, since we will block user inputs.
        if not self.is_video_paused:
            self.toggle_play_video()
        # Confirm before running
        ret = QMessageBox.question(
            self,
            "Run tracking model",
            "Are you sure you want to run tracking model? This can take long time.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes,
        )
        if ret != QMessageBox.StandardButton.Yes:
            return

        # Run tracker on videos.
        update_progress_dialog_box = QProgressDialog(
            "Running tracker", "Stop tracking", 0, self.dataset_manager.get_video_length_in_frames(), self
        )
        update_progress_dialog_box.setWindowModality(Qt.WindowModality.WindowModal)
        update_progress_dialog_box.show()
        # ToDo - Move logic of loading video to tracker and pass progress_callback to tracker.
        tracker = MultiVideoTracker(
            video_files=self.video_files,
            classes=[2, 5, 7]  # Only 2: 'car', 5: 'bus', 7: 'truck', Later allow customization.
        )
        tmp_dataset_manager = MultiVideoManager(video_files=self.video_files)
        for frame_num in range(self.dataset_manager.get_video_length_in_frames()):
            frames = tmp_dataset_manager.read()
            if frames is None:
                logging.error(f"Got None frames when fetching from tmp_dataset_manager, frame number: {frame_num}")
                continue
            tracker.track(frames)
            update_progress_dialog_box.setValue(frame_num)
            if update_progress_dialog_box.wasCanceled():
                break
        # Save all the values computed.
        update_progress_dialog_box.setValue(self.dataset_manager.get_video_length_in_frames())
        self.dataset_manager.add_annotations(*tracker.get_annotations())

    def merge_tracks(self):
        pass


def main():
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
