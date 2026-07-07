# RPG Maker MZ Handoff Format

## Purpose

This format defines how AtlasStudio should hand implementation work to Codex or another coding agent for an RPG Maker MZ repository.

It is designed to keep canon in AtlasStudio while giving implementation agents precise, protected, engine-specific instructions.

## Handoff Template

```markdown
---
work_order_id: WO-RPGM-0000
title: Short RPG Maker Implementation Task
status: proposed
project: the-last-sword-protocol
target_repo: TheLastSwordProtocol-Game
recommended_agent: codex
agent_role: implementation-engineer
risk_level: medium
player_facing: true
engine_specific: true
source_work_order: WO-0000
created: YYYY-MM-DD
---

# WO-RPGM-0000 - Title

## Purpose

What should be implemented in RPG Maker MZ?

## Player-Facing Goal

What should the player be able to experience after this change?

## Source Design

- Canon/design nodes:
  - `region.example`
  - `location.example`
- Source documents:
  - `projects/the-last-sword-protocol/...`
- Upstream work orders:
  - `WO-0000`

## RPG Maker Targets

| Target | Current Ownership | Allowed Change |
|---|---|---|
| `data/MapXXX.json` | unknown | Audit before edit |
| `data/System.json` | human-edited | Do not rewrite |
| `js/plugins.js` | human-edited | Additive plugin entry only if approved |

## Allowed Changes

- Explicit file or range.
- Explicit file or range.

## Protected Areas

- Existing hand-authored maps.
- Existing human-authored events.
- Existing database rows outside approved ranges.
- Switches and variables outside approved ranges.

## Implementation Notes

- Preserve existing RPG Maker JSON structure.
- Prefer additive edits.
- Do not run broad formatters.
- Do not change AtlasStudio canon.

## Acceptance Criteria

- Player-facing criterion.
- Player-facing criterion.
- Protected work was not overwritten.
- Bridge/audit record is updated.

## Verification Steps

```bash
command or manual test
```

## Submission Report

- Files changed:
- Ownership states changed:
- Verification performed:
- Risks or follow-up work:
```

## Handoff Fields

### Source Design

Source design links the implementation task back to AtlasStudio canon or design.

Acceptable references:

- Atlas Graph node IDs
- Project Markdown paths
- Work order IDs
- Bridge mapping documents

### RPG Maker Targets

Targets should be as specific as possible.

Examples:

- `data/Map001.json`
- `data/CommonEvents.json`
- `data/Switches` range
- `data/Variables` range
- `data/Enemies.json` rows
- `js/plugins.js`
- `img/characters/...`

If target IDs are unknown, the work order should require an audit step before implementation.

### Allowed Changes

Allowed changes must describe what the agent may edit, not merely what outcome is desired.

Good:

- Add new NPC events in audited empty event ID range.
- Add a new draft map only if map ID is unused.
- Add plugin parameter only after checking existing plugin list.

Bad:

- Make the village work.
- Fix the map.
- Update RPG Maker files as needed.

### Protected Areas

Protected areas should be explicit. If ownership is unknown, assume protection until audited.

### Verification

Verification should include both file-level and player-facing checks when possible.

Examples:

- RPG Maker project opens without JSON parse errors.
- Map transfer works from village to overworld.
- NPC dialogue triggers once and does not loop.
- Switch/variable usage stays in approved range.
- No protected map/event IDs changed.

## Handoff Lifecycle

```text
proposed
  ↓
approved
  ↓
assigned
  ↓
in_progress
  ↓
submitted
  ↓
qa_review
  ↓
accepted
  ↓
closed
```

RPG Maker handoffs follow the AtlasStudio work order lifecycle but must include ownership and verification details before implementation begins.

## Audit Summary Format

Implementation agents should include an audit summary in their submission:

```markdown
## RPG Maker Audit Summary

- Repository:
- Files inspected:
- Files changed:
- Ownership risks:
- Protected targets avoided:
- Switches used:
- Variables used:
- Map IDs used:
- Event IDs used:
- Database rows used:
- Manual test result:
```

## Bridge Rule

If the implementation task requires changing core story, world, region, character, or quest canon, stop and request an AtlasStudio canon revision work order.
