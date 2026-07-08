# Atlas Academy Observation Model

## Status

Documentation and schema only, per `work-orders/WO-2001-academy-observation-engine.md`'s constraints. This document defines the observation model; `schemas/academy-observation.schema.json` formalizes it as a machine-checkable record. Neither builds the tool that would produce or validate a record automatically - that is future work, not named or scoped here.

## Purpose

AtlasStudio should separate facts from conclusions. `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md` already draws this line for prose extraction reports - objective observations (directly verifiable from map data) kept structurally apart from subjective observations (interpretive judgments, labeled as such). The Observation Engine is the structured, schema-backed counterpart to that same discipline: a single record format an agent or future tool can fill in *before* any interpretation or grading happens, so that whatever grading model comes later (`academy/grading-rubric.md` today; the full `work-orders/WO-2005-map-grading-system.md` eventually) is graded against recorded facts, not against someone's memory of what a map looked like.

This document does not replace `PATTERN_EXTRACTION_GUIDE.md`. That guide remains the authoritative method for *how* to look at a source map and what to look for. This document defines the *record* that method now has a formal place to land in, in addition to (not instead of) the prose extraction report format that guide already specifies.

## Observation Fields

`schemas/academy-observation.schema.json` is the authoritative field list. In summary, an observation record has four parts:

1. **Source provenance** (`source`) - which repository, file, map, tileset, reference class, ownership state, and version this observation is about. See "Source Map Provenance" below.
2. **Objective observations** (`objective_observations`) - a list of directly verifiable facts, each carrying its own category, description, value, evidence citation, and an explicit `is_inferred` flag.
3. **Subjective observations** (`subjective_observations`) - a list of interpretive judgments, each explicitly grounded in one or more objective observations from the same record.
4. **Downstream linkage** (`feeds`) - optional pointers to whatever extraction report, pattern candidate, or Academy case study this record was used to support.

Objective observation categories mirror `PATTERN_EXTRACTION_GUIDE.md`'s "What to Measure" list directly - dimensions, door/threshold placement, spawn position, structural object placement, walkable tiles, interaction distances, NPC placement, dead space, tile/autotile usage, shadow/lighting data, event inventory, and transfer inventory - extended with one category that guide does not separately name: `room_zone`, added because `studio/design-patterns/interiors/inn.pattern.md` already documents a real multi-zone finding (common room versus guest-quarters wing) that the existing category list has no clean home for. No other category was invented beyond what already-published AtlasStudio evidence required.

