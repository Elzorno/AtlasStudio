# TileAssembly 0.1 Contract

`TileAssembly` is the reusable, engine-bound visual unit between abstract map
planning and an adapter's map serialization. It preserves a rectangular set of
layered tile cells copied from an identified source-map region, plus placement
anchors, collision, connectors, weighted variations, and preview evidence.

## Ownership boundary

AtlasStudio owns this schema and validation contract. The named engine adapter
in `adapter_ownership` owns extraction, tile interpretation, serialization, and
production instances. A TileAssembly is reusable evidence, not Atlas canon and
not permission to overwrite a production map.

## Source pinning and fail-closed behavior

Every artifact records exact SHA-256 pairs for the overall extraction source,
the source map, its tileset record, and every individual tileset image used by
that tileset. Each image record has a unique `asset_name`, so raw tile
provenance detects asset-sheet replacement even when the database tileset record
is unchanged. `expected_sha256` is the hash approved when the assembly was
authored; `observed_sha256` is the hash measured by the validating workflow. Any
mismatch invalidates the artifact. Producers must not refresh an expected hash
implicitly.

Schema validation rejects missing top-level components and malformed hashes.
Semantic validation additionally rejects incomplete or duplicate cell grids,
incorrectly sized collision masks, out-of-bounds anchors/connectors, duplicate
layers within a cell, and hash drift. Thus partially extracted assemblies never
degrade into apparently valid reusable components.

## Coordinates

Assembly `x`/`y` coordinates are zero-based and bounded by `dimensions`.
`source_coordinate` records the exact zero-based source map cell and layer from
which each tile ID came. Tile IDs and their serialization remain adapter-owned.

Every assembly has at least one placement `anchor`. `connectors` are optional:
an atomic prop such as a tree has no legitimate traversal or adjacency seam and
therefore uses an empty array. Assemblies that do expose connectors must provide
their type, facing, width, and an in-bounds coordinate; adapters must never add
dummy connectors merely to satisfy the contract.

`event_overlays` optionally preserves engine event graphics that are visually
part of the reusable assembly but are not map-layer tiles. This is required for
RPG Maker exterior doors. Each overlay records its local assembly coordinate,
original event ID and source-map coordinate, character sheet/name/index,
direction, pattern, priority, and through flag. Semantic validation requires
the local coordinate to be in bounds and its source coordinate to match the
layered cell provenance at that same local position; a blank character name is
never accepted as a complete graphic. Event commands and gameplay behavior are
not copied by this visual overlay record and remain adapter/game-owned.

Variations are weighted, explicitly named transformations or substitutions.
Version 0.1 leaves each variation's `operations` payload open so adapters can
define operations without pretending they are portable across engines.
