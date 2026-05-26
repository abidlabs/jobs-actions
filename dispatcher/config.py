"""Configuration loaded from environment.

All settings are read once at import time. Values are validated where it's cheap
to do so; anything that requires a network call (e.g. verifying the HF token)
fails lazily on first use.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


def _required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(
            f"Missing required env var: {name}. "
            f"See setup/SETUP.md for the full list."
        )
    return value


def _optional(name: str, default: str) -> str:
    return os.environ.get(name, default).strip() or default


@dataclass(frozen=True)
class Settings:
    # GitHub App
    gh_app_id: str
    gh_app_private_key: str
    webhook_secret: str

    # HF
    hf_token: str
    hf_namespace: str  # who gets billed for jobs

    # Runner images
    runner_image_cpu: str
    runner_image_gpu: str

    # Behavior
    default_timeout: str  # "1h" etc.
    log_level: str

    @classmethod
    def from_env(cls) -> Settings:
        # PEM keys are typically multi-line. Allow `\n` literal in env for ease
        # of pasting into HF Space "Secrets" UI which is single-line.
        raw_key = _required("GH_APP_PRIVATE_KEY")
        if "\\n" in raw_key and "\n" not in raw_key:
            raw_key = raw_key.replace("\\n", "\n")

        return cls(
            gh_app_id=_required("GH_APP_ID"),
            gh_app_private_key=raw_key,
            webhook_secret=_required("GH_WEBHOOK_SECRET"),
            hf_token=_required("HF_TOKEN"),
            hf_namespace=_required("HF_NAMESPACE"),
            runner_image_cpu=_optional(
                "RUNNER_IMAGE_CPU",
                "ghcr.io/abidlabs/jobs-actions-runner:latest",
            ),
            runner_image_gpu=_optional(
                "RUNNER_IMAGE_GPU",
                "ghcr.io/abidlabs/jobs-actions-runner-gpu:latest",
            ),
            default_timeout=_optional("JOB_TIMEOUT", "1h"),
            log_level=_optional("LOG_LEVEL", "INFO"),
        )
