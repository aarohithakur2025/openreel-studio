# A→Z generation plan

## 1. Prepare the backend

Install ComfyUI on a machine with a supported GPU. Use the official Wan2.2 ComfyUI workflow template and install the model files required by that workflow.

## 2. Connect safely

Run ComfyUI locally or on a private network. Do not publish an unauthenticated API endpoint.

## 3. Load a workflow

In ComfyUI, load the Wan2.2 TI2V-5B template and export it with **Save (API Format)**. The API format is a node-ID keyed object containing `class_type` and `inputs`.

## 4. Validate before execution

OpenReel checks:
- server reachability;
- backend node availability;
- workflow shape;
- presence of prompt/image nodes where required.

Validation happens before generation.

## 5. Execute one job

OpenReel uploads a reference image only when needed, patches the selected prompt inputs, submits exactly one `/prompt` request, records the returned `prompt_id`, and polls `/history/<prompt_id>` for a bounded period.

## 6. Verify output

A completed job must expose an output record before the UI reports success. A timeout is reported as a timeout; it is not silently retried.

## 7. Build longer reels

Wan2.2 short-video workflows should be treated as controlled chunks. For longer content, plan multiple shots and stitch verified outputs with FFmpeg.

## 8. Free-first policy

The core controller does not require a paid API. GPU/model availability depends on the user's own machine or a separately chosen free/open-source compute route. The project does not promise unlimited free GPU generation.

## Private repository boundary

This public project must not import, mirror, or modify `aarohithakur2025/empire-os`.
