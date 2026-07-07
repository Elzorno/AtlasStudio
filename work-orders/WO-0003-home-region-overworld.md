---
work_order_id: WO-0003
title: Home Region Overworld Design
status: proposed
project: the-last-sword-protocol
recommended_agent: gpt
agent_role: creative-systems-designer
risk_level: medium
player_facing: true
engine_specific: false
created: 2026-07-07
---

# WO-0003 - Home Region Overworld Design

## Purpose

Design the starting region as an overworld-first JRPG region.

## Player-Facing Goal

The player should begin in a small but explorable region with a village, overworld, cave, ruins, relay site, and departure point.

## Background

Atlas v1 modeled Home Island as a chain of screens. AtlasStudio v2 should model it as a JRPG region where the overworld connects locations.

## Scope

### In Scope

- Region map concept
- Required locations
- Progression gates
- Encounter zones
- NPC clue flow
- First-playable route
- Optional content hooks

### Out of Scope

- RPG Maker map IDs
- Tile-level layout
- Final art
- Event JSON
- Final dialogue

## Inputs

- `projects/the-last-sword-protocol/home-region.md`
- `projects/the-last-sword-protocol/world-model.md`

## Deliverables

- `projects/the-last-sword-protocol/regions/home-region-overworld.md`

## Acceptance Criteria

- Region contains a clear overworld layout.
- Region supports village → overworld → cave → sword → ruins → relay → dock progression.
- Region includes at least one optional location or secret.
- Region includes encounter identity.
- Region includes NPC clue logic.

## Verification Steps

Manual design review.

## Allowed Changes

- `projects/the-last-sword-protocol/regions/`

## Protected Areas

- Do not change engine implementation files.

## Notes for Assigned Agent

Design this like a classic Dragon Quest starting region. The player should know where to go from NPC hints and visible geography, not from quest markers.
