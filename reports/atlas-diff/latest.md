# Atlas Graph Diff

Base: HEAD (projects/the-last-sword-protocol/graph) (28 nodes, 31 edges)
Head: working tree (32 nodes, 37 edges)

Summary: nodes +4 -0 ~0, edges +6 -0 ~0

## Production Changes

### Nodes Added (4)

- tool.atlas_graph_diff (tool) "Atlas Graph Diff Engine" status=draft
- tool.studio_doctor (tool) "Studio Doctor" status=draft
- work_order.wo_0009 (work_order) "Studio Doctor" status=draft
- work_order.wo_0010 (work_order) "Graph Diff Engine" status=draft

### Edges Added (6)

- edge.production.000012: work_order.wo_0009 DEPENDS_ON work_order.wo_0008 status=draft
- edge.production.000013: work_order.wo_0009 ASSIGNED_TO agent.codex status=draft
- edge.production.000014: work_order.wo_0009 CREATES tool.studio_doctor status=draft
- edge.production.000015: work_order.wo_0010 DEPENDS_ON work_order.wo_0008 status=draft
- edge.production.000016: work_order.wo_0010 ASSIGNED_TO agent.claude_code status=draft
- edge.production.000017: work_order.wo_0010 CREATES tool.atlas_graph_diff status=draft
