#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from atlas_graph import DEFAULT_GRAPH_DIR, AtlasGraph, repo_root_from


NODE_REQUIRED = {"id", "type", "name", "status", "summary", "source"}
EDGE_REQUIRED = {"id", "from", "type", "to", "status", "source"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Atlas Graph JSON files.")
    parser.add_argument(
        "--graph-dir",
        default=str(DEFAULT_GRAPH_DIR),
        help="Graph directory containing nodes/ and edges/ folders.",
    )
    parser.add_argument("--json", action="store_true", help="Print machine-readable results.")
    args = parser.parse_args()

    root = repo_root_from()
    graph = AtlasGraph.load(args.graph_dir, root=root)
    errors = validate(graph)

    result = {
        "graph_dir": str(Path(args.graph_dir)),
        "files": len(graph.files),
        "nodes": len(graph.nodes),
        "edges": len(graph.edges),
        "errors": errors,
    }

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"Atlas Graph validation: {len(graph.nodes)} nodes, {len(graph.edges)} edges")
        if errors:
            print(f"FAILED with {len(errors)} error(s):")
            for error in errors:
                print(f"- {error}")
        else:
            print("OK")

    return 1 if errors else 0


def validate(graph: AtlasGraph) -> list[str]:
    errors: list[str] = []

    if not (graph.graph_dir / "nodes").is_dir():
        errors.append(f"Missing nodes directory: {graph.graph_dir / 'nodes'}")
    if not (graph.graph_dir / "edges").is_dir():
        errors.append(f"Missing edges directory: {graph.graph_dir / 'edges'}")

    node_ids: list[str] = []
    edge_ids: list[str] = []

    for graph_file in graph.files:
        data = graph_file.data
        if not isinstance(data.get("schema_version"), str):
            errors.append(f"{rel(graph_file.path, graph.root)} missing schema_version")
        if not isinstance(data.get("project"), str):
            errors.append(f"{rel(graph_file.path, graph.root)} missing project")

        item_key = "nodes" if graph_file.kind == "nodes" else "edges"
        items = data.get(item_key)
        if not isinstance(items, list):
            errors.append(f"{rel(graph_file.path, graph.root)} missing {item_key} array")
            continue

        for item in items:
            if not isinstance(item, dict):
                errors.append(f"{rel(graph_file.path, graph.root)} contains a non-object item")
                continue
            if graph_file.kind == "nodes":
                validate_item(errors, graph_file.path, graph.root, item, NODE_REQUIRED)
                if isinstance(item.get("id"), str):
                    node_ids.append(item["id"])
            else:
                validate_item(errors, graph_file.path, graph.root, item, EDGE_REQUIRED)
                if isinstance(item.get("id"), str):
                    edge_ids.append(item["id"])

    for duplicate_id, count in duplicated(node_ids).items():
        errors.append(f"Duplicate node id {duplicate_id} appears {count} times")
    for duplicate_id, count in duplicated(edge_ids).items():
        errors.append(f"Duplicate edge id {duplicate_id} appears {count} times")

    node_id_set = set(node_ids)
    for edge in graph.edges:
        edge_id = edge.get("id", "<missing edge id>")
        from_id = edge.get("from")
        to_id = edge.get("to")
        if isinstance(from_id, str) and from_id not in node_id_set:
            errors.append(f"Edge {edge_id} references missing from node {from_id}")
        if isinstance(to_id, str) and to_id not in node_id_set:
            errors.append(f"Edge {edge_id} references missing to node {to_id}")

    for missing in graph.missing_source_paths():
        errors.append(
            f"{missing['kind']} {missing['id']} references missing source {missing['source']}"
        )

    return errors


def validate_item(
    errors: list[str],
    path: Path,
    root: Path,
    item: dict[str, Any],
    required: set[str],
) -> None:
    item_id = item.get("id", "<missing id>")
    for field in sorted(required):
        if field not in item:
            errors.append(f"{rel(path, root)} item {item_id} missing {field}")
    if "source" in item and not isinstance(item["source"], list):
        errors.append(f"{rel(path, root)} item {item_id} source must be a list")


def duplicated(values: list[str]) -> dict[str, int]:
    return {value: count for value, count in Counter(values).items() if count > 1}


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())
