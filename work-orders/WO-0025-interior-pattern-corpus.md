---
work_order_id: WO-0025
title: Interior Pattern Corpus
status: submitted
project: atlasstudio
recommended_agent: claude-code
agent_role: senior-software-architect
risk_level: low
player_facing: false
engine_specific: true
required_capabilities:
  - documentation
  - architecture-review
preferred_capabilities:
  - qa-review
produces:
  - design-patterns.interior.house.v1_0
  - design-patterns.interior.inn.v1_0
  - design-patterns.interior.weapon_shop.v1_0
  - design-patterns.interior.armor_shop.v1_0
  - design-patterns.interior.bar.v1_0
  - design-patterns.interior.chief_house.v1_0
  - report.interior_pattern_corpus_review
created: 2026-07-08
---

# WO-0025 - Interior Pattern Corpus

## Purpose

`WO-0024` created the Design Pattern Library's framework and seeded it with exactly one pattern (`interiors/shop.pattern.md`), derived from a single official sample map. This work order expands the library by analyzing the remaining seven official RPG Maker MZ interior sample maps - House 1, House 2, Inn, Weapon Shop, Armor Shop, Bar, and Chief's House - producing one reusable pattern document per interior type, comparing each against the existing Shop pattern to determine which layout, composition, passability, and event rules actually recur across building types versus which are specific to one, and reviewing whether the new corroborating evidence justifies promoting `shop.pattern.md`'s confidence from Medium to High.

This work order extracts reusable design patterns only. It does not produce implementation guidance for `The Last Sword Protocol`.

## Player-Facing Goal

Indirect. A broader, better-corroborated pattern library makes future interior builds (houses, inns, shops, bars, notable-NPC residences) more likely to read as polished and intentional on the first pass, the same way `WO-0024`'s single shop pattern was scoped to do - but this work order itself changes no game file and ships no player-visible content.

## Background

`WO-0024` established the Design Pattern Library's schema (`PATTERN_SCHEMA.md`), extraction method (`PATTERN_EXTRACTION_GUIDE.md`), confidence model (`PATTERN_CONFIDENCE_MODEL.md`), and review process (`PATTERN_REVIEW_PROCESS.md`), and produced the library's first pattern, `interiors/shop.pattern.md`, derived from one sample map (`Map021.json`, "Item Shop") and filed at `confidence: medium` per the confidence model's single-source bar. `WO-0024` explicitly scoped itself to framework-plus-one-pattern and named populating the rest of the library as future work.

The official RPG Maker MZ sample project, already imported into `TheLastSwordProtocol-Game/data/` as part of the "Village 1" interior set (`MapInfos.json` IDs 17-25), contains seven further interior sample maps beyond the Item Shop: House 1 (`Map018`), House 2 (`Map019`), Inn (`Map020`), Weapon & Armor Shop (`Map022`), Bar (`Map023`), and the two-floor Chief's House (`Map024`/`Map025`). This work order analyzes all seven, following the same extraction discipline `WO-0024` established, and produces one pattern document per requested interior type (six documents total, since Weapon Shop and Armor Shop are both drawn from the single combined `Map022` and Chief's House's two floors are one building).

## Scope

### In Scope

- Extracting all seven remaining official sample interior maps, following `PATTERN_EXTRACTION_GUIDE.md`.
- Producing one pattern document per requested type: `house.pattern.md`, `inn.pattern.md`, `weapon-shop.pattern.md`, `armor-shop.pattern.md`, `bar.pattern.md`, `chief-house.pattern.md`, each conforming to `PATTERN_SCHEMA.md`.
- Comparing every new pattern against `interiors/shop.pattern.md` to determine recurring layout rules, recurring composition rules, recurring passability rules, and recurring event conventions.
- Reviewing `shop.pattern.md` in light of the new evidence and producing a justified recommendation on whether its confidence should remain Medium or be promoted to High.
- Producing `reports/design-patterns/interior-pattern-corpus-review.md` documenting the comparison and the confidence recommendation.

