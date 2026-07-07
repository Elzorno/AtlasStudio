# AtlasStudio

AtlasStudio is an AI game studio director and multi-agent coordination framework.

AtlasStudio exists to help human creators and AI agents build complete games together without losing canon, context, ownership, or production direction.

## Current Focus

The first production project is **The Last Sword Protocol**, a classic Dragon Quest-inspired JRPG built around overworld exploration, towns, caves, castles, dungeons, turn-based combat, and story-driven progression.

## Core Principle

AtlasStudio is not a document generator.

AtlasStudio is the director.

It owns creative direction, canon, work orders, agent assignments, acceptance tests, and production readiness. It does not directly own engine-specific implementation details such as RPG Maker map IDs, raw event JSON, final asset files, or hand-authored maps.

## Repository Layout

```text
studio/
  vision.md
  agent-roles.md
  workflow.md
  work-order-format.md

projects/
  the-last-sword-protocol/
    game-vision.md
    story-reset.md
    world-model.md
    home-region.md

work-orders/
  WO-0001-atlasstudio-foundation.md
  WO-0002-last-sword-story-reset.md
  WO-0003-home-region-overworld.md
  WO-0004-agent-assignment-system.md
  WO-0005-rpg-maker-bridge.md
```

## Relationship to Atlas v1

Atlas v1 proved that structured canon, work orders, validation, and machine-readable exports can help AI agents coordinate. AtlasStudio starts fresh from those lessons and shifts the emphasis from artifact production to playable game production.

Atlas v1 is the research prototype. AtlasStudio is the production director.
