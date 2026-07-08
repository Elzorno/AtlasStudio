# Agent Usage Guide

## Purpose

`studio/agent-roles.md` states each agent's role in one paragraph. `studio/scheduling/agent-scheduler-design.md` scores each agent numerically per task class. This document sits between the two: a practical, day-to-day reference for when a Production Director should reach for each agent, when not to, and why - so an assignment decision at Step 5 of `DAILY_WORKFLOW.md` does not require re-deriving the scheduler's scoring table from scratch every time.

This document does not change any capability score, risk ceiling, or avoid rule already established in `agent-roles.md` or `agent-scheduler-design.md`. It restates them as usage guidance.

## GPT

**Role:** Creative systems designer.

**Strengths:** Story design, quest structure, dialogue, NPC concepts, region planning, pacing, and translating real-world cybersecurity concepts into the game's fantasy metaphor layer. Scores `3` (primary strength) on `creative_design` in the Agent Scheduler's capability table.

**Limitations:** Scores `0` on `architecture` and `implementation` - not a reflection of general capability, but a statement that this is not where GPT's assignment should go. Weak fit for large code refactors or raw RPG Maker JSON editing.

**Recommended work types:** Anything classified `canon` by the Work Order Router (`work-orders/WO-0021`) - and note that `canon` work is routed to `TheLastSwordProtocol-Atlas`, not authored inside AtlasStudio, regardless of which agent drafts it. Within AtlasStudio's own scope, GPT is the right agent for early creative drafts intended for Atlas's own review process.

**When NOT to use GPT:** Large code refactors, raw RPG Maker JSON editing, repetitive boilerplate, or any `canon_decision` work - `canon_decision` always routes to `agent.human`; GPT may draft options but never makes the final call.

## Claude Code

**Role:** Senior software architect and refactoring specialist.

**Strengths:** Tool architecture, repository structure, exporter/importer design, test design, complex refactors, long-form implementation reasoning, and design-to-code translation plans. Scores `3` on `architecture`, `risk_ceiling: high`, `context_depth: deep` - the only agent cleared for high-risk work without a mandatory human-review condition.

**Limitations:** `scarcity: high` - Claude Code is a quota-conserving resource. Scores only `2` on `implementation`, behind Codex's `3`. Not the right choice for small repetitive edits or minor copy updates when quota is limited.

**Recommended work types:** Architecture-review and schema-design work, especially anything scoped as `production_orchestration` under the Work Order Router - the pattern library, the router itself, the scheduler, graph tooling. The `WO-0010 Graph Diff Engine` and `WO-0013 Canon Linter` assignments in `agent-scheduler-design.md`'s worked examples are the reference pattern: Claude Code architects, Codex may implement under review.

**When NOT to use Claude Code:** Small repetitive edits, minor copy updates, or any task that does not require architectural judgment while quota is limited - reserve it for work that specifically needs `risk_ceiling: high` or `context_depth: deep`.

## Codex

**Role:** Implementation engineer.

**Strengths:** RPG Maker implementation, Python scripts, JavaScript plugins, JSON transformations, build automation, tests and audits, and applying already-scoped work orders to a codebase. Scores `3` on `implementation`, the highest of any agent in that class.

**Limitations:** `risk_ceiling: medium` - high-risk implementation work needs a `REVIEWED_BY agent.human` condition, or should route to Claude Code instead. Not suited to open-ended story invention without concrete constraints.

**Recommended work types:** Any `game_implementation`-classified work order once it is `pending_approval` and approved, per the Work Order Router's gating rule - Codex is the default implementing agent once an AtlasStudio implementation contract (`WO-0020` pattern) exists to execute. Also the default for `repetitive_edit`-adjacent implementation work that is too structured for Copilot alone but does not need Claude Code's architectural judgment.

**When NOT to use Codex:** Open-ended story invention without concrete constraints, and any final creative judgment - Codex implements against a contract; it does not decide what the contract should say.

## GitHub Copilot

**Role:** Local coding assistant.

**Strengths:** Autocomplete, boilerplate, small edits, in-editor implementation support, repetitive code patterns. Scores `3` on `repetitive_edit`, the highest of any agent in that class, but `context_depth: shallow` and `risk_ceiling: low`.

**Limitations:** Not suited to multi-file production planning without supervision, and irreversible work is never recommended to a `shallow`-context agent per the Agent Scheduler's Risk-Based Routing rules.

**Recommended work types:** Small, well-scoped, single-file or single-function edits inside a change another agent or a human has already architected. The natural "last mile" agent once Claude Code or Codex has set the shape of a change.

**When NOT to use Copilot:** High-level architecture, canon decisions, or multi-file production planning without supervision. Never the sole agent on anything above `risk_level: low`.

## Ollama / Local Models

**Role:** Low-cost support agent.

**Strengths:** Long-running review, draft critique, consistency checks, summaries, low-risk scaffolding, offline brainstorming. Scores `3` on `review_qa`, the highest of any agent in that class, and `scarcity: none` - the right agent to absorb work that would otherwise consume a scarcer agent's quota.

**Limitations:** `risk_ceiling: low`, `context_depth: medium`. Any work assigned above its risk ceiling requires a `REVIEWED_BY agent.human` condition per the Agent Scheduler's Risk-Based Routing rules.

**Recommended work types:** QA passes, draft critique, and consistency audits over work another agent already produced - freeing Claude Code or GPT quota for the work that actually needs their strengths. Good for offline brainstorming before a request is formal enough to file as a work order.

**When NOT to use local models:** Final canon decisions, high-risk implementation unless explicitly reviewed, or any task that genuinely requires the strongest available reasoning - `unknown`/`limited` availability status degrades further caution per the scheduler's availability filter.

## Human Creator

**Role:** Executive Producer and final creative authority.

**Owns, and no agent may substitute for:** Final approval, creative taste, scope decisions, playtest feedback, priority calls, project direction, and every `canon_decision`-classified task. Modeled explicitly as `agent.human` in the Agent Scheduler with capabilities that "cannot be delegated" per `capability-based-orchestration.md`: `final-canon`, `creative-direction`, `risk-acceptance`, `scope-approval`, `merge-approval`.

**When an AI agent should not be trusted to decide alone:** Any Accept/Reject/Defer decision (`PLAYTEST_AND_ACCEPTANCE.md`), any routing decision an agent flags as `blocked_ambiguous`, and any work touching `hand_authored` or `locked` content regardless of which agent proposes the change.

## Quick Reference

| Task class | Primary | Fallback | Never assign |
|---|---|---|---|
| `creative_design` | GPT | Ollama (draft critique, reviewed) | Codex, Copilot |
| `architecture` | Claude Code | Codex (reviewed) | GPT, Copilot |
| `implementation` | Codex | Claude Code | GPT |
| `repetitive_edit` | Copilot | Codex, Ollama | Claude Code (quota) |
| `review_qa` | Ollama | Codex, Claude Code | - |
| `canon_decision` | Human | - | Any AI agent alone |

This table restates `agent-scheduler-design.md`'s capability table at a glance; the scheduler's scored output is the authoritative source if the two ever disagree.

## Review

This document should be revisited if `studio/agent-roles.md` or `studio/scheduling/agent-scheduler-design.md` change, or if a new agent or provider is added to the roster.
