# Atlas Academy Map Study Template

## Status

Documentation only, per `work-orders/WO-2007-official-rpgmaker-corpus-study.md`. This is a reusable template for studying one official RPG Maker sample map at a time. It does not itself study any map; `academy/case-studies/official-map-001.md` is the first filled instance. It does not replace `schemas/academy-observation.schema.json` (`WO-2001`), `academy/composition-rubric.md` (`WO-2002`), `academy/map-metrics.md` (`WO-2003`), or `academy/grading-rubric.md` (`WO-2005`) - it sequences them into one document shape for a single-map study, the way `academy/curriculum.md` sequences existing methods rather than inventing new ones.

## How To Use This Template

1. Copy this file to `academy/case-studies/official-map-NNN.md`, using the next unused number.
2. Fill every section below using only evidence already on file (an existing extraction report, an existing Design Pattern's `Source`/`Observed Maps` section, or a prior Academy record) where one exists. Only perform new map inspection if no such evidence exists yet, and say so explicitly in "Evidence Basis" below.
3. Tag every claim `[Observed Fact]` or `[Inference]`, per `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`'s objective/subjective distinction and `academy/knowledge/observation-rules.md`'s worked example (`Counter blocks direct access to shelves` is fact; `Counter implies public-versus-private boundary` is inference).
4. Where a section cannot be filled from evidence on file, write `insufficient_evidence` and name what record would resolve it, per `academy/grading-system.md`'s "Grading Without Complete Evidence" discipline - do not guess.
5. This template studies exactly one map per file. Do not use it to summarize a corpus; `academy/reports/official-corpus-methodology.md` is where corpus-level generalization, if any, is discussed.

## Evidence Basis

State the source(s) this study draws from: an existing extraction report path, an existing Design Pattern's `observed_maps`, or (if neither exists) a note that this is a first-pass direct inspection, with the map JSON path and date.

## 1. Observation

Map identity (repo, file path, map tree name, tileset, dimensions), door/threshold placement, spawn position (labeled inferred if it is), and a plain-language walkthrough of the space, per `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md` and `academy/observation-model.md`.

## 2. Composition

Apply `academy/composition-analysis.md`'s ten topics (focal point, negative space, traffic flow, sight lines, furniture grouping, room zones, entry readability, visual hierarchy, decoration balance, environmental storytelling) at whatever depth the evidence supports. Cite `academy/composition-rubric.md`'s Holds/Gap/N/A verdict per topic where applicable.

## 3. Traffic Flow

Where the player is expected to walk: entrance to focal point, browse loop, return to exit. Cite `academy/map-metrics.md`'s Traversal group (`average_aisle_width`, `door_to_focal_point_distance`) if a value can be derived from evidence on file; otherwise `insufficient_evidence`.

## 4. Negative Space

What open floor exists, and whether it corresponds to a movement path (per `academy/knowledge/composition-rules.md`'s Research Hypothesis entry on negative space as an active tool, not filler) or is unaccounted-for dead space.

## 5. Landmarks

Memorable, re-orientable elements: a focal display, an animated decorative event, a floor accent, a distinctive wall feature. Per `academy/knowledge/observation-rules.md`'s Research Hypothesis on cognitive mapping, name what a player would use to reacquire orientation.

## 6. Passability

Reachable set, blocked set, reachability-ring check per interactable/display object, and transfer event inventory, per `bridges/rpg-maker-mz/passability-rule.md`. State plainly whether this was verified against actual map data or inferred from a written description.

## 7. Environmental Storytelling

Apply the four silent questions from `references/atlas_academy_jrpg_map_research.md` Part 7 (also `academy/composition-analysis.md` Topic 10): what happens here, who controls it, what is allowed here, what changed recently.

## 8. Metrics

Any values computable from evidence already on file, per `academy/map-metrics.md`'s groups (Geometry, Traversal, Events And Interaction, Composition Inputs, RPG Maker Production Health). Mark every derived value with its basis (exact count from source data, or approximation from a partial/described set) and set `method.is_heuristic: true` in spirit (state it in prose; this template does not require filing a formal metrics record) whenever the value is not a full, direct recount.

## 9. Lessons Learned

What this map teaches that is reusable beyond itself - cross-reference against any existing Design Pattern already derived from this map (state its `pattern_id` and confidence), and note whether this study corroborates, refines, or is neutral toward that pattern's existing rules. Does not itself propose a pattern change; that is Level 4 (Propose) work per `academy/curriculum.md`.

## Non-Goals

- Does not implement anything.
- Does not extract or propose a Design Pattern - see `academy/curriculum.md` Level 4 for that separate step.
- Does not generate a map.
- Does not modify `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game`.

## References

- `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`
- `academy/observation-model.md`, `composition-analysis.md`, `composition-rubric.md`, `map-metrics.md`, `grading-system.md`, `curriculum.md`
- `academy/knowledge/observation-rules.md`, `composition-rules.md`, `validation-rules.md`
- `bridges/rpg-maker-mz/passability-rule.md`, `map-quality-standard.md`
- `references/atlas_academy_jrpg_map_research.md`
- `academy/case-studies/official-map-001.md` (first filled instance)
- Created by `work-orders/WO-2007-official-rpgmaker-corpus-study.md`
