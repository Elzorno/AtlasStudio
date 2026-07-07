#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True
TOOL_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOL_DIR.parents[1]
ATLAS_GRAPH_DIR = REPO_ROOT / "tools" / "atlas_graph"
ATLAS_DOCTOR_DIR = REPO_ROOT / "tools" / "atlas_doctor"
ATLAS_LINT_DIR = REPO_ROOT / "tools" / "atlas_lint"
for tool_path in (ATLAS_GRAPH_DIR, ATLAS_DOCTOR_DIR, ATLAS_LINT_DIR):
    if str(tool_path) not in sys.path:
        sys.path.insert(0, str(tool_path))

from atlas_graph import DEFAULT_GRAPH_DIR, AtlasGraph, format_edge, repo_root_from  # noqa: E402
from validate_graph import validate  # noqa: E402
from doctor import build_health  # noqa: E402
from canon_lint import DEFAULT_RULES_PATH, build_result as build_lint_result  # noqa: E402
from canon_lint import lint_graph, load_rules  # noqa: E402


ACTIVE_STATUSES = {"proposed", "approved", "assigned", "in_progress", "needs_revision"}
DONE_STATUSES = {"submitted", "qa_review", "accepted", "closed"}
SCORE_FIELDS = (
    "milestone_impact",
    "dependency_value",
    "technical_debt",
    "player_value",
    "core_platform_value",
)


@dataclass
class WorkOrder:
    path: str
    work_order_id: str
    title: str
    status: str
    project: str
    recommended_agent: str
    agent_role: str
    risk_level: str
    player_facing: bool
    engine_specific: bool
    purpose: str = ""
    player_goal: str = ""


@dataclass
class Recommendation:
    id: str
    title: str
    kind: str
    status: str
    recommended_agents: list[str]
    score: dict[str, int]
    priority: str
    evidence: list[str] = field(default_factory=list)
    source: str | None = None
    human_action: str = "Review and approve before creating or assigning work."

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "kind": self.kind,
            "status": self.status,
            "recommended_agents": self.recommended_agents,
            "score": self.score,
            "total_score": total_score(self.score),
            "priority": self.priority,
            "evidence": self.evidence,
            "source": self.source,
            "human_action": self.human_action,
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="Recommend next AtlasStudio work without creating it.")
    parser.add_argument("--project", default="the-last-sword-protocol", help="Primary project ID.")
    parser.add_argument(
        "--graph-dir",
        default=str(DEFAULT_GRAPH_DIR),
        help="Graph directory containing nodes/ and edges/ folders.",
    )
    parser.add_argument("--output", help="Optional Markdown report output path.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable planner output.")
    args = parser.parse_args()

    root = repo_root_from()
    try:
        graph = AtlasGraph.load(args.graph_dir, root=root)
        structural_errors = validate(graph)
        health = build_health(graph, args.project, structural_errors)
        lint_rules = load_rules(DEFAULT_RULES_PATH, root)
        lint_findings = lint_graph(graph, lint_rules)
        lint_result = build_lint_result(args.project, graph, lint_rules, lint_findings, structural_errors)
        work_orders = load_work_orders(root / "work-orders")
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Planning Engine failed: {error}", file=sys.stderr)
        return 1

    recommendations = build_recommendations(graph, work_orders, health, lint_result, args.project)
    result = build_result(args.project, graph, work_orders, health, lint_result, recommendations)
    rendered = json.dumps(result, indent=2, sort_keys=True) if args.json else render_markdown(result)

    print(rendered)

    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = root / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered + "\n", encoding="utf-8")

    return 1 if structural_errors else 0


def load_work_orders(work_order_dir: Path) -> list[WorkOrder]:
    return [
        parse_work_order(path)
        for path in sorted(work_order_dir.glob("WO-*.md"))
    ]


def parse_work_order(path: Path) -> WorkOrder:
    text = path.read_text("utf-8")
    frontmatter = parse_frontmatter(text)
    return WorkOrder(
        path=str(path.relative_to(path.parents[1])),
        work_order_id=str(frontmatter.get("work_order_id", path.stem.split("-", 2)[0])),
        title=str(frontmatter.get("title", path.stem)),
        status=str(frontmatter.get("status", "unknown")),
        project=str(frontmatter.get("project", "")),
        recommended_agent=str(frontmatter.get("recommended_agent", "")),
        agent_role=str(frontmatter.get("agent_role", "")),
        risk_level=str(frontmatter.get("risk_level", "")),
        player_facing=parse_bool(frontmatter.get("player_facing", False)),
        engine_specific=parse_bool(frontmatter.get("engine_specific", False)),
        purpose=section_text(text, "Purpose"),
        player_goal=section_text(text, "Player-Facing Goal"),
    )


