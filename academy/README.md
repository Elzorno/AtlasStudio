# Atlas Academy

## Purpose

Atlas Academy is AtlasStudio's design-learning subsystem. It studies reference maps, accepted maps, and rejected maps so that future implementation contracts can draw on observed composition knowledge instead of relying only on prose descriptions.

AtlasStudio already has a Design Pattern Library (`studio/design-patterns/`) that extracts reusable craft rules from official RPG Maker sample maps, and a pattern-aware implementation contract format (`studio/contracts/`) that applies those rules to real builds. What has been missing is a standing place to (a) study reference material methodically before it becomes a pattern, and (b) turn what actually happened to a build - accepted or rejected - back into reusable lessons. Atlas Academy is that place. It does not replace the Pattern Library or the contract format; it feeds them and learns from their outcomes.

## Why This Exists Now

Two concrete precedents motivated this foundation, and both are cited throughout this document set rather than summarized away:

- **`BUILD-0043`** (`rpgmakerLSP/reports/atlas-import/build-0043-guided-map-runtime-review.md`) recorded a formal "NO GO for automatic final map construction" - a real rejected outcome that directly caused the shift to manual, guided map-building packets (`IMP-HOM-017` onward). This is exactly the kind of lesson Academy exists to preserve systematically instead of relying on one report being remembered.
- **`reports/implementation-contracts/ashford-inn-pattern-aware-contract.md`** found that no Specialization-tier pattern in the current library actually matches a single-room lodging interior - `inn.pattern.md`'s own Required Conditions call for a two-zone building, and `IMP-HOM-020`'s approved single-room design does not meet them. That gap was documented as an exception in the moment, but nothing currently captures it as a standing curriculum item for whoever extracts the next reference map. Academy exists to close gaps like this one deliberately, not leave them scattered across individual contracts.

## Structure

```text
academy/
  README.md                  - this file
  curriculum.md               - initial curriculum levels (this work order)
  grading-rubric.md           - foundation-level accepted/rejected criteria (this work order; superseded/expanded by WO-2005)
  references/
    README.md                 - reference source rules (this work order; governance detail owned by WO-2004)
    reference-governance.md    - WO-2004 reference governance
    source-classes.md          - WO-2004 source class rules
    gold-standard-maps.md      - WO-2004 gold-standard criteria
  reports/
    README.md                 - where Academy's case-study output lives (this work order)
  observation-model.md        - WO-2001 (not yet created)
  observations/                - WO-2001 (not yet created)
  composition-analysis.md     - WO-2002 (not yet created)
  composition-rubric.md       - WO-2002 (not yet created)
  compositions/                - WO-2002 (not yet created)
  metrics/                     - WO-2003 map metrics framework
  grading-system.md           - WO-2005 (not yet created)
```

This work order (`WO-2000`) creates only the files it lists as deliverables. The remaining paths above are named here so the foundation states its own shape honestly - a reader should be able to see where the rest of Atlas Academy will slot in without this document pretending those pieces already exist.

## Reference Source Rules

See `academy/references/README.md`. In summary: official RPG Maker MZ sample maps are the primary reference source today, following the same `PATTERN_EXTRACTION_GUIDE.md` discipline the Design Pattern Library already uses (objective observations kept separate from subjective ones, every claim traceable to a specific map file and, where possible, tile coordinates). AtlasStudio's own accepted builds become a second reference source over time, per `studio/design-patterns/README.md`'s own stated direction ("and, over time, from AtlasStudio's own accepted builds"). Full governance - source classes, provenance, confidence, allowed-use rules, and a gold-standard list - is `WO-2004`'s scope, not this foundation's.

## Accepted-Map Rules

Atlas Academy does not invent a new acceptance vocabulary. It reuses `studio/operations/PLAYTEST_AND_ACCEPTANCE.md`'s four existing outcomes - **Accepted**, **Accepted with Notes**, **Rejected**, **Deferred** - exactly as written, because that document already defines the required evidence and documentation for each, and a build's outcome should mean the same thing whether Academy is reading it or a Production Director is recording it at acceptance time.

For Academy's purposes specifically:

- A map reaching **Accepted** or **Accepted with Notes** is eligible to become a reference source once it has a human playtest pass on file, per that document's Required Evidence - not merely because its ownership state reached `hand_authored` (`bridges/rpg-maker-mz/ownership-model.md`'s `hand_authored` state means a human pass happened, not that it was accepted, exactly as `PLAYTEST_AND_ACCEPTANCE.md` itself already warns).
- Any notes attached to an "Accepted with Notes" outcome are read as Academy input in their own right - a bounded, specific issue that shipped anyway is exactly the kind of nuance a pure pass/fail record would lose.

## Rejected-Map Rules

