# Exploration Principles

## Purpose

This document expands `jrpg-design-bible.md` Sections 1, 2, 3, and 7 into concrete, checkable exploration design principles. Where the bible states the philosophy, this document states the test: how do you know a piece of world design actually achieves it?

## The Overworld Is a Gameplay System, Not a Menu

A regional overworld map must do real gameplay work, not just serve as a pretty transition between menu-selected destinations.

**Test:** can the player get lost, take a wrong turn, or choose a longer scenic route instead of the shortest path? If the overworld only ever offers one meaningful path between any two points, it is functioning as a menu with extra steps, not a gameplay system.

**Requirements:**

- The overworld has its own encounter design, distinct from interior locations.
- The overworld has terrain variety (open fields, forest, coast, hills) that reads visually, not just mechanically.
- At least one landmark is visible from a distance before it is reachable, so the player forms a mental map before the game confirms it.

## The Journey Principle in Practice

Per the bible, every meaningful trip should carry discovery, risk, resource management, and anticipation. Concretely:

- **Discovery:** place at least one small point of interest (a landmark, an optional NPC, a treasure, a piece of environmental detail) along any route the player is expected to travel more than once.
- **Risk:** encounter tables should scale with the region's stage of the story, so a trip through Ashford Vale after the Last Sword feels different (safer against wisps, still dangerous near the ruins) than before it.
- **Resource management:** a trip should be long enough, or hazardous enough, that the player occasionally thinks about HP/MP/items during travel - not only during a boss fight.
- **Anticipation:** a location the player cannot yet enter should still be visible or mentioned before it becomes accessible (Glassfield Ruins visible on the Ashford Vale overworld before the sword unlocks it, per the milestone's Beat 3).

**Test:** if you removed the travel between two locations and replaced it with a menu warp, would the player lose something they'd miss? If not, the journey isn't doing its job yet.

## Curiosity-Driven Discovery, Kept Legible

Section 7 of the bible states players should discover objectives out of curiosity, not UI instruction. This must be balanced against never leaving the player genuinely stuck with no idea what to do next. The way to hold both:

- **Rumors, not markers.** An NPC in town describes what they've seen or heard ("the old road hasn't been safe since the tremors began") rather than a quest log entry saying "Go to Old North Road."
- **Visual invitation.** A cave mouth, a broken bridge, or a sealed gate visible from the overworld invites investigation without needing a marker - the player's own curiosity does the pointing.
- **Redundant, not singular, hints.** The critical path's next step should be discoverable through at least two independent signals (an NPC rumor *and* a visible landmark *and* the natural flow of the overworld's geography) so a player who misses one dialogue line is not stuck.
- **No exclusively-optional-dialogue gates.** Nothing required for progression should be locked behind a single NPC conversation that is easy to skip. Optional dialogue enriches; it never gates.

**Test:** could a player who skips every piece of optional dialogue still find their way to the next critical-path location using only what the world itself shows them? If not, a required hint has been mistakenly placed in optional content.

## Dragon Quest Principles as Design Checks

Each Dragon Quest-inspired principle from the bible converts into a review question:

| Principle | Review Question |
| --- | --- |
| Curiosity over objective markers | Would a player without a quest marker still know roughly where to go, from world cues alone? |
| Rumors over quest logs | Does the critical information come from a character's voice, not a UI system? |
| Towns as communities | Does at least one NPC exist purely for flavor/personality, with no mechanical function? |
| Exploration rewarded naturally | Does wandering off-path find something, even if small? |
| Optional dialogue | Can NPCs be talked to more than once without breaking or repeating identically forever in a way that feels dead? |
| Gradual world expansion | Is the currently-accessible map small enough to hold in memory at this story stage? |
| Meaningful overworld traversal | Does geography (a river, a mountain, a gate) create a real choice or obstacle, not just distance? |

## Regional Scale Discipline

Per the bible's Section 4, a region's overworld should be sized to its actual content. As a working rule:

- A region built for the First Playable Hour scale (one settlement, one-to-two adventure sites, a handful of landmarks) should take roughly 2-4 minutes to cross on foot at normal pace, not 10+ minutes of empty terrain.
- Every screen-width of overworld map should contain at least one of: an encounter zone, a landmark, a branching path, or a visible destination. A stretch with none of these is padding and should be compressed.
- "Optional" content (Fogfen Marsh, a Watchtower outpost, per `world-model.md`) is allowed to exist off the critical path, but it should still follow this density rule once built - optional does not mean exempt from mattering.

## Relationship to Other Design Documents

- `pacing-guidelines.md` sets the time budget these principles operate inside.
- `anti-patterns.md` names the specific failure modes (Zelda-style screen chains, empty overworlds, objective-marker dependency) that violate these principles, with the reasoning spelled out per anti-pattern.
