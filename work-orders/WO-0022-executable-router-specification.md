---
work_order_id: WO-0022
title: Executable Work Order Router Specification
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
  - spec.atlas_router_implementation
  - spec.atlas_router_cli
  - spec.atlas_router_test_plan
  - spec.atlas_router_error_handling
created: 2026-07-07
---

# WO-0022 - Executable Work Order Router Specification

## Purpose

`WO-0021` completed the architectural design for cross-repository routing: classification model, routing rules, target repository mapping, frontmatter/schema proposal, and safety rules. This work order converts that design into an implementation specification detailed enough that Codex can build `tools/atlas_router/` almost mechanically, without making any architectural decision of its own. This is the final design step before coding begins.

## Player-Facing Goal

Indirect. A precise, gap-free specification prevents an implementing agent from having to guess at routing behavior - a wrong guess here (an unstated default repository, an unspecified error path) is exactly the class of mistake that could reintroduce the canon-leak failure mode `WO-0018` already found and corrected once.

## Background

`work-orders/WO-0021-cross-repository-work-order-router.md`, `studio/orchestration/work-order-router.md`, and `schemas/work-order-routing.schema.json` establish what the router decides and why. They do not specify a directory layout, module boundaries, function signatures, CLI argument shapes, exit codes, or a concrete test suite - the gap this work order closes. This work order also reconciles the router with two pieces of prior design it did not originally reference in enough depth: `studio/scheduling/agent-scheduler-design.md` (WO-0012), whose deterministic agent-recommendation algorithm the router's `scheduler.py` module implements rather than reinvents, and `bridges/atlas/implementation-handoff.md` (WO-0019), whose "point, don't paraphrase" rule governs exactly how the router's `dispatcher.py` forwards canon and game-implementation requests to their owning repositories.

## Scope

### In Scope

- `IMPLEMENTATION_SPEC.md`: overall architecture, directory layout, every module's classes/functions/inputs/outputs, JSON structures, the internal routing pipeline, the module dependency graph, logging, and audit record format.
- `CLI_SPEC.md`: full specification of every `atlas` command named in this work order's brief (`wo create`, `wo classify`, `wo preview`, `wo dispatch`, `wo explain`, `doctor`, `plan`, `status`, `import`, `sync`, `validate`, `graph`, `scheduler`), including arguments, examples, exit codes, error behavior, and expected output for each.
- `ROUTING_TEST_PLAN.md`: at least 25 executable, representative test cases (input, expected classification, expected repository, expected agent) plus explicit edge cases, traceable to `work-order-router.md`'s rules.
- `ERROR_HANDLING.md`: deterministic specification for ambiguous requests, multiple matching repositories, missing authority data, unknown project, missing implementation packet, missing graph nodes, missing scheduler information, unknown agent, network failure, GitHub unavailable, and Atlas unavailable.
- A recommended Python package layout for `tools/atlas_router/`, matching the example given in this work order's brief and the conventions already established by `tools/atlas_planner/`, `tools/atlas_doctor/`, and `tools/atlas_graph/`.

### Out of Scope

- Writing any code under `tools/atlas_router/` other than the four specification documents.
- Modifying `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` in any way.
- Modifying AtlasStudio's canon.
- Redesigning any routing rule, classification category, or safety rule already established by `WO-0021` - this work order translates those rules into an implementable shape; it does not change what they say.
- Modifying `schemas/work-order-routing.schema.json` (a WO-0021 deliverable, referenced here read-only).

## Inputs

- `work-orders/WO-0018-repository-authority.md`, `work-orders/WO-0019-atlas-import-bridge.md`, `work-orders/WO-0020-ashford-village-implementation-contract-from-atlas-handoff.md`, `work-orders/WO-0021-cross-repository-work-order-router.md`.
- `studio/orchestration/work-order-router.md`, `schemas/work-order-routing.schema.json`.
- `studio/governance/repository-authority.md`.
- `studio/scheduling/agent-scheduler-design.md`, `schemas/agent-status.schema.json`, `studio/scheduling/agent-status.example.json`, `studio/agent-roles.md`.
- `bridges/atlas/implementation-handoff.md`, `bridges/atlas/import-architecture.md`, `bridges/atlas/synchronization-strategy.md`.
- `tools/atlas_planner/planner.py`, `tools/atlas_doctor/doctor.py`, `tools/atlas_graph/atlas_graph.py`, `tools/atlas_graph/query_graph.py`, `tools/atlas_format/format_guard.py` (existing code conventions this specification must match: stdlib-only, `argparse`, dataclasses, manual frontmatter parsing, `--json` flag, exit-code discipline).
- `studio/work-order-format.md` (the template `dispatcher.py` renders new work orders against).

## Deliverables

- `tools/atlas_router/IMPLEMENTATION_SPEC.md`
- `tools/atlas_router/CLI_SPEC.md`
- `tools/atlas_router/ROUTING_TEST_PLAN.md`
- `tools/atlas_router/ERROR_HANDLING.md`
- `work-orders/WO-0022-executable-router-specification.md`

## Acceptance Criteria

