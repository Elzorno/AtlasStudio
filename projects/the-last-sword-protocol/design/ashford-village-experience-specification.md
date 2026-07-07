# Ashford Village Experience Specification

## Purpose Of This Document

This is the last design document before implementation. It must contain every creative decision Codex needs to implement Ashford Village in `TheLastSwordProtocol-Game`. If a detail is not here, implementation should not have to invent it - flag the gap back to design instead of guessing.

This document directly unlocks **WP-03B - Ashford Village Implementation**. Everything below exists to make that package buildable; anything that would not help implement the village has been left out.

## Canon Alignment Note

Canon (`projects/the-last-sword-protocol/graph/nodes/canon.nodes.json`) establishes: `character.elara` as "Hero's guardian and emotional anchor" and `character.rowan` as "Village elder and local historian who understands legends but misunderstands the ancient technology." Neither has a canon house node yet - `projects/the-last-sword-protocol/milestones/first-playable-hour.md` previously flagged this as an open canon gap.

`projects/the-last-sword-protocol/design/player-experience-map.md` names the opening home location "Rowan's Cottage." This specification resolves the gap without requesting new canon: **Rowan's Cottage is a shared household** - Rowan (elder, historian, and head of the household) and Elara (the hero's day-to-day guardian) both live there. This satisfies Elara's canon role (guardian, present at home, still "appears in" Ashford Village) and matches the existing player-experience-map naming exactly, and it means no new canon location node is required - the gap closes by household composition, not by adding a second house. If a future work order wants Elara and Rowan to have separate homes, that is a canon decision, not an implementation detail, and should be requested explicitly rather than assumed.

## 1. Village Purpose

**Gameplay purpose:** Ashford Village is the player's first interactive space - it teaches movement, NPC interaction, shop use, and rumor-gathering before any combat exists. It is also the anchor the player returns to and measures change against (its state visibly shifts after the sword is obtained, per Beat 6 of the milestone).

**Narrative purpose:** it establishes that the Hero comes from an ordinary place, among ordinary people, and that something old and unexplained (tremors, strange lights, half-understood ruins) sits just beneath that ordinary life - exactly the "growing sense that the fantasy world is built on forgotten technology" from `game-vision.md`.

**Emotional purpose:** the player should feel **comfort** (a real home, people who know them), **belonging** (a community with its own routines and concerns, not a stage set for the player's arrival), and **curiosity** (enough half-answers and rumors that leaving feels like the player's own idea).

This matches `projects/the-last-sword-protocol/design/player-experience-map.md`'s Ashford Village row exactly: intended emotion "Belonging," player question "Who lives here?", playable expression "NPCs, shops, well, children, animals, village green."

## 2. Village Layout

No map is drawn here. Spatial relationships only - Codex has full discretion over exact tile placement as long as these relationships hold.

The village is small enough to fully explore on foot in the pacing target from `projects/the-last-sword-protocol/design/pacing-guidelines.md` (5-8 minutes for a first-time player who talks to everyone once). It reads as one walkable exterior space with four enterable interiors and one central outdoor gathering point, not a grid of disconnected screens.

**Spatial arrangement:** Rowan's Cottage sits at the village's edge closest to the player's eventual exit toward the overworld/Hidden Cave, so the opening sequence flows naturally outward without backtracking across the whole village. The Village Green with its well sits at the physical center, visible from most of the village, functioning as the social hub everything else arranges around. The General Store and Blacksmith sit near each other along the main path between the Green and the village entrance, reflecting a natural "commerce cluster." The Inn sits nearer the village's exit toward Hidden Cave/the overworld, consistent with an inn's role as a waypoint for travelers passing through toward the wider region. Exactly one clear path leads out of the village toward the Ashford Vale overworld; there is no second, redundant exit for this specification's scope.

### Rowan's Cottage (Home)

