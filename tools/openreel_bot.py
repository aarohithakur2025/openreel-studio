"""OpenReel maintenance bot.

This is a deterministic Python agent: it runs ordered checks, stops on the first
blocking failure, and produces a compact report. It never performs generation.
"""
from __future__ import annotations
import json, pathlib, subprocess, sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
STEPS=[
 ("required-files", lambda: all((ROOT/p).is_file() for p in [
  "README.md","SECURITY.md","openreel-studio/index.html",
  "openreel-studio/src/app.js","openreel-studio/src/styles.css"])),
 ("json", lambda: all(json.loads(p.read_text(encoding="utf-8")) is not None
                       for p in ROOT.rglob("*.json"))),
 ("python-compile", lambda: subprocess.run(
   [sys.executable,"-m","compileall","-q","tools"],cwd=ROOT).returncode==0),
]
def main():
    print("OpenReel Bot — ordered safety gate")
    for name,fn in STEPS:
        try: ok=bool(fn())
        except Exception as e: ok=False; print(f"{name}: ERROR {e}")
        print(f"{name}: {'PASS' if ok else 'FAIL'}")
        if not ok:
            print("BOT STOP: blocking issue detected; no retry loop.")
            return 1
    print("BOT RESULT: PASS")
    return 0
if __name__=="__main__":
    raise SystemExit(main())
