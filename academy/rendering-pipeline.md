# Atlas Academy Rendering Pipeline

## Status

Documentation only, per `work-orders/WO-2010-screenshot-analysis-pipeline.md`. This document specifies what a future rendering pipeline should do; it does not implement one. No image-processing code is written or run by this work order.

## Purpose

`work-orders/WO-2010`'s Objective states the gap directly: "Atlas Academy should analyze rendered maps rather than relying only on RPG Maker JSON." Every Atlas Academy artifact so far - observations, composition analyses, grades, composition reviews - is built entirely from map JSON, tileset data, and prose extraction reports. None has ever been checked against what the map actually looks like rendered. This document specifies the pipeline that would close that gap: what "rendering" means here, what already exists, and what a committed, reusable version would need beyond what exists today.

## What Already Exists (Real Precedent, Not Hypothetical)

A rendering pipeline is not a new idea for this project - it has already been run twice, for real, outside Atlas Academy:

- `rpgmakerLSP/reports/atlas-import/wo-0035-map002-render.png`
- `rpgmakerLSP/reports/atlas-import/wo-0036-map001-render.png`

Both are described in their respective build reports as an **"engine-faithful render"**, generated from the actual map JSON and tileset data using RPG Maker MZ's own autotile composition rules (`wo-0036-gate-a-ashford-exterior-production-map.md` cites "A2/A3/A4/B autotile rendering per `rmmz_core.js` tables" directly). This is real, working capability - not a proposal. Its documented limitation is what this work order exists to address: per that same report's own "Files Created" section, the render script "ran from the session scratchpad (not left in any repo), so it cannot be re-run over the hand-authored map." The rendering *logic* has already been proven twice; what does not exist yet is a **committed, reusable, re-runnable tool** any future Academy pass could invoke on demand.

## Three Distinct Image Types, Not One

This pipeline must keep three categories of image separate, because they carry entirely different evidentiary weight, and blurring them is the single most likely failure mode for a screenshot-analysis system:

1. **Engine-faithful renders** - generated deterministically from real map JSON and tileset data (the WO-0035/WO-0036 precedent above). The image is a visual reproduction of real, existing data; the underlying source of truth remains the JSON, and the render is a second, human-readable view of the same facts, not a new source of facts.
2. **Live gameplay screenshots** - captured from the actual running, built game. These can show things a static JSON-derived render cannot: animation state, lighting/tint overlays, UI, camera framing, and anything else only visible at runtime. See `academy/screenshot-guidelines.md` for capture requirements.
3. **Generated concept art** - AI image generation used for mood boards or visual direction. `bridges/rpg-maker-mz/map-quality-standard.md`'s existing "Image Generation Role" section already governs this category directly: "Image generation may be used for concept art, composition reference, mood boards, or visual direction. Image generation must not be treated as direct RPG Maker map data." **This pipeline does not change that rule and does not extend Academy's image-analysis discipline to generated concept art at all** - a generated image is a creative-direction input, never review evidence, and `academy/image-analysis.md` does not apply to it.

## Pipeline Stages

1. **Input.** Real map JSON (`data/MapXXX.json`) and its tileset data (`data/Tilesets.json`), exactly as `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md` already requires for any extraction pass. No other input is treated as ground truth.
2. **Render.** Deterministic autotile composition, per the WO-0035/WO-0036 precedent's own method (RPG Maker MZ's `rmmz_core.js` autotile tables). Given the same map JSON and tileset data, a render must be reproducible - the same input always produces the same output image, so a render can be regenerated after a map changes and meaningfully diffed against a prior pass.
3. **Capture (for live gameplay screenshots only).** Per `academy/screenshot-guidelines.md` - not part of the deterministic render stage, since a live screenshot depends on runtime state (camera position, animation frame, lighting) a render does not.
4. **File.** Per `academy/screenshot-guidelines.md`'s naming and metadata convention, so a stored image is traceable back to the exact map, commit/date, and render-vs-capture provenance that produced it.
5. **Analyze.** Per `academy/image-analysis.md` - a human or future AI reviewer examines the filed image against a specific, narrow set of questions the JSON-only pipeline cannot answer well, never as a replacement for JSON-grounded structural facts.

## What a Committed Tool Would Need Beyond the WO-0035/WO-0036 Precedent

Recorded here as a specification for future implementation work, not built by this documentation-only work order:

- Live in a versioned location (`tools/`, per this project's existing convention), not a session scratchpad, so it can be re-run on demand against any map, not only the one it was written for.
- Take a map JSON path as an argument and produce a deterministic image, with no manual per-map setup.
- Record its own provenance in the output filename or a sidecar record (map path, commit/date, tileset version) per `academy/screenshot-guidelines.md`.
- Use only data already required by `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md` - it introduces no new ground-truth source, only a new view of the existing one.

## Non-Goals

- Does not implement a rendering tool or any image-processing code.
- Does not re-run or modify the existing `wo-0035-map002-render.png` / `wo-0036-map001-render.png` renders.
- Does not change `bridges/rpg-maker-mz/map-quality-standard.md`'s "Image Generation Role" section.
- Does not modify `TheLastSwordProtocol-Atlas`, `TheLastSwordProtocol-Game`, or any map.

## References

- `academy/image-analysis.md`, `screenshot-guidelines.md`
- `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`
- `bridges/rpg-maker-mz/map-quality-standard.md`
- `rpgmakerLSP/reports/atlas-import/wo-0035-gate-a-map002-build-report.md`, `wo-0036-gate-a-map001-build-report.md` (read-only precedent)
- `reports/academy/screenshot-analysis-design.md`
- Created by `work-orders/WO-2010-screenshot-analysis-pipeline.md`
