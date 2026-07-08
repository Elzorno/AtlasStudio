# Pattern Inheritance Model

## Purpose

`WO-0024` built the library's schema, extraction method, confidence model, and review process. `WO-0025` populated it with seven interior patterns and, in doing so, surfaced relationships the framework did not yet have language for: `weapon-shop.pattern.md` and `armor-shop.pattern.md` clearly specialize `shop.pattern.md`; `bar.pattern.md` clearly contradicts one of `shop.pattern.md`'s rules, on purpose; and every interior pattern shares a cluster of rules (shell-plus-void construction, the threshold stack, no-NPC-by-default, region-free passability) that belongs at a level no single pattern document currently occupies. This document defines the hierarchy that makes those relationships explicit, before the library grows into overworlds, dungeons, and additional interiors and those relationships become unmanageable to track informally.

This document defines architecture. It does not add, rewrite, or reformat any pattern.

## The Hierarchy

```text
Environment
    Interior
        House
        Shop
            Item Shop
            Weapon Shop
            Armor Shop
        Inn
        Bar
        Chief's House
    Town
    Overworld
    Dungeon
        Cave
        Ruins
        Castle
```

Three tiers matter for the inheritance model:

- **Environment tier** - the broadest classification a pattern belongs to (`interior`, `town`, `overworld`, `dungeon`). This tier is not a pattern document in its own right; it is the value of the `category` field every pattern already carries in its frontmatter (`PATTERN_SCHEMA.md`, established in `WO-0024`). Every existing pattern already declares `category: interior`, so no existing file needs to change to participate in this tier.
- **Category tier** - a building or location archetype within an environment (`House`, `Shop`, `Inn`, `Bar`, `Chief's House` within `interior`; `Cave`, `Ruins`, `Castle` would sit one level down within `dungeon` - see below). A category-tier pattern is a normal pattern document; it simply has no `parent_pattern` of its own yet, or points at a not-yet-materialized environment-tier document (see "Materialized vs. Virtual Nodes" below).
- **Specialization tier** - a narrower variant of a category, adding or overriding rules the category doesn't state (`Item Shop`, `Weapon Shop`, `Armor Shop` within `Shop`). A specialization-tier pattern sets `parent_pattern` to its category's `pattern_id`.

A fourth, project-specific tier sits below specialization and is described in its own section further down.

## Current Library Mapping

This table states, honestly, where each existing pattern (all authored before this document existed) actually sits in the hierarchy above, and where the hierarchy currently has no document at all.

| Hierarchy node | Tier | Document | `parent_pattern` (if this model had existed at authoring time) |
|---|---|---|---|
| Interior | Environment | **None yet.** No `interior.pattern.md` exists. Its evidence base already exists, informally, as the "Recurring Layout/Composition/Passability/Event" sections of `reports/design-patterns/interior-pattern-corpus-review.md` - see "Materialized vs. Virtual Nodes." | n/a |
| House | Category | `interiors/house.pattern.md` | none (would be the Interior environment pattern, once materialized) |
| Shop | Category | `interiors/shop.pattern.md` | none (would be the Interior environment pattern, once materialized) |
| Item Shop | Specialization | **None separately.** `shop.pattern.md` was derived entirely from the Item Shop sample map and currently states no rule that goes beyond what "Shop" itself needs - see "The Shop / Item Shop Double Duty" below. | would be `PAT-INTERIOR-SHOP`, if split out |
| Weapon Shop | Specialization | `interiors/weapon-shop.pattern.md` | `PAT-INTERIOR-SHOP` |
| Armor Shop | Specialization | `interiors/armor-shop.pattern.md` | `PAT-INTERIOR-SHOP` |
| Inn | Category | `interiors/inn.pattern.md` | none (would be the Interior environment pattern, once materialized) |
| Bar | Category | `interiors/bar.pattern.md` | none (would be the Interior environment pattern, once materialized) |
| Chief's House | Category | `interiors/chief-house.pattern.md` | none (would be the Interior environment pattern, once materialized) |
| Town | Environment | None. | n/a |
| Overworld | Environment | None. | n/a |
| Dungeon | Environment | None. | n/a |
| Cave, Ruins, Castle | Category | None. | n/a |

Every `parent_pattern` value in the third column is stated for illustration only. This work order does not add a `parent_pattern` field to any existing file's frontmatter - see "Constraints" in `work-orders/WO-0026-design-pattern-inheritance-model.md`. Existing patterns are updated only with a references pointer to this document, per that work order's explicit exception.

## The Shop / Item Shop Double Duty

