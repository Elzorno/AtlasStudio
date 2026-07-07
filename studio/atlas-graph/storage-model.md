# Atlas Graph Storage Model

## v0 Decision

Atlas Graph v0 uses plain JSON files stored in Git.

This keeps the graph:

- Reviewable in pull requests
- Editable by any agent
- Compatible with simple scripts
- Easy to back up
- Easy to migrate later

## Folder Layout

```text
projects/<project-id>/graph/
  nodes/
    canon.nodes.json
    production.nodes.json
    bridge.nodes.json
  edges/
    canon.edges.json
    production.edges.json
    bridge.edges.json
```

For The Last Sword Protocol:

```text
projects/the-last-sword-protocol/graph/
  nodes/
    canon.nodes.json
    production.nodes.json
    bridge.nodes.json
  edges/
    canon.edges.json
    production.edges.json
    bridge.edges.json
```

## Node File Shape

```json
{
  "schema_version": "0.1.0",
  "project": "the-last-sword-protocol",
  "nodes": [
    {
      "id": "region.ashford_vale",
      "type": "region",
      "name": "Ashford Vale",
      "status": "draft",
      "summary": "Starting region for Journey I.",
      "source": ["projects/the-last-sword-protocol/home-region.md"]
    }
  ]
}
```

## Edge File Shape

```json
{
  "schema_version": "0.1.0",
  "project": "the-last-sword-protocol",
  "edges": [
    {
      "id": "edge.canon.000001",
      "from": "region.ashford_vale",
      "type": "CONTAINS",
      "to": "location.ashford_village",
      "status": "draft",
      "source": ["projects/the-last-sword-protocol/home-region.md"]
    }
  ]
}
```

## Status Values

Recommended node and edge statuses:

- draft
- proposed
- approved
- canon
- deprecated
- retired
- disputed

## Source Tracking

Every node and edge should include one or more source paths.

This keeps the graph connected to human-readable design documents.

## Edit Rules

1. Agents may add draft nodes and edges when working under an approved work order.
2. Agents should not promote draft graph facts to canon without human or AtlasStudio approval.
3. Agents should not delete graph facts unless the work order explicitly permits retirement or replacement.
4. Deprecated facts should usually remain with `status: deprecated` before removal.
5. Engine-specific implementation IDs belong in bridge graph files, not canon graph files.

## Why JSON Instead Of YAML

JSON is stricter, easier to validate, easier to query from Python or JavaScript, and less ambiguous for automated tooling.

Markdown remains the human-facing layer. JSON becomes the graph data layer.

## Future Migration Path

If the graph outgrows files, AtlasStudio can later migrate to:

- SQLite with edge tables
- DuckDB
- Neo4j
- RDF/Turtle
- Custom local service

The v0 file model should be treated as the canonical interchange format even if a faster query backend is added later.
