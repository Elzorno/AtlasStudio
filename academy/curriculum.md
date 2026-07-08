# Atlas Academy Curriculum

## Purpose

This document defines Atlas Academy's initial curriculum: the levels a map study or case study passes through, from raw reference material to a proposal the Design Pattern Library can actually accept. Each level is grounded in a method or precedent that already exists in this project - the curriculum sequences existing discipline, it does not invent a new one.

## Level 1 - Recognize

**Goal:** produce a factual, reproducible extraction from a reference map.

**Method:** `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`, applied exactly as written - dimensions, door/threshold placement, spawn position (labeled inferred if it is), structural object placement, walkable tiles, interaction distances, NPC placement, dead space, tile usage, event and transfer inventory. Objective observations (directly verifiable from map JSON and tileset data) are kept separate from subjective ones (interpretive judgments grounded in the objective data), per that guide's own distinction.

**Precedent:** `reports/map-analysis/item-shop-analysis.md` (`TheLastSwordProtocol-Game`) and `reports/design-patterns/interior-pattern-corpus-review.md` (`WO-0025`, eight official sample interiors) are both Level 1 work already performed under this exact method, before Atlas Academy existed to name it.

**Output:** an extraction report, not a pattern document - see `PATTERN_EXTRACTION_GUIDE.md`, "Output of an Extraction Pass." Once the Observation Engine (`WO-2001`) exists, Level 1 work should also produce a structured observation record per its schema; until then, the extraction report itself is the Level 1 artifact.

**Exit condition:** a second person or agent, given the same source map, would record the same objective facts. If they would not, the extraction is not yet done.

## Level 2 - Compare

**Goal:** check whether an already-cited pattern's rules actually held up against a real, accepted AtlasStudio build.

**Method:** take a build that reached **Accepted** or **Accepted with Notes** (`studio/operations/PLAYTEST_AND_ACCEPTANCE.md`) and its governing implementation contract's cited pattern layer(s) (`studio/contracts/PATTERN_CONTRACT_SPEC.md` Sections 5-8). Compare what the pattern required against what was actually built and accepted. Confirmation is itself a useful, recordable outcome, not just contradiction.

**Precedent:** none yet exists as a formal Level 2 case study, because Ashford Village's own maps (`Map001`, `Map002`) are `hand_authored` but not yet playtest-certified (`reports/production-review/ashford-shop-production-review.md` and `studio/governance/production-readiness.md` both note this gap directly). This is itself a Level 2 curriculum entry point once that certification lands - do not backfill a Level 2 case study against an uncertified build.

**Output:** a short comparison note - which pattern-derived rules held, which needed a documented exception (matching `PATTERN_CONTRACT_SPEC.md`'s own "Exceptions" discipline), and whether the exception should become a pattern revision proposal (routes to Level 4) or was a legitimate one-off.

**Exit condition:** every rule the citing contract pulled from a pattern layer has a stated held/exception verdict - none left unexamined.

## Level 3 - Diagnose

**Goal:** turn a rejected build, or a documented contract-level gap, into a specific, falsifiable finding - not a general impression.

**Method:** read the build's or contract's own recorded reason, per `PLAYTEST_AND_ACCEPTANCE.md`'s Rejected-outcome Required Evidence ("a specific, recorded reason the work failed... not a general impression"). Trace the reason to a specific rule, layer, or missing pattern, the way `academy/README.md`'s "Why This Exists Now" section already does for two real cases.

**Precedent, both already real:**

- `BUILD-0043` (`rpgmakerLSP/reports/atlas-import/build-0043-guided-map-runtime-review.md`): a rejected outcome with a stated, falsifiable verdict ("NO GO for automatic final map construction... no meaningful visible runtime improvement"), which directly caused the shift to manual, guided map-building packets. This is the model of what a Level 3 finding should look like: specific enough to change future practice, not just note that "something felt off."
- `reports/implementation-contracts/ashford-inn-pattern-aware-contract.md`'s Required Conditions finding: not a rejected build (nothing has been built yet), but a documented contract-level gap of the same diagnostic shape - a specific, falsifiable claim ("no Specialization-tier pattern in the current library matches a single-room lodging interior") traced to an exact rule (`inn.pattern.md`'s Required Conditions) rather than a vague sense that the pattern "didn't quite fit."

