---
work_order_id: WP-03A
title: Ashford Village Experience Specification
status: submitted
project: the-last-sword-protocol
source_work_order: WO-1000
recommended_agent: claude-code
agent_role: senior-software-architect
risk_level: low
player_facing: false
engine_specific: false
required_capabilities:
  - creative-writing
  - canon-design
preferred_capabilities:
  - documentation
produces:
  - design.ashford_village_experience_specification
created: 2026-07-07
---

# WP-03A - Ashford Village Experience Specification

## Purpose

Create the definitive implementation specification for Ashford Village - the last design document before implementation, detailed enough that Codex can begin implementing Ashford Village in `TheLastSwordProtocol-Game` without making creative decisions.

## Player-Facing Goal

Indirect. This package produces no playable content itself (`player_visible: false`); it exists solely to unlock **WP-03B - Ashford Village Implementation**, which will be player-visible.

## Background

`WP-04 Ashford Village Town Build` in `projects/the-last-sword-protocol/production/work-breakdown.md` and `projects/the-last-sword-protocol/design/player-experience-map.md`'s "Immediate Next Player-Visible Target" both point to the same next step: a full experience specification for Ashford Village. `projects/the-last-sword-protocol/design/jrpg-design-bible.md` and its companions (`exploration-principles.md`, `pacing-guidelines.md`, `anti-patterns.md`) establish the design standard this specification must satisfy.

## Scope

### In Scope

- Village purpose (gameplay, narrative, emotional).
- Complete building roster with spatial relationships (no map drawing).
- Complete NPC roster (major and background), personalities, routines, gameplay function, future relevance.
- Dialogue goals (topics/purpose, not scripted lines).
- Player flow from home to departure, marker-free.
- Interactable object list.
- Optional secrets.
- Cybersecurity concepts naturally emerging from village content.
- Acceptance criteria for a complete, playable village.
- A formal `produces` manifest for WP-03B.
- Resolving the previously-flagged Elara's-house canon gap without requesting new canon (household consolidation).

### Out of Scope

- Writing scripted dialogue lines.
- Drawing or laying out an actual map.
- RPG Maker implementation of any kind.
- Canon changes.
- Anything not directly needed to implement the village.

## Inputs

- `projects/the-last-sword-protocol/design/jrpg-design-bible.md`
- `projects/the-last-sword-protocol/design/exploration-principles.md`
- `projects/the-last-sword-protocol/design/pacing-guidelines.md`
- `projects/the-last-sword-protocol/design/anti-patterns.md`
- `projects/the-last-sword-protocol/design/player-experience-map.md`
- `projects/the-last-sword-protocol/milestones/first-playable-hour.md`
- `projects/the-last-sword-protocol/graph/nodes/canon.nodes.json`, `graph/edges/canon.edges.json`
- `studio/governance/player-visible-production-rule.md`

## Deliverables

- `projects/the-last-sword-protocol/design/ashford-village-experience-specification.md`

## Acceptance Criteria

- Covers all ten required sections: village purpose, village layout, NPC roster, dialogue goals, player flow, interactable objects, secrets, cybersecurity concepts, acceptance criteria, and a formal `produces` section.
- Every building has name, purpose, owner, gameplay interactions, and future story use.
- Every NPC has name, role, personality, normal daily activity, gameplay function, and future relevance; major NPCs are separated from background villagers.
- Dialogue goals describe communication intent only, never scripted lines.
- Player flow requires no quest markers.
- Every interactable object and secret is justified (rewards curiosity, reinforces character, or teaches the world).
- Cybersecurity concepts are identified without any classroom-style exposition.
- The `produces` section is a complete, concrete asset manifest WP-03B can be scoped against.
- The document complies with the JRPG Design Bible's anti-patterns list explicitly.
- No canon file, RPG Maker repository, or graph structure is modified.

## Verification Steps

```bash
find projects/the-last-sword-protocol/design -name "ashford-village-experience-specification.md"
git diff --stat -- projects/the-last-sword-protocol/graph
# expect no output: this package does not touch the graph
python3 tools/atlas_format/format_guard.py --check
```

## Allowed Changes

- `projects/the-last-sword-protocol/design/ashford-village-experience-specification.md`
- `work-orders/WP-03A-ashford-village-experience-specification.md`

## Protected Areas

- Do not modify canon.
- Do not modify RPG Maker repositories.
- Do not change graph structure.
- Preserve the Immutable Formatting Rule.

## Notes for Assigned Agent

This package's own `produces` field lists only the specification document itself (`design.ashford_village_experience_specification`) - the downstream implementation assets (`map.ashford_village`, `npc.rowan`, and so on) are listed inside the specification's Section 10 as the contract for WP-03B, not claimed as produced by this package. Do not conflate the two when this feeds into playability tracking (`WO-0017`).

This content sits squarely in GPT's recommended creative-design capability per `studio/agent-roles.md`; it was executed directly by Claude Code here per explicit human instruction, which is consistent with the tie-break rule in `studio/governance/atlas-principles.md` ("capabilities outlive providers... yields to explicit human instruction").

## Submission Record

Submitted 2026-07-07 by Claude Code.

Delivered:

- `projects/the-last-sword-protocol/design/ashford-village-experience-specification.md` covering all ten required sections, grounded in existing canon (`character.rowan`, `character.elara`, `location.ashford_village`) and every prior design document (bible, exploration principles, pacing guidelines, anti-patterns, player experience map) without contradicting any of them.
- A named, resolvable roster: 5 major NPCs (Rowan, Elara, and three production-only named NPCs - Garrick, Mabel, Tomas - explicitly flagged as not-yet-canon) plus a background villager roster, across 4 buildings and one outdoor commons.
- An explicit, transparent resolution of the previously-flagged Elara's-house canon gap (household consolidation into Rowan's Cottage) rather than a silent assumption or a new canon request.
- A concrete `produces` manifest (Section 10) covering 5 maps, 6 NPC entries, 5 interactions, 4 secrets, and 2 dialogue states, ready to scope WP-03B against.

No canon file, RPG Maker repository, or graph structure was touched - verified directly.

Formatting: preserved existing house style; no existing file was reformatted.

Verification performed:

```bash
find projects/the-last-sword-protocol/design -name "ashford-village-experience-specification.md"
git diff --stat -- projects/the-last-sword-protocol/graph
python3 tools/atlas_format/format_guard.py --check
```
