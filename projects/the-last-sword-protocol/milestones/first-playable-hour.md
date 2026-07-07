# Milestone: First Playable Hour

## Purpose

This milestone defines the complete playable vertical slice AtlasStudio will coordinate first: the opening hour of The Last Sword Protocol, from the opening sequence through the boat departure and prototype credits.

This document is the source of truth for scope. The roadmap (`projects/the-last-sword-protocol/roadmap/chapter-01-roadmap.md`) sequences it. The production plan (`projects/the-last-sword-protocol/production/`) breaks it into implementation work.

## Canon Basis

This milestone is built entirely on existing canon graph facts. No canon was changed to write this document.

```text
world.elyndor CONTAINS region.ashford_vale
region.ashford_vale CONTAINS location.ashford_village
region.ashford_vale CONTAINS location.hidden_cave
location.hidden_cave CONTAINS location.sword_shrine
region.ashford_vale CONTAINS location.glassfield_ruins
location.glassfield_ruins CONTAINS infrastructure.first_relay
region.ashford_vale CONTAINS location.rustshore_dock
location.ashford_village CONNECTED_TO location.hidden_cave
location.ashford_village CONNECTED_TO location.rustshore_dock
item.last_sword UNLOCKS location.glassfield_ruins
infrastructure.first_relay UNLOCKS location.rustshore_dock
location.sword_shrine REWARDS item.last_sword
item.last_sword TEACHES concept.authentication
item.last_sword REPRESENTS concept.authentication
location.glassfield_ruins TEACHES concept.access_control
character.rowan KNOWS_ABOUT location.hidden_cave
character.rowan MISUNDERSTANDS infrastructure.first_relay
```

## Canon Gaps (Flagged, Not Resolved Here)

Two locations named in `home-region.md` are not yet canon graph nodes. This milestone treats them as required but unresolved:

- **Elara's House** - an interior needed for the opening sequence (Elara is canon: `character.elara`, but her house is not yet a `location` node).
- **Old North Road** - a route named in the Home Region structure list, not yet a `route` node, though `location.ashford_village CONNECTED_TO location.hidden_cave` already covers the functional connection.

Per the Canon Change Rule in `studio/workflow.md`, this planning work order does not create these nodes. A small canon work order should formalize them before `WP-02` in the work breakdown begins. This is called out again in the dependency map.

## Target Experience

- **Length:** 45-60 minutes of playtime for a first-time player following the critical path with light exploration.
- **Feel:** Dragon Quest-style overworld-first opening. The player should leave this hour understanding the core loop (explore → clue → dungeon → reward → unlock) and sensing the cybersecurity fantasy layer without being lectured.
- **Ending state:** Player has the Last Sword, has restored the First Relay, has departed Ashford Vale from Rustshore Dock, and has seen a short credits sequence marking the end of the vertical-slice prototype.

## Beat Sequence

Beats are listed in critical-path order. Each beat states gameplay purpose, narrative purpose, cybersecurity concepts taught, required maps, NPCs, monsters, items, music, events, implementation dependencies, and acceptance criteria.

---

### Beat 1 - Opening Sequence

**Canon anchor:** production-only sequence; takes place at `location.ashford_village` (no dedicated canon node for the opening itself).

- **Gameplay purpose:** Establish player control, camera, and basic movement in a safe space before any combat.
- **Narrative purpose:** Introduce the Hero (`character.hero`) at home, establish Elara (`character.elara`) as guardian/mentor figure, and plant the first rumor of tremors or strange lights that motivates exploration.
- **Cybersecurity concepts taught:** None yet. This beat is scene-setting only.
- **Required maps:** Elara's House interior (canon gap - see above), Ashford Village exterior (`location.ashford_village`).
- **Required NPCs:** `character.elara`; Village Elder (role placeholder, canon TBD).
- **Required monsters:** None.
- **Required items:** None (starting equipment only, non-canon-blocking stub items).
- **Required music:** Opening theme (short, warm, home-village motif); ambient village loop.
- **Required events:** Wake-up/intro cutscene; first movement tutorial prompt; rumor dialogue trigger with Elara.
- **Implementation dependencies:** Elara's House canon node; RPG Maker bridge foundation (`WO-0005`) for cutscene/event implementation.
- **Acceptance criteria:**
  - Player can move, open a menu, and exit the house within the first two minutes.
  - Elara's dialogue references the tremor/rumor hook that motivates Beat 2.
  - No combat is possible during this beat.