def parse_frontmatter(text: str) -> dict[str, Any]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    data: dict[str, Any] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = parse_scalar(value.strip())
    return data


def parse_scalar(value: str) -> Any:
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    return value.strip('"').strip("'")


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).lower() == "true"


def section_text(text: str, heading: str) -> str:
    marker = f"## {heading}"
    lines = text.splitlines()
    try:
        start = lines.index(marker) + 1
    except ValueError:
        return ""
    collected: list[str] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        if line.strip():
            collected.append(line.strip())
    return " ".join(collected)


def build_recommendations(
    graph: AtlasGraph,
    work_orders: list[WorkOrder],
    health: dict[str, Any],
    lint_result: dict[str, Any],
    project: str,
) -> list[Recommendation]:
    recommendations: list[Recommendation] = []
    proposed = [
        work_order
        for work_order in work_orders
        if work_order.status in ACTIVE_STATUSES and work_order.work_order_id != "WO-0011"
    ]
    for work_order in proposed:
        recommendations.append(recommend_existing_work_order(graph, work_order, health, lint_result, project))

    recommendations.extend(recommend_followups(graph, health, lint_result))
    return sorted(
        recommendations,
        key=lambda rec: (-total_score(rec.score), rec.priority, rec.id),
    )


def recommend_existing_work_order(
    graph: AtlasGraph,
    work_order: WorkOrder,
    health: dict[str, Any],
    lint_result: dict[str, Any],
    project: str,
) -> Recommendation:
    node_id = work_order_node_id(work_order.work_order_id)
    graph_node = graph.get_node(node_id)
    edges = graph.all_edges_for(node_id)
    orphan_ids = {node["id"] for node in health["orphans"]["nodes"]}

    score = {
        "milestone_impact": score_milestone(work_order, health, lint_result),
        "dependency_value": score_dependency(work_order, graph_node, edges, health),
        "technical_debt": score_technical_debt(work_order, node_id, orphan_ids, health),
        "player_value": score_player_value(work_order),
        "core_platform_value": score_core_platform(work_order),
    }
    evidence = [
        f"{work_order.work_order_id} is {work_order.status} and has not been submitted or accepted.",
        f"Metadata recommends `{work_order.recommended_agent}` for role `{work_order.agent_role}`.",
    ]
    if work_order.player_facing:
        evidence.append("Work order is player-facing, so it can improve First Playable Hour momentum.")
    if work_order.engine_specific:
        evidence.append("Work order is engine-specific and may unlock implementation handoff.")
    if edges:
        evidence.append("Graph relationships: " + "; ".join(format_edge(edge) for edge in edges))
    if node_id in orphan_ids:
        evidence.append("Studio Doctor currently flags this work order as orphaned.")
    if work_order.work_order_id == "WO-0005":
        evidence.append("Studio Doctor reports no implementation targets or bridge implementation edges yet.")
    if work_order.work_order_id in {"WO-0002", "WO-0003"}:
        evidence.append("Canon lint reports production coverage gaps for current story/world canon.")
    if work_order.project == project:
        evidence.append(f"Project matches requested planning target `{project}`.")

    return Recommendation(
        id=node_id,
        title=work_order.title,
        kind="existing_work_order",
        status=work_order.status,
        recommended_agents=recommended_agents_for(work_order),
        score=score,
        priority=priority_label(score),
        evidence=evidence,
        source=work_order.path,
        human_action="Approve, assign, or revise this existing work order. The planner did not create new work.",
    )


