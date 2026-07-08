---
work_order_id: WO-0030
title: AtlasStudio Interactive CLI
status: submitted
project: atlasstudio
recommended_agent: claude-code
agent_role: senior-software-architect
risk_level: low
player_facing: false
engine_specific: false
required_capabilities:
  - architecture-review
  - documentation
created: 2026-07-08
---

# WO-0030 - AtlasStudio Interactive CLI

## Purpose

AtlasStudio has reached functional maturity (`studio/STATUS.md`). Six separate tools now exist - `atlas_doctor`, `atlas_router`, `atlas_planner`, `atlas_graph`, `atlas_format`, `atlas_lint` - each invoked by its own long-form command. This work order designs a single, unified user-facing interface, `atlas`, that becomes the primary entry point for all daily work, so a Production Director no longer needs to remember which of six tools answers which question. This is a design and documentation work order: it specifies the interface completely enough that a future work order can implement it "almost mechanically," matching the standard `WO-0022` already set for the Work Order Router's own CLI. No implementation code is written here.

## Player-Facing Goal

Indirect. This work order changes no game file and adds no code. Its purpose is to make the daily production loop (`studio/operations/DAILY_WORKFLOW.md`) faster and less error-prone to actually run, which - if the interface it specifies is later built and adopted - should reduce the chance that a step gets skipped under time pressure, the same operational risk `studio/operations/PRODUCTION_CHECKLIST.md` and `reports/production-review/lessons-learned.md` already named.

## Background

Review: `work-orders/WO-0021-cross-repository-work-order-router.md`, `WO-0022-executable-router-specification.md`, `WO-0023-executable-work-order-router.md`, `WO-0028-production-pipeline-validation.md`, `WO-0029-atlasstudio-daily-operations.md`.

Review of all existing AtlasStudio command-line tools: `tools/atlas_doctor/doctor.py`, `tools/atlas_router/` (`CLI_SPEC.md`, `IMPLEMENTATION_SPEC.md`, `ERROR_HANDLING.md`, `ROUTING_TEST_PLAN.md`, and its Python package), `tools/atlas_planner/planner.py`, `tools/atlas_graph/` (`atlas_graph.py`, `query_graph.py`, `validate_graph.py`, `diff_graph.py`), `tools/atlas_format/format_guard.py`, `tools/atlas_lint/canon_lint.py`.

`tools/atlas_router/CLI_SPEC.md` (`WO-0022`) already specifies `atlas wo create/classify/preview/dispatch/explain` and passthrough commands `atlas doctor`/`atlas plan`/`atlas graph`/`atlas validate`/`atlas scheduler recommend`, invoked today as `python3 tools/atlas_router/cli.py <command>`, and states directly that a real `atlas` shell entrypoint unifying these is future, out-of-scope work. This work order is that future work, scoped to design only, and it explicitly reconciles with `CLI_SPEC.md` rather than restating or redefining it - see `studio/interface/ATLAS_CLI_SPEC.md`'s "Relationship to Existing Specifications" section, including the one required naming decision: `CLI_SPEC.md`'s placeholder `atlas status` stub (reserved for a future Atlas import/sync status command) is superseded by this work order's higher-traffic `atlas status` (a Studio Health snapshot); that future import/sync command is redirected to `atlas import status` instead, recorded as an amendment without editing `CLI_SPEC.md` itself.

`studio/operations/DAILY_WORKFLOW.md` (`WO-0029`) already defines the eleven-step daily loop this interface is built to serve, and `studio/operations/PLAYTEST_AND_ACCEPTANCE.md`'s four recorded outcomes are the model for this work order's new `atlas playtest record` command.

## Scope

### In Scope

