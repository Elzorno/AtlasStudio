# Atlas Core 1.0

## Status

**Atlas Core 1.0 - Stable.**

This document is the engineering constitution of AtlasStudio: the philosophy, architecture, and governance that every future human contributor and AI agent operates under. It is not marketing copy and it is not a user guide. It exists to keep a multi-agent, multi-provider studio coherent as it grows.

Where this document summarizes, `studio/governance/atlas-principles.md` goes deeper, and `studio/governance/architectural-decision-log.md` records the specific decisions that produced the architecture described below.

## 1. Vision

AtlasStudio exists to coordinate human creators and specialized AI agents so they can build complete, playable games without losing canon, context, ownership, or production direction.

Atlas v1 proved that structure helps - work orders, canon documents, and validation gave multi-agent work a shared frame. But Atlas v1 drifted toward producing documents *about* a game rather than the game itself. AtlasStudio exists to correct that: the center of gravity moves from screens to worlds, from documents to playable builds, from single-agent execution to coordinated multi-agent production, and from static checklists to work orders with real acceptance tests.

Atlas Core is the reusable studio platform underneath that mission. The Last Sword Protocol is its first project, not its only intended one.

## 2. Core Philosophy

These are load-bearing beliefs. Any work order, tool, or process that contradicts one of these should be treated as a design smell, not a shortcut.

- **Planning should be explainable.** Every recommendation - what to build next, who should build it - must show its evidence and its score, not just its conclusion.
- **Deterministic systems before opaque AI.** Where a rule-driven script can validate, diff, lint, or plan, prefer it over an LLM judgment call. Opaque reasoning is reserved for creative work, not for QA gates.
- **Human approval for canon.** No agent silently changes what is true about the world. Canon moves only through explicit review.
- **Capabilities outlive providers.** Work orders should describe what a task requires, not which vendor must do it. Providers are swappable; the capability model is not.
- **Every asset has an owner.** Generated, agent-drafted, human-edited, hand-authored, and locked content are different states with different rules, especially at the engine bridge boundary.
- **Every change has provenance.** Nodes, edges, and work orders carry `source` references back to the document or file that justifies them. Nothing floats free of its evidence.
- **Preserve meaningful diffs.** Reformatting is not a substitute for review, and it must never be mixed with a semantic change in the same diff.
- **Atlas proposes. Humans approve.** Tooling recommends, scores, and flags. It does not dispatch, merge, or promote canon on its own authority.

See `studio/governance/atlas-principles.md` for the full rationale behind each belief and how they interact when they pull in different directions.

## 3. Atlas Core Architecture

Atlas Core is organized as a loop, not a pipeline. Each component reads and writes the same shared state - the Atlas Graph - so any agent picking up work mid-loop has the full context.

```text
Human Intent
  |
  v
Planning Engine  <---------------------------+
  | recommends next work (evidence-scored)   |
  v                                          |
Work Order (capability-tagged)               |
  |                                          |
  v                                          |
Capability-Based Orchestration                |
  | required capabilities -> registry ->      |
  | provider registry -> provider status ->   |
  | primary + fallback recommendation         |
  v                                          |
Human Approval                               |
  |                                          |
  v                                          |
Agent Executes                               |
  |                                          |
  v                                          |
Atlas Graph updated (canon / production / bridge)
  |
  +--> Validator        (structural integrity: required fields, unique ids, resolvable edges)
  +--> Immutable Formatting Guard  (flags formatting-only churn vs. semantic change)
  +--> Canon Linter      (deterministic design QA over canon coherence, if canon touched)
  +--> Graph Diff Engine (readable before/after report for review and agent handoff)
  +--> Bridge Layer      (engine-specific translation, if implementation-facing)
  |
  v
Studio Doctor  (aggregate health: graph integrity, orphans, missing sources, work order status, readiness)
  |
  v
Human Review --> Accept / Revise --> back to Planning Engine
  |
  v
Architectural Decision Log (if the change was itself architectural)
```

### Planning Engine

Recommends what to build next from graph state, work order metadata, Studio Doctor signals, and Canon Linter findings. Scores are transparent components (milestone impact, dependency value, technical debt, player value, core platform value) plus evidence. It never creates work orders on its own.

### Capability-Based Orchestration

