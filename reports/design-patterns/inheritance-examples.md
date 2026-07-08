# Inheritance Model Worked Examples

Status: submitted

Scope: `WO-0026`. Five worked examples showing how `PATTERN_INHERITANCE_MODEL.md` and `PATTERN_RESOLUTION_RULES.md` apply to the current Design Pattern Library, plus one purely illustrative example for a category the library has not analyzed yet. Every example states plainly whether it describes the library's real, current state or a hypothetical future state - none of the hypothetical framing here changes any existing pattern's frontmatter or confidence value.

Each example gives a `design-pattern.schema.json`-shaped instance (illustrative, not a claim that this JSON exists as a file anywhere) alongside a prose resolution walkthrough per `PATTERN_RESOLUTION_RULES.md`'s five-step pipeline.

## Example 1: House Inherits Interior

**Real relationship, through a virtual parent.** `interiors/house.pattern.md` is a Category-tier pattern. Its conceptual parent, the Environment-tier `Interior` pattern, is virtual - no `interior.pattern.md` file exists (`PATTERN_INHERITANCE_MODEL.md`, "Materialized vs. Virtual Nodes"). This example shows what resolution looks like when the parent layer is real (has real, corroborated evidence) but not yet a document.

```json
{
  "pattern_id": "PAT-INTERIOR-HOUSE",
  "parent_pattern": null,
  "category": "interior",
  "confidence": "high",
  "evidence_count": 2,
  "observed_sources": [
    "TheLastSwordProtocol-Game/data/Map018.json (House 1)",
    "TheLastSwordProtocol-Game/data/Map019.json (House 2)"
  ],
  "inherited_rules": [],
  "local_rules": [
    "layout.shell_family_17x13",
    "layout.centered_threshold",
    "composition.low_decoration_density",
    "composition.continuous_backwall_shelf",
    "event.no_npc_by_default"
  ]
}
```

`parent_pattern` is `null` today because `Interior` is not materialized - not because `House` has no conceptual parent. Its `inherited_rules` array is empty for the same reason: there is no parent document to inherit from yet, so every rule `house.pattern.md` states is necessarily local.

**Resolution walkthrough**, citing `Environment Pattern: Interior (virtual) -> Category: House`:

1. Walk the chain: `Interior` (virtual, evidence in `reports/design-patterns/interior-pattern-corpus-review.md`) -> `House` (`house.pattern.md`).
2. Collect local rules: `Interior`'s evidence base contributes the corpus review's recurring findings (shell-plus-void construction, the threshold stack, no-NPC-by-default, region-free passability, decorative-flame convention). `House` contributes its own local rules listed above.
3. Apply general to specific: `House`'s rules do not contradict any recurring `Interior`-tier finding - they narrow decoration density and specify the shelf convention, which the corpus review already flagged as function-dependent, not universal. No override needed.
4. No cross-branch clarification cited.
5. Resolved guidance: the full corpus-review recurring rule set, plus `House`'s own local rules, reported at `High` (Interior layer, 8/8 corpus corroboration) `/ High` (House layer, 2 independent buildings) - both layers happen to be `High` in this particular chain, which is not guaranteed in general.

**What would change if `Interior` were materialized:** `house.pattern.md`'s frontmatter would gain `"parent_pattern": "PAT-INTERIOR"` (or whatever `pattern_id` the new document used) and its `inherited_rules` array would be populated with labels pointing at the newly-authored parent's rules, shrinking `local_rules` to only what's genuinely House-specific. No rule text would need to change - only the bookkeeping of which layer states which rule.

## Example 2: Item Shop Inherits Shop

**Real relationship, degenerate case.** Per `PATTERN_INHERITANCE_MODEL.md`, "Item Shop" has no document distinct from `shop.pattern.md` - `shop.pattern.md`'s entire evidence base is the Item Shop sample map, and it states no rule beyond what "Shop" needs. This example shows the schema's correct representation of a specialization that adds nothing.