---

### Beat 2 - Ashford Village

**Canon anchor:** `location.ashford_village`

- **Gameplay purpose:** Teach NPC interaction, shop/inn basics, and rumor-gathering as the mechanism that points the player toward the Hidden Cave.
- **Narrative purpose:** Establish the village as home, seed the sense that something ancient lies beneath ordinary life. Rowan (`character.rowan`) delivers a partially wrong explanation of what lies in the Hidden Cave, per `character.rowan MISUNDERSTANDS infrastructure.first_relay`.
- **Cybersecurity concepts taught:** None directly; sets up authentication theme by having Rowan describe the cave's contents incorrectly (a "misunderstanding" the player will later correct - an early, wordless hint that trust and verification matter).
- **Required maps:** Ashford Village exterior (`location.ashford_village`).
- **Required NPCs:** `character.rowan` (`character.rowan KNOWS_ABOUT location.hidden_cave`), `character.elara`; 2-3 minor flavor NPCs (role placeholders, canon TBD) for shop/inn/rumor texture.
- **Required monsters:** None (village is safe).
- **Required items:** Basic starting consumable(s), non-canon-blocking.
- **Required music:** Village theme (looping, distinct from opening theme).
- **Required events:** Rowan dialogue chain pointing to Hidden Cave; optional shop/inn interactions; exit trigger to Ashford Vale Overworld.
- **Implementation dependencies:** Bridge foundation for NPC event wiring; NPC dialogue content (`WP-08`).
- **Acceptance criteria:**
  - Player receives a clear, in-fiction reason to seek the Hidden Cave from at least one NPC.
  - Village is fully walkable with no blocking geometry errors.
  - Exit to the overworld is reachable without backtracking confusion.

---

### Beat 3 - Ashford Vale Overworld

**Canon anchor:** `region.ashford_vale`

- **Gameplay purpose:** Teach overworld traversal, low-risk random encounters, and "see it before you can reach it" landmark visibility (per `studio/atlas-graph/... world-model.md` Overworld Area design).
- **Narrative purpose:** Show the player the shape of the region - visible but inaccessible Glassfield Ruins and Rustshore Dock, reinforcing that the world is bigger than the village.
- **Cybersecurity concepts taught:** None directly; establishes the "sealed/inaccessible until you have the right credential" visual language that will pay off with the sword and relay.
- **Required maps:** Ashford Vale Overworld (single connective exterior map linking Village, Hidden Cave, Glassfield Ruins, Rustshore Dock).
- **Required NPCs:** None required on this map; `character.hero` is the player avatar (`character.hero APPEARS_IN region.ashford_vale`).
- **Required monsters:** Rust Stingers (Scorpions), Gel Wisps (Slimes) - low-difficulty roaming encounters per `home-region.md` Encounter Identity.
- **Required items:** None new.
- **Required music:** Overworld theme (adventurous, open, loopable).
- **Required events:** Encounter zone triggers; landmark visibility for Glassfield Ruins and Rustshore Dock (visible, not enterable until later beats); entrance triggers to Hidden Cave.
- **Implementation dependencies:** Overworld map build (`WP-04`); monster implementation (`WP-09`).
- **Acceptance criteria:**
  - All four location entrances (Village, Hidden Cave, Glassfield Ruins, Rustshore Dock) are visible or reachable on the map per canon `CONTAINS`/`CONNECTED_TO` edges.
  - Glassfield Ruins and Rustshore Dock are visibly present but not enterable until their unlock conditions are met.
  - Encounter rate is tuned low enough not to frustrate a first-time player.

---

### Beat 4 - Hidden Cave

**Canon anchor:** `location.hidden_cave`

