# MapVision Contract 0.1

`MapVision` is the engine-neutral visual brief between Atlas story authority and
the existing seeded compiler. It answers what a location must communicate and
feel like. It does not decide exact coordinates, choose tiles, or serialize a
map.

## Trigger and reset record

This contract exists because the first reconciled Ashford exterior candidate
was human-rejected. The layout was an improvement and felt less mechanical,
but the candidate showed only the bottom half of a two-tile tree assembly,
buildings were too tall, building style did not match the references, and the
overall style and feel were wrong.

Further Ashford candidates are frozen until all four prerequisites are met:

1. this authority contract is approved;
2. the canonical Ashford `MapVision` is approved;
3. its concept target is human-approved as visual direction; and
4. the required complete `TileAssembly` records are verified.

## Authority model

Every descriptive statement carries both an `authority` and a `confidence`:

| Authority | Meaning | May establish canon? |
|---|---|---|
| `required_canon` | Must survive into every valid interpretation. Requires an `atlas_canon` source. | Yes, but only by citing already-authoritative Atlas canon. |
| `approved_visual_direction` | Human-approved visual interpretation compatible with canon. | No. |
| `preference` | Desired treatment that may yield to feasibility or stronger authority. | No. |
| `optional_inspiration` | Reference signal or idea; omission is valid. | No. |

Confidence records evidence quality: `verified`, `approved`, `provisional`, or
`speculative`. Confidence never elevates authority. A verified concept image is
still not canon.

### Exact human-decision trigger

Stop generation and ask Chris how to proceed when **two statements cannot both
be satisfied and either statement is `required_canon`, or when a proposed
statement would add, remove, or reinterpret story/world facts not supported by
an `atlas_canon` source**. Record the issue in
`approval.unresolved_conflicts[]`, set `canon_reconciled` to `false`, and keep
`status` at `pending_human_approval`. No compiler or agent may resolve that
conflict by authority ranking, concept art, majority evidence, or invention.

An approved record must have `canon_reconciled: true`, no unresolved conflicts,
and non-null `approved_by` and `approved_at` values.

## Field responsibilities

- `emotional_read` and `memorable_identity`: first emotional promise and the
  one-sentence identity that makes the map distinct.
- `geography` and `first_view`: environmental framing and ordered arrival read,
  without coordinates.
- `landmarks`: dominant/supporting/background hierarchy.
- `building_silhouettes`: relative scale, height profile, shape language, and
  variation rules. Tile dimensions belong downstream.
- `materials` and `color_language`: abstract material/color relationships, not
  asset names.
- `roads_and_circulation`: visible route hierarchy and approach intent;
  topology remains `GameplayGraph`, coordinates remain `MapPlan`.
- `density`: overall and zone-relative visual density plus purposeful negative
  space.
- `environmental_storytelling` and `story_state_variants`: visible story
  signals and canon-supported state changes.
- `canon_anchors` and `exclusions`: facts that must survive and inventions or
  treatments explicitly forbidden.
- `source_provenance`: revision-pinned authority ledger for every source.
- `concept_direction`: optional visual artifact references with the mandatory
  policy `visual_direction_only_not_structural_evidence`.

## Relationship to the existing pipeline

```text
Atlas canon -> MapIntent -> MapVision -> GameplayGraph / archetype selection
                              |                    |
                              | visual constraints|
                              v                    v
                          StylePack ----------> MapPlan
                                                  |
TileAssembly + TilePalette (engine adapter) ------|
                                                  v
                                      GenerationManifest + candidate
```

- `MapIntent` remains the concise statement of purpose and generation inputs.
  It gains an external `MapVision` companion reference in a future integration
  work order; 0.1 MapIntent files remain valid unchanged.
- `GameplayGraph` remains topology and required gameplay beats. MapVision prose
  cannot override its reachability or invent a route.
- `MapPlan` remains the existing Map Blueprint and sole resolved spatial
  contract. MapVision contains no coordinates and is not a second MapPlan.
- `StylePack` supplies abstract visual vocabulary compatible with the vision.
- `TilePalette` remains the only existing contract allowed to carry raw tile
  IDs. `TileAssembly` will bind complete multi-tile structures in WO-0070.
- `GenerationManifest` will pin `map_vision_id@version` once compiler
  integration lands; this 0.1 schema does not break existing manifests.
- Concept art illustrates approved direction. It is never structural,
  passability, adjacency, assembly, or canon evidence.

## Validation and invalidity

Schema validation checks required fields, closed object shapes, IDs, authority
vocabulary, and the absence of unrecognized raw binding fields. Semantic review
additionally rejects:

- `required_canon` statements whose cited provenance is not `atlas_canon`;
- approved records with unresolved conflicts or missing human approval;
- concept art promoted to structural evidence or canon;
- raw tile/tileset/database IDs or engine asset filenames anywhere in the
  record.

See `examples/map_vision/valid_map_vision.json` and the two intentionally invalid
fixtures beside it.

## Migration from WO-0056

This is an additive eleventh contract type, not a replacement pipeline.

1. Existing MapIntent, GameplayGraph, MapPlan, StylePack, TilePalette, and
   GenerationManifest instances remain valid byte-for-byte.
2. For a map entering the visual pipeline, create one `MapVision` referencing
   its existing `MapIntent` by exact `id@version`.
3. Move descriptive visual prose from implementation notes into authority-
   labeled MapVision statements. Do not move topology, coordinates, tile IDs,
   or event commands.
4. Reconcile every `required_canon` statement against Atlas sources. Stop at
   the exact human-decision trigger above.
5. After human approval, downstream work may decompose the vision into
   measurable constraints. WO-0071 will add version-pinned compiler/manifest
   integration; until then, no existing schema is rewritten to simulate it.