```json
{
  "pattern_id": "PAT-INTERIOR-ITEM-SHOP",
  "parent_pattern": "PAT-INTERIOR-SHOP",
  "category": "interior",
  "confidence": "medium",
  "evidence_count": 1,
  "observed_sources": [
    "TheLastSwordProtocol-Game/data/Map021.json (Item Shop)"
  ],
  "inherited_rules": [
    "layout.shell_family_17x13",
    "layout.centered_threshold",
    "layout.centerline_to_focal_point",
    "composition.bilateral_clusters",
    "composition.floor_accent_rug",
    "passability.reachability_ring",
    "event.no_npc_by_default"
  ],
  "local_rules": [],
  "exceptions": []
}
```

This instance is illustrative only - `PAT-INTERIOR-ITEM-SHOP` does not exist as a separate file, and this work order does not create one. It exists here to make a specific point precise: **an empty `local_rules` array is a valid, meaningful state, not an error.** If `Item Shop` were split from `Shop` into its own file today, this is exactly what it would contain - a full `inherited_rules` list mirroring everything `shop.pattern.md` already states, and nothing of its own.

**Resolution walkthrough**, citing `Category: Shop -> Specialization: Item Shop`:

1. Walk the chain: `Shop` (`shop.pattern.md`) -> `Item Shop` (hypothetically split, or today, `shop.pattern.md` itself again).
2. Collect local rules: `Shop` contributes everything in `shop.pattern.md`. `Item Shop` contributes nothing new.
3. Apply general to specific: no change - `Item Shop`'s resolved guidance is identical to `Shop`'s.
4. No cross-branch clarification.
5. Resolved guidance equals `shop.pattern.md`'s guidance verbatim, reported at a single `Medium` (both layers report the same value, since they are, today, the same document).

**Why not split it now:** splitting would add a citation target (`Apply: Specialization: Item Shop` instead of `Apply: Category: Shop`) without adding a single new rule. `PATTERN_INHERITANCE_MODEL.md` names this as deliberate future work, not an oversight - the split becomes worth doing the moment `Item Shop` needs even one rule `Weapon Shop` and `Armor Shop` don't share.

## Example 3: Shop Inherits Interior

**Real relationship, through a virtual parent - same shape as Example 1, different Category.** Shown separately because `Shop` has its own materialized children (`Weapon Shop`, `Armor Shop`), making it a useful second data point for how a virtual `Interior` parent interacts with a Category that itself has descendants.

```json
{
  "pattern_id": "PAT-INTERIOR-SHOP",
  "parent_pattern": null,
  "category": "interior",
  "confidence": "medium",
  "evidence_count": 1,
  "observed_sources": [
    "TheLastSwordProtocol-Game/data/Map021.json (Item Shop)"
  ],
  "inherited_rules": [],
  "local_rules": [
    "layout.shell_family_17x13",
    "layout.centered_threshold",
    "layout.centerline_to_focal_point",
    "composition.bilateral_clusters",
    "composition.floor_accent_rug",
    "composition.wall_anchored_storage",
    "passability.reachability_ring",
    "event.no_npc_by_default"
  ]
}
```

**Resolution walkthrough**, citing `Environment Pattern: Interior (virtual) -> Category: Shop`:

1. Walk the chain: `Interior` (virtual) -> `Shop` (`shop.pattern.md`).
2. Collect local rules: `Interior`'s virtual layer contributes the same corpus-review recurring findings as Example 1. `Shop` contributes its own rules, including `composition.wall_anchored_storage`.
3. Apply general to specific: no contradiction between `Shop`'s rules and the `Interior`-tier recurring findings.
4. No cross-branch clarification cited *for this chain* - but see Example 4, where a different Category (`Bar`) explicitly clarifies that `Shop`'s `composition.wall_anchored_storage` rule does not extend to it. That clarification is not part of *this* citation's resolution; it only matters when `Bar` itself is the pattern being resolved.
5. Resolved guidance: the corpus-review recurring rules plus `Shop`'s full local rule set, reported at `High / Medium` - notably lower than Example 1's `House` chain, because `Shop`'s own evidence is single-source while `House`'s is two independent buildings. This is `PATTERN_RESOLUTION_RULES.md`'s "Confidence Interactions" rule in action: the same `Interior` layer contributes `High` to both chains, but the Category layer's own confidence differs and is reported separately, not blended.

