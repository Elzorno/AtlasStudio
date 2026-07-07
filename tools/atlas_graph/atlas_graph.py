from __future__ import annotations

import json
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_GRAPH_DIR = Path("projects/the-last-sword-protocol/graph")


@dataclass(frozen=True)
class GraphFile:
    path: Path
    kind: str
    data: dict[str, Any]


@dataclass
class AtlasGraph:
    root: Path
    graph_dir: Path
    files: list[GraphFile]
    nodes: dict[str, dict[str, Any]]
    edges: list[dict[str, Any]]
    outgoing: dict[str, list[dict[str, Any]]]
    incoming: dict[str, list[dict[str, Any]]]

    @classmethod
    def load(
        cls, graph_dir: str | Path = DEFAULT_GRAPH_DIR, root: str | Path | None = None
    ) -> "AtlasGraph":
        root_path = Path(root or ".").resolve()
        graph_path = Path(graph_dir)
        if not graph_path.is_absolute():
            graph_path = root_path / graph_path
        graph_path = graph_path.resolve()

        graph_files: list[GraphFile] = []
        nodes: dict[str, dict[str, Any]] = {}
        edges: list[dict[str, Any]] = []
        outgoing: dict[str, list[dict[str, Any]]] = defaultdict(list)
        incoming: dict[str, list[dict[str, Any]]] = defaultdict(list)

        for path in sorted((graph_path / "nodes").glob("*.nodes.json")):
            data = _read_json(path)
            graph_files.append(GraphFile(path=path, kind="nodes", data=data))
            for node in data.get("nodes", []):
                node_id = node.get("id")
                if isinstance(node_id, str):
                    nodes[node_id] = node

        for path in sorted((graph_path / "edges").glob("*.edges.json")):
            data = _read_json(path)
            graph_files.append(GraphFile(path=path, kind="edges", data=data))
            for edge in data.get("edges", []):
                edges.append(edge)
                from_id = edge.get("from")
                to_id = edge.get("to")
                if isinstance(from_id, str):
                    outgoing[from_id].append(edge)
                if isinstance(to_id, str):
                    incoming[to_id].append(edge)

        return cls(
            root=root_path,
            graph_dir=graph_path,
            files=graph_files,
            nodes=nodes,
            edges=edges,
            outgoing=dict(outgoing),
            incoming=dict(incoming),
        )

    def get_node(self, node_id: str) -> dict[str, Any] | None:
        return self.nodes.get(node_id)

    def outgoing_edges(self, node_id: str, edge_type: str | None = None) -> list[dict[str, Any]]:
        return _filter_edges(self.outgoing.get(node_id, []), edge_type)

    def incoming_edges(self, node_id: str, edge_type: str | None = None) -> list[dict[str, Any]]:
        return _filter_edges(self.incoming.get(node_id, []), edge_type)

    def all_edges_for(self, node_id: str, edge_type: str | None = None) -> list[dict[str, Any]]:
        return self.outgoing_edges(node_id, edge_type) + self.incoming_edges(node_id, edge_type)

    def impact_edges(self, work_order_id: str) -> list[dict[str, Any]]:
        return [
            edge
            for edge in self.outgoing_edges(work_order_id)
            if edge.get("type") in {"CREATES", "MODIFIES", "DEPENDS_ON"}
        ]

    def nodes_with_status(self, status: str) -> list[dict[str, Any]]:
        return [node for node in self.nodes.values() if node.get("status") == status]

    def edges_with_status(self, status: str) -> list[dict[str, Any]]:
        return [edge for edge in self.edges if edge.get("status") == status]

    def orphan_nodes(self) -> list[dict[str, Any]]:
        return [
            node
            for node_id, node in self.nodes.items()
            if not self.outgoing.get(node_id) and not self.incoming.get(node_id)
        ]

    def missing_source_paths(self) -> list[dict[str, str]]:
        missing: list[dict[str, str]] = []
        for node in self.nodes.values():
            missing.extend(self._missing_sources_for("node", node))
        for edge in self.edges:
            missing.extend(self._missing_sources_for("edge", edge))
        return missing

    def shortest_path(self, start_id: str, end_id: str) -> list[dict[str, Any]]:
        if start_id == end_id:
            return []

        queue: deque[tuple[str, list[dict[str, Any]]]] = deque([(start_id, [])])
        visited = {start_id}

        while queue:
            node_id, path = queue.popleft()
            for edge in self.all_edges_for(node_id):
                next_id = edge.get("to") if edge.get("from") == node_id else edge.get("from")
                if not isinstance(next_id, str) or next_id in visited:
                    continue
                next_path = path + [edge]
                if next_id == end_id:
                    return next_path
                visited.add(next_id)
                queue.append((next_id, next_path))
        return []

    def _missing_sources_for(self, kind: str, item: dict[str, Any]) -> list[dict[str, str]]:
        missing: list[dict[str, str]] = []
        item_id = str(item.get("id", "<missing id>"))
        source_paths = item.get("source", [])
        if not isinstance(source_paths, list):
            return [{"kind": kind, "id": item_id, "source": "<source is not a list>"}]
        for source in source_paths:
            if not isinstance(source, str):
                missing.append({"kind": kind, "id": item_id, "source": "<non-string source>"})
                continue
            if not (self.root / source).exists():
                missing.append({"kind": kind, "id": item_id, "source": source})
        return missing


def repo_root_from(path: str | Path | None = None) -> Path:
    start = Path(path or ".").resolve()
    for candidate in (start, *start.parents):
        if (candidate / ".git").exists():
            return candidate
    return start


def format_edge(edge: dict[str, Any]) -> str:
    return f"{edge.get('from')} {edge.get('type')} {edge.get('to')} [{edge.get('id')}]"


def node_summary(node: dict[str, Any] | None) -> dict[str, Any] | None:
    if node is None:
        return None
    return {
        "id": node.get("id"),
        "type": node.get("type"),
        "name": node.get("name"),
        "status": node.get("status"),
        "summary": node.get("summary"),
        "source": node.get("source", []),
    }


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def _filter_edges(edges: list[dict[str, Any]], edge_type: str | None) -> list[dict[str, Any]]:
    if edge_type is None:
        return list(edges)
    return [edge for edge in edges if edge.get("type") == edge_type]
