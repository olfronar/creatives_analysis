from __future__ import annotations

import subprocess
from pathlib import Path


def make_test_video(tmp_path: Path, filename: str = "sample.mp4") -> Path:
    video_path = tmp_path / filename
    command = [
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        "color=c=black:s=360x640:d=1:r=30",
        "-f",
        "lavfi",
        "-i",
        "anullsrc=channel_layout=stereo:sample_rate=44100",
        "-shortest",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        str(video_path),
    ]
    subprocess.run(command, check=True, capture_output=True, text=True)
    return video_path
