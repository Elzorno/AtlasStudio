# Pattern Application Guide

## Purpose

`README.md` (`WO-0024`) established a single-layer citation format for implementation contracts: `Apply: Interior Pattern - Shop v1.0 / Confidence: Medium`. That format works for a library with no hierarchy. It does not say what to do once a Specialization exists beneath a Category, or once a project needs its own narrow addition on top of a reusable pattern. This document extends that citation format to the multi-tier case `PATTERN_INHERITANCE_MODEL.md` and `PATTERN_RESOLUTION_RULES.md` define, and shows implementation contracts exactly how to write a citation an implementing agent can resolve without guessing.

This document does not replace `README.md`'s original citation format - a contract citing a single, unspecialized pattern with no project-specific layer may still write the simple one-line form. This document adds the form for when more than one layer is in play.

## The Citation Format

A multi-tier citation names every layer in the chain, from most general to most specific, and reports each layer's own confidence in the same order - never merged into one value, per `PATTERN_RESOLUTION_RULES.md`'s "Confidence Interactions."

```text
Apply:
  Environment Pattern: Interior
  Specialization: Item Shop
  Project Pattern: Ashford Village

Confidence:
  High / Medium / High
```

Reading this citation, an implementing agent should be able to determine, without asking a follow-up question:

- Which pattern document(s) govern each named layer (or, for a virtual layer, where that layer's evidence actually lives - see `PATTERN_INHERITANCE_MODEL.md`, "Materialized vs. Virtual Nodes").
- What confidence each layer carries, in the same left-to-right order as the layers themselves.
- That every rule in the resolved guidance is binding unless the citation itself states an explicit override or exception, per `PATTERN_RESOLUTION_RULES.md`.

## Required Elements of a Citation

1. **Every layer actually in the chain**, not just the most specific one. Omitting the Environment or Category layer because "the Specialization implies it" defeats the purpose of stating per-layer confidence and provenance - name every layer explicitly, even a virtual one.
2. **The exact pattern name and version for every materialized layer** (matching `README.md`'s original single-layer convention: name plus `vMAJOR.MINOR`).
3. **An explicit note when a layer is virtual**, naming where that layer's evidence lives instead of a pattern document (see the worked examples below).
4. **A confidence value per layer**, in the same order the layers are listed, matching each layer's own pattern document (or, for a virtual layer, the evidence source's own corroboration count per `PATTERN_CONFIDENCE_MODEL.md`).
5. **Any override or exception the citation itself introduces**, stated explicitly per `PATTERN_RESOLUTION_RULES.md`'s "Overrides" and "Exceptions" sections - never left implicit.

## Worked Example 1: A Chain That Exists Today

This example uses only materialized patterns already in the library - no hypothetical layers, so it is directly citable by a real contract today.

```text
Apply:
  Category Pattern: Shop (interiors/shop.pattern.md v1.0)
  Specialization: Weapon Shop (interiors/weapon-shop.pattern.md v1.0)

Confidence:
  Medium / Medium
```

Resolution (per `PATTERN_RESOLUTION_RULES.md`): start with `shop.pattern.md`'s Layout/Composition/Passability/Event rules as the base (compact shell, centered threshold, reachability ring, no-NPC-by-default, etc.), then layer `weapon-shop.pattern.md`'s local additions (individually spaced wall-mounted rack stock, the deeper wall cluster, the stricter centerline-to-focal-item rule) on top. Neither layer contradicts the other - `weapon-shop.pattern.md` narrows and adds, it does not override - so no explicit-override note is needed. Both layers report `Medium`, and the citation should flag both as single-source-with-caveat per `weapon-shop.pattern.md`'s own Confidence section (its evidence is a zone within a shared map, not an independent sample - see `PATTERN_INHERITANCE_MODEL.md`).

## Worked Example 2: A Chain Through a Virtual Layer

This example uses the exact chain named in this work order's brief. The Environment layer (`Interior`) is virtual - no `interior.pattern.md` exists - so the citation must say where that layer's evidence comes from instead of pointing at a file.

```text
Apply:
  Environment Pattern: Interior (virtual - evidence in reports/design-patterns/interior-pattern-corpus-review.md, "Recurring Layout/Composition/Passability/Event Rules")
  Specialization: Item Shop (currently collapsed onto interiors/shop.pattern.md v1.0 - see PATTERN_INHERITANCE_MODEL.md, "The Shop / Item Shop Double Duty")

Confidence:
  High / Medium
```

Resolution: the `Interior` layer contributes the cross-cutting rules the corpus review corroborated across all eight analyzed interiors (shell-plus-void construction, the threshold stack, no-NPC-by-default, region-free passability) - corroborated by eight samples, which comfortably clears `PATTERN_CONFIDENCE_MODEL.md`'s two-or-more-sample bar for High. The `Item Shop` layer contributes everything in `shop.pattern.md` (since, per `PATTERN_INHERITANCE_MODEL.md`, Item Shop has no local rules distinct from Shop), reported at `shop.pattern.md`'s own current `Medium`. No third, Project-specific layer is cited here, so none is reported.

## Worked Example 3: A Fully Hypothetical Three-Layer Chain

This is the citation shown in this work order's brief, in full, with every hypothetical element clearly labeled as such. **No `Ashford Village` pattern exists in the library today** - this example illustrates the format a future project-specific pattern would use, not a citation any contract can actually make yet.

```text
Apply:
  Environment Pattern: Interior (virtual - evidence in reports/design-patterns/interior-pattern-corpus-review.md)
  Specialization: Item Shop (collapsed onto interiors/shop.pattern.md v1.0)
  Project Pattern: Ashford Village (HYPOTHETICAL - no such document exists; illustrates studio/design-patterns/projects/the-last-sword-protocol/ashford-village.pattern.md, a location not yet authored)

Confidence:
  High / Medium / High
```

The third layer's `High` in this illustration is not a claim about any real evidence - it stands in for what a Project-specific layer's confidence *would* report if, hypothetically, Ashford Village's shop interior had already been hand-built and playtested against `shop.pattern.md`'s acceptance criteria without deviation, which `PATTERN_CONFIDENCE_MODEL.md` would treat as a legitimate accepted-build corroboration. As of this document, Ashford Village's shop (`reports/implementation-contracts/ashford-shop-build-contract.md`, `WO-0020`) has not yet been built or playtested, so no such confidence value can honestly be reported today. A real citation of this chain, written now, would state the Project layer as **not yet authored** rather than assert a confidence value for it.

## What a Citation Must Not Do

- Must not merge per-layer confidence into a single number (`PATTERN_RESOLUTION_RULES.md`).
- Must not cite a Specialization without its Category, or a Project-specific layer without the Specialization (or Category) it customizes - every intermediate layer in the chain must be named, not skipped.
- Must not assert a confidence value for a layer that does not yet exist, the way Worked Example 3 explicitly avoids doing for the real (non-hypothetical) case.
- Must not silently apply an override - any deviation from an inherited rule must be stated in the citation itself, per `PATTERN_RESOLUTION_RULES.md`'s "Overrides."

## Future Integration

### Implementation Contracts

Implementation contracts should adopt the multi-tier citation format above whenever more than one layer is in play, placed in the same section `ashford-shop-build-contract.md` (`WO-0020`) already uses for citing `IMP-HOM-019` and other authoritative sources - patterns are one more authoritative source among the ones a contract already cites, not a separate concern. Until a Pattern Validator exists (see below), the contract author is responsible for manually walking `PATTERN_RESOLUTION_RULES.md`'s five-step pipeline and stating the resolved result; the citation format above is what makes that manual work checkable by a reviewer.

### Pattern Validator (future tool, not built by this work order)

A future Pattern Validator should consume `schemas/design-pattern.schema.json` and `PATTERN_RESOLUTION_RULES.md` to:

- Mechanically walk a citation's `parent_pattern` chain and confirm every named layer exists (materialized) or is explicitly flagged virtual with a stated evidence source.
- Confirm every entry in a pattern's `exceptions` field names a real ancestor rule, per `PATTERN_RESOLUTION_RULES.md`'s "Overrides."
- Confirm a pattern's stated `confidence` is consistent with its `evidence_count` and `observed_sources`, per `PATTERN_CONFIDENCE_MODEL.md`'s bars.
- Flag undeclared contradictions between a pattern's `local_rules` and any ancestor's `local_rules` it does not list in `exceptions`, per `PATTERN_RESOLUTION_RULES.md`'s fail-closed "Undeclared contradiction" rule.
- This is a validator in the same spirit as `tools/atlas_format/format_guard.py` and `tools/atlas_lint/` - it checks, it does not write or resolve on a human's behalf.

### Pattern Extraction Engine (future tool, not built by this work order)

A future Pattern Extraction Engine should consume `PATTERN_EXTRACTION_GUIDE.md` and this hierarchy to:

- Suggest a candidate `parent_pattern` for a newly extracted sample, based on its `category` and any already-materialized category/specialization patterns matching its structural signature.
- Populate `observed_sources` and compute a candidate `evidence_count` directly from the extraction's cited source map(s), applying `PATTERN_INHERITANCE_MODEL.md`'s independence distinction (a two-floor single building, like Chief's House, or a shared/split map, like Weapon & Armor Shop, should not automatically produce an `evidence_count` equal to the raw number of source files - see `schemas/design-pattern.schema.json`'s description of the field).
- Flag when accumulated cross-cutting evidence across several category-tier patterns (for example, several interior categories all corroborating the same rule) crosses `PATTERN_CONFIDENCE_MODEL.md`'s corroboration bar for a virtual environment-tier node, surfacing a recommendation to materialize that node - the mechanism `reports/design-patterns/interior-pattern-corpus-review.md`'s findings already anticipate for `Interior`.

## References

- `studio/design-patterns/README.md` - the original single-layer citation format this document extends.
- `studio/design-patterns/PATTERN_INHERITANCE_MODEL.md` - the hierarchy being cited.
- `studio/design-patterns/PATTERN_RESOLUTION_RULES.md` - the resolution procedure a citation invokes.
- `studio/design-patterns/PATTERN_CONFIDENCE_MODEL.md` - per-layer confidence definitions.
- `schemas/design-pattern.schema.json` - machine-checkable pattern fields a future validator would use.
- `reports/implementation-contracts/ashford-shop-build-contract.md` - precedent for how a contract cites authoritative sources, extended here to patterns.
- `reports/design-patterns/inheritance-examples.md` - additional worked examples.
- Created by `work-orders/WO-0026-design-pattern-inheritance-model.md`.
