# The Last Sword Protocol - JRPG Design Bible

## Purpose

This document defines how The Last Sword Protocol should **feel** to play. It is not story canon (`game-vision.md`, `story-reset.md`, `world-model.md`, `home-region.md`) and it is not implementation guidance (`bridges/rpg-maker-mz/`). It is the design standard AtlasStudio uses to review maps, towns, dungeons, quests, encounters, and pacing before accepting them.

Three companion documents go deeper on specific dimensions:

- `exploration-principles.md` - what makes traversal and discovery feel right.
- `pacing-guidelines.md` - target timing for the opening hour and beyond.
- `anti-patterns.md` - what to explicitly avoid, and why each one would break the feel this document defines.

Any work order that builds or reviews world content should be checked against this bible the same way a graph change is checked against the Validator - it is a quality gate, not inspirational reading.

## 1. Exploration First

The world is explored through regional overworld maps. Towns, caves, shrines, castles, ruins, forests, towers, and dungeons are entered *from* the overworld - the overworld is not a menu that teleports the player between disconnected content, it is where the game actually happens most of the time.

This matches `world-model.md`'s design rule directly: "The overworld is the connective tissue of the game... the world should not be modeled as a linear chain of screens." This bible exists to keep that rule in force at the moment-to-moment gameplay level, not just the document-structure level.

**What this means in practice:**

- Every settlement, adventure site, and landmark has a physical position on a regional overworld map that the player walks, rides, or sails across to reach.
- The overworld carries real gameplay content of its own - encounters, secrets, terrain variety, visible-but-locked landmarks - not just travel time.
- A player should be able to point at the overworld map and say where everything is relative to everything else.

## 2. The Journey Principle

Players should remember traveling *to* places as much as the places themselves. A great JRPG is not a series of great rooms connected by loading screens; it is a great world where the trip between two points is itself worth remembering.

Travel should involve:

