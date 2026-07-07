---
work_order_id: WO-0012
title: Capability-Based Orchestration Engine
status: proposed
project: atlasstudio
recommended_agent: claude-code
agent_role: senior-software-architect
risk_level: medium
player_facing: false
engine_specific: false
created: 2026-07-07
supersedes: Agent Scheduler
---

# WO-0012 - Capability-Based Orchestration Engine

## Status Note

The original WO-0012 concept, **Agent Scheduler**, is retired in place.

Reason:

AtlasStudio should not assign work directly to named agents first. It should identify the capabilities required by a work order, then match those capabilities to available providers.

This work order replaces the scheduler concept with a capability-based orchestration model.

## Purpose

Design the orchestration layer that maps work requirements to capabilities, capabilities to providers, and providers to assignments based on availability, confidence, quota, cost, locality, and project policy.

## Player-Facing Goal

Indirect. Better orchestration should conserve limited AI sessions, use each provider where it is strongest, and improve production throughput.

## Background

The human creator uses GPT, Claude Code, Codex, GitHub Copilot, and local/Ollama models. AtlasStudio should eventually understand which capabilities a task requires and which provider is best suited to supply those capabilities at the current moment.

This work order continues the AtlasStudio shift from direct agent assignment to capability-driven production.

## Architecture Direction

AtlasStudio should reason in this order:

```text
Planning Engine
  ↓
Recommended Work
  ↓
Required Capabilities
  ↓
Capability Registry
  ↓
Provider Registry
  ↓
Provider Status
  ↓
Primary and Fallback Assignments
  ↓
Human Approval
```

## Scope

### In Scope

- Define capability registry structure.
- Define provider registry structure.
- Define manual provider status model.
- Define capability matching rules.
- Define assignment scoring rules.
- Define primary and fallback assignment output.
- Define human provider support.
- Define how work orders declare required and preferred capabilities.
- Define how orchestration findings should be reported.
- Keep provider API integration optional and future-facing.

### Out of Scope

- Live provider API integration.
- Automatic dispatch to AI systems.
- Credential storage.
- Cost billing integration.
- Calendar scheduling.
- Modifying RPG Maker repositories.
- Running external model calls.

## Inputs

- `studio/agent-roles.md`
- `studio/atlas-core.md`
- `studio/work-order-format.md`
- `tools/atlas_planner/`
- Atlas Graph production nodes and edges
- Existing work orders

## Deliverables

- `atlas-core/capabilities/` registry files.
- `atlas-core/providers/` registry files.
- `atlas-core/orchestration/provider-status.example.json`.
- `studio/orchestration/capability-based-orchestration.md`.
- Optional schema files for capabilities, providers, and provider status.
- A proposed work-order frontmatter extension for `required_capabilities` and `preferred_capabilities`.
- Optional implementation follow-up work order for Codex if this work order remains design-only.

## Required Registry Concepts

### Capability Registry

Capabilities describe what a task needs.

Examples:

- architecture-review
- python-development
- creative-writing
- graph-analysis
- schema-design
- documentation
- qa-review
- rpg-maker-json
- canon-design
- human-approval

### Provider Registry

Providers describe who or what can supply capabilities.

Examples:

- gpt
- claude-code
- codex
- github-copilot
- ollama
- human

### Provider Status

Provider status should be manual-first.

Useful fields:

- available
- quota_remaining
- reset_time
- online
- cost_class
- local
- notes

No secrets should be stored.

## Work Order Metadata Direction

Future work orders should be able to declare capabilities directly.

Example:

```yaml
required_capabilities:
  - architecture-review
  - schema-design
preferred_capabilities:
  - graph-analysis
human_review: required
```

The orchestrator should use these fields when available and infer capabilities from existing fields only as a fallback.

## Acceptance Criteria

- AtlasStudio has a documented capability-based orchestration model.
- Capabilities are modeled separately from providers.
- Providers advertise capabilities independently.
- Human is modeled as a provider with approval, creative-direction, final-canon, and risk-acceptance capabilities.
- Manual provider status can influence recommendations.
- Primary and fallback assignments are supported.
- Assignment decisions are explainable.
- The model remains provider-agnostic.
- The design does not require live provider APIs.
- Existing work orders can still be interpreted during transition.

## Verification Steps

Manual architecture review using at least these examples:

```bash
# Future example commands if implemented later:
python3 tools/atlas_orchestrator/orchestrator.py --work-order WO-0005
python3 tools/atlas_orchestrator/orchestrator.py --status atlas-core/orchestration/provider-status.example.json
python3 tools/atlas_planner/planner.py
python3 tools/atlas_doctor/doctor.py
```

## Allowed Changes

- `atlas-core/capabilities/`
- `atlas-core/providers/`
- `atlas-core/orchestration/`
- `studio/orchestration/`
- `schemas/`
- production graph files if needed
- this work order file

## Protected Areas

- Do not store secrets.
- Do not attempt live provider API calls.
- Do not modify game repositories.
- Do not change story canon.
- Do not run broad formatters.

## Notes for Assigned Agent

Start with architecture and registry design. Do not overbuild provider automation. The goal is to make AtlasStudio choose providers based on capabilities rather than hardcoded agent names.

Formatting: preserve existing house style and avoid broad rewrites.
