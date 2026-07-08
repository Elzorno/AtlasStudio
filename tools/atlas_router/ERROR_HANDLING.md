# Work Order Router - Error Handling Specification

## Status

Specification only. Every error condition below must produce a deterministic result: same input, same failure, same output, every time. No error path may silently default to a repository, silently retry over the network, or silently degrade a blocking condition into a warning. Where a condition is explicitly downgraded to a non-fatal warning below, that downgrade is itself the deterministic, specified behavior - not a fallback improvised at implementation time.

## Error Catalogue

### 1. Ambiguous requests

**Condition:** `classifier.classify()` finds no matching signal, or the matched signals do not agree on a single classification (see `IMPLEMENTATION_SPEC.md`, `classifier.py`).

**Behavior:** `routing_status = "blocked_ambiguous"`, `target_repository = "none"`. `authority.py` never assigns a repository in this state, including AtlasStudio - defaulting an ambiguous request to AtlasStudio would itself be a canon-leak risk if the ambiguity involved canon content, per `studio/orchestration/work-order-router.md`'s Safety Rules.

**Output contract:**

```json
{
  "routing_status": "blocked_ambiguous",
  "target_repository": "none",
  "rationale": "<one of the two templates below>",
  "signals_matched": []
}
```

- `ambiguous_reason == "no_signal_matched"` -> rationale: `"No signal distinguishes canon, implementation, or orchestration scope. This request needs a named location, character, or content area, a named defect or file, or a named AtlasStudio system before it can be classified."`
- `ambiguous_reason == "conflicting_repository_signals"` -> rationale: `"This request matches signals for more than one repository (<list classifications>). Split it into one request per repository before resubmitting."`

**CLI exit code:** 4. **No dispatch is attempted.** The audit log still receives one entry (blocked decisions are recorded, not discarded).

### 2. Multiple matching repositories

