# Ashford Village Implementation Checklist

## Purpose

This is the engineering checklist for **WP-03B**. It exists to make "done" checkable, not debatable. Every line should be verifiable by a specific person or tool, named in parentheses where useful.

## Maps

- [ ] Ashford Village exterior map built to `ashford-village-map-brief.md` target dimensions and tileset role.
- [ ] Rowan's Cottage interior built.
- [ ] General Store interior built.
- [ ] Blacksmith interior built.
- [ ] Inn interior built.
- [ ] Village Green (well + memorial + open space) complete within the exterior map.
- [ ] Building placement relationships match the map brief's Road Layout And Building Placement Relationships section.
- [ ] Exactly one village exit/entrance to the Ashford Vale overworld exists.

## NPC Placement

- [ ] Rowan placed and functional (cottage placement and Green placement, flag-gated per the event plan).
- [ ] Elara placed and functional (cottage placement, garden placement if implemented).
- [ ] Garrick placed and functional inside the Blacksmith.
- [ ] Mabel placed and functional inside the General Store.
- [ ] Tomas placed and functional inside the Inn.
- [ ] Background villagers (children, elderly villager, farmer, optional peddler) placed per specification Section 3 locations.

## Events

- [ ] Player start configured at Rowan's Cottage on a passable tile.
- [ ] All transfers implemented per the event plan's Transfers section (cottage, store, blacksmith, inn, and the overworld exit).
- [ ] Village exit transfer confirmed unconditional (no flag/item/dialogue gate).
- [ ] Signs implemented at General Store, Blacksmith, and Inn.
- [ ] Bookshelf implemented in Rowan's Cottage with first-look and gated second-look (journal page) pages.
- [ ] Rest/HP-MP-restore interaction implemented at the Inn.
- [ ] General Store shop processing implemented (basic consumables).
- [ ] Blacksmith shop processing implemented (basic weapon/armor).
- [ ] Ambient background villager movement configured (non-blocking).
- [ ] Ambient audio (BGS) configured for the exterior map.
- [ ] Well interaction implemented, including the echo detail.
- [ ] Village Memorial interaction implemented.
- [ ] Fireplace interaction implemented (Rowan's Cottage).
- [ ] Barrel/crate flavor interactions implemented near shops.

## Secrets

- [ ] Hidden Herb implemented (Elara's garden), self-switch gated.
- [ ] Hidden Coin (Barrel) implemented, self-switch gated.
- [ ] Optional Viewpoint implemented at the village edge, with at least one overworld landmark visible from it.
- [ ] No secret blocks or is required for any critical-path action (Section 9 of the specification).

## World-State Flag

- [ ] A single before/after-sword flag controls every two-page NPC event (Rowan, Elara, Garrick, Mabel) - confirmed to be the same flag the milestone document's Beat 6 world-state change uses, not a duplicate.
- [ ] `dialogue.ashford_day` content wired to the default (before) state.
- [ ] `dialogue.ashford_after_sword` content wired to the flagged (after) state.

## Passability (per `bridges/rpg-maker-mz/passability-rule.md`)

- [ ] Default tileset passability preserved; no custom passability overrides without explicit documentation and work-order authorization.
- [ ] Player start tile confirmed passable.
- [ ] All required NPCs confirmed reachable.
- [ ] All required transfers confirmed reachable (not placed behind impassable tiles).
- [ ] All required events (signs, bookshelf, well, memorial, secrets) confirmed reachable.
- [ ] Required routes validated:
  - [ ] `player_start -> village_green`
  - [ ] `village_green -> rowan_cottage_door`
  - [ ] `village_green -> general_store_door`
  - [ ] `village_green -> blacksmith_door`
  - [ ] `village_green -> inn_door`
  - [ ] `village_green -> village_exit`
  - [ ] `village_exit -> ashford_vale_overworld` (confirmed reachable from the village side; full overworld-side validation belongs to the Ashford Vale Overworld package, not this checklist)
- [ ] No wall, roof, cliff, or water tile is walkable unless explicitly intended and documented.
- [ ] No required event sits on an unreachable or unintended tile.

## Player Flow

- [ ] Player can complete the opening scene and freely explore in any order.
- [ ] Player can obtain the Hidden Cave rumor from at least one of Rowan or Mabel independently of the other.
- [ ] Player can leave for Ashford Vale at any point after the opening scene, with no forced sequencing.
- [ ] No quest markers, objective arrows, or forced tutorial popups are present anywhere in the village.

## Quality Review

- [ ] Sample-map quality review passed - the village is believable as a polished RPG Maker MZ sample map adapted to this story, per `bridges/rpg-maker-mz/map-quality-standard.md`'s quality bar question.
- [ ] No empty filler space; no sloppy repeated decoration patterns (Map Quality Standard).
- [ ] Human playtest completed: movement feels natural, visual boundaries match collision boundaries, no route feels awkward or misleading (Passability Rule's Human Playtest requirement).
- [ ] Reviewed against the JRPG Design Bible and anti-patterns list (no Zelda-style screen progression, no objective markers, no forced tutorials, no fetch quests).

## Production Record

- [ ] Production graph facts recorded for `work_order.wp_03b` and its produced assets, per `studio/governance/player-visible-production-rule.md`'s `produces` convention.
- [ ] `python3 tools/atlas_graph/validate_graph.py` passes.
- [ ] `python3 tools/atlas_format/format_guard.py --check` shows no unexplained formatting churn.
- [ ] Human acceptance recorded for Ashford Village as a completed, playable beat.
