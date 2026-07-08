---
work_order_id: WO-2009
title: Atlas Academy CLI
status: proposed
priority: medium
phase: Atlas Academy
recommended_agent: codex
risk_level: medium
player_facing: false
---

# WO-2009 - Atlas Academy CLI

## Objective

Extend AtlasStudio with an Academy interface.

Implement the `atlas academy` command group as a first-class subsystem of the unified AtlasStudio CLI.

## Commands

Implement or specify stubs for:

- `atlas academy list`
- `atlas academy study`
- `atlas academy report`
- `atlas academy grade`
- `atlas academy references`
- `atlas academy help`

## Deliverables

Create:

- `tools/atlas_academy/README.md`
- `tools/atlas_academy/` CLI implementation
- `tools/atlas_academy/tests/`
- `work-orders/WO-2009-atlas-academy-cli.md`

## Constraints

Reuse the existing AtlasStudio CLI architecture.

Do not modify Atlas.

Do not modify TheLastSwordProtocol-Game.

Do not edit maps.

Do not create analysis content automatically unless explicitly requested by the command.

Preserve Immutable Formatting Rule.

## Success Criteria

Atlas Academy becomes a first-class subsystem inside AtlasStudio and can be reached through the unified CLI.
