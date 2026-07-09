---
work_order_id: WO-2007
title: Official RPG Maker Corpus Study
status: accepted
priority: high
phase: Atlas Academy
recommended_agent: claude_code
risk_level: low
player_facing: false
---

# WO-2007 - Official RPG Maker Corpus Study

## Objective

Develop the repeatable methodology for studying official RPG Maker maps.

Study exactly one official map.

Do not attempt to analyze the full corpus.

The purpose is to establish the Academy review methodology.

## Deliverables

Create:

- `academy/case-studies/official-map-001.md`
- `academy/templates/map-study-template.md`
- `academy/reports/official-corpus-methodology.md`
- `work-orders/WO-2007-official-rpgmaker-corpus-study.md`

## Required Analysis

Include:

- Observation
- Composition
- Traffic Flow
- Negative Space
- Landmarks
- Passability
- Environmental Storytelling
- Metrics
- Lessons Learned

## Constraints

Documentation only.

No implementation.

No pattern extraction.

No map generation.

Do not modify Atlas.

Do not modify TheLastSwordProtocol-Game.

Preserve Immutable Formatting Rule.

## Success Criteria

Atlas Academy has a repeatable map-analysis workflow that can later be applied to every official sample map.

---

## Submission Record

Submitted 2026-07-08 by Claude Code.

Delivered:

- `academy/templates/map-study-template.md` - a reusable nine-section template (Observation, Composition, Traffic Flow, Negative Space, Landmarks, Passability, Environmental Storytelling, Metrics, Lessons Learned), sequencing existing Academy methods (`PATTERN_EXTRACTION_GUIDE.md`, `composition-analysis.md`/`composition-rubric.md`, `map-metrics.md`, `passability-rule.md`) rather than inventing new ones, with an explicit `[Observed Fact]`/`[Inference]` tagging convention and an `insufficient_evidence` fallback per section.
- `academy/case-studies/official-map-001.md` - the first filled study, of Map021 ("Item Shop"), built entirely from already-verified evidence (`TheLastSwordProtocol-Game/reports/map-analysis/item-shop-analysis.md` and `shop.pattern.md`) with no new map inspection. Every metric is labeled exact or heuristic; two metrics (decoration density, room utilization) are honestly `insufficient_evidence` rather than guessed. Names directly that its Composition section cannot independently validate `shop.pattern.md`'s confidence tier, since the map and the pattern share the same single source.
- `academy/reports/official-corpus-methodology.md` - the evidence report: why Map021 was chosen (best-documented single map, to test the template rather than conflate template design with first-pass inspection), the five-step methodology as it actually worked, two template sections (Traffic Flow, Landmarks) that had no clean single existing document to cite and were routed to their nearest partial matches instead, and an explicit statement that applying this template to the remaining seven corpus interiors (not performed here, per this work order's constraint) would require more first-pass work than Map021 needed, since none of the seven has its own per-map extraction report.
- This work order, marked `submitted`.

Studied exactly one official map (Map021), per this work order's explicit constraint against analyzing the full corpus. No file under `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` was modified - the existing extraction report was read only. No Design Pattern was created or modified, and no pattern-confidence change is claimed. No map was generated. No implementation contract was created.

Formatting: preserved existing house style; no existing file was reformatted.

Verification performed:

```bash
find academy/templates academy/case-studies academy/reports/official-corpus-methodology.md -type f
git status --porcelain
```

## Acceptance

Accepted 2026-07-09 following independent verification: every file in this work order's Deliverables list exists on disk and is non-empty, and every JSON schema deliverable parses as valid JSON. Verified by a full-text read of this Submission Record against the actual repository state, not by re-running the commands listed above.