This is the specific subtype of Ambiguous Requests where `signals_matched` produced more than one distinct classification. It is not a separate error category from a data-shape standpoint - it always surfaces as `blocked_ambiguous` with `ambiguous_reason = "conflicting_repository_signals"` and a populated `conflicting_classifications` list, per case 24 and case 29 in `ROUTING_TEST_PLAN.md`. It is called out separately here because it is the one condition the router must actively distinguish from plain "no signal at all" (case 1's `no_signal_matched`) in its rationale text - the two failure modes require different corrective action from the requester (adding information, versus splitting a request), and collapsing them into identical output would be a regression against `ROUTING_TEST_PLAN.md`'s coverage checklist.

### 3. Missing authority (repository boundary data unavailable)

**Condition:** `authority.py`'s `REPOSITORY_BOUNDARIES` constant fails to load, is empty, or is missing an entry for a classification `classifier.py` can produce. Since this constant is a Python literal in the module (per `IMPLEMENTATION_SPEC.md`), this should be structurally impossible in a working build - this case exists to specify **fail-closed** behavior for the test suite to assert, and to forbid a specific bad implementation: falling back to a default repository when boundary data can't be found.

**Behavior:** Raise an internal error immediately. Do not classify, do not route, do not write to the audit log with a guessed target. `route()` must raise `RouterConfigurationError` (a new exception defined in `models.py` or `authority.py`) rather than return a `RoutingDecision` with a best-guess `target_repository`.

**CLI exit code:** 1. **Never** 0. A router that cannot verify ownership boundaries must refuse to operate, not operate permissively - this is the same fail-closed posture `repository-authority.md` already requires of humans ("AtlasStudio does not originate these changes" applies equally to a tool acting on AtlasStudio's behalf).

### 4. Unknown project

**Condition:** The request's `project` field does not match any project AtlasStudio's Atlas Graph or `repository-authority.md` recognizes (currently only `atlasstudio` and `the-last-sword-protocol`).

**Behavior:** Non-fatal. `project` is not itself a classification signal (per `classifier.py`'s signal table, which reasons about content nouns and capabilities, not the project label) - an unrecognized project does not change `classification` or `target_repository`. The router appends a warning: `"unknown_project: '<value>' not found in Atlas Graph project list"` to `RoutingDecision.warnings` and continues normally.

**CLI exit code:** unaffected - whatever the classification's own exit code would otherwise be (typically 0).

### 5. Missing implementation packet

**Condition:** A request classifies `game_implementation` (matches `rpg-maker-json` capability and a named `TheLastSwordProtocol-Game` file/map), but no `IMP-<AREA>-<NNN>` identifier appears anywhere in the request's Purpose or Scope text.

**Behavior:** The request still classifies `game_implementation` and still resolves to the default `pending_approval` / AtlasStudio-implementation-contract path - a missing packet reference does not change the classification, matching `game_implementation` case 28 in `ROUTING_TEST_PLAN.md`. However, this condition additionally sets a stronger block: even if `--approved-by` is later supplied to `atlas wo dispatch`, dispatch must refuse to progress past `pending_approval` until an implementation packet id is present, because `WO-0020`'s precedent establishes that implementation contracts are written *from* an existing Atlas packet, never invented independently. The refusal message: `"Cannot approve: no Atlas implementation packet (IMP-<AREA>-<NNN>) is cited in this request. Cite the packet this work implements before requesting approval."`

**CLI exit code:** 7 (same code as ordinary `pending_approval`, since this is a more specific reason for the same blocked state, not a new state).

### 6. Missing graph nodes

**Condition:** `atlas wo explain <work_order_id>` (or any future cross-reference into the Atlas Graph) is asked about an id with no corresponding entry.

**Behavior:** Non-fatal for classification (classification never depends on the graph already containing a node for the work order being classified - that would be circular, since classification happens before a node would ever be created). For `explain` specifically: print `"No routing record found for <id>"` to `stderr` and return.

**CLI exit code:** 1 for `atlas wo explain` on an unknown id (distinguished from a usage error because the id is well-formed, it simply has no record - matching `doctor.py`'s convention of using 1 for "read succeeded structurally but the requested data isn't there").

### 7. Missing scheduler information

**Condition:** Neither `studio/scheduling/agent-status.json` nor `studio/scheduling/agent-status.example.json` can be read, or an existing status file has entries older than 7 days (per `agent-scheduler-design.md`'s existing degrade rule).

**Behavior:** Two sub-cases, both already specified by `agent-scheduler-design.md` and inherited unchanged:

- **Stale entry (>7 days since `last_verified`):** degrade that single agent's `availability` to `unknown` per the existing rule; scheduling continues.
- **File entirely missing:** fall back from `agent-status.json` to `agent-status.example.json`; force `SchedulerRecommendation.advisory = True` regardless of `target_repository`, and append the warning `"no live agent-status.json found; using agent-status.example.json for illustrative scoring only"`.

**Behavior specific to this package (new rule, not already in `agent-scheduler-design.md`):** `atlas wo dispatch` must refuse to treat a recommendation computed from the example status file as sufficient grounds to proceed past `pending_approval` for `game_implementation` - the human's own `--approved-by` evidence is what gates that transition, never the scheduler's recommendation, so this case does not block dispatch by itself. It only affects the *displayed* recommendation's trustworthiness, which is why it is surfaced as a warning rather than an error.

**CLI exit code:** unaffected (0, assuming everything else succeeds); warnings appear in output regardless of `--json`.

### 8. Unknown agent

**Condition:** A work order's existing `recommended_agent` frontmatter value (a human-authored field, separate from the router's own computed recommendation) does not match any id in `studio/agent-roles.md`'s known set (`gpt`, `claude-code`, `codex`, `github-copilot`, `ollama`, `human`, `atlasstudio`).

**Behavior:** Non-fatal. The router's own `SchedulerRecommendation` is computed independently of this field (it is informational input to `parser.py`'s `WorkOrderRequest`, not used by `classifier.py` or `scheduler.py`'s ranking). Append the warning `"unknown_agent: '<value>' does not match any known agent id in studio/agent-roles.md"`. No recommendation is withheld because of this.

**CLI exit code:** unaffected.

### 9. Network failure

**Condition:** `github.py`'s `subprocess.run(["gh", ...])` call times out, the process is killed, or the underlying network is unreachable, during `atlas wo dispatch` for a `canon` or approved `game_implementation` request.

**Behavior:** Caught in `github.py`, re-raised as a specific `NetworkError`. No automatic retry loop - a single attempt, then a deterministic failure. Because `audit.append_routing_record` is called with the `RoutingDecision` *before* `dispatcher.py` attempts the GitHub call (see `IMPLEMENTATION_SPEC.md`'s pipeline diagram - classification is persisted independently of dispatch outcome), a network failure during dispatch never loses the classification decision; only the dispatch action itself fails and can be retried later via the same command, using `DispatchOutcome.idempotency_key` to avoid a duplicate issue if the first attempt actually succeeded server-side before the client-side failure was observed.

**Output:** `"Dispatch failed: network error contacting GitHub. The routing decision was recorded; no issue was created. Retry 'atlas wo dispatch' once connectivity is restored."` to `stderr`.

**CLI exit code:** 6.

### 10. GitHub unavailable

**Condition:** `gh` is not installed, not authenticated, rate-limited, or the target repository returns a permission error.

**Behavior:** Same handling path as Network Failure (`GithubUnavailableError`, distinguished from `NetworkError` only in the message text so a human can tell "check your connection" apart from "check your `gh auth status`"). The one rule that must never be violated regardless of cause: **a GitHub failure must never cause the router to fall back to writing directly into the sibling repository's local working tree as a workaround.** Even though `TheLastSwordProtocol-Atlas` and `TheLastSwordProtocol-Game` happen to be present as sibling directories on this machine (per `IMPLEMENTATION_SPEC.md`'s Source Documents review), the router has no code path that opens a file handle under either sibling directory, under any error condition - convenience is never a justification for bypassing `repository-authority.md`'s "must not write directly" rule.

**CLI exit code:** 6.

### 11. Atlas unavailable

**Condition:** A `cross_repository_bridge` classification's optional comparison step (e.g., diffing against an imported Atlas entity snapshot) cannot find the expected local snapshot data or sibling directory.

**Behavior:** Non-fatal for classification - none of the five classifications require live access to `TheLastSwordProtocol-Atlas` to be determined; they are all decided from the request's own content per `classifier.py`. Only a bridge command that explicitly performs a comparison (out of scope for this package's CLI surface; a future `atlas sync`/`atlas import` concern per `bridges/atlas/synchronization-strategy.md`) would skip that comparison step with a warning: `"Atlas snapshot unavailable; comparison skipped."` This is unrelated to GitHub reachability (case 10) - a missing local snapshot and an unreachable GitHub remote are independent failure conditions and must not be conflated in error messages.

**CLI exit code:** unaffected for classification-only commands; if a future comparison-dependent command cannot proceed at all without the snapshot, that command specifies its own exit code when it is designed - not retroactively defined here.

## Cross-Cutting Rules

- **Every blocked or rejected decision is still recorded.** `audit.append_routing_record` runs for every terminal state, including `blocked_ambiguous` and `rejected_authority_violation`. A blocked request is not a silent no-op; it is a permanent, reviewable record.
- **No silent default to any repository, ever, under any error condition.** This is the single rule every case above is checked against. If an implementation detail would require guessing a `target_repository` to keep running, the correct behavior is always to stop (exit 1, 4, or 5, never a guessed 0).
- **No automatic retries.** Network and GitHub failures fail once, deterministically, and are reported for a human-initiated retry - matching the router's broader "recommend/report, never autonomously act past what was asked" posture already established by `capability-based-orchestration.md` and `agent-scheduler-design.md`.
- **Warnings never suppress a blocking status, and blocking statuses never get downgraded to warnings.** The distinction between "append to `warnings` and continue" (cases 4, 6, 7, 8, 11) and "set a blocking `routing_status` / raise / non-zero exit" (cases 1, 2, 3, 5, 9, 10) is fixed by this document, not left to implementation judgment.
