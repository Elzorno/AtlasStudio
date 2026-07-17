# Schema-First RPG Maker MZ Map Generation Prototype

## Outcome

This prototype makes semantic occupancy, not a generated image, the structural source of truth. The deterministic pipeline is:

`MapIntent -> Topology -> SemanticOccupancy -> Validate/Repair -> TileProfile -> MZ map JSON`

The SVG preview is downstream review evidence only. It cannot affect layout.

## Contracts and assumptions

- `schema/map_intent.schema.json` is the portable JSON Schema contract. `intent_parser.js` supplies dependency-free runtime checks; a production integration should additionally validate with a Draft 2020-12 implementation such as Ajv.
- A topology contains typed nodes, routed edges, and district containment. The same intent and seed produce byte-equivalent topology.
- Semantic occupancy is a row-major `cells[y][x]` matrix. No tile IDs are permitted in this stage.
- The sample profile is deliberately swappable and illustrative. Its tile IDs are not certified for any production project. A target adapter must bind semantics to IDs verified from that project's `Tilesets.json`, sheet layout, passability flags, and autotile rules.
- The exporter creates six MZ layers in one flattened array. Indexing is `z * width * height + y * width + x`; layers 0-3 are tiles, layer 4 is shadow, and layer 5 is region ID.
- The result is intentionally close to `MapXXX.json`. Event entries are structured placeholders with empty pages, so they must be materialized into valid RPG Maker event pages before production use.

## Module responsibilities

| Module | Responsibility |
|---|---|
| `intent_parser.js` | Reject malformed or incomplete intent without generating partial output. |
| `topology_generator.js` | Seeded graph layout, circulation hierarchy, and containment. |
| `occupancy_builder.js` | Rasterize graph and POI footprints into semantic cells, anchors, and region intent. |
| `validator.js` | Reachability, islands, doorways, dead ends, dimensions, boundary, empty-space, adjacency, region, anchor, and map-type gates. |
| `repair_pass.js` | Bounded, recorded repairs; never silently loops forever. |
| `mz_exporter.js` | Resolve semantics through a profile and flatten six MZ layers. |
| `preview_renderer.js` | Render a semantic SVG after validation. |

## Validation policy

Errors fail export commands. Warnings remain visible in each report. Repair is bounded to four passes and every mutation is recorded. The prototype repairs connectivity and excess empty-field pressure; it does not invent missing canon, change requested POIs, or substitute tile art.

Town checks require a focal node and circulation hierarchy and detect the explicitly forbidden generic three-house pattern. Interior checks preserve clear floor circulation and require valid functional anchors. The same graph/grid primitives support dungeons, but a production dungeon grammar should add keys, gates, lock ordering, loops, chokepoint budgets, and progression-state simulation before claiming dungeon readiness.

## Autotile and adjacency boundary

RPG Maker autotiles are not arbitrary sequential IDs. The sample profile proves separation and layer flattening, not production autotile shape selection. A production profile should expose adjacency resolvers per semantic class, calculate the neighbor mask, and emit the correct MZ autotile shape ID. Complete multi-tile structures should resolve through the existing AtlasStudio `TileAssembly` catalog rather than individual semantic IDs.

## Running

From this directory:

```sh
npm test
npm run generate
```

Each example output contains the normalized input, topology JSON, semantic grid JSON and ASCII, MZ-ready JSON, validation report with repairs, and an optional SVG preview.

For the rural-village Ashford artwork review candidate:

```sh
npm run artwork
```

This second pass binds the semantic grid to the real `Outside` tileset, resolves floor-autotile shapes from eight-neighbor occupancy, stamps only approved or verified-reusable Ashford `TileAssembly` records, and composites the approved custom well into the review PNG. The well remains an explicitly external preview overlay until a combined tileset slot is approved; the pass therefore records `production_promotion: not_applied` rather than presenting the candidate as a production map.

## Production integration gates

Before writing a real `MapXXX.json`: certify a target tileset profile; implement autotile neighbor resolution; convert anchor placeholders to complete event pages; validate passability against `Tilesets.json` flags; compose approved `TileAssembly` records; load the disposable map in RPG Maker MZ; and require human visual/playtest approval. Production Game files are outside this prototype's write scope.
