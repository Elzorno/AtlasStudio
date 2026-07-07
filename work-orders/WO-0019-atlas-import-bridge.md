---
work_order_id: WO-0019
title: Atlas Import Bridge
status: submitted
project: the-last-sword-protocol
recommended_agent: claude-code
agent_role: senior-software-architect
risk_level: medium
player_facing: false
engine_specific: false
required_capabilities:
  - architecture-review
  - documentation
preferred_capabilities:
  - graph-analysis
produces:
  - bridge.atlas_import_architecture
  - bridge.atlas_imported_entity_model
  - bridge.atlas_synchronization_strategy
  - bridge.atlas_implementation_handoff
created: 2026-07-07
---

# WO-0019 - Atlas Import Bridge

## Purpose

`WO-0018` established that AtlasStudio is no longer the creative authority for The Last Sword Protocol - `TheLastSwordProtocol-Atlas` is. This work order designs how AtlasStudio imports and understands that authoritative information so it can plan, validate, orchestrate, review, schedule, and bridge to implementation, without ever becoming a competing version of the game.

## Player-Facing Goal

Indirect. This is architecture for how AtlasStudio stays honestly informed about a game it no longer authors, so future AtlasStudio-assisted work (scheduling, review, bridging) is grounded in Atlas's real, current state rather than AtlasStudio's own stale or competing assumptions.

## Background

`work-orders/WO-0018-repository-authority.md` and its conflict analysis found AtlasStudio had built parallel, conflicting canon and production plans for The Last Sword Protocol without knowledge that `TheLastSwordProtocol-Atlas` already existed and was further along. `studio/governance/repository-authority.md` set the permanent ownership boundary; this work order builds the mechanism that lets AtlasStudio respect that boundary in practice rather than only in policy.

## Scope

### In Scope

- Import architecture: discovery, parsing, normalization, traceability, versioning, and conflict detection.
- An entity model for imported characters, locations, quests, work orders, assets, implementation packets, maps, NPCs, and dialogue references, each carrying source repository/path/identifier/timestamp/version.
- A synchronization strategy covering first import, incremental updates, conflict reporting, deleted source items, and renamed items - reporting only, never silent merging.
- An implementation handoff design describing how imported Atlas work packages become provider-specific contracts for Codex, Copilot, GPT, Claude Code, and Ollama without rewriting the original Atlas document.
- Identifying what should explicitly not be imported.
- Recommending future tooling (`atlas_import.py`, `atlas_sync.py`, `atlas_diff.py`, `atlas_status.py`) by name and purpose only.

### Out of Scope

- Implementing any of the recommended tooling.
- Modifying `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` in any way.
- Modifying AtlasStudio's own canon.
- Redesigning gameplay or creating new story content.
- Establishing an actual import cadence or running a real import.

## Inputs

- `work-orders/WO-0018-repository-authority.md`, `reports/governance/repository-conflict-analysis.md`, `studio/governance/repository-authority.md`.
- `TheLastSwordProtocol-Atlas/atlas-exports/home-island.json` (its `contract`, `source`, and `home_island` structure, inspected directly).
- `TheLastSwordProtocol-Atlas/atlas/docs/00_Foundation/Canonical_ID_Registry.md`, `Atlas_ID_Specification.md`.
- Sample frontmatter from `atlas/docs/05_Characters/`, `atlas/docs/02_World/Screens/Home_Island/`, `atlas/docs/09_Technical/Implementation_Packets/Home_Island/`.
- `TheLastSwordProtocol-Atlas/atlas/planning/workorder_queue.json` and a sample `atlas/workorders/*.md` file (confirmed to carry no frontmatter of its own).
- `TheLastSwordProtocol-Game/map_ownership.json`.
- `studio/orchestration/capability-based-orchestration.md`, `studio/agent-roles.md`, `tools/atlas_graph/diff_graph.py`, `tools/atlas_doctor/doctor.py` (existing AtlasStudio tooling this design deliberately reuses rather than reinvents).

## Deliverables

