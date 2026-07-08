# Atlas Academy Reference Governance

## Status

Documentation and schema only, per `work-orders/WO-2004-reference-library-governance.md`. This document governs how Atlas Academy classifies and uses reference sources. It does not collect external maps, copy assets, modify Atlas canon, modify `TheLastSwordProtocol-Game`, or create maps.

## Purpose

Atlas Academy studies references so implementation contracts and pattern proposals can learn from real examples. Not every source carries the same authority. A polished official sample, a locally accepted project map, a rejected build, and a comparative JRPG screenshot can all teach different things, but they must not be mixed as if they had the same provenance, licensing posture, or confidence contribution.

This governance layer answers four questions:

1. What kind of source is this?
2. How was it approved for Academy use?
3. What may it influence?
4. How must it be cited?

## Governed Source Classes

See `academy/references/source-classes.md` for the full class table. The governed source classes are:

- `official_rpg_maker_sample`
- `approved_project_map`
- `rejected_project_map`
- `design_reference`
- `comparative_jrpg_reference`

These map to `WO-2004`'s requested classes: official RPG Maker sample maps, approved project maps, rejected project maps, design references, and comparative JRPG references.

## Approval Status

Every reference source record uses one of these approval statuses:

| Status | Meaning | Allowed influence |
|---|---|---|
| `candidate` | Captured for possible Academy use, not yet reviewed. | May be cited only as unreviewed evidence. Must not influence implementation contracts. |
| `approved` | Reviewed and allowed for its stated source class and allowed uses. | May influence the documents named in its `allowed_uses`. |
| `gold_standard` | Approved and meets `academy/references/gold-standard-maps.md` criteria. | May be used as high-weight comparison evidence for its declared scope. |
| `diagnostic_only` | Approved only as a lesson about failure, not as a positive model. | May influence rejection analysis and process/pattern gap reports. Must not be used as a positive design target. |
| `deprecated` | Was once usable but has been superseded or invalidated. | May be cited historically, not as current guidance. |
| `rejected` | Reviewed and rejected as an Academy source. | Must not influence Academy analysis except as a record of why it was rejected. |

Approval status is not a playtest outcome. A project map can have a Production Director outcome such as **Accepted** or **Rejected** under `studio/operations/PLAYTEST_AND_ACCEPTANCE.md`; its Academy reference approval says how Academy may use that outcome afterward.

## Confidence Contribution

Reference records state how much confidence they may contribute:

| Contribution | Meaning |
|---|---|
| `high` | Strong source for its stated scope. Usually an official sample with clear provenance, or a project map accepted with a playtest/acceptance record and stable contract linkage. |
| `medium` | Useful corroborating source, but with limits such as single-source evidence, partial acceptance notes, or project-specific constraints. |
| `low` | Useful context or diagnostic evidence only. Requires human interpretation before it can influence a pattern or contract. |
| `none` | Historical, rejected, deprecated, or illustrative-only source. Carries no positive confidence weight. |

Confidence contribution is scoped. A source may be high-confidence for "single-room shop counter composition" and irrelevant for "overworld route readability." The schema captures this with `scope`.

## Licensing And Copy Rules

Atlas Academy may cite and analyze references, but it must not copy external maps or assets into this repository unless a later work order explicitly authorizes and verifies that action.

Rules:

- Official RPG Maker sample maps may be studied as references, following existing `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md` practice, but the map files themselves are not copied into AtlasStudio.
- `TheLastSwordProtocol-Game` project maps may be cited by path and commit/provenance reference, but `WO-2004` does not authorize edits to that repo.
- External design or comparative JRPG references must use citation metadata, short notes, and optionally links. Do not copy proprietary map data, screenshots, or assets into the repo unless licensing has been separately cleared.
- A reference record must include `licensing.notes` and `licensing.asset_copy_allowed`. For this work order's default posture, `asset_copy_allowed` should be `false`.

## Citation Rules

Every reference citation must include:

- source class
- source title or map name
- repository or external source
- file path or URL
- provenance reference, such as commit, tag, release, date, or source version
- approval status
- allowed uses
- licensing notes

For map-data claims, cite exact files and, where possible, coordinates, event IDs, layers, or observation IDs. This keeps reference governance aligned with `academy/observation-model.md` and `PATTERN_EXTRACTION_GUIDE.md`.

## Accepted Versus Rejected Project Maps

Approved project maps and rejected project maps are both useful, but never in the same way.

### Approved Project Maps

An approved project map can become positive reference evidence only when:

- it has a recorded **Accepted** or **Accepted with Notes** outcome under `PLAYTEST_AND_ACCEPTANCE.md`;
- the source file and provenance are stable enough to cite;
- its implementation contract or work order is identified;
- any acceptance notes are preserved as caveats.

`hand_authored` ownership alone is not acceptance. It only proves a human-edited/protected state in the ownership model.

### Rejected Project Maps

A rejected project map can become `diagnostic_only` evidence only when:

- the rejection reason is specific and recorded;
- the failed artifact is not treated as a positive model;
- the record states what it may teach, such as "avoid this tile-classification method" or "automatic map construction failed to improve visible layout quality";
- any systemic issue is cross-filed through the appropriate governance or production-readiness path.

Rejected maps may influence implementation contracts only as warnings or non-goals. They must not define target layouts.

## When References Can Influence Implementation Contracts

A reference source may influence a pattern-aware implementation contract only when all of these are true:

1. Its approval status is `approved`, `gold_standard`, or `diagnostic_only`.
2. Its `allowed_uses` includes `implementation_contract`.
3. Its source class and scope match the contract question.
4. It does not contradict Creative Authority, the Implementation Packet, or Atlas canon.
5. Its confidence and caveats are stated in the contract instead of being silently upgraded.

`diagnostic_only` sources can influence contracts only as warnings, anti-patterns, or acceptance-risk notes. They cannot be cited as positive layout guidance.

## Relationship To Academy Records

- Observation records (`schemas/academy-observation.schema.json`) capture facts about a source.
- Metric records (`schemas/academy-map-metrics.schema.json`) compute measurements from sources.
- Reference source records (`schemas/academy-reference-source.schema.json`) govern whether a source may be used and with what authority.

A future source library can store one reference source record per governed source. `WO-2004` defines that shape but does not populate the library.

## Non-Goals

- This document does not approve any specific source as gold standard.
- This document does not copy, import, or store external maps.
- This document does not modify `TheLastSwordProtocol-Atlas`, `TheLastSwordProtocol-Game`, or Atlas canon.
- This document does not create maps.
- This document does not replace `PLAYTEST_AND_ACCEPTANCE.md`; it consumes its outcomes.

## References

- `academy/references/source-classes.md`
- `academy/references/gold-standard-maps.md`
- `schemas/academy-reference-source.schema.json`
- `academy/README.md`
- `academy/observation-model.md`
- `academy/map-metrics.md`
- `academy/grading-rubric.md`
- `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`
- `studio/design-patterns/PATTERN_CONFIDENCE_MODEL.md`
- `studio/contracts/PATTERN_CONTRACT_SPEC.md`
- `studio/operations/PLAYTEST_AND_ACCEPTANCE.md`
- Created by `work-orders/WO-2004-reference-library-governance.md`
