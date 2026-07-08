from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

from .models import DispatchOutcome, RoutingDecision


TOOL_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOL_DIR.parents[1]
DEFAULT_AUDIT_DIR = REPO_ROOT / "reports" / "atlas-router"


def audit_dir() -> Path:
    override = os.environ.get("ATLAS_ROUTER_AUDIT_DIR")
    return Path(override) if override else DEFAULT_AUDIT_DIR


def routing_log_path() -> Path:
    return audit_dir() / "routing-log.jsonl"


def corrections_path() -> Path:
    return audit_dir() / "corrections.jsonl"


def append_routing_record(decision: RoutingDecision, outcome: DispatchOutcome | None = None) -> None:
    record = decision.to_schema_dict()
    if outcome is not None:
        record["dispatch"] = outcome.to_dict()
    path = routing_log_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")


def read_routing_record(work_order_id: str) -> dict[str, Any] | None:
    path = routing_log_path()
    if not path.exists():
        return None
    result: dict[str, Any] | None = None
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            if record.get("work_order_id") == work_order_id:
                result = record
    return result


def prior_dispatch(idempotency_key: str) -> DispatchOutcome | None:
    path = routing_log_path()
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            dispatch = record.get("dispatch")
            if (
                isinstance(dispatch, dict)
                and dispatch.get("idempotency_key") == idempotency_key
                and dispatch.get("action") == "opened_github_issue"
            ):
                return DispatchOutcome.from_dict(dispatch)
    return None


def append_correction(
    work_order_id: str,
    original: str,
    corrected: str,
    reason: str,
    corrected_by: str,
) -> None:
    record = {
        "work_order_id": work_order_id,
        "original": original,
        "corrected": corrected,
        "reason": reason,
        "corrected_by": corrected_by,
        "corrected_at": datetime.now().isoformat(timespec="seconds"),
    }
    path = corrections_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
