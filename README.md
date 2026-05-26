# jobs-actions

Run your GitHub Actions workflows on **Hugging Face Jobs** with a one-line change:

```yaml
jobs:
  train:
    runs-on: hf-jobs-a10g-small   # was: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python train.py
```

GPU CI for the price of a Hub subscription. No self-hosted runner infrastructure to babysit.

## Why

GitHub-hosted runners don't sell GPU minutes at a sane price. HF Jobs does. This bridges the two: GitHub Actions stays in charge of orchestration, YAML, secrets, and the Checks UI; HF Jobs provides the actual compute.

| | GitHub-hosted | jobs-actions (HF Jobs) | Self-hosted on EC2 |
|---|---|---|---|
| GPU access | ❌ (limited beta only) | ✅ T4, A10G, A100, H200, L4, L40s | ✅ DIY |
| Cold start | ~5–15s | ~30–90s | ~0s (warm pool) |
| Idle cost | $0 | $0 (ephemeral) | $$ |
| Setup | None | 5-minute one-time install | Days |

## How it works

```
PR push
  → GitHub fires `workflow_job.queued` webhook
  → Dispatcher (HF Space) receives it, sees `runs-on: hf-jobs-*` label
  → Mints a one-shot GitHub Actions runner registration token
  → Launches an HF Job with the runner image + that token
  → Runner registers ephemerally, GitHub dispatches the job to it
  → Runner exits after one job, container terminates
```

Three pieces:

- **`dispatcher/`** — FastAPI service that handles GitHub webhooks and dispatches HF Jobs. Deploys to an HF Space.
- **`runner/`** — Docker images (CPU + GPU) with the GitHub Actions runner binary baked in.
- **`setup/`** — GitHub App manifest and setup walkthrough.

## Supported labels

| Label | HF Jobs flavor | Notes |
|---|---|---|
| `hf-jobs-cpu` | `cpu-basic` | 2 vCPU, 16GB RAM |
| `hf-jobs-cpu-upgrade` | `cpu-upgrade` | 8 vCPU, 32GB RAM |
| `hf-jobs-cpu-performance` | `cpu-performance` | Performance CPU tier |
| `hf-jobs-cpu-xl` | `cpu-xl` | Highest CPU tier |
| `hf-jobs-t4-small` | `t4-small` | T4 GPU (cheapest) |
| `hf-jobs-t4-medium` | `t4-medium` | T4 GPU, more RAM |
| `hf-jobs-l4x1` | `l4x1` | 1× L4 GPU |
| `hf-jobs-l4x4` | `l4x4` | 4× L4 GPU |
| `hf-jobs-a10g-small` | `a10g-small` | A10G GPU |
| `hf-jobs-a10g-large` | `a10g-large` | A10G, more RAM |
| `hf-jobs-a10g-largex2` | `a10g-largex2` | 2× A10G |
| `hf-jobs-a10g-largex4` | `a10g-largex4` | 4× A10G |
| `hf-jobs-a100-large` | `a100-large` | A100 GPU |
| `hf-jobs-l40sx1` | `l40sx1` | 1× L40s |
| `hf-jobs-h200` | `h200` | H200 GPU |

## Setup

See [`setup/SETUP.md`](setup/SETUP.md) for the one-time install. Roughly:

1. Deploy the dispatcher to an HF Space.
2. Create a GitHub App from the manifest in `setup/app-manifest.json`.
3. Set the webhook URL to your Space + paste secrets into Space settings.
4. Install the App on your repo.
5. Change `runs-on:` in your workflow.

## Status

- ✅ End-to-end dispatcher implementation
- ✅ Runner images (CPU + GPU)
- ✅ Test coverage of dispatcher critical paths
- ✅ One-click HF Space deploy
- ✅ Setup walkthrough
- ⏳ Pre-warmed runner pool (planned)
- ⏳ Cost dashboard (planned)

## License

Apache 2.0
