# Imported Entity Model

## Purpose

This document defines how AtlasStudio should represent information imported from `TheLastSwordProtocol-Atlas`, per the architecture in `import-architecture.md`. Every entity type below is a **read-only mirror** of an Atlas-owned fact. None of them are canon. None of them may be edited directly - they exist to be read, queried, validated, diffed, and scheduled against.

## Common Provenance Fields (Every Entity)

Every imported entity, regardless of `kind`, carries these fields, per `import-architecture.md`'s Traceability section:

```json
{
  "kind": "character | location | quest | work_order | asset | implementation_packet | map | npc | dialogue_reference",
  "source_repository": "TheLastSwordProtocol-Atlas",
  "source_path": "atlas/docs/05_Characters/Grandmother_Elara.md",
  "source_identifier": "NPC-ELA-001",
  "source_commit": "bc3598b",
  "imported_at": "2026-07-07T00:00:00Z",
  "imported_version": 1,
  "status_at_source": "Draft",
  "canonical_at_source": true
}
```

`status_at_source` and `canonical_at_source` are copied directly from the source frontmatter's `status` and `canonical` fields - AtlasStudio does not decide canonicity; it reports what Atlas already declared.

## Entity Types

### `character`

Mirrors an Atlas `object_type: NPC` or actor-level character document.

```json
{
  "kind": "character",
  "atlas_object_id": "NPC-ELA-001",
  "title": "Grandmother Elara",
  "appears_in": ["LOC-ASH-001"],
  "related_to": ["CHR-KAI-001", "LOC-SKY-001", "QST-HOM-001", "QST-HOM-002"],
  "implementation_status": "In Progress"
}
```

`appears_in` and `related_to` are copied verbatim from the source's `relationships` block - AtlasStudio does not add, remove, or reinterpret a relationship Atlas did not state.

### `location`

Mirrors an Atlas `object_type: Location` or region/location document (`atlas/docs/02_World/Locations/`, `Regions/`).

```json
{
  "kind": "location",
  "atlas_object_id": "LOC-ASH-001",
  "title": "Ashford",
  "region": "REG-HOM-001",
  "contains_screens": ["SCR-HOM-ASH-001", "SCR-HOM-ASH-002", "SCR-HOM-ASH-003"]
}
```

### `quest`

Mirrors a quest document under `atlas/docs/03_Story/Quests/`.

```json
{
  "kind": "quest",
  "atlas_object_id": "QST-HOM-001",
  "title": "(imported from source; not restated here)",
  "involves_characters": ["NPC-ELA-001"],
  "involves_locations": ["LOC-ASH-001"]
}
```

### `work_order`