- **Gameplay purpose:** Teach dungeon exploration fundamentals - linear-with-branches layout, light combat, simple traversal puzzle.
- **Narrative purpose:** First descent into "ancient technology as mystery" per `game-vision.md`. The cave should feel older and stranger than the village.
- **Cybersecurity concepts taught:** Ambient only - flickering lights, sealed inner door, a sense that something inside is waiting to recognize something, without naming any concept yet.
- **Required maps:** Hidden Cave interior (multi-room, one branch optional/secret).
- **Required NPCs:** None required (empty ruin feel), optional environmental "audio log" style flavor text.
- **Required monsters:** Gel Wisps, Cave Flutterers (Bats) per `home-region.md`.
- **Required items:** Minor treasure (consumable or gold-equivalent), non-canon-blocking.
- **Required music:** Cave/dungeon theme (tense but not frightening).
- **Required events:** Sealed inner door trigger (opens automatically upon nearing, or requires a simple traversal puzzle); transition to Sword Shrine.
- **Implementation dependencies:** Cave dungeon build (`WP-05`); monster implementation (`WP-09`).
- **Acceptance criteria:**
  - Player can reach the Sword Shrine only after making meaningful traversal progress (not an instant hallway).
  - At least one optional side room rewards exploration.
  - Combat difficulty stays below village-adjacent overworld difficulty (cave should not out-pace the player's level).

---

### Beat 5 - Sword Shrine

**Canon anchor:** `location.sword_shrine` (`location.hidden_cave CONTAINS location.sword_shrine`)

- **Gameplay purpose:** Deliver the first major reward moment and the first authentication metaphor payoff.
- **Narrative purpose:** The sword recognizes the Hero. This is the game's first explicit "worthiness/recognition" beat per `game-vision.md` Cybersecurity Fantasy Layer.
- **Cybersecurity concepts taught:** Authentication (`concept.authentication`, `item.last_sword TEACHES concept.authentication`). The fantasy framing is "the sword recognizes the hero" standing in for credential verification.
- **Required maps:** Sword Shrine interior (single ceremonial chamber, nested map/room within Hidden Cave).
- **Required NPCs:** None (solitary discovery moment).
- **Required monsters:** None (shrine is a sanctuary, no combat).
- **Required items:** `item.last_sword` (obtained here; `location.sword_shrine REWARDS item.last_sword`).
- **Required music:** Discovery/authentication fanfare - distinct musical sting separate from the cave loop.
- **Required events:** Sword recognition cutscene; item grant event; equip prompt; return-path trigger back through Hidden Cave.
- **Implementation dependencies:** Cave/shrine dungeon build (`WP-05`); opening/credit-style cutscene scripting capability (`WP-11` techniques, reused here).
- **Acceptance criteria:**
  - The recognition moment is unmissable and unskippable on first playthrough.
  - `item.last_sword` is granted and equipped (or equip-prompted) before the player leaves the shrine.
  - The moment reads as a reward, not a puzzle - no failure state exists here.

---

### Beat 6 - Last Sword Acquisition (Return & Unlock)

**Canon anchor:** `item.last_sword`, `item.last_sword UNLOCKS location.glassfield_ruins`

- **Gameplay purpose:** Close the loop on the cave detour and re-open the overworld with a new capability (the sword now functions as a key).
- **Narrative purpose:** The player returns to the overworld changed - the world reacts to the sword's presence (Glassfield Ruins becomes enterable).
- **Cybersecurity concepts taught:** Access control setup - possession of the credential (sword) is what will authorize entry to the sealed ruins in the next beat.
- **Required maps:** Reuses Ashford Vale Overworld (Beat 3 map) with an updated world-state flag.
- **Required NPCs:** Optional: Rowan or Elara brief reaction dialogue if the player returns to the village first (non-blocking, optional detour).
- **Required monsters:** None new (overworld encounters continue as in Beat 3).
- **Required items:** None new.
- **Required music:** Reuses overworld theme; optional short motif sting on sword-equip world-state change.
- **Required events:** World-state flag flip that unlocks Glassfield Ruins entrance; optional NPC reaction dialogue refresh.
- **Implementation dependencies:** Overworld map world-state wiring (`WP-04`); bridge event/flag system (`WP-01`).
- **Acceptance criteria:**
  - Glassfield Ruins becomes enterable immediately after leaving the cave with the sword, with no additional fetch quest required.
  - A visible or audible signal (map change, icon, sound) tells the player the ruins are now open.

---

### Beat 7 - Glassfield Ruins

**Canon anchor:** `location.glassfield_ruins`, `location.glassfield_ruins TEACHES concept.access_control`

- **Gameplay purpose:** Second dungeon, harder than Hidden Cave, introduces "sword as key" traversal mechanic (sealed doors that respond only to the sword).
- **Narrative purpose:** First confrontation with corrupted ancient constructs - the ruins reject what does not belong, teaching access control through enemy and environment design.
- **Cybersecurity concepts taught:** Access control (`concept.access_control`). Sealed doors open only for the sword-bearer; corrupted constructs represent unauthorized/rejected entities.
- **Required maps:** Glassfield Ruins interior (larger than Hidden Cave, 2-3 sealed-door gates using the sword-key mechanic).
- **Required NPCs:** None (ruin is uninhabited by the living).
- **Required monsters:** Pebble Constructs (Tiny Golems), Bit Wraiths (Corrupted Sprites) per `home-region.md`.
- **Required items:** Minor treasure; optional lore fragment describing the ruins pre-corruption.
- **Required music:** Ruins theme - colder, more mechanical/ancient than the cave theme.
- **Required events:** Sword-activated sealed door triggers (2-3 instances); construct battle triggers; transition to First Relay chamber.
- **Implementation dependencies:** Ruins dungeon build (`WP-06`); monster implementation (`WP-09`); bridge sword-key event pattern (`WP-01`).
- **Acceptance criteria:**
  - At least two sealed doors demonstrate the sword-key mechanic before the Relay chamber.
  - Corrupted constructs are visibly distinct from Hidden Cave enemies (palette/name/behavior).
  - Difficulty is noticeably higher than Hidden Cave but not punishing for a first-time player at expected level.

---

### Beat 8 - First Relay Activation

**Canon anchor:** `infrastructure.first_relay` (`location.glassfield_ruins CONTAINS infrastructure.first_relay`), `infrastructure.first_relay UNLOCKS location.rustshore_dock`

- **Gameplay purpose:** Climax event of the ruins dungeon - a short activation sequence or puzzle, not a boss fight, that pays off the access-control theme.
- **Narrative purpose:** The Hero restores the First Relay, the first proof that the "ruins" are actually a lost network/system. This directly sets up the deeper mystery per `story-reset.md`.
- **Cybersecurity concepts taught:** Restoration/recovery (backup recovery metaphor) and trust routing - the relay "trusts" the sword's signal, restoring a broken trust relationship per `game-vision.md`.
- **Required maps:** First Relay chamber (interior room within Glassfield Ruins map).
- **Required NPCs:** None (Rowan's earlier misunderstanding, `character.rowan MISUNDERSTANDS infrastructure.first_relay`, is paid off narratively here without Rowan present - the player now knows more than Rowan did).
- **Required monsters:** Optional final Bit Wraith encounter guarding the relay (not a full boss).
- **Required items:** None new.
- **Required music:** Relay activation theme - a rising, hopeful sting distinct from combat music.
- **Required events:** Relay activation cutscene/sequence; world-state flag unlocking Rustshore Dock; optional short vision/flashback hinting at the wider Elyndor mystery.
- **Implementation dependencies:** Ruins dungeon build (`WP-06`); relay activation event scripting (`WP-11` shared techniques).
- **Acceptance criteria:**
  - Activation sequence is readable without dialogue-heavy exposition dumps (show, don't lecture, per `game-vision.md`).
  - Rustshore Dock unlock flag fires immediately on sequence completion.
  - Sequence runs without soft-lock risk (no unrecoverable state if the player saves mid-sequence, if saving is enabled here).

---

### Beat 9 - Rustshore

**Canon anchor:** `location.rustshore_dock`, `location.ashford_village CONNECTED_TO location.rustshore_dock`

- **Gameplay purpose:** Final safe hub of the hour - light NPC interaction, a sense of arrival at "the edge of the known region."
- **Narrative purpose:** Show the player the wider world is real and reachable. Confirms the region-to-region structure from `world-model.md`.
- **Cybersecurity concepts taught:** None directly; a calm beat before departure.
- **Required maps:** Rustshore Dock exterior.
- **Required NPCs:** Dockmaster (role placeholder, canon TBD) - provides brief departure dialogue and any final rumor/hook for the next region.
- **Required monsters:** None (safe hub).
- **Required items:** None new.
- **Required music:** Dock/departure theme - reflective, transitional.
- **Required events:** Dockmaster dialogue chain; boat boarding trigger.
- **Implementation dependencies:** Dock map build (`WP-07`); NPC dialogue content (`WP-08`).
- **Acceptance criteria:**
  - Dockmaster dialogue clearly signals departure is imminent and voluntary (player is not forced in mid-exploration).
  - Player can freely leave and return to the overworld before boarding, if desired.

---

### Beat 10 - Boat Departure

**Canon anchor:** production-only sequence at `location.rustshore_dock`.

- **Gameplay purpose:** Deliver a clean, satisfying transition out of the milestone's playable space.
- **Narrative purpose:** Physically and narratively close Chapter 01 / Journey I, transitioning toward Journey 2 per `home-region.md` ("Transition to Journey 2").
- **Cybersecurity concepts taught:** None; pure narrative transition.
- **Required maps:** Rustshore Dock (Beat 9 map) plus a brief boat/sea transition shot (can be a simple scripted scene, not a new full map).
- **Required NPCs:** Dockmaster (farewell line).
- **Required monsters:** None.
- **Required items:** None.
- **Required music:** Departure theme swelling into a short transitional cue.
- **Required events:** Boarding cutscene; fade/transition out of the playable region.
- **Implementation dependencies:** Dock map build (`WP-07`); opening/credits-style cutscene scripting (`WP-11`).
- **Acceptance criteria:**
  - Transition is unskippable-but-brief (under 30 seconds) so it reads as a milestone marker, not padding.
  - No playable input is expected or required during the transition beyond an optional skip-forward prompt.

---

### Beat 11 - End of Prototype Credits

**Canon anchor:** production-only sequence, milestone closer.

- **Gameplay purpose:** Clearly signal "this is the end of the current build" to playtesters, distinguishing an intentional stopping point from a bug or crash.
- **Narrative purpose:** Give the vertical slice a sense of completeness and craft, proving AtlasStudio can carry a scene from idea to finished, presentable moment.
- **Cybersecurity concepts taught:** None.
- **Required maps:** None (title/credits screen, can be a simple scripted scene).
- **Required NPCs:** None.
- **Required monsters:** None.
- **Required items:** None.
- **Required music:** Short credits theme, can reprise the opening theme's motif for emotional bookending.
- **Required events:** Credits scroll/display; return-to-title or safe stop point.
- **Implementation dependencies:** Cutscene scripting (`WP-11`); final QA pass (`WP-12`).
- **Acceptance criteria:**
  - A first-time playtester unambiguously understands the prototype has ended as intended.
  - Credits correctly attribute the milestone (AtlasStudio, contributing agents/providers, human creator) without exposing internal tooling details inappropriate for a player-facing screen.

---

## Milestone-Level Acceptance Criteria

The milestone is complete when:

1. All eleven beats are playable in sequence without a blocking bug, from opening sequence to credits, in one continuous session.
2. Every `UNLOCKS` gate in canon (`item.last_sword UNLOCKS location.glassfield_ruins`, `infrastructure.first_relay UNLOCKS location.rustshore_dock`) is enforced in the actual build - the player cannot skip ahead by exploiting map geometry.
3. All required NPCs, monsters, items, music, and events listed above exist in the build (or are represented by clearly-labeled placeholder assets if a follow-up polish pass is explicitly scheduled).
4. Studio Doctor and Canon Linter both run clean against the production and canon graph state at milestone acceptance time.
5. A human playtest of the full hour is completed and the milestone is marked accepted in the production graph.
