from __future__ import annotations

import json
import hashlib
import shutil
import subprocess
import uuid
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

    timestamps = sample_timestamps(
        duration_seconds=row.duration_seconds,
        sample_frames=sample_frames,
    )
    frame_artifacts = extract_keyframes(
        video=video,
        keyframes_dir=keyframes_dir,
        timestamps=timestamps,
    )
    ocr_path = evidence_dir / "ocr.json"
    ocr_results = ocr_frames(frame_artifacts)
    ocr_path.write_text(json.dumps(ocr_results, indent=2, sort_keys=True))

    packet = {
        "video_id": video.stem,
        "source_video": str(video),
        "analysis_run": {
            "run_id": f"run_{uuid.uuid4().hex}",
            "source_sha256": sha256_file(video),
            "extractor": "creatives-extract",
            "schema_version": "evidence_packet.v2",
        },
        "manifest": row.model_dump(),
        "timeline_evidence": timeline_events(
            manifest=row.model_dump(),
            frame_artifacts=frame_artifacts,
            ocr_results=ocr_results,
            manifest_path=manifest_path,
            ocr_path=ocr_path,
        ),
        "artifacts": {
            "manifest": str(manifest_path),
            "keyframes_dir": str(keyframes_dir),
            "ocr": str(ocr_path),
            "transcript_status": "not_run",
            "scene_status": "not_run",
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
    timestamps: list[float],
) -> list[dict]:
    if not timestamps:
        return []

    artifacts = []
    for index, timestamp_seconds in enumerate(timestamps, start=1):
        frame_path = keyframes_dir / f"frame_{index:03d}_{timestamp_seconds:.3f}s.jpg"
        command = [
            "ffmpeg",
            "-y",
            "-ss",
            f"{timestamp_seconds:.3f}",
            "-i",
            str(video),
            "-frames:v",
            "1",
            str(frame_path),
        ]
        subprocess.run(command, check=True, capture_output=True, text=True)
        artifacts.append(
            {
                "evidence_id": f"ev_keyframe_{index:03d}",
                "timestamp": format_timestamp(timestamp_seconds),
                "timestamp_seconds": timestamp_seconds,
                "frame": str(frame_path),
            }
        )
    return artifacts


def ocr_frames(frame_artifacts: list[dict]) -> list[dict]:
    if not frame_artifacts:
        return []
    if shutil.which("tesseract") is None:
        return [
            {
                "evidence_id": artifact["evidence_id"].replace("keyframe", "ocr"),
                "timestamp": artifact["timestamp"],
                "frame": artifact["frame"],
                "text": "",
                "status": "skipped",
                "reason": "tesseract not found",
            }
            for artifact in frame_artifacts
        ]

    import pytesseract
    from PIL import Image

    results = []
    for artifact in frame_artifacts:
        frame_path = Path(artifact["frame"])
        with Image.open(frame_path) as image:
            text = pytesseract.image_to_string(image).strip()
        results.append(
            {
                "evidence_id": artifact["evidence_id"].replace("keyframe", "ocr"),
                "timestamp": artifact["timestamp"],
                "frame": str(frame_path),
                "text": text,
                "status": "ok",
                "confidence": "medium" if text else "low",
            }
        )
    return results


def sample_timestamps(*, duration_seconds: float, sample_frames: int) -> list[float]:
    if sample_frames <= 0:
        return []

    dense_hook_points = [0.0, 0.5, 1.0, 2.0, 3.0]
    timestamps = [
        timestamp
        for timestamp in dense_hook_points
        if timestamp <= duration_seconds
    ][:sample_frames]

    remaining = sample_frames - len(timestamps)
    if remaining > 0:
        step = duration_seconds / (remaining + 1)
        timestamps.extend(step * index for index in range(1, remaining + 1))

    return sorted({round(timestamp, 3) for timestamp in timestamps})


def timeline_events(
    *,
    manifest: dict,
    frame_artifacts: list[dict],
    ocr_results: list[dict],
    manifest_path: Path,
    ocr_path: Path,
) -> list[dict]:
    duration = manifest["duration_seconds"]
    events = [
        {
            "evidence_id": "ev_manifest_000",
            "timestamp": f"0.000-{duration:.3f}",
            "source": "metadata",
            "observation": (
                f"{manifest['filename']} is a {manifest['orientation']} "
                f"{manifest['width']}x{manifest['height']} video, "
                f"{duration:.2f}s long, fps={manifest['fps']:.2f}, "
                f"audio={'present' if manifest['has_audio'] else 'absent'}."
            ),
            "confidence": "high",
            "artifact": str(manifest_path),
        }
    ]

    for artifact in frame_artifacts:
        events.append(
            {
                "evidence_id": artifact["evidence_id"],
                "timestamp": artifact["timestamp"],
                "source": "keyframe",
                "observation": f"Sampled keyframe at {artifact['timestamp']}.",
                "confidence": "high",
                "artifact": artifact["frame"],
            }
        )

    for result in ocr_results:
        if not result.get("text"):
            continue
        events.append(
            {
                "evidence_id": result["evidence_id"],
                "timestamp": result["timestamp"],
                "source": "ocr",
                "observation": f"OCR text: {result['text']}",
                "confidence": result.get("confidence", "medium"),
                "artifact": str(ocr_path),
            }
        )

    return events


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def format_timestamp(timestamp_seconds: float) -> str:
    return f"{timestamp_seconds:.3f}"