Mirrors an entry from `atlas/workorders/*.md` joined with its matching record in `atlas/planning/workorder_queue.json`, since (per `import-architecture.md`'s Parsing section) the individual work order files carry no frontmatter of their own - their structured metadata lives in the queue.

```json
{
  "kind": "work_order",
  "atlas_object_id": "WO-0036",
  "title": "Build Gate A Ashford Exterior Production Map",
  "active": false,
  "milestone": "Milestone 7 - Runtime Playtest Certification",
  "priority": 30,
  "completion_note": "(copied verbatim from the queue record, if present)",
  "dependencies": ["WO-0031", "IMP-HOM-017"]
}
```

### `asset`

Mirrors an ownership-relevant reference to an art/audio/effect file - never the binary file itself (see "What Should Not Be Imported").

```json
{
  "kind": "asset",
  "atlas_object_id": "(asset mapping entry, if Atlas assigns one)",
  "referenced_by": ["SCR-HOM-ASH-001"],
  "asset_path_in_game_repo": "img/tilesets/Outside_A2.png",
  "ownership_note": "Final asset; game_owns per the export contract"
}
```

### `implementation_packet`

Mirrors an `object_type: ImplementationPacket` document.

```json
{
  "kind": "implementation_packet",
  "atlas_object_id": "IMP-HOM-017",
  "title": "Manual Map Build - Ashford Exterior",
  "implements": ["SCR-HOM-ASH-001", "LOC-ASH-001"],
  "requires": ["IMP-HOM-001"],
  "implementation_status": "Not Started"
}
```

### `map`

Mirrors a screen/map pairing, drawing on both the Atlas screen object and `TheLastSwordProtocol-Game`'s `map_ownership.json` and `MapInfos.json` - the one entity type that must cross-reference two source repositories, since Atlas owns the screen definition and the Game repository owns the ownership ledger and the physical map file.

```json
{
  "kind": "map",
  "atlas_object_id": "SCR-HOM-ASH-001",
  "rpg_maker_map_name": "TWN_Ashford_Exterior",
  "rpg_maker_map_id": 1,
  "ownership_state": "hand_authored",
  "ownership_source": "TheLastSwordProtocol-Game/map_ownership.json",
  "implementation_packet": "IMP-HOM-017"
}
```

### `npc`

A finer-grained sibling of `character`, used when Atlas or the export distinguishes a placed, in-map NPC instance (an event on a specific map) from the character concept itself. Where the export or frontmatter does not make this distinction, `npc` and `character` may refer to the same underlying record - AtlasStudio does not invent a distinction Atlas does not draw.

```json
{
  "kind": "npc",
  "atlas_object_id": "NPC-ELA-001",
  "placed_on_map": "SCR-HOM-ASH-002",
  "character_ref": "NPC-ELA-001"
}
```

### `dialogue_reference`

**Not** the dialogue text itself (see "What Should Not Be Imported"). A pointer to where dialogue content lives in Atlas, so AtlasStudio can schedule and track dialogue-authoring work without holding a copy of the words.

```json
{
  "kind": "dialogue_reference",
  "atlas_object_id": "(dialogue packet or screen ID that owns this dialogue)",
  "source_path": "atlas/docs/03_Story/Dialogue/...",
  "associated_npc": "NPC-ELA-001",
  "associated_screen": "SCR-HOM-ASH-002"
}
```

## Reused Entity Types (Not New)

`production_state` (Atlas's `production_readiness` export block) and `tileset`/`transfer`/`event` (already present in the Home Island export's `home_island` payload) are imported using the same common provenance envelope above, without needing bespoke entity types beyond what the export already structures - the export's own field names should be preserved rather than renamed, to keep traceability to the source unambiguous.

## What Should NOT Be Imported

- **Dialogue text itself.** Only `dialogue_reference` pointers are imported. Full dialogue content stays in Atlas; AtlasStudio never holds a copy that could drift from the source and be mistaken for current.
- **Binary assets** (art, audio, effects, fonts). Only ownership/reference metadata (`asset` entities) is imported, never the files themselves - AtlasStudio has no rendering or playback need for them and importing binaries would blur the "mirror, not a copy of the game" boundary.
- **Atlas's own internal tooling/session state** (`atlas/orchestrator/session_state.example.json`, `task_categories.json`, `assignment_policy.md`). These configure Atlas's *own* orchestrator, which AtlasStudio does not drive - importing them would imply AtlasStudio intends to operate Atlas's orchestrator by proxy, which it does not.
- **Save data and runtime files** (`TheLastSwordProtocol-Game/save/`). Explicitly out of scope for any design or production concern.
- **Locked Decision Records' internal deliberation** (only their final decision and ID should be imported as a reference, e.g. `ATLAS-DDR-0003`, not reproduced in full - AtlasStudio should point to a Decision Record, not restate it, so the restatement can never drift from the original).
- **Anything from the retired legacy fork** (`rpgmakerLSP/atlas/`). That fork is already retired per Atlas's own `WO-0029`; importing from it would reintroduce exactly the stale-canon risk that work order eliminated.

## Query Compatibility

Because every imported entity uses a `kind` field and common provenance envelope, AtlasStudio's existing graph query tooling (`tools/atlas_graph/query_graph.py`) could, in a future implementation, be pointed at the imported cache using the same command shape it already supports (`get`, `neighbors`, `status`, `missing-sources`) - `missing-sources` becomes especially useful here, since a broken `source_path` in the imported cache is exactly the kind of import-integrity problem that check already knows how to surface.
