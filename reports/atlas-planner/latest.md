# Atlas Planning Engine Report

Project: `the-last-sword-protocol`
Generated: 2026-07-07
Mode: `recommend_only`

## Inputs

- Graph: `projects/the-last-sword-protocol/graph`
- Nodes: 38
- Edges: 47
- Work orders read: 13
- Work order statuses: accepted: 3, proposed: 5, submitted: 5
- Canon lint findings: 18

## Doctor Signals

- Connect WO-0004 to its agent assignment or production impact, or retire it intentionally.
- Create bridge implementation targets before translating canon into RPG Maker tasks.
- Review WO-0005 before relying on the RPG Maker bridge for implementation work.

## Recommendations

### 1. Define RPG Maker implementation targets for Ashford Vale

- ID: `proposal.bridge_implementation_targets`
- Type: proposed_follow_up
- Status: not_created
- Priority: must-fix (80/100)
- Recommended agents: codex, claude-code
- Source: planner proposal
- Score:
  - milestone_impact: 5/5
  - dependency_value: 5/5
  - technical_debt: 3/5
  - player_value: 4/5
  - core_platform_value: 3/5
- Evidence:
  - Studio Doctor reports zero implementation target nodes.
  - Studio Doctor reports zero bridge implementation edges.
  - Canon lint Bridge category reports missing implementation mappings for region/location/infrastructure nodes.
  - This should be a human-approved work order before RPG Maker files are touched.
- Human action: Review and approve before creating or assigning work.

### 2. RPG Maker Bridge Design

- ID: `work_order.wo_0005`
- Type: existing_work_order
- Status: proposed
- Priority: must-fix (80/100)
- Recommended agents: claude-code, codex
- Source: `work-orders/WO-0005-rpg-maker-bridge.md`
- Score:
  - milestone_impact: 5/5
  - dependency_value: 5/5
  - technical_debt: 3/5
  - player_value: 3/5
  - core_platform_value: 4/5
- Evidence:
  - WO-0005 is proposed and has not been submitted or accepted.
  - Metadata recommends `claude-code` for role `senior-software-architect`.
  - Work order is engine-specific and may unlock implementation handoff.
  - Graph relationships: work_order.wo_0005 CREATES bridge.rpg_maker_mz [edge.production.000003]
  - Studio Doctor reports no implementation targets or bridge implementation edges yet.
  - Project matches requested planning target `the-last-sword-protocol`.
- Human action: Approve, assign, or revise this existing work order. The planner did not create new work.

### 3. Resolve orphaned production work orders

- ID: `proposal.resolve_orphan_work_orders`
- Type: proposed_follow_up
- Status: not_created
- Priority: should-do (68/100)
- Recommended agents: codex, claude-code
- Source: planner proposal
- Score:
  - milestone_impact: 2/5
  - dependency_value: 4/5
  - technical_debt: 5/5
  - player_value: 1/5
  - core_platform_value: 5/5
- Evidence:
  - Studio Doctor flags orphan work order nodes: work_order.wo_0004.
  - Orphaned production facts reduce graph usefulness for planning and scheduling.
- Human action: Review and approve before creating or assigning work.

### 4. Agent Assignment System

- ID: `work_order.wo_0004`
- Type: existing_work_order
- Status: proposed
- Priority: should-do (68/100)
- Recommended agents: claude-code
- Source: `work-orders/WO-0004-agent-assignment-system.md`
- Score:
  - milestone_impact: 0/5
  - dependency_value: 4/5
  - technical_debt: 5/5
  - player_value: 3/5
  - core_platform_value: 5/5
- Evidence:
  - WO-0004 is proposed and has not been submitted or accepted.
  - Metadata recommends `claude-code` for role `senior-software-architect`.
  - Studio Doctor currently flags this work order as orphaned.
- Human action: Approve, assign, or revise this existing work order. The planner did not create new work.

### 5. Connect existing canon facts to production work orders

