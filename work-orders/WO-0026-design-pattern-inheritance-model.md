---
work_order_id: WO-0026
title: Design Pattern Inheritance Model
status: submitted
project: atlasstudio
recommended_agent: claude-code
agent_role: senior-software-architect
risk_level: low
player_facing: false
engine_specific: true
required_capabilities:
  - architecture-review
  - schema-design
  - documentation
preferred_capabilities:
  - qa-review
produces:
  - design-patterns.inheritance_model
  - design-patterns.resolution_rules
  - design-patterns.application_guide
  - schema.design_pattern
  - report.inheritance_examples
created: 2026-07-08
---

# WO-0026 - Design Pattern Inheritance Model

## Purpose

`WO-0024` built the Design Pattern Library's framework and its first pattern. `WO-0025` populated it with seven interior patterns and, in the process, produced relationships the framework had no formal language for: specializations (`Weapon Shop`/`Armor Shop` under `Shop`), a rule one pattern explicitly contradicts in another (`Bar` versus `Shop`'s wall-anchoring rule), and a cluster of rules that recur across every interior analyzed so far but belong to no single document (the corpus review's "Recurring" findings). Before the library grows into overworlds, dungeons, and further interiors - each of which will multiply these same relationships - this work order defines the architecture that governs how patterns relate to, inherit from, and override one another.

This work order defines architecture. It adds no new pattern.

## Player-Facing Goal

Indirect. A well-architected inheritance model prevents the pattern library from becoming an unmanageable flat list of documents with silently duplicated or silently contradictory rules as it grows - which in turn keeps future interior, overworld, and dungeon builds grounded in consistent, traceable guidance rather than ad hoc rediscovery. This work order itself changes no game file and ships no player-visible content.

## Background

Review: `work-orders/WO-0024-design-pattern-library.md`, `work-orders/WO-0025-interior-pattern-corpus.md`.

Review: `studio/design-patterns/README.md`, `PATTERN_SCHEMA.md`, `PATTERN_CONFIDENCE_MODEL.md`, `PATTERN_REVIEW_PROCESS.md`, `interiors/*.pattern.md` (all seven), `reports/design-patterns/interior-pattern-corpus-review.md`.

`WO-0024` established the schema (`PATTERN_SCHEMA.md`), extraction method (`PATTERN_EXTRACTION_GUIDE.md`), confidence model (`PATTERN_CONFIDENCE_MODEL.md`), and review process (`PATTERN_REVIEW_PROCESS.md`), seeded with one pattern (`interiors/shop.pattern.md`). `WO-0025` added six more patterns (`house.pattern.md`, `inn.pattern.md`, `weapon-shop.pattern.md`, `armor-shop.pattern.md`, `bar.pattern.md`, `chief-house.pattern.md`) and, in its comparative review, found: rules that recur across nearly every interior regardless of type (a candidate for a level above any single pattern); two patterns (`weapon-shop.pattern.md`, `armor-shop.pattern.md`) that specialize a third (`shop.pattern.md`) without a formal specialization mechanism to express that; and one pattern (`bar.pattern.md`) that explicitly states it "overrides" another's rule despite neither being the other's ancestor - a relationship the existing framework has no vocabulary for. `WO-0025`'s review report also recommended, but explicitly did not apply, promoting `shop.pattern.md`'s confidence to High; this work order does not act on that recommendation either.

## Scope

### In Scope

- Defining a hierarchy for patterns (Environment / Category / Specialization / Project-specific tiers), including parent/child relationships, specialization, shared behavior, override behavior, and future extensibility (`PATTERN_INHERITANCE_MODEL.md`).
- Specifying exactly how multiple pattern layers combine into one resolved implementation guidance: precedence, conflict resolution, overrides, exceptions, and confidence interactions (`PATTERN_RESOLUTION_RULES.md`).
- Describing how implementation contracts should reference a multi-layer pattern chain, with worked examples (`PATTERN_APPLICATION_GUIDE.md`).
- Defining a JSON Schema for pattern documents covering `pattern_id`, `version`, `parent_pattern`, `category`, `confidence`, `evidence_count`, `observed_sources`, `exceptions`, `applicable_conditions`, `inherited_rules`, `local_rules`, and `references` (`schemas/design-pattern.schema.json`).
- Producing worked inheritance examples: House inherits Interior; Item Shop inherits Shop; Shop inherits Interior; Bar overrides Shop wall-anchoring; a fully hypothetical future Dungeon example (`reports/design-patterns/inheritance-examples.md`).
- Describing how Implementation Contracts, a future Pattern Validator, and a future Pattern Extraction Engine should consume this model.
- Adding a single, narrowly-scoped References-section pointer to `PATTERN_INHERITANCE_MODEL.md` in each of the seven existing `interiors/*.pattern.md` files, per this work order's own explicit exception to "do not modify existing patterns."

### Out of Scope

- Adding any new pattern document (no `interior.pattern.md`, no dungeon patterns, no Ashford Village project pattern - every example requiring one of these is explicitly illustrative/hypothetical, not delivered).
- Modifying `TheLastSwordProtocol-Atlas` in any way.
- Modifying `TheLastSwordProtocol-Game` in any way.
- Modifying any existing pattern beyond the single References-section pointer described above - no rule text, frontmatter field, or confidence value in any of the seven `interiors/*.pattern.md` files changes.
- Promoting `shop.pattern.md`'s confidence from Medium to High, despite `WO-0025`'s review report recommending it - this work order restates that recommendation accurately (in `reports/design-patterns/inheritance-examples.md`, Example 3) but does not apply it.
- Redesigning `PATTERN_SCHEMA.md`, `PATTERN_CONFIDENCE_MODEL.md`, `PATTERN_REVIEW_PROCESS.md`, or `README.md` - this work order does not modify any of the four `WO-0024` framework documents.
- Building the Pattern Validator or Pattern Extraction Engine named in "Future Integration" - both are named and scoped, not implemented, matching the precedent `WO-0021`/`WO-0022` set for the Work Order Router before `WO-0023` implemented it.
- Writing or modifying any code.

## Inputs

- `work-orders/WO-0024-design-pattern-library.md`, `work-orders/WO-0025-interior-pattern-corpus.md`.
- `studio/design-patterns/README.md`, `PATTERN_SCHEMA.md`, `PATTERN_CONFIDENCE_MODEL.md`, `PATTERN_REVIEW_PROCESS.md`, `interiors/shop.pattern.md`, `house.pattern.md`, `inn.pattern.md`, `weapon-shop.pattern.md`, `armor-shop.pattern.md`, `bar.pattern.md`, `chief-house.pattern.md`.
- `reports/design-patterns/interior-pattern-corpus-review.md`.
- `schemas/work-order-routing.schema.json`, `schemas/agent-status.schema.json` (existing JSON Schema style conventions this work order's schema follows).
- `studio/orchestration/work-order-router.md` (`WO-0021` precedent for fail-closed handling of ambiguity, reused in `PATTERN_RESOLUTION_RULES.md`).

## Deliverables

- `studio/design-patterns/PATTERN_INHERITANCE_MODEL.md`
- `studio/design-patterns/PATTERN_RESOLUTION_RULES.md`
- `studio/design-patterns/PATTERN_APPLICATION_GUIDE.md`
- `schemas/design-pattern.schema.json`
- `reports/design-patterns/inheritance-examples.md`
- `work-orders/WO-0026-design-pattern-inheritance-model.md`
- One References-section addition each to `studio/design-patterns/interiors/shop.pattern.md`, `house.pattern.md`, `inn.pattern.md`, `weapon-shop.pattern.md`, `armor-shop.pattern.md`, `bar.pattern.md`, `chief-house.pattern.md`.

## Acceptance Criteria

- `PATTERN_INHERITANCE_MODEL.md` defines a hierarchy (Environment / Interior, Town, Overworld, Dungeon; Category; Specialization; Project-specific) matching the brief's example shape, and documents parent/child relationships, specialization, shared behavior, override behavior, and future extensibility.
- `PATTERN_INHERITANCE_MODEL.md` states honestly, for every existing pattern, which hierarchy tier it currently occupies, including the two known architectural gaps this work order surfaces rather than silently resolves: `shop.pattern.md`'s double duty as both the `Shop` category and the (undocumented) `Item Shop` specialization, and the fact that no `Interior` environment-tier document exists yet.
- `PATTERN_RESOLUTION_RULES.md` specifies precedence, conflict resolution (including a fail-closed rule for undeclared contradictions, mirroring `work-order-router.md`'s ambiguity handling), overrides, exceptions, and confidence interactions, and states explicitly that confidence values are reported per layer, never merged into one number.
- `PATTERN_APPLICATION_GUIDE.md` describes the multi-layer citation format and gives at least three worked examples, at least one of which uses only patterns that exist in the library today (no hypothetical layer) and at least one of which is explicitly labeled hypothetical where it uses a Project-specific layer that does not yet exist.
- `schemas/design-pattern.schema.json` is valid JSON Schema (2020-12), matches the style of `schemas/work-order-routing.schema.json` and `schemas/agent-status.schema.json`, and includes `pattern_id`, `version`, `parent_pattern`, `category`, `confidence`, `evidence_count`, `observed_sources`, `exceptions`, `applicable_conditions`, `inherited_rules`, `local_rules`, and `references` as specified in the brief, without introducing structure beyond what those fields and the resolution rules require.
- `reports/design-patterns/inheritance-examples.md` contains all five requested examples (House inherits Interior; Item Shop inherits Shop; Shop inherits Interior; Bar overrides Shop wall-anchoring; a future Dungeon example), each stating plainly whether it reflects the library's real current state or a hypothetical future state.
- The Bar/Shop example correctly identifies that `Bar` and `Shop` are siblings, not parent and child, and reclassifies `bar.pattern.md`'s self-described "override" as a cross-branch clarification rather than a vertical override, without editing `bar.pattern.md`'s own wording beyond the permitted References-section pointer.
- "Future Integration" describes how Implementation Contracts, a future Pattern Validator, and a future Pattern Extraction Engine should consume the inheritance model, without implementing either tool.
- No existing pattern's frontmatter, rule text, or confidence value is modified - each of the seven `interiors/*.pattern.md` files gains exactly one new References-section bullet pointing at `PATTERN_INHERITANCE_MODEL.md` and nothing else changes.
- No confidence value anywhere in the library is promoted, including `shop.pattern.md`, despite `WO-0025`'s recommendation.
- `PATTERN_SCHEMA.md`, `PATTERN_CONFIDENCE_MODEL.md`, `PATTERN_REVIEW_PROCESS.md`, and `README.md` are not modified.
- No file under `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` is modified.
- Documentation only: no code is added or modified.
- The Immutable Formatting Rule is preserved: no existing file is reformatted beyond the single permitted addition per pattern file.
- This work order is marked `submitted`.

## Verification Steps

```bash
find studio/design-patterns -maxdepth 1 -name "PATTERN_INHERITANCE_MODEL.md" -o -maxdepth 1 -name "PATTERN_RESOLUTION_RULES.md" -o -maxdepth 1 -name "PATTERN_APPLICATION_GUIDE.md"
find schemas -name "design-pattern.schema.json"
find reports/design-patterns -name "inheritance-examples.md"
find work-orders -name "WO-0026-design-pattern-inheritance-model.md"
python3 -c "import json; json.load(open('schemas/design-pattern.schema.json')); print('valid json')"
git diff --stat -- studio/design-patterns/README.md studio/design-patterns/PATTERN_SCHEMA.md studio/design-patterns/PATTERN_CONFIDENCE_MODEL.md studio/design-patterns/PATTERN_REVIEW_PROCESS.md
# expect no output: the four WO-0024 framework documents are not modified
grep -c "confidence: high" studio/design-patterns/interiors/shop.pattern.md
# expect 0: shop.pattern.md's confidence remains medium, not promoted
python3 tools/atlas_format/format_guard.py --check
git -C ../TheLastSwordProtocol-Atlas status --porcelain
git -C ../TheLastSwordProtocol-Game status --porcelain
```

## Allowed Changes

- `studio/design-patterns/PATTERN_INHERITANCE_MODEL.md`
- `studio/design-patterns/PATTERN_RESOLUTION_RULES.md`
- `studio/design-patterns/PATTERN_APPLICATION_GUIDE.md`
- `schemas/design-pattern.schema.json`
- `reports/design-patterns/inheritance-examples.md`
- `work-orders/WO-0026-design-pattern-inheritance-model.md`
- References-section addition only, in `studio/design-patterns/interiors/shop.pattern.md`, `house.pattern.md`, `inn.pattern.md`, `weapon-shop.pattern.md`, `armor-shop.pattern.md`, `bar.pattern.md`, `chief-house.pattern.md`.

## Protected Areas

- Do not modify `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game`.
- Do not modify AtlasStudio canon.
- Do not modify `studio/design-patterns/README.md`, `PATTERN_SCHEMA.md`, `PATTERN_CONFIDENCE_MODEL.md`, or `PATTERN_REVIEW_PROCESS.md`.
- Do not modify any existing pattern file beyond the single permitted References-section addition - no rule text, frontmatter field, or confidence value may change.
- Do not promote any pattern's confidence value.
- Do not add any new pattern document.
- Do not redesign `schemas/design-pattern.schema.json` beyond the fields specified in this work order's brief and what the resolution rules require to be checkable.
- Do not write or modify code.
- Preserve the Immutable Formatting Rule.

## Notes for Assigned Agent

The hardest judgment call in this work order is resisting the pull to "clean up" the shape mismatches `WO-0025` left behind - `shop.pattern.md`'s double duty as both `Shop` and `Item Shop`, the missing `Interior` environment-tier document, and `bar.pattern.md`'s loosely-worded self-description as an "override" of a sibling's rule. This work order's job is to name these gaps precisely and define the model that will eventually close them, not to close them now. Splitting `shop.pattern.md`, authoring `interior.pattern.md`, or rewording `bar.pattern.md`'s Composition Rules section are all legitimate future work, explicitly out of scope here.

The Bar/Shop relationship deserves particular care: the brief asks for an example titled "Bar overrides Shop wall-anchoring," using the same word `bar.pattern.md` itself uses. Take the brief's framing at face value for the example's title, but do the harder work underneath it of showing precisely why "override" is not quite the right technical term given the actual hierarchy (siblings, not parent/child) - and introduce the vocabulary (`cross_branch_clarification` versus `vertical_override`) that makes the distinction checkable rather than a matter of prose interpretation. This is exactly the kind of correction a senior-architect-role agent should make explicit rather than paper over.

## Submission Record

Submitted 2026-07-08 by Claude Code.

Delivered:

- `studio/design-patterns/PATTERN_INHERITANCE_MODEL.md` - the four-tier hierarchy (Environment / Category / Specialization / Project-specific), a Current Library Mapping table stating honestly which existing pattern occupies which node (and which nodes are virtual), an explicit treatment of the `Shop`/`Item Shop` double duty, a "Materialized vs. Virtual Nodes" section defining how an unmaterialized parent is handled, parent/child/specialization/shared-behavior rules, and a two-relationship-type Override Behavior section distinguishing vertical override from cross-branch clarification - introduced specifically to correctly describe the Bar/Shop relationship.
- `studio/design-patterns/PATTERN_RESOLUTION_RULES.md` - a five-step resolution pipeline, a four-tier precedence order, three-way conflict resolution (declared vertical override, declared cross-branch clarification, undeclared contradiction - the last of which fails closed per `work-order-router.md`'s precedent rather than being silently resolved), explicit override and exception rules, and a "Confidence Interactions" section establishing that confidence is always reported per layer, never merged.
- `studio/design-patterns/PATTERN_APPLICATION_GUIDE.md` - the multi-layer citation format extending `README.md`'s original single-layer format, three worked examples (one fully real and citable today using `Shop -> Weapon Shop`; one through a virtual `Interior` layer; one fully hypothetical three-layer chain matching the brief's own example, with its Project-specific layer explicitly labeled as not-yet-authored rather than assigned an invented confidence value), and a "Future Integration" section naming a future Pattern Validator and Pattern Extraction Engine by responsibility, without implementing either.
- `schemas/design-pattern.schema.json` - valid JSON Schema (2020-12, `additionalProperties: false`, matching `schemas/work-order-routing.schema.json`'s style), covering every field named in the brief plus a small number of continuity fields retained from `PATTERN_SCHEMA.md`'s original frontmatter (`name`, `status`, `applicable_genres`, `source_report`, `created`, `last_reviewed`) needed for the schema to describe a complete pattern document rather than only its inheritance-specific fields. `exceptions` is a structured array distinguishing `vertical_override` from `cross_branch_clarification`, directly operationalizing the Bar/Shop distinction.
- `reports/design-patterns/inheritance-examples.md` - all five requested examples, each stating plainly whether it is real or hypothetical, plus a summary table. Example 2 (Item Shop inherits Shop) demonstrates that an empty `local_rules` array is a valid, meaningful specialization state rather than an error. Example 4 (Bar overrides Shop wall-anchoring) works through the sibling-versus-parent/child correction in full and explains what would need to change if `Interior` were ever materialized with wall-anchoring stated at that tier. Example 5 (future Dungeon) shows the model resolving to an intentionally empty result for a wholly unanalyzed category, rather than fabricating guidance.
- One References-section bullet added to each of `studio/design-patterns/interiors/shop.pattern.md`, `house.pattern.md`, `inn.pattern.md`, `weapon-shop.pattern.md`, `armor-shop.pattern.md`, `bar.pattern.md`, and `chief-house.pattern.md`, pointing at `PATTERN_INHERITANCE_MODEL.md`. No other line in any of these seven files was touched.
- This work order, marked `submitted`.

No new pattern document was added. `studio/design-patterns/README.md`, `PATTERN_SCHEMA.md`, `PATTERN_CONFIDENCE_MODEL.md`, and `PATTERN_REVIEW_PROCESS.md` were read but not modified - confirmed directly (not present in this work order's diff). No confidence value was promoted anywhere in the library - `shop.pattern.md` remains `confidence: medium`, confirmed directly; `WO-0025`'s promotion recommendation is restated accurately in `reports/design-patterns/inheritance-examples.md` but not applied. No file in `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` was modified - both were untouched (no read was even necessary for this work order, since it works entirely from AtlasStudio's own prior deliverables). No AtlasStudio canon file was modified. No code was written or modified.

Formatting: preserved existing house style; no existing file was reformatted beyond the single permitted References-section addition per pattern file, each a pure append with no reordering or re-indentation of surrounding content.

Verification performed:

```bash
find studio/design-patterns -maxdepth 1 -name "PATTERN_INHERITANCE_MODEL.md"
find studio/design-patterns -maxdepth 1 -name "PATTERN_RESOLUTION_RULES.md"
find studio/design-patterns -maxdepth 1 -name "PATTERN_APPLICATION_GUIDE.md"
find schemas -name "design-pattern.schema.json"
find reports/design-patterns -name "inheritance-examples.md"
python3 -c "import json; json.load(open('schemas/design-pattern.schema.json')); print('valid json')"
git diff --stat -- studio/design-patterns/README.md studio/design-patterns/PATTERN_SCHEMA.md studio/design-patterns/PATTERN_CONFIDENCE_MODEL.md studio/design-patterns/PATTERN_REVIEW_PROCESS.md
grep -c "confidence: high" studio/design-patterns/interiors/shop.pattern.md
git -C ../TheLastSwordProtocol-Atlas status --porcelain
git -C ../TheLastSwordProtocol-Game status --porcelain
```
