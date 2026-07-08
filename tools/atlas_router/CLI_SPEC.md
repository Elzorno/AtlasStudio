# Work Order Router - CLI Specification

## Status

Specification only; no code exists yet. This document fully specifies every `atlas` subcommand's arguments, examples, exit codes, error behavior, and expected output, so `tools/atlas_router/cli.py` can be implemented mechanically against it. See `IMPLEMENTATION_SPEC.md` for the modules each command calls.

## Invocation

There is no installed `atlas` binary. Every command below is invoked as:

```bash
python3 tools/atlas_router/cli.py <command> [subcommand] [args...]
```

`atlas <command>` in this document is shorthand for the above, matching the shorthand already used informally in this project's planning conversations. A future, separate work order may add a real `atlas` shell entrypoint (e.g., a thin wrapper script on `PATH`); that is out of scope here.

## Shared Exit Code Table

Every subcommand in this package (`atlas wo *` and the passthroughs) uses this exact table. A subcommand must never return a code outside this table.

| Code | Meaning | When |
|---|---|---|
| 0 | Success | Classification/routing/dispatch completed and reached a non-blocked, non-error terminal state |
| 1 | Internal error | Malformed input file, unreadable JSON/Markdown, unexpected exception - matches `doctor.py`'s existing `OSError`/`JSONDecodeError`/`ValueError` handling pattern |
| 2 | Usage error | Bad or missing CLI arguments - `argparse`'s own default behavior, unchanged |
| 3 | Not yet implemented | A registered but unbuilt passthrough command (`atlas status`, `atlas import`, `atlas sync`) |
| 4 | Blocked: ambiguous | `routing_status == "blocked_ambiguous"` |
| 5 | Blocked: authority violation refused | `routing_status == "rejected_authority_violation"` |
| 6 | Blocked: external dependency unavailable | GitHub unreachable or network failure during dispatch (see `ERROR_HANDLING.md`) |
| 7 | Blocked: pending human approval | `routing_status == "pending_approval"` and dispatch was attempted without approval evidence |

## `atlas wo create`

Creates a new work order request from CLI flags (no pre-existing Markdown file required), classifies it, and - only if it resolves to an AtlasStudio-owned target - writes a new `proposed` work order file. For any other classification, it stops after reporting the routing decision; it never files a canon or unapproved game-implementation request as an AtlasStudio work order (see `IMPLEMENTATION_SPEC.md`, `dispatcher.py`).

**Arguments**

| Flag | Required | Type | Notes |
|---|---|---|---|
| `--title` | yes | string | |
| `--project` | yes | string | e.g. `atlasstudio`, `the-last-sword-protocol` |
| `--purpose` | yes | string | Free text, becomes the `## Purpose` section |
| `--scope-in` | no, repeatable | string | Each occurrence is one In Scope bullet |
| `--scope-out` | no, repeatable | string | Each occurrence is one Out of Scope bullet |
| `--capability` | no, repeatable | string | Populates `required_capabilities` |
| `--preferred-capability` | no, repeatable | string | Populates `preferred_capabilities` |
| `--risk-level` | no | `low`\|`medium`\|`high` | Default `medium` |
| `--player-facing` / `--no-player-facing` | no | flag | Default `--no-player-facing` |
| `--engine-specific` / `--no-engine-specific` | no | flag | Default `--no-engine-specific` |
| `--approved-by` | no | string | Presence signals human approval evidence for `game_implementation` (see Routing Rule 3) |
| `--approved-at` | no | ISO date | Required if `--approved-by` is set; defaults to today if omitted while `--approved-by` is set |
| `--json` | no | flag | Print the full `RoutingDecision` (and `DispatchOutcome`, if any) as JSON instead of human-readable text |
| `--dry-run` | no | flag | Classify and report only; never writes a file even for AtlasStudio-owned targets |

**Example**

```bash
python3 tools/atlas_router/cli.py wo create \
  --title "Extend Planning Engine scoring" \
  --project atlasstudio \
  --purpose "Add a technical-debt weighting dimension to the Planning Engine." \
  --scope-in "Add technical_debt_weight scoring field" \
  --capability architecture-review \
  --risk-level medium
```

**Expected output (text mode)**