### Out of Scope

- Creating implementation guidance, briefs, or contracts for `The Last Sword Protocol`.
- Modifying `TheLastSwordProtocol-Atlas` in any way.
- Modifying `TheLastSwordProtocol-Game` in any way.
- Modifying any existing implementation contract under `reports/implementation-contracts/`.
- Automatically promoting `shop.pattern.md`'s confidence field - the review may recommend promotion, but this work order does not itself apply that change (see the review report's Confidence Review section for the reasoning).
- Analyzing any category beyond interiors (exteriors, dungeons, towns, transitions remain future work).
- Writing or modifying any code.

## Inputs

- `TheLastSwordProtocol-Game/data/Map018.json` ("House 1"), `Map019.json` ("House 2"), `Map020.json` ("Inn"), `Map021.json` ("Item Shop", read-only for comparison), `Map022.json` ("Weapon & Armor Shop"), `Map023.json` ("Bar"), `Map024.json` ("Chief's House 1F"), `Map025.json` ("Chief's House 2F"), `Map017.json` ("Village 1", context), `MapInfos.json`, `Tilesets.json`.
- `studio/design-patterns/PATTERN_SCHEMA.md`, `PATTERN_EXTRACTION_GUIDE.md`, `PATTERN_CONFIDENCE_MODEL.md`, `PATTERN_REVIEW_PROCESS.md`, `README.md` (all `WO-0024` deliverables).
- `studio/design-patterns/interiors/shop.pattern.md` (comparison baseline, read-only).
- `bridges/rpg-maker-mz/passability-rule.md`, `bridges/rpg-maker-mz/map-quality-standard.md`.
- `work-orders/WO-0024-design-pattern-library.md`.

## Deliverables

- `studio/design-patterns/interiors/house.pattern.md`
- `studio/design-patterns/interiors/inn.pattern.md`
- `studio/design-patterns/interiors/weapon-shop.pattern.md`
- `studio/design-patterns/interiors/armor-shop.pattern.md`
- `studio/design-patterns/interiors/bar.pattern.md`
- `studio/design-patterns/interiors/chief-house.pattern.md`
- `reports/design-patterns/interior-pattern-corpus-review.md`
- `work-orders/WO-0025-interior-pattern-corpus.md`

## Acceptance Criteria

- Each of the six new pattern documents conforms to `PATTERN_SCHEMA.md`: complete frontmatter and all thirteen required body sections (Name, Category, Source, Confidence, Observed Maps, Applicable Genres, Required Conditions, Layout Rules, Composition Rules, Passability Rules, Event Rules, Common Mistakes, References).
- Each pattern document cites its exact source map(s) by path and abstracts findings into reusable principles - no pattern document reproduces a source map's tile grid, coordinates as prescriptive instruction, or raw JSON.
- Each pattern document's `confidence` field matches what `PATTERN_CONFIDENCE_MODEL.md`'s bar actually supports given its evidence: two independent corroborating maps may be filed at High (`house.pattern.md`); a single map, or a map shared with another pattern, or two floors of one building, is filed at Medium with an explicit evidentiary caveat stated in its Confidence section (`inn.pattern.md`, `weapon-shop.pattern.md`, `armor-shop.pattern.md`, `bar.pattern.md`, `chief-house.pattern.md`).
- `weapon-shop.pattern.md` and `armor-shop.pattern.md` each state explicitly that they are derived from the same single shared source map (`Map022.json`), not from two independent buildings.
- `chief-house.pattern.md` states explicitly that its two source maps are two floors of one building, not two independent buildings.
- `reports/design-patterns/interior-pattern-corpus-review.md` states recurring layout rules, recurring composition rules, recurring passability rules, and recurring event conventions found across the corpus, distinguishing what is universal from what is specific to one building type - including at least one case where a new sample directly overrides or narrows an existing `shop.pattern.md` rule (the wall-anchoring composition rule, shown not to hold for `bar.pattern.md`).
- The review report reviews `shop.pattern.md` and produces an explicit, justified recommendation on whether its confidence should remain Medium or be promoted to High, grounded in a rule-by-rule comparison against at least one new corroborating or non-corroborating map - and the recommendation is not automatically applied to `shop.pattern.md` itself.
- `shop.pattern.md` is not modified by this work order.
- No file under `reports/implementation-contracts/` is modified.
- No file under `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` is modified.
- Documentation only: no code is added or modified.
- The Immutable Formatting Rule is preserved: no existing file is reformatted.
- This work order is marked `submitted`.

