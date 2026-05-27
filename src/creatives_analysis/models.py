from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


class VideoInventoryRow(BaseModel):
    filename: str
    path: str
    duration_seconds: float = Field(gt=0)
    size_bytes: int = Field(ge=0)
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    fps: float = Field(gt=0)
    video_codec: str
    audio_codec: str | None = None
    has_audio: bool
    orientation: str

    @classmethod
    def from_path_and_probe(cls, video_path: Path, probe: dict) -> "VideoInventoryRow":
        streams = probe.get("streams", [])
        video_stream = next(
            (stream for stream in streams if stream.get("codec_type") == "video"),
            None,
        )
        if not video_stream:
            raise ValueError(f"No video stream found in {video_path}")

        audio_stream = next(
            (stream for stream in streams if stream.get("codec_type") == "audio"),
            None,
        )
        width = int(video_stream["width"])
        height = int(video_stream["height"])
        duration = float(probe.get("format", {}).get("duration", 0))
        size = int(probe.get("format", {}).get("size", video_path.stat().st_size))

        return cls(
            filename=video_path.name,
            path=str(video_path),
            duration_seconds=duration,
            size_bytes=size,
            width=width,
            height=height,
            fps=parse_fps(video_stream.get("r_frame_rate", "0/0")),
            video_codec=str(video_stream.get("codec_name", "unknown")),
            audio_codec=audio_stream.get("codec_name") if audio_stream else None,
            has_audio=audio_stream is not None,
            orientation=orientation_for(width=width, height=height),
        )


class ValidationResult(BaseModel):
    fixture: Path
    schema_path: Path
    valid: bool
    errors: list[str] = Field(default_factory=list)


def orientation_for(*, width: int, height: int) -> str:
    if height > width:
        return "vertical"
    if width > height:
        return "horizontal"
    return "square"


def parse_fps(value: str) -> float:
    if "/" not in value:
        return float(value)

    numerator, denominator = value.split("/", 1)
    denominator_value = float(denominator)
    if denominator_value == 0:
        return 0.0
    return float(numerator) / denominator_value
