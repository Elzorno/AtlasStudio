# Capability-Based Orchestration

## Purpose

AtlasStudio should assign work based on required capabilities, not hardcoded agent names.

Agents and providers are replaceable. Capabilities are the stable abstraction.

## Core Flow

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
Assignment Recommendation
  ↓
Human Approval
```

## Why Capabilities First

If a work order says "use Claude," the workflow is tied to a vendor or tool.

If a work order says "requires architecture-review and schema-design," AtlasStudio can choose the best available provider at the time.

This allows AtlasStudio to adapt when:

- a provider is out of quota
- a stronger model becomes available
- a local model is sufficient
- a task should be split across providers
- human review is required

## Capabilities

Capabilities describe what work requires.

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

## Providers

Providers describe who or what can supply capabilities.

Examples:

- GPT
- Claude Code
- Codex
- GitHub Copilot
- Ollama
- Human

## Human As Provider

The human creator is modeled as a provider because some capabilities cannot be delegated.

Human-only or human-primary capabilities include:

- final-canon
- creative-direction
- risk-acceptance
- scope-approval
- merge-approval

## Provider Status

Provider status should be manual-first.

The first implementation should support a checked-in example file and a local ignored status file later.

Status may include:

- available
- quota_remaining
- reset_time
- online
- local
- cost_class
- notes

No secrets should be stored.

## Assignment Output

The orchestrator should recommend:

- required capabilities
- primary provider for each capability
- fallback provider for each capability
- confidence or score
- explanation
- any human approval requirement

## Design Rule

The orchestrator recommends. It does not dispatch automatically.

Human approval remains required before execution.
