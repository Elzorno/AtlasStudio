---
work_order_id: WO-0024
title: RPG Maker Design Pattern Library
status: submitted
project: atlasstudio
recommended_agent: claude-code
agent_role: senior-software-architect
risk_level: low
player_facing: false
engine_specific: true
required_capabilities:
  - documentation
  - architecture-review
preferred_capabilities:
  - qa-review
produces:
  - design-patterns.framework
  - design-patterns.interior.shop.v1_0
created: 2026-07-08
---

# WO-0024 - RPG Maker Design Pattern Library

## Purpose

AtlasStudio has completed its first reverse-engineering study of an official RPG Maker sample map (`TheLastSwordProtocol-Game/reports/map-analysis/item-shop-analysis.md`). That report is valuable but ephemeral - a one-off analysis with no standing place to live, no schema future extractions must follow, and no path for a future implementation contract to cite it without re-reading the whole report. This work order creates a permanent Design Pattern Library that captures reusable environment-design knowledge extracted from official RPG Maker sample maps, so future implementation contracts can reference proven design patterns instead of implementation agents inventing layouts from scratch.

This work order creates the framework only. It does not populate the entire library.

## Player-Facing Goal

Indirect. A well-grounded pattern library makes future interior and exterior builds (shops, houses, dungeons, towns) more likely to read as polished and intentional on the first pass, the same way `bridges/rpg-maker-mz/map-quality-standard.md` already raises the bar for map quality - but this work order itself changes no game file and ships no player-visible content.

## Background

Review: `work-orders/WO-0020-ashford-village-implementation-contract-from-atlas-handoff.md`, `work-orders/WO-0021-cross-repository-work-order-router.md`, `work-orders/WO-0022-executable-router-specification.md`, `work-orders/WO-0023-executable-work-order-router.md`.

`WO-0020` established the shape of a citable, source-grounded implementation contract (exact authoritative sources, exact Game-repo targets, ownership restrictions derived from the map ownership ledger, passability requirements, testable acceptance criteria). `WO-0021`/`WO-0022`/`WO-0023` established that AtlasStudio-owned standing knowledge (routing rules, in that case) should be designed, specified, and reviewable independently of any single implementation contract, with safety rules preventing scope creep into sibling repositories. This work order applies the same discipline to environment-design knowledge: a standing, schema-governed library, reviewed the way other AtlasStudio standing documents are, that implementation contracts can cite the way `ashford-shop-build-contract.md` already cites `IMP-HOM-019`.

Also reviewed: `reports/map-analysis/item-shop-analysis.md` (`TheLastSwordProtocol-Game`, the seed extraction this work order converts into the library's first pattern), `bridges/rpg-maker-mz/passability-rule.md`, `bridges/rpg-maker-mz/map-quality-standard.md` (the existing RPG Maker bridge documentation this library must stay consistent with), and the existing implementation contracts under `reports/implementation-contracts/` (the citing pattern this library's "Future Integration" section is designed to match).

## Scope

### In Scope

- A standard pattern document format (`PATTERN_SCHEMA.md`).
- A method for analyzing future official sample maps without copying them (`PATTERN_EXTRACTION_GUIDE.md`).
- A confidence system for rating how trustworthy a pattern is, and how that rating changes over time (`PATTERN_CONFIDENCE_MODEL.md`).
- A propose/review/accept/deprecate/version process, including how implementation contracts should reference an accepted pattern (`PATTERN_REVIEW_PROCESS.md`).
- Converting `reports/map-analysis/item-shop-analysis.md` into exactly one reusable, abstracted pattern document (`interiors/shop.pattern.md`) - not a copy of the report, but reusable engineering guidance derived from it.
- A `README.md` describing the library's purpose and its relationship to Atlas, AtlasStudio, implementation contracts, and RPG Maker.

### Out of Scope

- Populating the rest of the library (houses, inns, dungeons, towns, or any category beyond the single seeded `interiors/shop.pattern.md`).
- Modifying `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` in any way.
- Modifying AtlasStudio canon.
- Writing or modifying any code or tooling (e.g. an automated pattern linter) - documentation only.
- Modifying any existing implementation contract to add a pattern citation retroactively.

