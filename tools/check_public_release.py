"""Fail closed if a public release contains likely private artifacts."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache", "output"}
BANNED_SUFFIXES = {
    ".pt",
    ".pth",
    ".ckpt",
    ".onnx",
    ".engine",
    ".safetensors",
    ".npy",
    ".npz",
    ".stl",
    ".ipynb",
}
BANNED_TEXT = {
    "private dataset path": re.compile("/data/" + "MICCAI", re.IGNORECASE),
    "embedded token": re.compile(
        r"(?:token|api[_-]?key|secret)\s*[=:]\s*[^\s<]{8,}", re.IGNORECASE
    ),
    "private service address": re.compile("165" + r"\.132\.146\.87"),
}
MAX_PUBLIC_FILE_BYTES = 5 * 1024 * 1024


def iter_public_files():
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def main() -> int:
    errors: list[str] = []
    for path in iter_public_files():
        relative = path.relative_to(ROOT)
        if path.suffix.lower() in BANNED_SUFFIXES:
            errors.append(f"banned artifact: {relative}")
        if path.stat().st_size > MAX_PUBLIC_FILE_BYTES:
            errors.append(f"oversized file: {relative}")
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in BANNED_TEXT.items():
            if pattern.search(text):
                errors.append(f"{label}: {relative}")

    config = (ROOT / "configs/public_placeholder.yaml").read_text(encoding="utf-8")
    for required in (
        "needs_to_be_finetuned: true",
        "clinically_validated: false",
        "contains_real_calibration: false",
    ):
        if required not in config:
            errors.append(f"missing public safety flag: {required}")

    if errors:
        print("Public-release guard failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Public-release guard passed: no private artifacts or paths detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
