# RPG Maker MZ Bridge Design

## Purpose

The RPG Maker MZ Bridge translates AtlasStudio's engine-independent design into safe, reviewable RPG Maker implementation work.

The bridge is not the game project. It is the contract between AtlasStudio and an RPG Maker MZ repository such as `TheLastSwordProtocol-Game`.

## Design Goals

- Keep story, world, and region canon engine-independent.
- Give RPG Maker-specific details a defined home.
- Protect hand-authored maps, events, database rows, plugins, and assets.
- Produce implementation work orders that Codex can execute in the game repository.
- Preserve enough audit data for AtlasStudio to understand what was generated, drafted, edited, or locked.

## Bridge Boundary

AtlasStudio core documents may define:

- Regions
- Locations
- Characters
- Quests
- Story beats
- Progression gates
- Encounter identity
- Design intent

The RPG Maker MZ bridge may define:

- Map names and intended map roles
- Candidate map ID ranges
- Event ownership and event purpose
- Switch and variable ranges
- Database target ranges
- Plugin parameters
- Asset slots and naming conventions
- Implementation work order handoff data
- Audit records from game repository checks

The bridge must not silently change canon. If implementation reveals that canon needs to change, the agent must request a canon revision instead of rewriting project canon.

## Folder Model

```text
bridges/rpg-maker-mz/
  bridge-design.md
  ownership-model.md
  handoff-format.md
  mappings/
    maps.md
    switches.md
    variables.md
    database.md
    plugins.md
  audits/
    YYYY-MM-DD-audit.md
  handoffs/
    WO-XXXX-rpgmaker-implementation.md
```

Only the first three bridge documents are required for WO-0005. The remaining folders are the intended home for future bridge work.

## Translation Flow

```text
AtlasStudio canon/design
  ↓
Bridge mapping proposal
  ↓
Implementation work order
  ↓
Codex modifies RPG Maker repo
  ↓
RPG Maker audit
  ↓
Bridge records implementation facts
  ↓
AtlasStudio reviews playable result
```

## Design-To-Implementation Mapping

Each implementation target should connect one design entity to one RPG Maker responsibility.

Examples:

| AtlasStudio Entity | RPG Maker Target | Notes |
|---|---|---|
| `region.ashford_vale` | Overworld map group | One or more RPG Maker maps may implement a region. |
| `location.ashford_village` | Village exterior and interiors | Map IDs are bridge details, not canon. |
| `location.hidden_cave` | Dungeon map group | Encounters, treasure, and traversal belong in handoff details. |
| `infrastructure.first_relay` | Event sequence or map object | Switches/variables belong in bridge mappings. |
| `item.last_sword` | Database weapon/item row | Database IDs belong in bridge mappings. |

## Implementation Work Order Requirements

An RPG Maker implementation work order should include:

- Source canon/design nodes.
- Target RPG Maker repository path.
- Allowed map, event, database, plugin, asset, switch, and variable ranges.
- Ownership state for every touched target.
- Required backup or diff expectations.
- Verification steps that can run locally.
- Player-facing acceptance criteria.
- A clear rollback or review strategy.

## Verification Expectations

Bridge-driven implementation is complete only when:

1. The RPG Maker project opens or validates after edits.
2. The player-facing route or feature can be tested.
3. Protected work was not overwritten.
4. The bridge records what changed.
5. AtlasStudio can trace the implementation back to source canon and work orders.

## Non-Goals

This bridge design does not:

- Write RPG Maker JSON.
- Assign final map IDs.
- Reserve actual switch or variable ranges.
- Create tilesets or assets.
- Replace the game repository's own source control.

Those decisions belong to later implementation or audit work orders.
