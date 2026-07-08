# Atlas Academy Gold-Standard Maps

## Purpose

Gold-standard maps are the highest-confidence reference sources Atlas Academy can use for a specific scope. They are not simply "good maps." They are well-proven, well-cited examples whose provenance, licensing posture, source class, and allowed uses are clear.

`WO-2004` defines the criteria. It does not nominate or approve any specific gold-standard map.

## Gold-Standard Criteria

A map can be marked `gold_standard` only when all criteria below are satisfied.

### 1. Provenance Is Stable

The source record must identify:

- repository or external source;
- file path or URL;
- map name or area name;
- tileset or source version when applicable;
- commit, tag, release, date, or capture reference;
- source class.

### 2. Source Class Supports Positive Reference Use

Eligible positive source classes:

- `official_rpg_maker_sample`
- `approved_project_map`

Conditionally eligible:

- `design_reference`, only for art-direction or vocabulary scope, not map-construction scope.
- `comparative_jrpg_reference`, only for comparative player-experience scope, not implementation-detail scope.

Not eligible as positive gold standards:

- `rejected_project_map`

A rejected map may be a strong diagnostic case, but it is never a positive gold-standard map.

### 3. Approval Evidence Exists

For official samples:

- the source must be identified as an official sample or equivalent first-party RPG Maker example;
- the map must have an extraction, observation, or pattern record that cites exact source data.

For project maps:

- the map must have an **Accepted** or **Accepted with Notes** outcome under `PLAYTEST_AND_ACCEPTANCE.md`;
- the acceptance/playtest record must be cited;
- any acceptance notes must be preserved as caveats.

### 4. Scope Is Narrow And Explicit

Gold-standard status applies to a scope, not to the entire map forever. Examples:

- "single-room item shop counter readability"
- "interior bottom-door threshold construction"
- "small NPC interaction room with clear focal point"

Bad scope:

- "good map"
- "best inn"
- "RPG Maker standard"

### 5. Objective Evidence And Interpretation Are Separated

The source must have, or be ready to have:

- objective observations from map data;
- optional metrics;
- subjective analysis grounded in those observations.

Gold-standard status cannot rest only on a screenshot or preference statement.

### 6. Licensing Notes Are Clear

The source record must state whether assets or screenshots may be copied. The default is no copying. A source can still be gold standard for citation and analysis even when asset copying is prohibited.

### 7. Allowed Uses Include The Intended Use

If the source will influence implementation contracts, `allowed_uses` must include `implementation_contract`. If it will influence pattern proposals, `allowed_uses` must include `pattern_extraction`.

## Gold-Standard Record Requirements

A source record marked `gold_standard` must include:

- `approval_status: "gold_standard"`
- `confidence_contribution: "high"`
- at least one `scope` item;
- `allowed_uses`;
- `licensing`;
- `citation`;
- evidence links to observations, metrics, extraction reports, acceptance records, or pattern docs as appropriate.

## What Gold Standard Does Not Mean

- It does not override Creative Authority.
- It does not override an Implementation Packet.
- It does not authorize copying external assets.
- It does not mean every feature of the source should be copied.
- It does not make one project's accepted map authoritative for another project.

## Review And Deprecation

Gold-standard status should be reviewed when:

- source provenance changes;
- a better reference supersedes it;
- a licensing concern appears;
- a project acceptance outcome is revised;
- a later rejected build reveals that the lesson was misapplied.

Deprecated gold-standard maps remain useful historically, but they must not be cited as current guidance.

## Initial Gold-Standard List

None approved by this work order.

Official RPG Maker sample maps are eligible candidates because existing Design Pattern work already studies them, but each candidate still needs a source record and explicit scope before it is listed as gold standard.

## References

- `academy/references/reference-governance.md`
- `academy/references/source-classes.md`
- `schemas/academy-reference-source.schema.json`
- `academy/observation-model.md`
- `academy/map-metrics.md`
- `studio/operations/PLAYTEST_AND_ACCEPTANCE.md`
- `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`
- Created by `work-orders/WO-2004-reference-library-governance.md`
