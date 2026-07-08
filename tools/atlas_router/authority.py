from __future__ import annotations

import re
from dataclasses import replace
from datetime import date
from typing import Any

from .models import ClassificationResult, RouterConfigurationError, RoutingDecision, WorkOrderRequest


SCHEMA_VERSION = "0.1.0"
DECIDED_BY = "tools/atlas_router/router.py"
KNOWN_PROJECTS = {"atlasstudio", "the-last-sword-protocol"}
REPOSITORY_BOUNDARIES: dict[str, dict[str, Any]] = {
    "canon": {
        "owner": "TheLastSwordProtocol-Atlas",
        "may_be_authored_by_atlasstudio": False,
    },
    "game_implementation": {
        "owner": "TheLastSwordProtocol-Game",
        "requires_explicit_approval": True,
    },
    "production_orchestration": {
        "owner": "AtlasStudio",
        "may_be_authored_by_atlasstudio": True,
    },
    "cross_repository_bridge": {
        "owner": "AtlasStudio",
        "may_be_authored_by_atlasstudio": True,
        "write_restricted_to": "bridges/",
    },
}


def route(request: WorkOrderRequest, classification: ClassificationResult) -> RoutingDecision:
    _assert_boundaries_loaded(classification.classification)
    today = date.today().isoformat()
    work_order_id = request.work_order_id or "WO-UNFILED"
    safety_flags = {"canon_leak_risk": False, "cross_repo_write_attempted": False}
    warnings: list[str] = []
    if request.project and request.project not in KNOWN_PROJECTS:
        warnings.append(f"unknown_project: '{request.project}' not found in Atlas Graph project list")

    if classification.classification == "ambiguous":
        reason = classification.ambiguous_reason or "no_signal_matched"
        rationale = ambiguous_rationale(reason, classification.conflicting_classifications)
        return RoutingDecision(
            schema_version=SCHEMA_VERSION,
            work_order_id=work_order_id,
            title=request.title,
            classification="ambiguous",
            target_repository="none",
            target_path_hint=None,
            routing_status="blocked_ambiguous",
            requires_explicit_approval=False,
            approved_by=None,
            approved_at=None,
            signals_matched=classification.signals_matched,
            rationale=rationale,
            safety_flags=safety_flags,
            created=today,
            decided_by=DECIDED_BY,
            warnings=warnings,
        )

    target_repository, target_path_hint = _target_for(classification.classification)
    routing_status = "routed"
    requires_explicit_approval = False
    approved_by = request.approved_by
    approved_at = request.approved_at

    if request.claimed_target_repository and request.claimed_target_repository != target_repository:
        if classification.classification == "canon" and request.claimed_target_repository == "AtlasStudio":
            routing_status = "rejected_authority_violation"
            safety_flags["canon_leak_risk"] = True
            warnings.append("claimed_target_repository ignored; canon can never route to AtlasStudio")

    if classification.classification == "game_implementation":
        requires_explicit_approval = True
        missing_packet = not has_implementation_packet(request)
        if missing_packet:
            warnings.append(
                "Cannot approve: no Atlas implementation packet (IMP-<AREA>-<NNN>) is cited in this request. Cite the packet this work implements before requesting approval."
            )
        if approved_by and not approved_at:
            approved_at = today
        if approved_by and approved_at and not missing_packet:
            target_repository = "TheLastSwordProtocol-Game"
            target_path_hint = None
            routing_status = "routed"
        else:
            target_repository = "AtlasStudio"
            target_path_hint = "work-orders/WO-NNNN-*.md"
            routing_status = "pending_approval"
        if mentions_hand_authored_risk(request):
            warnings.append(
                "protected_content: confirm map_ownership.json awareness before any approved game dispatch"
            )

    rationale = routed_rationale(classification, target_repository, routing_status)
    decision = RoutingDecision(
        schema_version=SCHEMA_VERSION,
        work_order_id=work_order_id,
        title=request.title,
        classification=classification.classification,
        target_repository=target_repository,
        target_path_hint=target_path_hint,
        routing_status=routing_status,
        requires_explicit_approval=requires_explicit_approval,
        approved_by=approved_by if routing_status == "routed" else None,
        approved_at=approved_at if routing_status == "routed" else None,
        signals_matched=classification.signals_matched,
        rationale=rationale,
        safety_flags=safety_flags,
        created=today,
        decided_by=DECIDED_BY,
        warnings=warnings,
    )
    return _check_forced_override(request, decision)


def _target_for(classification: str) -> tuple[str, str | None]:
    if classification == "canon":
        return ("TheLastSwordProtocol-Atlas", None)
    if classification == "game_implementation":
        return ("TheLastSwordProtocol-Game", None)
    if classification == "production_orchestration":
        return ("AtlasStudio", "work-orders/WO-NNNN-*.md")
    if classification == "cross_repository_bridge":
        return ("AtlasStudio", "bridges/")
    raise RouterConfigurationError(f"missing target mapping for {classification}")


def _check_forced_override(request: WorkOrderRequest, decision: RoutingDecision) -> RoutingDecision:
    if not request.claimed_target_repository:
        return decision
    if request.claimed_target_repository == decision.target_repository:
        return decision
    warnings = list(decision.warnings)
    if "claimed_target_repository ignored; classifier target wins" not in warnings:
        warnings.append("claimed_target_repository ignored; classifier target wins")
    return replace(decision, warnings=warnings)


def _assert_boundaries_loaded(classification: str) -> None:
    if not REPOSITORY_BOUNDARIES:
        raise RouterConfigurationError("repository authority boundaries are unavailable")
    if classification != "ambiguous" and classification not in REPOSITORY_BOUNDARIES:
        raise RouterConfigurationError(f"missing repository authority for {classification}")


def ambiguous_rationale(reason: str, conflicts: list[str]) -> str:
    if reason == "conflicting_repository_signals":
        joined = ", ".join(conflicts)
        return (
            f"This request matches signals for more than one repository ({joined}). "
            "Split it into one request per repository before resubmitting."
        )
    return (
        "No signal distinguishes canon, implementation, or orchestration scope. "
        "This request needs a named location, character, or content area, a named defect or file, "
        "or a named AtlasStudio system before it can be classified."
    )


def routed_rationale(
    classification: ClassificationResult,
    target_repository: str,
    routing_status: str,
) -> str:
    signal_text = "; ".join(classification.signals_matched) or "no signals"
    return (
        f"Classification `{classification.classification}` selected from signals: {signal_text}. "
        f"Target repository `{target_repository}` with routing status `{routing_status}`."
    )


def has_implementation_packet(request: WorkOrderRequest) -> bool:
    text = " ".join([request.title, request.purpose, *request.scope_in, *request.scope_out])
    return bool(re.search(r"\bIMP-[A-Z]+-\d{3}\b", text))


def mentions_hand_authored_risk(request: WorkOrderRequest) -> bool:
    text = " ".join([request.title, request.purpose, *request.scope_in, *request.scope_out]).lower()
    return "map001" in text and ("from scratch" in text or "regenerate" in text)
