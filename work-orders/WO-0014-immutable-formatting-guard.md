---
work_order_id: WO-0014
title: Immutable Formatting Guard
status: proposed
project: atlasstudio
recommended_agent: codex
agent_role: implementation-engineer
risk_level: medium
player_facing: false
engine_specific: false
created: 2026-07-07
---

# WO-0014 - Immutable Formatting Guard

## Purpose

Implement the first AtlasStudio guard for the Immutable Formatting Rule.

## Player-Facing Goal

Indirect. Cleaner diffs and safer multi-agent workflows help the project move faster and reduce accidental merge conflicts.

## Background

During WO-0010 work, a script-based graph update initially reformatted existing hand-formatted graph arrays. The change was corrected before commit, but it exposed a recurring multi-agent risk: broad formatting churn can obscure semantic changes.

AtlasStudio needs a rule and tool support to keep semantic changes separate from formatting changes.

## Scope

### In Scope

- Create a check-only formatting guard.
- Document how agents should preserve existing file style.
- Detect broad reformatting patterns where practical.
- Prefer warnings over destructive behavior.
- Support graph JSON files first.
- Optionally support Markdown and YAML heuristics if simple.
- Add README or tool documentation.
- Update production graph facts for the new guard tool.

### Out of Scope

- Auto-formatting the repository.
- Rewriting existing graph files.
- Enforcing a universal formatter.
- Modifying RPG Maker repositories.
- Changing project canon.
- Blocking all whitespace changes.

## Inputs

- `studio/immutable-formatting-rule.md`
- `tools/atlas_graph/`
- `tools/atlas_doctor/`
- `tools/atlas_diff/` or graph diff tooling if present
- Current graph JSON files

## Deliverables

- `tools/atlas_format/format_guard.py` or equivalent.
- Usage documentation.
- Production graph nodes/edges for the formatting guard tool.
- Optional report output under `reports/atlas-format/`.

## Acceptance Criteria

- Tool runs in check-only mode by default.
- Tool does not modify files unless an explicitly named future write mode is implemented and invoked.
- Tool can identify when graph JSON files have broad non-semantic formatting churn compared to a base ref or working tree.
- Tool can report likely formatting-only changes separately from semantic changes.
- Tool exits successfully when no suspicious formatting churn is found.
- Tool reports warnings clearly when suspicious formatting churn is found.
- README or docs explain the Immutable Formatting Rule.

## Verification Steps

Suggested commands:

```bash
python3 tools/atlas_format/format_guard.py --check
python3 tools/atlas_format/format_guard.py --check --base HEAD~1 --head HEAD
python3 tools/atlas_graph/validate_graph.py
python3 tools/atlas_doctor/doctor.py
```

If synthetic fixtures are useful, place them under a clearly named test or scratch fixture folder and do not mix them into production graph data.

## Allowed Changes

- `tools/atlas_format/`
- `reports/atlas-format/`
- `README.md`
- `studio/immutable-formatting-rule.md` if clarification is needed
- `projects/the-last-sword-protocol/graph/nodes/production.nodes.json`
- `projects/the-last-sword-protocol/graph/edges/production.edges.json`

## Protected Areas

- Do not reformat existing graph JSON files.
- Do not modify canon graph files except if explicitly adding a production reference is not possible elsewhere.
- Do not modify RPG Maker repositories.
- Do not change story canon.
- Do not run broad formatters across the repo.

## Notes for Assigned Agent

The goal is not to create a perfect formatter. The goal is to prevent accidental broad reformatting from sneaking into semantic work orders. Start conservative and explain limitations clearly.
