---
work_order_id: WP-03
title: Ashford Village Production Package
status: submitted
project: the-last-sword-protocol
source_work_order: WO-1000
recommended_agent: claude-code
agent_role: senior-software-architect
risk_level: low
player_facing: false
engine_specific: true
required_capabilities:
  - architecture-review
  - rpg-maker-json
  - documentation
preferred_capabilities:
  - qa-review
produces:
  - production.ashford_village_production_package
  - production.ashford_village_map_brief
  - production.ashford_village_event_plan
  - production.ashford_village_implementation_checklist
created: 2026-07-07
---

# WP-03 - Ashford Village Production Package

## Purpose

Bridge the approved Ashford Village design (`WP-03A`) into an implementation contract implementation agents can execute with minimal creative interpretation. This is the final production package before RPG Maker implementation (WP-03B) begins - it does not redesign the village.

## Player-Facing Goal

Indirect. This package produces no playable content itself (`player_visible: false`); it exists to unlock **WP-03B - Ashford Village Implementation**, which will be player-visible.

## Background

`WP-03A` delivered the Ashford Village Experience Specification. `bridges/rpg-maker-mz/map-quality-standard.md` and `bridges/rpg-maker-mz/passability-rule.md` establish the quality and passability bar every RPG Maker map in this project must clear. `WP-03-preflight-map-quality-passability` was positioned to inspect the real game repository's tileset/passability data before implementation but remains `status: proposed` - this package works around that gap by specifying tileset roles and passability requirements rather than asserting unverified concrete IDs, and flags the gap explicitly rather than guessing.

## Scope

### In Scope

- A production package summary indexing the three companion documents and stating what each provider role (Codex, Copilot, GPT, Atlas tooling, Human) needs or should do.
- A map brief: target dimensions, tileset roles, visual goals, landmarks, environmental storytelling, composition, road layout, building placement, elevation, foliage/decoration density.
- An event plan: every required event (start, transfers, NPCs, signs, bookshelf, save/rest, shops, ambient events, secrets, expansion hooks), implementation requirements only, no dialogue text.
- An engineering implementation checklist for WP-03B.
- Studying the official RPG Maker MZ sample project under `references/` for composition, density, event organization, JSON structure, map scale, and passability assumptions.

### Out of Scope

- Redesigning gameplay or story.
- Modifying canon.
- Modifying any RPG Maker repository.
- Generating actual maps or events.
- Writing dialogue text.
- Copying any map, event, or dialogue content from the reference sample project.

## Inputs

- `ATLAS_CORE_1.0.md`, `studio/governance/atlas-principles.md`
- `projects/the-last-sword-protocol/design/jrpg-design-bible.md`, `exploration-principles.md`, `pacing-guidelines.md`, `anti-patterns.md`
- `projects/the-last-sword-protocol/design/player-experience-map.md`
- `projects/the-last-sword-protocol/design/ashford-village-experience-specification.md`
- `bridges/rpg-maker-mz/bridge-design.md`, `ownership-model.md`, `handoff-format.md`, `map-quality-standard.md`, `passability-rule.md`
- `references/rpg-maker-mz-samples/official sample project/` (reference-only, study composition and structure, do not copy)

## Deliverables

- `projects/the-last-sword-protocol/production/ashford-village-production-package.md`
- `projects/the-last-sword-protocol/production/ashford-village-map-brief.md`
- `projects/the-last-sword-protocol/production/ashford-village-event-plan.md`
- `projects/the-last-sword-protocol/production/ashford-village-implementation-checklist.md`

## Acceptance Criteria

- Map brief defines target dimensions, tileset role(s), visual goals, landmarks, environmental storytelling, composition notes, road layout, building placement relationships, elevation, foliage density, and decoration density, and states the sample-map comparable quality target.
- Event plan lists every required event category requested (player start, transfers, NPCs, signs, bookshelves, save point, shop, inn, ambient events, secrets, future expansion hooks) as implementation requirements only, with no dialogue text.
- Implementation checklist is a concrete, checkable engineering checklist covering buildings, NPC placement, transfers, passability, required routes, free departure, and sample-map quality review.
- Production package summary states what Codex needs, what Copilot can help with, what GPT should review, what Atlas validates, and what requires human approval.
- No map, event, or dialogue content is copied from the reference sample project - only composition, density, structure, and quality are matched.
- No canon file, RPG Maker repository, or graph structure is modified.

## Verification Steps

```bash
find projects/the-last-sword-protocol/production -name "ashford-village-*.md"
git diff --stat -- projects/the-last-sword-protocol/graph
# expect no output: this package does not touch the graph
python3 tools/atlas_format/format_guard.py --check
```

## Allowed Changes

- `projects/the-last-sword-protocol/production/ashford-village-production-package.md`
- `projects/the-last-sword-protocol/production/ashford-village-map-brief.md`
- `projects/the-last-sword-protocol/production/ashford-village-event-plan.md`
- `projects/the-last-sword-protocol/production/ashford-village-implementation-checklist.md`
- `work-orders/WP-03-ashford-village-production-package.md`

## Protected Areas

- Do not redesign gameplay or story.
- Do not modify canon.
- Do not modify RPG Maker repositories.
- Do not generate maps or events.
- Preserve the Immutable Formatting Rule.

## Notes for Assigned Agent

This package's own `produces` field lists the four production documents it creates, not the downstream map/NPC/event assets WP-03B will produce - those remain listed as WP-03B's future contract inside the event plan and checklist. Do not conflate the two for playability tracking (`WO-0017`).

The map brief deliberately avoids asserting concrete numeric tileset IDs from the real `TheLastSwordProtocol-Game` repository, since verifying those is `WP-03-preflight`'s explicit, still-open job. This is flagged prominently in the production package summary rather than silently worked around.

## Submission Record

Submitted 2026-07-07 by Claude Code.

Delivered:

- `ashford-village-production-package.md` - summary, reference materials used, the open WP-03-preflight dependency flagged explicitly, and the Codex/Copilot/GPT/Atlas/Human responsibility breakdown.
- `ashford-village-map-brief.md` - target dimensions grounded in real study of the reference sample project (its "Normal Town" at 40x40 and house/shop interiors at roughly 13x11 to 21x18, both cited as composition benchmarks, not copied content), tileset roles (not asserted concrete IDs), visual goals, landmarks, environmental storytelling, composition, road layout/building placement, elevation, foliage and decoration density, and the required "Comparable quality target: Official RPG Maker MZ sample maps" statement.
- `ashford-village-event-plan.md` - every requested event category as implementation requirements only, including an explicit scope clarification that Rowan's "morning vs. later" placement language in the specification should be implemented via the existing before/after-sword flag, not a new day/night system - a concrete ambiguity resolved before it could reach Codex as a creative decision.
- `ashford-village-implementation-checklist.md` - a full engineering checklist covering maps, NPC placement, events, secrets, the world-state flag, passability (with named required routes), player flow, quality review, and production graph recording.
- `work-orders/WP-03-ashford-village-production-package.md` - `status: submitted`.

No canon file, RPG Maker repository, or graph structure was touched - verified directly. No map, event, or dialogue content was copied from the reference sample project; only its scale, structure, and quality were studied and cited as benchmarks.

Formatting: preserved existing house style; no existing file was reformatted.

Verification performed:

```bash
find projects/the-last-sword-protocol/production -name "ashford-village-*.md"
git diff --stat -- projects/the-last-sword-protocol/graph
python3 tools/atlas_format/format_guard.py --check
```
