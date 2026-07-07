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

Create a rule-driven canon consistency checker that flags incomplete, conflicting, missing, or disconnected canon facts in the Atlas Graph.

## Player-Facing Goal

Indirect. Better canon consistency helps the game world feel coherent and prevents agents from introducing contradictions.

## Background

Atlas Graph validation confirms structural correctness: files parse, node IDs are unique, edge references resolve, and sources exist.

Canon Linter is different. It is Level 3 Atlas QA.

It should ask design-quality questions such as whether locations belong to regions, quests have rewards, NPCs appear somewhere, and concepts have gameplay representation.

## Atlas QA Level

This work order targets **Level 3 - Canon Validation**.

AtlasStudio validation levels:

1. Structural Validation: Can Atlas read this?
2. Referential Validation: Does everything point somewhere real?
3. Canon Validation: Does the world make sense?
4. Experience Validation: Will this actually be fun?

WO-0013 is Level 3 only.

## Scope

### In Scope

- Implement deterministic canon linting over Atlas Graph data.
- Make the linter rule-driven from day one.
- Load lint rules from metadata files, preferably JSON.
- Define lint rule categories.
- Report canon warnings separately from fatal structural graph errors.
- Detect canon nodes without required relationship types.
- Detect locations not contained by a region.
- Detect characters that appear nowhere.
- Detect quests with no start, goal, requirement, reward, completion, or unlock relationship where applicable.
- Detect concepts with no teaching location or representation.
- Detect infrastructure with no location.
- Detect duplicate names within a type.
- Detect monster families with no encounter/use relationship if such nodes exist.
- Detect story beats not connected to a journey or region if such nodes exist.
- Report findings without modifying files.

### Out of Scope

- Natural-language contradiction detection across all Markdown.
- LLM-based canon review.
- Automatic canon repair.
- Final approval of canon.
- Engine-specific implementation validation.
- Experience/fun scoring.
- Modifying canon graph files.

## Rule Categories

The first linter should support rule categories even if only some categories have initial rules.

| Category | Purpose | Example Finding |
|---|---|---|
| Structure | Missing required design relationships | Region has no contained settlement. |
| Completeness | Expected design content is missing | Quest has no reward. |
| Consistency | Facts conflict or duplicate each other | Duplicate character names within one project. |
| Coverage | Design goals are not represented | Authentication concept is never taught. |
| Production | Canon is disconnected from workflow | Canon node has no creating work order. |
| Bridge | Canon is not implementation-ready | Region has no implementation target. |

## Rule-Driven Requirement

The linter must not hardcode every rule directly into procedural Python.

Define lint rules as metadata so future agents can add or adjust rules without rewriting linter code.

Preferred location:

```text
rules/canon-lint/*.json
```

Acceptable alternative:

```text
tools/atlas_lint/rules/*.json
```

Rule metadata should include at least:

- rule id
- category
- severity
- description
- target node type or relationship pattern
- required relationship or condition
- applicable statuses

The implementing agent may refine the exact schema if it is documented.

## Inputs

- Atlas Graph canon nodes and edges
- `studio/atlas-graph/node-types.md`
- `studio/atlas-graph/relationship-types.md`
- `studio/immutable-formatting-rule.md`
- `tools/atlas_graph/`
- Current graph tooling and reports

## Deliverables

- Canon lint command under `tools/atlas_lint/` or `tools/atlas_graph/`.
- Rule metadata files for initial canon lint rules.
- Documentation for lint rule categories and rule format.
- Sample report under `reports/atlas-lint/`.
- Production graph facts for the Canon Linter tool.

## Acceptance Criteria

- Tool reports canon warnings separately from structural graph errors.
- Tool identifies disconnected or incomplete canon nodes.
- Tool is rule-driven through metadata files.
- Tool includes lint rule categories in output.
- Tool does not fail the build for draft-stage warnings unless configured.
- Tool can produce a readable console report.
- Tool can optionally write a Markdown report.
- Tool output is useful to GPT, Claude, Codex, and the human creator.
- Tool respects the Immutable Formatting Rule and does not reformat existing graph JSON.

## Verification Steps

Expected examples:

```bash
python3 tools/atlas_lint/canon_lint.py --project the-last-sword-protocol
python3 tools/atlas_lint/canon_lint.py --project the-last-sword-protocol --output reports/atlas-lint/latest.md
python3 tools/atlas_graph/validate_graph.py
python3 tools/atlas_format/format_guard.py --check
python3 tools/atlas_doctor/doctor.py
```

## Allowed Changes

- `tools/atlas_lint/`
- `tools/atlas_graph/` only if shared graph loading needs a small compatible extension
- `rules/canon-lint/` or `tools/atlas_lint/rules/`
- `reports/atlas-lint/`
- documentation files
- production graph nodes/edges for the new linter tool

## Protected Areas

- Do not modify canon graph files unless explicitly asked.
- Do not modify game repositories.
- Do not change story canon.
- Do not run broad formatters.
- Do not mix formatting normalization with semantic changes.

## Notes for Assigned Agent

Think of this as deterministic design QA, not syntax checking.

Start conservative. It is acceptable for the first rule set to produce warnings on the current draft graph. Warnings should teach the team what canon is incomplete, not block progress unnecessarily.

Formatting: preserve existing house style and avoid broad JSON rewrites.
