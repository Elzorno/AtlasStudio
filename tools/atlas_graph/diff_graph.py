#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any


sys.dont_write_bytecode = True
from atlas_graph import DEFAULT_GRAPH_DIR, repo_root_from


WORKING_TREE = "working tree"
KNOWN_SCOPES = ("canon", "production", "bridge")
HIGHLIGHT_FIELDS = ("status", "work_order_status", "source", "scope")


@dataclass
class GraphState:
    label: str
    nodes: dict[str, dict[str, Any]] = field(default_factory=dict)
    node_scopes: dict[str, str] = field(default_factory=dict)
    edges: dict[str, dict[str, Any]] = field(default_factory=dict)
    edge_scopes: dict[str, str] = field(default_factory=dict)


@dataclass
class ItemDiff:
    kind: str
    item_id: str
    change: str
    scope: str
    base: dict[str, Any] | None = None
    head: dict[str, Any] | None = None
    changed_fields: list[dict[str, Any]] = field(default_factory=list)

    def to_json(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "id": self.item_id,
            "change": self.change,
            "scope": self.scope,
            "base": self.base,
            "head": self.head,
            "changed_fields": self.changed_fields,
        }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare two Atlas Graph states and explain what changed."
    )
    parser.add_argument(
        "--graph-dir",
        default=str(DEFAULT_GRAPH_DIR),
        help="Graph directory containing nodes/ and edges/ folders.",
    )
    parser.add_argument("--base", help="Base Git ref or commit (e.g. HEAD~1).")
    parser.add_argument("--head", help="Head Git ref or commit. Defaults to the working tree.")
    parser.add_argument("--base-dir", help="Base graph directory instead of a Git ref.")
    parser.add_argument("--head-dir", help="Head graph directory instead of a Git ref.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable results.")
    parser.add_argument("--output", help="Also write the report to this file path.")
    parser.add_argument(
        "--exit-code",
        action="store_true",
        help="Exit with status 1 when the graph states differ.",
    )
    args = parser.parse_args()

    if args.base and args.base_dir:
        parser.error("Use --base or --base-dir, not both.")
    if args.head and args.head_dir:
        parser.error("Use --head or --head-dir, not both.")
    if not args.base and not args.base_dir:
        parser.error("A base is required: pass --base <ref> or --base-dir <path>.")

    root = repo_root_from()

    if args.base_dir:
        base = load_from_directory(args.base_dir, root)
    else:
        base = load_from_git_ref(args.base, args.graph_dir, root)

    if args.head_dir:
        head = load_from_directory(args.head_dir, root)
    elif args.head:
        head = load_from_git_ref(args.head, args.graph_dir, root)
    else:
        head = load_from_directory(args.graph_dir, root, label=WORKING_TREE)

    diffs = diff_states(base, head)
    result = build_result(base, head, diffs)

    if args.json:
        rendered = json.dumps(result, indent=2, sort_keys=True)
    else:
        rendered = render_report(result)
    print(rendered)

    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = root / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered + "\n", encoding="utf-8")

    if args.exit_code and diffs:
        return 1
    return 0


def load_from_directory(graph_dir: str | Path, root: Path, label: str | None = None) -> GraphState:
    graph_path = Path(graph_dir)
    if not graph_path.is_absolute():
        graph_path = root / graph_path
    graph_path = graph_path.resolve()
    if not graph_path.is_dir():
        raise SystemExit(f"Graph directory not found: {graph_path}")

    state = GraphState(label=label or str(graph_dir))
    for path in sorted((graph_path / "nodes").glob("*.nodes.json")):
        ingest_file(state, "node", scope_of(path.name), read_json_text(path.read_text("utf-8"), str(path)))
    for path in sorted((graph_path / "edges").glob("*.edges.json")):
        ingest_file(state, "edge", scope_of(path.name), read_json_text(path.read_text("utf-8"), str(path)))
    return state


def load_from_git_ref(ref: str, graph_dir: str | Path, root: Path) -> GraphState:
    graph_path = Path(graph_dir)
    if graph_path.is_absolute():
        graph_path = graph_path.relative_to(root)
    rel = PurePosixPath(graph_path.as_posix())

    listing = run_git(
        ["ls-tree", "-r", "--name-only", ref, "--", str(rel)],
        root,
        f"Cannot read Git ref {ref!r}",
    )
    state = GraphState(label=f"{ref} ({rel})")
    for line in sorted(listing.splitlines()):
        file_path = PurePosixPath(line)
        kind = kind_of(file_path)
        if kind is None:
            continue
        text = run_git(["show", f"{ref}:{line}"], root, f"Cannot read {line} at {ref!r}")
        ingest_file(state, kind, scope_of(file_path.name), read_json_text(text, f"{ref}:{line}"))
    return state


