#!/usr/bin/env python3
"""Local-only OpenReel -> WanGP bridge.

This bridge does not bundle or modify WanGP. It loads an existing local WanGP
installation through its documented Python API. Keep the listener on localhost.
"""

from __future__ import annotations

import argparse
import json
import os
import threading
import traceback
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

ROOT = Path(os.environ.get("WANGP_ROOT", "")).expanduser().resolve()
PORT = int(os.environ.get("OPENREEL_WANGP_PORT", "7861"))
HOST = os.environ.get("OPENREEL_WANGP_HOST", "127.0.0.1")

_SESSION = None
_SESSION_LOCK = threading.Lock()
_JOBS: dict[str, dict[str, Any]] = {}
_JOBS_LOCK = threading.Lock()


def json_response(handler: BaseHTTPRequestHandler, status: int, payload: Any) -> None:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(data)))
    handler.send_header("Access-Control-Allow-Origin", "http://127.0.0.1:8000")
    handler.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type")
    handler.end_headers()
    handler.wfile.write(data)


def load_session():
    global _SESSION
    with _SESSION_LOCK:
        if _SESSION is not None:
            return _SESSION
        if not ROOT or not (ROOT / "wgp.py").is_file():
            raise RuntimeError("WANGP_ROOT is not set to a valid WanGP folder containing wgp.py")
        import sys
        sys.path.insert(0, str(ROOT))
        from shared.api import init
        _SESSION = init(root=ROOT, console_output=False, console_isatty=False)
        return _SESSION


def validate_settings(payload: dict[str, Any]) -> dict[str, Any]:
    allowed = {
        "model_type", "prompt", "negative_prompt", "resolution", "video_length",
        "force_fps", "num_inference_steps", "seed", "repeat_generation",
        "output_filename", "settings_version", "sample_solver", "flow_shift",
    }
    settings = {k: v for k, v in payload.items() if k in allowed}
    if not settings.get("model_type"):
        raise ValueError("model_type is required")
    if not settings.get("prompt"):
        raise ValueError("prompt is required")
    settings.setdefault("repeat_generation", 1)
    return settings


def run_job(job_id: str, settings: dict[str, Any]) -> None:
    try:
        with _JOBS_LOCK:
            _JOBS[job_id]["status"] = "starting"
        session = load_session()
        with _JOBS_LOCK:
            _JOBS[job_id]["status"] = "running"
        job = session.submit_task(settings)
        result = job.result()
        with _JOBS_LOCK:
            _JOBS[job_id].update(
                status="completed" if result.success else "failed",
                generated_files=list(result.generated_files),
                errors=[getattr(e, "message", str(e)) for e in result.errors],
            )
    except Exception as exc:
        with _JOBS_LOCK:
            _JOBS[job_id].update(
                status="failed",
                error=str(exc),
                traceback=traceback.format_exc(limit=4),
            )


class Handler(BaseHTTPRequestHandler):
    server_version = "OpenReel-WanGP-Bridge/1.0"

    def log_message(self, fmt, *args):
        return

    def do_OPTIONS(self):
        json_response(self, 204, {})

    def do_GET(self):
        if self.path == "/health":
            json_response(
                self,
                200,
                {
                    "ok": True,
                    "wangp_root": str(ROOT) if ROOT else None,
                    "wangp_present": bool(ROOT and (ROOT / "wgp.py").is_file()),
                    "local_only": HOST in {"127.0.0.1", "localhost"},
                },
            )
            return
        if self.path.startswith("/jobs/"):
            job_id = self.path.rsplit("/", 1)[-1]
            with _JOBS_LOCK:
                job = _JOBS.get(job_id)
                if not job:
                    json_response(self, 404, {"error": "unknown job"})
                    return
                json_response(self, 200, dict(job))
            return
        json_response(self, 404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/generate":
            json_response(self, 404, {"error": "not found"})
            return
        if HOST not in {"127.0.0.1", "localhost"}:
            json_response(self, 400, {"error": "bridge must bind to localhost"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length > 128 * 1024:
                raise ValueError("request too large")
            payload = json.loads(self.rfile.read(length) or b"{}")
            settings = validate_settings(payload)
            with _JOBS_LOCK:
                if any(v["status"] in {"starting", "running"} for v in _JOBS.values()):
                    json_response(self, 409, {"error": "one WanGP job is already running"})
                    return
                job_id = str(uuid.uuid4())
                _JOBS[job_id] = {
                    "job_id": job_id,
                    "status": "queued",
                    "generated_files": [],
                    "errors": [],
                }
            threading.Thread(target=run_job, args=(job_id, settings), daemon=True).start()
            json_response(self, 202, {"job_id": job_id, "status": "queued"})
        except Exception as exc:
            json_response(self, 400, {"error": str(exc)})


def main() -> int:
    global ROOT, HOST, PORT
    parser = argparse.ArgumentParser(description="Local OpenReel -> WanGP bridge")
    parser.add_argument("--wangp-root", default=os.environ.get("WANGP_ROOT", ""))
    parser.add_argument("--host", default=HOST)
    parser.add_argument("--port", type=int, default=PORT)
    args = parser.parse_args()
    ROOT = Path(args.wangp_root).expanduser().resolve() if args.wangp_root else Path()
    HOST = args.host
    PORT = args.port
    if HOST not in {"127.0.0.1", "localhost"}:
        raise SystemExit("Refusing non-local bind. Keep the bridge on 127.0.0.1.")
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"OpenReel WanGP bridge: http://{HOST}:{PORT}")
    print(f"WanGP root: {ROOT}")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
