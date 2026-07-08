# Atlas CLI Specification

## Status

Specification only. No code exists yet, and this document introduces none - it designs the unified `atlas` command surface that `work-orders/WO-0022-executable-router-specification.md` already flagged as future work ("A future, separate work order may add a real `atlas` shell entrypoint... that is out of scope here"). This is that work order, scoped to design and documentation. Implementation is a future Codex-scoped work order, matching the `WO-0011` / `WO-0021`→`WO-0022`→`WO-0023` design-then-build precedent.

## Purpose

AtlasStudio Core is feature complete (`studio/STATUS.md`). Six tools now exist - `atlas_doctor`, `atlas_router`, `atlas_planner`, `atlas_graph`, `atlas_format`, `atlas_lint` - each invoked by its own long `python3 tools/atlas_<name>/<script>.py` command, each with its own argument conventions. A Production Director running `studio/operations/DAILY_WORKFLOW.md`'s eleven-step loop today has to remember which of six scripts answers which question. This document designs a single executable, `atlas`, that becomes the primary entry point for all of it - the daily loop, the Work Order Router, the Planning Engine, Studio Health, and the new quality-gate and production-milestone commands this work order adds.

`atlas` does not replace any existing tool. Every command below either passes an argument list straight through to an existing script (`tools/atlas_doctor/doctor.py`, `tools/atlas_planner/planner.py`, `tools/atlas_graph/query_graph.py`, `tools/atlas_format/format_guard.py`, `tools/atlas_router/cli.py`), or composes two or more of them, or - for nine commands that have no existing implementation - specifies a new command's behavior precisely enough that a future implementation work order can build it "almost mechanically," the same standard `WO-0022` set for the router itself.

## Relationship to Existing Specifications

`tools/atlas_router/CLI_SPEC.md` (`WO-0022`) already fully specifies `atlas wo create/classify/preview/dispatch/explain`, and passthrough commands `atlas doctor`, `atlas plan`, `atlas graph <get|neighbors|edges|incoming|path>`, `atlas validate`, and `atlas scheduler recommend`, all invoked today as `python3 tools/atlas_router/cli.py <command>`. This document does not redefine any of those - it is the outer layer around them.

Three things follow from that:

- Every command this document names that already appears in `CLI_SPEC.md` (`doctor`, `graph`, `validate`, `plan`/`planner`, `dispatch`) inherits that document's argument shape, output shape, and exit codes unchanged. This document states the inherited behavior briefly and points back to `CLI_SPEC.md` for the full detail, rather than restating it.
- This document adds nine commands with no prior specification: `today`, `next`, `status` (new meaning - see below), `ask`, `route`, `work review`/`work list`/`work show` (new `work` subcommands alongside the already-specified `work create`), `review`, `playtest`, and `history`, plus one command marked explicitly speculative: `release`.
- One naming decision has to be made explicitly, not left implicit: `CLI_SPEC.md` already reserves `atlas status` as a **stub** for a not-yet-built Atlas import/sync status command (`bridges/atlas/import-architecture.md`'s future `atlas_status.py`, `WO-0019`), exiting 3 with "not yet implemented." This document's `atlas status` (below) is a different, higher-traffic command - the one-screen Studio Health snapshot the Interactive Shell's banner needs (`INTERACTIVE_SHELL.md`). Because the unified CLI's own success criterion is that `atlas status` should be the single obvious thing a director types to see "is everything okay," that meaning wins the name. **Amendment:** when the future `atlas_status.py` import/sync command is eventually implemented, it is named `atlas import status`, not `atlas status`. `tools/atlas_router/CLI_SPEC.md` itself is not modified by this work order - this section is the recorded reconciliation a future implementer follows instead.

`atlas planner` is this document's preferred name for the command `CLI_SPEC.md` specified as `atlas plan`. Both names invoke the same passthrough to `tools/atlas_planner/planner.py`; `atlas plan` remains a valid alias so nothing in `CLI_SPEC.md` becomes incorrect.

## Command Groups

| Group | Commands | What it answers |
|---|---|---|
| Situational awareness | `today`, `next`, `status`, `doctor`, `history` | "Where do things stand, and what should I look at?" |
| Natural-language front door | `ask` | "I don't know which command I want - here's what I'm trying to do." |
| Routing and work management | `route`, `work`, `dispatch` | "Where does this request go, and how do I move a work order through its lifecycle?" |
| Quality gates | `review`, `playtest`, `validate` | "Is this output actually correct, and is it accepted?" |
| Knowledge and graph | `graph`, `planner` | "What does AtlasStudio know, and what does it recommend next?" |
| Production milestones | `release` | "Is this batch of accepted work ready to be called a release?" |

## Invocation

There is no installed `atlas` binary yet. Once built, `atlas <command>` is intended as a thin dispatcher - a single entrypoint script, likely `tools/atlas_cli/atlas.py` or a renamed evolution of `tools/atlas_router/cli.py`, exposed on `PATH` via a wrapper - that either handles a command in-process or forwards its arguments to the existing script that already implements it, exactly as `tools/atlas_router/cli.py` already does for its own passthroughs. Every example in this document and in `COMMAND_REFERENCE.md` is written in the target `atlas <command>` form; until that entrypoint exists, the equivalent long-form invocation is given in each command's "Underlying tools invoked" row.

## Shared Exit Code Table

This table extends `tools/atlas_router/CLI_SPEC.md`'s existing 0-7 table with two additional codes needed by the new commands this document specifies. Codes 0-7 keep their exact prior meaning; nothing is renumbered.

| Code | Meaning | When |
|---|---|---|
| 0 | Success | Command completed and reached a non-blocked, non-error terminal state |
| 1 | Internal error | Malformed input, unreadable file, unexpected exception |
| 2 | Usage error | Bad or missing CLI arguments, or missing required evidence for a recorded decision (e.g. `atlas playtest record` without `--evidence`) |
| 3 | Not yet implemented | A registered but unbuilt passthrough or stub command |
| 4 | Blocked: ambiguous | Router classification returned `blocked_ambiguous` |
| 5 | Blocked: authority violation refused | Router classification returned `rejected_authority_violation` |
| 6 | Blocked: external dependency unavailable | GitHub unreachable or network failure during dispatch |
| 7 | Blocked: pending human approval | A `game_implementation` request is `pending_approval` and no approval evidence was supplied |
| 8 | Attention (non-blocking) | The command completed and printed its report, but surfaced a condition worth human attention: unclean repository state, structural graph errors, a nonzero `blocked_ambiguous`/`pending_approval` count, or a `release` gate that is not yet green |
| 9 | Nothing found | A read-only query (`next`, `history`, a filtered `work list`) matched zero results - not an error, just an empty answer |

Passthrough commands (`doctor`, `validate`, `graph`, `planner`/`plan`, `dispatch`, `route`, `work create`) preserve the wrapped tool's own exit code unchanged, per the convention `CLI_SPEC.md` already established - they do not get remapped onto this table. Every other command in this document (`today`, `next`, `status`, `ask`, `work review`/`list`/`show`, `review`, `playtest`, `history`, `release`) uses this table directly.

## `atlas today`

**Purpose:** Run `studio/operations/DAILY_WORKFLOW.md`'s Steps 1-3 (Start of Day, Check Studio Health, Review Router Recommendations) as one command, so a session never starts with "what do I check first?"

**Inputs:** `--project` (default `the-last-sword-protocol`); `--json`.

**Outputs (text mode):**

```text
AtlasStudio - Today (2026-07-08)

Repositories:
  TheLastSwordProtocol-Atlas   clean
  AtlasStudio                  clean
  TheLastSwordProtocol-Game    clean

Studio Health: Healthy (0 structural errors, 8 work orders: 3 accepted, 4 proposed, 1 submitted)

Router: 1 pending_approval, 0 blocked_ambiguous
  - REQ-IMPLEMENT-IMP-HOM-019 (game_implementation, pending_approval)

Top recommendation: "Define RPG Maker implementation targets for Ashford Vale" (must-fix, 80/100)
  Run `atlas next` for full detail, or `atlas work review` on items already in flight.
```

**Underlying tools invoked:** `git status --porcelain` against all three repositories; `tools/atlas_doctor/doctor.py --project <project>`; `reports/atlas-router/routing-log.jsonl` (read, filtered to the most recent status per `work_order_id`); `tools/atlas_planner/planner.py` (read only the top-ranked recommendation).

**Exit codes:** 0 if all three repositories are clean and Studio Health reports zero structural errors; 8 if any repository has uncommitted changes, Studio Health reports a structural error, or the router log has any `blocked_ambiguous`/`pending_approval` entry - the report still prints in full either way; 1 on internal error.

**Failure behavior:** Never blocks - `today` is read-only across all three repositories and always finishes and prints, even when it has bad news to report. If Doctor itself fails to run (e.g. an unreadable graph file), that failure is shown inline under Studio Health rather than aborting the rest of the report.

## `atlas next`

**Purpose:** Answer "what should I work on" with exactly one recommendation, not the Planning Engine's full ranked report - the everyday shorthand for `DAILY_WORKFLOW.md` Step 4's first priority tier.

**Inputs:** `--project`; `--agent <id>` (filter to recommendations whose `Recommended agents` list includes this agent - the mechanism behind `atlas ask "What should Codex work on?"`, see `USER_EXPERIENCE.md`); `--json`.

**Outputs (text mode):**

```text
Next: "Define RPG Maker implementation targets for Ashford Vale"
  Priority: must-fix (80/100)
  Recommended agents: codex, claude-code
  Evidence:
    - Studio Doctor reports zero implementation target nodes.
    - Studio Doctor reports zero bridge implementation edges.
  Human action: Review and approve before creating or assigning work.

Run `atlas planner` for the full ranked list.
```

**Underlying tools invoked:** `tools/atlas_planner/planner.py`, filtered to its top-ranked entry (or the top entry matching `--agent`, if given).

**Exit codes:** 0 if a recommendation exists; 9 if the Planning Engine returns zero recommendations (a clean backlog, or `--agent` matches nothing); 1 on internal error.

**Failure behavior:** Never creates a work order and never assigns one - `next`, like the Planning Engine itself, only recommends.

## `atlas status`

**Purpose:** The one-screen Studio Health snapshot behind the Interactive Shell's banner (`INTERACTIVE_SHELL.md`) - narrower than `atlas doctor`'s full report, meant to answer "is everything okay?" at a glance, not to enumerate every finding.

**Inputs:** `--project`; `--json`.

**Outputs (text mode):**

```text
Project: The Last Sword Protocol
Studio Health: Healthy
Work Orders: 8 (3 accepted, 4 proposed, 1 submitted)
Router: 1 pending_approval, 0 blocked_ambiguous
Journey: I
```

**Underlying tools invoked:** `tools/atlas_doctor/doctor.py` (reused in-process for its health summary, not its full report), `reports/atlas-router/routing-log.jsonl` (counts only), and the project's current milestone/journey marker (`studio/STATUS.md`'s `Last Major Milestone` field today; a per-project `Journey` marker is a natural near-term extension once one exists per project, not invented by this document).

