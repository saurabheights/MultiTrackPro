from __future__ import absolute_import

import logging
import time
from queue import Queue
from threading import Thread, Lock

import cv2


class CachedVideoReader:
    def __init__(self, video_file, threaded_capture=True, queue_size=128):
        self.stream = cv2.VideoCapture(str(video_file))
        self.size = int(self.stream.get(cv2.CAP_PROP_FRAME_COUNT))
        self.stopped = False
        self.is_rewinds = False
        self.threaded_capture = threaded_capture

        if threaded_capture:
            self.lock = Lock()
            self.Q = Queue(maxsize=queue_size)
            self.thread = Thread(target=self.update, args=(), daemon=True)
            self.thread.daemon = True
            self.thread.start()

    def update(self):
        while True:
            if self.stopped:
                break

            # ToDo Replace queue with an in-mem cache.
            with self.lock:
                if self.is_rewinds:  # ToDo - The frames may go out of sync between different CachedVideoReader.
                    continue
                if not self.Q.full():
                    (grabbed, frame) = self.stream.read()
                    if not grabbed:
                        self.stopped = True
                    self.Q.put(frame)  # ToDo Put frame with frame number to ensure synchronization.
                else:
                    time.sleep(0.01)
        self.stream.release()

    def read(self):
        if self.threaded_capture:
            return not self.stopped, self.Q.get()
        else:
            return self.stream.read()

    def is_opened(self):
        return self.stream.isOpened()

    def release(self):
        if self.threaded_capture:
            self.stopped = True
            self.thread.join()
        else:
            self.stream.release()

    def set_frame(self, frame_num: int):
        logging.debug(f"Changing frame number to {frame_num}")
        if self.threaded_capture:
            self.is_rewinds = True
            with self.lock:
                self.stream.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
                while not self.Q.empty():  # Empty the queue
                    self.Q.get()
            self.is_rewinds = False
        else:
            self.stream.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
