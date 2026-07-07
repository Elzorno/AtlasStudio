#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
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


DEFAULT_RULES_PATH = TOOL_DIR / "rules" / "canon_lint_rules.json"
CANON_TYPES = {
    "world",
    "region",
    "location",
    "character",
    "faction",
    "quest",
    "story_beat",
    "infrastructure",
    "monster_family",
    "item",
    "concept",
}
CATEGORY_ORDER = ("Structure", "Completeness", "Consistency", "Coverage", "Production", "Bridge")
SEVERITY_ORDER = {"error": 0, "warning": 1, "info": 2}


@dataclass(frozen=True)
class LintFinding:
    rule_id: str
    category: str
    severity: str
    node_id: str
    node_type: str
    node_name: str
    message: str

    def to_json(self) -> dict[str, str]:
        return {
            "rule_id": self.rule_id,
            "category": self.category,
            "severity": self.severity,
            "node_id": self.node_id,
            "node_type": self.node_type,
            "node_name": self.node_name,
            "message": self.message,
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic Atlas Graph canon lint rules.")
    parser.add_argument("--project", default="the-last-sword-protocol", help="Project ID to lint.")
    parser.add_argument(
        "--graph-dir",
        default=str(DEFAULT_GRAPH_DIR),
        help="Graph directory containing nodes/ and edges/ folders.",
    )
    parser.add_argument(
        "--rules",
        default=str(DEFAULT_RULES_PATH),
        help="Canon lint rule metadata JSON path.",
    )
    parser.add_argument("--output", help="Optional Markdown report output path.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable lint results.")
    parser.add_argument(
        "--fail-on-warning",
        action="store_true",
        help="Exit 1 when warning-level canon findings exist.",
    )
    args = parser.parse_args()

    root = repo_root_from()
    try:
        graph = AtlasGraph.load(args.graph_dir, root=root)
        rules = load_rules(Path(args.rules), root)
        structural_errors = validate(graph)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Canon Linter failed: {error}", file=sys.stderr)
        return 1

    findings = lint_graph(graph, rules)
    result = build_result(args.project, graph, rules, findings, structural_errors)
    rendered = json.dumps(result, indent=2, sort_keys=True) if args.json else render_markdown(result)

    print(rendered)

    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = root / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered + "\n", encoding="utf-8")

    if structural_errors or result["severity_counts"].get("error", 0):
        return 1
    if args.fail_on_warning and result["severity_counts"].get("warning", 0):
        return 1
    return 0


def load_rules(path: Path, root: Path) -> list[dict[str, Any]]:
    if not path.is_absolute():
        path = root / path
    data = json.loads(path.read_text("utf-8"))
    rules = data.get("rules")
    if not isinstance(rules, list):
        raise ValueError(f"{path} must contain a rules array")
    for rule in rules:
        validate_rule(rule, path)
    return rules


def validate_rule(rule: dict[str, Any], source: Path) -> None:
    required = {"id", "category", "severity", "description", "kind", "target_types"}
    missing = sorted(required - set(rule))
    if missing:
        raise ValueError(f"{source} rule missing fields: {', '.join(missing)}")
    if not isinstance(rule["target_types"], list):
        raise ValueError(f"{source} rule {rule.get('id')} target_types must be a list")


def lint_graph(graph: AtlasGraph, rules: list[dict[str, Any]]) -> list[LintFinding]:
    findings: list[LintFinding] = []
    for rule in rules:
        kind = rule["kind"]
        if kind == "required_relationship":
            findings.extend(lint_required_relationship(graph, rule))
        elif kind == "duplicate_name_within_type":
            findings.extend(lint_duplicate_names(graph, rule))
        elif kind == "production_coverage":
            findings.extend(lint_production_coverage(graph, rule))
        elif kind == "implementation_coverage":
            findings.extend(lint_implementation_coverage(graph, rule))
        else:
            findings.append(
                LintFinding(
                    rule_id=str(rule["id"]),
                    category=str(rule["category"]),
                    severity="error",
                    node_id="<rule>",
                    node_type="rule",
                    node_name=str(rule["id"]),
                    message=f"Unsupported lint rule kind: {kind}",
                )
            )
    return sorted(findings, key=finding_sort_key)