def kind_of(file_path: PurePosixPath) -> str | None:
    if file_path.parent.name == "nodes" and file_path.name.endswith(".nodes.json"):
        return "node"
    if file_path.parent.name == "edges" and file_path.name.endswith(".edges.json"):
        return "edge"
    return None


def scope_of(file_name: str) -> str:
    scope = file_name.split(".", 1)[0]
    return scope if scope in KNOWN_SCOPES else "other"


def ingest_file(state: GraphState, kind: str, scope: str, data: dict[str, Any]) -> None:
    items = data.get("nodes" if kind == "node" else "edges", [])
    if not isinstance(items, list):
        return
    for item in items:
        if not isinstance(item, dict):
            continue
        item_id = item.get("id")
        if not isinstance(item_id, str):
            continue
        if kind == "node":
            state.nodes[item_id] = item
            state.node_scopes[item_id] = scope
        else:
            state.edges[item_id] = item
            state.edge_scopes[item_id] = scope


def diff_states(base: GraphState, head: GraphState) -> list[ItemDiff]:
    diffs: list[ItemDiff] = []
    diffs.extend(diff_items("node", base.nodes, base.node_scopes, head.nodes, head.node_scopes))
    diffs.extend(diff_items("edge", base.edges, base.edge_scopes, head.edges, head.edge_scopes))
    return diffs


def diff_items(
    kind: str,
    base_items: dict[str, dict[str, Any]],
    base_scopes: dict[str, str],
    head_items: dict[str, dict[str, Any]],
    head_scopes: dict[str, str],
) -> list[ItemDiff]:
    diffs: list[ItemDiff] = []
    for item_id in sorted(set(base_items) | set(head_items)):
        base_item = base_items.get(item_id)
        head_item = head_items.get(item_id)
        if base_item is None:
            diffs.append(
                ItemDiff(kind, item_id, "added", head_scopes[item_id], head=head_item)
            )
            continue
        if head_item is None:
            diffs.append(
                ItemDiff(kind, item_id, "removed", base_scopes[item_id], base=base_item)
            )
            continue

        changed_fields = diff_fields(base_item, head_item)
        base_scope = base_scopes[item_id]
        head_scope = head_scopes[item_id]
        if base_scope != head_scope:
            changed_fields.append({"field": "scope", "base": base_scope, "head": head_scope})
        if changed_fields:
            diffs.append(
                ItemDiff(
                    kind,
                    item_id,
                    "changed",
                    head_scope,
                    base=base_item,
                    head=head_item,
                    changed_fields=changed_fields,
                )
            )
    return diffs


def diff_fields(base_item: dict[str, Any], head_item: dict[str, Any]) -> list[dict[str, Any]]:
    changed: list[dict[str, Any]] = []
    for key in sorted(set(base_item) | set(head_item)):
        base_value = base_item.get(key)
        head_value = head_item.get(key)
        if base_value != head_value:
            changed.append({"field": key, "base": base_value, "head": head_value})
    return changed


def build_result(base: GraphState, head: GraphState, diffs: list[ItemDiff]) -> dict[str, Any]:
    scopes: dict[str, Any] = {}
    for diff in diffs:
        scope_bucket = scopes.setdefault(
            diff.scope,
            {
                "node": {"added": [], "removed": [], "changed": []},
                "edge": {"added": [], "removed": [], "changed": []},
            },
        )
        scope_bucket[diff.kind][diff.change].append(diff.to_json())

    status_changes = [
        {
            "kind": diff.kind,
            "id": diff.item_id,
            "scope": diff.scope,
            "field": change["field"],
            "base": change["base"],
            "head": change["head"],
        }
        for diff in diffs
        for change in diff.changed_fields
        if change["field"] in {"status", "work_order_status"}
    ]
    source_changes = [
        {
            "kind": diff.kind,
            "id": diff.item_id,
            "scope": diff.scope,
            "base": change["base"],
            "head": change["head"],
        }
        for diff in diffs
        for change in diff.changed_fields
        if change["field"] == "source"
    ]
    scope_moves = [
        {
            "kind": diff.kind,
            "id": diff.item_id,
            "base": change["base"],
            "head": change["head"],
        }
        for diff in diffs
        for change in diff.changed_fields
        if change["field"] == "scope"
    ]

    summary = {
        "nodes": count_changes(diffs, "node"),
        "edges": count_changes(diffs, "edge"),
        "identical": not diffs,
    }

    return {
        "base": {"label": base.label, "nodes": len(base.nodes), "edges": len(base.edges)},
        "head": {"label": head.label, "nodes": len(head.nodes), "edges": len(head.edges)},
        "summary": summary,
        "scopes": scopes,
        "status_changes": status_changes,
        "source_changes": source_changes,
        "scope_moves": scope_moves,
    }


