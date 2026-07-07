# Atlas Core

## Purpose

AtlasStudio should be treated as two related layers:

```text
Atlas Core
  Reusable studio platform
  Graph tooling
  Work order lifecycle
  Agent assignment
  Diagnostics
  QA intelligence
  Engine bridge framework

Projects
  Individual games and creative projects
  Project-specific canon
  Project-specific graphs
  Project-specific engine bridges
```

## Why This Matters

The Last Sword Protocol is the first AtlasStudio project, but AtlasStudio should not be designed as if it only exists for one game.

Atlas Core should become reusable for future projects, including other RPGs, simulations, visual novels, educational games, or non-game software projects.

## Atlas Core Owns

- Graph model and tooling
- Work order format and lifecycle
- Agent role model
- Provider assignment model
- Studio diagnostics
- Canon validation patterns
- Production health reporting
- Engine bridge standards
- QA report formats

## Projects Own

- Game vision
- Story canon
- World canon
- Characters
- Quests
- Region design
- Project graph facts
- Project-specific engine mappings
- Project-specific playtest goals

## Design Rule

If a feature would be useful to multiple projects, it belongs in Atlas Core.

If a feature is specific to The Last Sword Protocol, it belongs under:

```text
projects/the-last-sword-protocol/
```

## Current Direction

Phase 3 introduces Studio Intelligence: diagnostics, graph diffing, work order planning, agent scheduling, and canon linting.

These should be designed as Atlas Core capabilities first, then applied to The Last Sword Protocol as the first project.
