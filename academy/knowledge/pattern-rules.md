# Atlas Academy Knowledge: Pattern Rules

## Status

Documentation only, per `work-orders/WO-2006-atlas-academy-knowledge-extraction.md`. This file converts `references/atlas_academy_jrpg_map_research.md` (Part 2, Part 3, Part 5, Part 6, Part 10 "Pattern rules," Module 8) into reusable Atlas Academy knowledge. **It does not create a Design Pattern.** `studio/design-patterns/` documents (governed by `PATTERN_SCHEMA.md`, `PATTERN_REVIEW_PROCESS.md`) are a separate, formal artifact with their own review path per `academy/curriculum.md` Level 4 (Propose); nothing in this file has been through that review, and nothing here should be cited as if it had.

## Observed Fact

- Towns in official guidance are composed around a few recognizable civic or service nodes - entry road, inn, shop, central square, a handful of residences - with clustered relevance rather than density for its own sake.[cite:16]
- Interior guidance states that counters protect private zones, storage goes near commercial activity, and domestic functions should not sit carelessly in the middle of customer flow unless the awkwardness is intentional characterization.[cite:46]
- DQIII's roundtable states the Earth-like world shape was chosen because it was familiar and easier to grasp - a direct, documented link between macro-layout choice and readability.[cite:30]
- Official world-map guidance frames the overworld as an abstraction meant to improve pacing, using roads, borders, and route constraints to make travel legible and efficient rather than realistic.[cite:20]

## Expert Opinion

- Horii explained that Dragon Quest's map philosophy begins with understandability, given that broad audiences could be overwhelmed by genre freedom - implying exploration patterns should teach through traversal rather than require external explanation.[cite:11][cite:30]
- Horii spoke positively about discovering fun through play rather than reducing the experience to guide-following, favoring secrets that validate curiosity over secrets that punish reasonable play.[cite:30]

## Community Practice

The source report's community-practice material concerns visual density and decoration preference (see `academy/knowledge/composition-rules.md`), not exploration-structure patterns specifically. No community-practice pattern claim is asserted here; this is a stated gap, consistent with this extraction's provenance discipline.

## Atlas Interpretation

- The report's Part 10 "Pattern rules" gives four example abstract exploration schemas: "safe hub with two readable branches," "visible landmark with deferred access," "looping dungeon branch that returns near entrance," and "service cluster near main route with one optional hidden reward."[cite:20][cite:30][cite:33] These are recorded here as **candidate pattern-extraction targets** for a future Level 4 (Propose) work order under `academy/curriculum.md` and `studio/design-patterns/PATTERN_REVIEW_PROCESS.md` - not as accepted patterns. None has been checked against `PATTERN_CONFIDENCE_MODEL.md`'s two-source corroboration bar, and none has passed `PATTERN_REVIEW_PROCESS.md`'s three-check review.
- The report's town-composition principle ("dominant circulation spine and one or two secondary branches")[cite:16][cite:34] and its inn/shop/house transferable principle ("every furnishing cluster should answer a purpose question")[cite:46][cite:49] both describe the same shape of finding the existing `inn.pattern.md` Required Conditions gap already surfaced in `reports/implementation-contracts/ashford-inn-pattern-aware-contract.md` (`WO-0027`) and `reports/academy/composition-analysis-framework.md` (`WO-2002`): official guidance states a general principle, but the current Specialization-tier pattern library does not yet have an entry for every building type that principle implies (a single-room lodging interior, most concretely). This file does not resolve that gap; it records that the research corpus corroborates the gap already found by direct project work, which is itself useful provenance for a future Level 4 proposal.
- Dragon Quest's "constrained local freedom, visible but deferred goals, repeated relief points" rhythm[cite:11][cite:15][cite:30] is directly relevant to `DDR-0005`'s (`TheLastSwordProtocol-Atlas`) decision to move Ashford toward a primary-town-map-plus-building-submaps exploration model, since that decision is itself a Dragon-Quest-style structural choice. This file notes the connection for future Academy reference; it does not modify `DDR-0005` or any Atlas canon, and DDR-0005 was decided on direct Production Director instruction, not derived from this research corpus.

## Research Hypothesis

- The official sample-map family likely feels coherent not because every map is highly detailed, but because each map type reuses a small vocabulary of readable signals - entry, destination, obstacle, reward cue, optional branch - implemented with different tile themes.[cite:16][cite:17][cite:20][cite:46]
- Across Dragon Quest I, II, III, V, and XI, the most durable pattern is not any specific map shape but a sequence of constrained local freedom, visible but deferred goals, and repeated relief points.[cite:11][cite:15][cite:30]
- Secrets are strongest when the player can later reconstruct why the secret was there - the "good feeling" of exploration is often retrospective.[cite:33][cite:37]
- Overworld elements (roads, mountains, forests, rivers, bridges) work best with one consistent dominant semantic role each, so players form stable expectations.[cite:20][cite:34]
- A satisfying dungeon combines a clear main vector with limited optional branches and occasional loops reconnecting to known space; looping converts anxiety into mastery.[cite:33][cite:37][cite:38]

## Non-Goals

- Does not create, propose, or modify any `studio/design-patterns/` document.
- Does not analyze any specific map.
- Does not assert that any candidate schema listed here has passed `PATTERN_REVIEW_PROCESS.md` review or `PATTERN_CONFIDENCE_MODEL.md` corroboration.
- Does not modify `DDR-0005` or any `TheLastSwordProtocol-Atlas` canon.

## References

- `references/atlas_academy_jrpg_map_research.md` (Part 2, Part 3, Part 5, Part 6, Part 10 "Pattern rules," Module 8)
- `studio/design-patterns/PATTERN_SCHEMA.md`, `PATTERN_REVIEW_PROCESS.md`, `PATTERN_CONFIDENCE_MODEL.md`
- `academy/curriculum.md` (Level 4 - Propose)
- `reports/implementation-contracts/ashford-inn-pattern-aware-contract.md`, `reports/academy/composition-analysis-framework.md`
- `TheLastSwordProtocol-Atlas/atlas/docs/99_Reference/Decision_Records/DDR-0005_Ashford_Inn.md` (read-only reference, not modified)
- `reports/academy/knowledge-extraction-report.md`
- Created by `work-orders/WO-2006-atlas-academy-knowledge-extraction.md`
