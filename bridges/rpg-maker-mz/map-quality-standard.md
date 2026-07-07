# RPG Maker MZ Map Quality Standard

## Purpose

The Last Sword Protocol should not merely have functional maps. It should have maps that feel worthy of a polished classic JRPG.

The previous prototype produced maps that were technically present but visually uninspired, sloppy, and aligned to the wrong screen-by-screen gameplay model. AtlasStudio v2 should target Dragon Quest-style regional exploration with map quality comparable to strong RPG Maker MZ sample/demo maps.

## Quality Bar

A completed map should pass this question:

> Would this be believable as a polished RPG Maker MZ sample map adapted to The Last Sword Protocol's story?

If the answer is no, the map is not finished.

## Design Principle

AtlasStudio should generate map briefs and implementation contracts, not blindly generate final maps.

Map implementation should be tile-constrained, passability-aware, and validated against RPG Maker data.

## Required Map Qualities

Every shipped map should demonstrate:

- Clear gameplay purpose
- Clear narrative purpose
- Strong visual composition
- Readable player paths
- Believable environmental detail
- At least one memorable landmark when appropriate
- No empty filler space
- No sloppy repeated decoration patterns
- No disconnected screen-chain feel unless the location truly requires it
- Passability consistent with RPG Maker's tileset rules

## Visual Composition Standard

Maps should use composition techniques common in high-quality RPG Maker demo maps:

- paths that curve or branch naturally
- irregular building placement where appropriate
- layered environmental detail
- elevation, cliffs, fences, water, or vegetation to guide movement
- landmarks that orient the player
- small story details such as carts, tools, gardens, ruins, or worn paths
- negative space used intentionally, not as empty filler

## Dragon Quest Alignment

For overworld and town maps, the player should feel they are exploring a place in a larger world.

Avoid Zelda-style screen chains where the map primarily exists to connect adjacent puzzle rooms.

The intended flow is:

```text
Town
  ↓
Overworld
  ↓
Discovery
  ↓
Adventure Site
  ↓
Return or Continue
```

## Map Brief Requirement

Each new map should be preceded by a map design brief containing:

- emotional goal
- gameplay goal
- narrative goal
- dimensions or target scale
- tileset assumptions
- required landmarks
- required paths
- required events
- required transfers
- visual references or benchmark notes
- passability expectations
- acceptance criteria

## Image Generation Role

Image generation may be used for concept art, composition reference, mood boards, or visual direction.

Image generation must not be treated as direct RPG Maker map data.

It cannot be trusted for:

- exact tile IDs
- RPG Maker autotile behavior
- passability
- event placement
- transfer correctness

## Implementation Rule

Codex or any implementation agent should translate approved briefs and visual references into RPG Maker maps using actual project tilesets and RPG Maker data.

Implementation agents must not invent passability behavior or overwrite tileset rules unless a work order explicitly authorizes the change.

## Acceptance

A map is accepted only when it is:

1. visually coherent
2. playable
3. passability-correct
4. aligned to the JRPG Design Bible
5. faithful to its map brief
6. reviewed against the sample-map quality bar
