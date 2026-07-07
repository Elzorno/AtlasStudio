# AtlasStudio Health Report

Project: `the-last-sword-protocol`
Generated: 2026-07-07

## Graph Integrity

- Graph directory: `projects/the-last-sword-protocol/graph`
- Files: 6
- Nodes: 30
- Edges: 34
- Structural errors: 0
- Missing sources: 0

### Structural Errors

- None.

## Canon

- Canon graph has implementation candidates, but none have implementation links yet.

## Production

- Work orders: 8
- Work order statuses: accepted: 3, proposed: 4, submitted: 1

### Production Findings

- Orphan work orders need assignment, dependency, review, or impact edges: work_order.wo_0004.
- Work order lifecycle mix: accepted=3, proposed=4, submitted=1.

### Orphan Nodes

- work_order.wo_0004 (work_order) - Agent Assignment System

## Implementation

- Bridges: 1
- Bridge edges: 0
- Implementation targets: 0
- Implementation-candidate canon nodes: 7
- Canon nodes with implementation links: 0

### Readiness Signals

- bridge_defined: ready - At least one engine bridge node exists.
- implementation_targets_defined: not ready - Implementation target nodes are recorded.
- bridge_edges_defined: not ready - Bridge implementation edges exist.
- canon_implementation_links: not ready - Canon nodes have implementation mappings.

### Implementation Findings

- RPG Maker bridge node exists in graph data.
- No implementation target nodes are present yet.
- No bridge implementation edges are present yet.
- RPG Maker bridge design work order is proposed.
- Playable implementation readiness is early: canon exists, but graph has no implementation mappings.

## Tools

- Registered tools: 3

### Tool Findings

- Registered AtlasStudio tools: tool.atlas_graph_query, tool.atlas_graph_validator, tool.studio_doctor.

## Missing Sources

- None.

## Recommendations

- Connect WO-0004 to its agent assignment or production impact, or retire it intentionally.
- Create bridge implementation targets before translating canon into RPG Maker tasks.
- Review WO-0005 before relying on the RPG Maker bridge for implementation work.