`WO-2001`'s own brief names several examples (map dimensions, door coordinates, room zones, event count, walkable percentage, furniture groups, counter placement, window count, transfer locations) - every one of these maps onto the categories above (`dimensions`, `door_threshold`, `room_zone`, `event`, `walkable_tiles`, `structural_object`, `structural_object` again, `tile_usage`, `transfer`, respectively). Two of the brief's examples are worth flagging directly: **"event count" and "walkable percentage" are computed summaries, not raw facts** - they are legitimate objective observations here (a count or percentage derived from the record's own `event`/`walkable_tiles` entries is still reproducible, per the reproducibility bar below), but a richer, more systematic set of computed metrics is `work-orders/WO-2003-map-metrics-framework.md`'s fuller scope, not this foundation's. This document records the simple case; it does not attempt `WO-2003`'s job.

## Evidence Requirements

Every `objective_observations` entry requires an `evidence` object naming an `evidence_type`, a `file_path`, and (where applicable) `coordinates`, an `event_id`, or a `layer`. This is not a formality - it is the same reproducibility bar `PATTERN_EXTRACTION_GUIDE.md` already states directly: "Every objective observation must be reproducible: a second agent given the same map file should arrive at the same fact." An observation entry that cannot name where in the source file it came from does not meet that bar and should not be recorded as objective - if it cannot be pinned to specific data, it likely belongs in `subjective_observations` instead, honestly grounded rather than dressed up as a fact.

A subjective observation carries a different kind of evidence requirement: not a file citation, but a `grounded_in` reference back to one or more objective observations in the *same record*. An interpretive claim with nothing to ground it is not yet ready to record, per `PATTERN_EXTRACTION_GUIDE.md`'s own test: "if a second agent, given the same map data, could disagree with the claim while agreeing on every objective fact, the claim is subjective" - which presupposes agreed-upon objective facts exist to disagree around.

## Source Map Provenance

`source.repo`, `source.file_path`, and `source.map_name` identify what was observed. Two further fields exist specifically because source data changes over time, and an observation record should stay valid evidence even after it does:

- **`source.ownership_state_at_capture`** records a Game-repo map's `bridges/rpg-maker-mz/ownership-model.md` state (from `map_ownership.json`) at the moment of observation - `generated`, `agent-drafted`, `human-edited`, `hand-authored`, or `locked`. A map that was `generated` when observed and is `hand_authored` by the time someone reads the record later is a different map in every sense that matters to Academy; pinning the state at capture time prevents that drift from silently invalidating old evidence.
- **`source.provenance_ref`** anchors the observation to a specific git commit, tag, or date, for the same reason `academy/references/README.md` requires every citation to trace to a specific source - a map file with no version anchor is a moving target, not evidence.

`source.source_class` (`official_sample`, `accepted_build`, `rejected_build`, `other`) matches the reference source classes named in `academy/references/README.md`. This document does not add governance beyond what that document (and its future full form, `work-orders/WO-2004-reference-library-governance.md`) already states - it only requires that every observation record say which class its source belongs to.

## Screenshot References

`screenshot_references` exists for supplementary, human-readable material - the kind of engine-render image `rpgmakerLSP`'s own build reports already attach (e.g. `wo-0035-map002-render.png`, `wo-0036-map001-render.png`). Every entry's `role` is fixed to `illustrative_only` in the schema, on purpose: `PATTERN_EXTRACTION_GUIDE.md`'s core rule is to "work from the actual map data file... not from a screenshot or memory of the tileset," and this schema enforces that rule structurally rather than trusting every future record author to remember it. A screenshot may accompany a record. It may never be the `evidence` for an `objective_observations` entry.

## JSON References

Every piece of `evidence` on an objective observation is, in practice, a JSON reference: a `file_path` (normally the source map's own `data/MapXXX.json`, occasionally a sibling file like `Tilesets.json` for tile-usage evidence), plus `coordinates`, an `event_id`, or a `layer` locating the exact fact inside it. This is deliberately the same discipline `PATTERN_EXTRACTION_GUIDE.md` already uses ("Use exact tile coordinates throughout extraction") formalized into a structured field instead of prose. Coordinates and event IDs recorded here are evidence, not prescription - per that guide's own warning, "The door is at (8,11) in this map" is a fact about this map, not a rule about where doors belong; turning coordinate-level facts into a general layout rule is pattern-writing (`studio/design-patterns/PATTERN_SCHEMA.md`), a separate and later step this record does not perform.

## Distinction Between Objective and Subjective Notes

This is the model's central discipline, inherited unchanged from `PATTERN_EXTRACTION_GUIDE.md` and enforced structurally by the schema rather than left to convention:

- `objective_observations` and `subjective_observations` are two separate top-level arrays. A record cannot interleave them inside one entry.
- Every objective entry carries `is_inferred` - `false` for a fact explicitly present in the data, `true` for something reasoned rather than confirmed (a spawn position with no incoming transfer to verify it, for instance). An inferred fact is still objective in kind - it is a claim about the source data, not a design judgment - but it carries weaker evidentiary weight, and this schema requires that distinction be visible rather than silently upgrading an inference to a confirmed fact, per `PATTERN_EXTRACTION_GUIDE.md`'s "What Not to Infer."
- Every subjective entry must name what objective observation(s) it is `grounded_in`. An ungrounded interpretation is not recordable under this model.

## How Observations Feed Pattern Extraction

The `feeds` object is this record's link forward into the rest of Atlas Academy and the existing Pattern Library:

- `feeds.extraction_report` points at the prose report (`PATTERN_EXTRACTION_GUIDE.md`'s existing output format) this observation record supports, once one is written.
- `feeds.pattern_candidates` names any existing or proposed `pattern_id` this record's findings bear on - the mechanism `academy/curriculum.md`'s Level 4 ("Propose") uses to route a finding back into `studio/design-patterns/PATTERN_REVIEW_PROCESS.md`'s existing, unchanged proposal path. Recording an observation never itself proposes or changes a pattern; it only marks relevance for whoever later does.
- `feeds.case_study` points at an `academy/reports/` entry, if this record was used to build one.

None of these fields are required at capture time. An observation can be recorded before anyone knows what it will be used for - the same way `PATTERN_EXTRACTION_GUIDE.md`'s extraction step is already separated from the later pattern-writing step it feeds.

## Worked Example

This example is not new analysis. It re-expresses facts already published in `reports/map-analysis/item-shop-analysis.md` (`TheLastSwordProtocol-Game`, read-only, cited here per that repository's own convention) in this document's structured shape, to show what a real observation record looks like without performing a fresh extraction pass - `WO-2001` is documentation and schema only and does not authorize new analysis. Abbreviated for readability; a real record would cover every category that report addresses.

```json
{
  "schema_version": "0.1.0",
  "observation_id": "OBS-ITEMSHOP-001",
  "source": {
    "repo": "TheLastSwordProtocol-Game",
    "file_path": "data/Map021.json",
    "map_name": "Item Shop",
    "tileset_reference": "Inside (tilesetId: 3)",
    "source_class": "official_sample",
    "captured_at": "2026-07-08",
    "ownership_state_at_capture": null,
    "provenance_ref": "as cited in reports/map-analysis/item-shop-analysis.md"
  },
  "observer": "atlas-academy-worked-example",
  "created": "2026-07-08",
  "objective_observations": [
    {
      "category": "dimensions",
      "description": "Full map is 17x13 tiles; the playable shop shell occupies roughly x4-x12, y1-y11, with void/darkness outside it.",
      "value": { "full_width": 17, "full_height": 13, "shell_x": [4, 12], "shell_y": [1, 11] },
      "evidence": { "evidence_type": "map_json_tile_layer", "file_path": "data/Map021.json", "coordinates": null, "event_id": null, "layer": 0 },
      "is_inferred": false,
      "inference_reasoning": null
    },
    {
      "category": "door_threshold",
      "description": "Threshold tile at (8,10), floor/door tile with the exit transfer at (8,11), centered on the bottom axis at x8.",
      "value": { "threshold": [8, 10], "transfer_tile": [8, 11] },
      "evidence": { "evidence_type": "map_json_tile_layer", "file_path": "data/Map021.json", "coordinates": [8, 11], "event_id": null, "layer": 0 },
      "is_inferred": false,
      "inference_reasoning": null
    },
    {
      "category": "spawn_position",
      "description": "Player spawn inferred at (8,10), one tile inside the doorway.",
      "value": [8, 10],
      "evidence": { "evidence_type": "map_json_tile_layer", "file_path": "data/Map021.json", "coordinates": [8, 10], "event_id": null, "layer": 0 },
      "is_inferred": true,
      "inference_reasoning": "No current-project event transfers into Map021, so spawn is not explicit in the data. Inferred from the Village 1 sample interiors' convention of centered bottom doors with a transfer event one tile below the visible threshold, per reports/map-analysis/item-shop-analysis.md."
    },
    {
      "category": "transfer",
      "description": "One exit transfer event (EV002) at (8,11): player-touch trigger, below-characters priority, plays SE Move1, transfers to map 2 at (20,15). No incoming transfer to this map found in the project.",
      "value": { "trigger": "player_touch", "destination_map": 2, "destination_tile": [20, 15], "reverse_transfer_found": false },
      "evidence": { "evidence_type": "map_json_event", "file_path": "data/Map021.json", "coordinates": [8, 11], "event_id": "EV002", "layer": null },
      "is_inferred": false,
      "inference_reasoning": null
    },
    {
      "category": "npc_placement",
      "description": "No shopkeeper or other NPC event exists on this map.",
      "value": { "npc_count": 0 },
      "evidence": { "evidence_type": "map_json_event", "file_path": "data/Map021.json", "coordinates": null, "event_id": null, "layer": null },
      "is_inferred": false,
      "inference_reasoning": null
    }
  ],
  "subjective_observations": [
    {
      "description": "The room feels balanced because it is bilaterally organized around x8, with the doorway, center aisle, and back-wall mass on or near the center axis.",
      "grounded_in": ["door_threshold: threshold centered at x8", "dimensions: shell spans x4-x12"]
    }
  ],
  "screenshot_references": [],
  "feeds": {
    "extraction_report": "reports/map-analysis/item-shop-analysis.md",
    "pattern_candidates": ["PAT-INTERIOR-SHOP"],
    "case_study": null
  },
  "notes": "Worked example only, built from already-published facts in reports/map-analysis/item-shop-analysis.md. Not a new extraction pass; abbreviated for illustration."
}
```

Note what this example deliberately shows: the `spawn_position` entry is marked `is_inferred: true` with its reasoning stated, exactly matching the source report's own "inferred as (8,10)" language - this model does not let a structured record quietly upgrade that inference to a confirmed fact just because it is now stored in a schema instead of prose.

## Relationship to Other Atlas Academy Documents

- `academy/curriculum.md` - this model's records are the artifact Level 1 ("Recognize") produces.
- `academy/references/README.md` - `source.source_class` uses that document's reference source classes directly.
- `academy/reports/README.md` - a completed case study may cite one or more observation records via `feeds.case_study`.
- `academy/grading-rubric.md` - grading happens after observation, never inside it; this model records facts, not verdicts.

## Non-Goals

- This document and its schema do not build a tool that produces, validates, or queries observation records. That is future work, not named here.
- This document does not perform a new extraction pass against any map. The worked example above re-expresses already-published facts.
- This document does not modify `TheLastSwordProtocol-Atlas`, `TheLastSwordProtocol-Game`, or any map.
- This document does not compute the fuller metrics set (`work-orders/WO-2003-map-metrics-framework.md`'s scope) beyond the two simple computed-summary examples named in "Observation Fields."

## References

- `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`, `PATTERN_SCHEMA.md`, `PATTERN_REVIEW_PROCESS.md`
- `academy/README.md`, `curriculum.md`, `grading-rubric.md`, `references/README.md`, `reports/README.md`
- `schemas/academy-observation.schema.json`
- `bridges/rpg-maker-mz/ownership-model.md`
- `reports/map-analysis/item-shop-analysis.md` (`TheLastSwordProtocol-Game`, read-only)
- `studio/design-patterns/interiors/inn.pattern.md` (source of the `room_zone` category addition)
- Created by `work-orders/WO-2001-academy-observation-engine.md`