def count_changes(diffs: list[ItemDiff], kind: str) -> dict[str, int]:
    counts = {"added": 0, "removed": 0, "changed": 0}
    for diff in diffs:
        if diff.kind == kind:
            counts[diff.change] += 1
    return counts


def render_report(result: dict[str, Any]) -> str:
    lines: list[str] = ["# Atlas Graph Diff", ""]
    base = result["base"]
    head = result["head"]
    lines.append(f"Base: {base['label']} ({base['nodes']} nodes, {base['edges']} edges)")
    lines.append(f"Head: {head['label']} ({head['nodes']} nodes, {head['edges']} edges)")
    lines.append("")

    nodes = result["summary"]["nodes"]
    edges = result["summary"]["edges"]
    lines.append(
        "Summary: "
        f"nodes +{nodes['added']} -{nodes['removed']} ~{nodes['changed']}, "
        f"edges +{edges['added']} -{edges['removed']} ~{edges['changed']}"
    )
    lines.append("")

    if result["summary"]["identical"]:
        lines.append("No graph changes between base and head.")
        return "\n".join(lines)

    if result["status_changes"]:
        lines.append("## Status Changes")
        lines.append("")
        for change in result["status_changes"]:
            lines.append(
                f"- {change['kind']} {change['id']} [{change['scope']}] "
                f"{change['field']}: {change['base']} -> {change['head']}"
            )
        lines.append("")

    if result["scope_moves"]:
        lines.append("## Scope Moves")
        lines.append("")
        for move in result["scope_moves"]:
            lines.append(f"- {move['kind']} {move['id']} moved {move['base']} -> {move['head']}")
        lines.append("")

    if result["source_changes"]:
        lines.append("## Source Reference Changes")
        lines.append("")
        for change in result["source_changes"]:
            lines.append(
                f"- {change['kind']} {change['id']} [{change['scope']}]: "
                f"{format_value(change['base'])} -> {format_value(change['head'])}"
            )
        lines.append("")

    for scope in (*KNOWN_SCOPES, "other"):
        bucket = result["scopes"].get(scope)
        if bucket is None:
            continue
        lines.append(f"## {scope.capitalize()} Changes")
        lines.append("")
        for kind, kind_label in (("node", "Nodes"), ("edge", "Edges")):
            for change, verb in (("added", "Added"), ("removed", "Removed"), ("changed", "Changed")):
                entries = bucket[kind][change]
                if not entries:
                    continue
                lines.append(f"### {kind_label} {verb} ({len(entries)})")
                lines.append("")
                for entry in entries:
                    lines.extend(render_entry(entry))
                lines.append("")

    return "\n".join(lines).rstrip()


def render_entry(entry: dict[str, Any]) -> list[str]:
    item = entry["head"] or entry["base"] or {}
    if entry["kind"] == "node":
        headline = f"- {entry['id']} ({item.get('type')}) \"{item.get('name')}\""
    else:
        headline = f"- {entry['id']}: {item.get('from')} {item.get('type')} {item.get('to')}"
    if entry["change"] in {"added", "removed"}:
        headline += f" status={item.get('status')}"
    lines = [headline]
    for change in entry["changed_fields"]:
        lines.append(
            f"  - {change['field']}: {format_value(change['base'])} -> {format_value(change['head'])}"
        )
    return lines


def format_value(value: Any, limit: int = 80) -> str:
    if value is None:
        return "<missing>"
    text = json.dumps(value, ensure_ascii=False) if isinstance(value, (list, dict)) else str(value)
    if len(text) > limit:
        text = text[: limit - 3] + "..."
    return text


def read_json_text(text: str, source: str) -> dict[str, Any]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError as error:
        raise SystemExit(f"Invalid JSON in {source}: {error}") from error
    if not isinstance(data, dict):
        raise SystemExit(f"{source} must contain a JSON object")
    return data


def run_git(args: list[str], root: Path, error_context: str) -> str:
    process = subprocess.run(
        ["git", *args],
        cwd=root,
        capture_output=True,
        text=True,
    )
    if process.returncode != 0:
        detail = process.stderr.strip() or process.stdout.strip()
        raise SystemExit(f"{error_context}: {detail}")
    return process.stdout


if __name__ == "__main__":
    raise SystemExit(main())
