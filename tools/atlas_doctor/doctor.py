#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True
TOOL_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOL_DIR.parents[1]
ATLAS_GRAPH_DIR = REPO_ROOT / "tools" / "atlas_graph"
if str(ATLAS_GRAPH_DIR) not in sys.path:
    sys.path.insert(0, str(ATLAS_GRAPH_DIR))

from atlas_graph import DEFAULT_GRAPH_DIR, AtlasGraph, repo_root_from  # noqa: E402
from validate_graph import validate  # noqa: E402


IMPLEMENTATION_CANDIDATE_TYPES = {
    "region",
    "location",
    "infrastructure",
    "quest",
    "story_beat",
}
IMPLEMENTATION_EDGE_TYPES = {"IMPLEMENTED_BY", "TRANSLATES_TO", "GENERATED_FROM"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Print an AtlasStudio health report.")
    parser.add_argument(
        "--project",
        default="the-last-sword-protocol",
        help="Project ID to diagnose. Defaults to the first AtlasStudio project.",
    )
    parser.add_argument(
        "--graph-dir",
        default=str(DEFAULT_GRAPH_DIR),
        help="Graph directory containing nodes/ and edges/ folders.",
    )
    parser.add_argument(
        "--output",
        help="Optional Markdown output path. The tool is read-only unless this is provided.",
    )
    parser.add_argument("--json", action="store_true", help="Print machine-readable health data.")
    args = parser.parse_args()

    root = repo_root_from()
    try:
        graph = AtlasGraph.load(args.graph_dir, root=root)
        validation_errors = validate(graph)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Studio Doctor failed to read graph data: {error}", file=sys.stderr)
        return 1

    health = build_health(graph, args.project, validation_errors)
    report = render_markdown(health)

    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = root / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding="utf-8")

    if args.json:
        print(json.dumps(health, indent=2, sort_keys=True))
    else:
        print(report)

    return 1 if health["graph_integrity"]["structural_error_count"] else 0


def build_health(
    graph: AtlasGraph, project: str, validation_errors: list[str]
) -> dict[str, Any]:
    missing_sources = graph.missing_source_paths()
    structural_errors = [
        error for error in validation_errors if "references missing source" not in error
    ]
    orphan_nodes = sorted(graph.orphan_nodes(), key=lambda node: str(node.get("id", "")))
    work_orders = sorted(
        [node for node in graph.nodes.values() if node.get("type") == "work_order"],
        key=lambda node: str(node.get("id", "")),
    )
    work_order_status_counts = Counter(
        str(node.get("work_order_status") or node.get("status") or "unknown")
        for node in work_orders
    )

    canon_nodes = [node for node in graph.nodes.values() if node.get("type") in IMPLEMENTATION_CANDIDATE_TYPES]
    implemented_canon_nodes = [
        node
        for node in canon_nodes
        if has_implementation_signal(graph, str(node.get("id")))
    ]
    implementation_targets = [
        node for node in graph.nodes.values() if node.get("type") == "implementation_target"
    ]
    bridge_nodes = [node for node in graph.nodes.values() if node.get("type") == "bridge"]
    bridge_edges = [
        edge
        for edge in graph.edges
        if edge.get("type") in {"TRANSLATES_TO", "PROTECTED_BY", "GENERATED_FROM", "IMPLEMENTED_BY"}
    ]

    tools = sorted(
        [node for node in graph.nodes.values() if node.get("type") == "tool"],
        key=lambda node: str(node.get("id", "")),
    )

    findings = {
        "canon": canon_findings(canon_nodes, implemented_canon_nodes),
        "production": production_findings(orphan_nodes, work_order_status_counts),
        "implementation": implementation_findings(
            bridge_nodes,
            bridge_edges,
            implementation_targets,
            canon_nodes,
            implemented_canon_nodes,
            graph,
        ),
        "tools": tool_findings(tools),
    }

    return {
        "project": project,
        "generated_on": date.today().isoformat(),
        "graph_integrity": {
            "graph_dir": str(graph.graph_dir.relative_to(graph.root)),
            "file_count": len(graph.files),
            "node_count": len(graph.nodes),
            "edge_count": len(graph.edges),
            "validation_error_count": len(validation_errors),
            "structural_error_count": len(structural_errors),
            "missing_source_count": len(missing_sources),
            "structural_errors": structural_errors,
        },
        "orphans": {
            "count": len(orphan_nodes),
            "work_order_count": sum(1 for node in orphan_nodes if node.get("type") == "work_order"),
            "nodes": [node_entry(node) for node in orphan_nodes],
        },
        "missing_sources": missing_sources,
        "work_orders": {
            "count": len(work_orders),
            "status_counts": dict(sorted(work_order_status_counts.items())),
            "items": [
                {
                    "id": node.get("id"),
                    "name": node.get("name"),
                    "status": node.get("work_order_status") or node.get("status"),
                }
                for node in work_orders
            ],
        },
        "implementation_readiness": {
            "bridge_count": len(bridge_nodes),
            "bridge_edge_count": len(bridge_edges),
            "implementation_target_count": len(implementation_targets),
            "canon_candidate_count": len(canon_nodes),
            "implemented_canon_count": len(implemented_canon_nodes),
            "unimplemented_canon_count": len(canon_nodes) - len(implemented_canon_nodes),
            "signals": implementation_signals(
                bridge_nodes, bridge_edges, implementation_targets, canon_nodes, implemented_canon_nodes
            ),
        },
        "tools": {
            "count": len(tools),
            "items": [node_entry(node) for node in tools],
        },
        "findings": findings,
        "recommendations": recommendations(findings, missing_sources, structural_errors),
    }


