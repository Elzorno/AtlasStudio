# Reusable Seeded Map Compiler Contract (WO-0056)

This directory is the versioned contract for a reusable, deterministic Atlas map
compiler that assembles authored JRPG building archetypes and layout families
from seeds, applies style packs, and emits `MapPlan` review candidates for engine
adapters to export. It is documentation and schema-valid fixtures only: no
compiler implementation lives here yet (that is `WO-0057` and later).

See the architecture decision this contract implements:
`TheLastSwordProtocol-Atlas/atlas/docs/09_Technical/Map_Generation/ATLAS-TEC-063_Reusable_Seeded_Map_Compiler_Contract.md`.

## The Twelve Contract Types

| Type | Schema | What it is |
|---|---|---|
| `MapVision` | `schemas/map_vision.schema.json` | Authority-labeled visual brief between Atlas canon/`MapIntent` and spatial generation. No coordinates or engine bindings. See `MapVision_Contract.md`. |
| `TileAssembly` | `schemas/tile_assembly.schema.json` | Adapter-owned, source-pinned reusable layered tile component with anchors, collision, connectors, variations, and preview evidence. See `TileAssembly_Contract.md`. |
| `MapIntent` | `schemas/map_intent.schema.json` | What a map should be and why, before generation runs. Formalizes the existing Map Blueprint's `map_intent` header as a standalone artifact. |
| `GameplayGraph` | `schemas/gameplay_graph.schema.json` | The semantic skeleton: zones, typed ports, required beats, edges, reachability. Topology, not pixels. |
| `BuildingArchetype` | `schemas/building_archetype.schema.json` | A building type's shape grammar: which `GameplayGraph` it uses, which `Module`s are required per zone. No tile IDs. |
| `LayoutFamily` | `schemas/layout_family.schema.json` | How to spatially resolve one archetype's zones: placement rules, rotation/reflection permissions, weighted variants. No tile IDs. |
| `Module` | `schemas/module.schema.json` | A small reusable sub-layout unit (a furniture cluster, a service point) with a footprint and ports. |
| `Connector` | `schemas/connector.schema.json` | A typed join between zones/modules: compatible port types, width, traversal. |
| `StylePack` | `schemas/style_pack.schema.json` | Engine-neutral visual vocabulary (abstract tags) bound to a biome. Not tile IDs. |
| `TilePalette` | `schemas/tile_palette.schema.json` | The engine-specific binding of a `StylePack`'s vocabulary to raw tile IDs. **This is where tile IDs are allowed to live.** |
| `MapPlan` | `schemas/map_plan.schema.json` | The resolved, still engine-neutral spatial plan. **This is the existing Map Blueprint format**, formalized as real JSON Schema, plus one additive field. Not a second format. |
| `GenerationManifest` | `schemas/generation_manifest.schema.json` | Seed + version-pinned provenance record for one compiler run: which archetype/layout/style versions produced which `MapPlan`. |

## Explicit Boundaries

Per WO-0056 required task 8:

- **Archetypes and layout families contain semantics only.** `BuildingArchetype`,
  `LayoutFamily`, `GameplayGraph`, `Module`, and `Connector` MUST NOT reference
  raw engine tile IDs, asset filenames, or database row IDs. `tests/test_contract_examples.py`
  asserts this mechanically for every archetype/layout-family example (all 3
  archetypes, all 7 layout families, as of `WO-0059`).
- **Style packs contain visual vocabulary, not tile IDs.** A `StylePack`'s
  `visual_tags` are abstract strings (`hearth_focal_feature`, `wall_mounted_flame`,
  ...). They say *that* a hearth-like landmark belongs in this zone, not *which*
  tile paints it.
- **Engine adapters contain raw tile IDs and serialization.** A `TilePalette`
  is the only contract type allowed to carry a raw tile ID, and its `owner_repo`
  field records which repository actually authors instances of it (for RPG Maker
  MZ: `rpgmakerLSP`, the existing engine adapter). The illustrative example in
  `examples/shared/tile_palette_ashford_cozy_interior_illustrative.json` lives
  here only to demonstrate the schema shape; production `TilePalette` instances
  belong in the adapter repo, not in this reusable library.
- **Canon, gameplay intent, generated candidates, and accepted production maps
  remain distinct.** A `GenerationManifest.status` follows this project's
  existing status vocabulary (`generated_pending_review` / `accepted` /
  `accepted_with_notes` / `rejected`); nothing in this contract marks its own
  output accepted.
- **MapVision describes visual intent but cannot add canon or spatial evidence.**
  Every statement is authority/confidence labeled. Concept art is always
  `visual_direction_only_not_structural_evidence`. Canon conflicts trigger a
  human question and halt generation; see `MapVision_Contract.md` for the exact
  trigger and the Ashford rejection record.

## Zone Role / Port Type / Connector Type Vocabulary

`GameplayGraph.zones[].role`, `ports[].port_type`, and `edges[].connector_type`
are open (documented, not closed-enum) string vocabulary, so a second implementer
can introduce a new value without a contract version bump. Values already in use
by the shop, inn, and house examples:

- **Zone roles:** `entry_threshold`, `center_aisle`, `browse_loop`, `wall_stock`,
  `focal_feature`, `service_point`, `vestibule_alcove`, `common_room`,
  `spine_corridor`, `guest_quarters_wing`, `main_floor`, `hearth_accent`,
  `hearth_area`, `keepsake_corner`.
- **Port types:** `exterior_door`, `service_point`, `open_floor`. Aligned to
  `WO-0058`'s typed-port vocabulary (`exterior door, interior door, service
  point, stairs, road, waterfront, dungeon connector, transfer anchor, event
  anchor`) where the interior archetypes here actually need one -- `stairs`,
  `road`, `waterfront`, and `dungeon_connector` are reserved for future
  exterior/dungeon/town archetypes this work order does not author.
  `door_transfer` (WO-0056's original name) was renamed to `exterior_door`
  during `WO-0059` for this alignment; `interior_door` is reserved but unused,
  since none of Shop/Inn/House currently model an internal door as a distinct
  event (their internal zone boundaries are walkable chokepoints, not door
  events, per each source pattern's own Event Rules).
- **Connector types:** `open_floor`, `chokepoint_corridor`.
- **Gameplay beats:** `npc_service_point`, `treasure_anchor`, `exit_transfer`.

New values are welcome; document them alongside their source pattern the same
way the existing values cite `PAT-INTERIOR-SHOP` / `PAT-INTERIOR-INN` / `PAT-INTERIOR-HOUSE`.

## Seed Derivation

Per WO-0056 required task 5, seed derivation must be deterministic without
prescribing language-runtime `hash()` behavior (Python's `hash()` on strings is
randomized per-process by default and is not a legitimate seed source). This
contract uses `sha256_truncated_64`:

```text
value = int(sha256("|".join(inputs)).hexdigest()[:16], 16)
```

where `inputs` is the ordered list, recorded verbatim in
`GenerationManifest.seed.inputs`:

```text
[map_intent_id,
 f"{archetype_id}@{archetype_version}",
 f"{layout_family_id}@{layout_family_version}",
 variant_id,
 f"{style_pack_id}@{style_pack_version}",
 salt]
