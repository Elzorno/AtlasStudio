from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


CLASSIFICATIONS = (
    "canon",
    "game_implementation",
    "production_orchestration",
    "cross_repository_bridge",
    "ambiguous",
)
TARGET_REPOSITORIES = (
    "TheLastSwordProtocol-Atlas",
    "TheLastSwordProtocol-Game",
    "AtlasStudio",
    "none",
)
ROUTING_STATUSES = (
    "routed",
    "pending_approval",
    "blocked_ambiguous",
    "rejected_authority_violation",
)
TASK_CLASSES = (
    "creative_design",
    "architecture",
    "implementation",
    "repetitive_edit",
    "review_qa",
    "canon_decision",
)


class RouterConfigurationError(RuntimeError):
    """Raised when the router cannot prove repository authority boundaries."""


class GithubUnavailableError(RuntimeError):
    """Raised when GitHub issue creation is unavailable."""


class NetworkError(RuntimeError):
    """Raised when GitHub cannot be reached deterministically."""


@dataclass
class WorkOrderRequest:
    source_path: str | None
    work_order_id: str | None
    title: str
    project: str
    purpose: str
    scope_in: list[str] = field(default_factory=list)
    scope_out: list[str] = field(default_factory=list)
    required_capabilities: list[str] = field(default_factory=list)
    preferred_capabilities: list[str] = field(default_factory=list)
    risk_level: str = "medium"
    player_facing: bool = False
    engine_specific: bool = False
    claimed_target_repository: str | None = None
    approved_by: str | None = None
    approved_at: str | None = None
    agent_role: str | None = None
    recommended_agent: str | None = None
    task_class: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_path": self.source_path,
            "work_order_id": self.work_order_id,
            "title": self.title,
            "project": self.project,
            "purpose": self.purpose,
            "scope_in": self.scope_in,
            "scope_out": self.scope_out,
            "required_capabilities": self.required_capabilities,
            "preferred_capabilities": self.preferred_capabilities,
            "risk_level": self.risk_level,
            "player_facing": self.player_facing,
            "engine_specific": self.engine_specific,
            "claimed_target_repository": self.claimed_target_repository,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at,
            "agent_role": self.agent_role,
            "recommended_agent": self.recommended_agent,
            "task_class": self.task_class,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "WorkOrderRequest":
        return cls(
            source_path=data.get("source_path"),
            work_order_id=data.get("work_order_id"),
            title=str(data.get("title", "")),
            project=str(data.get("project", "atlasstudio")),
            purpose=str(data.get("purpose", data.get("title", ""))),
            scope_in=listify(data.get("scope_in", [])),
            scope_out=listify(data.get("scope_out", [])),
            required_capabilities=listify(data.get("required_capabilities", [])),
            preferred_capabilities=listify(data.get("preferred_capabilities", [])),
            risk_level=str(data.get("risk_level", "medium")),
            player_facing=bool(data.get("player_facing", False)),
            engine_specific=bool(data.get("engine_specific", False)),
            claimed_target_repository=data.get("claimed_target_repository")
            or data.get("target_repository"),
            approved_by=data.get("approved_by"),
            approved_at=data.get("approved_at"),
            agent_role=data.get("agent_role"),
            recommended_agent=data.get("recommended_agent"),
            task_class=data.get("task_class"),
        )


@dataclass(frozen=True)
class ClassificationResult:
    classification: str
    signals_matched: list[str]
    conflicting_classifications: list[str] = field(default_factory=list)
    ambiguous_reason: str | None = None

    def __post_init__(self) -> None:
        if self.classification not in CLASSIFICATIONS:
            raise ValueError(f"unknown classification: {self.classification}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "classification": self.classification,
            "signals_matched": self.signals_matched,
            "conflicting_classifications": self.conflicting_classifications,
            "ambiguous_reason": self.ambiguous_reason,
        }


@dataclass
class SchedulerRecommendation:
    task_class: str
    primary_agent: str | None
    primary_provider: str | None
    score: int | None
    components: dict[str, int] = field(default_factory=dict)
    fallbacks: list[dict[str, Any]] = field(default_factory=list)
    excluded: list[dict[str, str]] = field(default_factory=list)
    advisory: bool = False
    evidence: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_class": self.task_class,
            "primary_agent": self.primary_agent,
            "primary_provider": self.primary_provider,
            "score": self.score,
            "components": self.components,
            "fallbacks": self.fallbacks,
            "excluded": self.excluded,
            "advisory": self.advisory,
            "evidence": self.evidence,
        }


@dataclass
class RoutingDecision:
    schema_version: str
    work_order_id: str
    title: str
    classification: str
    target_repository: str
    target_path_hint: str | None
    routing_status: str
    requires_explicit_approval: bool
    approved_by: str | None
    approved_at: str | None
    signals_matched: list[str]
    rationale: str
    safety_flags: dict[str, bool]
    created: str
    decided_by: str
    scheduler_recommendation: SchedulerRecommendation | None = None
    warnings: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.classification not in CLASSIFICATIONS:
            raise ValueError(f"unknown classification: {self.classification}")
        if self.target_repository not in TARGET_REPOSITORIES:
            raise ValueError(f"unknown target repository: {self.target_repository}")
        if self.routing_status not in ROUTING_STATUSES:
            raise ValueError(f"unknown routing status: {self.routing_status}")

    def to_schema_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "schema_version": self.schema_version,
            "work_order_id": self.work_order_id,
            "title": self.title,
            "classification": self.classification,
            "target_repository": self.target_repository,
            "routing_status": self.routing_status,
            "requires_explicit_approval": self.requires_explicit_approval,
            "signals_matched": self.signals_matched,
            "rationale": self.rationale,
            "safety_flags": self.safety_flags,
            "created": self.created,
            "decided_by": self.decided_by,
        }
        if self.target_path_hint is not None:
            data["target_path_hint"] = self.target_path_hint
        if self.approved_by is not None:
            data["approved_by"] = self.approved_by
        if self.approved_at is not None:
            data["approved_at"] = self.approved_at
        return data

    def to_full_dict(self) -> dict[str, Any]:
        data = self.to_schema_dict()
        data["warnings"] = self.warnings
        if self.scheduler_recommendation is not None:
            data["scheduler_recommendation"] = self.scheduler_recommendation.to_dict()
        return data


@dataclass(frozen=True)
class DispatchOutcome:
    action: str
    target_repository: str
    path_or_url: str | None
    dispatched_at: str | None
    idempotency_key: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "action": self.action,
            "target_repository": self.target_repository,
            "path_or_url": self.path_or_url,
            "dispatched_at": self.dispatched_at,
            "idempotency_key": self.idempotency_key,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DispatchOutcome":
        return cls(
            action=str(data.get("action", "")),
            target_repository=str(data.get("target_repository", "")),
            path_or_url=data.get("path_or_url"),
            dispatched_at=data.get("dispatched_at"),
            idempotency_key=str(data.get("idempotency_key", "")),
        )


def listify(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, tuple):
        return [str(item) for item in value]
    if isinstance(value, str) and "," in value:
        return [item.strip() for item in value.split(",") if item.strip()]
    if isinstance(value, str) and value:
        return [value]
    return []