def has_implementation_signal(graph: AtlasGraph, node_id: str) -> bool:
    return any(
        edge.get("type") in IMPLEMENTATION_EDGE_TYPES
        for edge in graph.all_edges_for(node_id)
    )


def canon_findings(
    canon_nodes: list[dict[str, Any]], implemented_canon_nodes: list[dict[str, Any]]
) -> list[str]:
    if not canon_nodes:
        return ["No implementation-candidate canon nodes are present yet."]
    if not implemented_canon_nodes:
        return [
            "Canon graph has implementation candidates, but none have implementation links yet."
        ]
    return [
        f"{len(implemented_canon_nodes)} of {len(canon_nodes)} implementation-candidate canon nodes have implementation links."
    ]


def production_findings(
    orphan_nodes: list[dict[str, Any]], status_counts: Counter[str]
) -> list[str]:
    findings: list[str] = []
    orphan_work_orders = [node for node in orphan_nodes if node.get("type") == "work_order"]
    if orphan_work_orders:
        ids = ", ".join(str(node.get("id")) for node in orphan_work_orders)
        findings.append(f"Orphan work orders need assignment, dependency, review, or impact edges: {ids}.")
    else:
        findings.append("No orphan work orders found.")
    if status_counts:
        findings.append(
            "Work order lifecycle mix: "
            + ", ".join(f"{status}={count}" for status, count in sorted(status_counts.items()))
            + "."
        )
    return findings


def implementation_findings(
    bridge_nodes: list[dict[str, Any]],
    bridge_edges: list[dict[str, Any]],
    implementation_targets: list[dict[str, Any]],
    canon_nodes: list[dict[str, Any]],
    implemented_canon_nodes: list[dict[str, Any]],
    graph: AtlasGraph,
) -> list[str]:
    findings: list[str] = []
    if bridge_nodes:
        findings.append("RPG Maker bridge node exists in graph data.")
    else:
        findings.append("No engine bridge node exists yet.")
    if not implementation_targets:
        findings.append("No implementation target nodes are present yet.")
    if not bridge_edges:
        findings.append("No bridge implementation edges are present yet.")
    bridge_work = graph.get_node("work_order.wo_0005")
    if bridge_work:
        findings.append(
            f"RPG Maker bridge design work order is {bridge_work.get('work_order_status', bridge_work.get('status'))}."
        )
    if canon_nodes and not implemented_canon_nodes:
        findings.append("Playable implementation readiness is early: canon exists, but graph has no implementation mappings.")
    return findings


def tool_findings(tools: list[dict[str, Any]]) -> list[str]:
    if not tools:
        return ["No AtlasStudio tools are registered in the production graph."]
    tool_ids = ", ".join(str(tool.get("id")) for tool in tools)
    return [f"Registered AtlasStudio tools: {tool_ids}."]


def implementation_signals(
    bridge_nodes: list[dict[str, Any]],
    bridge_edges: list[dict[str, Any]],
    implementation_targets: list[dict[str, Any]],
    canon_nodes: list[dict[str, Any]],
    implemented_canon_nodes: list[dict[str, Any]],
) -> list[str]:
    signals = [
        signal("bridge_defined", bool(bridge_nodes), "At least one engine bridge node exists."),
        signal(
            "implementation_targets_defined",
            bool(implementation_targets),
            "Implementation target nodes are recorded.",
        ),
        signal("bridge_edges_defined", bool(bridge_edges), "Bridge implementation edges exist."),
        signal(
            "canon_implementation_links",
            bool(canon_nodes and implemented_canon_nodes),
            "Canon nodes have implementation mappings.",
        ),
    ]
    return signals


