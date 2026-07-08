from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

from .models import (
    ClassificationResult,
    RoutingDecision,
    SchedulerRecommendation,
    WorkOrderRequest,
)


TOOL_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOL_DIR.parents[1]
DEFAULT_STATUS_PATH = REPO_ROOT / "studio" / "scheduling" / "agent-status.json"
EXAMPLE_STATUS_PATH = REPO_ROOT / "studio" / "scheduling" / "agent-status.example.json"
RISK_LEVELS = {"low": 1, "medium": 2, "high": 3}
CAPABILITY_TABLE: dict[str, dict[str, int]] = {
    "agent.gpt": {
        "creative_design": 3,
        "architecture": 0,
        "implementation": 0,
        "repetitive_edit": 0,
        "review_qa": 1,
        "canon_decision": 0,
    },
    "agent.claude_code": {
        "creative_design": 1,
        "architecture": 3,
        "implementation": 2,
        "repetitive_edit": 0,
        "review_qa": 2,
        "canon_decision": 0,
    },
    "agent.codex": {
        "creative_design": 0,
        "architecture": 1,
        "implementation": 3,
        "repetitive_edit": 2,
        "review_qa": 2,
        "canon_decision": 0,
    },
    "agent.github_copilot": {
        "creative_design": 0,
        "architecture": 0,
        "implementation": 1,
        "repetitive_edit": 3,
        "review_qa": 0,
        "canon_decision": 0,
    },
    "agent.ollama": {
        "creative_design": 1,
        "architecture": 0,
        "implementation": 1,
        "repetitive_edit": 2,
        "review_qa": 3,
        "canon_decision": 0,
    },
}
AGENT_PROFILES: dict[str, dict[str, Any]] = {
    "agent.gpt": {
        "provider": "provider.openai",
        "risk_ceiling": "medium",
        "context_depth": "deep",
        "scarcity": "high",
    },
    "agent.claude_code": {
        "provider": "provider.anthropic",
        "risk_ceiling": "high",
        "context_depth": "deep",
        "scarcity": "high",
    },
    "agent.codex": {
        "provider": "provider.openai",
        "risk_ceiling": "medium",
        "context_depth": "medium",
        "scarcity": "medium",
    },
    "agent.github_copilot": {
        "provider": "provider.github_copilot",
        "risk_ceiling": "low",
        "context_depth": "shallow",
        "scarcity": "medium",
    },
    "agent.ollama": {
        "provider": "provider.ollama",
        "risk_ceiling": "low",
        "context_depth": "medium",
        "scarcity": "none",
    },
}


def task_class_for(request: WorkOrderRequest, classification: ClassificationResult) -> str:
    text = f"{request.title} {request.purpose}".lower()
    if request.task_class:
        return request.task_class
    if classification.classification == "canon":
        if any(verb in text for verb in ("decide", "resolve", "finalize", "canonize")):
            return "canon_decision"
        return "creative_design"
    if classification.classification == "game_implementation":
        return "implementation"
    if classification.classification == "cross_repository_bridge":
        if any(word in text for word in ("summary", "summarize", "report")):
            return "review_qa"
        return "architecture"
    if classification.classification == "production_orchestration":
        return _production_task_class(request)
    raise ValueError("scheduler is not called for ambiguous requests")


def load_agent_status(path: Path | None = None) -> dict[str, dict[str, Any]]:
    selected_path = path or DEFAULT_STATUS_PATH
    used_example = False
    if not selected_path.exists():
        selected_path = EXAMPLE_STATUS_PATH
        used_example = True
    data = json.loads(selected_path.read_text("utf-8"))
    agents: dict[str, dict[str, Any]] = {}
    for entry in data.get("agents", []):
        if not isinstance(entry, dict) or "id" not in entry:
            continue
        normalized = dict(entry)
        normalized["_status_source"] = str(selected_path)
        normalized["_used_example"] = used_example
        normalized["availability"] = _degraded_availability(normalized)
        agents[str(entry["id"])] = normalized
    return agents


