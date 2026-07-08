# Atlas Academy Screenshot Guidelines

## Status

Documentation only, per `work-orders/WO-2010-screenshot-analysis-pipeline.md`. Specifies capture, filing, comparison, and review requirements for images used in Academy work. Does not implement a capture tool and does not create any image or directory.

## Image Provenance (Required for Every Filed Image)

Every image used as Academy evidence must record, at minimum:

- **Type**: `engine_faithful_render` or `live_gameplay_screenshot`, per `academy/rendering-pipeline.md`'s three-category split. Generated concept art is never filed as Academy evidence at all - see that document's Non-Goals.
- **Source map**: repo and file path (e.g. `TheLastSwordProtocol-Game/data/Map001.json`).
- **Commit or date snapshot**: which version of the map the image reflects, since a map can change after an image is captured.
- **Capture context** (live screenshots only): camera position/zoom if variable, and any runtime state that affects what is visible (time of day, active event, NPC schedule) so a reviewer does not mistake a transient state for a permanent one.
- **Ownership state at capture**: per `map_ownership.json`, matching `schemas/academy-observation.schema.json`'s existing `source.ownership_state_at_capture` convention - an image of a `generated` map and an image of a `hand-authored` map carry different weight.

An image without this provenance is not usable as cited evidence in any Academy record - it may still be useful as an informal reference, but must not be cited in a Composition Review, grade, or observation the way a properly-provenanced image can be.

## Screenshot Capture

- Prefer an engine-faithful render (`academy/rendering-pipeline.md`) over a live screenshot whenever the question at hand does not require runtime state - it is reproducible and carries no camera or lighting variance to account for.
- Capture a live gameplay screenshot only when the question specifically concerns runtime-only state: animation, lighting/tint, UI, or camera framing a static render cannot show.
- Capture at a resolution and zoom that keeps the full map (or the full room, for an interior) in frame where practical; a partial capture must state explicitly what portion of the map it omits.
- Do not retouch, crop for aesthetics, or otherwise alter a captured image before filing it as evidence - an edited image is no longer a faithful record of what the engine or the map actually produced.

## Filing Convention

Until a dedicated `academy/` subdirectory is created by a future work order (not created here, consistent with this document's own documentation-only constraint), file an image's provenance record alongside whatever Academy record cites it (an observation, a Composition Review, a case study), following the same "point, don't paraphrase" citation discipline already used throughout Academy documents - cite the image's actual file path (for example the existing `rpgmakerLSP/reports/atlas-import/wo-0036-map001-render.png` precedent) rather than re-describing its content as if it were the primary record.

## Comparison Workflow

Comparing two images of the same map (a rejected pass against a revised one, or a `WO-2005`-style before/after) requires:

1. Both images share the same type (do not compare a render against a live screenshot - the visual differences would conflate rendering-method variance with actual map-content variance).
2. Both images' provenance is recorded, per above, so the comparison can state exactly what changed between the two commit/date snapshots.
3. The comparison names specific, falsifiable visual differences (per `academy/curriculum.md` Level 3's diagnostic standard: "the counter placement felt cramped" is not a finding; "the counter cluster now terminates into the wall instead of floating mid-floor" is), not a general impression of "looks better."
4. Any visual difference cited as evidence for a score change (in a Composition Review or a grade) must also be checked against the underlying JSON where the claim is structural, per `academy/image-analysis.md`'s governing boundary - a comparison should not assume a visual improvement implies a structural one.

## Human Review

Until an automated pass exists (see Future AI Integration below), every image analysis finding is a human judgment, tagged `[Observed Fact]` or `[Inference]` per `academy/image-analysis.md`. A human reviewer should:

- State which of `academy/image-analysis.md`'s "What an Image Can Support" questions they are answering - an unscoped "does this look good" review is not reproducible and should not be filed as Academy evidence.
- Cross-check any structural claim against the map's JSON before treating it as more than a visual impression, per the same governing boundary.
- Record disagreement between the visual read and the JSON-derived facts explicitly, rather than silently preferring one - a mismatch (e.g. a wall tile that visually reads as walkable) is itself a useful finding, not an error to suppress.

## Future AI Integration

Not built here. This section records what a future automated image-analysis pass would need to respect, so a future work order does not have to re-derive these constraints:

- It must operate only within `academy/image-analysis.md`'s "What an Image Can Support" boundary - an automated pass proposing a passability, event, or tile-ID claim from an image alone would violate `PATTERN_EXTRACTION_GUIDE.md`'s existing JSON-first rule as much as a human doing the same would.
- Its output should use the same `[Observed Fact]`/`[Inference]` tagging and the same evidence-citation discipline as human review, with a `confidence` tier per `academy/scoring-model.md`'s existing four-tier vocabulary, so automated and human findings remain comparable rather than requiring a parallel scale.
- It must not be treated as a Design Pattern, Composition Review, or grade on its own - its output is evidence a human-produced Academy record cites, matching how `academy/composition-validator.md` already treats a Composition Review relative to a full grade.
- It should be evaluated against a set of images with known-correct human findings before being trusted at anything above `low` confidence, the same bar `studio/design-patterns/PATTERN_CONFIDENCE_MODEL.md` already sets for any new evidence source entering this project.

## Non-Goals

- Does not implement a capture tool, comparison tool, or automated vision integration.
- Does not create an `academy/screenshots/` directory or any image file.
- Does not modify `map_ownership.json`, any map, or `TheLastSwordProtocol-Atlas`/`TheLastSwordProtocol-Game`.

## References

- `academy/rendering-pipeline.md`, `image-analysis.md`
- `schemas/academy-observation.schema.json`
- `academy/scoring-model.md`, `curriculum.md`
- `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`, `PATTERN_CONFIDENCE_MODEL.md`
- `bridges/rpg-maker-mz/passability-rule.md`
- `rpgmakerLSP/reports/atlas-import/wo-0036-map001-render.png` (read-only precedent)
- `reports/academy/screenshot-analysis-design.md`
- Created by `work-orders/WO-2010-screenshot-analysis-pipeline.md`
