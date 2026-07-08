---
work_order_id: WO-0023
title: Executable Work Order Router
status: submitted
project: atlasstudio
recommended_agent: codex
agent_role: implementation-engineer
risk_level: medium
player_facing: false
engine_specific: false
required_capabilities:
  - implementation
  - testing
  - architecture-review
preferred_capabilities:
  - qa-review
produces:
  - tool.atlas_router
created: 2026-07-07
---

# WO-0023 - Executable Work Order Router

## Purpose

Implement the executable Work Order Router from the `WO-0022` specification, translating the approved classification, authority, scheduling, dispatch-safety, and audit-log rules into a stdlib-only Python package under `tools/atlas_router/`.

## Player-Facing Goal

Indirect. Safer routing prevents canon, implementation, and orchestration requests from drifting into the wrong repository, protecting player-facing production work from duplicated canon decisions or unsafe implementation shortcuts.

## Background

`WO-0021` defined the router's repository authority model and `WO-0022` converted it into an implementation-ready specification. This work order builds the specified executable package without modifying sibling repositories, AtlasStudio canon, or the routing schema.

## Scope

### In Scope

- Implement `tools/atlas_router/` as a stdlib-only Python package.
- Implement classify, preview, explain, audit logging, scheduler recommendation, and safe dispatch boundaries.
- Add automated tests for the practical WO-0022 routing test plan cases.
- Preserve direct-text CLI usage for the verification commands.

### Out of Scope

- Modifying `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game`.
- Modifying canon.
- Changing `schemas/work-order-routing.schema.json`.
- Writing directly to sibling repositories under any dispatch path.

## Inputs

- `tools/atlas_router/IMPLEMENTATION_SPEC.md`
- `tools/atlas_router/CLI_SPEC.md`
- `tools/atlas_router/ROUTING_TEST_PLAN.md`
- `tools/atlas_router/ERROR_HANDLING.md`
- `studio/orchestration/work-order-router.md`
- `schemas/work-order-routing.schema.json`

## Deliverables

- `tools/atlas_router/__init__.py`
- `tools/atlas_router/models.py`
- `tools/atlas_router/parser.py`
- `tools/atlas_router/classifier.py`
- `tools/atlas_router/authority.py`
- `tools/atlas_router/scheduler.py`
- `tools/atlas_router/dispatcher.py`
- `tools/atlas_router/github.py`
- `tools/atlas_router/audit.py`
- `tools/atlas_router/cli.py`
- `tools/atlas_router/tests/`

## Acceptance Criteria

- `classify`, `preview`, and `explain` run from the CLI.
- Audit logging appends routing decisions to `reports/atlas-router/routing-log.jsonl`.
- Ambiguous requests fail closed with `target_repository: none`.
- Canon requests never route to AtlasStudio, including attempted frontmatter overrides.
- Dispatch never writes to sibling repositories and can only preview or open GitHub issues through the approved `gh issue create` mechanism.
- Automated tests cover the practical routing, authority, scheduler, parser, audit, and CLI behavior from the WO-0022 test plan.

## Verification Steps

```bash
python3 -m tools.atlas_router.cli classify "Write shopkeeper dialogue"
python3 -m tools.atlas_router.cli preview "Implement IMP-HOM-019"
python3 -m tools.atlas_router.cli explain "Create a graph diff tool"
python3 -m unittest discover -s tools/atlas_router/tests -v
python3 tools/atlas_graph/validate_graph.py
python3 tools/atlas_format/format_guard.py --check
python3 tools/atlas_doctor/doctor.py
```

## Allowed Changes

- `tools/atlas_router/`
- `reports/atlas-router/`
- `work-orders/WO-0023-executable-work-order-router.md`

## Protected Areas

- Do not modify `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game`.
- Do not modify canon.
- Do not modify `schemas/work-order-routing.schema.json`.
- Preserve the Immutable Formatting Rule.

## Notes for Assigned Agent

Prefer fail-closed behavior whenever a request cannot be classified cleanly. The router may recommend and record, but it must not quietly become a write channel into Atlas or Game.

## Submission Record

Submitted 2026-07-07 by Codex.

Delivered:

- A complete `tools/atlas_router/` package with parser, classifier, authority, scheduler, dispatcher, GitHub issue adapter, audit logging, data models, and CLI entrypoint.
- Top-level `classify`, `preview`, and `explain` aliases for the requested verification commands, alongside the specified `wo` subcommands.
- Append-only audit logging under `reports/atlas-router/routing-log.jsonl`.
- Safe dispatch behavior: local AtlasStudio writes are restricted to local work-order creation paths, sibling repository dispatch is limited to GitHub issue creation, and blocked or pending requests do not write to sibling repositories.
- Automated stdlib `unittest` coverage for practical WO-0022 routing-plan cases, including canon override rejection, conflicting signals, missing implementation packet approval blocking, parser list handling, audit append/read, scheduler recommendations, and CLI aliases.

No file in `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` was modified. No AtlasStudio canon file was modified. `schemas/work-order-routing.schema.json` was read and preserved unchanged.

Verification performed:

```bash
python3 -m tools.atlas_router.cli classify "Write shopkeeper dialogue"
python3 -m tools.atlas_router.cli preview "Implement IMP-HOM-019"
python3 -m tools.atlas_router.cli explain "Create a graph diff tool"
python3 -m unittest discover -s tools/atlas_router/tests -v
python3 tools/atlas_graph/validate_graph.py
python3 tools/atlas_format/format_guard.py --check
python3 tools/atlas_doctor/doctor.py
git -C ../TheLastSwordProtocol-Atlas status --porcelain
git -C ../TheLastSwordProtocol-Game status --porcelain
```

## Follow-up Fix: Implementation Packet Verb Routing

Submitted 2026-07-08 by Codex.

Issue fixed:

- Requests such as `Build Ashford Shop from IMP-HOM-019` referenced a valid Atlas implementation packet but did not match the original narrow `implement IMP-*` classifier pattern, so they failed closed as ambiguous.

Delivered:

- Expanded `tools/atlas_router/classifier.py` so an `IMP-<AREA>-<NNN>` implementation packet plus implementation verbs (`build`, `implement`, `create`, `apply`, `wire`, `update`, `add`, `modify`) or implementation nouns (`shop`, `map`, `event`, `NPC placement`, `transfer`, `tileset`, `route`) classifies as `game_implementation`.
- Preserved stronger canon and AtlasStudio tooling contexts so canon authoring and router/tooling work do not get pulled into implementation routing by a packet reference alone.
- Added regression coverage for:
  - `Build Ashford Shop from IMP-HOM-019`
  - `Create Ashford Shop from IMP-HOM-019`
  - `Add Shopkeeper event from IMP-HOM-019`
  - `Wire transfers for IMP-HOM-019`
  - Canon phrase guardrail: `Write shopkeeper dialogue`
  - AtlasStudio tooling phrase guardrail: `Create a graph diff tool`
  - Fail-closed guardrail: `Fix the village`

No sibling repository was modified. No canon file was modified.
