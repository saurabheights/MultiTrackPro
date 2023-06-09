import os
from pathlib import Path
from typing import List


def get_video_files(dataset_path: Path) -> List[Path]:
    allow: List[str] = ['.mkv', '.avi', '.mp4']
    files: List[str] = os.listdir(dataset_path)
    video_files: List[Path] = []
    for file in files:
        for extension in allow:
            if file.endswith(extension):
                video_files.append(Path(file))
    return video_files
