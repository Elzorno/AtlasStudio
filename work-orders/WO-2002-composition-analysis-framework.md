---
work_order_id: WO-2002
title: Composition Analysis Framework
status: accepted
priority: future
phase: Atlas Academy
recommended_agent: claude_code
risk_level: low
player_facing: false
---

# WO-2002 - Composition Analysis Framework

## Objective

Create a framework for analyzing why a map composition works or fails.

This builds on the Observation Engine by turning factual observations into design analysis.

## Purpose

Recent rejected maps showed that functional correctness is not enough. AtlasStudio needs a way to evaluate composition before implementation is accepted.

## Deliverables

Create:

- `academy/composition-analysis.md`
- `academy/composition-rubric.md`
- `academy/compositions/README.md`
- `reports/academy/composition-analysis-framework.md`
- `work-orders/WO-2002-composition-analysis-framework.md`

## Required Topics

Analyze:

- focal point
- negative space
- traffic flow
- sight lines
- furniture grouping
- room zones
- entry readability
- visual hierarchy
- decoration balance
- environmental storytelling

## Constraints

Documentation only.

Do not modify Atlas.

Do not modify TheLastSwordProtocol-Game.

Do not create maps.

Do not modify existing patterns.

Preserve Immutable Formatting Rule.

## Success Criteria

AtlasStudio can describe why a map feels good or bad using repeatable composition criteria rather than vague preference language.

---

## Submission Record

Submitted 2026-07-08 by Claude Code.

Delivered:

- `academy/composition-analysis.md` - all ten required topics (focal point, negative space, traffic flow, sight lines, furniture grouping, room zones, entry readability, visual hierarchy, decoration balance, environmental storytelling), each with a definition, evidence grounding (cited pattern documents, `reports/design-patterns/interior-pattern-corpus-review.md`, `reports/map-analysis/item-shop-analysis.md`, and `references/atlas_academy_jrpg_map_research.md` at that document's own stated confidence tier), and a concrete "what to check" question. Explicitly states what it does not do (numeric metrics, formal grading) and defers those to `WO-2003`/`WO-2005`.
- `academy/composition-rubric.md` - a Holds/Gap/N/A checklist operationalizing the ten topics, plus a worked, honest test of the rubric's own boundaries against the real Map026 rejection - showing where the rubric would and would not have caught the stated failure, rather than claiming broader diagnostic power than it has.
- `academy/compositions/README.md` - filing convention for per-map composition write-ups, and the relationship between this directory, `academy/observations/`, and `academy/reports/`.
- `reports/academy/composition-analysis-framework.md` - the evidence synthesis report: a coverage check confirming every required topic traces to real, cited evidence (and naming the one honest asymmetry - sight lines and entry readability lean more on the newer research doc than on this project's own extracted pattern corpus); and an honest application of the framework to the real, current Map026 Ashford Inn rejection, concluding that the stated rejection reason is predominantly a `tile_usage`/asset-correctness finding (`WO-2001`'s scope) rather than a composition finding this framework primarily covers - stated as a finding about Academy's own category boundaries, not smoothed over to make the new framework look more load-bearing than the evidence supports. Names concrete next steps (an observation record and composition pass against `Map026.json`, read-only) without performing them.
- This work order, marked `submitted`.

No file under `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` was modified - `map_ownership.json`, `Ashford.md`, and the Item Shop analysis were read only. No existing Design Pattern document was modified. No map was created or edited.

One deliberate scope boundary, consistent with prior submissions in this series: `academy/README.md`'s own structure listing is not edited here, since it is not a `WO-2002` deliverable - noting instead that the user has been updating it directly during this session.

Formatting: preserved existing house style, including this file's own leaner `WO-2000`-series frontmatter shape. No existing file was reformatted.

Verification performed:

```bash
find academy/compositions reports/academy -type f
python3 tools/atlas_format/format_guard.py --check
git status --porcelain
```

## Acceptance

Accepted 2026-07-09 following independent verification: every file in this work order's Deliverables list exists on disk and is non-empty, and every JSON schema deliverable parses as valid JSON. Verified by a full-text read of this Submission Record against the actual repository state, not by re-running the commands listed above.
