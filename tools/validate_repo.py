"""Deterministic OpenReel repository and ComfyUI contract validator.

Usage:
  python tools/validate_repo.py
  python tools/validate_repo.py --comfy http://127.0.0.1:8189

The validator never retries generation and never submits a real generation job.
"""
from __future__ import annotations
import argparse, json, pathlib, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md", "SECURITY.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md",
    "openreel-studio/index.html", "openreel-studio/src/app.js",
    "openreel-studio/src/styles.css", "tools/verify_backend.py",
    "tools/mock_comfy_server.py", "docs/GENERATION_PLAN.md",
]

def check_files() -> None:
    missing = [p for p in REQUIRED if not (ROOT / p).is_file()]
    if missing:
        raise SystemExit("Missing files: " + ", ".join(missing))
    for p in ROOT.rglob("*.json"):
        json.loads(p.read_text(encoding="utf-8"))
    print("files/json: PASS")

def get(base: str, path: str):
    with urllib.request.urlopen(base.rstrip("/") + path, timeout=5) as r:
        return json.load(r)

def check_comfy(base: str) -> None:
    stats = get(base, "/system_stats")
    info = get(base, "/object_info")
    assert isinstance(stats, dict)
    required = {"CLIPTextEncode", "LoadImage", "CreateVideo", "SaveVideo"}
    missing = sorted(required - set(info))
    if missing:
        raise SystemExit("ComfyUI missing nodes: " + ", ".join(missing))
    print("comfy/system_stats: PASS")
    print("comfy/object_info: PASS")

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--comfy", help="optional ComfyUI base URL; read-only checks only")
    args = ap.parse_args()
    check_files()
    if args.comfy:
        check_comfy(args.comfy)
    print("OpenReel validation: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
