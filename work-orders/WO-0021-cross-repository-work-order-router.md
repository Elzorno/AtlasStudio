---
work_order_id: WO-0021
title: Cross-Repository Work Order Router
status: submitted
project: atlasstudio
recommended_agent: claude-code
agent_role: senior-software-architect
risk_level: medium
player_facing: false
engine_specific: false
required_capabilities:
  - architecture-review
  - schema-design
  - documentation
preferred_capabilities:
  - qa-review
produces:
  - orchestration.work_order_router
  - schema.work_order_routing
created: 2026-07-07
---

# WO-0021 - Cross-Repository Work Order Router

## Purpose

Design a routing system that lets a human or agent create a single work order request and have AtlasStudio determine which of the three active repositories - `TheLastSwordProtocol-Atlas`, `TheLastSwordProtocol-Game`, or AtlasStudio itself - owns it, without guessing, without writing into a sibling repository, and without ever repeating the exact conflict `WO-0018` had to unwind (canon drafted inside AtlasStudio by an author who did not know a more authoritative version already existed elsewhere).

## Player-Facing Goal

Indirect. Correct routing prevents wasted or conflicting work (a quest drafted twice under different canon, a map edited outside its ownership ledger), which protects the player-facing content that is already real and hand-authored from being duplicated, contradicted, or silently overwritten.

## Background

`work-orders/WO-0018-repository-authority.md` and `studio/governance/repository-authority.md` established permanent ownership boundaries and a change-flow model across the three active repositories, after finding that AtlasStudio had built conflicting canon and production plans without knowing a more mature parallel system already existed. `work-orders/WO-0019-atlas-import-bridge.md` then designed how AtlasStudio imports and understands Atlas's authoritative state without becoming a competing source of truth. Neither work order, however, defines how a *new* work order request - not yet filed anywhere - gets pointed at the correct repository in the first place. This work order closes that gap: it is the front door those two prior work orders assumed existed.

## Scope

### In Scope

- Routing rules mapping request types to owning repository, grounded in `repository-authority.md`'s existing ownership boundaries.
- A work order classification model (signal-based, deterministic, explainable) covering canon, game implementation, production/orchestration, cross-repository bridge, and ambiguous/unresolved requests.
- A target repository / path mapping table.
- A frontmatter extension proposal for `studio/work-order-format.md`, additive and backward-compatible with every existing work order.
- A standalone JSON Schema for a routing decision record, independent of the frontmatter proposal.
- Safety rules preventing silent canon migration into AtlasStudio, ungated direct writes to `TheLastSwordProtocol-Game`, and silent guessing on ambiguous requests.
- Worked examples covering canon, game implementation, orchestration, bridge, and ambiguous cases.
- An implementation plan naming the future Codex-implemented tool (`tools/atlas_router/router.py`) by responsibility, not implementing it.

### Out of Scope

- Implementing the router tool itself.
- Modifying `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` in any way.
- Modifying AtlasStudio's own canon or redefining any ownership boundary already set by `repository-authority.md`.
- Granting any agent or tool new write access to a sibling repository.
- Establishing an actual approval workflow UI or automated dispatch - approval remains a manual, recorded human step.

## Inputs