**Exit codes:** 0 if Studio Health is clean and the router has no `blocked_ambiguous` entries; 8 otherwise (still prints); 1 on internal error.

**Failure behavior:** Same read-only, always-prints behavior as `atlas today`, but deliberately terser - this is the command run every few minutes inside the Interactive Shell, not once per session, so it must stay fast and short. See the naming reconciliation in "Relationship to Existing Specifications" above.

## `atlas doctor`

**Purpose:** Full AtlasStudio health report - graph integrity, canon, production, implementation readiness, tools, missing sources, recommendations. Unchanged from `CLI_SPEC.md`'s existing passthrough specification.

**Inputs:** Identical to `python3 tools/atlas_doctor/doctor.py` - `--project`, `--json`.

**Outputs:** The existing `reports/atlas-doctor/latest.md`-shaped report (see that file for a worked example).

**Underlying tools invoked:** `tools/atlas_doctor/doctor.py`, forwarded verbatim.

**Exit codes:** The wrapped tool's own: `0` if `structural_error_count` is zero, `1` otherwise or on internal error.

**Failure behavior:** Unchanged from the existing tool - read-only, never mutates the graph or any work order.

## `atlas ask "<request>"`

**Purpose:** The natural-language front door named directly by this work order's brief - the command a director reaches for when they know what they want in plain language ("I want to continue Journey I," "What's blocking production?") but not which of the other fourteen commands answers it. `ask` interprets the request and either runs the matching read-only command directly, or - for anything that would write - prints exactly which command it would run and requires confirmation before running it. See `USER_EXPERIENCE.md` for the full worked set of example phrases and their interpretations.

