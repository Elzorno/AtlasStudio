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

## Studio Diagnostics

Run the Studio Doctor for a readable project health report:

```bash
python3 tools/atlas_doctor/doctor.py
python3 tools/atlas_doctor/doctor.py --project the-last-sword-protocol
python3 tools/atlas_doctor/doctor.py --output reports/atlas-doctor/latest.md
```

The report summarizes graph integrity, orphan nodes, missing sources, work order status, implementation readiness, registered tools, and recommendations.

## Graph Diffing

Compare two Atlas Graph states to see which facts were added, removed, or changed:

```bash
python3 tools/atlas_graph/diff_graph.py --base HEAD~1 --head HEAD
python3 tools/atlas_graph/diff_graph.py --base HEAD
python3 tools/atlas_graph/diff_graph.py --base-dir old_graph --head-dir projects/the-last-sword-protocol/graph
```

The report groups changes by canon, production, and bridge scope, and highlights status changes, scope moves, and source reference changes. See `studio/atlas-graph/diff-model.md` for the full model.

## Immutable Formatting Guard

Check graph JSON changes for suspicious formatting churn without rewriting files:

```bash
python3 tools/atlas_format/format_guard.py --check
python3 tools/atlas_format/format_guard.py --check --base HEAD~1 --head HEAD
python3 tools/atlas_format/format_guard.py --check --output reports/atlas-format/latest.md
```

The guard is check-only. It reports formatting-only graph JSON changes separately from semantic graph fact changes and warns when broad non-semantic churn may obscure review.