- **Discovery** - something new is visible or reachable partway through the trip (a landmark, a side path, a hint of a location not yet accessible).
- **Risk** - encounters or hazards that make the player treat travel as a real activity, not a formality.
- **Resource management** - HP, MP, items, and light/darkness or terrain conditions should matter enough that a long trip is a real decision, not a free action.
- **Anticipation** - the player should be able to see or hear about a destination before they can enter it (a distant silhouette, an NPC's warning, a locked gate visible from the road), so arrival is a payoff, not a surprise.

If a trip between two points can be skipped entirely without losing anything the player would miss, the trip has failed the Journey Principle.

## 3. Dragon Quest Philosophy

Dragon Quest is the primary exploration inspiration - not because of its specific mechanics (turn order, menu structure, random encounter formulas), but because of the *principles* underneath those mechanics that make its worlds feel worth exploring. AtlasStudio should borrow the principles and reinterpret the mechanics freely.

Principles to carry forward:

- **Curiosity over objective markers.** The player explores because they want to know what's over there, not because a marker told them to walk there.
- **Rumors over quest logs.** NPCs mention things in conversation - a strange light, a monster sighting, a sealed door - and the player carries that information in their head, not in a checklist UI.
- **Towns as communities.** A town is a small society with its own concerns, not a vending machine with an inn attached.
- **Exploration rewarded naturally.** Wandering off the critical path finds a chest, an NPC, or a piece of world texture - never a mandatory unlock the player is punished for missing.
- **Optional dialogue.** NPCs can be talked to more than once and say something worth hearing, but nothing essential to progression is ever hidden exclusively behind optional dialogue.
- **Gradual world expansion.** The map starts small and legible, then opens outward - the player is never dropped into an overwhelming open world in the first hour.
- **Meaningful overworld traversal.** Distance and geography are real - a bridge, a mountain pass, or a boat matters, rather than every location being one menu-tap away.

## 4. Regional World Design

A **region** (per `world-model.md`'s hierarchy: World -> Region -> Overworld Area / Settlement / Adventure Site / Route / Landmark) is the primary unit of world design. Each region should contain:

- **One primary settlement** - the region's social anchor, where the player returns for rest, rumors, and shops.
- **Secondary landmarks** - memorable overworld points (a broken tower, an old relay stone, a strange glowing tree per `world-model.md`) that aid orientation and storytelling without necessarily being enterable.
- **Optional discoveries** - side content (a hidden grove, a minor NPC, an optional treasure) that rewards a player who wanders off the critical path.
- **One or more adventure sites** - the dangerous, mysterious locations that deliver the region's combat, puzzle, and story climax.
- **One regional identity** - a distinct terrain, tone, and cybersecurity metaphor that makes the region feel different from its neighbors (Ashford Vale teaches authentication and access control; a later region should teach something else).

**Avoid giant empty overworlds.** A region's overworld map should be sized to what it actually contains - empty distance is not exploration, it's padding. If a map has long stretches with nothing to see, do, or notice, it is oversized for its content.

**Avoid Zelda-style connected screen progression.** Locations are not a chain of discrete rooms entered and exited in a fixed sequence with no larger geography connecting them. The region is one continuous, legible space the player can navigate with their own sense of direction, not a series of screens stitched together by transition triggers.

## 5. Town Design

Towns should feel lived in, not staged for the player's arrival.

- **NPCs should have routines.** Where feasible, NPCs occupy believable positions and behaviors (a smith at the forge, a child playing near the well) rather than standing in place purely to deliver one line of dialogue to the player.
- **Dialogue should teach through observation rather than exposition.** An NPC comment that reveals character or world state ("The well's been dry since the tremors started") does more work than a line that explains a game mechanic directly.
- **Shops should support the world, not just sell items.** A shopkeeper's stock and manner should reflect the town's identity and current state - a coastal dock town sells different things and talks differently than a mountain outpost.

A town passes this bar when a player who talks to everyone once comes away with a sense of the town's personality and current worries, not just a shopping list.

## 6. Dungeon Design

Dungeons should feel like destinations - places the player was traveling toward, not just combat gauntlets that happen to exist. Every dungeon should have:

- **Narrative purpose** - it exists because of something the story needs (a relic to recover, a threat to confront, a mystery to explain).
- **Gameplay purpose** - it teaches or exercises a specific mechanic or difficulty step the player hasn't faced yet.
- **Environmental storytelling** - the dungeon's own geography and decay tell part of the story without a line of dialogue (Glassfield Ruins should look like a corrupted, ancient system even before anyone explains what it is).
- **Optional rewards** - at least one meaningful reward reachable only by deviating from the critical path through the dungeon.
- **Memorable identity** - a distinct visual, musical, and enemy-roster identity that keeps it from blurring into the dungeon before or after it.

## 7. Discovery

Players should discover objectives because they are curious, not because the UI instructed them. A rumor, a visible landmark, or an NPC's half-answer should be enough to make the player want to go find out for themselves. If a location's discoverability depends entirely on a quest marker or an explicit "go here next" instruction, the design has substituted UI direction for actual curiosity, and the moment stops being memorable.

This does not mean the player should ever be genuinely lost with no way forward - see `exploration-principles.md` for how to keep curiosity-driven design legible rather than confusing.

## 8. Cybersecurity Integration

Security concepts should emerge naturally through exploration and story, exactly as `game-vision.md`'s Cybersecurity Fantasy Layer intends: authentication becomes the sword recognizing its bearer, access control becomes sealed doors and corrupted constructs, backup recovery becomes restoring a lost archive. The player should encounter these ideas by *doing* them in the fiction - fighting a rejected construct, watching a sealed door respond to the sword - not by being told about them.

**Avoid classroom-style exposition.** No NPC should explain a real-world security concept directly ("this represents two-factor authentication"). If a design draft needs a character to explain what something "really" means, the metaphor has failed and needs to be re-expressed environmentally or through implication instead.

## 9. Pacing

See `pacing-guidelines.md` for full detail. In summary, this bible sets pacing targets for the first hour, first town, first dungeon, first boss, and first region, because pacing is a first-class design concern, not an afterthought tuned in playtesting alone.

## 10. Anti-Patterns

See `anti-patterns.md` for the full list and rationale. This bible names them here because a design standard that only states what to do, without naming what to avoid, is too easy to violate by accident: Zelda-style screen progression, objective-marker-driven design, tutorial overload, excessive fast travel, empty overworld maps, filler content, arbitrary fetch quests, and plugin-first solutions.

## How This Bible Is Used

- **Design review:** any new region, town, or dungeon design should be checked against Sections 4-7 before it is accepted as canon or handed to implementation.
- **Production review:** work packages in `projects/the-last-sword-protocol/production/work-breakdown.md` that build maps, towns, or dungeons should cite the relevant section of this bible in their completion definition.
- **QA:** `anti-patterns.md` names concrete, checkable violations; some of these are candidates for deterministic Canon Linter rules (see that document's Future Integration section).

This bible does not replace human judgment. It exists so that judgment has a shared reference point across every agent and every session.
