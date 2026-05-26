# Runner image

Docker image with the [`actions/runner`](https://github.com/actions/runner) binary preinstalled. The container registers ephemerally with GitHub on startup, picks up one queued job matching its labels, and exits.

## Variants

- `Dockerfile` — Ubuntu 22.04, CPU-only.
- `Dockerfile.gpu` — `nvidia/cuda:12.4.0-runtime-ubuntu22.04`, for GPU jobs.

## Building locally

```bash
docker buildx build --platform linux/amd64 \
    -t ghcr.io/<org>/jobs-actions-runner:latest \
    -f runner/Dockerfile runner/

docker buildx build --platform linux/amd64 \
    -t ghcr.io/<org>/jobs-actions-runner-gpu:latest \
    -f runner/Dockerfile.gpu runner/
```

HF Jobs runs Linux x86; if you're on Apple Silicon you must build for `linux/amd64`.

## Publishing

The repo's [`publish-runner-image.yml`](../.github/workflows/publish-runner-image.yml) workflow builds and pushes both variants to GHCR on push to `main` and on tag.

## Required env vars (set by dispatcher)

| Var | Purpose |
|---|---|
| `GH_REPO` | `"owner/name"` |
| `RUNNER_TOKEN` | One-shot registration token |
| `RUNNER_LABELS` | Comma-separated labels |
| `RUNNER_NAME` | Unique runner name |

## Notes

- The runner is configured with `--ephemeral`, so it deregisters after one job. No long-lived state.
- We pin `RUNNER_VERSION` (default `2.319.1`) and use `--disableupdate` to prevent the runner self-updating mid-job. Bump the pin in the Dockerfile when needed.
- `installdependencies.sh` is run at build time so `actions/runner` itself works, but workflow steps that need additional tools (Docker, Node, etc.) must install them themselves or use an image that includes them.
