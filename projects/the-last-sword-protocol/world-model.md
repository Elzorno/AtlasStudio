# The Last Sword Protocol - World Model

## Purpose

This document replaces the Atlas v1 screen-first structure with a Dragon Quest-inspired overworld-first structure.

## World Hierarchy

```text
World
  Region
    Overworld Area
    Settlement
      Town
      Village
      Castle
      Camp
    Adventure Site
      Cave
      Dungeon
      Tower
      Shrine
      Ruin
      Mine
    Route
    Landmark
    Secret
    Encounter Zone
    Story Beat
```

## Design Rule

The overworld is the connective tissue of the game.

The player should travel across an overworld map to discover towns, caves, castles, dungeons, shrines, ruins, and routes. Individual locations may have interior maps, but the world should not be modeled as a linear chain of screens.

## Location Types

### Overworld Area

A broad explorable map that connects important locations.

Owns:

- Terrain identity
- Encounter zones
- Travel gates
- Landmark placement
- Route progression
- Secrets

### Settlement

A safe or semi-safe location where the player gathers information, rests, shops, and receives story context.

Owns:

- NPCs
- Shops
- Inns
- Rumors
- Local conflict
- Quest hooks
- Cultural flavor

### Adventure Site

A dangerous or mysterious location where the player gains progression through combat, exploration, puzzles, or story events.

Owns:

- Encounter design
- Treasure
- Puzzle or traversal mechanic
- Boss or climax
- Reward
- World-state change

### Route

A constrained travel space that teaches geography, danger, or gating.

Owns:

- Encounter pacing
- One or more landmarks
- Possible blocked paths
- Clues about nearby locations

### Landmark

A memorable point on the overworld that helps orientation and storytelling.

Examples:

- Broken tower
- Old relay stone
- Abandoned checkpoint
- Sealed bridge
- Wrecked cart
- Strange glowing tree

## Region Design Template

Each region should define:

- Region name
- Role in story
- Emotional tone
- Overworld layout
- Major settlements
- Major adventure sites
- Encounter identity
- Progression gates
- Cybersecurity metaphor
- Critical path
- Optional content
- Exit to next region

## Engine Translation

This world model is engine-independent.

RPG Maker MZ implementation details such as map IDs, event IDs, switch IDs, variables, and database rows belong in an engine bridge, not in this core model.