```text
Classification: production_orchestration
Target repository: AtlasStudio
Routing status: routed
Signals matched:
  - required_capabilities contains architecture-review and scope names AtlasStudio tooling
Scheduler recommendation (advisory=False): agent.claude_code (score 17)
Wrote work-orders/WO-0023-extend-planning-engine-scoring.md (status: proposed)
```

**Exit codes**: 0 on successful write or successful dry-run; 4 if the request classifies `ambiguous` (no file written); 2 on bad arguments; 1 on internal error. `game_implementation` and `canon` requests never reach exit 0 via `create` in the "file written" sense - they exit 0 with a message directing the requester to `atlas wo dispatch` (canon/approved game_implementation) or noting the implementation-contract path, since no local write beyond the audit log occurs for those without going through `dispatch`. Precisely: `create` for `production_orchestration` and `cross_repository_bridge` writes and returns 0; `create` for `game_implementation` (any approval state) and `canon` classifies, records, prints the routing decision, writes nothing, and returns 0 (not an error - correctly declining to create a misplaced AtlasStudio work order is success, not failure).

## `atlas wo classify`

Runs parser + classifier + authority only (pipeline stages 1-3). No scheduler call, no dispatch, no file write beyond the audit log append.

**Arguments**

| Flag | Required | Notes |
|---|---|---|
| `<path>` (positional) | yes, unless `--stdin` | Path to an existing work order Markdown file |
| `--stdin` | no | Read a JSON-encoded request object from stdin instead of a file |
| `--json` | no | Print `ClassificationResult` + `RoutingDecision` as JSON |

**Examples**

```bash
python3 tools/atlas_router/cli.py wo classify work-orders/WO-0021-cross-repository-work-order-router.md
python3 tools/atlas_router/cli.py wo classify --stdin --json < request.json
```

**Expected output (JSON mode)**

```json
{
  "classification": "production_orchestration",
  "signals_matched": ["required_capabilities contains architecture-review; scope names studio/orchestration/"],
  "routing_status": "routed",
  "target_repository": "AtlasStudio",
  "safety_flags": {"canon_leak_risk": false, "cross_repo_write_attempted": false}
}
```

**Exit codes**: 0 = `routed` or `pending_approval`; 4 = `blocked_ambiguous`; 5 = `rejected_authority_violation`; 1 = unreadable input; 2 = bad arguments.

## `atlas wo preview`