**Inputs:** `<request>` (positional, quoted free text); `--yes` (skip the confirmation step for a write-shaped interpretation); `--json`.

**Outputs (text mode):**

```text
$ atlas ask "What's blocking production?"

Interpreted as: atlas today --project the-last-sword-protocol
(read-only - running now)

Router: 1 pending_approval, 0 blocked_ambiguous
  - REQ-IMPLEMENT-IMP-HOM-019 (game_implementation, pending_approval)
Studio Health: Healthy
Nothing else is blocking production right now.
```

```text
$ atlas ask "Prepare a Claude work order for extending the Planning Engine"

Interpreted as: atlas work create --title "Extend Planning Engine" --project atlasstudio \
  --purpose "..." --capability architecture-review
(this would create a file - not run without confirmation)

Run again with --yes, or run the command above directly.
```

**Underlying tools invoked:** Deterministic, signal-based interpretation over the same evidence `studio/orchestration/work-order-router.md` already uses for classification (keywords, named nouns, named repositories) - never a call to an external LLM API. This matches `studio/scheduling/agent-scheduler-design.md`'s "manual-first... no provider API is called, ever" principle and the router's "signal-based, deterministic, explainable" principle: `ask` is a keyword/pattern dispatcher over the other fourteen `atlas` commands, not a model call. Recognized intent shapes and their target commands:

| Example phrase shape | Delegates to |
|---|---|
| "I want to continue/improve X," "what should I work on" | `atlas today` then `atlas next` |
| "I have N hour(s) tonight" | `atlas next`, filtered to `risk_level: low`/single-session-scoped recommendations |
| "What should <agent> work on?" | `atlas next --agent <agent>` |
| "What's blocking production?" | `atlas today` (surfaces `blocked_ambiguous`/`pending_approval`/structural errors specifically) |
| "Prepare a <agent> work order for X" | `atlas work create` (drafted, not run, pending `--yes` or confirmation) |
| "Review today's progress" | `atlas review` |
| Anything unrecognized | Falls back to `atlas route "<request>"`, since the router's own classifier is AtlasStudio's general-purpose triage for free text it cannot otherwise place |

**Exit codes:** Delegates to the chosen command's exit code. If `ask` cannot match any recognized shape and its `atlas route` fallback returns `blocked_ambiguous`, the visible result is exit 4, with the message naming both facts ("could not interpret this locally; routed as a classification request, which was also ambiguous").

**Failure behavior:** Never performs a write (a new work order file, a dispatch, a playtest record) without either `--yes` or a separate confirmed re-run of the printed command - `ask` is a dispatcher and a teacher, not a second, looser approval path around the write-gates every other command already enforces.

## `atlas route "<request>"`

**Purpose:** The literal Work Order Router front door - "which repository owns this?" - narrower and more mechanical than `atlas ask`. Where `ask` interprets open-ended intent across all fifteen commands, `route` does exactly one thing: classify a request and report the routing decision, using the router pipeline `work-orders/WO-0021-cross-repository-work-order-router.md` and `tools/atlas_router/CLI_SPEC.md` already fully specify.

**Inputs:** Identical to `atlas wo classify` plus the advisory scheduler step from `atlas wo preview` - `<request>` or `--stdin`, `--json`.

**Outputs:** `CLI_SPEC.md`'s `wo classify`/`wo preview` output shape, unchanged.

