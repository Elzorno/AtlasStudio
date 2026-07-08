# Atlas Academy Knowledge Extraction - Evidence Report

Status: submitted

Scope: `WO-2006`. Documents how `references/atlas_academy_jrpg_map_research.md` was converted into `academy/knowledge/observation-rules.md`, `composition-rules.md`, `pattern-rules.md`, `validation-rules.md`, and `teaching-lessons.md`. This report is process documentation, not a new analysis pass - it does not analyze any map, create an implementation contract, or create a Design Pattern.

## Why a Five-Category Taxonomy, Not the Source's Own Four

`references/atlas_academy_jrpg_map_research.md` itself distinguishes Observed Fact, Expert Opinion, Community Practice (discussed as its own section, "Community best practices versus official guidance," rather than tagged inline like the other three), and Research Hypothesis. `work-orders/WO-2006` requires a fifth: **Atlas Interpretation**. That category is not present in the source report at all - it is new material added during extraction, specifically the act of connecting a research claim to an existing AtlasStudio artifact (a pattern document, a schema, `academy/curriculum.md`, `academy/grading-system.md`, and so on). Every "Atlas Interpretation" entry across the five knowledge files is a reconciliation or correspondence statement, never a restatement of the source dressed up as project authority. Keeping it as a separate, fifth category - rather than folding it into "Research Hypothesis" - makes it possible to tell, for any claim, whether the interpretive step came from the source researcher or from this extraction pass.

## Coverage Check

All five required deliverables under `academy/knowledge/` were produced, plus this report. Each source Part was routed to at least one knowledge file:

| Source material | Knowledge file(s) |
|---|---|
| Part 1 (Design philosophy, psychological principles) | `observation-rules.md` |
| Part 2 (Official RPG Maker patterns) | `pattern-rules.md` |
| Part 3 (Dragon Quest patterns) | `pattern-rules.md` |
| Part 4 (Composition) | `composition-rules.md` |
| Part 5 (Overworld design) | `pattern-rules.md` |
| Part 6 (Dungeon design) | `pattern-rules.md` |
| Part 7 (Environmental storytelling) | `observation-rules.md` (cited fact), `composition-rules.md` (Topic 10 correspondence) |
| Part 8 (Metrics) | `validation-rules.md` |
| Part 9 (Design anti-patterns) | `validation-rules.md` |
| Part 10 (Teaching Atlas Academy: observation/composition/pattern/validation rules, grading rubrics, implementation guidance, confidence levels) | Split across all five files by sub-section |
| Community best practices vs. official guidance | `composition-rules.md`, `validation-rules.md` (as a caution, not a rule) |
| Architecture and real-world planning | Not separately routed - its content (public/private zoning, circulation efficiency) duplicates ground already covered by `composition-rules.md`'s room-zoning correspondence and did not add a distinct extractable rule beyond what was already captured. |
| Assumptions, biases, alternative viewpoints | Not separately routed - this section is the source's own self-critique of its assumptions, not source material to extract as a rule. It is referenced qualitatively in `teaching-lessons.md`'s confidence-tier discussion. |
| Curriculum for Atlas Academy (ten modules) | `teaching-lessons.md`, reconciled against `academy/curriculum.md`'s existing four levels rather than adopted as a parallel curriculum |
| Closing synthesis | `teaching-lessons.md`, tagged Research Hypothesis |

## Key Reconciliation Decisions

Three places in the source material could have been adopted as new Atlas Academy structure. Each was instead reconciled against something that already exists, following the same discipline `academy/grading-system.md` (`WO-2005`) already established for outcomes:

1. **The five-axis grading rubric (Part 10)** was already reconciled once, in `WO-2005` - `academy/grading-system.md` states directly that its nine categories are adapted from this same report. `validation-rules.md` records the correspondence table rather than re-deriving it.
2. **The ten-module curriculum ("Curriculum for Atlas Academy")** is reconciled against `academy/curriculum.md`'s existing four levels (Recognize, Compare, Diagnose, Propose) in `teaching-lessons.md`, module-by-module, rather than stood up as a second curriculum.
3. **The four candidate exploration-structure schemas (Part 10 "Pattern rules")** are recorded in `pattern-rules.md` as candidates for a future Level 4 (Propose) work order, explicitly not as accepted Design Patterns - nothing in this work order has been through `PATTERN_REVIEW_PROCESS.md`'s review.

## What This Extraction Does Not Do

Per `work-orders/WO-2006`'s own stated scope: it does not analyze any map, does not create an implementation contract, and does not create a Design Pattern. Two gaps surfaced honestly during extraction (no overworld or dungeon Specialization-tier pattern exists yet in `studio/design-patterns/`, per `teaching-lessons.md`'s module 4/5 correspondence row) are recorded as findings, not acted on - resolving them is later work, per the same document's own "Those come later" framing.

## Constraints Observed

- Documentation only - no code, no map, no implementation contract, no Design Pattern.
- No file under `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` was modified. `DDR-0005` was cited read-only.
- No existing Design Pattern document was modified.
- `academy/curriculum.md`, `academy/composition-analysis.md`, `academy/map-metrics.md`, `academy/grading-system.md`, and `academy/grading-rubric.md` were read as reconciliation targets and cited, not modified.
- Preserved the Immutable Formatting Rule.

## Verification Performed

```bash
find academy/knowledge -type f
grep -rl "Atlas Interpretation" academy/knowledge/
```

## References

- `references/atlas_academy_jrpg_map_research.md`
- `academy/knowledge/observation-rules.md`, `composition-rules.md`, `pattern-rules.md`, `validation-rules.md`, `teaching-lessons.md`
- `academy/curriculum.md`, `composition-analysis.md`, `map-metrics.md`, `grading-system.md`, `grading-rubric.md`
- `academy/references/reference-governance.md`, `source-classes.md`
- Created by `work-orders/WO-2006-atlas-academy-knowledge-extraction.md`