- ID: `proposal.connect_canon_to_work_orders`
- Type: proposed_follow_up
- Status: not_created
- Priority: should-do (56/100)
- Recommended agents: codex
- Source: planner proposal
- Score:
  - milestone_impact: 2/5
  - dependency_value: 3/5
  - technical_debt: 4/5
  - player_value: 1/5
  - core_platform_value: 4/5
- Evidence:
  - Canon Linter reports 11 Production coverage findings.
  - Better production coverage helps future agents understand why canon facts exist.
- Human action: Review and approve before creating or assigning work.

### 6. Home Region Overworld Design

- ID: `work_order.wo_0003`
- Type: existing_work_order
- Status: proposed
- Priority: should-do (52/100)
- Recommended agents: gpt, claude-code
- Source: `work-orders/WO-0003-home-region-overworld.md`
- Score:
  - milestone_impact: 5/5
  - dependency_value: 2/5
  - technical_debt: 0/5
  - player_value: 5/5
  - core_platform_value: 1/5
- Evidence:
  - WO-0003 is proposed and has not been submitted or accepted.
  - Metadata recommends `gpt` for role `creative-systems-designer`.
  - Work order is player-facing, so it can improve First Playable Hour momentum.
  - Graph relationships: work_order.wo_0003 MODIFIES region.ashford_vale [edge.production.000002]
  - Canon lint reports production coverage gaps for current story/world canon.
  - Project matches requested planning target `the-last-sword-protocol`.
- Human action: Approve, assign, or revise this existing work order. The planner did not create new work.

### 7. Agent Scheduler

- ID: `work_order.wo_0012`
- Type: existing_work_order
- Status: proposed
- Priority: should-do (52/100)
- Recommended agents: claude-code
- Source: `work-orders/WO-0012-agent-scheduler.md`
- Score:
  - milestone_impact: 0/5
  - dependency_value: 4/5
  - technical_debt: 3/5
  - player_value: 1/5
  - core_platform_value: 5/5
- Evidence:
  - WO-0012 is proposed and has not been submitted or accepted.
  - Metadata recommends `claude-code` for role `senior-software-architect`.
- Human action: Approve, assign, or revise this existing work order. The planner did not create new work.

### 8. Last Sword Protocol Story Reset

- ID: `work_order.wo_0002`
- Type: existing_work_order
- Status: proposed
- Priority: should-do (48/100)
- Recommended agents: gpt, claude-code
- Source: `work-orders/WO-0002-last-sword-story-reset.md`
- Score:
  - milestone_impact: 4/5
  - dependency_value: 2/5
  - technical_debt: 0/5
  - player_value: 5/5
  - core_platform_value: 1/5
- Evidence:
  - WO-0002 is proposed and has not been submitted or accepted.
  - Metadata recommends `gpt` for role `creative-systems-designer`.
  - Work order is player-facing, so it can improve First Playable Hour momentum.
  - Graph relationships: work_order.wo_0002 MODIFIES character.hero [edge.production.000001]
  - Canon lint reports production coverage gaps for current story/world canon.
  - Project matches requested planning target `the-last-sword-protocol`.
- Human action: Approve, assign, or revise this existing work order. The planner did not create new work.

### 9. Seed Agent Scheduler production graph facts

- ID: `proposal.seed_agent_scheduler_graph`
- Type: proposed_follow_up
- Status: not_created
- Priority: nice-to-have (44/100)
- Recommended agents: claude-code, codex
- Source: planner proposal
- Score:
  - milestone_impact: 1/5
  - dependency_value: 2/5
  - technical_debt: 3/5
  - player_value: 0/5
  - core_platform_value: 5/5
- Evidence:
  - WO-0012 exists as a Markdown work order but is not yet represented in production graph nodes.
  - Planning and scheduling tools work better when work-order metadata is reflected in graph data.
- Human action: Review and approve before creating or assigning work.

## Guardrails

- This report does not create work orders.
- Human approval is required before new work is created, assigned, or implemented.
- No canon or RPG Maker files are modified by the planner.

