# Pattern Extraction Guide

## Purpose

This guide teaches a future agent how to analyze an official RPG Maker sample map and turn what it finds into evidence a pattern can be built from. It exists because `reports/map-analysis/item-shop-analysis.md` (in `TheLastSwordProtocol-Game`) was produced once, by one agent, without a standing method - this guide is that method, written down so the next extraction does not have to be reinvented, and so two different agents extracting two different sample maps produce comparably rigorous evidence.

Extraction and pattern-writing are two separate steps. This guide covers extraction: producing an analysis report with objective, citable observations. Turning that report into a pattern document is covered by `PATTERN_SCHEMA.md` and `PATTERN_REVIEW_PROCESS.md`.

## What to Measure

Work from the actual map data file (e.g. `data/MapXXX.json`), not from a screenshot or memory of the tileset. For each sample map, record:

- **Dimensions.** Full map size, and separately, the playable/architectural footprint if it is smaller than the full map (void/darkness margins do not count as playable space).
- **Door and threshold placement.** Exact tile coordinates of the entrance/exit tile(s), the threshold tile(s), and the transfer event(s) that make them work.
- **Inferred or explicit spawn position.** Where the player lands, and the evidence for that inference (an adjacent transfer target elsewhere, a convention observed across sibling maps, etc.). Label it "inferred" if it is not explicit in the data.
- **Structural object placement.** Coordinates and extents of counters, shelves, cabinets, tables, or other structural furniture, and which wall or edge each is anchored to.
- **Walkable tiles.** The full reachable set from the spawn point, traced tile by tile using the tileset's passability flags, not by visual guess.
- **Interaction distances.** For every object that looks interactable, the walkable tile(s) adjacent to it.
- **NPC placement**, if any, and whether an interaction event is actually wired to it.
- **Dead space.** Both the outer void/darkness margin and any blocked-but-inside-the-shell zones, measured as tile counts.
- **Autotile and tile usage.** Which named autotile groups are used where (e.g. `A2 Table A (Wood)`, `A4 Wall H (Wood)`), sourced from the tileset's own labels, not guessed from appearance.
- **Shadow and lighting data.** Where shadow values are set, and where animated/decorative events exist.
- **Event inventory.** Every event on the map: ID, position, image, trigger type, priority, and full command list (or "none").
- **Transfer inventory.** Every transfer event: source tile, trigger, destination map and tile, and whether the reverse transfer exists anywhere in the project.

Use exact tile coordinates throughout extraction. This is evidence-gathering, not pattern-writing - coordinates belong in the extraction report; they must not be copied forward into the pattern document as prescriptive positions (see "What Not to Infer" and `PATTERN_SCHEMA.md`, "Format Discipline").

## What Not to Infer

Do not treat the following as facts unless the map data explicitly supports them:

- **Player spawn position**, when no incoming transfer targets the map in the current project. State it as inferred, and state the reasoning (sibling-map convention, adjacency to the threshold tile, etc.) - never present an inferred spawn as confirmed.
- **NPC roles or intent** for NPCs that do not exist in the data. If a shop map has no shopkeeper event, the correct observation is "no shopkeeper event exists," not "the shopkeeper stands behind the counter."
- **Gameplay systems the map does not implement.** An official sample map that looks like a shop is not necessarily wired for RPG Maker's Shop Processing. Check the event commands; do not assume the visual genre implies the mechanical system.
- **Exact tile coordinates as universal law.** "The door is at (8,11) in this map" is a fact about this map. "Doors should be centered on the primary aisle" is a pattern. Extraction produces the former; pattern-writing (governed by `PATTERN_SCHEMA.md`) produces the latter, and the jump from one to the other requires corroboration per `PATTERN_CONFIDENCE_MODEL.md`, not a single observation.
- **Authorial intent beyond what the data shows.** "This shelf cluster suggests the designer wanted a cluttered feel" is a subjective read (allowed, but must be labeled subjective) - "this shelf cluster has 6 blocked tiles against the back wall" is objective.

## Objective Observations

Objective observations are directly verifiable from the map JSON and tileset data without interpretation:

- Tile coordinates, dimensions, tile/autotile IDs.
- Passability flags per tile (from `Tilesets.json`).
- Event existence, position, trigger type, priority, and command list.
- Counts (number of events, number of blocked tiles, number of walkable tiles).
- Presence or absence of a specific system (e.g. "no Shop Processing command exists in any event on this map").

Every objective observation must be reproducible: a second agent given the same map file should arrive at the same fact.

## Subjective Observations

Subjective observations are interpretive judgments about why a layout works, even though they are grounded in the objective data:

- "The room feels balanced because it is bilaterally organized around the center column" - grounded in coordinate symmetry, but "feels balanced" is a judgment call.
- "The centered entry pulls the eye toward the back wall" - a composition claim, not a measurable fact.
- "This rhythm of dense-wall / open-aisle / dense-display reads as intentional, not accidental" - an interpretation of a pattern in the data.

Subjective observations are legitimate and necessary - `PATTERN_SCHEMA.md`'s "Composition Rules" section depends on them - but they must be presented as interpretation, not fact.

## How to Distinguish Them

State every subjective observation in "why" or "feels" language tied explicitly back to an objective observation it is derived from. A useful test: if a second agent, given the same map data, could disagree with the claim while agreeing on every objective fact, the claim is subjective and must be labeled as such.

In the extraction report, keep objective and subjective observations in separate sections (see `reports/map-analysis/item-shop-analysis.md`'s `Layout`/`Tile Usage`/`Passability`/`Event Design` sections for objective data, and its `Composition` section for labeled interpretation) rather than interleaving them inside a single paragraph.

## How to Cite Evidence

- Every claim in an extraction report must trace to a specific map file and, wherever possible, specific tile coordinates or event IDs.
- When an extraction report is later used to write or revise a pattern (`PATTERN_SCHEMA.md`'s "Source" and "Observed Maps" sections), the pattern must cite the extraction report by path, not restate the raw data - "point, don't paraphrase," the same discipline `bridges/atlas/implementation-handoff.md` already uses for Atlas-to-Game handoffs.
- If an observation is inferred rather than confirmed (see "What Not to Infer"), the inference and its reasoning must survive into any pattern that depends on it, not get silently upgraded to fact.
- A pattern's confidence level is only as strong as its extraction evidence - see `PATTERN_CONFIDENCE_MODEL.md` for how citation count and quality map to confidence.

## Output of an Extraction Pass

An extraction pass produces an analysis report (e.g. `reports/map-analysis/<name>-analysis.md` in the relevant project repo), not a pattern document. The report should read the way `reports/map-analysis/item-shop-analysis.md` does: `Layout`, `Tile Usage`, `Composition`, `Passability`, `Event Design`, and a closing `Reusable Design Rules` / `AtlasStudio Recommendations` section that bridges into pattern-writing without being the pattern itself. A future work order (or the same one, at the author's discretion) then applies `PATTERN_SCHEMA.md` to convert that report's `Reusable Design Rules` into an actual pattern document, subject to `PATTERN_REVIEW_PROCESS.md`.