def signal(name: str, ready: bool, description: str) -> str:
    state = "ready" if ready else "not ready"
    return f"{name}: {state} - {description}"


def recommendations(
    findings: dict[str, list[str]],
    missing_sources: list[dict[str, str]],
    structural_errors: list[str],
) -> list[str]:
    recs: list[str] = []
    if structural_errors:
        recs.append("Fix structural graph errors before assigning new implementation work.")
    if missing_sources:
        recs.append("Restore or correct missing source paths so graph facts remain auditable.")
    if any("work_order.wo_0004" in finding for finding in findings["production"]):
        recs.append("Connect WO-0004 to its agent assignment or production impact, or retire it intentionally.")
    if any("No implementation target" in finding for finding in findings["implementation"]):
        recs.append("Create bridge implementation targets before translating canon into RPG Maker tasks.")
    if any("proposed" in finding for finding in findings["implementation"]):
        recs.append("Review WO-0005 before relying on the RPG Maker bridge for implementation work.")
    if not recs:
        recs.append("No blocking studio health issues found.")
    return recs


def render_markdown(health: dict[str, Any]) -> str:
    lines = [
        "# AtlasStudio Health Report",
        "",
        f"Project: `{health['project']}`",
        f"Generated: {health['generated_on']}",
        "",
        "## Graph Integrity",
        "",
        f"- Graph directory: `{health['graph_integrity']['graph_dir']}`",
        f"- Files: {health['graph_integrity']['file_count']}",
        f"- Nodes: {health['graph_integrity']['node_count']}",
        f"- Edges: {health['graph_integrity']['edge_count']}",
        f"- Structural errors: {health['graph_integrity']['structural_error_count']}",
        f"- Missing sources: {health['graph_integrity']['missing_source_count']}",
    ]
    append_list(lines, "Structural Errors", health["graph_integrity"]["structural_errors"], empty="None.")

    lines.extend(["", "## Canon", ""])
    append_list(lines, None, health["findings"]["canon"])

    lines.extend(["", "## Production", ""])
    lines.append(f"- Work orders: {health['work_orders']['count']}")
    status_text = ", ".join(
        f"{status}: {count}" for status, count in health["work_orders"]["status_counts"].items()
    )
    lines.append(f"- Work order statuses: {status_text or 'none'}")
    append_list(lines, "Production Findings", health["findings"]["production"])
    append_list(
        lines,
        "Orphan Nodes",
        [f"{node['id']} ({node['type']}) - {node['name']}" for node in health["orphans"]["nodes"]],
        empty="None.",
    )

    lines.extend(["", "## Implementation", ""])
    readiness = health["implementation_readiness"]
    lines.append(f"- Bridges: {readiness['bridge_count']}")
    lines.append(f"- Bridge edges: {readiness['bridge_edge_count']}")
    lines.append(f"- Implementation targets: {readiness['implementation_target_count']}")
    lines.append(f"- Implementation-candidate canon nodes: {readiness['canon_candidate_count']}")
    lines.append(f"- Canon nodes with implementation links: {readiness['implemented_canon_count']}")
    append_list(lines, "Readiness Signals", readiness["signals"])
    append_list(lines, "Implementation Findings", health["findings"]["implementation"])

    lines.extend(["", "## Tools", ""])
    lines.append(f"- Registered tools: {health['tools']['count']}")
    append_list(lines, "Tool Findings", health["findings"]["tools"])

    lines.extend(["", "## Missing Sources", ""])
    missing_source_lines = [
        f"{item['kind']} {item['id']} -> {item['source']}"
        for item in health["missing_sources"]
    ]
    append_list(lines, None, missing_source_lines, empty="None.")

    lines.extend(["", "## Recommendations", ""])
    append_list(lines, None, health["recommendations"])

    return "\n".join(lines) + "\n"


def append_list(
    lines: list[str], title: str | None, items: list[str], empty: str | None = None
) -> None:
    if title:
        lines.extend(["", f"### {title}", ""])
    if items:
        for item in items:
            lines.append(f"- {item}")
    elif empty is not None:
        lines.append(f"- {empty}")


def node_entry(node: dict[str, Any]) -> dict[str, str | None]:
    return {
        "id": node.get("id"),
        "type": node.get("type"),
        "name": node.get("name"),
        "status": node.get("work_order_status") or node.get("status"),
    }


if __name__ == "__main__":
    raise SystemExit(main())
