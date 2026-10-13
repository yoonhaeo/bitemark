"""Check publishable Git files, not ignored local model/data installations."""
from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANNED = {".pt", ".pth", ".ckpt", ".stl", ".npz", ".npy", ".ipynb", ".so", ".o"}
PATTERNS = {
    "patient case identifier": re.compile(r"\bF(?!0000\b)\d{4}\b"),
    "private service": re.compile(r"165[.]132[.]146[.]87"),
    "GitHub token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})"),
    "private key": re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
}


def main() -> int:
    raw = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=ROOT
    )
    errors = []
    for name in set(raw.decode().split("\0")) - {""}:
        path = ROOT / name
        if not path.is_file():
            continue
        if name == "final2/model/s/b/b/nn/modules/kernels/dispositions/k_015_center.ply":
            expected = "b3161cd3d2bdc325b48831d60b19038f33359105c675742a9289c5ca6eca2b6a"
            if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                errors.append("Synthetic convolution kernel changed; review before release")
            continue
        if path.suffix.lower() in BANNED or path.stat().st_size > 5 * 1024 * 1024:
            errors.append(f"Non-source/oversized Git artifact: {name}")
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"Review binary Git artifact: {name}")
            continue
        for label, pattern in PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{label}: {name}")
    if errors:
        print("\n".join(errors))
        return 1
    print("Release guard passed: no forbidden data/weights, case IDs or token patterns in Git files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
