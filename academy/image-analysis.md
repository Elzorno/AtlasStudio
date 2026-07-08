# Atlas Academy Image Analysis

## Status

Documentation only, per `work-orders/WO-2010-screenshot-analysis-pipeline.md`. Specifies what an image (an engine-faithful render or a live gameplay screenshot, per `academy/rendering-pipeline.md`'s three-category split) can and cannot be used as evidence for. Does not implement an image analyzer, human or automated. Does not analyze any real map's image as part of its own deliverable - `reports/academy/screenshot-analysis-design.md` performs one worked, real example.

## The Governing Boundary

`studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md` already states the rule this document must not contradict: "Work from the actual map data file... not from a screenshot or memory of the tileset." That rule stands, unchanged, for anything **structural or factual** - exact tile IDs, passability, event placement, transfer targets, region/encounter data. This document does not reopen that rule. What it adds is narrower: a small set of questions where a visual image is a *better* source than raw JSON, specifically because those questions are about how a composition **reads to a viewer**, not what data is technically present.

## What an Image Can Support

- **Emergent visual read.** Individual tile IDs composed together can produce a visual effect not obvious from the tile list alone. `reports/academy/screenshot-analysis-design.md`'s worked example demonstrates this directly: a roof built from a multi-color "patchwork" tile pattern reads as visually busy next to two solid-color roofs nearby, a composition observation about *perceived contrast* that a tile-ID listing does not surface on its own.
- **Visual hierarchy and focal contrast**, per `academy/composition-analysis.md` Topic 8 and `academy/composition-validator.md`'s `visual_hierarchy` area - whether a claimed focal point actually draws the eye, as opposed to merely occupying the centerline coordinate-wise.
- **Atmosphere and color read**, per `academy/composition-validator.md`'s `atmosphere` area - density, warmth, and rhythm as they visually present, not merely as a coordinate-based density gradient.
- **Landmark distinctiveness**, per `academy/composition-validator.md`'s `landmarks` area - whether an intended landmark is visually distinguishable from its surroundings at normal render scale.
- **Gross layout sanity-checking.** A render can catch an obviously wrong-looking result (a building rendering as disconnected fragments, an autotile seam, a tileset mismatch) faster than a human reading raw tile IDs would, even though the underlying JSON remains the authority on whether it is technically correct.

## What an Image Cannot Support

- **Exact tile IDs, autotile family membership, or shadow values** - these remain `PATTERN_EXTRACTION_GUIDE.md`'s domain, read from JSON directly.
- **Passability.** A tile can look walkable and be blocked, or look blocked and be walkable, depending on collision flags an image never shows. `bridges/rpg-maker-mz/passability-rule.md` remains the sole authority here.
- **Event logic, triggers, or transfer targets.** These are invisible in a static render by construction; only the JSON's event list is authoritative.
- **Region or encounter data.** Never visually rendered; JSON-only.
- **Anything about a live gameplay screenshot's runtime state that isn't stable across replays** (a random encounter that happened to trigger, a particular NPC schedule frame) unless the capture explicitly records that state, per `academy/screenshot-guidelines.md`.

## Relationship to Existing Scoring Frameworks

An image analysis pass does not introduce an eleventh `academy/composition-validator.md` area or a tenth `academy/grading-system.md` category. It is a **new evidence type** that can support several existing areas/categories more strongly than JSON-only evidence could - `visual_hierarchy`, `atmosphere`, `landmarks`, and `environmental_storytelling` most directly. A future Composition Review or map grade citing an image analysis should cite it the same way it already cites an `academy/composition-rubric.md` verdict or an observation record: as `evidence`, with the image's file path and provenance (render vs. capture, per `academy/rendering-pipeline.md`), never as a replacement for the structural facts JSON already establishes.

## How An Image Analysis Pass Should Be Recorded

Until a dedicated schema exists (not created by this documentation-only work order), an image analysis finding should be recorded as prose evidence citing the image's file path directly, following this project's standing "point, don't paraphrase" discipline - state what is visually observed, tag it `[Observed Fact]` (directly visible in the image) or `[Inference]` (an interpretation of what is visible), per the same convention `academy/knowledge/observation-rules.md` already established for text-based observation.

## Non-Goals

- Does not implement an image analyzer, human workflow tool, or automated vision model integration.
- Does not override `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`'s JSON-first rule for structural facts.
- Does not apply to AI-generated concept art, per `academy/rendering-pipeline.md`'s three-category split and `bridges/rpg-maker-mz/map-quality-standard.md`'s existing "Image Generation Role."
- Does not modify `academy/composition-analysis.md`, `composition-validator.md`, or `academy/grading-system.md`.

## References

- `academy/rendering-pipeline.md`, `screenshot-guidelines.md`
- `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`
- `bridges/rpg-maker-mz/passability-rule.md`, `map-quality-standard.md`
- `academy/composition-analysis.md`, `composition-validator.md`, `grading-system.md`
- `academy/knowledge/observation-rules.md`
- `reports/academy/screenshot-analysis-design.md`
- Created by `work-orders/WO-2010-screenshot-analysis-pipeline.md`
