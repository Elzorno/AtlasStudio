# RPG Maker MZ Ownership Model

## Purpose

The ownership model protects RPG Maker MZ implementation work from accidental overwrites by agents, scripts, imports, or regeneration.

Every bridge target should have an ownership state before an implementation work order modifies it.

## Ownership States

| State | Meaning | Agent Behavior |
|---|---|---|
| `generated` | Fully generated from AtlasStudio or a bridge tool. | May be regenerated when the work order allows it. |
| `agent-drafted` | Drafted by an agent but not yet reviewed by a human. | May be edited by agents with care and clear diffs. |
| `human-edited` | Human has edited or curated the target. | Do not overwrite; modify only explicitly requested ranges. |
| `hand-authored` | Human-authored or intentionally crafted implementation. | Treat as protected; request approval before edits. |
| `locked` | Must not be modified by agents. | Do not edit under any ordinary work order. |

## Protected Target Types

The bridge must track ownership for:

- Maps
- Events
- Common events
- Switches
- Variables
- Database rows
- Plugins and plugin parameters
- Script files
- Tilesets
- Images
- Audio
- Generated reports or manifests

## Map Ownership

Maps are high-risk because RPG Maker stores maps as generated JSON blobs that can contain hand-authored layout, events, encounters, and metadata.

Each map target should record:

- Human-readable map role
- RPG Maker map ID, if known
- File path, if known
- Source design node
- Ownership state
- Last known editor
- Safe edit zones
- Protected event IDs
- Protected region IDs or encounter zones
- Notes for future agents

Example:

```yaml
target: implementation_target.rpgmaker.ashford_village_exterior
design_source: location.ashford_village
map_id: TBD
file: data/MapXXX.json
ownership: agent-drafted
safe_edit_zones:
  - Add new NPC events in reserved event range after audit.
protected:
  - Existing human-authored events
  - Tile layout after human pass
```

## Event Ownership

Events should be protected at event-level granularity when possible.

Each event target should record:

- Event purpose
- Event ID, if known
- Page ownership
- Switch/variable dependencies
- Whether event commands are generated, drafted, or hand-authored

Agents must not reorder, regenerate, or delete existing events unless the work order explicitly authorizes it.

## Database Ownership

Database rows should be handled through reserved ranges rather than ad hoc edits.

Recommended bridge records:

- Actor row range
- Class row range
- Skill row range
- Item/weapon/armor row range
- Enemy row range
- Troop row range
- State row range
- Animation row range

Until ranges are audited and approved, implementation work orders should avoid claiming final database IDs.

## Switch And Variable Ownership

Switches and variables are global coordination points. The bridge should reserve ranges before implementation work uses them.

Recommended fields:

- Range label
- Numeric range
- Purpose
- Owner work order
- Status
- Notes

Example:

```yaml
range: 0101-0125
purpose: Journey 1 critical path
owner: WO-TBD
status: proposed
```

## Audit Rule

Before modifying an existing RPG Maker target, an implementation agent should audit the target and record:

- Current ownership state.
- Existing human-authored or protected content.
- Proposed changed files.
- Whether edits are additive, replacement, or regeneration.
- How the result will be verified.

## Default Assumptions

If ownership is unknown, treat the target as `human-edited`.

If a file exists in the RPG Maker repository and the bridge has no ownership record, agents should inspect it before editing and prefer additive changes over rewrites.

If a work order asks for regeneration but a target is `human-edited`, `hand-authored`, or `locked`, the agent must stop and request approval.

## Reporting Requirement

Every RPG Maker implementation handoff should report:

- Targets changed.
- Ownership state before change.
- Ownership state after change.
- Protected areas avoided.
- Verification performed.
- Any unresolved ownership risks.
