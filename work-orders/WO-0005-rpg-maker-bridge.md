---
work_order_id: WO-0005
title: RPG Maker Bridge Design
status: proposed
project: the-last-sword-protocol
recommended_agent: claude-code
agent_role: senior-software-architect
risk_level: medium
player_facing: false
engine_specific: true
created: 2026-07-07
---

# WO-0005 - RPG Maker Bridge Design

## Purpose

Design the bridge that translates AtlasStudio engine-independent game design into RPG Maker MZ implementation work.

## Player-Facing Goal

Indirect. The bridge should help agents create playable RPG Maker builds without polluting core design documents with engine-specific details.

## Background

Atlas v1 mixed design concepts with RPG Maker implementation details such as map IDs, event IDs, switch ranges, variables, and animation IDs. AtlasStudio should keep these separate.

## Scope

### In Scope

- RPG Maker bridge folder design
- Map ownership rules
- Design-to-implementation translation model
- Work order handoff between AtlasStudio and TheLastSwordProtocol-Game
- Generated vs hand-authored content states
- Audit expectations

### Out of Scope

- Writing actual RPG Maker JSON
- Rebuilding maps
- Creating tilesets
- Final implementation scripts

## Inputs

- `studio/workflow.md`
- `projects/the-last-sword-protocol/world-model.md`
- Lessons from Atlas v1 import tools

## Deliverables

- `bridges/rpg-maker-mz/bridge-design.md`
- `bridges/rpg-maker-mz/ownership-model.md`
- Optional `bridges/rpg-maker-mz/handoff-format.md`

## Acceptance Criteria

- Core design remains engine-independent.
- RPG Maker implementation details have a defined home.
- Map ownership is protected.
- Bridge can produce implementation work orders for Codex.
- Bridge can support audits similar to Atlas v1, but focused on playable progress.

## Verification Steps

Manual architecture review.

## Allowed Changes

- `bridges/rpg-maker-mz/`

## Protected Areas

- Do not modify TheLastSwordProtocol-Game from this work order.
- Do not modify Atlas v1 repositories.

## Notes for Assigned Agent

This is a design work order, not an implementation work order. Preserve the successful ideas from Atlas v1 while avoiding its screen-first and implementation-leaking design.