- A **Rejected** outcome is read for its stated reason (`PLAYTEST_AND_ACCEPTANCE.md`'s Required Evidence: "a specific, recorded reason the work failed... not a general impression"), never for the artifact itself - Academy studies why a build failed, not the rejected map's geometry as if it were reference-quality data.
- `BUILD-0043` remains the model case: a specific, falsifiable verdict ("no meaningful visible runtime improvement" from automatic final map construction) rather than a vague impression. A rejection that cannot be stated this concretely is not yet ready to become an Academy lesson - route it back through `PLAYTEST_AND_ACCEPTANCE.md`'s Rejected-outcome documentation requirements first.
- A rejection that reveals a systemic issue (a pattern, a tool, or a process producing bad results repeatedly) is escalated the same way `PLAYTEST_AND_ACCEPTANCE.md` already requires - to `studio/governance/production-readiness.md`'s backlog - and is *also* recorded as an Academy case study. The two are not substitutes for each other.

## Relationship to Design Patterns

Atlas Academy does not modify `studio/design-patterns/`. It is upstream and downstream of the Pattern Library, never a peer editor of it:

- **Upstream:** reference-map study performed under Academy's curriculum produces the same kind of extraction-report evidence `PATTERN_EXTRACTION_GUIDE.md` already requires before a pattern can be proposed. Academy does not shortcut `PATTERN_REVIEW_PROCESS.md`'s proposal path - a curriculum exercise that finds new pattern-worthy evidence still becomes a pattern only through that existing process (schema completeness, extraction discipline, confidence accuracy, a work order naming the exact pattern file).
- **Downstream:** case studies of accepted and rejected builds test whether an already-cited pattern's rules actually held up in practice. The Ashford Inn contract's Required Conditions gap (see "Why This Exists Now") is exactly this kind of finding - it does not change `inn.pattern.md`, but it is exactly the sort of evidence a future `PATTERN_REVIEW_PROCESS.md` revision proposal for that pattern, or a new pattern for single-room lodging interiors, should cite.

## Relationship to Implementation Contracts

`studio/contracts/PATTERN_CONTRACT_SPEC.md`'s `Pattern Resolution` section already requires a contract to check a cited pattern's `Required Conditions` and document any exception explicitly rather than forcing or silently dropping a citation. Atlas Academy is where the accumulated record of those checks lives across many contracts, not just one. A future contract author facing the same "no pattern fits this shape" situation the Ashford Inn contract found should be able to check Academy's case studies first, rather than rediscovering the gap from scratch.

Academy does not gain any authority a pattern-aware contract does not already have. It does not override `Creative Authority` or an `Implementation Packet`, per `PATTERN_CONTRACT_SPEC.md`'s existing precedence rules - it is a record of what was learned, not a new authority layer inserted into contract resolution.

## Relationship to Playtest and Acceptance

Playtest and acceptance (`studio/operations/PLAYTEST_AND_ACCEPTANCE.md`, `DAILY_WORKFLOW.md` Steps 8-9) is where a build's outcome is decided and recorded. Atlas Academy consumes that decision - it never makes one. A map's Academy case study is written *from* its recorded Accepted/Rejected/Deferred outcome and evidence, after the fact; Academy has no acceptance authority of its own and does not gate a build's status.

## Initial Curriculum Levels

See `academy/curriculum.md` for the full statement. In summary, four levels, each grounded in a method or precedent that already exists in this project rather than invented fresh: Recognize (extraction against official samples, `PATTERN_EXTRACTION_GUIDE.md`), Compare (accepted AtlasStudio builds against their cited patterns), Diagnose (rejected builds and contract-level gaps, `BUILD-0043` and the Ashford Inn Required Conditions case), and Propose (routing findings into the existing `PATTERN_REVIEW_PROCESS.md` proposal path - Academy proposes, it does not self-approve).

## Non-Goals

- Atlas Academy does not modify `TheLastSwordProtocol-Atlas`, `TheLastSwordProtocol-Game`, or any existing Design Pattern document. This work order is documentation only.
- Atlas Academy does not create or edit any map.
- Atlas Academy does not replace `PATTERN_REVIEW_PROCESS.md`'s proposal, review, or acceptance path - it feeds evidence into that path.
- This foundation does not build the Observation Engine (`WO-2001`), the Composition Analysis Framework (`WO-2002`), the Map Metrics Framework (`WO-2003`), Reference Library Governance (`WO-2004`), or the Map Grading System (`WO-2005`). Each is named where this document set anticipates it, and none is built here.

## References

- `studio/design-patterns/README.md`, `PATTERN_EXTRACTION_GUIDE.md`, `PATTERN_REVIEW_PROCESS.md`, `PATTERN_SCHEMA.md`, `PATTERN_CONFIDENCE_MODEL.md`
- `studio/contracts/PATTERN_CONTRACT_SPEC.md`, `PATTERN_APPLICATION_CHECKLIST.md`
- `studio/operations/PLAYTEST_AND_ACCEPTANCE.md`, `DAILY_WORKFLOW.md`
- `bridges/rpg-maker-mz/ownership-model.md`
- `rpgmakerLSP/reports/atlas-import/build-0043-guided-map-runtime-review.md` (read-only, sibling repo)
- `reports/implementation-contracts/ashford-inn-pattern-aware-contract.md`
- `work-orders/WO-2001-academy-observation-engine.md`, `WO-2002-composition-analysis-framework.md`, `WO-2003-map-metrics-framework.md`, `WO-2004-reference-library-governance.md`, `WO-2005-map-grading-system.md`
- Created by `work-orders/WO-2000-atlas-academy-foundation.md`
