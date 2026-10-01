# OpenReel Studio

Open-source, local-first control plane for AI video generation with ComfyUI and Wan2.2.

## Architecture

- **Web UI** — project/shot planning, prompt building, backend checks, validation, controlled job submission.
- **Optional WanGP connector** — localhost-only Python bridge to an separately installed WanGP runtime; no WanGP source or model weights are bundled.
- **Python validation bot** — deterministic repository and ComfyUI API-contract checks; no blind retries.
- **ComfyUI adapter** — uses the documented `/system_stats`, `/object_info`, `/prompt`, `/history/<prompt_id>` flow.
- **Wan2.2 workflow layer** — accepts an API-format workflow exported from ComfyUI.
- **CI gate** — syntax, Python compile, JSON validation and security-policy checks on every push/PR.

## Safety / operating model

1. No paid API is required by the core project.
2. No credentials are stored in project JSON or source.
3. One controlled generation submission at a time.
4. Polling is bounded; failed jobs are surfaced instead of retried blindly.
5. UI/graph workflow JSON is not silently treated as API-format JSON.
6. Never expose an unauthenticated ComfyUI server to the public internet.
7. This public repository is independent of the private `aarohithakur2025/empire-os` repository.

## Quick start

Open `openreel-studio/index.html` locally, or serve the folder with any static HTTP server. Connect it to a ComfyUI instance, import a **Save (API Format)** workflow, run the validation gate, then submit one job.

For local verification:

```bash
python tools/mock_comfy_server.py
python tools/verify_backend.py http://127.0.0.1:8189
```

Expected result ends with `OUTPUT: PASS`.

## Generation reality

Wan2.2 TI2V-5B is a chunked video workflow. OpenReel does not claim that one short model sample is a 20-second render. Longer reels should be planned as controlled chunks and stitched with FFmpeg.

See [docs/GENERATION_PLAN.md](docs/GENERATION_PLAN.md), [docs/WANGP_INTEGRATION.md](docs/WANGP_INTEGRATION.md), and [docs/SOURCES.md](docs/SOURCES.md).

## License

MIT.
