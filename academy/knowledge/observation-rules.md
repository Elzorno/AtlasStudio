# Atlas Academy Knowledge: Observation Rules

## Status

Documentation only, per `work-orders/WO-2006-atlas-academy-knowledge-extraction.md`. This file converts `references/atlas_academy_jrpg_map_research.md` (Part 1, Part 10 "Observation rules," Module 1) into reusable Atlas Academy knowledge. It does not analyze any map, does not create an implementation contract, and does not create or modify a Design Pattern. It does not modify `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md` or `schemas/academy-observation.schema.json` (`WO-2001`) - both remain the actual governing method and schema for Level 1 (Recognize) work per `academy/curriculum.md`. This file supplies the rationale and vocabulary behind that existing method; it does not replace it.

## Observed Fact

- Official RPG Maker guidance repeatedly states that maps should be only as large as needed and that space should be used meaningfully rather than left blank or padded.[cite:16][cite:46]
- Tile layering and passability rules mean the last-placed tile can determine walkability, so composition and collision cannot be observed as separate concerns.[cite:17]
- Official interior guidance assumes object placement implies use, ownership, and practical logic - a basic environmental-storytelling signal present even in beginner-focused tutorials.[cite:46]
- The report's own worked example of the observed-fact/inference boundary: "Counter blocks direct access to shelves" is observed fact; "Counter implies public-versus-private boundary" is inference.[cite:46][cite:49]
- Horii and Nakamura's published remarks state that Dragon Quest's early design explicitly prioritized ease of understanding and concise, memorable dialogue.[cite:30]

## Expert Opinion

- Horii and Nakamura emphasized understandability, subtle balancing, and preserving simple-but-deep systems over novelty for its own sake.[cite:11][cite:15][cite:30]
- Horii described deliberately making players feel the effect of leveling and equipment upgrades - a form of competence feedback that extends to map observation: a well-designed map rewards correct spatial interpretation (a recognized shortcut, a correctly read landmark) with smoother movement or a found reward.[cite:30]
- Horii cautioned against relying blindly on strategy guides, favoring discoverability through play - implying an observer should expect maps to be legible through traversal, not only through external explanation.[cite:30]

## Community Practice

The source report's community-practice material (`Community best practices versus official guidance`) concerns visual richness, elevation tricks, and decoration density generally; it does not offer community guidance specific to observation methodology as such. No community-practice claim is asserted here as a distinct observation rule. This is a stated gap, not a filled one - inventing a community-practice observation rule the source does not support would violate this extraction's own provenance discipline (see `academy/references/reference-governance.md`).

## Atlas Interpretation

- The report's Part 10 "Observation rules" proposes a sequence: identify map type, then circulation spine, then public/service/private/optional zones, then landmarks, then visible barriers, then reward cues, then assess readability and pacing.[cite:16][cite:20][cite:33][cite:46] This sequence is **not** adopted here as a second or competing observation method. `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md` already governs Level 1 (Recognize) work under `academy/curriculum.md`, with its own objective/subjective distinction. This knowledge file's role is to record that the report's proposed sequence and the existing guide's method converge on the same underlying discipline - describe before judging, and tag every claim by evidentiary status - rather than to introduce a rival checklist.
- The report's observed-fact/inference distinction (`Counter blocks direct access to shelves` vs. `Counter implies public-versus-private boundary`) maps directly onto `PATTERN_EXTRACTION_GUIDE.md`'s objective/subjective split and onto `schemas/academy-observation.schema.json`'s structure (`WO-2001`). No new field or category is proposed; this is a confirmation that the research and the existing schema already agree, recorded explicitly so a future reader does not have to re-derive it.
- Where the report names "reward cues" and "barriers" as things an observer should identify, the closest existing hook is `academy/observation-model.md`'s object/event/transfer inventory fields (`WO-2001`) - reward cues and barriers are not new schema fields, they are a way of describing what those existing fields are for.

## Research Hypothesis

- Players enjoy JRPG maps when the maps feel like interpretable puzzles rather than raw geography; exploration pleasure is framed as successfully decoding spatial intent.[cite:33][cite:34][cite:37]
- Cognitive mapping: players build internal representations from landmarks, routes, edges, and districts, and spaces supporting this process are easier and more satisfying to navigate.[cite:33][cite:34][cite:38]
- Attention control: empty space, focal contrast, and landmark recognizability influence route selection and reduce navigational friction.[cite:33][cite:37][cite:38]
- Curiosity pacing: alternating certainty and uncertainty (readable local maps against a simpler world map) sustains exploration motivation.[cite:20]

## Non-Goals

- Does not modify `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`, `schemas/academy-observation.schema.json`, or `academy/observation-model.md`.
- Does not analyze, observe, or grade any specific map.
- Does not propose a new observation method or a new schema field.

## References

- `references/atlas_academy_jrpg_map_research.md` (Part 1, Part 10 "Observation rules," Module 1)
- `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`
- `schemas/academy-observation.schema.json`, `academy/observation-model.md`
- `academy/curriculum.md` (Level 1 - Recognize)
- `academy/references/reference-governance.md`, `source-classes.md`
- `reports/academy/knowledge-extraction-report.md`
- Created by `work-orders/WO-2006-atlas-academy-knowledge-extraction.md`
