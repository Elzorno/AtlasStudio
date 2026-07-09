---
work_order_id: WO-2009
title: Atlas Academy CLI
status: accepted
priority: medium
phase: Atlas Academy
recommended_agent: codex
risk_level: medium
player_facing: false
---

# WO-2009 - Atlas Academy CLI

## Objective

Extend AtlasStudio with an Academy interface.

Implement the `atlas academy` command group as a first-class subsystem of the unified AtlasStudio CLI.

## Commands

Implement or specify stubs for:

- `atlas academy list`
- `atlas academy study`
- `atlas academy report`
- `atlas academy grade`
- `atlas academy references`
- `atlas academy help`

## Deliverables

Create:

- `tools/atlas_academy/README.md`
- `tools/atlas_academy/` CLI implementation
- `tools/atlas_academy/tests/`
- `work-orders/WO-2009-atlas-academy-cli.md`

## Constraints

Reuse the existing AtlasStudio CLI architecture.

Do not modify Atlas.

Do not modify TheLastSwordProtocol-Game.

Do not edit maps.

Do not create analysis content automatically unless explicitly requested by the command.

Preserve Immutable Formatting Rule.

## Success Criteria

Atlas Academy becomes a first-class subsystem inside AtlasStudio and can be reached through the unified CLI.

---

## Submission Record

Submitted 2026-07-08 by Claude Code.

Unlike the rest of this WO-20xx series, this work order required real implementation (its own Objective and Deliverables list a CLI implementation and a tests directory, not documentation), so - departing from this series' otherwise documentation/schema-only pattern - actual code was written here, in Python's standard library only, matching `tools/atlas_cli`'s existing implementation constraint. `recommended_agent` on this work order names `codex`; it was completed by Claude Code instead because the user asked for the remaining `WO-20xx` series to be completed in sequence, and `recommended_agent` is an advisory routing hint rather than a hard assignment (per `tools/atlas_router/scheduler.py`'s existing "recommend, never dispatch" principle, already the standing rule for this project's own Work Order Router).

Delivered:

- `tools/atlas_academy/README.md` - documents all six commands, usage, exit-code convention, and the read-only design constraint.
- `tools/atlas_academy/cli.py` - implements all six named commands (`list`, `study`, `report`, `grade`, `references`, `help`) as read-only lookups over existing `academy/`, `reports/academy/`, and (if it ever exists) `academy/grades/` content. No command creates, edits, or generates any file - `list`/`study`/`report`/`references` read and summarize; `grade` reports honestly that no grade has been filed as a standalone record yet (`academy/grades/` does not exist) rather than fabricating one or creating the directory, per this work order's "Do not create analysis content automatically unless explicitly requested by the command" constraint.
- `tools/atlas_academy/tests/` - 12 unit tests (`unittest`, matching `tools/atlas_router`'s and `tools/atlas_cli`'s existing test style), run against this repository's real Academy content (the `WO-2006`/`WO-2007`/`WO-2008` deliverables) rather than synthetic fixtures, including an explicit test that the CLI never writes into `academy/` across a full command sweep.
- Integration into `tools/atlas_cli/cli.py`: registered `academy` as a passthrough command (same mechanism as `doctor`, `planner`, `graph`), added it to the interactive shell's help text, and added one integration test to `tools/atlas_cli/tests/test_cli.py` confirming the passthrough wiring. This touches a file outside this work order's literal Deliverables list, but is required by its own Objective ("Implement the `atlas academy` command group as a first-class subsystem of the unified AtlasStudio CLI") and Constraint ("Reuse the existing AtlasStudio CLI architecture") - the command group cannot be reached through the unified CLI without it. Updated `tools/atlas_cli/README.md`'s command list to match, for the same reason.
- This work order, marked `submitted`.

No Design Pattern, `academy/*.md` content document, or schema was modified - this is integration and read access only. No map was edited. No file under `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` was touched. No analysis content (observation, composition, grade, or review) was created by this tool or by this work order.

Formatting: preserved existing house style for markdown deliverables; Python source follows `tools/atlas_cli`'s existing style (`from __future__ import annotations`, standard library only, `sys.dont_write_bytecode = True`).

Verification performed:

```bash
python3 -m unittest discover -s tools -p "test_*.py"
# Ran 29 tests, OK (12 new tools/atlas_academy tests, 1 new tools/atlas_cli
# integration test, 16 pre-existing tests unaffected)
python3 -m tools.atlas_cli.cli academy list
python3 -m tools.atlas_cli.cli academy study 001
python3 -m tools.atlas_cli.cli academy grade
python3 tools/atlas_format/format_guard.py --check
git status --porcelain
```

## Acceptance

Accepted 2026-07-09 following independent verification: every deliverable exists, `python3 -m unittest discover -s tools -p "test_*.py"` passes all 29 tests (12 new `tools/atlas_academy` tests included), and `atlas academy list` / `atlas academy help` were run live and behave as documented.
