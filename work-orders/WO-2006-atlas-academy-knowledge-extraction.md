---
work_order_id: WO-2006
title: Atlas Academy Knowledge Extraction
status: submitted
priority: high
phase: Atlas Academy
recommended_agent: claude_code
risk_level: low
player_facing: false
---

# WO-2006 - Atlas Academy Knowledge Extraction

## Objective

Transform the Atlas Academy research corpus into Atlas-native knowledge.

The primary source is the Atlas Academy JRPG Map Research report under `references/`.

Additional Academy research may be incorporated if properly cited.

This work converts research into structured Academy knowledge.

It does not analyze maps.

It does not create implementation contracts.

It does not create patterns.

Those come later.

## Deliverables

Create:

- `academy/knowledge/observation-rules.md`
- `academy/knowledge/composition-rules.md`
- `academy/knowledge/pattern-rules.md`
- `academy/knowledge/validation-rules.md`
- `academy/knowledge/teaching-lessons.md`
- `academy/reports/knowledge-extraction-report.md`
- `work-orders/WO-2006-atlas-academy-knowledge-extraction.md`

## Required Sections

Separate all findings into:

- Observed Fact
- Expert Opinion
- Community Practice
- Atlas Interpretation
- Research Hypothesis

Each rule must retain provenance.

## Constraints

Documentation only.

Do not modify Atlas.

Do not modify TheLastSwordProtocol-Game.

Do not modify existing design patterns.

Do not create maps.

Preserve Immutable Formatting Rule.

## Success Criteria

Atlas Academy contains reusable knowledge rather than only external research.

---

## Submission Record

Submitted 2026-07-08 by Claude Code.

Delivered:

- `academy/knowledge/observation-rules.md`, `composition-rules.md`, `pattern-rules.md`, `validation-rules.md`, `teaching-lessons.md` - each extracted from `references/atlas_academy_jrpg_map_research.md`, with every finding separated into the five required sections (Observed Fact, Expert Opinion, Community Practice, Atlas Interpretation, Research Hypothesis) and provenance ([cite:N] markers and source Part) retained. `Atlas Interpretation` is used specifically for reconciliation statements connecting a research claim to an existing AtlasStudio artifact - never for restating the source as if it were already project authority.
- `academy/reports/knowledge-extraction-report.md` - the evidence report, including a coverage table mapping every source Part to a knowledge file, and three explicit reconciliation decisions: the Part 10 five-axis grading rubric (already reconciled once in `WO-2005`'s `academy/grading-system.md` - not re-derived here), the ten-module research curriculum (reconciled against `academy/curriculum.md`'s existing four levels, module-by-module, rather than stood up as a second curriculum), and four candidate exploration-structure schemas (recorded as candidates for a future Level 4 proposal, not adopted as Design Patterns).
- This work order, marked `submitted`.

No file under `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` was modified - `DDR-0005` was read only, for one correspondence note in `academy/knowledge/pattern-rules.md`. No existing Design Pattern was created or modified. No map was analyzed, created, or edited. No implementation contract was created. `academy/curriculum.md`, `composition-analysis.md`, `map-metrics.md`, `grading-system.md`, and `grading-rubric.md` were read as reconciliation targets and cited, not modified.

Formatting: preserved existing house style; no existing file was reformatted.

Verification performed:

```bash
find academy/knowledge academy/reports/knowledge-extraction-report.md -type f
grep -rl "Atlas Interpretation" academy/knowledge/
git status --porcelain
```
