---
work_order_id: WO-0001
title: AtlasStudio Foundation
status: accepted
project: atlasstudio
recommended_agent: gpt
agent_role: director
risk_level: low
player_facing: false
engine_specific: false
created: 2026-07-07
---

# WO-0001 - AtlasStudio Foundation

## Purpose

Create the initial AtlasStudio repository foundation.

## Player-Facing Goal

No direct player-facing change yet. This establishes the production system that will guide future playable builds.

## Background

Atlas v1 proved that AI-assisted game development benefits from canon, work orders, validation, and explicit ownership. AtlasStudio starts fresh as a game studio director rather than a document generator.

## Scope

### In Scope

- README
- Studio vision
- Agent roles
- Workflow
- Work order format
- Initial Last Sword Protocol project model

### Out of Scope

- RPG Maker implementation
- Import/export scripts
- Playable game changes
- Final story decisions

## Deliverables

- `README.md`
- `studio/vision.md`
- `studio/agent-roles.md`
- `studio/workflow.md`
- `studio/work-order-format.md`
- `projects/the-last-sword-protocol/game-vision.md`
- `projects/the-last-sword-protocol/story-reset.md`
- `projects/the-last-sword-protocol/world-model.md`
- `projects/the-last-sword-protocol/home-region.md`

## Acceptance Criteria

- AtlasStudio is clearly defined as a director/coordinator.
- The Last Sword Protocol is reframed as an overworld-first JRPG.
- Agent roles are documented.
- Work order format is documented.
- RPG Maker implementation details are separated from core design.

## Verification Steps

Manual review of the committed Markdown files.

## Allowed Changes

- Repository foundation files

## Protected Areas

- No other repositories should be changed by this work order.

## Notes for Assigned Agent

This work order is complete once the initial foundation files are committed.