## Inputs

- `TheLastSwordProtocol-Game/reports/map-analysis/item-shop-analysis.md`
- `work-orders/WO-0020-ashford-village-implementation-contract-from-atlas-handoff.md`, `work-orders/WO-0021-cross-repository-work-order-router.md`, `work-orders/WO-0022-executable-router-specification.md`, `work-orders/WO-0023-executable-work-order-router.md`
- `bridges/rpg-maker-mz/passability-rule.md`, `bridges/rpg-maker-mz/map-quality-standard.md`, `bridges/rpg-maker-mz/bridge-design.md`, `bridges/rpg-maker-mz/handoff-format.md`, `bridges/rpg-maker-mz/ownership-model.md`
- `reports/implementation-contracts/ashford-village-contract.md`, `ashford-shop-build-contract.md`, `ashford-dialogue-application-contract.md`, `ashford-existing-map-verification-contract.md`
- `studio/immutable-formatting-rule.md`, `studio/work-order-format.md`, `studio/agent-roles.md`, `studio/governance/decision-record-template.md`

## Deliverables

- `studio/design-patterns/README.md`
- `studio/design-patterns/PATTERN_SCHEMA.md`
- `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`
- `studio/design-patterns/PATTERN_CONFIDENCE_MODEL.md`
- `studio/design-patterns/PATTERN_REVIEW_PROCESS.md`
- `studio/design-patterns/interiors/shop.pattern.md`
- `work-orders/WO-0024-design-pattern-library.md`

## Acceptance Criteria

- `README.md` describes purpose, relationship to Atlas, relationship to AtlasStudio, relationship to implementation contracts, and relationship to RPG Maker.
- `PATTERN_SCHEMA.md` defines a standard pattern format including name, category, source, confidence, observed maps, applicable genres, required conditions, layout rules, composition rules, passability rules, event rules, common mistakes, and references.
- `PATTERN_EXTRACTION_GUIDE.md` teaches what to measure, what not to infer, objective vs. subjective observations, how to distinguish them, and how to cite evidence.
- `PATTERN_CONFIDENCE_MODEL.md` defines High/Medium/Low/Experimental (or equivalent) confidence levels and describes how confidence changes over time, in both directions.
- `PATTERN_REVIEW_PROCESS.md` describes how patterns are proposed, reviewed, accepted, deprecated, versioned, and referenced by implementation contracts.
- `interiors/shop.pattern.md` is an abstraction of `item-shop-analysis.md`'s findings into reusable engineering guidance, not a copy of the report - it contains no verbatim reproduction of the report's prose and cites the report as its source rather than restating its raw tile-coordinate data as prescriptive instruction.
- The pattern library stores principles only: no copyrighted RPG Maker sample layout, tile grid, or JSON export is reproduced anywhere in the deliverables.
- No deliverable authorizes a pattern to replace an implementation packet or screen object - `README.md` and `PATTERN_REVIEW_PROCESS.md` both state this explicitly.
- Every pattern document references its authoritative source(s) by exact path.
- A future implementation contract can write `Apply Interior Pattern: Shop v1.0` and, per `README.md`'s "Future Integration" section and `PATTERN_REVIEW_PROCESS.md`'s citation rules, an implementation agent can determine exactly what that means without further explanation.
- Documentation only: no code is added or modified; no file under `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` is modified; no AtlasStudio canon file is modified.
- The Immutable Formatting Rule is preserved: no existing file is reformatted.
- This work order is marked `submitted`.

## Verification Steps

```bash
find studio/design-patterns -name "*.md"
find work-orders -name "WO-0024-design-pattern-library.md"
python3 tools/atlas_format/format_guard.py --check
git -C ../TheLastSwordProtocol-Atlas status --porcelain
git -C ../TheLastSwordProtocol-Game status --porcelain
# expect no changes attributable to this work order in either sibling repository
```

## Allowed Changes

- `studio/design-patterns/`
- `work-orders/WO-0024-design-pattern-library.md`

## Protected Areas

- Do not modify `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game`.
- Do not modify AtlasStudio canon.
- Do not write or modify code.
- Do not populate the library beyond the single seeded `interiors/shop.pattern.md`.
- Preserve the Immutable Formatting Rule.

