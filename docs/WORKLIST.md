# OpenReel Studio — System Worklist

Updated: 2026-10-01

## Operating rules

- Keep `aarohithakur2025/empire-os` private and untouched for this project.
- Public work belongs in `openreel-studio`.
- No paid credits, subscriptions, paid APIs, or paid GPU by default.
- Never blind-retry a failed job.
- Validate locally/contractually before changing GitHub.
- One controlled generation attempt at a time.
- Never call a feature complete until the artifact/test result is verified.
- Keep credentials and model weights out of Git.
- Separate planning/control-plane code from GPU/model backends.

## Completed

### Repository foundation
- [x] Public `openreel-studio` repository created.
- [x] README, SECURITY, CONTRIBUTING, CODE_OF_CONDUCT, MIT license and .gitignore.
- [x] Issue templates.
- [x] Deterministic Python validation bot.
- [x] GitHub Actions validation workflow.
- [x] Push-trigger spam fixed: validation is now manual/PR-only.
- [x] Maintenance bot changed to manual-only.
- [x] `empire-os` remained private/untouched.

### OpenReel controller
- [x] Local-first web UI.
- [x] 9:16 / 16:9 / 1:1 planning.
- [x] Prompt builder.
- [x] ComfyUI `/system_stats` and `/object_info` checks.
- [x] API-format workflow validation.
- [x] Reference-image upload path.
- [x] One-job-at-a-time submission.
- [x] Bounded history polling.
- [x] Output-link extraction.
- [x] Dry-run/mock backend verification.
- [x] No blind retry loop.

### Wan2.2 / backend research
- [x] Wan2.2 + ComfyUI path researched.
- [x] Wan2.2 5B chunking reality documented; do not label one ~5-second sample as a 20-second render.
- [x] Kaggle Wan2.2 helper/notebook package prepared.
- [x] WanGP audited as a backend candidate.
- [x] Optional localhost-only WanGP Python bridge added.
- [x] WanGP license boundary documented; WanGP is not bundled/copied into OpenReel.

## Pending — ordered execution

### P0 — Real backend proof
- [ ] Run WanGP bridge health check against an actual WanGP installation.
- [ ] Discover actual installed model IDs/settings; do not guess flags.
- [ ] Run one controlled real GPU generation.
- [ ] Verify resulting MP4 with ffprobe and inspect duration/fps/resolution.
- [ ] Record hardware, VRAM, model, resolution, steps, time and failure mode.
- [ ] Add I2V/reference-image support only after T2V path is proven.

### P0 — Free GPU safety lane
- [ ] Keep GitHub as source/control/CI, not as the video GPU.
- [ ] Prefer already-free/eligible external GPU routes: Kaggle notebook path and eligible NVIDIA program credits.
- [ ] Audit NVIDIA Inception/Connect eligibility before relying on any cloud credit.
- [ ] Treat Hugging Face ZeroGPU as a limited test route, not the main long-render backend.
- [ ] Never enable paid GPU/larger GitHub runners.
- [ ] Add explicit quota/cost preflight before any external GPU job.
- [ ] Add timeout + output-size guardrails.
- [ ] Add a backend capability matrix so the controller knows which backend can actually run a requested job.

### P1 — Backend abstraction
- [ ] Create a common backend contract: health, capabilities, submit, status, output, error.
- [ ] Implement ComfyUI adapter under that contract.
- [ ] Implement WanGP adapter under that contract.
- [ ] Add Kaggle/remote execution as a separate job handoff, not as a hidden dependency.
- [ ] Add backend selection based on verified capabilities, VRAM/quota and user-selected constraints.
- [ ] Never silently fall back from one backend to another.

### P1 — Production video pipeline
- [ ] Shot/scene schema.
- [ ] Multi-chunk reel planner.
- [ ] Consistent character/reference handling.
- [ ] FFmpeg stitch pipeline.
- [ ] Audio/music placeholder pipeline with copyright-safe inputs.
- [ ] Final 9:16 export validation.
- [ ] Render manifest containing model/settings/source/backend/output checksums.

### P1 — Reliability / security
- [ ] Add preflight gate before every generation.
- [ ] Validate model availability, disk space, VRAM/quota and required nodes before submission.
- [ ] Add structured job states: queued → running → completed/failed/cancelled.
- [ ] Add cancellation support where backend permits it.
- [ ] Keep logs bounded and redact secrets.
- [ ] Add regression tests for each backend contract.
- [ ] Keep GitHub Actions manual/PR-only unless a real need for automation is proven.

### P2 — Public project growth
- [ ] GitHub Pages/demo landing page.
- [ ] Screenshots/GIF of the verified workflow.
- [ ] Clear quick-start for Windows/Linux/Kaggle.
- [ ] Contributor guide and good first issues.
- [ ] Upstream attribution/source matrix.
- [ ] Release tags only after verified milestones.
- [ ] Optional sponsor/donation documentation later; no fake earning claims.

### P2 — Monetization readiness
- [ ] First prove reproducible free generation.
- [ ] Then package a useful open-source tool/workflow.
- [ ] Measure stars, forks, issues, demo usage and repeatable outputs.
- [ ] Consider ethical monetization around support, hosted convenience or templates only where upstream/model licenses permit it.
- [ ] Do not monetize or host WanGP-derived functionality in a way prohibited by its current license.

## GPU/backend decision record

### GitHub
Use for source code, validation and public CI. Standard GitHub-hosted runners are free for public repositories; larger GPU runners are not the free path.

### NVIDIA
Potential credit source only after eligibility is verified. NVIDIA documents free cloud-credit opportunities for eligible Inception/Connect members through cloud partners. No assumption of automatic credits.

### Kaggle
Prepared as a practical free-GPU execution lane for Wan2.2 experiments. Real execution still requires the user's Kaggle session and available quota/hardware.

### Hugging Face ZeroGPU
Useful for short tests, but free accounts have a daily GPU quota. Do not make it the main backend for long video generation.

### WanGP
Optional local/eligible GPU backend. Strong candidate for low-VRAM execution, but model-specific hardware/time must be measured rather than assumed.

## Current truth

The control plane is substantially built and contract-tested. The major unproven milestone is **real GPU generation on a live backend**. Until that happens, OpenReel is a verified controller/planner, not a verified end-to-end free AI video factory.
