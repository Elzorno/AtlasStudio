# Atlas Academy Grading Rubric (Foundation Level)

## Status

Foundation-level only. `WO-2005-map-grading-system.md` will define the full formal grading model (composition, traffic flow, readability, visual hierarchy, passability, environmental storytelling, project fit, RPG Maker quality, Dragon Quest exploration feel, overall recommendation) and its own `academy/grading-rubric.md`/`academy/grading-system.md`. This document is deliberately narrower: it states only what `work-orders/WO-2000-atlas-academy-foundation.md` itself requires - accepted-map rules and rejected-map rules - so that Atlas Academy has a working accept/reject vocabulary before the full grading model exists. When `WO-2005` is executed, it supersedes this file; it should reconcile against it explicitly rather than starting over, since this file's four-outcome vocabulary is not a placeholder to be discarded - it is `studio/operations/PLAYTEST_AND_ACCEPTANCE.md`'s own outcome vocabulary, reused here rather than replaced.

## Purpose

Before Atlas Academy can teach composition, metrics, or a formal grading model, it needs a settled answer to a simpler question: on what basis does a map case study count as "accepted" or "rejected" evidence at all? This document answers that question, grounded entirely in process that already exists, so `WO-2005`'s later, fuller rubric has a foundation to extend rather than a gap to fill retroactively.

## The Four Outcomes

Atlas Academy does not define a new outcome vocabulary. It reuses `studio/operations/PLAYTEST_AND_ACCEPTANCE.md`'s four outcomes exactly as that document defines them:

| Outcome | What it means for Atlas Academy |
|---|---|
| **Accepted** | Eligible as a positive reference case (Curriculum Level 2, `academy/curriculum.md`) once a human playtest pass is on file, per `PLAYTEST_AND_ACCEPTANCE.md`'s Required Evidence for this outcome. |
| **Accepted with Notes** | Eligible the same way as Accepted, and the notes themselves are read as Academy input - a bounded, specific issue that shipped anyway is informative in its own right, not noise to discard. |
| **Rejected** | Eligible as a negative reference case (Curriculum Level 3) only when the recorded reason is specific and falsifiable, per `PLAYTEST_AND_ACCEPTANCE.md`'s Required Evidence for this outcome - "a specific, recorded reason the work failed... not a general impression." `BUILD-0043`'s "NO GO for automatic final map construction... no meaningful visible runtime improvement" is the model. |
| **Deferred** | Not yet eligible either way. A deferred item is real and in-flight, not yet judged - Academy does not treat it as either a positive or negative case until it resolves to one of the other three outcomes. |

## Foundation-Level Acceptance Criteria (for a case study, not for the underlying build)

A case study itself - not the map it studies - is ready to file under `academy/reports/` (see that directory's `README.md`) when:

1. **The outcome is real and recorded**, not inferred. A map's `hand_authored` ownership state (`bridges/rpg-maker-mz/ownership-model.md`) means a human edited it, not that it was accepted - `PLAYTEST_AND_ACCEPTANCE.md` states this distinction directly, and this rubric restates it because it is the single most likely mistake a future case study could make.
2. **The reason, for a Rejected case, traces to a specific rule, layer, or missing pattern** - matching Curriculum Level 3's diagnostic standard (`academy/curriculum.md`), not a restatement of "the map didn't feel right."
3. **The pattern-derived comparison, for an Accepted case, states a held/exception verdict per rule** - matching Curriculum Level 2, not a blanket "the pattern worked."
4. **Every claim cites its source** - the build's own contract, the playtest/acceptance record, and (where applicable) the cited pattern document - per `PATTERN_EXTRACTION_GUIDE.md`'s "point, don't paraphrase" citation discipline, reused here rather than restated differently.
5. **Systemic findings are cross-filed**, not kept only inside the case study. A rejection or gap that reveals a repeated problem (a pattern, a tool, or a process producing bad results more than once) is also escalated to `studio/governance/production-readiness.md`'s backlog, per `academy/README.md`'s Rejected-Map Rules - a case study is not a substitute for that escalation.

## What This Rubric Deliberately Does Not Grade

This foundation-level rubric does not attempt composition quality, traffic flow, readability, visual hierarchy, passability scoring, environmental storytelling, project fit, RPG Maker production-quality comparison, or "Dragon Quest exploration feel." All of these are named directly in `WO-2005`'s brief and belong to the full grading model that work order will build. Grading them here would either duplicate `WO-2005`'s scope or foreclose decisions that work order should make with its own evidence - specifically, `bridges/rpg-maker-mz/map-quality-standard.md` already states a quality bar ("Would this be believable as a polished RPG Maker MZ sample map...") that a full grading rubric should operationalize, not this narrower document.

## References

- `studio/operations/PLAYTEST_AND_ACCEPTANCE.md` - the outcome vocabulary this rubric reuses, unchanged.
- `academy/curriculum.md` - Levels 2 and 3, which this rubric's eligibility criteria are drawn from.
- `academy/reports/README.md` - where a case study meeting this rubric's criteria is filed.
- `bridges/rpg-maker-mz/ownership-model.md`, `map-quality-standard.md`
- `rpgmakerLSP/reports/atlas-import/build-0043-guided-map-runtime-review.md`
- `work-orders/WO-2005-map-grading-system.md` - the future work order that supersedes and expands this document.
- Created by `work-orders/WO-2000-atlas-academy-foundation.md`
