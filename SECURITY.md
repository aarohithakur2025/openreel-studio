# Security

- Do not commit API keys, access tokens, cookies, private workflow credentials, or personal data.
- Do not expose an unauthenticated ComfyUI endpoint to the public internet.
- Prefer localhost, a private LAN, or an authenticated tunnel.
- Browser project state is local-only.
- Generation is intentionally one-job-at-a-time with bounded polling and no blind retry loop.
- Public issues and pull requests should contain sanitized logs only.
