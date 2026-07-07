# Pacing Guidelines

## Purpose

This document sets target pacing for The Last Sword Protocol's opening content, expanding `jrpg-design-bible.md` Section 9. Pacing here means "how much real time should this take before the next meaningful beat," used to review whether a map, town, or dungeon draft is over-built, under-built, or correctly scaled - not a hard technical limit.

These targets apply to the First Playable Hour milestone (`projects/the-last-sword-protocol/milestones/first-playable-hour.md`) and should generalize to later regions and chapters.

## First Hour

Target: **55-65 minutes** for a first-time player following the critical path with light exploration, ending at the credits sequence.

This matches the pacing table already established in `projects/the-last-sword-protocol/roadmap/chapter-01-roadmap.md`, reproduced here as the canonical reference for design review:

| Beat | Target | Cumulative |
| --- | --- | --- |
| Opening Sequence | 3-5 min | 5 min |
| Ashford Village | 5-8 min | 13 min |
| Ashford Vale Overworld (first pass) | 5-7 min | 20 min |
| Hidden Cave | 8-10 min | 30 min |
| Sword Shrine | 2-3 min | 33 min |
| Last Sword Acquisition (return trip) | 3-5 min | 38 min |
| Glassfield Ruins | 10-12 min | 50 min |
| First Relay Activation | 3-4 min | 54 min |
| Rustshore | 3-5 min | 59 min |
| Boat Departure | <1 min | 60 min |
| End of Prototype Credits | 1-2 min | ~62 min |

**Review rule:** if a beat's actual playtest length runs more than ~50% over its target, treat that as a signal the content is over-built for its place in the hour (too many rooms, too much dialogue, too much backtracking) rather than immediately extending the target.

## First Town (Ashford Village)

Target: **5-8 minutes** for a first-time player who talks to the available NPCs once and does not shop extensively.

- Should be small enough to fully explore without a map/minimap dependency.
- Should deliver exactly one clear rumor pointing toward the Hidden Cave (per the Journey Principle - discoverable through NPC dialogue, not a marker) within the first 2-3 minutes of arrival.
- Should not require more than one loop of the town to find every NPC with something to say.

**Review rule:** if a first-time playtester needs more than 8 minutes or gets confused about where to go next, the town has too many NPCs, too much dialogue, or an unclear layout for its position at the very start of the game.

## First Dungeon (Hidden Cave, including the Sword Shrine)

Target: **10-13 minutes total** (8-10 min cave traversal + 2-3 min shrine).

- Should introduce dungeon traversal and light combat without teaching more than 2-3 new ideas at once (see Tutorial Overload in `anti-patterns.md`).
- Should include exactly one optional side room or branch, reachable within the time budget, not several.
- The Sword Shrine climax should read as a reward beat with no failure state, distinct in pacing from the traversal that precedes it - short, deliberate, and unhurried, not padded with additional combat.

**Review rule:** a first dungeon that takes a first-time player more than ~15 minutes is very likely testing patience rather than teaching mechanics.

## First Boss

The First Playable Hour milestone does not currently include a traditional boss battle - its climax (First Relay Activation) is explicitly a restoration sequence, not a fight, with only an optional single Bit Wraith guardian encounter beforehand. This is a deliberate milestone-scope decision, not an oversight, but it means "first boss" pacing cannot yet be validated against real content and is stated here as forward guidance for whichever region or chapter introduces one:

- Target: **3-6 minutes** of actual combat for a genuine first boss encounter - long enough to feel like an event, short enough that a loss doesn't feel like a large time investment lost.
- A first boss should telegraph its arrival (approach corridor, changed music, visual buildup) for at least 30-60 seconds before combat starts, so the encounter reads as a destination rather than an ambush.
- A first boss should be beatable with the level and equipment reasonably available at that point in the critical path, without requiring optional-content grinding.

**Recommendation:** when a future region or chapter roadmap introduces the game's actual first boss, this section should be revised with a real beat-by-beat pacing entry, following the same table format as the First Hour section above.

## First Region (Ashford Vale / Journey I)

Target: **55-65 minutes** critical path (same as First Hour, since the region and the milestone are currently the same scope), with an additional, uncapped amount of optional time for deferred content (Fogfen Marsh, a Watchtower outpost) that a completionist player might add on a later pass.

- A first region should establish the world's baseline difficulty, the player's core toolkit (the Last Sword and its unlock behavior), and one full "problem introduced -> problem resolved -> world opens further" arc, per `story-reset.md`'s Story Shape.
- A first region should end with an unambiguous sense of departure (Rustshore's boat departure), not an open-ended stopping point that leaves the player unsure whether more content exists nearby.

## Using These Guidelines in Review

- Treat every number in this document as a target band, not a hard requirement - a beat that runs faster because it reads cleanly is not automatically a problem; a beat that runs longer because it is genuinely richer is not automatically a problem either. The review question is always *why* a beat deviates, not whether it deviates.
- When a work package under `projects/the-last-sword-protocol/production/work-breakdown.md` builds a map, town, or dungeon, its completion definition should be checked against the relevant target here before the package is marked complete.
- Playtest data (from `WP-12 Consistency & QA Pass` in the work breakdown) should be compared against these targets and used to revise them - this document should be treated as a living standard, updated by future design work orders as real playtesting accumulates, not fixed at first-draft numbers forever.
