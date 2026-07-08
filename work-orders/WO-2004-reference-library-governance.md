---
work_order_id: WO-2004
title: Reference Library Governance
status: submitted
priority: future
phase: Atlas Academy
recommended_agent: claude_code
risk_level: low
player_facing: false
---

# WO-2004 - Reference Library Governance

## Objective

Define how Atlas Academy stores and classifies reference sources.

## Purpose

Not every reference map should have equal weight. AtlasStudio needs a governed reference library with provenance, scope, confidence, and allowed-use rules.

## Source Classes

- official RPG Maker sample maps
- approved project maps
- rejected project maps
- design references
- comparative JRPG references

## Deliverables

Create:

- `academy/references/reference-governance.md`
- `academy/references/source-classes.md`
- `academy/references/gold-standard-maps.md`
- `schemas/academy-reference-source.schema.json`
- `work-orders/WO-2004-reference-library-governance.md`

## Required Content

Define:

- source provenance
- approval status
- confidence contribution
- licensing notes
- citation rules
- accepted versus rejected project maps
- gold-standard map criteria
- when a reference can influence implementation contracts

## Constraints

Documentation and schema only.

Do not modify Atlas.

Do not modify TheLastSwordProtocol-Game.

Do not copy external maps.

Do not create maps.

Preserve Immutable Formatting Rule.

## Success Criteria

AtlasStudio can distinguish high-quality references, accepted project maps, rejected case studies, and experimental examples without mixing their authority levels.

---

## Submission Record

Submitted 2026-07-08 by Codex.

Delivered:

- `academy/references/reference-governance.md` - governance for source classes, approval status, confidence contribution, licensing and copy rules, citation rules, accepted versus rejected project maps, implementation-contract influence, and relationship to observation/metrics records.
- `academy/references/source-classes.md` - detailed rules for `official_rpg_maker_sample`, `approved_project_map`, `rejected_project_map`, `design_reference`, and `comparative_jrpg_reference`.
- `academy/references/gold-standard-maps.md` - criteria for gold-standard maps, including provenance, source-class eligibility, approval evidence, scope, evidence separation, licensing, allowed uses, and deprecation.
- `schemas/academy-reference-source.schema.json` - JSON Schema (2020-12) for governed reference source records.
- `academy/references/README.md` - updated to point at the new governance documents.
- `academy/README.md` - updated directory listing for the new reference governance files.
- This work order, marked `submitted`.

No file in `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` was modified. No map was created or edited. No Atlas canon file or Design Pattern document was modified. No external map or asset was copied.

Formatting: preserved existing `WO-2000`-series style; no broad reformatting performed.

Verification performed:

```bash
node -e "JSON.parse(require('fs').readFileSync('schemas/academy-reference-source.schema.json','utf8')); console.log('schema ok')"
python3 tools/atlas_format/format_guard.py --check
git status --porcelain
```