def recommend_followups(
    graph: AtlasGraph, health: dict[str, Any], lint_result: dict[str, Any]
) -> list[Recommendation]:
    followups: list[Recommendation] = []
    if health["implementation_readiness"]["implementation_target_count"] == 0:
        followups.append(
            Recommendation(
                id="proposal.bridge_implementation_targets",
                title="Define RPG Maker implementation targets for Ashford Vale",
                kind="proposed_follow_up",
                status="not_created",
                recommended_agents=["codex", "claude-code"],
                score={
                    "milestone_impact": 5,
                    "dependency_value": 5,
                    "technical_debt": 3,
                    "player_value": 4,
                    "core_platform_value": 3,
                },
                priority="must-fix",
                evidence=[
                    "Studio Doctor reports zero implementation target nodes.",
                    "Studio Doctor reports zero bridge implementation edges.",
                    "Canon lint Bridge category reports missing implementation mappings for region/location/infrastructure nodes.",
                    "This should be a human-approved work order before RPG Maker files are touched.",
                ],
            )
        )

    orphan_work_orders = [node for node in health["orphans"]["nodes"] if node["type"] == "work_order"]
    if orphan_work_orders:
        ids = ", ".join(node["id"] for node in orphan_work_orders)
        followups.append(
            Recommendation(
                id="proposal.resolve_orphan_work_orders",
                title="Resolve orphaned production work orders",
                kind="proposed_follow_up",
                status="not_created",
                recommended_agents=["codex", "claude-code"],
                score={
                    "milestone_impact": 2,
                    "dependency_value": 4,
                    "technical_debt": 5,
                    "player_value": 1,
                    "core_platform_value": 5,
                },
                priority="should-do",
                evidence=[
                    f"Studio Doctor flags orphan work order nodes: {ids}.",
                    "Orphaned production facts reduce graph usefulness for planning and scheduling.",
                ],
            )
        )

    production_count = lint_result["category_counts"].get("Production", 0)
    if production_count:
        followups.append(
            Recommendation(
                id="proposal.connect_canon_to_work_orders",
                title="Connect existing canon facts to production work orders",
                kind="proposed_follow_up",
                status="not_created",
                recommended_agents=["codex"],
                score={
                    "milestone_impact": 2,
                    "dependency_value": 3,
                    "technical_debt": 4,
                    "player_value": 1,
                    "core_platform_value": 4,
                },
                priority="should-do",
                evidence=[
                    f"Canon Linter reports {production_count} Production coverage findings.",
                    "Better production coverage helps future agents understand why canon facts exist.",
                ],
            )
        )

    if graph.get_node("work_order.wo_0012") is None:
        followups.append(
            Recommendation(
                id="proposal.seed_agent_scheduler_graph",
                title="Seed Agent Scheduler production graph facts",
                kind="proposed_follow_up",
                status="not_created",
                recommended_agents=["claude-code", "codex"],
                score={
                    "milestone_impact": 1,
                    "dependency_value": 2,
                    "technical_debt": 3,
                    "player_value": 0,
                    "core_platform_value": 5,
                },
                priority="nice-to-have",
                evidence=[
                    "WO-0012 exists as a Markdown work order but is not yet represented in production graph nodes.",
                    "Planning and scheduling tools work better when work-order metadata is reflected in graph data.",
                ],
            )
        )
    return followups


def score_milestone(work_order: WorkOrder, health: dict[str, Any], lint_result: dict[str, Any]) -> int:
    text = f"{work_order.title} {work_order.purpose} {work_order.player_goal}".lower()
    score = 0
    if any(term in text for term in ("home region", "overworld", "first playable", "starting region")):
        score = max(score, 5)
    if any(term in text for term in ("rpg maker", "bridge", "implementation")):
        score = max(score, 4)
    if work_order.player_facing:
        score = max(score, 4)
    if lint_result["category_counts"].get("Bridge", 0) and "bridge" in text:
        score = max(score, 5)
    if health["implementation_readiness"]["implementation_target_count"] == 0 and "bridge" in text:
        score = max(score, 5)
    return score


def score_dependency(
    work_order: WorkOrder,
    graph_node: dict[str, Any] | None,
    edges: list[dict[str, Any]],
    health: dict[str, Any],
) -> int:
    text = f"{work_order.title} {work_order.purpose}".lower()
    score = 1 if graph_node else 0
    if edges:
        score = max(score, min(5, 1 + len(edges)))
    if "bridge" in text and health["implementation_readiness"]["implementation_target_count"] == 0:
        score = 5
    if "assignment" in text or "scheduler" in text or "planner" in text:
        score = max(score, 4)
    return score


def score_technical_debt(
    work_order: WorkOrder,
    node_id: str,
    orphan_ids: set[str],
    health: dict[str, Any],
) -> int:
    text = f"{work_order.title} {work_order.purpose}".lower()
    score = 0
    if node_id in orphan_ids:
        score = 5
    if any(term in text for term in ("assignment", "scheduler", "bridge", "diagnostic")):
        score = max(score, 3)
    if health["graph_integrity"]["structural_error_count"]:
        score = 5
    return score


def score_player_value(work_order: WorkOrder) -> int:
    text = f"{work_order.title} {work_order.purpose} {work_order.player_goal}".lower()
    if work_order.player_facing:
        return 5
    if any(term in text for term in ("rpg maker", "bridge", "playable", "implementation")):
        return 3
    if any(term in text for term in ("story", "region", "overworld")):
        return 4
    return 1