## Verification Steps

```bash
find studio/design-patterns/interiors -name "*.md"
find reports/design-patterns -name "interior-pattern-corpus-review.md"
find work-orders -name "WO-0025-interior-pattern-corpus.md"
python3 tools/atlas_format/format_guard.py --check
git diff --stat -- studio/design-patterns/interiors/shop.pattern.md
# expect no output: shop.pattern.md is reviewed but not modified by this work order
git diff --stat -- reports/implementation-contracts
# expect no output: no implementation contract is touched by this work order
git -C ../TheLastSwordProtocol-Atlas status --porcelain
git -C ../TheLastSwordProtocol-Game status --porcelain
# expect no changes attributable to this work order in either sibling repository
```

## Allowed Changes

- `studio/design-patterns/interiors/house.pattern.md`
- `studio/design-patterns/interiors/inn.pattern.md`
- `studio/design-patterns/interiors/weapon-shop.pattern.md`
- `studio/design-patterns/interiors/armor-shop.pattern.md`
- `studio/design-patterns/interiors/bar.pattern.md`
- `studio/design-patterns/interiors/chief-house.pattern.md`
- `reports/design-patterns/interior-pattern-corpus-review.md`
- `work-orders/WO-0025-interior-pattern-corpus.md`

## Protected Areas

- Do not modify `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game`.
- Do not modify AtlasStudio canon.
- Do not modify `studio/design-patterns/interiors/shop.pattern.md`, `README.md`, `PATTERN_SCHEMA.md`, `PATTERN_EXTRACTION_GUIDE.md`, `PATTERN_CONFIDENCE_MODEL.md`, or `PATTERN_REVIEW_PROCESS.md` - reference them, do not restate or alter their rules.
- Do not modify any file under `reports/implementation-contracts/`.
- Do not write or modify code.
- Do not produce implementation guidance for `The Last Sword Protocol`.
- Preserve the Immutable Formatting Rule.

## Notes for Assigned Agent