def recommend(
    request: WorkOrderRequest,
    classification: ClassificationResult,
    routing: RoutingDecision,
    status_path: Path | None = None,
) -> SchedulerRecommendation:
    task_class = task_class_for(request, classification)
    if task_class == "canon_decision":
        return SchedulerRecommendation(
            task_class=task_class,
            primary_agent="agent.human",
            primary_provider=None,
            score=None,
            advisory=True,
            evidence=["canon_decision work routes to agent.human for final authority"],
        )

    status = load_agent_status(status_path)
    used_example = any(entry.get("_used_example") for entry in status.values())
    advisory = routing.target_repository != "AtlasStudio" or used_example
    effective_risk = (
        "low"
        if task_class == "repetitive_edit" and request.risk_level == "medium"
        else request.risk_level
    )
    excluded: list[dict[str, str]] = []
    candidates: list[dict[str, Any]] = []

    for agent_id, profile in AGENT_PROFILES.items():
        capability = CAPABILITY_TABLE[agent_id][task_class]
        if capability == 0:
            excluded.append({"agent": agent_id, "reason": f"capability 0 for {task_class}"})
            continue
        risk_ceiling = profile["risk_ceiling"]
        if RISK_LEVELS.get(risk_ceiling, 0) < RISK_LEVELS.get(effective_risk, 2):
            excluded.append(
                {
                    "agent": agent_id,
                    "reason": f"risk ceiling {risk_ceiling} below {effective_risk}",
                }
            )
            continue
        agent_status = status.get(agent_id, {"availability": "unknown"})
        availability = agent_status.get("availability", "unknown")
        if availability in {"exhausted", "offline"}:
            excluded.append({"agent": agent_id, "reason": f"availability {availability}"})
            continue
        if availability in {"limited", "unknown"} and capability < 3:
            excluded.append(
                {
                    "agent": agent_id,
                    "reason": f"availability {availability} requires capability 3",
                }
            )
            continue
        components = _components(agent_id, task_class, effective_risk, availability)
        candidates.append(
            {
                "agent": agent_id,
                "provider": profile["provider"],
                "score": sum(components.values()),
                "components": components,
                "conditions": _conditions(capability, availability),
                "evidence": [
                    f"{agent_id.removeprefix('agent.')} capability {capability} for {task_class}",
                    f"{agent_id.removeprefix('agent.')} availability: {availability}",
                    f"risk {effective_risk} within {agent_id.removeprefix('agent.')} risk ceiling {profile['risk_ceiling']}",
                ],
            }
        )

    candidates.sort(
        key=lambda item: (
            -item["score"],
            -_quota_conservation_raw(item["agent"]),
            item["agent"],
        )
    )
    if not candidates:
        return SchedulerRecommendation(
            task_class=task_class,
            primary_agent=None,
            primary_provider=None,
            score=None,
            excluded=excluded,
            advisory=advisory,
            evidence=["No agent passed capability, risk, and availability filters."],
        )

    primary = candidates[0]
    evidence = list(primary["evidence"])
    if used_example:
        evidence.append("no live agent-status.json found; using agent-status.example.json for illustrative scoring only")
    return SchedulerRecommendation(
        task_class=task_class,
        primary_agent=primary["agent"],
        primary_provider=primary["provider"],
        score=primary["score"],
        components=primary["components"],
        fallbacks=[
            {
                "agent": item["agent"],
                "provider": item["provider"],
                "score": item["score"],
                "conditions": item["conditions"],
            }
            for item in candidates[1:]
        ],
        excluded=excluded,
        advisory=advisory,
        evidence=evidence,
    )


def _production_task_class(request: WorkOrderRequest) -> str:
    if request.agent_role == "senior-software-architect":
        return "architecture"
    if request.agent_role == "implementation-engineer":
        return "implementation"
    if request.agent_role == "creative-systems-designer":
        return "creative_design"
    if request.agent_role == "qa-reviewer":
        return "review_qa"
    if request.engine_specific:
        return "implementation"
    capabilities = {capability.lower() for capability in request.required_capabilities}
    if capabilities & {"architecture-review", "schema-design", "graph-analysis"}:
        return "architecture"
    if "implementation" in capabilities:
        return "implementation"
    text = f"{request.title} {request.purpose}".lower()
    if any(word in text for word in ("rename", "copy", "format")):
        return "repetitive_edit"
    if any(word in text for word in ("story", "quest", "dialogue", "region", "npc")):
        return "creative_design"
    if any(word in text for word in ("design", "architecture", "model")):
        return "architecture"
    if any(word in text for word in ("implement", "script", "tool", "export")):
        return "implementation"
    if any(word in text for word in ("lint", "audit", "review", "consistency", "summary", "report")):
        return "review_qa"
    return "implementation"


def _degraded_availability(entry: dict[str, Any]) -> str:
    availability = str(entry.get("availability", "unknown"))
    last_verified = entry.get("last_verified")
    if not last_verified:
        return "unknown"
    try:
        verified = date.fromisoformat(str(last_verified))
    except ValueError:
        return "unknown"
    if (date.today() - verified).days > 7:
        return "unknown"
    return availability


def _components(agent_id: str, task_class: str, risk_level: str, availability: str) -> dict[str, int]:
    capability = CAPABILITY_TABLE[agent_id][task_class]
    profile = AGENT_PROFILES[agent_id]
    return {
        "capability_fit": capability * 3,
        "risk_alignment": 2
        if RISK_LEVELS.get(profile["risk_ceiling"], 0) >= RISK_LEVELS.get(risk_level, 2)
        else 0,
        "availability": (2 if availability == "available" else 1) * 2,
        "context_fit": {"deep": 2, "medium": 1, "shallow": 0}[profile["context_depth"]],
        "quota_conservation": _quota_conservation_raw(agent_id),
    }


def _quota_conservation_raw(agent_id: str) -> int:
    scarcity = AGENT_PROFILES[agent_id]["scarcity"]
    return {"none": 2, "medium": 1, "high": 0}[scarcity]


def _conditions(capability: int, availability: str) -> list[str]:
    conditions: list[str] = []
    if capability < 3:
        conditions.append("review recommended because capability score is below primary strength")
    if availability in {"limited", "unknown"}:
        conditions.append(f"scope condition: availability is {availability}")
    return conditions
