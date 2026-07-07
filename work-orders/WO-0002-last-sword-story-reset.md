---
work_order_id: WO-0002
title: Last Sword Protocol Story Reset
status: proposed
project: the-last-sword-protocol
recommended_agent: gpt
agent_role: creative-systems-designer
risk_level: medium
player_facing: true
engine_specific: false
created: 2026-07-07
---

# WO-0002 - Last Sword Protocol Story Reset

## Purpose

Refactor the current Last Sword Protocol story into a Dragon Quest-inspired JRPG structure.

## Player-Facing Goal

The player should experience a world-driven adventure rather than a chain of disconnected screens.

## Background

The current prototype became too Zelda-like, with screen-by-screen progression. The desired direction is overworld exploration with towns, caves, castles, dungeons, shrines, and classic turn-based JRPG progression.

## Scope

### In Scope

- Reframe the story around regions and overworld exploration.
- Preserve the sword/protocol premise.
- Preserve subtle cybersecurity metaphors.
- Define the first three major story arcs at a high level.
- Identify which Atlas v1 concepts should be kept, revised, or retired.

### Out of Scope

- RPG Maker map IDs
- Event JSON
- Final dialogue
- Full game script
- Final boss balancing

## Inputs

- `projects/the-last-sword-protocol/game-vision.md`
- `projects/the-last-sword-protocol/story-reset.md`
- `projects/the-last-sword-protocol/world-model.md`
- Prior Atlas v1 materials as reference only

## Deliverables

- `projects/the-last-sword-protocol/story-bible.md`
- Updated list of preserved/revised/retired Atlas v1 concepts
- High-level Journey 1, Journey 2, and Journey 3 arc summaries

## Acceptance Criteria

- Story supports overworld-first JRPG progression.
- First three arcs have clear player goals.
- Cybersecurity concepts are embedded subtly.
- The sword remains central.
- The structure avoids returning to screen-chain design.

## Verification Steps

Manual review by the human creator.

## Allowed Changes

- `projects/the-last-sword-protocol/`

## Protected Areas

- Do not change RPG Maker game files.
- Do not change Atlas v1 repositories.

## Notes for Assigned Agent

Focus on playable adventure structure, not lore density. The story should help build the game.
