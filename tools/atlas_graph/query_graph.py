#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from typing import Any

from atlas_graph import DEFAULT_GRAPH_DIR, AtlasGraph, format_edge, node_summary, repo_root_from


def main() -> int:
    parser = argparse.ArgumentParser(description="Query Atlas Graph JSON files.")
    parser.add_argument(
        "--graph-dir",
        default=str(DEFAULT_GRAPH_DIR),
        help="Graph directory containing nodes/ and edges/ folders.",
    )
    parser.add_argument("--json", action="store_true", help="Print machine-readable results.")

    subparsers = parser.add_subparsers(dest="command", required=True)

    get_parser = subparsers.add_parser("get", help="Show a node with incoming/outgoing edges.")
    get_parser.add_argument("node_id")

    neighbors_parser = subparsers.add_parser("neighbors", help="Show all edges touching a node.")
    neighbors_parser.add_argument("node_id")
    neighbors_parser.add_argument("--type", dest="edge_type")

    edges_parser = subparsers.add_parser("edges", help="Show outgoing edges from a node.")
    edges_parser.add_argument("node_id")
    edges_parser.add_argument("--type", dest="edge_type")

    incoming_parser = subparsers.add_parser("incoming", help="Show incoming edges to a node.")
    incoming_parser.add_argument("node_id")
    incoming_parser.add_argument("--type", dest="edge_type")

    path_parser = subparsers.add_parser("path", help="Find a shortest undirected edge path.")
    path_parser.add_argument("start_id")
    path_parser.add_argument("end_id")

    impact_parser = subparsers.add_parser("impact", help="Show what a work order affects.")
    impact_parser.add_argument("work_order_id")

    status_parser = subparsers.add_parser("status", help="Show nodes and edges by status.")
    status_parser.add_argument("status")

    subparsers.add_parser("orphans", help="Show nodes with no incoming or outgoing edges.")
    subparsers.add_parser("missing-sources", help="Show graph facts with missing source paths.")

    args = parser.parse_args()
    graph = AtlasGraph.load(args.graph_dir, root=repo_root_from())
    result = run_query(graph, args)

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print_human(result)

    return 0


def run_query(graph: AtlasGraph, args: argparse.Namespace) -> dict[str, Any]:
    command = args.command
    if command == "get":
        node = graph.get_node(args.node_id)
        return {
            "command": command,
            "node": node,
            "incoming": graph.incoming_edges(args.node_id),
            "outgoing": graph.outgoing_edges(args.node_id),
        }
    if command == "neighbors":
        return {
            "command": command,
            "node": node_summary(graph.get_node(args.node_id)),
            "edges": graph.all_edges_for(args.node_id, args.edge_type),
        }
    if command == "edges":
        return {
            "command": command,
            "node": node_summary(graph.get_node(args.node_id)),
            "edges": graph.outgoing_edges(args.node_id, args.edge_type),
        }
    if command == "incoming":
        return {
            "command": command,
            "node": node_summary(graph.get_node(args.node_id)),
            "edges": graph.incoming_edges(args.node_id, args.edge_type),
        }
    if command == "path":
        return {
            "command": command,
            "start": node_summary(graph.get_node(args.start_id)),
            "end": node_summary(graph.get_node(args.end_id)),
            "path": graph.shortest_path(args.start_id, args.end_id),
        }
    if command == "impact":
        return {
            "command": command,
            "work_order": node_summary(graph.get_node(args.work_order_id)),
            "edges": graph.impact_edges(args.work_order_id),
        }
    if command == "status":
        return {
            "command": command,
            "status": args.status,
            "nodes": graph.nodes_with_status(args.status),
            "edges": graph.edges_with_status(args.status),
        }
    if command == "orphans":
        return {"command": command, "nodes": graph.orphan_nodes()}
    if command == "missing-sources":
        return {"command": command, "missing_sources": graph.missing_source_paths()}
    raise ValueError(f"Unsupported command: {command}")


def print_human(result: dict[str, Any]) -> None:
    command = result["command"]
    if command == "get":
        node = result["node"]
        if node is None:
            print("Node not found")
            return
        print_node(node)
        print_edges("Incoming", result["incoming"])
        print_edges("Outgoing", result["outgoing"])
        return

    if command in {"neighbors", "edges", "incoming", "impact"}:
        label = "Work order" if command == "impact" else "Node"
        node = result.get("work_order") or result.get("node")
        print(f"{label}: {node.get('id') if node else 'not found'}")
        print_edges("Edges", result["edges"])
        return

    if command == "path":
        start = result["start"]["id"] if result["start"] else "not found"
        end = result["end"]["id"] if result["end"] else "not found"
        print(f"Path: {start} -> {end}")
        print_edges("Edges", result["path"])
        return

    if command == "status":
        print(f"Status: {result['status']}")
        print(f"Nodes: {len(result['nodes'])}")
        for node in result["nodes"]:
            print(f"- {node.get('id')} ({node.get('type')})")
        print(f"Edges: {len(result['edges'])}")
        for edge in result["edges"]:
            print(f"- {format_edge(edge)}")
        return

    if command == "orphans":
        print(f"Orphan nodes: {len(result['nodes'])}")
        for node in result["nodes"]:
            print(f"- {node.get('id')} ({node.get('type')})")
        return

    if command == "missing-sources":
        print(f"Missing sources: {len(result['missing_sources'])}")
        for missing in result["missing_sources"]:
            print(f"- {missing['kind']} {missing['id']}: {missing['source']}")


def print_node(node: dict[str, Any]) -> None:
    print(f"{node.get('id')} ({node.get('type')})")
    print(f"Name: {node.get('name')}")
    print(f"Status: {node.get('status')}")
    print(f"Summary: {node.get('summary')}")
    sources = node.get("source", [])
    if sources:
        print("Sources:")
        for source in sources:
            print(f"- {source}")


def print_edges(label: str, edges: list[dict[str, Any]]) -> None:
    print(f"{label}: {len(edges)}")
    for edge in edges:
        print(f"- {format_edge(edge)}")


if __name__ == "__main__":
    raise SystemExit(main())
