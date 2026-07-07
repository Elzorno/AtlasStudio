# Home Region - Starting Region Draft

## Purpose

This is the first AtlasStudio v2 region model for The Last Sword Protocol.

It replaces the previous Home Island screen-chain with an overworld-first JRPG region.

## Working Name

Home Region

Possible final names:

- Ashford Vale
- Eldermere Island
- Hearthwatch Coast
- Greenwake Isle
- Elara's Reach

## Role In Game

The Home Region teaches the player how the world works.

It should include:

- A starting village
- A local overworld
- A nearby cave where the sword is found
- A small castle or elder hall that gives regional context
- A sealed ruin or relay site that cannot be understood at first
- A first dungeon or dangerous site after the sword is obtained
- A departure point to the next region

## Region Structure

```text
Home Region Overworld
  Ashford Village
  Elara's House
  Old North Road
  Hidden Cave
  Sword Shrine / Sanctum
  Glassfield Ruins
  Sealed Relay Node
  Rustshore Dock
  Optional: Fogfen Marsh
  Optional: Watchtower or small castle outpost
```

## Player Progression

```text
Start in Ashford Village
  ↓
Learn local rumors
  ↓
Explore overworld
  ↓
Find Hidden Cave
  ↓
Discover the sword
  ↓
Return to village or elder
  ↓
Use sword to open Glassfield Ruins
  ↓
Restore first relay/archive fragment
  ↓
Unlock Rustshore Dock
  ↓
Leave for next region
```

## Required Locations

### Ashford Village

Starting town.

Purpose:

- Establish home
- Teach NPC interaction
- Provide first supplies
- Hint at tremors, strange lights, or old ruins

### Home Region Overworld

Main exterior map connecting all starting locations.

Purpose:

- Teach exploration
- Provide low-risk encounters
- Show landmarks before they are usable
- Let the player see places they cannot access yet

### Hidden Cave

First adventure site.

Purpose:

- Teach dungeon exploration
- Lead to the sword discovery
- Introduce ancient technology as mystery

### Sword Shrine / Sanctum

Discovery site.

Purpose:

- The sword recognizes the hero
- First authentication metaphor
- Unlocks new progression

### Glassfield Ruins

First post-sword sealed site.

Purpose:

- Show that the sword is a key/interface
- Introduce corrupted constructs or protocol ghosts

### Sealed Relay Node

First major objective.

Purpose:

- Restore a local relay/archive fragment
- Reveal that the world has a hidden ancient infrastructure
- Unlock travel to next region

### Rustshore Dock

Departure point.

Purpose:

- Transition to Journey 2
- Show the world is larger than the starting region

## Encounter Identity

Early enemies should be simple, readable, and variant-friendly.

Examples:

- Slimes / Glitches / Gel Wisps
- Bats / Cave Flutterers
- Tiny Golems / Pebble Constructs
- Scorpions / Rust Stingers
- Skeletons / Archive Husks
- Corrupted Sprites / Bit Wraiths

Enemy variants should reuse base sprites with recolors, renamed abilities, and adjusted stats.

## Cybersecurity Metaphor

The Home Region teaches authentication and access control.

Fantasy layer:

- The sword chooses the hero.
- Old doors open only to the recognized bearer.
- Ruins reject corrupted entities.
- The relay trusts the sword's signal.

Underlying concept:

- Authentication
- Authorization
- Tokens
- Trust relationship
- Broken relay path

## Design Notes

This region should feel open but controlled. The player should be able to wander, but NPC hints, encounter strength, and progression gates should naturally guide them.

The first playable goal should be a short but complete loop: village → overworld → cave → sword → ruins → relay → dock.
