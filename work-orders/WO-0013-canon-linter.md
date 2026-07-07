---
work_order_id: WO-0013
title: Canon Linter
status: proposed
project: atlasstudio
recommended_agent: codex
agent_role: implementation-engineer
risk_level: medium
player_facing: false
engine_specific: false
created: 2026-07-07
---

# WO-0013 - Canon Linter

## Purpose

Create a consistency checker that flags missing, conflicting, incomplete, or disconnected canon facts in Atlas Graph and related project files.

## Player-Facing Goal

Indirect. Canon consistency helps the game world feel coherent and prevents agents from introducing contradictions.

## Background

Atlas Graph validation confirms structural correctness. Canon Linter should go further and ask design-quality questions such as whether locations belong to regions, quests have rewards, NPCs appear somewhere, and concepts have gameplay representation.

## Scope

### In Scope

- Detect canon nodes without required relationship types.
- Detect locations not contained by a region.
- Detect characters that appear nowhere.
- Detect quests with no start, requirement, reward, or unlock.
- Detect concepts with no teaching location or representation.
- Detect infrastructure with no location.
- Detect duplicate names within a type.
- Report warnings without modifying files.

### Out of Scope

- Natural-language contradiction detection across all Markdown.
- Automatic canon repair.
- Final approval of canon.
- Engine-specific implementation validation.

## Inputs

- Atlas Graph canon nodes and edges
- `studio/atlas-graph/node-types.md`
- `studio/atlas-graph/relationship-types.md`

## Deliverables

- Canon lint command under `tools/atlas_graph/` or `tools/atlas_lint/`.
- Documentation for lint rules.
- Sample report.

## Acceptance Criteria

- Tool reports canon warnings separately from structural graph errors.
- Tool identifies disconnected or incomplete canon nodes.
- Tool does not fail the build for draft-stage warnings unless configured.
- Tool output is useful to GPT, Claude, Codex, and the human creator.

## Verification Steps

Example future command:

```bash
python3 tools/atlas_lint/canon_lint.py --project the-last-sword-protocol
```

## Allowed Changes

- `tools/atlas_graph/`
- `tools/atlas_lint/`
- `reports/atlas-lint/`
- documentation files

## Protected Areas

- Do not modify canon graph files unless explicitly asked.
- Do not modify game repositories.

## Notes for Assigned Agent

Think of this as design QA, not just syntax checking. The first version can use simple deterministic graph rules.