## Example 4: Bar Overrides Shop Wall-Anchoring

**Real relationship, but not vertical inheritance - a cross-branch clarification.** `Bar` and `Shop` are siblings under `Interior`, not parent and child (see the hierarchy diagram in `PATTERN_INHERITANCE_MODEL.md`). `bar.pattern.md`'s own text says it "overrides" `shop.pattern.md`'s wall-anchoring rule; this example shows precisely why that word is doing double duty and how the schema represents the relationship correctly.

```json
{
  "pattern_id": "PAT-INTERIOR-BAR",
  "parent_pattern": null,
  "category": "interior",
  "confidence": "medium",
  "evidence_count": 1,
  "observed_sources": [
    "TheLastSwordProtocol-Game/data/Map023.json (Bar)"
  ],
  "exceptions": [
    {
      "rule": "composition.wall_anchored_storage (\"anchor all shelving and heavy storage furniture directly against a wall\")",
      "relationship": "cross_branch_clarification",
      "source_pattern": "PAT-INTERIOR-SHOP",
      "reason": "Bar furniture represents seating islands, not merchandise storage. shop.pattern.md's wall-anchoring rule is scoped to display/storage furniture; it was never inherited by Bar in the first place, since Bar is Shop's sibling, not its child, so there is nothing to vertically override. This entry exists to stop a reader from assuming shop.pattern.md's rule generalizes to the whole Interior tier just because Shop currently states it in the most detail."
    }
  ],
  "local_rules": [
    "layout.wider_interior_shell",
    "layout.no_single_centerline",
    "composition.floating_furniture_islands",
    "composition.high_floor_coverage",
    "composition.multi_flame_spread"
  ]
}
```

**Resolution walkthrough**, citing `Category: Bar` alone (no `Shop` ancestor in this chain, because there is none):

1. Walk the chain: `Interior` (virtual) -> `Bar` (`bar.pattern.md`). `Shop` never appears in this chain - it is not an ancestor of `Bar`.
2. Collect local rules: `Interior`'s recurring findings, plus `Bar`'s own rules above.
3. Apply general to specific: no conflict, since `Bar`'s chain never touches `Shop`'s `composition.wall_anchored_storage` rule in the first place.
4. Apply the cited cross-branch clarification: the `exceptions` entry above is not resolving a conflict *within this chain* - it exists to prevent a *different* mistake, where someone citing `Bar` might also assume `Shop`'s well-documented wall-anchoring rule applies here by generalization. Recording it in `exceptions` makes that non-applicability explicit and checkable rather than relying on a reader noticing `PATTERN_INHERITANCE_MODEL.md`'s prose discussion.
5. Resolved guidance for a `Bar` citation never included wall-anchoring to begin with - the `exceptions` entry documents *why*, not what replaces it.

**The precise correction this example makes to `bar.pattern.md`'s own wording:** that document says the pattern "overrides" `shop.pattern.md`'s rule. Per this model, `Bar` cannot override a rule it was never positioned to inherit - siblings do not inherit from each other. The accurate description is that `bar.pattern.md` **clarifies the scope** of a rule that lives on a different branch, for the benefit of a reader who might otherwise over-generalize it. This is a wording precision, not a substantive disagreement - `bar.pattern.md`'s underlying claim (open floor furniture is correct for a bar, wall-anchoring does not apply) is fully correct and unchanged by this correction. Per this work order's constraints, this report notes the precision here; it does not edit `bar.pattern.md`'s wording, since that would go beyond the narrow "reference the future inheritance model" exception this work order's Constraints allow for existing pattern files.