- `studio/interface/ATLAS_CLI_SPEC.md`: the unified `atlas` executable, its command groups, and, for each of the fifteen named core commands, its Purpose, Inputs, Outputs, Underlying tools invoked, Exit codes, and Failure behavior.
- `studio/interface/COMMAND_REFERENCE.md`: a concise, example-driven reference covering the brief's named examples and representative examples for every command group.
- `studio/interface/INTERACTIVE_SHELL.md`: the design of `atlas` run with no arguments - prompt behavior, help, in-session history, a stated future scope for autocomplete, status banner behavior, and error handling.
- `studio/interface/USER_EXPERIENCE.md`: the intended user workflow for the six example requests named in this work order's brief, showing how `atlas` (specifically `atlas ask`) responds to each.
- `reports/interface/daily-cli-walkthrough.md`: a complete work session walked entirely through the unified CLI, starting at `atlas today` and ending at a committed implementation, including one accepted and one rejected outcome, routing, validation, and playtest.
- Reconciling this specification explicitly with `tools/atlas_router/CLI_SPEC.md` wherever a command name or behavior already exists there.
- A "Future Integration" section in `ATLAS_CLI_SPEC.md` describing how `atlas` is intended to grow into the Work Order Router, Planning Engine, Agent Scheduler, Studio Doctor, Pattern Library, Implementation Contracts, and GitHub automation.

### Out of Scope

- Implementing any part of `atlas` - no `.py` file is added or modified by this work order.
- Modifying `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` in any way.
- Modifying `tools/atlas_doctor/`, `tools/atlas_router/`, `tools/atlas_planner/`, `tools/atlas_graph/`, `tools/atlas_format/`, or `tools/atlas_lint/` - this work order specifies a layer above them and reconciles naming where needed, but does not edit any of their files.
- Adding a call to an external LLM API for natural-language interpretation - `atlas ask`'s interpretation is specified as deterministic, signal-based dispatch, matching the Work Order Router's and Agent Scheduler's existing "manual-first" / "no provider API called" principles.
- Building any automated dispatch beyond what `tools/atlas_router/github.py` already allows (`gh issue create`) - `atlas release` in particular is specified as report-and-propose only, never as a command that writes `studio/STATUS.md` automatically.

## Inputs

- `work-orders/WO-0021` through `WO-0023`, `WO-0028`, `WO-0029`.
- `tools/atlas_router/CLI_SPEC.md`, `IMPLEMENTATION_SPEC.md`, `ERROR_HANDLING.md`.
- `tools/atlas_doctor/doctor.py`, `tools/atlas_planner/planner.py`, `tools/atlas_planner/README.md`, `tools/atlas_graph/query_graph.py`, `tools/atlas_graph/validate_graph.py`, `tools/atlas_format/format_guard.py`, `tools/atlas_lint/canon_lint.py`, `tools/atlas_lint/README.md`.
- `studio/operations/DAILY_WORKFLOW.md`, `PRODUCTION_CHECKLIST.md`, `AGENT_USAGE_GUIDE.md`, `PLAYTEST_AND_ACCEPTANCE.md`, `REPOSITORY_DECISION_TREE.md`.
- `reports/operations/atlasstudio-day-in-the-life.md`.
- `studio/orchestration/work-order-router.md`, `studio/scheduling/agent-scheduler-design.md`, `studio/agent-roles.md`.
- `studio/immutable-formatting-rule.md`, `studio/work-order-format.md`, `studio/workflow.md`, `studio/STATUS.md`.

## Deliverables

- `studio/interface/ATLAS_CLI_SPEC.md`
- `studio/interface/COMMAND_REFERENCE.md`
- `studio/interface/INTERACTIVE_SHELL.md`
- `studio/interface/USER_EXPERIENCE.md`
- `reports/interface/daily-cli-walkthrough.md`
- `work-orders/WO-0030-atlasstudio-interactive-cli.md`

## Acceptance Criteria

