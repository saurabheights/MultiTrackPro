import logging
from collections import defaultdict
from typing import List, Dict, Tuple

import numpy as np
from ultralytics import YOLO, RTDETR
from ultralytics.yolo.engine.results import Results
from ultralytics.yolo.utils.plotting import Annotator


class MultiVideoTracker():

    def __init__(self, video_files: List[str], classes=None):
        """
        number_of_videos is the number of videos
        """
        super().__init__()

        self.video_files = video_files
        self.classes = classes

        self.model = YOLO('yolov8n.pt')
        logging.info("Fusing the model")
        self.model.fuse()

        assert self.model.names is not None, f"Model used cannot have names field set to None, f{self.model}"

        # Saves output for each frame of all videos.
        self.annotations: Dict[str, List[np.ndarray]] = defaultdict(list)

    def get_annotations(self) -> Tuple[Dict[str, List[np.ndarray]], Dict[int, str]]:
        return self.annotations, self.model.names

    def track(self, frames: List[np.ndarray], frame_num=0) -> np.ndarray:
        """
        :param frames: The frames to run object detection and tracking on. Assumed to be in same order as video files.
        :param frame_num: The frame number
        :return: Rendered image for preview.
        """
        results: Results = self.model.predict(source=frames, classes=self.classes)

        for index, (result, frame) in enumerate(zip(results, frames)):
            annotator = Annotator(frame)
            result = result.cpu().numpy()
            # Detection
            boxes_xyxy = result.boxes.xyxy  # box with xyxy format but normalized, (N, 4)
            conf = result.boxes.conf  # confidence score, (N, 1)
            cls = result.boxes.cls  # cls, (N, 1)

            self.annotations[self.video_files[index]].append(np.column_stack((boxes_xyxy, conf, cls)))

            for (box, c) in zip(boxes_xyxy, cls):
                annotator.box_label(box, self.model.names[int(c)])

        # Tile all 4 images.
        # ToDo - Move to a generic tile method.
        row_1 = np.hstack(frames[:2])
        row_2 = np.hstack(frames[2:])
        return np.vstack([row_1, row_2])
