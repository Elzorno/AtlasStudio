from __future__ import annotations

import hashlib
import re
from datetime import datetime
from pathlib import Path

from . import audit, github
from .models import DispatchOutcome, RoutingDecision, SchedulerRecommendation, WorkOrderRequest


TOOL_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOL_DIR.parents[1]


def dispatch(
    request: WorkOrderRequest,
    routing: RoutingDecision,
    recommendation: SchedulerRecommendation | None,
    *,
    dry_run: bool,
    force_reissue: bool = False,
) -> DispatchOutcome:
    idempotency_key = _idempotency_key(routing)
    if routing.routing_status in {"blocked_ambiguous", "rejected_authority_violation"}:
        return DispatchOutcome(
            action="no_action_blocked",
            target_repository=routing.target_repository,
            path_or_url=None,
            dispatched_at=None,
            idempotency_key=idempotency_key,
        )
    if routing.routing_status == "pending_approval":
        preview_path = _preview_path(routing)
        return DispatchOutcome(
            action="would_write_local_work_order" if dry_run else "no_action_pending_approval",
            target_repository=routing.target_repository,
            path_or_url=str(preview_path.relative_to(REPO_ROOT)),
            dispatched_at=None,
            idempotency_key=idempotency_key,
        )
    if routing.target_repository == "AtlasStudio":
        work_orders_dir = REPO_ROOT / "work-orders"
        work_order_id = _next_work_order_id(work_orders_dir)
        path = work_orders_dir / f"{work_order_id}-{slugify(request.title)}.md"
        rendered = _render_work_order_markdown(request, routing, recommendation, work_order_id)
        if dry_run:
            return DispatchOutcome(
                action="would_write_local_work_order",
                target_repository="AtlasStudio",
                path_or_url=str((_preview_path(routing)).relative_to(REPO_ROOT)),
                dispatched_at=None,
                idempotency_key=idempotency_key,
            )
        path.write_text(rendered, encoding="utf-8")
        return DispatchOutcome(
            action="wrote_local_work_order",
            target_repository="AtlasStudio",
            path_or_url=str(path.relative_to(REPO_ROOT)),
            dispatched_at=datetime.now().isoformat(timespec="seconds"),
            idempotency_key=idempotency_key,
        )
    if routing.target_repository in {"TheLastSwordProtocol-Atlas", "TheLastSwordProtocol-Game"}:
        prior = None if force_reissue else audit.prior_dispatch(idempotency_key)
        if prior is not None:
            return prior
        if dry_run:
            return DispatchOutcome(
                action="would_open_github_issue",
                target_repository=routing.target_repository,
                path_or_url=f"github://{routing.target_repository}/issues/new",
                dispatched_at=None,
                idempotency_key=idempotency_key,
            )
        url = github.open_issue(
            routing.target_repository,
            request.title,
            _render_github_issue_body(request, routing, recommendation),
            labels=["atlas-router", routing.classification],
        )
        return DispatchOutcome(
            action="opened_github_issue",
            target_repository=routing.target_repository,
            path_or_url=url,
            dispatched_at=datetime.now().isoformat(timespec="seconds"),
            idempotency_key=idempotency_key,
        )
    return DispatchOutcome(
        action="no_action_blocked",
        target_repository=routing.target_repository,
        path_or_url=None,
        dispatched_at=None,
        idempotency_key=idempotency_key,
    )


def _next_work_order_id(work_orders_dir: Path) -> str:
    highest = 0
    for path in work_orders_dir.glob("WO-*.md"):
        match = re.match(r"WO-(\d{4})", path.name)
        if match:
            highest = max(highest, int(match.group(1)))
    return f"WO-{highest + 1:04d}"


def _render_work_order_markdown(
    request: WorkOrderRequest,
    routing: RoutingDecision,
    recommendation: SchedulerRecommendation | None,
    work_order_id: str,
) -> str:
    agent = recommendation.primary_agent.removeprefix("agent.") if recommendation and recommendation.primary_agent else "atlasstudio"
    agent = agent.replace("_", "-")
    scope_in = "\n".join(f"- {item}" for item in (request.scope_in or [request.purpose]))
    scope_out = "\n".join(f"- {item}" for item in (request.scope_out or ["Direct sibling-repository writes."]))
    return f"""---
work_order_id: {work_order_id}
title: {request.title}
status: proposed
project: {request.project}
recommended_agent: {agent}
agent_role: implementation-engineer
risk_level: {request.risk_level}
player_facing: {str(request.player_facing).lower()}
engine_specific: {str(request.engine_specific).lower()}
classification: {routing.classification}
target_repository: {routing.target_repository}
routing_status: {routing.routing_status}
requires_explicit_approval: {str(routing.requires_explicit_approval).lower()}
created: {routing.created}
---

# {work_order_id} - {request.title}

## Purpose

{request.purpose}

## Player-Facing Goal

Indirect unless this request is later accepted by the target repository's own process.

## Background

Generated by the Work Order Router from {request.source_path or "an inline request"}.

## Scope

### In Scope

{scope_in}

### Out of Scope

{scope_out}

## Inputs

- Routing classification: {routing.classification}
- Routing rationale: {routing.rationale}

## Deliverables

- Proposed AtlasStudio work order or implementation contract.

## Acceptance Criteria

- The routed work stays inside the target repository authority boundary.
- No sibling repository is modified directly.

## Verification Steps

```bash
python3 tools/atlas_format/format_guard.py --check
```

## Allowed Changes

- AtlasStudio paths named by this work order after human review.

## Protected Areas

- Do not modify TheLastSwordProtocol-Atlas or TheLastSwordProtocol-Game directly.
- Do not modify canon.

## Notes for Assigned Agent

Use the original request as source context; do not expand canon or implementation content beyond the approved source.
"""


def _render_github_issue_body(
    request: WorkOrderRequest,
    routing: RoutingDecision,
    recommendation: SchedulerRecommendation | None,
) -> str:
    lines = [
        "Filed by AtlasStudio Work Order Router.",
        "",
        "Original request:",
        request.purpose,
        "",
        f"Classification: {routing.classification}",
        f"Routing rationale: {routing.rationale}",
        "Safety: AtlasStudio did not write to this repository.",
    ]
    if recommendation is not None:
        lines.append(
            f"Scheduler recommendation: {recommendation.primary_agent} (advisory={recommendation.advisory})"
        )
    return "\n".join(lines)


def _preview_path(routing: RoutingDecision) -> Path:
    return REPO_ROOT / "reports" / "atlas-router" / "previews" / f"{routing.work_order_id}.md"


def _idempotency_key(routing: RoutingDecision) -> str:
    seed = f"{routing.work_order_id}:{routing.classification}:{routing.target_repository}"
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16]


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:72] or "untitled"