`shop.pattern.md` (`PAT-INTERIOR-SHOP`, "Interior Pattern - Shop") is named and scoped generically ("Shop"), but every one of its rules and all of its evidence come from exactly one sample: the Item Shop map. It therefore currently occupies **two hierarchy nodes at once**: the category-tier "Shop" node (parent to Weapon Shop and Armor Shop) and the specialization-tier "Item Shop" node (a sibling of Weapon Shop and Armor Shop).

This is not an error to fix immediately. It is the expected shape of a category pattern whose only evidence so far comes from one specialization: **a specialization with zero incremental local rules simply resolves to exactly what its category states.** `Item Shop`, if it were split into its own document today, would have an empty `local_rules` list and a `parent_pattern` of `PAT-INTERIOR-SHOP` - its resolved guidance would be byte-for-byte identical to `shop.pattern.md`'s own guidance. Splitting it into a separate file would add a citation target without adding any new rule, so this document leaves the split as explicitly named future work (see `PATTERN_REVIEW_PROCESS.md` for how such a split would be proposed and reviewed) rather than doing it here. `reports/design-patterns/inheritance-examples.md` works through this case in full.

## Materialized vs. Virtual Nodes

A hierarchy node is **materialized** when an actual `.pattern.md` file exists for it, and **virtual** when the node is real in the model (other patterns can be its conceptual children, and evidence for it can exist) but no file has been authored yet.

`Interior`, `Town`, `Overworld`, and `Dungeon` are all virtual today. `Cave`, `Ruins`, and `Castle` are virtual. `Item Shop` is virtual in the sense described above (its node exists conceptually but has no file distinct from its parent).

A virtual node is not a broken reference. `PATTERN_RESOLUTION_RULES.md` specifies exactly how resolution behaves when a citation's chain passes through a virtual node: that layer contributes whatever evidence already exists for it (for `Interior`, that evidence is `reports/design-patterns/interior-pattern-corpus-review.md`'s recurring-findings sections) without requiring a dedicated file, and the citation should say so explicitly rather than silently treating the layer as absent.

## Parent/Child Relationships

- A child's `parent_pattern` field (see `schemas/design-pattern.schema.json`) names exactly one parent by `pattern_id`. This model is single-inheritance: a pattern has at most one parent, not several.
- A parent may have any number of children. `Shop` currently has two materialized children (`Weapon Shop`, `Armor Shop`) and one virtual/collapsed child (`Item Shop`).
- Depth is not fixed at three tiers. A category may itself specialize further before reaching a leaf pattern (for example, a future `Ruins` category under `Dungeon` could specialize into `Collapsed Ruins` and `Flooded Ruins` before any project-specific pattern is written against it). The tiers named above (Environment / Category / Specialization / Project-specific) are the tiers currently populated, not a hard limit on how many levels the tree may eventually have.

## Specialization

A specialization narrows its parent's `Required Conditions` (or the schema-level `applicable_conditions`, see `schemas/design-pattern.schema.json`) and may add rules the parent does not state. `weapon-shop.pattern.md` specializes `Shop` by narrowing "retail browsing" to "weapon stock specifically" and adding the wall-mounted-rack convention `shop.pattern.md` never mentions. A specialization must satisfy every one of its parent's `Required Conditions` that it does not explicitly narrow further - it cannot loosen a parent's required condition, only tighten it or leave it unchanged.

## Shared Behavior

Every rule stated at a parent tier applies to every descendant by default, without needing to be repeated in the child's own document. This is why `weapon-shop.pattern.md` and `armor-shop.pattern.md` do not restate `shop.pattern.md`'s threshold construction, spawn placement, or region-free passability rules - those are inherited, not duplicated. A pattern document's own body should state only what is new or different at its tier; `PATTERN_RESOLUTION_RULES.md` is what actually assembles the full, inherited-plus-local picture at citation time.

## Override Behavior

Two distinct relationships can look similar on the page but are not the same, and the library already contains one example of each:

1. **Vertical override (parent to child).** A child pattern may explicitly replace one of its parent's stated rules, provided it names the exact rule being replaced and states why. This is ordinary specialization taken one step further - not a contradiction, because the child is authorized to speak for its own, narrower domain. The library does not yet contain a clean example of this (neither `weapon-shop.pattern.md` nor `armor-shop.pattern.md` currently overrides a `shop.pattern.md` rule outright; both only narrow and add).
2. **Cross-branch clarification (sibling to sibling, or between unrelated branches).** A pattern may explicitly state that a rule declared elsewhere does **not** apply to it, even though the two patterns are not in a parent/child relationship. `bar.pattern.md`'s own text says it "overrides `shop.pattern.md`'s... wall-anchoring rule" - but per the hierarchy above, `Bar` and `Shop` are **siblings** under `Interior`, not parent and child. `Bar` cannot override a rule it never inherited. What `bar.pattern.md` is actually doing is stating that a reader should not assume `shop.pattern.md`'s wall-anchoring rule generalizes across the whole `Interior` environment tier just because it is currently the most detailed pattern available - it is scoped to display/storage furniture, and `Bar`'s furniture is not display/storage furniture. This is a **cross-branch clarification**, not a vertical override, and this document treats the two as distinct relationship types going forward. `reports/design-patterns/inheritance-examples.md` works through why this distinction matters and what would change if `Interior` were ever materialized with wall-anchoring stated at that tier.