def lint_required_relationship(graph: AtlasGraph, rule: dict[str, Any]) -> list[LintFinding]:
    findings: list[LintFinding] = []
    for node in target_nodes(graph, rule):
        node_id = str(node["id"])
        if not relationship_matches(graph, node, rule):
            findings.append(
                finding(
                    rule,
                    node,
                    f"{node_id} is missing required {relationship_description(rule)}.",
                )
            )
    return findings


def lint_duplicate_names(graph: AtlasGraph, rule: dict[str, Any]) -> list[LintFinding]:
    buckets: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for node in target_nodes(graph, rule):
        name = normalize_name(node.get("name"))
        if name:
            buckets[(str(node.get("type")), name)].append(node)

    findings: list[LintFinding] = []
    for (_node_type, _name), nodes in buckets.items():
        if len(nodes) < 2:
            continue
        ids = ", ".join(str(node.get("id")) for node in nodes)
        for node in nodes:
            findings.append(finding(rule, node, f"Duplicate canon name shared by: {ids}."))
    return findings


def lint_production_coverage(graph: AtlasGraph, rule: dict[str, Any]) -> list[LintFinding]:
    findings: list[LintFinding] = []
    edge_types = set(rule.get("edge_types", []))
    for node in target_nodes(graph, rule):
        node_id = str(node["id"])
        covered = any(
            edge.get("type") in edge_types and is_work_order(graph, edge.get("from"))
            for edge in graph.incoming_edges(node_id)
        ) or any(
            edge.get("type") in edge_types and is_work_order(graph, edge.get("to"))
            for edge in graph.outgoing_edges(node_id)
        )
        if not covered:
            findings.append(
                finding(rule, node, f"{node_id} is not connected to a creating or modifying work order.")
            )
    return findings


def lint_implementation_coverage(graph: AtlasGraph, rule: dict[str, Any]) -> list[LintFinding]:
    findings: list[LintFinding] = []
    edge_types = set(rule.get("edge_types", []))
    for node in target_nodes(graph, rule):
        node_id = str(node["id"])
        covered = any(edge.get("type") in edge_types for edge in graph.all_edges_for(node_id))
        if not covered:
            findings.append(
                finding(rule, node, f"{node_id} has no bridge or implementation mapping edge yet.")
            )
    return findings


def target_nodes(graph: AtlasGraph, rule: dict[str, Any]) -> list[dict[str, Any]]:
    target_types = set(rule.get("target_types", []))
    statuses = set(rule.get("applicable_statuses", []))
    return [
        node
        for node in graph.nodes.values()
        if node.get("type") in target_types
        and node.get("type") in CANON_TYPES
        and (not statuses or node.get("status") in statuses)
    ]


def relationship_matches(graph: AtlasGraph, node: dict[str, Any], rule: dict[str, Any]) -> bool:
    node_id = str(node["id"])
    direction = rule.get("direction", "outgoing")
    if direction == "incoming":
        edges = graph.incoming_edges(node_id)
    elif direction == "outgoing":
        edges = graph.outgoing_edges(node_id)
    else:
        edges = graph.all_edges_for(node_id)

    edge_types = set(rule.get("edge_types", []))
    neighbor_types = set(rule.get("neighbor_types", []))
    neighbor_subtypes = set(rule.get("neighbor_subtypes", []))

    for edge in edges:
        if edge_types and edge.get("type") not in edge_types:
            continue
        neighbor_id = edge.get("from") if edge.get("to") == node_id else edge.get("to")
        if not isinstance(neighbor_id, str):
            continue
        neighbor = graph.get_node(neighbor_id)
        if neighbor is None:
            continue
        if neighbor_types and neighbor.get("type") not in neighbor_types:
            continue
        if neighbor_subtypes and neighbor.get("subtype") not in neighbor_subtypes:
            continue
        return True
    return False


def relationship_description(rule: dict[str, Any]) -> str:
    direction = rule.get("direction", "outgoing")
    edge_types = ", ".join(rule.get("edge_types", [])) or "relationship"
    neighbor_types = ", ".join(rule.get("neighbor_types", []))
    if neighbor_types:
        return f"{direction} {edge_types} relationship with {neighbor_types}"
    return f"{direction} {edge_types} relationship"


