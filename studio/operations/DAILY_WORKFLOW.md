# Daily Workflow

## Purpose

This document describes a complete production day for a Production Director using AtlasStudio to run `The Last Sword Protocol`. It exists so that no session starts with the question "what do I do first?" - the answer is always the same eleven steps, in the same order, whether the day ends in an accepted build or a rejected one.

This document does not introduce any new tool, gate, or authority. It sequences what `studio/workflow.md`, `studio/governance/repository-authority.md`, `studio/orchestration/work-order-router.md`, `studio/scheduling/agent-scheduler-design.md`, and `studio/governance/production-readiness.md` already define, in the order a human actually uses them across one day.

## The Daily Loop

```text
Start of day
  |
  v
Check Studio Health
  |
  v
Review Router recommendations
  |
  v
Select work
  |
  v
Assign agent
  |
  v
Review output
  |
  v
Validate
  |
  v
Playtest
  |
  v
Accept or Reject
  |
  v
Commit
  |
  v
Update production status
```

Each step is described below with what it means, which tool or document governs it, and what "done" looks like before moving to the next step.

## 1. Start of Day

Open all three repositories (`TheLastSwordProtocol-Atlas`, `AtlasStudio`, `TheLastSwordProtocol-Game`) side by side, or at minimum confirm all three are on their expected branch with no unexpected local changes:

```bash
git -C ../TheLastSwordProtocol-Atlas status --porcelain
git -C ../AtlasStudio status --porcelain
git -C ../TheLastSwordProtocol-Game status --porcelain
```

If any repository shows unexpected uncommitted changes, resolve that before doing anything else - a day should never start on unknown state.

## 2. Check Studio Health

Run AtlasStudio's own diagnostic before trusting anything it recommends today:

```bash
python3 tools/atlas_doctor/doctor.py --project the-last-sword-protocol
```

Read the result against `reports/atlas-doctor/latest.md`, the most recent stored report. Look specifically at:

- **Graph Integrity** - structural errors must be zero before work order graph edges are trusted.
- **Production** - the work order status mix (`proposed` / `assigned` / `submitted` / `accepted` / etc.) tells you what is already in flight before you add more.
- **Orphan Nodes** - a work order with no assignment, dependency, review, or impact edge is a loose end from a prior day, not new information.

If Studio Health reports a structural error, fix or triage it before selecting new work - a broken graph makes every later recommendation in the day less trustworthy.

## 3. Review Router Recommendations

Before drafting anything new, check what the Work Order Router (`studio/orchestration/work-order-router.md`, `tools/atlas_router/`) already knows:

```bash
cat reports/atlas-router/routing-log.jsonl
```

This tells you which requests have already been classified, which are `pending_approval` and waiting on a human decision, and which are `blocked_ambiguous` and need a clearer scope before they can move at all. A `blocked_ambiguous` entry from a prior day is unfinished business, not something to re-guess today - it needs the missing signal named in its `rationale`, per the Repository Decision Tree (`REPOSITORY_DECISION_TREE.md`).

## 4. Select Work

Choose the day's work from what Studio Health and the Router surfaced, in this priority order:

1. Anything `blocked_ambiguous` that now has enough information to classify.
2. Anything `pending_approval` that is ready for the human approval step it is waiting on.
3. The highest-priority item in `studio/governance/production-readiness.md`'s backlog (Immediate, then Near-Term, then Long-Term) that has no open blocker.
4. New work the human creator wants to start, classified fresh:

```bash
python3 tools/atlas_router/cli.py wo classify "<request text or work order path>" --json
```

Never select work by skipping classification because "it's obviously an AtlasStudio thing" - that assumption is exactly the failure mode `WO-0018` had to unwind. See `REPOSITORY_DECISION_TREE.md`.

## 5. Assign Agent

Once a request is classified and its target repository confirmed, decide who does it using `AGENT_USAGE_GUIDE.md` and the Agent Scheduler's scoring model (`studio/scheduling/agent-scheduler-design.md`). Check `studio/scheduling/agent-status.json` (or the example file, if no live status file exists yet) for current availability before assigning - do not assign to an agent whose quota is already `exhausted`.

The scheduler recommends; it does not dispatch. The human creator makes the final call, especially for anything above `risk_level: low` or touching `hand_authored`/`locked` content.

## 6. Review Output

