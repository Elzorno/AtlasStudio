# Story Reset Direction

## Purpose

This document captures the AtlasStudio v2 story reset for The Last Sword Protocol.

The goal is not to throw away the original idea. The goal is to reframe it as a classic JRPG rather than a Zelda-style sequence of screens.

## Current Decision

The Last Sword Protocol should be rebuilt around an overworld-first Dragon Quest-style structure.

The player should begin in a home region, explore an overworld, discover locations, gather clues from towns, enter caves and dungeons, defeat threats, recover protocol fragments, and gradually unlock the larger world.

## Preserve From Prior Work

Keep:

- Young hero discovers the sword.
- Sword is both magical artifact and ancient system interface.
- Ancient technology is interpreted as magic.
- Cybersecurity concepts appear as fantasy metaphors.
- Home Island / starting region remains the beginning.
- Hidden cave and sword discovery remain important.
- Node/relay/archive concepts remain part of the deeper mystery.
- Dragon Quest-style enemy variants are desirable.

## Change From Prior Work

Change:

- Replace screen-chain structure with overworld exploration.
- Stop treating each location as a Zelda-style room progression.
- Make towns, caves, castles, dungeons, shrines, and routes first-class world objects.
- Make NPC clues and world geography drive progression.
- Move RPG Maker implementation details out of story canon.

## Story Shape

The game should begin small and expand outward.

```text
Home village
  ↓
Local overworld
  ↓
Nearby cave
  ↓
Sword discovery
  ↓
First sealed location opens
  ↓
Local region threat revealed
  ↓
First relay/archive restored
  ↓
Path to mainland or next region opens
```

## Tone

The game should feel earnest, adventurous, and nostalgic without becoming parody.

It should draw on the emotional memory of classic 80s and early console fantasy adventure:

- A young hero called into danger
- Strange ancient powers
- Colorful monsters
- Townspeople with useful rumors
- Castles with worried rulers
- A widening world map
- Hopeful adventure with darker mystery beneath

## Cybersecurity Layer

The sword should gradually reveal that "magic" is partly misunderstood technology.

Early examples should be subtle:

- The sword recognizes the hero.
- Sealed doors respond to old credentials.
- Corrupted monsters behave like infected processes.
- Ancient relays fail because trust routes are broken.
- The world has forgotten the difference between spell, signal, and protocol.

## Open Questions

- Is the starting region still an island, or should it be a coastal kingdom?
- Does the hero know the sword by legend before finding it?
- Who first explains the sword incorrectly?
- Who later understands the truth more clearly?
- What is the first major villain or corrupting force called?