def is_work_order(graph: AtlasGraph, node_id: Any) -> bool:
    if not isinstance(node_id, str):
        return False
    node = graph.get_node(node_id)
    return bool(node and node.get("type") == "work_order")


def finding(rule: dict[str, Any], node: dict[str, Any], message: str) -> LintFinding:
    return LintFinding(
        rule_id=str(rule["id"]),
        category=str(rule["category"]),
        severity=str(rule["severity"]),
        node_id=str(node.get("id")),
        node_type=str(node.get("type")),
        node_name=str(node.get("name", "")),
        message=message,
    )


def build_result(
    project: str,
    graph: AtlasGraph,
    rules: list[dict[str, Any]],
    findings: list[LintFinding],
    structural_errors: list[str],
) -> dict[str, Any]:
    severity_counts = Counter(finding.severity for finding in findings)
    category_counts = Counter(finding.category for finding in findings)
    return {
        "project": project,
        "generated_on": date.today().isoformat(),
        "graph": {
            "graph_dir": str(graph.graph_dir.relative_to(graph.root)),
            "nodes": len(graph.nodes),
            "edges": len(graph.edges),
            "canon_nodes": sum(1 for node in graph.nodes.values() if node.get("type") in CANON_TYPES),
        },
        "rules": {
            "count": len(rules),
            "categories": sorted({str(rule["category"]) for rule in rules}),
        },
        "structural_errors": structural_errors,
        "severity_counts": dict(sorted(severity_counts.items(), key=lambda item: SEVERITY_ORDER.get(item[0], 99))),
        "category_counts": dict(sorted(category_counts.items())),
        "findings": [finding.to_json() for finding in findings],
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Atlas Canon Lint Report",
        "",
        f"Project: `{result['project']}`",
        f"Generated: {result['generated_on']}",
        "",
        "## Summary",
        "",
        f"- Graph: `{result['graph']['graph_dir']}`",
        f"- Nodes: {result['graph']['nodes']}",
        f"- Edges: {result['graph']['edges']}",
        f"- Canon nodes: {result['graph']['canon_nodes']}",
        f"- Rules loaded: {result['rules']['count']}",
        f"- Structural errors: {len(result['structural_errors'])}",
        f"- Findings: {len(result['findings'])}",
    ]

    lines.extend(["", "## Severity Counts", ""])
    append_counts(lines, result["severity_counts"])

    lines.extend(["", "## Category Counts", ""])
    append_counts(lines, result["category_counts"])

    lines.extend(["", "## Structural Graph Errors", ""])
    append_items(lines, result["structural_errors"], empty="None.")

    for category in CATEGORY_ORDER:
        category_findings = [
            finding for finding in result["findings"] if finding["category"] == category
        ]
        lines.extend(["", f"## {category}", ""])
        if not category_findings:
            lines.append("- No findings.")
            continue
        for item in category_findings:
            lines.append(
                f"- {item['severity'].upper()} `{item['node_id']}` ({item['node_type']}): "
                f"{item['message']}"
            )
            lines.append(f"  - Rule: `{item['rule_id']}`")

    lines.extend(["", "## Recommendation", ""])
    if result["structural_errors"]:
        lines.append("- Fix structural graph errors before acting on canon lint findings.")
    elif result["findings"]:
        lines.append("- Treat warnings as design QA prompts; revise canon through approved work orders only.")
    else:
        lines.append("- No canon lint findings.")

    return "\n".join(lines) + "\n"


def append_counts(lines: list[str], counts: dict[str, int]) -> None:
    if not counts:
        lines.append("- None.")
        return
    for key, count in counts.items():
        lines.append(f"- {key}: {count}")


def append_items(lines: list[str], items: list[str], empty: str) -> None:
    if not items:
        lines.append(f"- {empty}")
        return
    for item in items:
        lines.append(f"- {item}")


def finding_sort_key(finding: LintFinding) -> tuple[int, str, str, str]:
    return (
        SEVERITY_ORDER.get(finding.severity, 99),
        finding.category,
        finding.rule_id,
        finding.node_id,
    )


def normalize_name(name: Any) -> str:
    return " ".join(str(name or "").casefold().split())


if __name__ == "__main__":
    raise SystemExit(main())
