# Official RPG Maker Corpus Methodology - Evidence Report

Status: submitted

Scope: `WO-2007`. Documents the methodology established by studying exactly one official RPG Maker sample map (`academy/case-studies/official-map-001.md`, Map021 "Item Shop") using `academy/templates/map-study-template.md`. Per this work order's own constraint, only one map was studied; this report does not analyze the remaining corpus, and does not extract or propose a Design Pattern.

## Why Map021 ("Item Shop") Was Chosen

`work-orders/WO-2007` names no specific map, only "exactly one official map." Map021 was selected because it is the single most thoroughly and independently documented official sample already on file in this project: it has its own dedicated extraction report (`TheLastSwordProtocol-Game/reports/map-analysis/item-shop-analysis.md`, predating Atlas Academy), a Design Pattern derived directly from it (`shop.pattern.md`, `WO-0024`), and a worked observation-record example built from the same facts (`academy/observation-model.md`'s `OBS-ITEMSHOP-001`, `WO-2001`). Choosing the best-documented map lets this work order test the template against real, already-verified evidence and expose gaps in the template itself, rather than conflating template design with first-pass map inspection. A future application of this template to a less-documented map (for example the seven interiors covered only by `reports/design-patterns/interior-pattern-corpus-review.md`'s corpus-level pass, which has no per-map extraction report of its own) would need to state that in "Evidence Basis" and perform more first-pass inspection accordingly.

## The Methodology, As It Actually Worked

1. **Check for existing evidence before inspecting anything new.** Map021 already had a full extraction report and a derived pattern; the case study reused both rather than re-deriving facts. This produced a study built almost entirely from citation and structured re-application, with only a handful of light coordinate-arithmetic inferences (aisle width ranges, approximate distances) added on top.
2. **Tag every claim's evidentiary status inline** (`[Observed Fact]` / `[Inference]`), per `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`'s existing objective/subjective distinction - not a new tagging scheme invented for this work order.
3. **Route composition claims through `academy/composition-rubric.md`'s existing Holds/Gap/N/A form**, rather than inventing a new composition checklist for case studies specifically.
4. **Compute metrics only from evidence already on file, and flag every non-exact value as heuristic in prose**, per `academy/map-metrics.md`'s Source Discipline. Several metrics (decoration density, room utilization) came back `insufficient_evidence` rather than a guessed number - the source report describes them qualitatively but not numerically, and this study did not perform new inspection to fill that gap, consistent with this work order's documentation-only constraint.
5. **State plainly when a template section is close to circular.** The Composition section (Section 2) checks Map021 against `shop.pattern.md`, a pattern derived from that same map - every topic reads "Holds" by near-construction. The case study says this directly rather than presenting the result as independent validation. This is itself a methodology finding: a single-map study of a map that already has a derived pattern cannot corroborate that pattern's confidence tier (see `PATTERN_CONFIDENCE_MODEL.md`'s two-source bar); it can only confirm internal consistency between the map and the pattern's own stated rules.

## What the Template Needed That Didn't Already Exist

Two of the required nine sections (Traffic Flow, Landmarks) had no single existing Academy document they could cite wholesale - Traffic Flow partially overlaps `academy/composition-analysis.md` Topic 3 and `academy/map-metrics.md`'s Traversal group, and Landmarks partially overlaps Topic 1 (Focal Point) and the observation-rules knowledge file's cognitive-mapping material, but neither is a clean one-to-one match. The template routes both sections to their nearest existing anchors rather than declaring either a wholly new category, consistent with this series' standing discipline against introducing parallel structures where a partial match to something existing is available.

## Generalizing to the Rest of the Corpus (Not Performed Here)

Per `WO-2007`'s explicit constraint, the remaining seven official interiors already covered by `reports/design-patterns/interior-pattern-corpus-review.md` (House 1, House 2, Inn, Weapon & Armor Shop, Bar, Chief's House 1F, Chief's House 2F) were **not** studied individually here. Applying this same template to each would be more first-pass work than Map021's study required, because none of the seven has a per-map extraction report of its own - only the corpus-level review. A future work order applying the template corpus-wide should expect each individual study to need more original inspection (or, at minimum, a closer re-reading of the corpus review's per-map findings) than this first study did, and should budget accordingly rather than assuming Map021's speed generalizes.

## Constraints Observed

- Documentation only - no implementation, no pattern extraction, no map generation.
- Exactly one map was studied (Map021), per the work order's explicit constraint against analyzing the full corpus.
- No file under `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` was modified; `item-shop-analysis.md` was read only.
- No existing Design Pattern was created or modified.
- Preserved the Immutable Formatting Rule.

## References

- `academy/templates/map-study-template.md`
- `academy/case-studies/official-map-001.md`
- `TheLastSwordProtocol-Game/reports/map-analysis/item-shop-analysis.md` (read-only)
- `studio/design-patterns/interiors/shop.pattern.md`
- `reports/design-patterns/interior-pattern-corpus-review.md`
- `academy/composition-analysis.md`, `composition-rubric.md`, `map-metrics.md`, `observation-model.md`
- `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`, `PATTERN_CONFIDENCE_MODEL.md`
- Created by `work-orders/WO-2007-official-rpgmaker-corpus-study.md`
