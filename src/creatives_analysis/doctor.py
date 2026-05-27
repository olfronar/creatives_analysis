from __future__ import annotations

import importlib.util
import shutil


SYSTEM_TOOLS = ("ffmpeg", "ffprobe", "tesseract")
PYTHON_PACKAGES = (
    "faster_whisper",
    "cv2",
    "PIL",
    "pytesseract",
    "pydantic",
    "jsonschema",
    "typer",
)


def collect_doctor_status() -> dict:
    return {
        "system_tools": {
            tool: {
                "available": shutil.which(tool) is not None,
                "path": shutil.which(tool),
            }
            for tool in SYSTEM_TOOLS
        },
        "python_packages": {
            package: importlib.util.find_spec(package) is not None
            for package in PYTHON_PACKAGES
        },
    }


def doctor_has_failures(status: dict) -> bool:
    missing_tools = [
        name for name, item in status["system_tools"].items() if not item["available"]
    ]
    missing_packages = [
        name for name, available in status["python_packages"].items() if not available
    ]
    return bool(missing_tools or missing_packages)
