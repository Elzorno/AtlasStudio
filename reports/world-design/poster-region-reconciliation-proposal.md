# Poster Region Reconciliation - Proposal

Status: **proposal, not canon.** Nothing in this document is authorized for use in `TheLastSwordProtocol-Atlas` until a human (ideally routed through `agent.gpt` per `studio/agent-roles.md`'s region-planning role) reviews and accepts it. AtlasStudio does not invent Atlas canon; this document points at a decision Atlas needs to make, it does not make that decision.

## Why This Exists

`AtlasStudio/references/a_detailed_illustrated_game_design_map_poster_wo.png` was rejected as a reference for Map027 (Home Island Overworld) with the finding "not even close to representing the reference map." Investigating why surfaced a deeper issue than tile art: the poster depicts a full continent of 16 named regions, and none of them exist anywhere in Atlas canon - `AtlasStudio/references/README.md` and `IMP-HOM-024` both explicitly scope the poster as style/composition reference only, "not direct RPG Maker map data," introducing "no new locations, characters, story beats, or progression rules."

The human's direction: reconcile the poster's 16 regions against the world that **does** already exist in canon - Journey II (Coalmouth, Athenaeum, Irongate, Driftlands, New Meridian), Journey III (Dead Circuit), and Journey IV (The Vault) - rather than either building the poster literally or discarding it.

## A Structural Mismatch, Named Up Front

The poster is a single open continent the player roams freely between named biome regions. The actual planned world (per `World_and_Location_Bible.md`, `Story_Structure_Bible.md`, `Story_Bible.md`) is a **sequence of discrete, self-contained journey locations** - a mining town, then a library-city, then a fortress, then a caravan camp, then a city, then a tech-graveyard, then a hardened vault - each visited in turn, not a continuous explorable landmass. Home Island (Journey I) is itself already this shape: a compact hub, not a sprawling continent.

This means most of the poster's 16 regions will not find a clean home in the existing structure, and forcing all 16 into it would be inventing geography the existing story doesn't call for. The honest approach is a partial mapping: strong matches stated with evidence, weak or absent matches stated as such, not papered over.

## Proposed Strong Matches (3 of 7)

| Existing region | Poster region | Evidence |
|---|---|---|
| **Coalmouth** (Journey II-A) - "cliffs, rails, lamps, old tunnels," mining/industrial, `Regions/Coalmouth/index.md` | **Silverhollow Mines** (Lv 15-20, dungeon/mine icon, north-central) | Both are explicitly mining locations. Coalmouth has no stated level range anywhere in canon (only an Archive Recovery target of 10-12%); Silverhollow's Lv 15-20 is a plausible, unforced fit for "first mainland region." |
| **Irongate** (Journey II-C) - "fortified military settlement... buried bunker," `World_and_Location_Bible.md` lines 203-221 | **The Forgotten Bastion** (Lv 25-30, locked behind "Bastion Key Protocol") | The poster's own name is a fortress word. Both are gated/locked military-coded sites you must earn access to, not open on arrival. |
| **Dead Circuit** (Journey III/IV, see numbering note below) - "ruined server and infrastructure graveyard... beauty gives way to silence and scale" | **The Shrouded Waste** (Lv 45-50, endgame, "Keeper Shrine" ancient facility) | Both are the late-game wasteland immediately preceding the true final area, both explicitly host decayed ancient-tech infrastructure. |

## Regions With No Good Match (4 of 7)

Stated honestly rather than forced:

- **Athenaeum** - a library-city built into a collapsed university/archive complex. None of the poster's 16 names evoke a library, archive, or scholarly site. No proposed match.
- **Driftlands** - deliberately mobile, a nomadic caravan camp that relocates "around ancient trade routes." A poster is a fixed-geography format; a region whose defining trait is *not having a fixed location* cannot map onto a named point on it. No proposed match, and possibly none should be forced - Driftlands may simply not be the kind of thing this style of poster can depict.
- **New Meridian** - "the largest surviving city... near-functioning steam-powered civilization." No poster region is described as a major city; the closest by settlement-type (Bridgegate, Eastwatch, Northport) are all explicitly smaller (village/port). No proposed match.
- **The Vault** - the final hardened, underground data-center cathedral. Frosthold Peaks and The Glimmering Isles were considered (both isolated, locked-adjacent, high-level) but the fit is structural-position-only, not thematic - The Vault is explicitly underground/artificial, not a mountain or island. No proposed match.

## Unplaced Poster Regions (13 of 16)

After the 3 matches above, these poster names are not used: Northport, Westerwald Forest, Frosthold Peaks, Stoneveil Pass, Eastwatch, Sundered Plains, Bridgegate, Veridian Plains, Seacrest Ruins, Dustfall Desert, The Echoing Swamp, Southshore, The Glimmering Isles.

Three options for these, not mutually exclusive, all requiring a human/creative decision:

1. **Discard them.** They were concept-art texture for a continent this game doesn't build; nothing requires reusing every name.
2. **Demote them to minor waypoints**, not full journey regions - unnamed-on-the-poster travel texture between the 7 real regions (a forest you pass through en route to Coalmouth, a plains crossing before Irongate) without becoming their own story locations.
3. **Bank them for a future journey** beyond Journey IV, if the story ever needs one - Atlas's own call, not AtlasStudio's to schedule.

## A Pre-Existing Canon Bug, Found Along the Way

`World_and_Location_Bible.md` (lines 76-86) labels Dead Circuit "Journey III" and The Vault "Journey IV." `Story_Structure_Bible.md` and `Story_Bible.md` use a five-journey scheme where they fall under Journey III/IV ("The Architects" / "The Broken Trust") and Journey V ("The Last Protocol") respectively. These two canon documents disagree with each other right now, independent of anything in this proposal. Worth its own fix regardless of how the poster reconciliation goes.

## The Poster's "Ancient Network" Lore Should Not Become a Parallel System

The poster's Data Spires / Archive Nodes / Security Vaults / Core Reactors / five Keeper Shrines have no existing precedent under those names, but they re-describe mechanics the project already has:

| Poster term | Existing equivalent |
|---|---|
| Data Spires (fast travel) | Relay Nodes |
| Archive Nodes (lore) | Archive / Archive Recovery |
| Security Vaults (challenges) | Shrines / Memory Shrines, or the Chain of Trust / Authorization mechanic |
| Core Reactors (story-critical) | Relay Nodes themselves (Node Six, Node Seven, ...), or the NEMESIS Core / Vault |
| Five Keeper Shrines (Integrity/Clarity/Vigilance/Resilience/Truth) | `Cybersecurity_Layer_Bible.md`'s existing World Rules (Identity, Authentication, Authorization, Integrity, Availability, Zero Trust, Chain of Trust, Revocation) - "Integrity" and "Trust" are already load-bearing canonical terms |

`Cybersecurity_Layer_Bible.md` states no supernatural exception may be introduced without a Design Decision Record. Recommendation: if any of this reconciliation proceeds, route the poster's flavor text through the existing Relay/Archive/Shrine vocabulary rather than adopt "Keepers" and "Ancient Network" as new, parallel terms.

## What This Means For Map027

Building follows this doesn't happen. Map027 (Home Island Overworld) depicts Journey I only - none of Coalmouth, Athenaeum, Irongate, or the rest are reachable from it in current canon, and this reconciliation doesn't change that. Nothing here should be read as "regenerate Map027 with these new regions" - Home Island's own geography and scope (per `IMP-HOM-024`) is unaffected by whether or how the mainland journeys get reconciled with the poster.

## Recommended Next Steps

1. A human (or `agent.gpt`, per its region-planning role) reviews the 3 proposed matches, the 4 no-match findings, and decides what to do with the 13 unplaced names.
2. If any match is accepted, it becomes real Atlas canon through Atlas's own process (a Decision Record at minimum, given it assigns geography/level range to already-existing regions) - not written directly by AtlasStudio.
3. The Journey III/IV vs III/IV/V numbering inconsistency gets its own fix, independent of this proposal.
4. Map027 stays exactly as scoped (Home Island / Journey I) regardless of this proposal's outcome - it was never blocked on this reconciliation, and the "not even close" rejection is really about the tile-art gaps named in the prior turn (black-void mountains, no labels/icons, repetitive forest), not about scope.

## References

- `AtlasStudio/references/README.md`, `references/a_detailed_illustrated_game_design_map_poster_wo.png`
- `TheLastSwordProtocol-Atlas/atlas/docs/09_Technical/Implementation_Packets/Home_Island/IMP_HOM_024_Overworld_Canon_Reset.md`
- `TheLastSwordProtocol-Atlas/atlas/docs/02_World/World_and_Location_Bible.md`
- `TheLastSwordProtocol-Atlas/atlas/docs/03_Story/Story_Structure_Bible.md`, `Story_Bible.md`
- `TheLastSwordProtocol-Atlas/atlas/docs/09_Technical/Cybersecurity_Layer_Bible.md`, `Atlas_Concordance.md`, `Glossary.md`
- `studio/agent-roles.md` - GPT's region-planning role, cited for the recommended review path
- `studio/governance/repository-authority.md` - AtlasStudio does not invent Atlas canon
