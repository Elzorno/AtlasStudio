# Work Order Format

AtlasStudio work orders are structured Markdown files with YAML frontmatter.

## Required Frontmatter

```yaml
---
work_order_id: WO-0000
title: Short Action Title
status: proposed
project: the-last-sword-protocol
recommended_agent: atlasstudio
fallback_agent: human
agent_role: director
risk_level: low
player_facing: true
engine_specific: false
created: 2026-07-07
---
```

`fallback_agent` is optional. It names the next-best agent if `recommended_agent` is unavailable or over its risk ceiling, per `studio/agent-assignment-model.md`'s fallback chain. Older work orders may omit it.

## Recommended Status Values

- proposed
- approved
- assigned
- in_progress
- submitted
- qa_review
- needs_revision
- accepted
- closed

## Recommended Agents

- atlasstudio
- gpt
- claude-code
- codex
- github-copilot
- ollama
- human

## Work Order Body Template

```markdown
# WO-0000 - Title

## Purpose

What is this work order trying to accomplish?

## Player-Facing Goal

What should be better for the player after this work is complete?

## Background

Relevant canon, technical context, or prior work.

## Scope

### In Scope

- Item 1
- Item 2

### Out of Scope

- Item 1
- Item 2

## Inputs

- Source document or repo path
- Prior work order
- Design decision

## Deliverables

- File, document, build artifact, or implementation result

## Acceptance Criteria

- Concrete testable condition
- Concrete testable condition

## Verification Steps

```bash
command or manual review step
```

## Allowed Changes

- Paths or systems the agent may change

## Protected Areas

- Paths or systems the agent must not change

## Notes for Assigned Agent

Specific implementation guidance.
```

## Work Order Design Standard

A good work order should be small enough for one agent session but meaningful enough to improve the game.

Prefer:

> Build Ashford Village as a functional starting town with five NPCs, one shop, one inn, one story hook, and one exit to the overworld.

Avoid:

> Make the game better.