- **Purpose:** the Hero's home; opening-sequence interior; comfort anchor; site of the Rowan Bookshelf secret (Section 7).
- **Owner:** Rowan (household head), shared with Elara.
- **Gameplay interactions:** wake-up/start point, fireplace interaction, bookshelf interaction (secret), brief morning dialogue with Elara and/or Rowan before the player is free to explore.
- **Future story use:** the Beat 10 "Walk Home" / "Night Sequence" / "Morning After" moments from `player-experience-map.md` return here after the Hidden Cave, so its interior must support a distinct night/after-sword dialogue and ambience state (see Section 4, `dialogue.ashford_after_sword`).

### General Store

- **Purpose:** first supplies (consumables); a natural rumor-gathering stop since everyone passes through a shop.
- **Owner:** Mabel, the General Store Owner (production-only name; not yet canon - see Section 3).
- **Gameplay interactions:** shop menu (basic consumables only - no equipment); optional dialogue distinct from the shop transaction itself.
- **Future story use:** stock and dialogue should be revisitable with a small after-sword variant (Mabel reacting to village mood change), reusing `dialogue.ashford_after_sword`.

### Blacksmith

- **Purpose:** first equipment (basic weapon/armor); thematic echo of "a legendary blade" before the player has found one.
- **Owner:** Garrick, the Blacksmith (production-only name; not yet canon).
- **Gameplay interactions:** shop menu (basic weapon/armor); optional dialogue about metalwork, old blades, or half-remembered legends - never a direct spoiler of the Last Sword's nature.
- **Future story use:** Garrick is a natural NPC to react visibly once the player returns bearing the actual Last Sword (after-sword dialogue variant), reinforcing the "sword as recognized artifact" theme without new content beyond a dialogue swap.

### Inn

- **Purpose:** rest/save point; the village's window onto the wider world, since travelers passing through are a natural source of rumors about places the player hasn't seen yet (Rustshore, the sea, other regions).
- **Owner:** Tomas, the Innkeeper (production-only name; not yet canon).
- **Gameplay interactions:** rest/save interaction; optional dialogue with Tomas and, if included, a passing traveler (see Section 3, Background Villagers).
- **Future story use:** the Inn is the natural place to seed a rumor about Rustshore Dock well before Beat 9, satisfying the Journey Principle's "anticipation" requirement across the whole hour, not just within the village.

### Village Green (outdoor, not a building)

- **Purpose:** the social and spatial center of the village; where children, animals, and casual villager life are visible without needing an interior.
- **Owner:** communal (no single NPC owner).
- **Gameplay interactions:** well interaction (Section 6), village memorial interaction (Section 6), background villager placements (Section 3).
- **Future story use:** the well's "funny echo" detail (Section 8) is a low-key hidden-systems hint that can be revisited or paid off in later regions without any changes needed here.

## 3. NPC Roster

### Major NPCs

**Rowan** - Village Elder and Local Historian (`character.rowan`)