```

`salt` is `MapIntent.generation_seed_salt`, a stable, human-chosen, map-specific
string. Regenerating with the same inputs always reproduces the same seed;
bumping any referenced artifact's version changes it, which is intentional --
see `map_intent.generation_seed_salt` and `layout_family.version` for the two
places a human deliberately forces a re-roll. This mirrors the seed policy
already stated in `atlas-tools/mapgen/future_architecture.md`
("same seed plus same Atlas inputs should produce the same blueprint").

WO-0057 implements this contract in `seed_streams.py`, `generation_manifest.py`,
`map_plan.py`, and `legacy_adapters.py`. A manifest also pins the reusable
compiler in `generator_ref` and records `adapter_ref` as null until an engine
adapter is selected. Named sub-streams derive from the manifest's root seed by
hashing `root_seed|stream_name|scope`; changing a decoration stream therefore
cannot alter structural streams such as terrain, roads, rooms, transfers, or
event anchors.

## Validating

```sh
python3 validate_contract.py
python3 -m unittest discover -s tests -v
```

Both are stdlib-only, matching this compiler's existing convention (see
`atlas-tools/mapgen/compiler/spec_parser.py` and `specs/world_spec.schema.json`'s
own "stdlib only" note) -- no `jsonschema` package is required or assumed.
`validate_contract.py` implements the subset of JSON Schema (2020-12 vocabulary)
actually used by `schemas/*.json`: `type`, `properties`, `required`,
`additionalProperties`, `items`, `enum`, `pattern`, `minimum`/`maximum`,
`minItems`/`minLength`. It does not implement `$ref`/`$defs`, `oneOf`, or
cross-file references -- none of the eleven schemas need them; every cross-artifact
relationship is a plain ID+version string (e.g. `BuildingArchetype.gameplay_graph_ref`),
not a JSON Pointer.

WO-0066 adds `MapVision` as an eleventh additive type, and WO-0070 adds
`TileAssembly` as a twelfth. Existing WO-0056
artifacts remain valid unchanged; migration guidance is in
`MapVision_Contract.md`.

## Examples

- `examples/map_vision/` -- one schema-valid, engine-neutral visual brief plus
  explicit invalid raw-tile and silent-canon fixtures exercised by the tests.

- `examples/tile_assembly/` -- complete source-pinned building and connectorless
  atomic-prop assemblies plus explicit incomplete/hash-drift fixtures. Only the
  valid fixtures are in the validation manifest; focused tests prove the invalid
  fixtures fail closed.

- `examples/shop/` -- `MapIntent`, `GameplayGraph`, `BuildingArchetype`,
  `GenerationManifest`, and **two** `LayoutFamily` tiers (`layout_family.json`
  = compact, `layout_family_offset.json` = offset/L-shaped) for a generic
  single-room retail shop, built from `studio/design-patterns/interiors/shop.pattern.md`.
  A third (zoned/expanded) tier is deliberately not authored -- see
  `building_archetype.json`'s provenance notes: it would violate
  `PAT-INTERIOR-SHOP`'s own single-room Required Condition.
- `examples/inn/` -- `MapIntent`, `GameplayGraph`, `BuildingArchetype`,
  `GenerationManifest`, and **three** `LayoutFamily` tiers (`layout_family_compact.json`,
  `layout_family.json` = offset/L-shaped, `layout_family_zoned_expanded.json`),
  built from `studio/design-patterns/interiors/inn.pattern.md`. Inn is the one
  archetype whose Required Conditions permit all three tiers, since the source
  pattern itself is inherently multi-zone.
- `examples/house/` -- the same five-artifact-type set plus **two** `LayoutFamily`
  tiers (`layout_family_compact.json`, `layout_family_offset.json`), built from
  `studio/design-patterns/interiors/house.pattern.md`. Like Shop, a third
  zoned/expanded tier is deliberately not authored (multi-room residences are
  `chief-house.pattern.md`'s territory, a different archetype this work order
  does not author).
- `examples/shared/` -- six `Module`s, two `Connector`s, one `StylePack`,
  and one illustrative `TilePalette` referenced across the three building
  examples.

This is the `WO-0059` "First Building Archetype Kit": 3 archetypes x up to 3
layout families each = 7 authored `LayoutFamily` records (not 9 -- two tiers
were explicitly not authored where the source pattern's own Required
Conditions forbid them; see each archetype's `building_archetype.json`
provenance notes for the specific citation).

Now that `WO-0058`'s `SemanticAssembler` exists,
`../generate_wo0059_fixtures.py` (one directory up from here, alongside
Codex's own `generate_wo0058_fixtures.py`) assembles 3 deterministic seed
fixtures per layout family -- 21 structural candidates total (7 x 3, not 27,
matching the 7-not-9 layout-family count above) -- into
`../prototypes/wo0059/*.map_plan.json` (plus `.txt` ASCII and `.svg`
previews, and an `index.json` summary). All 21 assemble without a reachability
or required-zone failure and reproduce byte-identically on regeneration.

**WO-0058 integration amendment:** the seam found during WO-0059 fixture
generation is resolved. `SemanticAssembler` now clamps each
`LayoutFamily.size_range` within its archetype-wide `size_constraints`, fails
closed when the ranges do not overlap, and resolves authored `landmark_slots`
into engine-neutral MapPlan records with semantic tag, zone, required/dominant
flags, and anchor. `symmetry_rules` and `circulation_rules` remain authored
layout-family guidance expressed by zone placement and reachability rules.

No `MapPlan` example was authored from scratch: `tests/test_contract_examples.py`
instead validates the entire existing, already-production-used blueprint corpus
in `TheLastSwordProtocol-Atlas/atlas-tools/mapgen/prototype/*.blueprint.json`
(17 files) against `schemas/map_plan.schema.json` directly -- stronger evidence
that `MapPlan` is genuinely blueprint-compatible than a new synthetic example
would be.

## Style Packs (WO-0060)

Two `StylePack`s now exist, covering all three archetypes:

- `STY-ASHFORD-COZY-INTERIOR` (`examples/shared/style_pack_ashford_cozy_interior.json`)
  -- the temperate-village pack. Ashford already reads as a temperate village,
  so this existing pack was extended in place with structured `vocabulary`
  (floor/wall/threshold/furniture/lighting/landmark/edge_dressing) rather than
  authoring a near-duplicate.
- `STY-COASTAL-SETTLEMENT-INTERIOR` (`examples/shared/style_pack_coastal_settlement_interior.json`)
  -- new. Built entirely from color/material substitution (whitewash, pale
  stone, blue-checkered tile, striped linen) already present on the `Inside`
  tileset family -- this project's asset library has no purpose-built nautical
  props (no net/shell/anchor/driftwood tile was found), which is disclosed as
  a real limitation, not silently worked around.
- `biome_substitution` (new field on `StylePack`) explicitly maps each of the
  coastal pack's tags back to the temperate tag it replaces, so the same
  `MapPlan`/archetype can be re-skinned by substitution rule.
  `tests/test_contract_examples.py::test_style_pack_biome_substitution_references_are_consistent`
  checks every `from_tag`/`to_tag` actually exists in its respective pack's
  vocabulary.

The full contact-sheet evidence trail (which `Inside_A2`/`A4`/`A5`/`B` kind or
tile number backs each abstract tag) lives one directory up, in
`../style_study/wo0060/temperate-and-coastal-interior-study.md`, along with
the six labeled contact sheets and the (now-reproducible, no longer
scratchpad-dependent) generator script that produced them. **Nothing in that
study has been passability/layer/adjacency-verified** -- per `WO-0060`'s own
task split (Claude: visual study and specification; Codex: palette tooling),
building the actual verified `TilePalette` instances from this evidence is
task 2, not done here, and a live RPG Maker render review by Chris (task 6)
is required before either pack is used in a production map.