## Notes for Assigned Agent

This is a documentation and schema work order, matching the shape of `WO-0021` (design a standing system) rather than `WO-0023` (implement it). The single hardest constraint is the one stated directly in the brief: never copy a map, never store a copyrighted layout, never let a pattern replace an implementation packet. Every section of every deliverable should be checked against that constraint specifically - the risk is subtle, since the source material (`item-shop-analysis.md`) already contains exact tile coordinates and autotile names, and it is easy to let those slip from "evidence in the source report" into "instructions in the pattern document" by accident. `PATTERN_SCHEMA.md`'s "Format Discipline" section and `PATTERN_EXTRACTION_GUIDE.md`'s "What Not to Infer" section exist specifically to catch that failure mode.

## Submission Record

Submitted 2026-07-08 by Claude Code.

Delivered:

- `studio/design-patterns/README.md` - purpose, and explicit relationship sections to Atlas (principles never override canon), AtlasStudio (owned standing knowledge, versioned and reviewed like other standing documents), implementation contracts (an additional citable input alongside packets, never a replacement), and RPG Maker (every pattern traces to official sample data; the library stores principles, never copied layouts).
- `studio/design-patterns/PATTERN_SCHEMA.md` - required frontmatter (`pattern_id`, `name`, `version`, `category`, `status`, `confidence`, `observed_maps`, `applicable_genres`, `source_report`, `created`, `last_reviewed`) and required body sections (Name, Category, Source, Confidence, Observed Maps, Applicable Genres, Required Conditions, Layout Rules, Composition Rules, Passability Rules, Event Rules, Common Mistakes, References), plus an explicit "Format Discipline" rule prohibiting prescriptive source-map coordinates in a pattern document.
- `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md` - what to measure from map JSON and tileset data, what not to infer (unconfirmed spawn points, invented NPC roles, gameplay systems the map does not implement, universalized single-map coordinates), the objective/subjective distinction with a reproducibility test, and an evidence-citation rule requiring pattern documents to cite extraction reports by path rather than restate raw data.
- `studio/design-patterns/PATTERN_CONFIDENCE_MODEL.md` - four levels (High: repeated official-sample corroboration; Medium: observed once; Low: project preference without sample-map backing; Experimental: unverified idea), with explicit upward and downward transition rules and a requirement that every confidence change be recorded in the pattern document itself.
- `studio/design-patterns/PATTERN_REVIEW_PROCESS.md` - proposal paths (extraction-driven and project-preference-driven), a three-part review check (schema completeness, extraction discipline, confidence accuracy), acceptance criteria, deprecation triggers (never delete, mark and point to a successor), `MAJOR.MINOR` versioning rules, and explicit citation rules for implementation contracts (cite by name and current version, state the pattern's actual current confidence, treat cited rules as binding unless the contract states an override).
- `studio/design-patterns/interiors/shop.pattern.md` - `PAT-INTERIOR-SHOP v1.0`, filed at `confidence: medium` (single-source, per the confidence model's own bar - not `high`, since only one official sample map has been studied so far). Abstracts `item-shop-analysis.md`'s `Reusable Design Rules` and `AtlasStudio Recommendations` into schema-shaped Layout/Composition/Passability/Event rules and Common Mistakes, with Required Conditions scoping it to single-room, single-entrance, browsing-focused retail interiors reached from a town exterior. Contains no reproduced tile coordinates, autotile grid, or JSON from the source map - only abstracted principles, with the source report cited for evidence.
- This work order, marked `submitted`.

No file in `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` was modified - confirmed directly (read-only inspection of `item-shop-analysis.md`, `AGENTS.md`, and `map_ownership.json` only). No AtlasStudio canon file was modified. No code was written or modified. The library was seeded with exactly one pattern, per scope.

Formatting: preserved existing house style; no existing file was reformatted. All deliverables are new files.

Verification performed:

```bash
find studio/design-patterns -name "*.md"
find work-orders -name "WO-0024-design-pattern-library.md"
git -C ../TheLastSwordProtocol-Atlas status --porcelain
git -C ../TheLastSwordProtocol-Game status --porcelain
```