- `IMPLEMENTATION_SPEC.md` names every module (`models.py`, `parser.py`, `classifier.py`, `authority.py`, `scheduler.py`, `dispatcher.py`, `github.py`, `audit.py`, `cli.py`), its functions and their signatures, the exact JSON shapes it produces or consumes, the dependency graph between modules, and the audit-log file paths and append-only discipline.
- `CLI_SPEC.md` specifies every named command's arguments, at least one example invocation, its exit codes drawn from one shared table, its error behavior, and its expected output shape.
- `ROUTING_TEST_PLAN.md` contains at least 25 representative test cases plus explicitly labeled edge cases, and at least one case directly testing that canon can never be forced into AtlasStudio by a self-declared override.
- `ERROR_HANDLING.md` covers all eleven named error categories with a deterministic, specified behavior for each, distinguishing non-fatal warnings from blocking states explicitly.
- The recommended package layout matches the brief's example and is consistent with existing `tools/atlas_*` conventions (stdlib-only, no new third-party dependency).
- No routing rule, classification category, or safety rule from `WO-0021` is redefined - every behavior specified here is traceable to an existing rule.
- No code is written. No sibling repository is modified. No AtlasStudio canon file is modified. `schemas/work-order-routing.schema.json` is not modified.

## Verification Steps

```bash
find tools/atlas_router -maxdepth 1 -name "*.md"
find work-orders -name "WO-0022-executable-router-specification.md"
find tools/atlas_router -name "*.py"
# expect no output: this work order is documentation only
python3 tools/atlas_format/format_guard.py --check
git -C ../TheLastSwordProtocol-Atlas status --porcelain
git -C ../TheLastSwordProtocol-Game status --porcelain
```

## Allowed Changes

- `tools/atlas_router/IMPLEMENTATION_SPEC.md`
- `tools/atlas_router/CLI_SPEC.md`
- `tools/atlas_router/ROUTING_TEST_PLAN.md`
- `tools/atlas_router/ERROR_HANDLING.md`
- `work-orders/WO-0022-executable-router-specification.md`

## Protected Areas

- Do not modify `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game`.
- Do not modify AtlasStudio's canon.
- Do not modify `schemas/work-order-routing.schema.json` or `studio/orchestration/work-order-router.md` - reference them, do not restate or alter their rules.
- Do not redesign the routing rules established by `WO-0021`.
- Do not write any `.py` file under `tools/atlas_router/` - this is a specification-only work order.
- Preserve the Immutable Formatting Rule.

## Notes for Assigned Agent

The success criterion given for this work order is that Codex should be able to implement the router "almost mechanically without making significant architectural decisions." Treat every ambiguity found while writing these documents as a signal to make an explicit, stated decision here rather than leaving it for the implementing agent to improvise - in particular, the gap between the router's five classification categories and the Agent Scheduler's six task classes (`WO-0012`) needed an explicit mapping table, and the fact that `TheLastSwordProtocol-Atlas` and `TheLastSwordProtocol-Game` are real GitHub-hosted repositories (confirmed by checking their `origin` remotes) rather than abstract concepts meant "dispatch" needed a concrete, safe mechanism - a `github.py` module limited to opening issues via the `gh` CLI, never a direct write - instead of being left undefined.

## Submission Record

Submitted 2026-07-07 by Claude Code.

Delivered:

- `tools/atlas_router/IMPLEMENTATION_SPEC.md` - full architecture: a five-stage pipeline (parse -> classify -> authority -> schedule -> dispatch), a nine-file module layout with per-module function signatures and dataclasses in `models.py` mirroring `schemas/work-order-routing.schema.json` field-for-field, a dependency graph explaining why `cli.py` shells out to existing tools via subprocess rather than importing them in-process, and an append-only JSON Lines audit log design under `reports/atlas-router/`.
- `tools/atlas_router/CLI_SPEC.md` - every command from the brief specified: `atlas wo create/classify/preview/dispatch/explain` fully (arguments, examples, exit codes, output shape) plus `doctor`, `plan`, `graph`, `validate`, and `scheduler recommend` as passthroughs or in-process implementations, and `status`/`import`/`sync` as explicitly stubbed, not-yet-implemented commands pointing at their WO-0019 design documents. One shared 8-value exit code table (0 through 7) used by every command.
- `tools/atlas_router/ROUTING_TEST_PLAN.md` - 30 test cases (6 canon, 6 game_implementation, 6 production_orchestration, 4 cross_repository_bridge, 8 ambiguous/edge cases), each with input, matched signals, expected classification, repository, task class, agent, and routing status, plus a coverage checklist and an explicit release-blocking case (case 30) proving canon cannot be forced into AtlasStudio via a self-declared frontmatter override.
- `tools/atlas_router/ERROR_HANDLING.md` - all eleven requested error categories specified deterministically, with an explicit cross-cutting rule set distinguishing non-fatal warnings from blocking states, and a stated fail-closed rule for missing authority data.
- This work order, marked `submitted`.

No file was written under `tools/atlas_router/` other than the four specification documents listed above - confirmed directly; no `.py` file exists in that directory. No file in `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` was modified. No AtlasStudio canon file was modified. `schemas/work-order-routing.schema.json` and `studio/orchestration/work-order-router.md` were read and referenced, not edited. No routing rule from `WO-0021` was redefined - every specified behavior traces to an existing rule in that document or in `studio/scheduling/agent-scheduler-design.md`.

Formatting: preserved existing house style; no existing file was reformatted.

Verification performed:

```bash
find tools/atlas_router -maxdepth 1 -name "*.md"
find work-orders -name "WO-0022-executable-router-specification.md"
find tools/atlas_router -name "*.py"
python3 tools/atlas_format/format_guard.py --check
git -C ../TheLastSwordProtocol-Atlas status --porcelain
git -C ../TheLastSwordProtocol-Game status --porcelain
```
