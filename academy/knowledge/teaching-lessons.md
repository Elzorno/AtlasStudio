# Atlas Academy Knowledge: Teaching Lessons

## Status

Documentation only, per `work-orders/WO-2006-atlas-academy-knowledge-extraction.md`. This file converts `references/atlas_academy_jrpg_map_research.md`'s "Curriculum for Atlas Academy" (ten modules), "Part 10: Teaching Atlas Academy" (implementation guidance, confidence levels), and its closing synthesis into reusable Atlas Academy knowledge. It does not modify `academy/curriculum.md` (`WO-2000`), which remains the single governing curriculum for Atlas Academy case-study work.

## A Reconciliation, Not a Second Curriculum

The source report proposes its own ten-module lesson sequence (Reading maps; Readability and wayfinding; Purposeful composition; Overworld pacing; Dungeon structure; Environmental storytelling; Metrics and validation; Pattern abstraction; Controlled rule-breaking; Critique before construction). `academy/curriculum.md` already defines Atlas Academy's actual curriculum as four levels - Recognize, Compare, Diagnose, Propose - each grounded in an existing project method (`PATTERN_EXTRACTION_GUIDE.md`, `PLAYTEST_AND_ACCEPTANCE.md`, `PATTERN_REVIEW_PROCESS.md`). Introducing the report's ten modules as a second, parallel curriculum would fracture that existing structure the same way `academy/grading-system.md` (`WO-2005`) explicitly declined to fracture `PLAYTEST_AND_ACCEPTANCE.md`'s outcome vocabulary. This file reconciles instead: the ten modules are recorded as **topic content** that belongs inside the four existing levels, not as competing levels of their own.

## Observed Fact

- The report states its own goal directly: "the central lesson is not to imitate historic layouts but to teach agents how to read spatial intent," so that an agent can explain why a map is legible, curious, fair, atmospheric, and mechanically coherent before it critiques or builds.[cite:16][cite:30][cite:46][cite:49]
- Module 8 explicitly forbids pattern descriptions that reveal copyrighted layouts or one-to-one reconstruction.[cite:20][cite:30][cite:33]

## Expert Opinion

- The report's stated confidence tiers are themselves an expert-opinion-adjacent judgment about its own material: high confidence for compactness, purposeful furnishing, readability, landmark utility, and simplified-over-realistic map logic; medium confidence for the quantitative target bands and cross-series Dragon Quest synthesis; lower confidence for genre-wide claims about all JRPG towns or all community best practices.[cite:11][cite:15][cite:16][cite:20][cite:21][cite:26][cite:30][cite:33][cite:34][cite:37][cite:38][cite:46] This confidence structure corresponds to, and does not replace, `studio/design-patterns/PATTERN_CONFIDENCE_MODEL.md`'s existing confidence tiers - a future citation of this report should carry its own stated tier per claim, exactly as `academy/composition-analysis.md` and `academy/grading-system.md` already do.

## Community Practice

- Not separately represented in the module/curriculum material beyond what is already recorded in `academy/knowledge/composition-rules.md` and `validation-rules.md`. No community-practice teaching claim is asserted here beyond that existing record.

## Atlas Interpretation

- Correspondence table, module to existing curriculum level:

| Report module | `academy/curriculum.md` level | Notes |
|---|---|---|
| Module 1: Reading maps | Level 1 - Recognize | Direct match: both require distinguishing observed fact from inference before conclusions.[cite:16][cite:20][cite:46] |
| Module 2: Readability and wayfinding | Level 1 - Recognize (extended by Level 3 - Diagnose when a finding is falsifiable) | Wayfinding critique starts as observation; becomes a Level 3 finding only when specific and falsifiable, per Level 3's own exit condition. |
| Module 3: Purposeful composition | Level 1 - Recognize / `academy/composition-analysis.md` | Content-level match to the existing composition framework (`WO-2002`), not a new level. |
| Module 4: Overworld pacing | Level 1 - Recognize (topic content); candidate Level 4 (Propose) material if a reusable schema is later extracted | No overworld-specific Design Pattern exists yet in `studio/design-patterns/`; this module names a gap, not a ready proposal. |
| Module 5: Dungeon structure | Same as Module 4 | No dungeon-specific pattern layer exists yet either; same gap. |
| Module 6: Environmental storytelling | Level 1 - Recognize / `academy/composition-analysis.md` Topic 10 | Direct match to an existing composition topic. |
| Module 7: Metrics and validation | Level 2 - Compare, using `academy/map-metrics.md` | Matches the point in `academy/curriculum.md`'s own "Future Curriculum Work" section stating Level 2 should be revisited once `WO-2002`/`WO-2003` exist to give it quantifiable measurements - which they now do. |
| Module 8: Pattern abstraction | Level 4 - Propose | Direct match: both route through `PATTERN_REVIEW_PROCESS.md`'s existing proposal path, not a new one. |
| Module 9: Controlled rule-breaking | Level 3 - Diagnose / Level 4 - Propose | A documented exception (per `PATTERN_CONTRACT_SPEC.md`'s "Exceptions" discipline, already used in `reports/implementation-contracts/ashford-inn-pattern-aware-contract.md`) is this module's real project precedent. |
| Module 10: Critique before construction | The relationship between Level 1-3 and Level 4 as a whole | `academy/curriculum.md` already states this exact ordering: "A case study does not have to pass through all four levels," but Level 4 always follows, never precedes, grounded observation. |

- The report's "Implementation guidance" three-pass structure (structural critique; experiential critique; implementation critique)[cite:17][cite:20][cite:37][cite:46] is recorded here as a description of what happens *inside* Level 1-3 work, not as a fifth level or a required new process. No work order has adopted it as a mandatory sequence; a future Academy work order could formalize it against `academy/curriculum.md`'s existing levels if useful, but that adoption is out of this documentation-only work order's scope.
- Two report modules (4: Overworld pacing, 5: Dungeon structure) name a real, honest gap: `studio/design-patterns/` currently has no overworld or dungeon Specialization-tier patterns to compare against, unlike interiors (which already have `inn.pattern.md`, `house.pattern.md`, `shop.pattern.md`, `bar.pattern.md`, `chief-house.pattern.md`). This is recorded as a finding for `studio/governance/production-readiness.md`'s backlog consideration, not resolved here.

## Research Hypothesis

- The report's central closing claim - that classic JRPG maps feel good because they are readable, compressive, emotionally paced spaces that simplify architecture and geography into memorable landmarks, purposeful routes, and reward-bearing detours - is offered as a synthesis conclusion, not a single sourced fact, and is recorded here at that tier.[cite:20][cite:30][cite:33][cite:34][cite:46]

## Non-Goals

- Does not modify `academy/curriculum.md`.
- Does not introduce a second, competing Atlas Academy curriculum.
- Does not adopt the three-pass implementation-guidance structure as a required process.
- Does not propose a new Design Pattern for overworld or dungeon map types.

## References

- `references/atlas_academy_jrpg_map_research.md` ("Curriculum for Atlas Academy," Part 10, closing synthesis)
- `academy/curriculum.md`
- `studio/design-patterns/PATTERN_CONFIDENCE_MODEL.md`, `PATTERN_REVIEW_PROCESS.md`
- `studio/contracts/PATTERN_CONTRACT_SPEC.md`
- `reports/implementation-contracts/ashford-inn-pattern-aware-contract.md`
- `studio/governance/production-readiness.md`
- `reports/academy/knowledge-extraction-report.md`
- Created by `work-orders/WO-2006-atlas-academy-knowledge-extraction.md`
