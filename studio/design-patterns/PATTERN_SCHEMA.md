# Pattern Schema

## Purpose

Every pattern document in `studio/design-patterns/` must follow this schema. A consistent schema is what lets an implementation contract cite a pattern by name and version and have an implementing agent trust that the referenced document answers the same set of questions every time, in the same order, regardless of which category or agent authored it.

This schema defines structure and required content. It does not define the content of any individual pattern - see `PATTERN_EXTRACTION_GUIDE.md` for how to derive that content from an official sample map, and `interiors/shop.pattern.md` for a worked example.

## File Naming and Location

- One pattern per file, named `<pattern-name>.pattern.md`, in kebab-case.
- Filed under `studio/design-patterns/<category>/`, where `<category>` matches the pattern's `category` field (see below).
- A category directory is created the first time a pattern needs it. `interiors/` is the first category, seeded by this work order.

## Required Frontmatter

```yaml
---
pattern_id: PAT-INTERIOR-SHOP
name: Interior Pattern - Shop
version: 1.0
category: interior
status: accepted
confidence: high
observed_maps:
  - "TheLastSwordProtocol-Game/data/Map021.json (RPG Maker MZ official sample, Item Shop)"
applicable_genres:
  - jrpg
  - dragon-quest-style
source_report: "TheLastSwordProtocol-Game/reports/map-analysis/item-shop-analysis.md"
created: 2026-07-08
last_reviewed: 2026-07-08
---
```

Field notes:

- `pattern_id` - stable identifier, `PAT-<CATEGORY>-<SLUG>`, uppercase. Never reused for a different pattern, even after deprecation.
- `name` - human-readable name, matches the "Apply:" phrasing implementation contracts will cite (see `README.md`, "Future Integration").
- `version` - semantic-ish version, `MAJOR.MINOR`. See `PATTERN_REVIEW_PROCESS.md` for what triggers each.
- `category` - one of the top-level directories under `studio/design-patterns/` (`interior`, and future categories such as `exterior`, `dungeon`, `town`, `transition`).
- `status` - one of `proposed`, `accepted`, `deprecated`. See `PATTERN_REVIEW_PROCESS.md`.
- `confidence` - one of `high`, `medium`, `low`, `experimental`. See `PATTERN_CONFIDENCE_MODEL.md`.
- `observed_maps` - exact source paths/identifiers for every map this pattern was derived from. At minimum one entry; grows as more maps corroborate the pattern (see confidence model).
- `applicable_genres` - which project genres this pattern is meant for. Prevents, for example, a Zelda-style screen-chain pattern from being silently applied to a Dragon Quest-style project (see `bridges/rpg-maker-mz/map-quality-standard.md`).
- `source_report` - the AtlasStudio or sibling-repo report that performed the original extraction. This is the evidence trail; see `PATTERN_EXTRACTION_GUIDE.md`, "How to Cite Evidence."
- `created` / `last_reviewed` - ISO dates.

## Required Body Sections

Every pattern document body must contain the following sections, in this order:

### Name

A one-line restatement of the pattern's purpose in plain language. What kind of space is this, and what problem does the pattern solve.

### Category

Which category this pattern belongs to and why, if not obvious from the directory alone (for example, distinguishing a small shop interior from a general-purpose interior pattern).

### Source

Full citation of every observed map and the report that extracted it. Must match `observed_maps` and `source_report` in frontmatter, expanded with enough context (map name, dimensions, tileset) that a reader does not need to open the source report to know what was studied.

### Confidence

The current confidence level, restated from frontmatter, plus the justification: how many maps corroborate this pattern, and what would raise or lower the confidence level. See `PATTERN_CONFIDENCE_MODEL.md`.

### Observed Maps

A short table or list: map identifier, source project, what specifically was observed there. If more than one map contributed, this section is where they are distinguished (which rule came from which map).

### Applicable Genres

Restated from frontmatter, with a one-line reason. A pattern derived from a Dragon-Quest-style regional exploration sample should say so explicitly, so it is not misapplied to a screen-chain dungeon crawler.

### Required Conditions

The preconditions that must be true before this pattern applies at all. Example: "the interior is a small single-room shop, not a multi-room general store" or "the screen has exactly one primary entrance." A pattern applied outside its required conditions is a misapplication, not a pattern failure.

### Layout Rules

Spatial rules: room shell proportions, door/entrance placement, aisle/lane structure, zone division (e.g. outer void, wall shell, entry threshold, center aisle, browse zone). Stated as principles ("center the entrance on the primary aisle unless there is a strong reason not to"), never as fixed coordinates from the source map.

### Composition Rules

Why the layout reads as balanced, believable, and intentional: focal points, object clustering, negative space usage, visual rhythm, left/right balance. This is the "why it looks good" counterpart to Layout Rules' "where things go."

### Passability Rules

Collision and reachability principles, grounded in `bridges/rpg-maker-mz/passability-rule.md`: which zones must be walkable, which must be blocked, the "reachability ring" requirement for interactable objects, and any route validation the pattern implies (see `bridges/rpg-maker-mz/passability-rule.md`, "Route Validation").

### Event Rules

What event behavior the pattern does or does not prescribe: doorway transfer conventions, decorative-vs-functional event distinction, and an explicit statement of what the pattern does **not** cover (for example: "this pattern teaches shop atmosphere and layout; it does not teach RPG Maker Shop Processing configuration").

### Common Mistakes

Concrete failure modes to avoid, phrased as mistakes, not restated rules. Example: "floating shelf tiles not terminated into a wall" rather than "shelves must terminate into walls" (already covered under Layout Rules).

### References

Links to every other document this pattern depends on or was cross-checked against: the source report, `bridges/rpg-maker-mz/passability-rule.md`, `bridges/rpg-maker-mz/map-quality-standard.md`, related patterns (via `[[pattern-name]]`-style reference), and the work order that created or last revised the pattern.

## Format Discipline

- Markdown only, no code generation, no RPG Maker JSON embedded in a pattern file.
- No tile coordinates from the source map may appear as prescriptive coordinates for future builds - coordinates are evidence in the source report, not instructions in the pattern (see `PATTERN_EXTRACTION_GUIDE.md`, "What Not to Infer").
- Preserve the Immutable Formatting Rule (`studio/immutable-formatting-rule.md`) when editing an existing pattern file: a version bump is a semantic change to the relevant sections, not a license to reformat the whole document.