- `work-orders/WO-0018-repository-authority.md`, `studio/governance/repository-authority.md`.
- `work-orders/WO-0019-atlas-import-bridge.md`, `bridges/atlas/implementation-handoff.md` (existing "point, don't paraphrase" and per-provider routing precedent).
- `work-orders/WO-0020-ashford-village-implementation-contract-from-atlas-handoff.md` (existing pattern for gated, approval-required implementation contracts).
- `work-orders/WO-0011-work-order-planner.md` (existing precedent for a design work order later implemented by Codex as a deterministic tool).
- `studio/orchestration/capability-based-orchestration.md` (existing "recommends, does not dispatch" design rule, reused here).
- `studio/work-order-format.md` (existing frontmatter this work order proposes extending).
- `schemas/agent-status.schema.json` (existing schema style this work order's schema follows).

## Deliverables

- `studio/orchestration/work-order-router.md`
- `schemas/work-order-routing.schema.json`
- `work-orders/WO-0021-cross-repository-work-order-router.md`

## Acceptance Criteria

- Routing rules explicitly state: canon work goes to `TheLastSwordProtocol-Atlas`; production/orchestration work goes to AtlasStudio; game implementation work goes to `TheLastSwordProtocol-Game` only with explicit approval; ambiguous work orders stop and request classification.
- The classification model is signal-based and explainable - every classification traces to specific matched signals, not to an unexplained judgment call.
- The router design never allows canon to be silently filed, drafted, or migrated into AtlasStudio, and never allows a direct, unapproved write into `TheLastSwordProtocol-Game`.
- The frontmatter proposal is additive: every existing work order in this repository remains valid without modification under a stated default.
- `schemas/work-order-routing.schema.json` is valid JSON Schema (2020-12), matches the style of `schemas/agent-status.schema.json`, and models classification, target repository, routing status, approval fields, and rationale.
- At least five worked examples are given, covering canon, game implementation, orchestration, bridge, and ambiguous cases.
- An implementation plan names the future tool, its CLI shape, its integration points, and its explicit non-goals, without implementing it.
- No sibling repository is modified. No AtlasStudio canon file is modified. No existing document is overwritten.

## Verification Steps

```bash
find studio/orchestration -name "work-order-router.md"
find schemas -name "work-order-routing.schema.json"
find work-orders -name "WO-0021-cross-repository-work-order-router.md"
python3 -c "import json; json.load(open('schemas/work-order-routing.schema.json')); print('valid json')"
python3 tools/atlas_format/format_guard.py --check
git -C ../TheLastSwordProtocol-Atlas status --porcelain
git -C ../TheLastSwordProtocol-Game status --porcelain
# expect no changes attributable to this work order in either sibling repository
```

## Allowed Changes

- `studio/orchestration/work-order-router.md`
- `schemas/work-order-routing.schema.json`
- `work-orders/WO-0021-cross-repository-work-order-router.md`

## Protected Areas

- Do not modify `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game`.
- Do not modify AtlasStudio's story canon or any existing canon graph file.
- Do not redefine any ownership boundary already established in `studio/governance/repository-authority.md` - operationalize it, don't replace it.
- Do not overwrite any existing document.
- Preserve the Immutable Formatting Rule.

## Notes for Assigned Agent

This is a design and schema work order, matching the shape of `WO-0011`, `WO-0018`, and `WO-0019`: it defines rules, a classification model, and a schema, and explicitly hands off implementation to a future Codex-scoped work order rather than building the tool now. The single hardest constraint is the one already stated by the user directly: the router must never silently move canon into AtlasStudio. Every rule and safety section should be checked against that constraint specifically, since it is the exact failure mode `WO-0018` already found and corrected once.

## Submission Record

Submitted 2026-07-07 by Claude Code.

Delivered:

- `studio/orchestration/work-order-router.md` - a five-category classification model (`canon`, `game_implementation`, `production_orchestration`, `cross_repository_bridge`, `ambiguous`) with a signal table for how each is detected, five routing rules matching the user's exact wording, a target repository/path mapping table, an additive frontmatter proposal (`classification`, `target_repository`, `routing_status`, `requires_explicit_approval`) with a stated backward-compatible default for every pre-existing work order, seven safety rules (including the explicit no-silent-canon-leak rule and preservation of `WO-0018` authority), six worked examples, and an implementation plan for a future `tools/atlas_router/router.py` naming its CLI shape, integration points, correction-logging approach, and explicit non-goals.
- `schemas/work-order-routing.schema.json` - a standalone JSON Schema (2020-12, `additionalProperties: false`, following `schemas/agent-status.schema.json`'s style) for the router's own audit record: classification, target repository, routing status, approval fields, matched signals, safety flags, and rationale.
- This work order, marked `submitted`.

No file in `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` was modified - confirmed directly; the pre-existing modified/untracked files present in `TheLastSwordProtocol-Game`'s working tree (`data/Map001.json`, `data/Map002.json`, `data/System.json`, `map_ownership.json`, `img/tilesets/readme_en.pdf`) predate this work order and were not touched by it. No AtlasStudio canon file was modified. No existing document was overwritten. No ownership boundary from `studio/governance/repository-authority.md` was redefined - this document only operationalizes it.

Formatting: preserved existing house style; no existing file was reformatted.

Verification performed:

```bash
find studio/orchestration -name "work-order-router.md"
find schemas -name "work-order-routing.schema.json"
find work-orders -name "WO-0021-cross-repository-work-order-router.md"
python3 -c "import json; json.load(open('schemas/work-order-routing.schema.json')); print('valid json')"
python3 tools/atlas_format/format_guard.py --check
git -C ../TheLastSwordProtocol-Atlas status --porcelain
git -C ../TheLastSwordProtocol-Game status --porcelain
```
