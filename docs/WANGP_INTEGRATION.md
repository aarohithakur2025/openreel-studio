# WanGP backend integration

OpenReel Studio can use **WanGP** as an optional local generation backend.

## Why this backend

WanGP is a separate project that provides a Python API, headless queue
processing, model discovery, low-VRAM execution, and support for Wan 2.1/2.2
and other open models. Its documented Python API uses `shared.api.init(...)`
and `submit_task(...)`.

OpenReel does **not** bundle WanGP, copy its source, or silently install its
large model dependencies.

## License boundary

WanGP has its own **WanGP Community License 2.0**. That license permits Free
Use but restricts certain commercialization, hosted/API, and embedded uses
unless a separate written commercial license is obtained. Third-party models
and dependencies retain their own licenses.

This connector is intentionally an **optional local connector**: the user
installs WanGP separately and runs the bridge locally. Read the upstream
license before redistributing WanGP or using it in a paid hosted service.

When this backend is enabled, OpenReel documents that it uses WanGP, as
required by WanGP's API documentation.

## Safe local bridge

Start the bridge on the same machine as WanGP:

```bash
python tools/wangp_bridge.py --wangp-root /path/to/Wan2GP
```

Default endpoint:

```text
http://127.0.0.1:7861
```

Health check:

```text
GET /health
```

Submit one text-to-video job:

```json
POST /generate
{
  "model_type": "<model id from your WanGP installation>",
  "prompt": "cinematic golden-hour city street",
  "resolution": "832x480",
  "video_length": "5s",
  "force_fps": "24",
  "num_inference_steps": 20
}
```

Then poll:

```text
GET /jobs/<job_id>
```

## Safety rules

- localhost only; the bridge refuses non-local binding
- one active WanGP job at a time
- no automatic retry
- no credentials stored by the bridge
- model IDs/settings come from the user's installed WanGP version
- use an exported WanGP settings file as the authoritative model-specific
  template rather than guessing model flags

## Current scope

The first connector is deliberately T2V/settings-only. Image/video uploads,
model discovery, cancellation, and richer progress events are separate steps.
This avoids pretending that a generic settings payload works for every WanGP
model.

## Sources

- WanGP: https://github.com/deepbeepmeep/Wan2GP
- WanGP API: https://github.com/deepbeepmeep/Wan2GP/blob/main/docs/API.md
- WanGP settings: https://github.com/deepbeepmeep/Wan2GP/blob/main/docs/SETTINGS.md
- WanGP CLI: https://github.com/deepbeepmeep/Wan2GP/blob/main/docs/CLI.md
- WanGP license: https://github.com/deepbeepmeep/Wan2GP/blob/main/LICENSE.txt
