---
work_order_id: WO-0018
title: Repository Authority and Canon Reconciliation
status: submitted
project: the-last-sword-protocol
recommended_agent: claude-code
agent_role: senior-software-architect
risk_level: high
player_facing: false
engine_specific: false
required_capabilities:
  - architecture-review
  - canon-design
  - documentation
preferred_capabilities:
  - qa-review
produces:
  - governance.repository_authority
  - governance.atlas_migration_plan
  - report.repository_conflict_analysis
created: 2026-07-07
---

# WO-0018 - Repository Authority and Canon Reconciliation

## Purpose

`WP-03-preflight-map-quality-passability.md` discovered that AtlasStudio and `TheLastSwordProtocol-Atlas` have diverged: two independently canonical design systems targeting the same game, with conflicting protagonist, characters, locations, and production plans. This work order establishes the official ownership boundaries between all repositories involved so implementation can proceed without conflicting sources of truth. It is a governance and migration work order - it does not rewrite story, and it does not implement anything.

## Player-Facing Goal

Indirect, and unusually important despite being indirect: without this reconciliation, implementation agents risk building content that conflicts with, duplicates, or overwrites already-real, already-hand-authored player-facing work.

## Background

Git chronology across all four repositories (`rpgmakerLSP`, `TheLastSwordProtocol-Atlas`, `TheLastSwordProtocol-Game`, AtlasStudio) shows AtlasStudio is the third system in this lineage, not the second, and was started without knowledge that `TheLastSwordProtocol-Atlas` had already cleanly split away from the legacy prototype three days earlier and was already in active, more mature production - including real hand-authored RPG Maker maps for Ashford Village under a different canon (protagonist Kai, Grandmother Elara, no Rowan) than AtlasStudio independently designed.

## Scope

### In Scope

- Review of all three active repositories (AtlasStudio, `TheLastSwordProtocol-Atlas`, `TheLastSwordProtocol-Game`) plus chronology context from `rpgmakerLSP`.
- Determining authoritative ownership per area: story canon, characters, world lore, dialogue, quests, locations, gameplay philosophy, production planning, implementation planning, work orders, validation, tooling, implementation, RPG Maker assets.
- Identifying every significant conflict, classified as CANON, PRODUCTION, IMPLEMENTATION, TOOLING, or DOCUMENTATION, each with an individually-reasoned recommendation (KEEP ATLAS, KEEP ATLASSTUDIO, MERGE, DEPRECATE, or ARCHIVE) - no blanket verdict.
- A permanent repository authority document and change-flow model.
- A migration plan naming what moves forward, becomes historical, should be archived, becomes authoritative, and what implementation agents should ignore.
- A production recommendation for `WP-03A` (unchanged, updated, or superseded).

### Out of Scope

- Modifying `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` in any way.
- Modifying AtlasStudio's existing canon graph files.
- Overwriting, deleting, or rewriting any existing AtlasStudio document.
- Redesigning gameplay or creating new story content.
- Deciding Rowan's fate unilaterally (that decision belongs to `TheLastSwordProtocol-Atlas`'s own process, per the conflict analysis).

## Inputs

- `work-orders/WP-03-preflight-map-quality-passability.md` and its three reports under `reports/rpg-maker-bridge/`.
- `TheLastSwordProtocol-Atlas/AGENTS.md`, `README.md`, `atlas/docs/00_Foundation/`, `atlas/planning/workorder_queue.json`, `atlas/planning/Journey_I_Completion_Plan.md`.
- `TheLastSwordProtocol-Game/AGENTS.md`, `map_ownership.json`, `data/System.json`, `data/Tilesets.json`, `data/Map001.json`, `data/Map002.json`.
- `rpgmakerLSP/atlas/README.md` (chronology and precedent only).
- AtlasStudio's own `README.md`, `studio/vision.md`, canon graph, and every project-specific document listed in the migration plan.

## Deliverables

- `studio/governance/repository-authority.md`
- `studio/governance/atlas-v1-to-atlas-v2-migration.md`
- `reports/governance/repository-conflict-analysis.md`
- `work-orders/WO-0018-repository-authority.md`

## Acceptance Criteria

- Ownership is determined for every listed area, with cited evidence, not assertion.
- Every significant conflict is identified, classified by type, and given an individually-reasoned recommendation - no conflict is resolved by silently choosing a winner without stated evidence.
- `repository-authority.md` defines permanent responsibilities for all three active repositories and how future changes flow between them.
- The migration plan states what moves forward, what becomes historical, what should be archived, what becomes authoritative, and what implementation agents should ignore.
- A clear, reasoned recommendation is given for `WP-03A`'s status (unchanged, updated, or superseded), with minimum-edit reasoning if "updated" is chosen.
- No RPG Maker repository is modified. No AtlasStudio canon file is modified. No existing document is overwritten.

