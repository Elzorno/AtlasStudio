---
work_order_id: WO-0031
title: Implement AtlasStudio Unified CLI
status: submitted
project: atlasstudio
recommended_agent: codex
agent_role: implementation-engineer
risk_level: medium
player_facing: false
engine_specific: false
required_capabilities:
  - python
  - cli
  - architecture-review
created: 2026-07-08
---

# WO-0031 - Implement AtlasStudio Unified CLI

## Purpose

Implement the unified `atlas` command from the WO-0030 interface specification, using the existing AtlasStudio tools wherever possible instead of duplicating their domain logic.

## Player-Facing Goal

Indirect. This work order changes AtlasStudio operations, not game content. Its value is reducing friction in the daily production loop so implementation work can move from request to validation with fewer manual command choices.

## Background

Reference:

- `studio/interface/ATLAS_CLI_SPEC.md`
- `studio/interface/COMMAND_REFERENCE.md`
- `studio/interface/INTERACTIVE_SHELL.md`
- `studio/interface/USER_EXPERIENCE.md`
- `reports/interface/daily-cli-walkthrough.md`
- `work-orders/WO-0030-atlasstudio-interactive-cli.md`

WO-0030 specified the unified CLI as an implementation-ready interface. This work order builds the first version in `tools/atlas_cli/` without changing the existing command tools it wraps.

## Scope

### In Scope

- Add `tools/atlas_cli/` as the unified command package.
- Implement first-version commands: `today`, `status`, `doctor`, `route`, `validate`, `planner`, `graph`, `work`, `review`, and `history`.
- Add a practical no-argument interactive shell via `python3 -m tools.atlas_cli.cli`.
- Reuse existing AtlasStudio command tools and router modules.
- Add focused unit tests for wrapper routing behavior.

### Out of Scope

- Redesigning the WO-0030 interface.
- Modifying sibling repositories.
- Modifying canon.
- Modifying implementation contracts.
- Modifying existing AtlasStudio tool behavior.
- Adding non-stdlib dependencies.

## Inputs

- `tools/atlas_doctor/doctor.py`
- `tools/atlas_router/cli.py`
- `tools/atlas_router/`
- `tools/atlas_planner/planner.py`
- `tools/atlas_graph/query_graph.py`
- `tools/atlas_graph/validate_graph.py`
- `tools/atlas_format/format_guard.py`
- `studio/immutable-formatting-rule.md`

## Deliverables

- `tools/atlas_cli/__init__.py`
- `tools/atlas_cli/cli.py`
- `tools/atlas_cli/README.md`
- `tools/atlas_cli/tests/__init__.py`
- `tools/atlas_cli/tests/test_cli.py`
- `work-orders/WO-0031-implement-atlasstudio-unified-cli.md`

## Acceptance Criteria

- `python3 -m tools.atlas_cli.cli --help` prints the unified CLI help.
- `python3 -m tools.atlas_cli.cli status` prints a Studio Health snapshot.
- `python3 -m tools.atlas_cli.cli today` prints a start-of-day snapshot.
- `python3 -m tools.atlas_cli.cli doctor` forwards to the Studio Doctor.
- `python3 -m tools.atlas_cli.cli route preview "Build Ashford Inn"` routes through the existing router logic.
- `python3 -m tools.atlas_cli.cli validate` runs graph validation and the format guard.
- `python3 -m tools.atlas_cli.cli planner` forwards to the Planning Engine.
- `python3 -m tools.atlas_cli.cli graph validate` runs Atlas Graph validation.
- `python3 -m tools.atlas_cli.cli work` exposes work-order lifecycle helpers.
- `python3 -m tools.atlas_cli.cli review` exposes day-level and work-order review.
- `python3 -m tools.atlas_cli.cli history` reads routing, work-order, and decision history.
- `python3 -m unittest discover -s tools/atlas_cli/tests -v` passes.
- Existing tools under `tools/atlas_doctor`, `tools/atlas_router`, `tools/atlas_planner`, `tools/atlas_graph`, `tools/atlas_format`, and `tools/atlas_lint` are not modified.
- No sibling repository is modified.
- No canon file is modified.
- The Immutable Formatting Rule is preserved.
- This work order is marked `submitted`.

## Verification Steps

```bash
python3 -m tools.atlas_cli.cli --help
python3 -m tools.atlas_cli.cli status
python3 -m tools.atlas_cli.cli today
python3 -m tools.atlas_cli.cli doctor
python3 -m tools.atlas_cli.cli route preview "Build Ashford Inn"
python3 -m tools.atlas_cli.cli validate
python3 -m tools.atlas_cli.cli planner
python3 -m tools.atlas_cli.cli graph validate
python3 -m unittest discover -s tools/atlas_cli/tests -v
python3 tools/atlas_graph/validate_graph.py
python3 tools/atlas_format/format_guard.py --check
python3 tools/atlas_doctor/doctor.py
```

## Allowed Changes

- `tools/atlas_cli/`
- `work-orders/WO-0031-implement-atlasstudio-unified-cli.md`

## Protected Areas

- Do not modify `TheLastSwordProtocol-Atlas`.
- Do not modify `TheLastSwordProtocol-Game`.
- Do not modify Atlas canon.
- Do not modify implementation contracts.
- Do not modify existing design patterns.
- Do not modify implementation contracts.
- Preserve the Immutable Formatting Rule.

## Notes for Assigned Agent

Keep this implementation as a thin shell over the existing tools. The existing router, doctor, planner, graph, and format commands remain authoritative for their domains.

## Submission Record

Submitted 2026-07-08 by Codex.

Delivered:

- `tools/atlas_cli/__init__.py` - package marker for the unified CLI.
- `tools/atlas_cli/cli.py` - stdlib-only dispatcher implementing `today`, `status`, `doctor`, `route`, `validate`, `planner`/`plan`, `graph`, `work`, `review`, `history`, `dispatch`, and the no-argument interactive shell.
- `tools/atlas_cli/README.md` - usage notes and command summary.
- `tools/atlas_cli/tests/` - focused unit coverage for route preview, graph validation routing, validate sequencing, and work-order reads.
- This work order, marked `submitted`.

Formatting: preserved existing house style; no broad reformatting performed.