Answers *who* should do recommended work, without hardcoding agent names. A work order (or its inferred profile) declares required and preferred capabilities; the Capability Registry (`atlas-core/capabilities/`) defines what those capabilities mean; the Provider Registry (`atlas-core/providers/`) defines who can supply them; manual Provider Status (`atlas-core/orchestration/provider-status.example.json`) supplies availability, quota, and cost signals. The output is a primary and fallback assignment with an explanation, always subject to human approval. The human is modeled as a provider for capabilities that cannot be delegated: final canon authority, creative direction, risk acceptance, and scope approval. This replaced an earlier named-agent Agent Scheduler design; see ADR-0007 in the decision log.

### Graph

The shared memory layer (`projects/<project>/graph/`). Canon, production, and bridge facts are stored as Git-native JSON so relationships between world canon, production work, agents, providers, and engine bridges are explicit rather than re-inferred from prose on every agent session. Markdown remains the home for narrative, rationale, and tone; the graph is the home for entities, relationships, dependencies, and queryable facts.

### Doctor

`tools/atlas_doctor/` aggregates project health into one readable report: graph integrity, orphan nodes, missing sources, work order status, implementation readiness, and registered tools. It is the first thing to run before trusting any other signal.

### Validator

`tools/atlas_graph/validate_graph.py` checks structural integrity: parseable JSON, required fields present, unique node and edge ids, edges that resolve to real nodes, and source paths that exist on disk. This is the deterministic floor every graph change must clear.

### Canon Linter

`tools/atlas_lint/` runs deterministic, rule-driven design QA over canon coherence - structure, completeness, consistency, coverage, production linkage, and bridge readiness - without ever modifying canon. Rules live in `tools/atlas_lint/rules/canon_lint_rules.json` so the rule set itself is reviewable, not hidden in code.

### Graph Diff Engine

`tools/atlas_graph/diff_graph.py` compares two graph states (refs, commits, or directories) and reports added, removed, and changed facts, grouped by canon/production/bridge scope, with status changes, scope moves, and source reference changes highlighted. This is the mechanism that makes a work order's graph impact reviewable by a human or the next agent in one pass.

### Immutable Formatting Guard

`tools/atlas_format/format_guard.py` is check-only: it detects formatting-only churn versus semantic change and warns when broad, non-semantic reformatting would obscure a real diff. It enforces the Immutable Formatting Rule (`studio/immutable-formatting-rule.md`) without ever rewriting a file itself.

### Bridge Layer

`bridges/<engine>/` and its supporting tools (for example `tools/rpg_maker_bridge/`) translate engine-independent design into engine-specific implementation work, without leaking engine IDs, map data, or event structures back into core canon. The bridge owns the ownership model (generated / agent-drafted / human-edited / hand-authored / locked) that protects hand-authored work from being silently overwritten, and produces read-only handoff checklists for implementation agents rather than writing directly into a game repository.

## 4. Governance

Atlas Core and Projects are deliberately separate layers:

```text
Atlas Core        - reusable studio platform: graph tooling, work order lifecycle,
                    capability/provider model, diagnostics, QA intelligence,
                    engine bridge framework.
Projects          - individual games: their canon, their graph facts, their
                    engine mappings, their playtest goals.
```

**Rule of thumb:** if a feature would be useful to more than one project, it belongs in Atlas Core. If it is specific to The Last Sword Protocol (or any single project), it belongs under `projects/<project-id>/`.

Full governance detail - what triggers an Atlas Core change, what requires an ADR, how project-specific work escalates to a core capability - lives in `studio/governance/atlas-principles.md`.

## 5. Architectural Decision Records

Atlas Core's architecture is not assumed to be final. It is expected to change, deliberately and traceably.

- New architectural decisions use `studio/governance/decision-record-template.md`.
- Accepted decisions are appended to `studio/governance/architectural-decision-log.md`, numbered sequentially, never renumbered or deleted - superseded decisions are marked superseded, not erased.
- A decision is architectural (and needs an ADR) if it changes a schema, a governance boundary, a QA gate's behavior, or how agents/providers are assigned work. A decision that only adds project content, a new canon fact, or a new work order does not need one.

## 6. Version

**Atlas Core 1.0 - Stable**, declared 2026-07-07.

Stable means: the graph node/edge shape, work order frontmatter contract, capability/provider registry shape, and the QA tool chain (Validator, Canon Linter, Graph Diff, Formatting Guard, Doctor) are considered load-bearing. Breaking changes to any of them require an ADR and a version bump of this document. Additive changes - new node types, new capabilities, new tools that read but do not alter this contract - do not require a version bump, only a decision log entry if they are architectural.