Both relationship types must be explicit and named - an undeclared contradiction between two patterns (one stating a rule, another silently doing something different with no stated reason) is not a valid override of either kind. It is a defect to be caught by `PATTERN_REVIEW_PROCESS.md`'s review checks, not a resolution-time judgment call.

## The Project-Specific Tier

Below specialization, a fourth tier exists for rules specific to one project's one location - for example, a hypothetical "Ashford Village" pattern capturing decisions specific to that location in `The Last Sword Protocol` that do not generalize to every shop or house AtlasStudio might ever describe. Project-specific patterns:

- Are not filed under `studio/design-patterns/interiors/` (or any other environment-tier directory) alongside reusable archetypes. They are filed under `studio/design-patterns/projects/<project-slug>/`, keeping reusable craft knowledge and one-off project decisions physically separate.
- Set `parent_pattern` to whichever specialization (or, absent one, category) pattern they customize.
- Are typically filed at `confidence: low` per `PATTERN_CONFIDENCE_MODEL.md` ("project preference... not derived from official sample data"), unless the project pattern itself cites independent sample-map or playtest evidence beyond what its parent already provides.
- Are the only tier expected to reference Atlas-owned narrative or world-design facts (a specific settlement's name, a specific NPC role) - every tier above it must stay generic and reusable across projects, per `README.md`'s existing "Relationship to Atlas" section.

No project-specific pattern exists in the library yet. `reports/design-patterns/inheritance-examples.md` and `PATTERN_APPLICATION_GUIDE.md` use a hypothetical Ashford Village example to illustrate the tier, clearly labeled as illustrative rather than an existing citable document.

## Future Extensibility

- **Adding a new specialization under an existing category** (for example, a future "Apothecary Shop" under `Shop`) requires no change to this document - it is an ordinary new pattern file with `parent_pattern: PAT-INTERIOR-SHOP`, reviewed under `PATTERN_REVIEW_PROCESS.md` exactly like `weapon-shop.pattern.md` was.
- **Adding a new category under an existing environment** (for example, a future `Blacksmith` under `Interior`, or `Cave`/`Ruins`/`Castle` under `Dungeon` once dungeon extraction begins) also requires no change to this document - it is a new pattern file with no `parent_pattern` (or one pointing at the environment-tier pattern, once materialized).
- **Adding a new environment tier entirely** (for example, if a future genre required a tier this model does not anticipate) is the one case that would require revising this document's hierarchy diagram and Current Library Mapping table - a structural change, not a routine addition, and should go through a dedicated work order the way this one did.
- **Materializing a virtual node** (for example, finally authoring `interior.pattern.md` once enough cross-cutting evidence exists) does not require a new work order to be architecturally valid under this model - it is an ordinary pattern proposal under `PATTERN_REVIEW_PROCESS.md`. What it *would* require, as a courtesy to every pattern that would newly point at it, is updating each existing category pattern's `parent_pattern` field from absent to the new pattern's `pattern_id` - a small, mechanical, explicitly-scoped edit that a future work order should perform deliberately rather than as a side effect of authoring the new parent.

## References

- `studio/design-patterns/PATTERN_SCHEMA.md`, `PATTERN_CONFIDENCE_MODEL.md`, `PATTERN_REVIEW_PROCESS.md`, `README.md` - the `WO-0024` framework this model extends.
- `studio/design-patterns/PATTERN_RESOLUTION_RULES.md` - how a citation chain through this hierarchy is actually resolved into implementation guidance.
- `studio/design-patterns/PATTERN_APPLICATION_GUIDE.md` - how implementation contracts cite a multi-tier chain.
- `schemas/design-pattern.schema.json` - the machine-checkable representation of `parent_pattern`, `evidence_count`, `observed_sources`, `exceptions`, `applicable_conditions`, `inherited_rules`, and `local_rules`.
- `reports/design-patterns/interior-pattern-corpus-review.md` - the evidence base for the virtual `Interior` environment-tier node.
- `reports/design-patterns/inheritance-examples.md` - worked examples of every relationship type defined above.
- Created by `work-orders/WO-0026-design-pattern-inheritance-model.md`.
