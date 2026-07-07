---
work_order_id: WO-0004
title: Agent Assignment System
status: proposed
project: atlasstudio
recommended_agent: claude-code
agent_role: senior-software-architect
risk_level: medium
player_facing: false
engine_specific: false
created: 2026-07-07
---

# WO-0004 - Agent Assignment System

## Purpose

Design the first version of AtlasStudio's agent assignment model.

## Player-Facing Goal

Indirect. Better agent assignments should produce better playable game builds faster.

## Background

The human creator wants AtlasStudio to coordinate GPT, Claude Code, Codex, GitHub Copilot, and local/Ollama models. One goal is to conserve session usage by routing work to the best available agent.

## Scope

### In Scope

- Agent capability model
- Task classification model
- Assignment metadata
- Quota/session availability fields
- Risk-based assignment rules
- Recommended JSON/YAML schema

### Out of Scope

- Live API integration with provider quota systems
- Automated dispatch to providers
- GUI dashboard
- GitHub Actions implementation

## Inputs

- `studio/agent-roles.md`
- `studio/work-order-format.md`

## Deliverables

- `studio/agent-assignment-model.md`
- Optional schema draft in `schemas/work-order.schema.json`

## Acceptance Criteria

- Work orders can specify recommended agent and fallback agent.
- Assignment model accounts for strengths, quota, risk, and task type.
- Model supports manual entry of session status if APIs do not expose it.
- Model does not depend on any one AI provider.

## Verification Steps

Manual review and test against WO-0002 through WO-0005.

## Allowed Changes

- `studio/`
- `schemas/`

## Protected Areas

- Do not change project story files unless needed for examples.

## Notes for Assigned Agent

Assume quota APIs may not be available. Design for manual status updates first, automated provider connectors later.