- `bridges/atlas/import-architecture.md`
- `bridges/atlas/imported-entity-model.md`
- `bridges/atlas/synchronization-strategy.md`
- `bridges/atlas/implementation-handoff.md`

## Acceptance Criteria

- Import architecture defines discovery, parsing, normalization, traceability, versioning, and conflict detection, grounded in Atlas's actual export contract and document shapes, not invented abstractly.
- Entity model covers all nine requested entity kinds, each preserving source repository, source path, source identifier, imported timestamp, and imported version.
- What should not be imported is identified explicitly and justified.
- Synchronization strategy covers first import, incremental updates, conflict reporting, deleted source items, and renamed items, and states plainly that AtlasStudio reports changes and never silently merges them.
- Implementation handoff describes provider-specific framing for Codex, Copilot, GPT, Claude Code, and Ollama without rewriting the original Atlas work order or packet.
- Future tooling is named and described, not implemented.
- No sibling repository is modified. No AtlasStudio canon file is modified. No gameplay is redesigned.

## Verification Steps

```bash
find bridges/atlas -name "*.md"
git diff --stat -- projects/the-last-sword-protocol/graph
# expect no output: this work order does not touch canon or graph structure
python3 tools/atlas_format/format_guard.py --check
```

## Allowed Changes

- `bridges/atlas/import-architecture.md`
- `bridges/atlas/imported-entity-model.md`
- `bridges/atlas/synchronization-strategy.md`
- `bridges/atlas/implementation-handoff.md`
- `work-orders/WO-0019-atlas-import-bridge.md`

## Protected Areas

- Do not modify `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game`.
- Do not modify AtlasStudio's canon.
- Do not redesign gameplay.
- Preserve the Immutable Formatting Rule.

## Notes for Assigned Agent

`TheLastSwordProtocol-Atlas` already exports a structured, self-declared `read_only_import: true` contract (`atlas-exports/home-island.json`). Design around that real interface first; treat direct frontmatter/queue parsing as the fallback for what the export does not yet cover, not as the primary path. Reuse AtlasStudio's existing capability-orchestration and Graph Diff Engine machinery wherever the shape fits, rather than inventing parallel concepts.

## Submission Record

Submitted 2026-07-07 by Claude Code.

Delivered:

- `bridges/atlas/import-architecture.md` - discovery built around Atlas's real `atlas-exports/home-island.json` export contract (confirmed by direct inspection: `schema_version`, `source.git_commit`, `contract.atlas_owns`/`game_owns`/`read_only_import`), with frontmatter and work-order-queue parsing as documented fallbacks for what the export does not yet cover; traceability, versioning (source version vs. import version, kept distinct), conflict detection, and a Future Tooling section naming all four requested tools with concrete responsibilities.
- `bridges/atlas/imported-entity-model.md` - all nine requested entity kinds plus reused `production_state`/`tileset`/`transfer`/`event` types, each with the common provenance envelope, grounded in real frontmatter shapes observed in Atlas's own character, screen, and implementation packet documents; an explicit "What Should NOT Be Imported" list (dialogue text, binary assets, Atlas's own orchestrator session state, save data, Decision Record deliberation detail, and the already-retired legacy fork).
- `bridges/atlas/synchronization-strategy.md` - first import, incremental updates (keyed by `source_identifier`, never silently merged), conflict reporting, deleted source items (marked `not_found_at_last_sync`, never auto-deleted), and renamed items (handled per Atlas's own "IDs are stable, names can change" rule).
- `bridges/atlas/implementation-handoff.md` - per-provider framing for Codex, Copilot, GPT, Claude Code, and Ollama, governed by a single "point, don't paraphrase" rule, reusing AtlasStudio's existing capability-orchestration design and `studio/agent-roles.md` provider guidance rather than reinventing routing logic.

No file in `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` was modified. No AtlasStudio canon file was modified. No gameplay was redesigned. Verified directly.

Formatting: preserved existing house style; no existing file was reformatted.

Verification performed:

```bash
find bridges/atlas -name "*.md"
git diff --stat -- projects/the-last-sword-protocol/graph
python3 tools/atlas_format/format_guard.py --check
```