The hardest judgment call in this work order is evidentiary honesty under pressure to fill in six named deliverables from only five genuinely distinct source maps (Weapon & Armor Shop is one map serving two requested pattern names; Chief's House 1F/2F is one building serving one requested pattern name but from two files). Resist the temptation to round a shared or same-building source up to full independent-corroboration status - `PATTERN_CONFIDENCE_MODEL.md` already draws this distinction (High requires *independent* corroboration), and `house.pattern.md`'s two genuinely independent buildings should read as visibly stronger evidence than `weapon-shop.pattern.md`/`armor-shop.pattern.md`'s or `chief-house.pattern.md`'s shared-source patterns. State every caveat explicitly in the affected pattern's own Confidence section rather than letting it default silently to a stronger-sounding Medium.

On the `shop.pattern.md` confidence question specifically: the work order brief is explicit that a recommendation, not an automatic promotion, is required. Even if the evidence clearly supports High (it does - see the review report), leave `shop.pattern.md` itself untouched and record the recommendation and its full justification in the review report instead, since `shop.pattern.md` is not in this work order's Deliverables or Allowed Changes.

## Submission Record

Submitted 2026-07-08 by Claude Code.

Delivered:

- `studio/design-patterns/interiors/house.pattern.md` (`PAT-INTERIOR-HOUSE v1.0`, `confidence: high`) - derived from two independent official sample maps (House 1, House 2), the corpus's strongest-evidenced new pattern. Documents the domestic-interior convention: same shell/threshold/event family as `shop.pattern.md`, but markedly lower decoration density, a continuous back-wall shelf run instead of side clusters, and no bilateral merchandise-cluster requirement.
- `studio/design-patterns/interiors/inn.pattern.md` (`PAT-INTERIOR-INN v1.0`, `confidence: medium`) - derived from one sample map (Inn). First pattern in the corpus to document a genuine multi-zone building: an off-center door aligned to the common room's own sub-axis, a chokepoint-connected guest-quarters wing with repeated bed-nook partitions, and the corpus's first wall-mounted (non-floor-adjacent) decorative flame.
- `studio/design-patterns/interiors/weapon-shop.pattern.md` and `studio/design-patterns/interiors/armor-shop.pattern.md` (`PAT-INTERIOR-WEAPON-SHOP v1.0`, `PAT-INTERIOR-ARMOR-SHOP v1.0`, both `confidence: medium` with an explicit shared-single-source caveat) - both derived from the one combined "Weapon & Armor Shop" sample map, each documenting a distinct display convention observed within it (individually spaced wall-mounted racks versus a compact secondary counter display). Each document states plainly that it does not have independent single-purpose-map corroboration.
- `studio/design-patterns/interiors/bar.pattern.md` (`PAT-INTERIOR-BAR v1.0`, `confidence: medium`) - derived from one sample map (Bar). The corpus's clearest counterexample to `shop.pattern.md`'s wall-anchoring rule: documents a floating-furniture-island composition convention appropriate to social/seating spaces, and an off-center door with no structural cause.
- `studio/design-patterns/interiors/chief-house.pattern.md` (`PAT-INTERIOR-CHIEF-HOUSE v1.0`, `confidence: medium` with an explicit same-building-two-floor caveat) - derived from both floors of the Chief's House. The corpus's only multi-floor pattern: a three-tile internal staircase, a symmetric formal ground-floor hall, and a true multi-room chamber layout on the upper floor, distinct from the Inn's chokepoint-only zoning.
- `reports/design-patterns/interior-pattern-corpus-review.md` - full comparative evidence: source data table, a note on why transfer-target map IDs are treated as structural artifacts rather than meaningful destinations, recurring layout/composition/passability/event findings (including the wall-anchoring override found in the Bar), a pattern-by-pattern comparison table against `shop.pattern.md`, and a rule-by-rule corroboration check of `shop.pattern.md` against the Weapon & Armor Shop map. Concludes that promotion to High is evidentially justified, explicitly recommends it with the exact frontmatter/body changes a follow-up action should make, and explicitly does not apply that change itself, consistent with this work order's "do not automatically promote confidence" instruction and `shop.pattern.md` being outside this work order's Allowed Changes.
- This work order, marked `submitted`.

`shop.pattern.md` was reviewed but not modified - confirmed directly (not present in this work order's diff). No file under `reports/implementation-contracts/` was modified. No file in `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` was modified - both were read-only (map JSON and tileset data inspected for extraction only). No AtlasStudio canon file was modified. No code was written or modified. No implementation guidance for `The Last Sword Protocol` was produced - every pattern document and the review report describe reusable RPG Maker layout principles only.

Formatting: preserved existing house style; no existing file was reformatted. All deliverables are new files.

Verification performed:

```bash
find studio/design-patterns/interiors -name "*.md"
find reports/design-patterns -name "interior-pattern-corpus-review.md"
find work-orders -name "WO-0025-interior-pattern-corpus.md"
git diff --stat -- studio/design-patterns/interiors/shop.pattern.md
git diff --stat -- reports/implementation-contracts
git -C ../TheLastSwordProtocol-Atlas status --porcelain
git -C ../TheLastSwordProtocol-Game status --porcelain
```
