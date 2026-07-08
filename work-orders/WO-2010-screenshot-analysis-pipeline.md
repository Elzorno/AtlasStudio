---
work_order_id: WO-2010
title: Screenshot Analysis Pipeline
status: submitted
priority: medium
phase: Atlas Academy
recommended_agent: claude_code
risk_level: medium
player_facing: false
---

# WO-2010 - Screenshot Analysis Pipeline

## Objective

Design a screenshot-based review workflow.

Atlas Academy should analyze rendered maps rather than relying only on RPG Maker JSON.

## Deliverables

Create:

- `academy/image-analysis.md`
- `academy/rendering-pipeline.md`
- `academy/screenshot-guidelines.md`
- `academy/reports/screenshot-analysis-design.md`
- `work-orders/WO-2010-screenshot-analysis-pipeline.md`

## Topics

Include:

- Rendering
- Image provenance
- Screenshot capture
- Visual hierarchy
- Comparison workflow
- Human review
- Future AI integration

## Constraints

Documentation only.

No image processing implementation.

Do not modify Atlas.

Do not modify TheLastSwordProtocol-Game.

Do not create or edit maps.

Preserve Immutable Formatting Rule.

## Success Criteria

Atlas Academy has a complete specification for future screenshot-based analysis.

---

## Submission Record

Submitted 2026-07-08 by Claude Code.

Delivered:

- `academy/rendering-pipeline.md` - grounds the design in real, already-existing precedent rather than a blank proposal: `rpgmakerLSP/reports/atlas-import/wo-0035-map002-render.png` and `wo-0036-map001-render.png` are documented, working "engine-faithful renders" generated from real map JSON using RPG Maker MZ's own autotile tables, with one named, honest gap (the render script "ran from the session scratchpad... so it cannot be re-run"). Defines three distinct image categories (engine-faithful render, live gameplay screenshot, generated concept art) and keeps generated concept art fully outside this pipeline's evidentiary scope, per `bridges/rpg-maker-mz/map-quality-standard.md`'s existing "Image Generation Role."
- `academy/image-analysis.md` - states the governing boundary explicitly: `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`'s "work from the actual map data file... not from a screenshot" rule stands unchanged for every structural fact; this document adds only a narrow set of perception-based questions (emergent visual read, visual hierarchy, atmosphere, landmark distinctiveness) an image is a better source for than JSON alone.
- `academy/screenshot-guidelines.md` - provenance requirements, capture guidance, a comparison workflow with a falsifiability requirement (per `academy/curriculum.md` Level 3's diagnostic standard), human-review discipline, and a Future AI Integration section stating the constraints any later automated pass must respect (the same `[Observed Fact]`/`[Inference]` tagging and confidence tiers as human review, no claims outside the stated evidentiary boundary).
- `reports/academy/screenshot-analysis-design.md` - the evidence report, including two real worked visual analyses against the actual `wo-0035`/`wo-0036` renders (both images viewed directly for this report, not generated or modified): a "patchwork roof reads as visually busy" finding on Map001's exterior, and a "the rug is the room's strongest visual focal point, more dominant than the bed" finding on Map002's interior - both tagged `[Observed Fact]`/`[Inference]` and both explicitly checked against what the image cannot support (passability, event logic, exact tile data).
- This work order, marked `submitted`.

No image-processing code was implemented. No file under `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` was modified. The two cited renders under `rpgmakerLSP/reports/atlas-import/` were viewed and read only, not modified or regenerated. No map was created or edited. No `academy/screenshots/` directory or new image file was created, per this work order's documentation-only constraint.

Formatting: preserved existing house style; no existing file was reformatted.

Verification performed:

```bash
find academy/rendering-pipeline.md academy/image-analysis.md academy/screenshot-guidelines.md reports/academy/screenshot-analysis-design.md -type f
git status --porcelain
git -C ../rpgmakerLSP status --porcelain -- reports/atlas-import/wo-0035-map002-render.png reports/atlas-import/wo-0036-map001-render.png
```
