# WO-0071 Implementation Notes

Author: Claude Code, 2026-07-15. Executed directly (Codex not invoked this
round) at Chris's request immediately after WO-0070's completion decision.
This note is technical detail for whoever next touches this code (most
likely Codex, WO-0071's nominal owner) -- the work-order file itself carries
the acceptance-facing summary.

## What this integration is and is not

It wires the approved `MV-HOM-ASH-001` MapVision and the approved Ashford
`TileAssembly` catalog into the *existing* `SemanticAssembler`
(`assembler.py`, WO-0058) -- it does not add a second generator. A caller who
does not pass `map_vision=` gets byte-identical behavior to before this work
order; every pre-existing test (34 compiler + 23 tile_assembly) still passes
unmodified.

## New modules and why they are separate

- `tile_assembly_catalog.py` -- pure I/O + normalization. Knows how to read a
  WO-0070 kit `index.json` and the custom-extension `manifest.json` into one
  `AssemblyRecord` shape. Has no opinion about MapVision, archetypes, or
  Ashford specifically.
- `map_vision_resolution.py` -- pure validation + resolution logic. Owns
  `SEMANTIC_TAG_CANDIDATES`, the one place that maps a building role /
  landmark id to plausible TileAssembly ids. This mapping is deliberately
  **not** part of the TileAssembly contract (kits don't declare a "target
  role") and **not** baked into `assembler.py` -- keeping it in one small,
  auditable table is the point: when a kit's enabled set changes (a new
  cottage gets approved, say), this is the only file that needs an edit.
- `assembler.py` -- the actual wiring: resolve once per `assemble()` call,
  pick deterministically via the existing `building_selection` seed stream,
  verify fit/adapter, attach to the output.

## The enablement-rule judgment call

The authored kit's `index.json` carries a **kit-level** `"enabled": false`
and `"approval_state": "partial_human_approval"`, while five of its nine
**individual** records are `"review_state": "human_approved"` /
`"downstream_generation_allowed": true` (Elara House, Shop, Inn, Elder House,
Warm Vent -- all approved by Chris on 2026-07-15 per
`AUTHORED-PACK-FIDELITY-REVIEW.md`'s "Subsequent human decision" section).

I read the kit-level flag as an advisory package-lifecycle marker, not a
gate, and treat each record's own `downstream_generation_allowed` (falling
back to `enabled` for the reference kit and custom extension, which don't
carry a kit-level flag at all) as the single source of truth. Reasoning:

1. That per-record field is literally what WO-0070's "Post-review hardening"
   section says was added *so downstream selection could fail closed record
   by record* -- a kit-level blanket flag would make the granular field
   pointless.
2. The kit's own test suite (`tile_assembly/tests/test_ashford_authored_kit.py::test_human_selection_is_partial_and_fail_closed`)
   already asserts on individual `enabled`/`downstream_generation_allowed`
   values, not the kit-level flag, confirming record-level is the intended
   contract.
3. Honoring the kit-level `false` literally would make WO-0071 unable to use
   *any* authored assembly, which would contradict the task board's own
   recorded state ("WO-0070 complete and WO-0071 unblocked").

If this reading turns out wrong, the fix is one line in
`tile_assembly_catalog.load_tile_assembly_kit_index` (AND'ing in the kit-level
flag) -- it is intentionally isolated there.

## The star-topology placement bug (a real, general fix, not an Ashford hack)

The first Ashford fixture attempt failed `placement_budget_exhausted`
deterministically (not a bad-luck seed issue) with `well_square` fanning out
to four children (Shop, Inn, Elder House, route mouth). `_place_zones`
computes each child's four candidate rects (N/E/S/W) purely from its own
size relative to its *parent* -- when children are much larger than a small
parent, two children's candidate rects can spill into and overlap each
other's compass direction even though each is nominally on a "different
side." The fix applied here has two parts:

1. **Graph-level**: reduced `well_square`'s fan-out to three new children
   (Shop, Inn, Elder House) by moving `route_mouth` to hang off
   `shop_frontage` and `forest_edge` to hang off `elder_frontage` instead --
   a parent should not need more free sides than it has (its own parent
   already occupies one of four).
2. **Sizing**: gave `well_square` a `min_area` (144, i.e. 12x12) comfortably
   larger than the widest child footprint (9, the Inn) so no child's N/E/S/W
   candidate rect can geometrically spill past the parent's own bounding box
   into a neighboring candidate's territory.

Neither is Ashford-specific magic; both are the general condition this
placement algorithm needs to succeed reliably, and are worth remembering if
a future archetype has one small hub zone with several large neighbors.

## `_place_modules` behavior change (backward compatible)

Previously, any `modules_required` entry with `min_count >= 1` whose
`zone_role` was not selected this run raised `module_parent_zone_missing`,
even when that zone role is legitimately optional and simply wasn't
requested via `required_beats`. That made it impossible to have an optional,
beat-gated zone with its own required decoration module (exactly the
Ashford fence/tree case). Fixed by passing the *full, unfiltered* set of
zone roles from the gameplay graph into `_place_modules`: if the role exists
in the graph at all but wasn't selected this run, skip quietly; if it
doesn't exist in the graph at all, still raise (a genuine archetype/graph
authoring mismatch). Verified this is a no-op for every existing shop/house/
inn fixture, since their `min_count >= 1` entries only ever target
always-required zones.

## Current catalog state as of 2026-07-15 (for whoever revisits binding)

Enabled: Elara House, Shop, Inn, Elder House (authored kit); Warm Vent
(authored kit); roofed well, humming panel, patched-metal fence, drainage
(custom extension); broadleaf tree, window, shop sign (reference kit).
Disabled: both cottage variants, farm-fence-cluster, well-open-context,
bridge/drainage-authored, shop-tavern-frontage, inn-broad-01, shop/inn prop
clusters, house-compact-01, humming-panel-authored,
patched-metal-fence-authored, well-roofed-authored (superseded by the custom
extension). `village_cottage` therefore has zero enabled candidates right
now -- deliberately not included as a required module in the WO-0071
fixture archetype; see `test_missing_assembly_fails_closed_for_village_cottage`.