- `ATLAS_CLI_SPEC.md` names the unified executable `atlas`, states its Command Groups, and documents Purpose, Inputs, Outputs, Underlying tools invoked, Exit codes, and Failure behavior for all fifteen named core commands (`today`, `next`, `status`, `doctor`, `ask`, `route`, `work`, `review`, `playtest`, `validate`, `graph`, `planner`, `dispatch`, `history`, `release`), plus a shared exit code table and a Future Integration section.
- `ATLAS_CLI_SPEC.md` explicitly reconciles every command that already exists in `tools/atlas_router/CLI_SPEC.md` (`doctor`, `plan`/`planner`, `graph`, `validate`, `dispatch`) rather than silently redefining it, and names the one required naming decision (`atlas status`'s new meaning superseding `CLI_SPEC.md`'s placeholder stub) explicitly rather than leaving the conflict implicit.
- `COMMAND_REFERENCE.md` includes, at minimum, the exact examples named in this work order's brief (`atlas today`, `atlas next`, `atlas ask "Improve Journey I"`, `atlas work create`, `atlas work review`, `atlas doctor`, `atlas validate`, `atlas release`) plus representative examples for every command group in `ATLAS_CLI_SPEC.md`.
- `INTERACTIVE_SHELL.md` documents prompt behavior, help, history, autocomplete (explicitly scoped as future), status banner behavior, and error handling, and shows the exact banner example given in this work order's brief.
- `USER_EXPERIENCE.md` shows how `atlas` responds to all six example requests named in this work order's brief ("I want to continue Journey I," "I have one hour tonight," "What should Codex work on?," "What's blocking production?," "Prepare a Claude work order," "Review today's progress").
- `daily-cli-walkthrough.md` starts at `atlas today` and ends with a successful implementation committed, and includes routing, validation, playtest, one accepted implementation (marked plainly as illustrative), and one rejected implementation (grounded in the real `BUILD-0043` precedent, not invented).
- No `.py` file, or any file outside the six deliverables listed above, is added or modified.
- No file under `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` is modified.
- No existing tool under `tools/` is modified.
- The Immutable Formatting Rule is preserved: no existing file is reformatted.
- This work order is marked `submitted`.

## Verification Steps

```bash
find studio/interface -name "ATLAS_CLI_SPEC.md" -o -name "COMMAND_REFERENCE.md" -o -name "INTERACTIVE_SHELL.md" -o -name "USER_EXPERIENCE.md"
find reports/interface -name "daily-cli-walkthrough.md"
find work-orders -name "WO-0030-atlasstudio-interactive-cli.md"
git diff --stat -- tools
# expect no output: no existing tool is modified
find studio/interface reports/interface -name "*.py"
# expect no output: documentation only, no code added
python3 tools/atlas_format/format_guard.py --check
git -C ../TheLastSwordProtocol-Atlas status --porcelain
git -C ../TheLastSwordProtocol-Game status --porcelain
```

## Allowed Changes

- `studio/interface/ATLAS_CLI_SPEC.md`
- `studio/interface/COMMAND_REFERENCE.md`
- `studio/interface/INTERACTIVE_SHELL.md`
- `studio/interface/USER_EXPERIENCE.md`
- `reports/interface/daily-cli-walkthrough.md`
- `work-orders/WO-0030-atlasstudio-interactive-cli.md`

## Protected Areas

- Do not modify `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game`.
- Do not modify any file under `tools/` (`atlas_doctor`, `atlas_router`, `atlas_planner`, `atlas_graph`, `atlas_format`, `atlas_lint`).
- Do not write or modify any code (`.py` or otherwise) - documentation only.
- Do not modify AtlasStudio canon.
- Preserve the Immutable Formatting Rule.

## Notes for Assigned Agent

This work order's own brief names fifteen core commands, several of which overlap in name or purpose with commands `tools/atlas_router/CLI_SPEC.md` (`WO-0022`) already fully specified. Do not silently redefine those - state explicitly, in `ATLAS_CLI_SPEC.md`, which commands are inherited unchanged, which are new, and how the one real naming conflict (`atlas status`) is resolved. This is the same discipline `WO-0028` and `WO-0029` already applied when their own investigation found a fact the work order's brief hadn't anticipated: report the reconciliation directly rather than writing around it.

The brief's Core commands list includes both a top-level `atlas review` and an `atlas work review` example in `COMMAND_REFERENCE.md`. These are not the same command - resolve the apparent overlap explicitly rather than picking one and dropping the other silently, since a reader hitting both names in the brief would reasonably expect a stated distinction.

