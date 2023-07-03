import logging
from typing import List

import numpy as np

from multitracker.core.io.cached_video_reader import CachedVideoReader


class MultiVideoManager:
    def __init__(self, video_files: List[str], threaded_capture=True, queue_size=128):
        self.file_video_streamers: List[CachedVideoReader] = list(map(
            lambda x: CachedVideoReader(x, threaded_capture=threaded_capture, queue_size=queue_size), video_files
        ))
        self.MIN_FRAME_COUNT = min(list(map(lambda x: x.size, self.file_video_streamers)))
        print(self.MIN_FRAME_COUNT)

    def get_video_length_in_frames(self) -> int:
        return self.MIN_FRAME_COUNT

    def read(self) -> List[np.ndarray]:
        successflags_and_frames = list(map(lambda x: x.read(), self.file_video_streamers))
        successflags, frames = zip(*successflags_and_frames)
        if not all(successflags):
            logging.error("Not all frames successfully captured.")
            return None
        return frames

    def set_frame(self, frame_num: int):
        logging.debug(f"Changing frame number to {frame_num}")
        list(map(lambda x: x.set_frame(frame_num=frame_num), self.file_video_streamers))
