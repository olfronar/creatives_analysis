from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from .inventory import collect_inventory


def build_evidence_packet(
    *,
    video: Path,
    output_root: Path = Path("outputs"),
    sample_frames: int = 8,
) -> Path:
    row = collect_inventory([video])[0]
    evidence_dir = output_root / video.stem / "evidence"
    keyframes_dir = evidence_dir / "keyframes"
    keyframes_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = evidence_dir / "manifest.json"
    manifest_path.write_text(json.dumps(row.model_dump(), indent=2, sort_keys=True))

    frame_paths = extract_keyframes(
        video=video,
        keyframes_dir=keyframes_dir,
        duration_seconds=row.duration_seconds,
        sample_frames=sample_frames,
    )
    ocr_path = evidence_dir / "ocr.json"
    ocr_path.write_text(json.dumps(ocr_frames(frame_paths), indent=2, sort_keys=True))

    packet = {
        "video_id": video.stem,
        "source_video": str(video),
        "manifest": row.model_dump(),
        "artifacts": {
            "manifest": str(manifest_path),
            "keyframes_dir": str(keyframes_dir),
            "ocr": str(ocr_path),
        },
        "transcript": {
            "status": "not_run",
            "note": "Transcription is intentionally not run by default to avoid model download during build-only setup.",
        },
        "scenes": {
            "status": "not_run",
            "note": "Scene detection is available for future runs but is not required for build-only validation.",
        },
        "reports_generated": [],
    }
    packet_path = evidence_dir / "evidence_packet.json"
    packet_path.write_text(json.dumps(packet, indent=2, sort_keys=True))
    return packet_path


def extract_keyframes(
    *,
    video: Path,
    keyframes_dir: Path,
    duration_seconds: float,
    sample_frames: int,
) -> list[Path]:
    if sample_frames <= 0:
        return []

    interval = max(duration_seconds / sample_frames, 1)
    output_pattern = keyframes_dir / "frame_%03d.jpg"
    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(video),
        "-vf",
        f"fps=1/{interval:.4f}",
        "-frames:v",
        str(sample_frames),
        str(output_pattern),
    ]
    subprocess.run(command, check=True, capture_output=True, text=True)
    return sorted(keyframes_dir.glob("frame_*.jpg"))


def ocr_frames(frame_paths: list[Path]) -> list[dict]:
    if not frame_paths:
        return []
    if shutil.which("tesseract") is None:
        return [
            {
                "frame": str(frame_path),
                "text": "",
                "status": "skipped",
                "reason": "tesseract not found",
            }
            for frame_path in frame_paths
        ]

    import pytesseract
    from PIL import Image

    results = []
    for frame_path in frame_paths:
        with Image.open(frame_path) as image:
            text = pytesseract.image_to_string(image).strip()
        results.append(
            {
                "frame": str(frame_path),
                "text": text,
                "status": "ok",
            }
        )
    return results