`atlas ask` and `atlas release` are the two commands with the least existing precedent to build from. Keep both grounded in principles this project has already established elsewhere (deterministic, signal-based interpretation for `ask`, matching the Router and Scheduler's existing "no provider API, ever" rule; "recommend, never dispatch" for `release`, matching the Planner and Scheduler) rather than inventing new governing principles for either.

## Submission Record

Submitted 2026-07-08 by Claude Code.

Delivered:

- `studio/interface/ATLAS_CLI_SPEC.md` - the unified `atlas` executable specified across six command groups and fifteen core commands, each with Purpose/Inputs/Outputs/Underlying tools invoked/Exit codes/Failure behavior; an explicit "Relationship to Existing Specifications" section reconciling every command already defined by `tools/atlas_router/CLI_SPEC.md` (inherited unchanged: `doctor`, `graph`, `validate`, `dispatch`, `work create`; renamed with a preserved alias: `plan` → `planner`); the one required naming decision recorded explicitly (`atlas status`'s new Studio Health meaning supersedes `CLI_SPEC.md`'s placeholder import/sync stub, which is redirected to a future `atlas import status`); a shared exit code table extending `CLI_SPEC.md`'s existing 0-7 range with two new codes (8 = non-blocking attention, 9 = nothing found); full specifications for the nine new commands (`today`, `next`, `status`, `ask`, `route`, `work review`/`list`/`show`, `review`, `playtest record`/`show`, `history`, and the explicitly speculative `release`); a Future Integration section covering the Router, Planner, Scheduler, Doctor, Pattern Library, Implementation Contracts, and GitHub automation; and a Non-Goals section stating directly that `atlas ask` never calls an external model and `atlas release` never writes `STATUS.md` automatically.
- `studio/interface/COMMAND_REFERENCE.md` - a concise reference organized by the six command groups, including every example named in this work order's brief plus representative examples for each new command.
- `studio/interface/INTERACTIVE_SHELL.md` - the shell's launch banner (matching the brief's exact example), prompt behavior (a REPL over the same in-process command dispatch table, not a second parser), `help`/`help <command>` generated from `ATLAS_CLI_SPEC.md` rather than duplicated, in-session line history explicitly distinguished from the persistent `atlas history` command, autocomplete scoped as a stated future addition limited to two closed vocabularies, status banner refresh rules (delta lines instead of a full reprint after every command), and error handling (unknown-command suggestions, non-fatal command failures, Ctrl-C/Ctrl-D behavior).
- `studio/interface/USER_EXPERIENCE.md` - all six example requests from this work order's brief walked through `atlas ask`'s deterministic interpretation, each showing the interpreted command and its response, plus a closing section naming the read-only-runs-immediately / write-only-proposes distinction that governs every example.
- `reports/interface/daily-cli-walkthrough.md` - a full session narrated entirely through `atlas` commands: `atlas today` at the start, narrowing a broad `atlas ask` request, `atlas route`, assigning a carried-forward item via `atlas dispatch --approved-by` and a new item via `atlas work create`, `atlas work review`, `atlas validate`, two `atlas playtest record` outcomes (`WO-0031` Accepted, explicitly marked illustrative; `WO-0032` Rejected, grounded in the real `BUILD-0043` precedent), `atlas review`, and a final commit, closing with "Successful implementation committed."
- This work order, marked `submitted`.

No `.py` file was added or modified - confirmed directly; all six deliverables are Markdown. No file under `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` was modified - both were read-only throughout. No file under `tools/` was modified - `tools/atlas_router/CLI_SPEC.md` and the other existing tool documentation were read and reconciled against, not edited. No AtlasStudio canon file was modified.

Formatting: preserved existing house style; no existing file was reformatted. All six deliverables are new files.

Verification performed:

```bash
find studio/interface -maxdepth 1 -type f
find reports/interface -maxdepth 1 -type f
find work-orders -name "WO-0030-atlasstudio-interactive-cli.md"
git diff --stat -- tools
find studio/interface reports/interface -name "*.py"
python3 tools/atlas_format/format_guard.py --check
git -C ../TheLastSwordProtocol-Atlas status --porcelain
git -C ../TheLastSwordProtocol-Game status --porcelain
```
