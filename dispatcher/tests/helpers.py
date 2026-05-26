"""Helpers for crafting realistic GitHub webhook payloads + signatures."""

from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any


def sign(body: bytes, secret: str) -> str:
    return "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()


def workflow_job_payload(
    *,
    action: str = "queued",
    labels: list[str] | None = None,
    repo: str = "owner/repo",
    installation_id: int | None = 1,
    run_id: int = 100,
    job_id: int = 200,
    conclusion: str | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "action": action,
        "workflow_job": {
            "id": job_id,
            "run_id": run_id,
            "labels": labels or ["hf-jobs-cpu-basic"],
            "status": "queued" if action == "queued" else "completed",
            "conclusion": conclusion,
        },
        "repository": {"full_name": repo},
    }
    if installation_id is not None:
        payload["installation"] = {"id": installation_id}
    return payload


def encode(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, separators=(",", ":")).encode()
