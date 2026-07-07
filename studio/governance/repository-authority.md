# Repository Authority

## Purpose

This document defines the permanent ownership boundaries between the repositories involved in The Last Sword Protocol, and how changes should flow between them going forward. It exists because `reports/governance/repository-conflict-analysis.md` found that AtlasStudio was built independently of, and without knowledge of, an already-more-mature parallel system - `TheLastSwordProtocol-Atlas` - governing the same game. This document is the permanent fix for that blind spot, not a one-time patch.

This is a governance document, not a design document. It does not create or rewrite any story, character, location, or gameplay content.

## The Four Repositories

### `TheLastSwordProtocol-Atlas`

**Role: the canonical specification for The Last Sword Protocol.**

Owns, for this project:

- Story canon, characters, world lore, dialogue, quests, and locations.
- Gameplay philosophy and the cybersecurity metaphor layer, as they apply to this specific game.
- Production planning (journeys, milestones, build gates) and implementation planning (implementation packets) for this project.
- The work order series that governs this project's actual production (`WO-0001` onward in that repository).
- Validation of its own canonical object model (`atlas-tools/validator/`).

This repository's own `AGENTS.md` already states its rule correctly: "Treat `atlas/` as the source of truth." This document extends that same rule to include AtlasStudio - AtlasStudio should treat it as the source of truth too, for this project.

### `TheLastSwordProtocol-Game`

**Role: the implementation target.**

Owns:

- The actual RPG Maker MZ runtime project, its map files, database, and assets.
- `map_ownership.json`, the per-map ownership ledger, which is the sole authority on which map files may be written by pipeline scripts versus which are hand-authored or locked.
- Final art, audio, and effect assets.

This repository consumes Atlas exports and implementation packets from `TheLastSwordProtocol-Atlas`. It should not be treated as a second source of design truth even though it is where the game actually runs - its own `AGENTS.md` already says as much.

### AtlasStudio (this repository)

**Role, corrected by this document: general-purpose, project-agnostic Atlas Core methodology and tooling - not an active design or production authority for The Last Sword Protocol.**

Retains, going forward:

- Atlas Core tooling that has no equivalent in `TheLastSwordProtocol-Atlas`'s toolchain and may be proposed for adoption there: the Graph Diff Engine (`tools/atlas_graph/diff_graph.py`) and the Immutable Formatting Guard (`tools/atlas_format/format_guard.py`).
- Governance methodology of general value: the ADR practice (`studio/governance/architectural-decision-log.md`), the capability-based orchestration *design rationale* (independent of which repository's orchestrator executes it), and the ownership-model methodology in `bridges/rpg-maker-mz/ownership-model.md` as a template, not as this project's live ledger.
- A complete, preserved historical record of AtlasStudio's own parallel work on this project (work orders, canon graph, design documents, production plans) - retained for provenance, not deleted, per the Immutable Formatting Rule's broader spirit of never destroying history to hide a mistake.

Does **not** own, going forward, for The Last Sword Protocol specifically:

- Story canon, characters, world lore, dialogue, quests, or locations.
- Gameplay philosophy specific to this project (superseded by `Studio_Manifesto.md` and `Gameplay_Systems_Bible.md`).
- Production or implementation planning for this project (superseded by `Journey_I_Completion_Plan.md` and the Implementation Packets series).
- Any claim to be "the director" of this specific game's production.

If AtlasStudio is used to direct a *future*, different game project, none of the above restriction applies to that future project - this document scopes the correction to The Last Sword Protocol only, because that is the specific conflict found.

### `rpgmakerLSP` (legacy, referenced for completeness)

**Role: retired legacy prototype.** Already handled correctly by `TheLastSwordProtocol-Atlas`'s own `WO-0029` - its stale Atlas fork was replaced with a pointer README on 2026-07-05. No further action is needed from AtlasStudio regarding this repository; it is documented here only so the full lineage is visible in one place.

## Change Flow Between Repositories

```text
TheLastSwordProtocol-Atlas (canonical specification)
  |
  | exports, implementation packets
  v
TheLastSwordProtocol-Game (implementation target)
```

- Any change to this project's canon, characters, world lore, dialogue, quests, locations, gameplay philosophy, or production/implementation plans happens in `TheLastSwordProtocol-Atlas`, through that repository's own work-order and Decision Record process. AtlasStudio does not originate these changes.
- Any change to `TheLastSwordProtocol-Game`'s map, database, or asset files happens through that repository's own `map_ownership.json` ledger rules and `AGENTS.md` workflow, driven by `TheLastSwordProtocol-Atlas`'s implementation packets.
- If AtlasStudio identifies a tool or methodology (per the "Retains" list above) that could benefit `TheLastSwordProtocol-Atlas`, AtlasStudio may **propose** it - as a document, a described approach, or a standalone script offered for review - but must not write directly into `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game`. Adoption requires an explicit decision recorded in `TheLastSwordProtocol-Atlas`'s own Decision Records by its Production Director, mirroring how AtlasStudio requires an ADR for its own architectural changes (`studio/governance/atlas-principles.md`).
- If a future AtlasStudio-directed project (not The Last Sword Protocol) needs its own canon and production planning, AtlasStudio performs that role directly for that project, since no equivalent conflict exists there.

## What This Document Does Not Do

It does not merge the two repositories, does not delete or overwrite any AtlasStudio document (see `atlas-v1-to-atlas-v2-migration.md` for exactly what is archived versus what remains active), and does not modify `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` in any way. Every conflict's specific reasoning lives in `reports/governance/repository-conflict-analysis.md`; this document states the resulting permanent boundary, not the case-by-case argument for it.

## Review

This document should be revisited if AtlasStudio takes on a new project, if `TheLastSwordProtocol-Atlas` and `TheLastSwordProtocol-Game` are retired or merged, or if a proposed tooling adoption (Graph Diff Engine, Immutable Formatting Guard) is accepted into `TheLastSwordProtocol-Atlas`'s own toolchain, at which point this document's "Retains" list should be updated to reflect what was actually adopted.
