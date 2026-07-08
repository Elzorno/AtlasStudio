# Atlas Academy Source Classes

## Purpose

Source classes prevent Atlas Academy from treating unlike references as interchangeable. Each class defines provenance requirements, allowed uses, confidence contribution, and implementation-contract influence.

## Class Summary

| Source class | Positive reference? | Diagnostic use? | Can influence contracts? |
|---|---:|---:|---:|
| `official_rpg_maker_sample` | Yes | Yes | Yes, when scope matches and citation is exact. |
| `approved_project_map` | Yes | Yes | Yes, after accepted/accepted-with-notes outcome. |
| `rejected_project_map` | No | Yes | Only as warning, anti-pattern, or risk note. |
| `design_reference` | Limited | Yes | Only as non-authoritative inspiration unless promoted by a later approved process. |
| `comparative_jrpg_reference` | Limited | Yes | Only as comparative/inspirational context, never as direct implementation authority. |

## `official_rpg_maker_sample`

Official RPG Maker sample maps are first-party engine examples studied through map JSON, event data, and tileset data. This is the strongest current source class for RPG Maker production craft because the Design Pattern Library already uses it.

Required provenance:

- engine/version or sample package context, if known;
- source file path, such as `data/Map021.json`;
- map name, if known;
- tileset reference;
- date or commit/source snapshot used for the analysis.

Allowed uses:

- observation records;
- metric records;
- pattern extraction evidence;
- gold-standard candidate review;
- implementation-contract guidance when the source scope matches.

Confidence contribution:

- Usually `high` for facts about RPG Maker map construction.
- Usually `medium` for general design lessons if only one sample supports the lesson.
- Never automatically high for project-specific creative direction.

Contract influence:

- May inform pattern-aware contracts through cited patterns, reference studies, or Academy records.
- Must not override Creative Authority or an Implementation Packet.

## `approved_project_map`

Approved project maps are AtlasStudio or game-project maps that have a recorded **Accepted** or **Accepted with Notes** outcome under `studio/operations/PLAYTEST_AND_ACCEPTANCE.md`.

Required provenance:

- project repository;
- map file path;
- map name or ID;
- acceptance/playtest record path;
- implementation contract or work order, if one exists;
- commit, tag, or date snapshot;
- ownership state at capture.

Allowed uses:

- project-specific reference evidence;
- observation and metric baselines;
- implementation-contract guidance for the same project or a clearly similar context;
- pattern revision proposals, if the accepted map exposes a reusable rule.

Confidence contribution:

- `high` only within the project and scope it was accepted for.
- `medium` as cross-project evidence unless corroborated by official samples or other accepted builds.
- Acceptance notes must travel with the citation.

Contract influence:

- May influence implementation contracts as positive project evidence when acceptance is recorded.
- Must not be treated as accepted merely because a map is `hand_authored`.

## `rejected_project_map`

Rejected project maps are failed implementation attempts with a recorded **Rejected** outcome or equivalent explicit human rejection reason.

Required provenance:

- project repository;
- failed artifact path or identifier;
- rejection record or note;
- specific rejection reason;
- commit, tag, or date snapshot;
- whether the artifact should be preserved, reverted, or ignored.

Allowed uses:

- diagnostic case studies;
- anti-patterns;
- process/tooling risk analysis;
- acceptance-checklist improvement;
- composition or metrics comparison when framed as failure analysis.

Confidence contribution:

- `none` as positive design evidence.
- `low` or `medium` as diagnostic evidence depending on how specific and reproducible the rejection reason is.

Contract influence:

- May influence contracts only as warnings, explicit non-goals, or risk checks.
- Must not become a target layout, style reference, or positive pattern source.

## `design_reference`

Design references are non-map or non-project sources, such as design essays, diagrams, sketches, mood boards, public architecture references, or internal art-direction notes.

Required provenance:

- title or short name;
- author/owner, if known;
- URL or file path;
- access date;
- licensing/copyright notes;
- summary of which design question it informs.

Allowed uses:

- inspiration;
- vocabulary;
- art-direction discussion;
- design hypotheses to test against stronger sources.

Confidence contribution:

- Usually `low` until corroborated by map data or accepted project outcomes.
- Can be `medium` for internal project art-direction documents when they are authoritative for visual intent, but still not map-construction evidence.

Contract influence:

- May influence implementation contracts only as non-authoritative context unless the reference is also a Creative Authority document for that project.

## `comparative_jrpg_reference`

Comparative JRPG references are examples from released games or public media used to discuss genre feel, pacing, readability, or interaction conventions.

Required provenance:

- game title;
- platform/version if known;
- area/map/scene name if known;
- URL, citation, or capture note;
- access/capture date;
- licensing notes;
- short statement of what is being compared.

Allowed uses:

- comparative analysis;
- genre vocabulary;
- exploration-feel discussion;
- high-level player-experience framing.

Confidence contribution:

- Usually `low` for implementation details because the underlying map data is unavailable.
- Can be useful for qualitative comparison when clearly labeled.

Contract influence:

- May influence contracts only as comparative context. It must not dictate tile placement, event structure, or project canon.

## Cross-Class Rules

- Stronger source classes do not erase scope. An official sample inn does not govern an overworld map.
- Lower-confidence sources can suggest questions, not answers.
- Rejected maps are lessons, not models.
- External references require licensing notes even when only cited.
- Every source record must state allowed uses; absence of permission means no implementation-contract influence.

## References

- `academy/references/reference-governance.md`
- `academy/references/gold-standard-maps.md`
- `schemas/academy-reference-source.schema.json`
- `academy/grading-rubric.md`
- `studio/operations/PLAYTEST_AND_ACCEPTANCE.md`
- `studio/contracts/PATTERN_CONTRACT_SPEC.md`
- Created by `work-orders/WO-2004-reference-library-governance.md`