**Output:** a diagnosis - the specific failure or gap, the rule or layer it traces to, and whether it is a one-off (stays local to the case study) or systemic (escalates to `studio/governance/production-readiness.md`'s backlog, per `academy/README.md`'s Rejected-Map Rules).

**Exit condition:** the finding could be falsified by a second reviewer checking the same evidence - "the counter placement felt cramped" is not a Level 3 diagnosis; "the counter's interaction side has zero adjacent walkable tiles, per the map's own passability data" is.

## Level 4 - Propose

**Goal:** turn an accumulated Level 1-3 finding into an actual proposal, routed through the Design Pattern Library's existing, unchanged review path.

**Method:** `studio/design-patterns/PATTERN_REVIEW_PROCESS.md`'s existing "How Patterns Are Proposed" section, unchanged by Atlas Academy. A Level 4 proposal is either extraction-driven (a Level 1 report's "Reusable Design Rules" section becomes a new or revised pattern document, per `PATTERN_SCHEMA.md`) or project-preference-driven (a Production Director decision, filed at `confidence: low`). Either way, the proposal is filed under its own work order, exactly as `PATTERN_REVIEW_PROCESS.md` already requires - Atlas Academy does not add a second, parallel approval mechanism.

**Precedent:** every pattern currently in `studio/design-patterns/interiors/` was proposed this way already; Atlas Academy names the step, it does not change it.

**Worked example, not yet executed:** the Ashford Inn Required Conditions gap (Level 3, above) is a live candidate for a Level 4 proposal - either a narrower `inn.pattern.md` revision that acknowledges a single-room variant, or a new pattern for single-room lodging interiors once a second reference source exists to corroborate it (`studio/design-patterns/PATTERN_CONFIDENCE_MODEL.md`'s two-source bar for anything above Medium). This curriculum does not propose it here - that is a future work order's job, not this foundation's.

**Exit condition:** a pattern document reaches `status: proposed` under `PATTERN_REVIEW_PROCESS.md`'s existing three-check review (schema completeness, extraction discipline, confidence accuracy). Atlas Academy's own role ends there; acceptance remains the Pattern Library's, per that document's "How Patterns Are Accepted."

## How the Levels Relate

```text
Level 1 (Recognize)  -> extraction report, objective + labeled subjective observations
Level 2 (Compare)     -> held/exception verdict per pattern-derived rule, against an accepted build
Level 3 (Diagnose)    -> specific, falsifiable finding, from a rejected build or a documented contract gap
Level 4 (Propose)     -> routed into PATTERN_REVIEW_PROCESS.md's existing, unchanged proposal path
```

A case study does not have to pass through all four levels. A Level 1 extraction of a new official sample map is complete and useful on its own. A Level 3 diagnosis of a rejected build is a full curriculum item even if no Level 4 proposal follows immediately - `BUILD-0043` sat as a Level 3-shaped finding for real production time before its consequences (the manual map-building packet series) were fully realized.

## Future Curriculum Work

- Level 2's comparison method should be revisited once the Composition Analysis Framework (`WO-2002`) and Map Metrics Framework (`WO-2003`) exist, since both will give Level 2 comparisons quantifiable measurements to check pattern-derived rules against, not just qualitative agreement.
- The full grading model referenced informally throughout this curriculum (composition, traffic flow, readability, passability, and so on) is `WO-2005`'s scope. `academy/grading-rubric.md` (this work order) states only the foundation-level Accepted/Rejected criteria this curriculum needs today.

## References

- `academy/README.md`
- `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`, `PATTERN_REVIEW_PROCESS.md`, `PATTERN_SCHEMA.md`, `PATTERN_CONFIDENCE_MODEL.md`
- `studio/contracts/PATTERN_CONTRACT_SPEC.md`
- `studio/operations/PLAYTEST_AND_ACCEPTANCE.md`
- `reports/map-analysis/item-shop-analysis.md` (`TheLastSwordProtocol-Game`), `reports/design-patterns/interior-pattern-corpus-review.md`
- `rpgmakerLSP/reports/atlas-import/build-0043-guided-map-runtime-review.md`
- `reports/implementation-contracts/ashford-inn-pattern-aware-contract.md`
- Created by `work-orders/WO-2000-atlas-academy-foundation.md`
