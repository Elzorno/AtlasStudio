---
work_order_id: WO-0012
title: Agent Scheduler
status: proposed
project: atlasstudio
recommended_agent: claude-code
agent_role: senior-software-architect
risk_level: medium
player_facing: false
engine_specific: false
created: 2026-07-07
---

# WO-0012 - Agent Scheduler

## Purpose

Design an agent scheduling model that recommends the best AI provider or agent for each work order based on task type, capability, risk, and available session/quota status.

## Player-Facing Goal

Indirect. Better agent assignment should conserve limited sessions and use each model where it is strongest.

## Background

The human creator uses GPT, Claude Code, Codex, GitHub Copilot, and local/Ollama models. AtlasStudio should eventually understand which agent is best suited to a task and whether that agent is currently available.

## Scope

### In Scope

- Agent capability profiles.
- Manual quota/session status fields.
- Task classification.
- Risk-based routing.
- Fallback agent logic.
- Recommendation output format.
- Graph representation for providers and agents.

### Out of Scope

- Live provider API integration.
- Automatic dispatch.
- Credential storage.
- Cost billing integration.

## Inputs

- `studio/agent-roles.md`
- `work-orders/WO-0004-agent-assignment-system.md`
- Atlas Graph production nodes and edges

## Deliverables

- `studio/scheduling/agent-scheduler-design.md`
- Optional `schemas/agent-status.schema.json`
- Optional sample `studio/scheduling/agent-status.example.json`

## Acceptance Criteria

- Scheduler can recommend an agent for a work order.
- Scheduler can explain the recommendation.
- Scheduler can use manual quota/session fields.
- Scheduler can identify fallback agents.
- Scheduler does not depend on provider APIs.

## Verification Steps

Manual review using existing work orders as examples.

## Allowed Changes

- `studio/scheduling/`
- `schemas/`
- production graph files if needed

## Protected Areas

- Do not store secrets.
- Do not attempt live provider API calls.
- Do not modify game repositories.

## Notes for Assigned Agent

Start manual-first. APIs for session limits may not exist or may not be accessible. AtlasStudio should still be useful if the human updates status manually.
