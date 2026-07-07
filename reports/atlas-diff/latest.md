# Atlas Graph Diff

Base: HEAD (projects/the-last-sword-protocol/graph) (38 nodes, 47 edges)
Head: working tree (46 nodes, 60 edges)

Summary: nodes +8 -0 ~0, edges +13 -0 ~0

## Production Changes

### Nodes Added (8)

- agent.github_copilot (agent) "GitHub Copilot" status=draft
- agent.ollama (agent) "Ollama / Local Models" status=draft
- provider.anthropic (provider) "Anthropic" status=draft
- provider.github_copilot (provider) "GitHub Copilot" status=draft
- provider.ollama (provider) "Ollama" status=draft
- provider.openai (provider) "OpenAI" status=draft
- work_order.wo_0012 (work_order) "Agent Scheduler" status=draft
- work_order.wo_1000 (work_order) "First Playable Hour Master Plan" status=draft

### Edges Added (13)

- edge.production.000028: work_order.wo_0012 DEPENDS_ON work_order.wo_0004 status=draft
- edge.production.000029: work_order.wo_0012 ASSIGNED_TO agent.claude_code status=draft
- edge.production.000030: agent.gpt PROVIDED_BY provider.openai status=draft
- edge.production.000031: agent.codex PROVIDED_BY provider.openai status=draft
- edge.production.000032: agent.claude_code PROVIDED_BY provider.anthropic status=draft
- edge.production.000033: agent.github_copilot PROVIDED_BY provider.github_copilot status=draft
- edge.production.000034: agent.ollama PROVIDED_BY provider.ollama status=draft
- edge.production.000035: work_order.wo_0012 REVIEWED_BY agent.human status=draft
- edge.production.000036: work_order.wo_1000 DEPENDS_ON work_order.wo_0002 status=draft
- edge.production.000037: work_order.wo_1000 DEPENDS_ON work_order.wo_0003 status=draft
- edge.production.000038: work_order.wo_1000 DEPENDS_ON work_order.wo_0005 status=draft
- edge.production.000039: work_order.wo_1000 ASSIGNED_TO agent.claude_code status=draft
- edge.production.000040: work_order.wo_1000 REVIEWED_BY agent.human status=draft