def score_core_platform(work_order: WorkOrder) -> int:
    text = f"{work_order.title} {work_order.purpose}".lower()
    if work_order.project == "atlasstudio":
        return 5
    if any(term in text for term in ("scheduler", "assignment", "planner", "graph", "guard", "linter")):
        return 5
    if "bridge" in text:
        return 4
    return 1


def recommended_agents_for(work_order: WorkOrder) -> list[str]:
    agents = []
    if work_order.recommended_agent:
        agents.append(work_order.recommended_agent)
    text = f"{work_order.title} {work_order.agent_role} {work_order.purpose}".lower()
    if work_order.player_facing or "creative" in text or "story" in text:
        agents.append("gpt")
    if "architect" in text or "design" in text:
        agents.append("claude-code")
    if "implementation" in text or work_order.engine_specific:
        agents.append("codex")
    return dedupe(agents)


def build_result(
    project: str,
    graph: AtlasGraph,
    work_orders: list[WorkOrder],
    health: dict[str, Any],
    lint_result: dict[str, Any],
    recommendations: list[Recommendation],
) -> dict[str, Any]:
    statuses = Counter(work_order.status for work_order in work_orders)
    return {
        "project": project,
        "generated_on": date.today().isoformat(),
        "mode": "recommend_only",
        "graph": {
            "graph_dir": str(graph.graph_dir.relative_to(graph.root)),
            "nodes": len(graph.nodes),
            "edges": len(graph.edges),
        },
        "inputs": {
            "work_orders_read": len(work_orders),
            "work_order_statuses": dict(sorted(statuses.items())),
            "doctor_recommendations": health["recommendations"],
            "canon_lint_findings": len(lint_result["findings"]),
            "canon_lint_categories": lint_result["category_counts"],
        },
        "recommendations": [recommendation.to_json() for recommendation in recommendations],
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Atlas Planning Engine Report",
        "",
        f"Project: `{result['project']}`",
        f"Generated: {result['generated_on']}",
        f"Mode: `{result['mode']}`",
        "",
        "## Inputs",
        "",
        f"- Graph: `{result['graph']['graph_dir']}`",
        f"- Nodes: {result['graph']['nodes']}",
        f"- Edges: {result['graph']['edges']}",
        f"- Work orders read: {result['inputs']['work_orders_read']}",
        "- Work order statuses: "
        + ", ".join(
            f"{status}: {count}"
            for status, count in result["inputs"]["work_order_statuses"].items()
        ),
        f"- Canon lint findings: {result['inputs']['canon_lint_findings']}",
    ]
    lines.extend(["", "## Doctor Signals", ""])
    for rec in result["inputs"]["doctor_recommendations"]:
        lines.append(f"- {rec}")

    lines.extend(["", "## Recommendations", ""])
    for index, rec in enumerate(result["recommendations"], start=1):
        lines.append(f"### {index}. {rec['title']}")
        lines.append("")
        lines.append(f"- ID: `{rec['id']}`")
        lines.append(f"- Type: {rec['kind']}")
        lines.append(f"- Status: {rec['status']}")
        lines.append(f"- Priority: {rec['priority']} ({rec['total_score']}/100)")
        lines.append(f"- Recommended agents: {', '.join(rec['recommended_agents']) or 'none'}")
        lines.append(f"- Source: `{rec['source']}`" if rec["source"] else "- Source: planner proposal")
        lines.append("- Score:")
        for field in SCORE_FIELDS:
            lines.append(f"  - {field}: {rec['score'][field]}/5")
        lines.append("- Evidence:")
        for item in rec["evidence"]:
            lines.append(f"  - {item}")
        lines.append(f"- Human action: {rec['human_action']}")
        lines.append("")

    lines.extend(
        [
            "## Guardrails",
            "",
            "- This report does not create work orders.",
            "- Human approval is required before new work is created, assigned, or implemented.",
            "- No canon or RPG Maker files are modified by the planner.",
        ]
    )
    return "\n".join(lines) + "\n"


def total_score(score: dict[str, int]) -> int:
    return sum(score[field] for field in SCORE_FIELDS) * 4


def priority_label(score: dict[str, int]) -> str:
    total = total_score(score)
    if total >= 72:
        return "must-fix"
    if total >= 48:
        return "should-do"
    return "nice-to-have"


def work_order_node_id(work_order_id: str) -> str:
    return "work_order." + work_order_id.lower().replace("-", "_")


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


if __name__ == "__main__":
    raise SystemExit(main())
