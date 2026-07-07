# Legacy Prototype To Atlas Migration

## Purpose

This document describes what moves forward, what becomes historical, what should be archived, what becomes authoritative, and what implementation agents should ignore, following the findings in `reports/governance/repository-conflict-analysis.md` and the boundaries set in `studio/governance/repository-authority.md`.

## Naming Note

This document is filed as `atlas-v1-to-atlas-v2-migration.md` per the work order that requested it, but the investigation found the lineage is not a clean "v1 to v2" story - it is three systems, not two. To avoid perpetuating the same ambiguity that caused this conflict (Conflict 16 in the conflict analysis), this document uses precise names throughout:

- **Legacy Prototype** = `rpgmakerLSP` (first commit 2026-06-27) - the original monolithic prototype.
- **Atlas** = `TheLastSwordProtocol-Atlas` + `TheLastSwordProtocol-Game` (first commits 2026-07-04) - the clean split of the Legacy Prototype, and the system this document confirms as authoritative for The Last Sword Protocol.
- **AtlasStudio** = this repository (first commit 2026-07-07) - a third, independently-started system whose project-specific work on The Last Sword Protocol is superseded by Atlas, per this migration.

## What Moves Forward

For The Last Sword Protocol, everything moves forward under **Atlas** (`TheLastSwordProtocol-Atlas` + `TheLastSwordProtocol-Game`):

- All story canon, characters (Kai, Grandmother Elara, and the rest of the Character Bible), world lore, dialogue, quests, and locations.
- The Journey I Completion Plan and its Build Gate/Implementation Packet production model.
- The already-hand-authored Ashford Exterior (Map001) and Elara House (Map002) maps, and the `map_ownership.json` ledger governing them.
- The Studio Manifesto and Gameplay Systems Bible as this project's gameplay philosophy.
- The Cybersecurity Layer Bible as this project's cybersecurity metaphor authority.

For AtlasStudio itself, as a repository, these move forward regardless of this migration:

- The Graph Diff Engine and Immutable Formatting Guard tools, as project-agnostic Atlas Core capabilities, proposable to Atlas but not dependent on this project to remain useful.
- The ADR practice and governance methodology in `studio/governance/`.
- The capability-based orchestration design rationale, as methodology independent of any one project.
- AtlasStudio's ability to direct a different, future game project, unaffected by this migration.

## What Becomes Historical

The following AtlasStudio artifacts, produced for The Last Sword Protocol before this migration, become historical record. They are **not deleted** - git history and the files themselves remain - but they should no longer be read as active canon, active production plans, or a live implementation contract for this project:

- `projects/the-last-sword-protocol/graph/nodes/canon.nodes.json` and `graph/edges/canon.edges.json` (world.elyndor, region.ashford_vale, character.hero, character.elara, character.rowan, item.last_sword, and related canon facts).
- `projects/the-last-sword-protocol/game-vision.md`, `story-reset.md`, `world-model.md`, `home-region.md`.
- `work-orders/WO-1000-first-playable-hour-master-plan.md` and its production documents: `milestones/first-playable-hour.md`, `roadmap/chapter-01-roadmap.md`, `production/implementation-plan.md`, `production/dependency-map.md`, `production/work-breakdown.md`.
- `work-orders/WP-03A-ashford-village-experience-specification.md` and `projects/the-last-sword-protocol/design/ashford-village-experience-specification.md`.
- `work-orders/WP-03-ashford-village-production-package.md` and its four companion documents (`ashford-village-production-package.md`, `ashford-village-map-brief.md`, `ashford-village-event-plan.md`, `ashford-village-implementation-checklist.md`).
- `projects/the-last-sword-protocol/design/jrpg-design-bible.md` and its companions (`exploration-principles.md`, `pacing-guidelines.md`, `anti-patterns.md`), superseded in authority (though not necessarily in quality - see the conflict analysis's Conflict 10) by the Studio Manifesto and Gameplay Systems Bible.
- `projects/the-last-sword-protocol/design/player-experience-map.md`.
- AtlasStudio's own production-graph facts tied to these work orders (`work_order.wo_1000`, `work_order.wp_03a`, `work_order.wp_03`, and their associated nodes/edges).

## What Should Be Archived

No file move or deletion is performed by this work order (per its constraints: do not overwrite existing documents, do not modify canon). Instead, "archived" here means: each historical document above should be understood as **frozen and non-authoritative for this project**, starting from this migration record's existence. A future, narrowly-scoped documentation work order may add a short pointer note atop each historical file (in the style of `rpgmakerLSP/atlas/README.md`'s "Atlas Has Moved" pattern) without rewriting their content, if that becomes useful. This document itself, plus `studio/governance/repository-authority.md`, is sufficient to establish the historical status in the meantime.

## What Should Become Authoritative

Going forward, anyone working on The Last Sword Protocol - human or agent - should treat as authoritative:

- `TheLastSwordProtocol-Atlas/atlas/docs/` for all story, character, world, gameplay, and cybersecurity-layer canon.
- `TheLastSwordProtocol-Atlas/atlas/planning/` and `atlas/workorders/` for production and implementation planning.
- `TheLastSwordProtocol-Atlas/atlas-tools/` for validation of that canon.
- `TheLastSwordProtocol-Game/map_ownership.json` and `AGENTS.md` for what may and may not be written in the implementation target.

## What Implementation Agents Should Ignore

Any agent (Codex, Claude Code, GPT, GitHub Copilot, Ollama, or human) picking up implementation work on The Last Sword Protocol should ignore, for this project:

- AtlasStudio's canon graph (`character.hero`, `character.rowan`, "Rowan's Cottage," the four-building Ashford roster) as a source of what to build.
- `work-orders/WO-1000` and its production documents as a scheduling authority.
- `WP-03A`'s Ashford Village Experience Specification and `WP-03`'s production package as an implementation contract for Ashford Village.
- Any AtlasStudio recommendation that a village, character, or location "does not yet exist" for The Last Sword Protocol without first checking `TheLastSwordProtocol-Atlas` and `TheLastSwordProtocol-Game` directly - AtlasStudio's own graph is demonstrably incomplete relative to what Atlas already has implemented (Skyreach Hill and Fogfen Marsh being the clearest examples, per Conflict 7 in the conflict analysis).

Agents should still read `studio/governance/repository-authority.md` and this document first, precisely so they do not repeat the mistake this migration corrects.

## What This Migration Does Not Do

It does not rewrite, delete, or silently supersede any file's content - every historical document listed above remains exactly as written, in git history and on disk. It does not modify `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game`. It does not invent new story, canon, or gameplay content. It is a governance record of what already happened and what should happen next, nothing more.
