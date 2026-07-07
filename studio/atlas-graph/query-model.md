# Atlas Graph Query Model

## Purpose

The query model defines what agents and tools should be able to ask the Atlas Graph.

v0 does not require a full database. Queries can be implemented as simple scripts over JSON files.

## Query Categories

### Entity Lookup

Find one node by ID.

Example:

```bash
atlas-graph get region.ashford_vale
```

Expected answer:

- Node fields
- Incoming edges
- Outgoing edges
- Source documents

### Relationship Lookup

Find all relationships for a node.

Example:

```bash
atlas-graph neighbors region.ashford_vale
```

### Typed Relationship Lookup

Find relationships of a specific type.

Example:

```bash
atlas-graph edges region.ashford_vale --type CONTAINS
```

### Reverse Lookup

Find all nodes that point to a node.

Example:

```bash
atlas-graph incoming location.hidden_cave
```

### Path Query

Find how two nodes are connected.

Example:

```bash
atlas-graph path character.rowan infrastructure.first_relay
```

### Work Order Impact Query

Find what a work order creates, modifies, or depends on.

Example:

```bash
atlas-graph impact work_order.wo_0003
```

### Canon Consistency Query

Find draft, disputed, deprecated, or orphaned facts.

Examples:

```bash
atlas-graph status disputed
atlas-graph orphans
atlas-graph missing-sources
```

## Natural Language Target Questions

AtlasStudio should eventually answer questions like:

- Which locations are in Ashford Vale?
- Which NPCs know about the Hidden Cave?
- Which places teach authentication?
- Which quests require the Last Sword?
- Which work orders affect the RPG Maker bridge?
- Which locations are not yet implemented?
- Which story beats depend on the First Relay?
- Which regions border the Iron Marches?
- Which concepts have no gameplay representation yet?

## Query Output Standard

Query results should include:

- Matching nodes or edges
- Source document paths
- Status values
- Confidence or approval state if available
- Related work orders if available

## Tooling Direction

A future implementation may provide:

```text
tools/atlas_graph/validate_graph.py
tools/atlas_graph/query_graph.py
tools/atlas_graph/explain_node.py
tools/atlas_graph/impact_report.py
```

## Agent Query Rule

Before creating new canon, agents should query the graph or inspect graph files for related existing nodes.

This reduces duplicate names, conflicting lore, and accidental rewrites.