When the assigned agent returns a deliverable, read it before running any tooling against it. Confirm:

- It matches the work order's `Deliverables` and `Acceptance Criteria` - not a superset or a subset.
- It cites its authoritative sources by path, not by paraphrase (`bridges/atlas/implementation-handoff.md`'s "point, don't paraphrase" rule).
- It reports formatting was preserved, per `studio/immutable-formatting-rule.md`'s Agent Reporting Requirement.
- If it is a `TheLastSwordProtocol-Game` implementation artifact, it names which AtlasStudio implementation contract it executed, per `lessons-learned.md`'s standing practice recommendation.

## 7. Validate

Run the automated checks that apply to what changed:

```bash
python3 tools/atlas_format/format_guard.py --check
python3 tools/atlas_graph/validate_graph.py   # if graph facts changed
```

For `TheLastSwordProtocol-Game` implementation work, re-run the engine bridge's own round-trip and route-audit tooling (`rpgmakerLSP`) **against the artifact that will actually ship**, not an earlier scaffold - this is the specific gap `pipeline-gap-analysis.md` found in the Ashford Shop build, where validation only ever covered an earlier version.

A build that fails validation does not proceed to Playtest. Send it back to the assigned agent with the specific failure, or reassign per the Agent Scheduler's fallback chain.

## 8. Playtest

Validation confirms structural correctness; playtest confirms it plays right. For any player-facing change, a human actually plays the affected screen or system before an acceptance decision is made. See `PLAYTEST_AND_ACCEPTANCE.md` for what evidence a playtest pass must produce.

Do not skip this step because a build "looks finished." `lessons-learned.md`'s central finding is that a good-looking artifact is not the same as an accepted one, and nothing catches that gap except an actual playtest.

## 9. Accept or Reject

This is a recorded human decision, not an inferred state. Use `PLAYTEST_AND_ACCEPTANCE.md`'s four outcomes (Accepted, Accepted with Notes, Rejected, Deferred) and file the evidence and documentation each outcome requires. A map's ownership state (`generated` / `agent-drafted` / `human-edited` / `hand-authored` / `locked`) is never treated as a stand-in for this decision - `hand_authored` means a human pass happened, not that it was accepted.

### Successful Path

Accepted or Accepted with Notes → proceed to Commit with the acceptance decision recorded → the work order moves to `accepted`.

### Rejected Path

Rejected → do **not** commit the rejected artifact as final. Record the rejection (evidence, reason, required follow-up) per `PLAYTEST_AND_ACCEPTANCE.md`, open or update the work order to `needs_revision`, and route the follow-up work back through Step 4 (Select Work) on a future day - or, if the fix is small and the same session has capacity, immediately back through Step 5 (Assign Agent). The Ashford Shop automated-generation rejection (`BUILD-0043`, walked through in `reports/operations/atlasstudio-day-in-the-life.md`) is the concrete precedent: a "NO GO" playtest verdict stopped an automatically generated map from shipping and routed production toward a manual rebuild instead, rather than silently patching the rejected version forward.

## 10. Commit

Commit only what was actually accepted (or explicitly accepted-with-notes). Follow each repository's own commit discipline - `TheLastSwordProtocol-Game`'s `map_ownership.json` ledger rules, `AtlasStudio`'s Immutable Formatting Rule, `TheLastSwordProtocol-Atlas`'s own work-order process. Never commit across repository boundaries in a way that implies one repository's change authorized another's - each repository's own history is its own record.

## 11. Update Production Status

Close the loop before ending the day:

- Update the work order's `status` field (per `studio/workflow.md`'s lifecycle: Proposed → Approved → Assigned → In Progress → Submitted → QA Review → Needs Revision → Accepted → Closed).
- If the decision was Rejected or Deferred, make sure that is visible in the work order status, not just in a report only you have read.
- If a Decision Record was warranted (any map moving toward `locked`, any governance-relevant call), file it per `studio/governance/decision-record-template.md`.
- Re-run Studio Health at the end of the day if enough changed that tomorrow's Step 2 should start from a fresh baseline.

## Review

This document should be revisited if the Work Order Router or Agent Scheduler moves from recommendation-only to any form of automated dispatch, if a fourth repository is introduced, or if production experience shows a step here is consistently skipped or reordered in practice - per `studio/STATUS.md`'s rule that new AtlasStudio process should originate from demonstrated production experience, not speculation.