## Verification Steps

```bash
find studio/governance -name "repository-authority.md" -o -name "atlas-v1-to-atlas-v2-migration.md"
find reports/governance -name "repository-conflict-analysis.md"
git diff --stat -- projects/the-last-sword-protocol/graph
# expect no output: this work order does not touch canon or graph structure
python3 tools/atlas_format/format_guard.py --check
python3 tools/atlas_graph/validate_graph.py
```

## Allowed Changes

- `studio/governance/repository-authority.md`
- `studio/governance/atlas-v1-to-atlas-v2-migration.md`
- `reports/governance/repository-conflict-analysis.md`
- `work-orders/WO-0018-repository-authority.md`

## Protected Areas

- Do not modify `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game`.
- Do not modify AtlasStudio's story canon.
- Do not overwrite any existing document.
- Do not redesign gameplay or create new story content.
- Preserve the Immutable Formatting Rule.

## Notes for Assigned Agent

This is a hard finding to deliver cleanly: most of AtlasStudio's project-specific work on The Last Sword Protocol is superseded by a more mature parallel system it didn't know existed. State this plainly and with evidence, not defensively. The correct response to discovering this is to document it precisely and set a boundary that prevents recurrence, not to minimize it or to quietly patch around it.

## Production Recommendation: WP-03A

**Recommendation: SUPERSEDED**, not merely updated.

**Reasoning:** `WP-03A`'s Ashford Village Experience Specification was built on the premise that Ashford Village was an unclaimed design space. It is not - `TheLastSwordProtocol-Atlas` already has completed implementation packets (`IMP-HOM-017`, `IMP-HOM-018`) and real, hand-authored maps (`Map001`, `Map002`) for this exact location, under different, already-implemented canon (Kai, Grandmother Elara, no Rowan, a different building roster, a different starting location). This is not a case of a few outdated details in an otherwise-sound document - the document's central premises (who lives there, what the home is called, what buildings exist, where the player starts) are each individually contradicted by already-real implementation. "Updated" would imply a small, bounded edit could bring it back into alignment; that is not the case here, because the correct source document for Ashford Village already exists in `TheLastSwordProtocol-Atlas` under a different name (its own Implementation Packets), not as a variant of `WP-03A`.

**What this means concretely:** `WP-03A` and its companion `WP-03` production package should not be used to guide any future implementation work on Ashford Village. If AtlasStudio has a future role regarding this location at all, it would be as a bridge-documentation consumer of `TheLastSwordProtocol-Atlas`'s existing packets - not as an independent spec author. No minimum-edit list is provided because there is no bounded edit that resolves a superseded premise; per the "Do NOT redesign gameplay" constraint, no replacement specification is drafted here either.

## Submission Record

Submitted 2026-07-07 by Claude Code.

Delivered:

- `reports/governance/repository-conflict-analysis.md` - full chronology across four repositories, ownership determination for all fourteen requested areas with cited evidence, and sixteen individually-classified and individually-reasoned conflicts (protagonist, Elara, Rowan, building roster, starting location, first-hour scope, region geography, map ownership, work-order numbering, gameplay philosophy, cybersecurity framing, and four tooling/terminology conflicts), each recommending KEEP ATLAS, KEEP ATLASSTUDIO, MERGE, DEPRECATE, or ARCHIVE with rationale - no blanket verdict applied.
- `studio/governance/repository-authority.md` - permanent ownership boundaries for all three active repositories plus the retired legacy prototype, and a change-flow model requiring any AtlasStudio tooling proposal to `TheLastSwordProtocol-Atlas` to go through that repository's own Decision Record process rather than a direct write.
- `studio/governance/atlas-v1-to-atlas-v2-migration.md` - precise three-system naming (Legacy Prototype / Atlas / AtlasStudio) replacing the ambiguous "v1" framing that partly caused this conflict, plus explicit what-moves-forward, what-becomes-historical, what-becomes-authoritative, and what-implementation-agents-should-ignore sections.
- The WP-03A production recommendation above: **SUPERSEDED**, with full reasoning and no fabricated minimum-edit list, since none exists for a superseded premise.

No file in `TheLastSwordProtocol-Atlas`, `TheLastSwordProtocol-Game`, or AtlasStudio's canon graph was modified - verified directly. No existing AtlasStudio document was overwritten; historical status is established by this migration record, not by editing the historical files themselves.

Formatting: preserved existing house style; no existing file was reformatted.

Verification performed:

```bash
find studio/governance -name "repository-authority.md" -o -name "atlas-v1-to-atlas-v2-migration.md"
find reports/governance -name "repository-conflict-analysis.md"
git diff --stat -- projects/the-last-sword-protocol/graph
python3 tools/atlas_format/format_guard.py --check
python3 tools/atlas_graph/validate_graph.py
```
