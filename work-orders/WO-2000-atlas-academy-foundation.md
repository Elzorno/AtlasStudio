---
work_order_id: WO-2000
title: Atlas Academy Foundation
status: accepted
priority: future
phase: Atlas Academy
recommended_agent: claude_code
risk_level: low
player_facing: false
---

# WO-2000 - Atlas Academy Foundation

## Objective

Create the foundation for Atlas Academy, the design-learning subsystem of AtlasStudio.

Atlas Academy studies reference maps, accepted maps, and rejected maps so future implementation contracts can use observed composition knowledge instead of relying only on prose descriptions.

## Purpose

This work preserves lessons from map reviews and turns them into reusable production knowledge.

## Deliverables

Create:

- `academy/README.md`
- `academy/curriculum.md`
- `academy/grading-rubric.md`
- `academy/references/README.md`
- `academy/reports/README.md`
- `work-orders/WO-2000-atlas-academy-foundation.md`

## Required Content

Define:

- Academy purpose
- Reference source rules
- Accepted-map rules
- Rejected-map rules
- Relationship to Design Patterns
- Relationship to Implementation Contracts
- Relationship to Playtest and Acceptance
- Initial curriculum levels

## Constraints

Documentation only.

Do not modify Atlas.

Do not modify TheLastSwordProtocol-Game.

Do not create or edit maps.

Do not modify existing design patterns.

Preserve Immutable Formatting Rule.

## Success Criteria

AtlasStudio has a clear place to store map lessons, reference studies, acceptance/rejection case studies, and future analysis outputs.

---

## Submission Record

Submitted 2026-07-08 by Claude Code.

Delivered:

- `academy/README.md` - Academy's purpose, directory structure (including the not-yet-built `WO-2001`-`WO-2005` paths, named honestly rather than implied to exist), reference source rules summary, accepted-map rules, rejected-map rules, and explicit relationship sections to Design Patterns, Implementation Contracts, and Playtest and Acceptance - each grounded in an existing document rather than asserted independently. Accepted/Rejected rules reuse `studio/operations/PLAYTEST_AND_ACCEPTANCE.md`'s four existing outcomes rather than inventing a new vocabulary. Grounded in two real precedents: `BUILD-0043` (`rpgmakerLSP`, the real rejected-automatic-map-construction case) and this session's own `reports/implementation-contracts/ashford-inn-pattern-aware-contract.md` (a real, just-produced case where no Specialization pattern's Required Conditions matched the build).
- `academy/curriculum.md` - four initial curriculum levels (Recognize, Compare, Diagnose, Propose), each tied to an existing method or document (`PATTERN_EXTRACTION_GUIDE.md`, `PLAYTEST_AND_ACCEPTANCE.md`, `PATTERN_REVIEW_PROCESS.md`) rather than a new one, with the `BUILD-0043` and Ashford Inn cases used as worked (not fabricated) examples at Levels 3 and 4.
- `academy/grading-rubric.md` - explicitly scoped as foundation-level only, stating it will be superseded/expanded by `WO-2005-map-grading-system.md` rather than silently claiming that work order's full scope (composition, traffic flow, readability, and so on, none of which this document grades). Defines foundation-level accepted/rejected eligibility criteria for an Academy case study, reusing `PLAYTEST_AND_ACCEPTANCE.md`'s outcome vocabulary unchanged.
- `academy/references/README.md` - reference source rules for the two source classes already in active use (official RPG Maker MZ sample maps; AtlasStudio's own accepted builds, none of which currently qualify since Ashford Village's maps are not yet playtest-certified), explicitly deferring full governance (source classes, provenance, gold-standard list) to `WO-2004-reference-library-governance.md` rather than pre-empting it.
- `academy/reports/README.md` - states what belongs in this directory (Level 1-4 case-study output) and explicitly distinguishes it from the separate `reports/academy/` top-level path `WO-2002`'s own brief already names, rather than silently conflating the two or picking one without saying so.
- This work order, marked `submitted`.

No file under `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` was modified - not touched, read-only citations only. No existing Design Pattern document under `studio/design-patterns/` was modified - all five deliverables are new files under a new `academy/` directory. No map was created or edited. `work-orders/WO-2001` through `WO-2005` were read for context (to avoid contradicting or duplicating their planned deliverables) but not modified.

Formatting: preserved existing house style, including this file's own leaner `WO-2000`-series frontmatter shape (matching `WO-2001`-`WO-2005`, not the older `work-orders/WO-0030`-era schema) rather than reformatting it. No existing file was reformatted.

Verification performed:

```bash
find academy -type f
python3 tools/atlas_format/format_guard.py --check
git status --porcelain
```

## Acceptance

Accepted 2026-07-09 following independent verification: every file in this work order's Deliverables list exists on disk and is non-empty, and every JSON schema deliverable parses as valid JSON. Verified by a full-text read of this Submission Record against the actual repository state, not by re-running the commands listed above.
