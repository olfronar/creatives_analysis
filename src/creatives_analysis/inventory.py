from __future__ import annotations

import json
import subprocess
from collections.abc import Iterable
from pathlib import Path

from .models import VideoInventoryRow


def collect_inventory(video_paths: Iterable[Path]) -> list[VideoInventoryRow]:
    rows: list[VideoInventoryRow] = []
    for video_path in sorted(video_paths):
        if not video_path.exists():
            raise FileNotFoundError(video_path)
        rows.append(VideoInventoryRow.from_path_and_probe(video_path, probe_video(video_path)))
    return rows


def probe_video(video_path: Path) -> dict:
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate",
        "-of",
        "json",
        str(video_path),
    ]
    completed = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def inventory_as_json(rows: list[VideoInventoryRow]) -> str:
    return json.dumps(
        [row.model_dump() for row in rows],
        indent=2,
        sort_keys=True,
    )


def inventory_as_table(rows: list[VideoInventoryRow]) -> str:
    header = "| file | duration | resolution | fps | audio | orientation |"
    separator = "|---|---:|---|---:|---|---|"
    body = [
        (
            f"| {row.filename} | {row.duration_seconds:.2f}s | "
            f"{row.width}x{row.height} | {row.fps:.2f} | "
            f"{'yes' if row.has_audio else 'no'} | {row.orientation} |"
        )
        for row in rows
    ]
    return "\n".join([header, separator, *body])