**Underlying tools invoked:** `tools/atlas_router/cli.py wo classify` (stages 1-3: parse, classify, authority) followed by `wo preview` (adds the scheduler's advisory recommendation) when the classification is not `ambiguous`.

**Exit codes:** Inherited from `CLI_SPEC.md`'s `wo classify` table: 0 = `routed` or `pending_approval`; 4 = `blocked_ambiguous`; 5 = `rejected_authority_violation`; 1 = unreadable input; 2 = bad arguments.

**Failure behavior:** Read-only - never writes a file, never dispatches. Use `atlas work create` or `atlas dispatch` to act on a routing decision once it looks right.

## `atlas work`

A command group over a request's full lifecycle inside AtlasStudio's own process, before or instead of dispatch to a sibling repository.

### `atlas work create`

**Purpose:** Classify a new request and, only for AtlasStudio-owned targets, write a new `proposed` work order file. Unchanged from `CLI_SPEC.md`'s `wo create`.

**Inputs / Outputs / Exit codes:** Identical to `CLI_SPEC.md`'s `wo create`.

**Underlying tools invoked:** `tools/atlas_router/cli.py wo create`.

### `atlas work review`

**Purpose:** New. Run the mechanically checkable half of `studio/operations/PRODUCTION_CHECKLIST.md` against one submitted work order - the parts of `DAILY_WORKFLOW.md` Step 6 (Review Output) that don't require human judgment - so a reviewer's first pass is "here is what already checks out" rather than starting from a blank file.

**Inputs:** `<work_order_id>` (positional, e.g. `WO-0021`); `--json`.

**Outputs (text mode):**

```text
atlas work review WO-0023

Deliverables match Allowed Changes:        yes (git diff --stat matches declared paths)
Formatting preserved note present:         yes ("Formatting: preserved existing house style...")
Sources cited by path, not paraphrased:    needs human judgment
format_guard.py --check:                   clean
Sibling repositories untouched:            yes (git status clean in both)

3 of 5 checks automated and passing. 1 requires human judgment (see PRODUCTION_CHECKLIST.md).
```

**Underlying tools invoked:** `git diff --stat` against the work order's own `Allowed Changes` list; a text match for the Immutable Formatting Rule's recommended submission note (`studio/immutable-formatting-rule.md`); `tools/atlas_format/format_guard.py --check`; `git -C ../TheLastSwordProtocol-Atlas status --porcelain` and the Game-repo equivalent, when the work order's `engine_specific` or `player_facing` frontmatter suggests a sibling repository is involved.

**Exit codes:** 0 if every automatable check passes; 8 if at least one automatable check fails or needs attention (still prints the full table); 1 if the named work order does not exist; 2 on bad arguments.

**Failure behavior:** Never marks a work order `accepted` or `needs_revision` itself - that decision belongs to `atlas playtest record`. `work review` only reports what it can mechanically confirm; the "citation, not paraphrase" and "matches Acceptance Criteria in full" checks always come back `needs human judgment`, on purpose, since `lessons-learned.md` found exactly this kind of thing false-positived when treated as automatically satisfied.

### `atlas work list`

**Purpose:** New. List work orders, filterable by status - the everyday way to answer "what's already in flight" without opening `work-orders/` by hand.

**Inputs:** `--status <status>` (repeatable); `--project`; `--json`.

**Outputs (text mode):** One line per matching work order: id, title, status, `recommended_agent`.

**Underlying tools invoked:** Direct frontmatter read of `work-orders/*.md` (the same parsing convention `tools/atlas_router/parser.py` already uses).

**Exit codes:** 0 if any match; 9 if the filter matches nothing; 1 on a malformed work order file.

**Failure behavior:** Read-only.

### `atlas work show <id>`

**Purpose:** New. Print one work order's frontmatter, Purpose, and current status alongside its latest router log entry and graph node status, so a director doesn't have to open the Markdown file and cross-reference the routing log by hand.

**Inputs:** `<work_order_id>` (positional); `--json`.

**Underlying tools invoked:** `work-orders/<id>-*.md` (direct read); `reports/atlas-router/routing-log.jsonl` (last matching entry); `tools/atlas_graph/query_graph.py get work_order.<id>` (if a corresponding graph node exists).

**Exit codes:** 0 if found; 1 if no matching work order file exists; 2 on bad arguments.

**Failure behavior:** Read-only.

## `atlas review`

**Purpose:** New. The day/session-level counterpart to `atlas work review` - "Review today's progress" from `USER_EXPERIENCE.md`. Where `atlas work review` checks one submitted item, bare `atlas review` rolls up everything that changed today: work orders whose `status` field moved, accepted/rejected counts, and a fresh `atlas status` snapshot - `DAILY_WORKFLOW.md` Step 11 (Update Production Status) made checkable rather than left to memory.

**Inputs:** `--work-order <id>` (narrows to a single item - an alias for `atlas work review <id>`, kept here for discoverability since a director asking "review this" doesn't always know the two commands are different); `--since <date>` (default: today); `--json`.

**Outputs (text mode):**

```text
atlas review --since 2026-07-08

Work orders updated today:
  WO-0031  accepted        "Wire Ashford Shop cabinet flavor text"
  WO-0032  needs_revision  "Automated landmark decoration pass - REJECTED"

Studio Health: Healthy
Router: 0 pending_approval, 0 blocked_ambiguous
```

**Underlying tools invoked:** Without `--work-order`: `git log --since <date> -- work-orders/` (to find which work order files changed today), each changed file's frontmatter `status`, plus `atlas status`'s summary. With `--work-order`: delegates to `atlas work review <id>` directly.

**Exit codes:** 0 if at least one item was reviewed today or `--work-order` succeeds; 9 if nothing changed in the window; 1 on internal error.

**Failure behavior:** Read-only. Never changes a work order's status itself - see `atlas playtest record` for the command that actually records an acceptance decision.

## `atlas playtest`

**Purpose:** New. A structured recorder for the human decision `studio/operations/PLAYTEST_AND_ACCEPTANCE.md` already requires at `DAILY_WORKFLOW.md` Steps 8-9 - Accepted, Accepted with Notes, Rejected, or Deferred - so that decision lands in the work order file itself, not only in a chat transcript or a report nobody but today's director reads (the exact gap `lessons-learned.md` found and named a standing practice to close). `atlas playtest` never performs the playtest - a human must actually play the build - it only records an already-made decision and its required evidence pointer, and fails closed if the evidence `PLAYTEST_AND_ACCEPTANCE.md` requires for the chosen outcome is missing.

### `atlas playtest record`

**Inputs:**

| Flag | Required | Notes |
|---|---|---|
| `--work-order <id>` | yes | |
| `--outcome` | yes | `accepted` \| `accepted-with-notes` \| `rejected` \| `deferred` |
| `--evidence` | yes for `accepted`/`accepted-with-notes`/`rejected` | Free text: what was actually played, and the validation run it was checked against |
| `--reason` | yes for `rejected` | The specific, recorded failure reason `PLAYTEST_AND_ACCEPTANCE.md` requires - not a general impression |
| `--notes` | repeatable, required for `accepted-with-notes` | Each occurrence becomes one tracked note |
| `--json` | no | |

**Outputs:** Appends a `## Playtest Record` subsection to the named work order's Markdown file recording the outcome, evidence, reason/notes, date, and recorder, and updates its `status` frontmatter field per `studio/workflow.md`'s lifecycle (`accepted`/`accepted-with-notes` → `accepted`; `rejected` → `needs_revision`; `deferred` → left unchanged, flagged as `deferred` in the new subsection).

**Underlying tools invoked:** Direct, targeted edit of the named work order's Markdown file (append-only to a new subsection plus the single `status` field - never a broad reformat, per the Immutable Formatting Rule); reads `studio/operations/PLAYTEST_AND_ACCEPTANCE.md`'s required-evidence table to decide which flags are mandatory for the given `--outcome`.

**Exit codes:** 0 on successful record; 2 if a required flag for the chosen outcome is missing (e.g. `rejected` without `--reason`) - `playtest record` fails closed exactly the way the router does for ambiguous requests, rather than recording an outcome it cannot justify; 1 if the named work order does not exist.

**Failure behavior:** Never records `accepted` without `--evidence` naming an actual playtest, per `PLAYTEST_AND_ACCEPTANCE.md`'s Required Evidence section. Never silently overwrites a prior recorded outcome for the same work order - a second `record` call appends a new dated subsection rather than replacing the first, so a Rejected → (fix) → Accepted history stays visible.

### `atlas playtest show <id>`

**Purpose:** Print a work order's recorded playtest history.

**Underlying tools invoked:** Direct read of the work order's `## Playtest Record` subsection(s).

**Exit codes:** 0 if found; 9 if the work order has no recorded playtest yet; 1 if the work order does not exist.

## `atlas validate`

**Purpose:** Composite validation gate - unchanged from `CLI_SPEC.md`'s existing specification.

**Inputs / Outputs:** Identical to `CLI_SPEC.md`'s `atlas validate`.

**Underlying tools invoked:** `tools/atlas_graph/validate_graph.py`, then, only if that exits 0, `tools/atlas_format/format_guard.py --check`.

**Exit codes:** 0 only if both succeed; otherwise the first non-zero exit code encountered.

**Failure behavior:** Unchanged - read-only, never mutates graph or file content.

## `atlas graph`

**Purpose:** Query Atlas Graph nodes and edges - unchanged from `CLI_SPEC.md`'s existing specification.

**Inputs / Outputs:** Identical to `CLI_SPEC.md`'s `atlas graph <get|neighbors|edges|incoming|path>`.

**Underlying tools invoked:** `tools/atlas_graph/query_graph.py`, forwarded verbatim.

**Exit codes:** The wrapped tool's own.

**Failure behavior:** Unchanged - read-only.

## `atlas planner`

**Purpose:** Full Planning Engine report - unchanged in behavior from `CLI_SPEC.md`'s `atlas plan`; renamed here as the unified CLI's preferred surface name, with `atlas plan` preserved as an alias (see "Relationship to Existing Specifications").

**Inputs / Outputs:** Identical to `python3 tools/atlas_planner/planner.py`.

**Underlying tools invoked:** `tools/atlas_planner/planner.py`, forwarded verbatim.

**Exit codes:** The wrapped tool's own.

**Failure behavior:** Unchanged - never creates a work order.

## `atlas dispatch`

**Purpose:** Run the router's full five-stage pipeline including the real file write or GitHub issue call - unchanged from `CLI_SPEC.md`'s `wo dispatch`, exposed as a shorter top-level name because dispatch is common enough in the daily loop (Step 5, Assign Agent, once a `pending_approval` item is approved) to deserve one.

**Inputs / Outputs / Exit codes:** Identical to `CLI_SPEC.md`'s `wo dispatch`.

**Underlying tools invoked:** `tools/atlas_router/cli.py wo dispatch`.

**Failure behavior:** Unchanged - never writes directly into a sibling repository; the only sibling-repository side effect is a GitHub issue via `github.py`.

## `atlas history`

**Purpose:** New. One place to see what happened - routing decisions, work order status transitions, and governance Decision Records - instead of reading `reports/atlas-router/routing-log.jsonl`, `git log`, and `studio/governance/decisions/` separately.

**Inputs:** `--work-order <id>` (all router log entries and status transitions for one item - a superset of `CLI_SPEC.md`'s `wo explain`, which stays available directly for router-only detail); `--repository <name>` (filter to items targeting one repository); `--since <date>`; `--router` (router log only, equivalent to `wo explain` across all entries); `--json`.

**Outputs (text mode):**

```text
atlas history --work-order WO-0020

2026-07-07  routed          game_implementation -> AtlasStudio (pending_approval)
2026-07-07  approved        by Christopher Zornes
2026-07-08  status: accepted (via atlas playtest record)
```

**Underlying tools invoked:** `reports/atlas-router/routing-log.jsonl` (filtered); `git log --follow -- work-orders/<id>-*.md` (status transitions over time); `studio/governance/decisions/` (any Decision Record naming the same work order id).

**Exit codes:** 0 if any entry matches; 9 if the filter matches nothing; 2 on bad arguments.

**Failure behavior:** Read-only.

## `atlas release`

**Purpose:** New and explicitly the least mature command in this specification - no existing tool composes this today, and this document only specifies its intended shape for a future implementation work order, the same treatment `CLI_SPEC.md` gave `atlas status`/`import`/`sync` as stubs. `release` is a studio-level checkpoint: is the batch of work accepted since the last recorded milestone (`studio/STATUS.md`'s `Last Major Milestone` field) ready to be called a release? It gates on Studio Health, `atlas validate`, and lists every `accepted` work order since that marker; on a non-dry-run invocation it proposes (never silently writes) an updated milestone line for human confirmation, following the same "recommend, never dispatch" principle already governing the Planner and the Scheduler.

**Inputs:** `--dry-run` (default; report only); `--confirm` (required to actually propose the `STATUS.md` update - still requires a human to apply it, matching the router's own "recommends; does not dispatch" rule); `--json`.

**Outputs (text mode):**

```text
atlas release --dry-run

Since "WO-0021 — Cross-Repository Work Order Router" (last recorded milestone):
  Accepted: WO-0022, WO-0023, WO-0024, WO-0025, WO-0026, WO-0027, WO-0028, WO-0029

Gates:
  Studio Health:  Healthy
  atlas validate: clean

Release-ready: yes
Run `atlas release --confirm` to propose an updated STATUS.md milestone line for review.
```

**Underlying tools invoked:** `atlas status`; `atlas validate`; `work-orders/*.md` frontmatter (`status: accepted`, filtered by `created` date after the current milestone marker); `studio/STATUS.md` (read; proposes a diff, never writes it directly even with `--confirm` - `--confirm` prints the exact diff for a human to apply by hand, consistent with every other AtlasStudio recommend-only mechanism).

**Exit codes:** 0 if every gate is green; 8 if any gate is not green (report still prints, `Release-ready: no`, with the specific failing gate named); 1 on internal error.

**Failure behavior:** Never edits `studio/STATUS.md` or any other file under any flag combination - `release` is a report-and-propose command, identical in spirit to the Planning Engine and the Agent Scheduler's "recommend, never dispatch" rule. This is a deliberate, explicit non-goal, not an oversight: AtlasStudio's operating principle across every prior work order in this area is that AI-facing tooling recommends and a human commits.

## Future Integration

This section states how `atlas` is meant to grow into the systems that already exist, without any of it being built by this work order.

- **Work Order Router (`tools/atlas_router/`):** already the largest source of existing commands (`route`, `work create`, `dispatch`, half of `history`). Future growth: `atlas ask`'s deterministic interpretation table should eventually share its signal vocabulary with `studio/orchestration/work-order-router.md`'s own classification signals, so the two front doors ("what am I trying to do" and "which repository owns this") stay in sync instead of drifting into two separate keyword lists.
- **Planning Engine (`tools/atlas_planner/`):** already `atlas next`/`atlas planner`. Future growth: `atlas next --agent`'s filter and `atlas release`'s milestone gate are both natural inputs the Planning Engine could eventually score directly, rather than this CLI layer filtering its output after the fact.
- **Agent Scheduler (`studio/scheduling/`):** currently reached only indirectly through `atlas wo preview`'s advisory recommendation (inherited via `atlas route`). A future `atlas work assign <id> --agent <agent>` command is a natural next addition once the Scheduler's `agent-status.json` (not just its example file) is in regular use - deliberately not added here, since it does not yet exist in production and this document does not invent commands for tools that are not real yet, per `studio/STATUS.md`'s frozen-Core, production-driven-growth rule.
- **Studio Doctor (`tools/atlas_doctor/`):** already `atlas doctor` (full) and `atlas status`/`atlas today` (summary). No further integration is anticipated beyond keeping the summary views in sync with whatever Doctor's health dictionary reports next.
- **Design Pattern Library (`studio/design-patterns/`):** not directly wrapped by any command here. Future growth: `atlas work create` for a `game_implementation` request could eventually prompt for (or auto-suggest) an applicable pattern by name and confidence tier, the way `reports/implementation-contracts/ashford-shop-pattern-aware-contract.md` already does by hand - a CLI convenience over an existing practice, not a new one.
- **Implementation Contracts (`reports/implementation-contracts/`):** `atlas work create` for `game_implementation` already produces this shape of file today via the router's `dispatcher.py`. Future growth: `atlas work show` could render a contract's cited pattern and packet inline, once contracts consistently name them in a machine-readable frontmatter field rather than prose.
- **GitHub automation:** already reached through `atlas dispatch`'s existing, narrow `github.py` (`gh issue create` only, never a direct write). Future growth, explicitly out of scope for now: `atlas release --confirm` opening a release-tracking GitHub issue once AtlasStudio has a public issue tracker workflow to open it into - not specified further here because no such workflow exists yet to integrate with.

## Non-Goals

- `atlas` does not call any external LLM API to interpret `atlas ask` requests. Interpretation is deterministic keyword/pattern matching, per the same principle already governing the Agent Scheduler and the Work Order Router.
- `atlas` never gains write access to `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` beyond what `tools/atlas_router/github.py` already allows (opening a GitHub issue). No command in this document writes a file into either sibling repository.
- `atlas release` never edits `studio/STATUS.md` automatically, under any flag. It proposes; a human applies.
- No command in this document is implemented by this work order. This is a specification, matching `tools/atlas_router/CLI_SPEC.md`'s own precedent of a fully detailed, unimplemented command surface handed to a future build work order.
