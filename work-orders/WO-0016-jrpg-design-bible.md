---
work_order_id: WO-0016
title: JRPG Design Bible
status: submitted
project: the-last-sword-protocol
recommended_agent: claude-code
agent_role: senior-software-architect
risk_level: low
player_facing: false
engine_specific: false
created: 2026-07-07
---

# WO-0016 - JRPG Design Bible

## Purpose

Create the gameplay philosophy document set that defines how The Last Sword Protocol should feel: exploration, town, dungeon, discovery, and pacing standards that AtlasStudio uses when reviewing maps, towns, dungeons, quests, encounters, and pacing. This is not story canon and not implementation guidance - it is the design standard every future content work order and design review should be checked against.

## Player-Facing Goal

Indirect. No player-facing content is produced. This work order exists so future world-building work orders (regions, towns, dungeons, quests) are reviewed against one explicit, shared standard rather than each agent inferring "JRPG feel" independently.

## Background

`world-model.md`, `story-reset.md`, `home-region.md`, and `game-vision.md` establish canon and an overworld-first structural rule, and the First Playable Hour milestone (`WO-1000`) sequenced concrete content against that canon. None of these documents state the underlying gameplay-feel philosophy in one place, reviewable independently of any specific beat or region. This work order fills that gap.

## Scope

### In Scope

- A design bible defining exploration-first philosophy, the Journey Principle, Dragon Quest-inspired principles (not mechanics), regional world design, town design, dungeon design, discovery, and cybersecurity integration as gameplay-feel standards.
- An exploration principles document converting the bible's exploration philosophy into concrete, checkable review tests.
- A pacing guidelines document with target pacing for the first hour, first town, first dungeon, first boss, and first region.
- An anti-patterns document naming specific failure modes to avoid, with the reasoning for each, and recommendations for future Atlas Canon Linter rules that could check adherence.

### Out of Scope

- Story canon changes.
- RPG Maker implementation or bridge changes.
- Building new Canon Linter rules (recommended only, not implemented).
- Modifying the First Playable Hour milestone, roadmap, or production documents (referenced, not altered).

## Inputs

- `projects/the-last-sword-protocol/game-vision.md`
- `projects/the-last-sword-protocol/story-reset.md`
- `projects/the-last-sword-protocol/world-model.md`
- `projects/the-last-sword-protocol/home-region.md`
- `projects/the-last-sword-protocol/milestones/first-playable-hour.md`
- `projects/the-last-sword-protocol/roadmap/chapter-01-roadmap.md`
- `tools/atlas_lint/rules/canon_lint_rules.json`
- `studio/governance/atlas-principles.md`
- `studio/immutable-formatting-rule.md`

## Deliverables

- `projects/the-last-sword-protocol/design/jrpg-design-bible.md`
- `projects/the-last-sword-protocol/design/exploration-principles.md`
- `projects/the-last-sword-protocol/design/pacing-guidelines.md`
- `projects/the-last-sword-protocol/design/anti-patterns.md`

## Acceptance Criteria

- The design bible covers all ten requested topics: exploration first, the Journey Principle, Dragon Quest philosophy (principles, not mechanics), regional world design, town design, dungeon design, discovery, cybersecurity integration, pacing (summary, detailed in the companion doc), and anti-patterns (summary, detailed in the companion doc).
- Regional world design explicitly states the required region contents (primary settlement, secondary landmarks, optional discoveries, adventure sites, regional identity) and explicitly rejects giant empty overworlds and Zelda-style connected screen progression.
- Pacing guidelines cover the first hour, first town, first dungeon, first boss, and first region, grounded in the existing milestone/roadmap pacing table where content already exists, with an honest note where content (a true first boss) does not yet exist in current scope.
- Anti-patterns document names all eight requested anti-patterns (Zelda-style screen progression, objective-marker-driven design, tutorial overload, excessive fast travel, empty overworld maps, filler content, arbitrary fetch quests, plugin-first solutions) with reasoning for each.
- Anti-patterns document recommends specific future Canon Linter rules, distinguishing what is graph-checkable from what must remain human/AI creative review.
- No canon file, RPG Maker repository, or graph structure is modified. Existing house formatting style is preserved everywhere.

## Verification Steps

```bash
find projects/the-last-sword-protocol/design -type f
git diff --stat -- projects/the-last-sword-protocol/graph
# expect no output: this work order does not touch the graph
python3 tools/atlas_format/format_guard.py --check
```

## Allowed Changes

- `projects/the-last-sword-protocol/design/`
- `work-orders/WO-0016-jrpg-design-bible.md`

## Protected Areas

- Do not modify canon.
- Do not modify RPG Maker repositories.
- Do not change graph structure.
- Preserve the Immutable Formatting Rule - no reformatting of existing files.

## Notes for Assigned Agent

Documentation only. Ground every principle in what canon and prior work orders already establish (the milestone's actual beats, the world model's actual hierarchy) rather than inventing new lore or contradicting the existing First Playable Hour plan. Where the requested topic (a first boss) has no corresponding content yet in current scope, say so honestly and give forward guidance instead of fabricating content that doesn't exist.

## Submission Record

Submitted 2026-07-07 by Claude Code.

Delivered:

- `projects/the-last-sword-protocol/design/jrpg-design-bible.md` - all ten requested topics, cross-referencing existing canon and the First Playable Hour milestone throughout rather than restating or contradicting it.
- `projects/the-last-sword-protocol/design/exploration-principles.md` - the overworld-as-gameplay-system test, the Journey Principle's four components made concrete, a curiosity-vs-legibility balance rule (redundant hints, no exclusively-optional-dialogue gates), a Dragon Quest principle-to-review-question table, and a regional scale density rule.
- `projects/the-last-sword-protocol/design/pacing-guidelines.md` - first hour (reproducing and citing the existing roadmap pacing table as the canonical reference rather than duplicating a second, divergent one), first town, first dungeon, first boss (honestly noting the milestone has no traditional boss yet and giving forward guidance instead of inventing one), and first region targets, plus a review-usage section.
- `projects/the-last-sword-protocol/design/anti-patterns.md` - all eight requested anti-patterns with feel-breaking rationale tied back to the bible and existing canon documents, plus a Future Integration section recommending specific new Canon Linter rule categories and rule shapes, explicitly separating what is graph-checkable now, what would need a new rule `kind`, and what must remain human/AI creative review per the "deterministic systems before opaque AI" principle.

No canon file, RPG Maker repository, or graph structure was touched - verified directly rather than assumed.

Formatting: preserved existing house style; no existing file was reformatted.

Verification performed:

```bash
find projects/the-last-sword-protocol/design -type f
git diff --stat -- projects/the-last-sword-protocol/graph
python3 tools/atlas_format/format_guard.py --check
```
