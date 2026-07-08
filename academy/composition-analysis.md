# Atlas Academy Composition Analysis

## Purpose

`academy/observation-model.md` (`WO-2001`) records what a map *is* - facts, kept separate from judgment. This document defines how Atlas Academy turns those facts into design analysis: why a composition works or fails, using the ten topics named in `work-orders/WO-2002-composition-analysis-framework.md`'s Required Topics list, each grounded here in evidence already on file in this project rather than asserted from general principle.

The immediate motivation is concrete, not hypothetical: `map_ownership.json` (`TheLastSwordProtocol-Game`) records a real rejection dated 2026-07-08 - Ashford Inn's first build pass (`Map026`, `SCR-HOM-ASH-004`) was rejected with the stated reason "interior tiles are incorrect; rocks appear in the room; sofa/furniture rendering is poor." `work-orders/WO-2002`'s own Purpose line ("Recent rejected maps showed that functional correctness is not enough") anticipates exactly this kind of case. See `reports/academy/composition-analysis-framework.md` for how this framework reads that specific rejection - honestly, including where the stated reason falls outside composition's own scope.

## How This Fits Curriculum

Per `academy/curriculum.md`, composition analysis sits between Level 1 ("Recognize" - an observation record, facts only) and Level 3 ("Diagnose" - a specific, falsifiable finding about a rejected build or documented gap). It is not a new curriculum level; it is the method a Level 2 or Level 3 case study applies once raw observations exist. A composition analysis without a grounding observation record is not yet ready to write - go back to `academy/observation-model.md` first.

## Evidence Base

This document does not invent composition theory. It draws on four sources already on file:

1. **`studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`** and the pattern documents it produced (`studio/design-patterns/interiors/*.pattern.md`) - each pattern's own Composition Rules section is primary evidence, extracted from official RPG Maker sample maps.
2. **`reports/design-patterns/interior-pattern-corpus-review.md`** (`WO-0025`) - cross-pattern findings, most importantly that wall-anchoring is a display/storage-specific convention, not universal (the corpus's single most load-bearing composition correction).
3. **`reports/map-analysis/item-shop-analysis.md`** (`TheLastSwordProtocol-Game`, read-only) - a real, worked composition analysis of one official sample map, cited throughout below as the concrete case each abstract topic is checked against.
4. **`references/atlas_academy_jrpg_map_research.md`** - a research synthesis of official RPG Maker guidance, Dragon Quest design commentary, and wayfinding/environmental-storytelling literature, explicitly labeled by confidence tier (observed fact / expert opinion / community opinion / research hypothesis). This document cites it at the confidence level it states for itself - a "research hypothesis" claim is presented as one here too, never upgraded to settled fact.

## The Ten Topics

### 1. Focal Point

**Definition:** the element a room or screen directs the player's attention to first - functional (a counter, a stair, a pedestal) or scenic, but always something the composition itself points at rather than something the player must search for.

**Grounding:** `item-shop-analysis.md`'s Composition section states this almost verbatim: "the centered entry pulls the eye upward; the rug marks the browsing zone; the animated flame and window/painting cluster give the back wall a visual anchor." The research doc's Part 4 corroborates at "observed fact" tier that official RPG Maker interior/town tutorials repeatedly reinforce establishing a fast reading order via counters, stairs, windows, and pedestals.

**What to check:** does the room have exactly one primary focal point reachable within a short read time from the entrance? A room with zero identifiable focal point, or with two or more competing equally, is a finding worth recording.

### 2. Negative Space

**Definition:** deliberately open floor that serves circulation or atmosphere, distinct from dead space that serves nothing.

**Grounding:** `interior-pattern-corpus-review.md`'s Recurring Composition Rules already distinguish "dwelling versus browsing versus socializing" density needs (`house.pattern.md`'s sparse floor versus `shop.pattern.md`'s denser one). `item-shop-analysis.md` states this precisely: "the center aisle and the tiles around the rug are deliberately open... The negative space is not empty filler; it is the customer path." The research doc's Part 4 (research-hypothesis tier) adds that subtle empty-space structure can steer movement, while its Part 9 anti-patterns section names "empty space without meaning" as the single most common composition mistake, citing official guidance directly (observed-fact tier) against unused floor area.

**What to check:** every open-floor region should have a stated purpose (a path, a browsing zone, an atmosphere choice) recorded, not left implicit. Open floor with no stated purpose is the anti-pattern, not open floor itself.

### 3. Traffic Flow

**Definition:** where a player naturally walks, inferable from composition rather than discovered through collision testing.

**Grounding:** `item-shop-analysis.md`'s Passability section traces the exact walkable set from the inferred spawn tile, and its Layout section states the resulting "traffic flow" plainly: "entry at bottom center, move north to the central aisle, branch left/right to browse display clusters, then return to the same centerline and exit. There is no maze and no hidden path." `bar.pattern.md`'s Passability Rules extend this to a denser, non-linear case: furniture islands may fragment the floor into a "connected mesh" rather than a single centerline aisle, provided no island fully seals off a walkable pocket. The research doc's Part 4 (observed-fact tier, official passability guidance) states good maps "let the player infer walkable routes from composition itself rather than from trial-and-error against collision."

**What to check:** trace the reachable set from spawn (an `academy/observation-model.md` `walkable_tiles` observation already provides this). Does the visible composition (aisle width, furniture edges, door alignment) predict that same set, or does it mislead?

### 4. Sight Lines

**Definition:** what is visible, unobstructed, from a given vantage point along the main route - distinct from traffic flow (where the player can walk) though closely related.

**Grounding:** `item-shop-analysis.md`'s Layout section: "the bottom door aligns with the central aisle, central rug, back wall window/flame area, and upper merchandise. The player sees the room's purpose immediately on entry." The research doc's Part 8 metrics table names "Average sight line" as a measurable diagnostic aid (wayfinding-research tier), while noting thresholds should vary by map type rather than being treated as a fixed target - this document does not adopt a numeric target itself; that belongs to `work-orders/WO-2003-map-metrics-framework.md`'s fuller scope.

**What to check:** from the spawn/entry tile, what is visible without moving? Does that view communicate the room's purpose (per Topic 10, Environmental Storytelling), or does the entry composition hide it behind obstruction?

### 5. Furniture Grouping

**Definition:** whether related objects are clustered by function and anchored consistently, versus scattered without evident logic.

**Grounding:** this is the corpus's most explicitly corrected topic. `shop.pattern.md` states storage furniture should be wall-anchored, never floating; `house.pattern.md` corroborates this for a second building type. `bar.pattern.md` **overrides** that same rule for its own domain: "The observed bar's furniture is overwhelmingly *not* wall-anchored - it is scattered as small islands throughout the open floor, which is correct and intentional for a social/seating space... wall-anchoring is a display-furniture convention, not a universal interior rule." The research doc's Part 9 names "random furniture or prop placement" as a distinct anti-pattern from over-decoration - "a bed beside a shop counter... weakens both realism and navigational intuition" (official-guidance tier).

**What to check:** is every furniture cluster's grouping logic statable in one sentence ("stock display," "seating island," "storage")? A cluster whose logic cannot be stated, or that mixes unrelated object types without narrative reason, is a finding. Do not apply `shop.pattern.md`'s wall-anchoring rule to a room whose `Required Conditions` do not match it (per `studio/design-patterns/PATTERN_RESOLUTION_RULES.md`'s "Exceptions" - the same discipline `reports/implementation-contracts/ashford-inn-pattern-aware-contract.md` already applied when `inn.pattern.md` itself did not resolve for a single-room build).

### 6. Room Zones

**Definition:** distinct functional sub-areas within one building, connected by deliberate chokepoints rather than open boundaries, when a building is large or complex enough to have more than one.

**Grounding:** `inn.pattern.md` is the corpus's primary zoning evidence: common room versus guest-quarters wing, connected by "a single narrow spine... not a wide open boundary." `interior-pattern-corpus-review.md`'s Recurring Passability Rules generalize this across both multi-zone buildings in the corpus (Inn, Chief's House 2F): "zones never share a wide-open boundary - they connect through a single narrow corridor or doorway gap." `chief-house.pattern.md` extends zoning to a second axis (public ground floor versus private upper-floor chambers) with its own composition consequence: private chambers "should read as individually furnished," not a repeated module, unlike the Inn's deliberately repeated guest-nook rhythm. This is also the exact category (`room_zone`) added to `schemas/academy-observation.schema.json` in `WO-2001`, specifically because this finding had no clean home in the prior category list.

**What to check:** does the building have more than one functional zone? If so, is the connection a deliberate chokepoint (per the corpus finding above) or an open, undifferentiated boundary? A building whose `Required Conditions` call for single-room simplicity (per Topic 5's note) does not need this check applied at all - zoning analysis presupposes a multi-zone building exists to analyze.

### 7. Entry Readability

**Definition:** whether a player can tell, immediately on entering, what a space is for and how to move through it.

**Grounding:** every pattern in the corpus corroborates a specific, shared threshold construction (stairs-family tile one row above a floor tile carrying the transfer event) precisely because it makes entry legible and consistent across every interior type - `interior-pattern-corpus-review.md`'s Recurring Layout Rules calls this "the single most universal finding in the corpus (8/8)" for the shell-plus-void construction and threshold stack together. The research doc's Part 9 names "maze-like civic space" as an anti-pattern at the town scale: hiding critical services behind visually similar branches "may increase search time without increasing delight" (research-hypothesis tier, but directly citing official guidance on small-town service clustering).

**What to check:** from the entry tile, is the room's purpose inferable within the "short read time" Topic 1 already established? Entry readability is largely the composite of Topics 1, 3, and 4 checked together at the specific moment of arrival, not a separate measurement - record it as a synthesis note, not a duplicate check.

### 8. Visual Hierarchy

**Definition:** whether the composition establishes a clear order of importance among its elements, so the player's eye is drawn to what matters most first.

**Grounding:** the research doc's Part 4 states this as the composition section's opening claim (observed-fact tier, citing official town/interior tutorials directly): "Good JRPG maps establish a reading order. The eye should identify the entrance, main destination, notable obstacle, and optional point of interest within seconds." `chief-house.pattern.md`'s "most formal, symmetric composition in the corpus" for its ground-floor hall is a worked example of hierarchy serving a specific narrative purpose (a hall meant for gathering or audience, not private living) rather than symmetry for its own sake.

**What to check:** can a viewer name, in order, what they notice first, second, and third? If every element competes equally (the research doc's Part 9 "over-decoration" anti-pattern - "when every tile competes for attention, players lose hierarchy"), that is the finding, not a vague sense that the room looks busy.

### 9. Decoration Balance

**Definition:** whether decorative density matches the room's function, neither so sparse it reads as empty nor so dense it obscures hierarchy.

**Grounding:** `interior-pattern-corpus-review.md`'s Recurring Composition Rules states this directly: "decoration density scales with function, not just size... `house.pattern.md` (17x13) is sparsely furnished... while `shop.pattern.md`... `bar.pattern.md` (also 17x13) are all much denser. Density tracks what the room is *for*." `inn.pattern.md` adds a lighting-specific version of the same rule: flame count should scale with zone count, not room size alone. The research doc's Part 8 offers a provisional, explicitly hypothesis-tier numeric band ("8-20 [decorative objects] per 100 [walkable tiles] for towns; 4-12 for dungeons") - cited here as a diagnostic prompt per that document's own "Metric interpretation notes" caveat, not as a pass/fail threshold this framework adopts as settled.

**What to check:** does decoration density read as intentional for this room's function, checked against the closest-fitting pattern's own density (a shop denser than a house; a bar denser still)? A room that copies one pattern's density onto a functionally different room (the research doc's and the corpus review's shared warning) is a finding.

### 10. Environmental Storytelling

**Definition:** what a space communicates about its use, ownership, and history without dialogue or text.

**Grounding:** the research doc's Part 7 states the operative test directly (citing environmental-narrative research, expert/research-hypothesis tier): "every important map should answer four silent questions - what happens here, who controls it, what is allowed here, and what changed recently. If the map cannot answer those questions visually, it is under-expressive." This project already practices this principle in its own canon, independent of this framework: `LOC-ASH-001` (`TheLastSwordProtocol-Atlas`)'s "Hidden Reality" section states Ashford is built inside an old-world factory shell, and its own guidance is explicit that "technology should appear as village texture, not sci-fi" - composition (which tiles, which objects, how salvaged metal is folded into ordinary buildings) is literally how that canon fact is meant to reach the player, not through a stated line of dialogue.

**What to check:** can the room's use, ownership, and recent history be read from its composition alone? For an Ashford interior specifically, does the composition carry the "warm, ordinary, quietly strange" tone `LOC-ASH-001` requires, or does it read as generic?

## What This Framework Does Not Do

- It does not compute the numeric metrics named throughout (walkable percentage, decoration density, sight-line length) as a formal, systematic measurement pass - that is `work-orders/WO-2003-map-metrics-framework.md`'s scope. Where a metric is mentioned here, it is cited as a diagnostic prompt from `references/atlas_academy_jrpg_map_research.md`, at that document's own stated confidence tier, not adopted as this framework's own settled threshold.
- It does not assign a numeric grade. `academy/composition-rubric.md` operationalizes these ten topics into a checkable form; the full, multi-category grading model that would combine a composition verdict with passability, metrics, and project fit into one overall recommendation is `work-orders/WO-2005-map-grading-system.md`'s scope.
- It does not modify `TheLastSwordProtocol-Atlas`, `TheLastSwordProtocol-Game`, any existing Design Pattern, or create or edit any map.

## References

- `academy/observation-model.md`, `curriculum.md`, `composition-rubric.md`, `compositions/README.md`
- `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`, `PATTERN_RESOLUTION_RULES.md`
- `studio/design-patterns/interiors/shop.pattern.md`, `house.pattern.md`, `inn.pattern.md`, `bar.pattern.md`, `chief-house.pattern.md`
- `reports/design-patterns/interior-pattern-corpus-review.md`
- `reports/map-analysis/item-shop-analysis.md` (`TheLastSwordProtocol-Game`, read-only)
- `references/atlas_academy_jrpg_map_research.md`
- `atlas/docs/02_World/Locations/Home_Island/Ashford.md` (`LOC-ASH-001`, `TheLastSwordProtocol-Atlas`, read-only)
- `reports/implementation-contracts/ashford-inn-pattern-aware-contract.md`
- `reports/academy/composition-analysis-framework.md`
- Created by `work-orders/WO-2002-composition-analysis-framework.md`