**If `Interior` is ever materialized with wall-anchoring stated at that tier:** this relationship would need to be re-expressed. If a future `interior.pattern.md` stated wall-anchoring as a blanket Environment-tier rule (which the corpus review's own findings argue against - see `reports/design-patterns/interior-pattern-corpus-review.md`, "Recurring Composition Rules," item 1), then `Bar` would become `Interior`'s child in fact, and its clarification would become a genuine `vertical_override` instead of a `cross_branch_clarification`. This is exactly why the corpus review recommended *against* promoting wall-anchoring to a universal rule - doing so would force every social/seating interior to carry an override rather than simply never having inherited the rule in the first place.

## Example 5: Future Dungeon Patterns

**Fully hypothetical - illustrates extensibility, not a claim about existing evidence.** No dungeon sample map has been analyzed by AtlasStudio. This example shows that the model in `PATTERN_INHERITANCE_MODEL.md` needs no redesign to accommodate a wholly new Environment branch - only new pattern documents, authored the same way `WO-0025` authored the interior corpus.

```json
{
  "pattern_id": "PAT-DUNGEON-CAVE",
  "parent_pattern": null,
  "category": "dungeon",
  "confidence": "experimental",
  "evidence_count": 0,
  "observed_sources": [],
  "applicable_conditions": [
    "NOT YET AUTHORED - illustrative placeholder only"
  ],
  "inherited_rules": [],
  "local_rules": []
}
```

**Resolution walkthrough**, citing a hypothetical `Environment Pattern: Dungeon (virtual) -> Category: Cave (unauthored)`:

1. Walk the chain: `Dungeon` (virtual, zero evidence today) -> `Cave` (unauthored - this instance is a placeholder, not a real pattern).
2. Collect local rules: none exist for either layer.
3. Apply general to specific: nothing to apply.
4. No cross-branch clarification possible - no dungeon patterns exist to clarify against.
5. Resolved guidance: **empty.** A citation of this chain today would correctly fail `PATTERN_RESOLUTION_RULES.md`'s resolution process, because no rules exist at either named layer - not because the model is broken, but because the library genuinely has no evidence yet. This is the intended, correct behavior: the model does not fabricate guidance for an unanalyzed category.

**What extending the corpus would look like:** per `PATTERN_INHERITANCE_MODEL.md`'s "Future Extensibility" section, adding `Cave`, `Ruins`, and `Castle` under `Dungeon` requires no change to `PATTERN_INHERITANCE_MODEL.md` itself - each would be an ordinary new Category-tier pattern with `category: "dungeon"` and `parent_pattern: null` (until a `Dungeon` environment-tier pattern is materialized, exactly as `interiors/*.pattern.md` relate to the still-virtual `Interior` today), authored via the same extraction-and-review process `WO-0025` already established. Only introducing the `dungeon` environment-tier value itself required this work order's schema to name it in advance (`schemas/design-pattern.schema.json`'s `category` enum already lists `dungeon`, `town`, and `overworld` alongside `interior`, anticipating this future work without requiring a schema change when it happens).

## Summary Table

| Example | Relationship type | Materialized today? | Confidence shown |
|---|---|---|---|
| 1. House inherits Interior | Vertical (through virtual parent) | Interior: no. House: yes. | High / High |
| 2. Item Shop inherits Shop | Vertical, degenerate (empty local_rules) | Item Shop: no (collapsed onto Shop). Shop: yes. | Medium (single value - same document) |
| 3. Shop inherits Interior | Vertical (through virtual parent) | Interior: no. Shop: yes. | High / Medium |
| 4. Bar overrides Shop wall-anchoring | Cross-branch clarification (not vertical) | Bar: yes. Shop: yes. Neither is the other's parent. | N/A - not a chain; a clarification recorded in Bar's own `exceptions` |
| 5. Future Dungeon patterns | Vertical (fully hypothetical) | Neither. | Experimental / none (empty resolution) |

## Constraints Observed

- Documentation only. No code was written or modified.
- `TheLastSwordProtocol-Atlas` was not read or modified.
- `TheLastSwordProtocol-Game` was not modified (its already-analyzed map data is cited, not re-read, for this report).
- No pattern document's frontmatter, confidence value, or rule text was changed by this report - every JSON instance shown above is illustrative, not a diff applied to any real file.
- No confidence value was promoted. `shop.pattern.md` remains at `medium`, exactly as `WO-0025` left it and as `WO-0025`'s own review report recommended (without applying) promoting to `high` - that recommendation is restated accurately here (Example 3) but not acted on.
- The Immutable Formatting Rule (`studio/immutable-formatting-rule.md`) was preserved: this is a new report; no existing file was reformatted.
