---
work_order_id: WO-0015
title: Atlas Constitution and Core Principles
status: submitted
project: atlasstudio
recommended_agent: claude-code
agent_role: senior-software-architect
risk_level: low
player_facing: false
engine_specific: false
created: 2026-07-07
---

# WO-0015 - Atlas Constitution and Core Principles

## Purpose

Atlas Core has reached Version 1.0. Create the foundational document set that defines the philosophy, engineering principles, governance, and design decisions that future humans and AI agents must follow - the engineering constitution of AtlasStudio, not marketing copy or user documentation.

## Player-Facing Goal

Indirect. No player-facing content is produced. This work order exists so that every future architectural decision across AtlasStudio is made against a shared, explicit set of principles and a traceable decision history, rather than being re-derived or contradicted ad hoc.

## Background

Atlas Core has grown organically through WO-0001 (foundation), WO-0007/WO-0008 (graph and tooling), WO-0010 (graph diff), WO-0011 (planning engine), WO-0012 (originally Agent Scheduler, since retired and replaced by capability-based orchestration), WO-0013 (canon linter), WO-0014 (immutable formatting guard), and WO-0005 (RPG Maker bridge). Each of these embodied a real architectural decision, but none of those decisions were recorded in one place with their rationale. This work order consolidates that history and declares Atlas Core 1.0 stable.

## Scope

### In Scope

- A root constitution document (`ATLAS_CORE_1.0.md`) covering vision, core philosophy, Atlas Core architecture and component interaction, governance summary, ADR process summary, and a 1.0 stability declaration.
- A deeper principles document (`studio/governance/atlas-principles.md`) explaining the rationale behind each core belief, how to resolve conflicts between principles, and the concrete Atlas Core vs. Projects governance test.
- A reusable ADR template (`studio/governance/decision-record-template.md`).
- An architectural decision log (`studio/governance/architectural-decision-log.md`) seeded with the major decisions already made, including the Agent Scheduler -> Capability-Based Orchestration supersession.

### Out of Scope

- Modifying game repositories.
- Modifying canon.
- Changing graph structure (no graph node or edge additions/changes).
- Building new tooling.

## Inputs

- `studio/atlas-core.md`, `studio/vision.md`, `studio/workflow.md`, `studio/agent-roles.md`, `studio/work-order-format.md`, `studio/immutable-formatting-rule.md`
- `studio/atlas-graph/` (overview, storage model, query model, diff model)
- `studio/orchestration/capability-based-orchestration.md`, `atlas-core/capabilities/README.md`, `atlas-core/providers/README.md`
- `tools/atlas_doctor/`, `tools/atlas_graph/`, `tools/atlas_lint/`, `tools/atlas_planner/`, `tools/atlas_format/`, `tools/rpg_maker_bridge/`
- `bridges/rpg-maker-mz/`
- Existing work orders WO-0001 through WO-0014, WO-1000, WP-01, WP-02

## Deliverables

- `ATLAS_CORE_1.0.md`
- `studio/governance/atlas-principles.md`
- `studio/governance/decision-record-template.md`
- `studio/governance/architectural-decision-log.md`

## Acceptance Criteria

- The constitution document covers vision, core philosophy, Atlas Core architecture (Planning Engine, Capability-Based Orchestration, Graph, Doctor, Validator, Canon Linter, Graph Diff, Immutable Formatting Guard, Bridge Layer) with an explicit description of how they interact, governance, and an ADR process summary, and declares Atlas Core 1.0 stable.
- The governance section states when Atlas Core changes are appropriate versus when a change belongs under `projects/`.
- The ADR template is reusable and includes status, context, decision, consequences, alternatives considered, and related work orders/documents.
- The decision log is seeded with the major decisions already made: capability-first orchestration (and its supersession of the original Agent Scheduler), the Immutable Formatting Rule, the human provider, the rule-driven Canon Linter, the Atlas Core vs. Projects split, and deterministic planning.
- No canon, graph structure, or game repository is modified.

## Verification Steps

```bash
git diff --stat -- projects/the-last-sword-protocol/graph
# expect no output: graph structure is untouched by this work order
find ATLAS_CORE_1.0.md studio/governance -type f
python3 tools/atlas_format/format_guard.py --check
```

## Allowed Changes

- `ATLAS_CORE_1.0.md`
- `studio/governance/`
- `work-orders/WO-0015-atlas-constitution-and-core-principles.md`

## Protected Areas

- Do not modify game repositories.
- Do not modify canon.
- Do not change graph structure.

## Notes for Assigned Agent

Documentation only. Preserve existing house style across every referenced document; do not reformat any file this work order does not own. Ground every architectural claim in what has actually been built (read the referenced tools and docs rather than describing an aspirational version of them).

## Submission Record

Submitted 2026-07-07 by Claude Code.

Delivered:

- `ATLAS_CORE_1.0.md` - vision, eight core philosophy statements, an architecture section covering all nine named components (Planning Engine, Capability-Based Orchestration, Graph, Doctor, Validator, Canon Linter, Graph Diff Engine, Immutable Formatting Guard, Bridge Layer) with a single interaction-loop diagram, a governance summary, an ADR process summary, and a Version 1.0 Stable declaration defining what "stable" binds.
- `studio/governance/atlas-principles.md` - each philosophy statement expanded with why it matters and how to apply it, a precedence order for resolving conflicts between principles, and a concrete Atlas Core vs. Projects governance test plus a list of what does/does not require an ADR.
- `studio/governance/decision-record-template.md` - reusable ADR template with Status, Date, Context, Decision, Consequences, Alternatives Considered, Related, and a Governance Note field tying back to the ADR-trigger criteria.
- `studio/governance/architectural-decision-log.md` - eleven seeded ADRs covering: Atlas Core vs. Projects split, the Git-native JSON graph decision, stdlib-only deterministic tooling, the Immutable Formatting Rule, the Graph Diff Engine, the original manual-first Agent Scheduler (marked superseded), its replacement by capability-based orchestration, the rule-driven Canon Linter, the deterministic Planning Engine, the engine bridge ownership model, and the human-as-provider decision.

No canon file, graph JSON file, or game repository was touched. This was verified directly (see Verification Steps) rather than assumed.

Formatting: preserved existing house style across all new documents; no existing file was reformatted.

Verification performed:

```bash
git diff --stat -- projects/the-last-sword-protocol/graph
find ATLAS_CORE_1.0.md studio/governance -type f
python3 tools/atlas_format/format_guard.py --check
```