Runs stages 1-4 (adds the scheduler's advisory agent recommendation) and shows exactly what `atlas wo dispatch` would do, without doing it. Always a dry run; never writes a file, never calls GitHub.

**Arguments**: identical to `atlas wo classify`, plus:

| Flag | Required | Notes |
|---|---|---|
| `--status-file` | no | Override path to the agent status file (default: `studio/scheduling/agent-status.json`, falling back to the `.example.json`) |

**Expected output (text mode)**

```text
Classification: game_implementation
Target repository: AtlasStudio (pending_approval)
Would write: work-orders/WO-0023-<slug>.md as an implementation contract pointing at IMP-HOM-019
Scheduler recommendation (advisory=True): agent.codex (score 14) - advisory only; approval and final assignment for TheLastSwordProtocol-Game remain with that repository's own process
```

**Exit codes**: same table as `classify`; `preview` never returns 6 or 7 since it never actually dispatches.

## `atlas wo dispatch`

Runs the full five-stage pipeline, including the real file write or GitHub issue call.

**Arguments**: identical to `atlas wo preview`, plus:

| Flag | Required | Notes |
|---|---|---|
| `--approved-by` | conditionally | Required to move a `game_implementation` request past `pending_approval` |
| `--approved-at` | no | Defaults to today when `--approved-by` is set |
| `--force-reissue` | no | Bypass the idempotency check in `github.py`'s `open_issue` (documented, rarely used; requires a stated reason via `--reason`) |
| `--reason` | conditionally | Required if `--force-reissue` is set |

**Examples**

```bash
python3 tools/atlas_router/cli.py wo dispatch work-orders/WO-0021-cross-repository-work-order-router.md
python3 tools/atlas_router/cli.py wo dispatch draft-requests/ashford-shop-wire.md --approved-by "Christopher Zornes" --approved-at 2026-07-07
```

**Expected output (text mode, canon case)**

```text
Classification: canon
Target repository: TheLastSwordProtocol-Atlas
Routing status: routed
Action: opened_github_issue
Issue: https://github.com/Elzorno/TheLastSwordProtocol-Atlas/issues/142
Note: AtlasStudio did not author this content. The issue contains the original request verbatim for Atlas's own work-order process to pick up.
```

**Exit codes**: 0 = dispatch completed (local write or GitHub issue created, or already existed per idempotency check); 4 = `blocked_ambiguous`, nothing dispatched; 5 = `rejected_authority_violation`, nothing dispatched; 6 = GitHub/network unavailable during an attempted dispatch to a sibling repository; 7 = `game_implementation` still `pending_approval` and no `--approved-by` was supplied; 1 = internal error; 2 = bad arguments.

## `atlas wo explain`

Read-only lookup into the audit log.

**Arguments**

| Flag | Required | Notes |
|---|---|---|
| `<work_order_id>` (positional) | yes | e.g. `WO-0021` |
| `--json` | no | Print the raw stored record |

**Example**

```bash
python3 tools/atlas_router/cli.py wo explain WO-0020
```

**Expected output (text mode)**

```text
WO-0020 - Ashford Village Implementation Contract from Atlas Handoff
Classification: game_implementation
Routing status: pending_approval -> routed (approved by Christopher Zornes, 2026-07-07)
Rationale: required_capabilities contains rpg-maker-json; scope names Map003 and IMP-HOM-019.
```

**Exit codes**: 0 = found; 1 = no record for that id (not a usage error, since the id itself may be well-formed but simply never routed - printed to stderr as "No routing record found for WO-XXXX").

## Passthrough Commands

These commands unify AtlasStudio's existing tools under one CLI surface without reimplementing them. Each forwards its arguments verbatim (after the command name) to the named script via `subprocess.run([sys.executable, <script path>, *forwarded_args])` and returns that process's exit code unchanged. `cli.py` performs no interpretation of these commands' arguments beyond splitting `command` from `forwarded_args`.

| Command | Forwards to | Status |
|---|---|---|
| `atlas doctor [args...]` | `tools/atlas_doctor/doctor.py` | Implemented (existing tool) |
| `atlas plan [args...]` | `tools/atlas_planner/planner.py` | Implemented (existing tool) |
| `atlas graph <get\|neighbors\|edges\|incoming\|path> [args...]` | `tools/atlas_graph/query_graph.py` | Implemented (existing tool) |
| `atlas validate [args...]` | Runs `tools/atlas_graph/validate_graph.py` then, only if that exits 0, `tools/atlas_format/format_guard.py --check`; exits 0 only if both succeed, otherwise returns the first non-zero exit code encountered | Implemented (composes two existing tools) |
| `atlas scheduler recommend <path> [--status-file PATH] [--json]` | Calls `scheduler.recommend()` in-process (this package's own module - not a subprocess, since this package implements the algorithm directly per `IMPLEMENTATION_SPEC.md`) | Implemented by this package |
| `atlas status [args...]` | Not yet implemented (see `bridges/atlas/import-architecture.md`'s named future tool `atlas_status.py`) | **Stub**: prints `"atlas status is not yet implemented. See bridges/atlas/import-architecture.md for its design."` to stderr, exits 3 |
| `atlas import [args...]` | Not yet implemented (`atlas_import.py`, WO-0019) | **Stub**: same pattern, referencing `bridges/atlas/import-architecture.md`, exits 3 |
| `atlas sync [args...]` | Not yet implemented (`atlas_sync.py`, WO-0019) | **Stub**: same pattern, referencing `bridges/atlas/synchronization-strategy.md`, exits 3 |

`atlas scheduler recommend` output matches `studio/scheduling/agent-scheduler-design.md`'s exact "Recommendation Output Format" JSON block when `--json` is passed; text mode prints the primary recommendation, its component scores, and its fallback chain as indented text, mirroring the worked examples in that document.

## Global Behavior

- Every command accepts `--json` where noted above; when omitted, output is human-readable text to `stdout` and diagnostics go to `stderr`, matching `tools/atlas_doctor/doctor.py` and `tools/atlas_planner/planner.py`'s existing convention.
- No command prompts interactively. All input is via flags, a file path, or `--stdin`. This is a deliberate constraint so the router can run unattended in a script or a future CI check without hanging on input.
- No command mutates a sibling repository's local working tree under any circumstance, including `--force-reissue`. The only sibling-repository side effect any command can ever produce is a GitHub issue via `github.py`.
