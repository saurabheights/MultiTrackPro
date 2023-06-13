from time import sleep
from typing import List

import numpy as np


class Tracker:

    def __init__(self):
        super().__init__()

    def track(self, frames: List[np.ndarray]):
        assert frames is not None, "Tracking module received None frames"
        sleep(0.1)

    def get_annotations(self):
        pass
