import logging
from typing import List, Optional

import numpy as np

from multitracker.core.io.multi_video_manager import MultiVideoManager


class DatasetManager:

    def __init__(self, video_files: List[str]):
        self.video_files = video_files
        self.videos_sync_reader = MultiVideoManager(video_files)
        self.current_frame_num = -1
        self.number_of_frames = self.videos_sync_reader.get_video_length_in_frames()

    def tile_images(self, frames: List[np.ndarray]) -> np.ndarray:
        # ToDo Handle when number of images is not 4 or if image dimension are different.

        # Concatenate images horizontally
        row_1 = np.hstack(frames[:2])
        row_2 = np.hstack(frames[2:])
        return np.vstack([row_1, row_2])

    def get_data(self, frame_num: int) -> Optional[List[np.ndarray]]:
        """
        Returns QImage for display with render-able objects (annotations) that can be manipulated via GUI.
        """
        if frame_num >= self.number_of_frames:
            logging.info("Reached end of the video files.")
            return None

        if frame_num == self.current_frame_num + 1:
            all_video_frames = self.videos_sync_reader.read()
        else:
            # Set frame calls are slow and will cause issue when user is trying to rewind back.
            # ToDo - Instead of using queue to store next frames, use cache that stores previous 60 and next 60 frames.
            self.videos_sync_reader.set_frame(self.current_frame_num)
            all_video_frames = self.videos_sync_reader.read()

        self.current_frame_num = frame_num

        if all_video_frames is None:
            logging.error("all_video_frames are None, video read failed.")
            return None
        tiled_image = self.tile_images(all_video_frames)
        return tiled_image

    def get_video_length_in_frames(self) -> int:
        return self.videos_sync_reader.MIN_FRAME_COUNT
