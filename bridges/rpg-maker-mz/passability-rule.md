# RPG Maker MZ Passability Rule

## Purpose

Passability is gameplay logic, not visual decoration.

The previous prototype exposed passability problems, including cases where walls or other visually blocking tiles could be walked through. AtlasStudio must prevent visually correct but mechanically broken maps.

## Core Rule

AtlasStudio must treat RPG Maker passability as engine data.

Use the passability settings already defined in the RPG Maker tileset whenever possible.

Do not override passability unless a work order explicitly authorizes it.

## Default Policy

Implementation agents must:

- read `Tilesets.json`
- respect tile passability flags
- preserve default tileset passability
- avoid custom passability edits unless authorized
- document any passability override
- validate all required routes before acceptance

## Prohibited By Default

Unless explicitly approved, agents must not:

- change tileset passage settings
- make wall, roof, cliff, water, or blocking terrain passable
- place required events on unreachable tiles
- place transfers behind impassable tiles
- place player starts on impassable tiles
- rely on visual appearance alone to infer walkability

## Required Validation

Before any map implementation is accepted, AtlasStudio should verify:

- player start is on a passable tile
- required NPCs are reachable when intended
- required transfers are reachable
- required events are reachable
- required routes are walkable
- walls, roofs, cliffs, and water are not walkable unless intended
- no custom passability overrides exist without documentation

## Route Validation

Each map implementation package should define required routes.

Examples:

```text
player_start -> village_green
village_green -> general_store_door
village_green -> blacksmith_door
village_green -> north_exit
```

A validator should eventually test these routes using map data and tileset passability flags.

## Human Playtest Still Required

Automated passability validation is necessary but not sufficient.

A human playtest must still confirm:

- movement feels natural
- visual boundaries match collision boundaries
- paths are readable
- no important route feels awkward or misleading

## Acceptance Rule

A map with known passability errors cannot be accepted, even if it looks good.