- **Personality:** warm but distractible; talks about the past more easily than the present; genuinely learned about local legend, genuinely wrong about what the old ruins actually are.
- **Normal daily activity:** at home (Rowan's Cottage) in the morning; found at the Village Green later in the day, favoring a bench near the well where he can "keep an eye on things."
- **Gameplay function:** delivers the rumor that points toward the Hidden Cave (per canon: `character.rowan KNOWS_ABOUT location.hidden_cave`); houses the Bookshelf secret; his morning and after-sword dialogue anchor the home beat and the return beat.
- **Future relevance:** his canon misunderstanding of the First Relay (`character.rowan MISUNDERSTANDS infrastructure.first_relay`) means his dialogue must plant a wrong-but-plausible explanation now, so the player can recognize later that Rowan didn't have the full picture - do not have him say anything that would need to be retconned once Beat 8 restores the relay.

**Elara** - Guardian and Emotional Anchor (`character.elara`)

- **Personality:** practical, warm, quietly worried; the one who actually manages the household day-to-day while Rowan tells stories.
- **Normal daily activity:** at home (Rowan's Cottage) in the morning; tending a small garden or window box near the cottage during the day (ties to the Hidden Herb secret, Section 7).
- **Gameplay function:** delivers the opening "comfort" beat; grants the player's initial sense of permission to go explore (per the Journey Principle, this should read as trust extended, not a quest assignment - see Section 8, "Trust"); reacts with visible concern in the Walk Home / Night Sequence beats per `player-experience-map.md`.
- **Future relevance:** her reaction after the Hidden Cave (concern, noticing the player "looks pale") is a required emotional beat referenced in `player-experience-map.md`'s "Walk Home" row - her after-sword dialogue must include this.

**Garrick** - Blacksmith (production-only NPC; not yet canon)

- **Personality:** gruff but not unkind; proud of his craft; a little wistful about not having made anything "worth remembering."
- **Normal daily activity:** at the forge inside the Blacksmith building throughout the day.
- **Gameplay function:** basic equipment shop; optional dialogue foreshadowing "legendary blades" without naming the Last Sword directly.
- **Future relevance:** natural candidate for a visible reaction when the player returns bearing the Last Sword (after-sword dialogue).

**Mabel** - General Store Owner (production-only NPC; not yet canon)

- **Personality:** talkative, observant, the village's natural rumor clearinghouse - she hears everything because everyone passes through her shop.
- **Normal daily activity:** behind the counter of the General Store during shop hours.
- **Gameplay function:** basic consumables shop; a second, independent source for the Hidden Cave rumor and general village texture, satisfying the "redundant hints" rule from `exploration-principles.md`.
- **Future relevance:** minor after-sword dialogue variant reflecting village mood change.

**Tomas** - Innkeeper (production-only NPC; not yet canon)

- **Personality:** easygoing, well-traveled by local standards, enjoys talking to whoever passes through.
- **Normal daily activity:** behind the inn counter.
- **Gameplay function:** rest/save point; seeds the Rustshore/wider-world rumor well ahead of Beat 9.
- **Future relevance:** natural NPC to eventually mention departures/ships once Rustshore becomes relevant (no dialogue changes required for this package beyond the initial seed).

### Background Villagers (collective roster, not individually named)

- **Village Children (2-3):** playing near the Village Green/well; purely atmospheric, at most one line of overheard dialogue about the well's echo or a game they're playing.
- **Elderly Villager:** seated near the Green; shares a half-remembered superstition about "the ridge" or "the old road," reinforcing curiosity without repeating Rowan's information verbatim.
- **Farmer/Field Worker:** found near the village edge; mentions weather, crops, or the assumption that "the roads have always been safe" (see Section 8, "Assumptions").
- **Optional Wandering Peddler:** if included, appears near the Inn; a light, inessential source of an out-of-region rumor, reinforcing that the world is larger than Ashford Vale.

Background villagers do not require unique names, portraits, or dialogue trees beyond one or two lines each; they exist to make the village feel populated, per the bible's "towns as communities" principle, not to carry plot weight.

## 4. Dialogue Goals

No line-by-line dialogue is scripted here. Each entry states what the NPC should communicate; Codex/GPT dialogue authoring fills in the actual lines against these goals.

- **Rowan:** local history and legend (in general terms - old stories about the region, not exposition about "ancient technology"); the specific rumor that something is in the Hidden Cave worth investigating; a wrong-but-plausible guess about what the "old ruins" or tremors mean (his canon misunderstanding); warmth toward the Hero as family.
- **Elara:** everyday household warmth and routine; quiet worry about the tremors/strange lights without naming a specific danger; explicit, spoken trust that the Hero can go explore the overworld - this is the moment that grants the player permission to leave, and it must read as trust, not an objective assignment.
- **Garrick:** pride in craftsmanship; an offhand, non-spoiling reference to old legends of a "last" or "true" blade; practical shop-keeper efficiency.
- **Mabel:** general village gossip (independent confirmation of the Hidden Cave rumor, phrased differently than Rowan's); light personality texture; no new plot information Rowan didn't already establish.
- **Tomas:** travel talk; a first, subtle mention of Rustshore or "the coast" as a place people go; innkeeper hospitality.
- **Background villagers:** local color only - weather, routines, small superstitions - each contributing one small piece of the village's texture rather than plot information.

**Cybersecurity metaphor opportunities in dialogue** (see Section 8 for full concept mapping): Rowan's "old stories" should carry a "history/hidden systems" undertone; Elara's trust-granting line is the "trust" concept in its purest form; the Farmer's "the roads have always been safe" line is the "assumptions" concept; none of this should ever be stated as a concept - only as ordinary village speech that happens to carry the metaphor.

**Dialogue should encourage curiosity rather than issue objectives.** No NPC line should read as a command ("Go to the cave"); every line should read as a person sharing what they know or feel, leaving the decision to explore with the player.

## 5. Player Flow

```text
Home (Rowan's Cottage)
  ↓  wake, brief morning scene, Elara's trust-granting line
Village (exterior)
  ↓  free exploration - any order, any subset of NPCs/buildings
Exploration
  ↓  shops, Village Green, background villagers, secrets (optional)
Rumors
  ↓  Rowan and/or Mabel independently point toward the Hidden Cave
Leave Town
  ↓  player exits toward the Ashford Vale overworld entirely by choice
```

No quest markers, journal entries, or forced sequencing are required at any step after the opening scene. The player may visit buildings in any order, skip any optional NPC, and still receive the Hidden Cave rumor from at least one of two independent sources (Rowan, Mabel) before leaving, satisfying the redundant-hints rule from `exploration-principles.md`.

## 6. Interactable Objects

Every interaction below either rewards curiosity, reinforces a character, or teaches the world - none exist purely as filler.

- **Fireplace (Rowan's Cottage):** rewards curiosity with a small, warm flavor line; reinforces the home's comfort.
- **Bookshelf (Rowan's Cottage):** reinforces Rowan's historian character; also the access point for the Rowan Bookshelf secret (Section 7).
- **Well (Village Green):** teaches the world - a normal object with one small "off" detail (an echo that sounds wrong), a low-key hidden-systems hint.
- **Village Memorial (Village Green):** teaches the world - a small stone or marker referencing a past event tied to the region's history, reinforcing the "history" cybersecurity concept and foreshadowing that the ruins have a real, forgotten past.
- **Shop Signs (General Store, Blacksmith, Inn):** reinforce character/world texture (each sign's wording or condition can hint at the shopkeeper's personality or the village's age) at zero implementation cost beyond a signpost object.
- **Barrels/Crates (near General Store and Blacksmith):** reward curiosity with small, optional flavor text or the hidden coin (Section 7).
- **Flowers/Garden (near Rowan's Cottage, tended by Elara):** reinforce Elara's character; access point for the Hidden Herb secret (Section 7).

## 7. Secrets

All secrets are optional. None are required to progress, per the bible's "no mandatory secrets" rule.

- **Hidden Herb:** found in Elara's garden/flowerbed near the cottage; a small material reward that rewards curiosity with zero narrative weight.
- **Rowan's Bookshelf Interaction:** examining the bookshelf a second time (or after an initial dialogue) surfaces a hidden journal page - a fragment of local history referencing the "old ruins" in a way that reads as a genuine historical record, tying into the "history" and "hidden systems" concepts (Section 8) without explaining anything the player couldn't have half-guessed already.
- **Optional Viewpoint:** a spot at the village's edge (near the Blacksmith or the exit path) where the player can look out over the coming overworld terrain before ever leaving - a landmark or two (per `exploration-principles.md`'s "visual invitation" rule) becomes visible from here, rewarding a curious player with early anticipation.
- **Hidden Coin (Barrel):** a small, no-strings-attached reward tucked in a barrel or crate near the shops - pure "curiosity pays off" texture, no lore attached.

## 8. Cybersecurity Concepts

These emerge through ordinary village life and dialogue - never through direct exposition. No NPC explains a concept; the concept is only visible in hindsight.

- **Trust:** Elara's spoken permission for the Hero to go explore is an act of trust extended without a checklist - the game's first, gentlest instance of the trust relationship that the sword and the relay will later formalize.
- **Identity:** Rowan and Elara's easy, unquestioning recognition of the Hero as family/one-of-us is the emotional precursor to the sword's later, literal act of recognition/authentication.
- **Verification:** the state of the shop signs, the road, or a passing comment ("no one's checked that old bridge in years") plants the idea that things are assumed safe rather than confirmed safe.
- **Assumptions:** the Farmer's belief that "the roads have always been safe" is an explicit, ordinary instance of an unverified assumption - exactly the failure mode the game will later show has consequences.
- **History:** Rowan's role, the Village Memorial, and the Bookshelf secret all carry the idea that the past is recorded, partial, and worth recovering - the seed of the "restoring lost archives" metaphor.
- **Hidden systems:** the well's echo and the general sense (per `game-vision.md`) that ordinary village life sits atop something older is planted here lightly, to be paid off structurally once the Hidden Cave and Glassfield Ruins reveal what that "something" is.

## 9. Acceptance Criteria

Ashford Village is complete when:

- All four buildings (Rowan's Cottage, General Store, Blacksmith, Inn) and the Village Green are implemented and enterable/traversable as described in Section 2.
- All NPCs in Section 3 - Rowan, Elara, Garrick, Mabel, Tomas, and the background villager roster - are placed and reachable in their described locations.
- All interactions listed in Section 6 are implemented and functional.
- The exploration loop is playable start to finish: the player can wake at Rowan's Cottage, freely explore the village in any order, gather the Hidden Cave rumor from at least one independent source, and leave for Ashford Vale without any forced sequencing beyond the opening scene.
- Dialogue is complete for the goals in Section 4 for both the initial (`dialogue.ashford_day`) and after-sword (`dialogue.ashford_after_sword`) states.
- The player can freely leave for Ashford Vale at any point after the opening scene, with no blocking condition beyond having completed that scene.
- No quest markers, forced tutorial popups, or objective-arrow UI are present anywhere in the village.

## 10. Produces

```yaml
produces:
  - map.ashford_village
  - map.rowan_cottage
  - map.general_store
  - map.blacksmith
  - map.inn
  - npc.rowan
  - npc.elara
  - npc.garrick
  - npc.mabel
  - npc.tomas
  - npc.villagers
  - interaction.village_well
  - interaction.village_memorial
  - interaction.rowan_bookshelf
  - interaction.rowan_fireplace
  - interaction.shop_signs
  - secret.hidden_herb
  - secret.rowan_journal_page
  - secret.overlook_viewpoint
  - secret.hidden_coin_barrel
  - dialogue.ashford_day
  - dialogue.ashford_after_sword
```

This list is the implementation contract for **WP-03B**. Every entry above should exist, and be traceable to this specification, by the time WP-03B is marked complete.

## Design Constraints Compliance

This specification follows `projects/the-last-sword-protocol/design/jrpg-design-bible.md` and its companions throughout:

- **No Zelda-style screen progression:** the village is one continuous walkable space with enterable interiors, not a chain of disconnected screens (Section 2).
- **No puzzle-first gameplay:** every interaction (Section 6) is a simple examine/talk/shop action, never a puzzle mechanic.
- **No objective markers:** the rumor system (Sections 4-5) is the only progression signal, delivered redundantly through two independent NPCs.
- **No excessive tutorials:** no tutorial popups are specified; movement and interaction are taught by the environment itself (fireplace, bookshelf, shop signs inviting simple examine/talk actions).
- **No artificial fetch quests:** no NPC requests an item or errand anywhere in this specification.

Players leave Ashford Village because Rowan and Mabel have made them curious about the Hidden Cave, and because the exit path is visibly there to be taken - never because the game forces or instructs them to.
