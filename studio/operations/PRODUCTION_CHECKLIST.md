# Production Checklist

## Purpose

A concise, per-work-item checklist for `DAILY_WORKFLOW.md`'s steps. Print it, copy it into a work order's submission notes, or run through it from memory - its job is to make sure nothing in a work item gets skipped under time pressure, not to add new process beyond what `studio/workflow.md`, `studio/governance/repository-authority.md`, and `studio/orchestration/work-order-router.md` already require.

Use one copy of this checklist per work item, not per day - a day may close several of these.

## Checklist

```text
□ Repository confirmed
    The work item's target repository (TheLastSwordProtocol-Atlas,
    AtlasStudio, or TheLastSwordProtocol-Game) is named explicitly,
    per REPOSITORY_DECISION_TREE.md. Not "probably AtlasStudio because
    that's what's open."

□ Authority confirmed
    The content area this work item touches is actually owned by the
    confirmed repository, per studio/governance/repository-authority.md.
    Canon nouns (story, character, quest, lore, location) never resolve
    to AtlasStudio, even provisionally.

□ Work order exists
    A work order (or, for canon work, an Atlas-side work order/decision
    record) exists in the target repository's own process before any
    agent starts producing a deliverable. No work item proceeds on a
    verbal request alone.

□ Agent assigned
    An agent (or the human creator) is assigned per AGENT_USAGE_GUIDE.md
    and studio/scheduling/agent-scheduler-design.md, with current
    availability checked, not assumed.

□ Validation completed
    Automated checks appropriate to the change have been run against the
    artifact that will actually ship - not an earlier scaffold. For
    TheLastSwordProtocol-Game changes, this includes format_guard.py
    --check and the engine bridge's round-trip / route-audit tooling.

□ Playtest completed
    For any player-facing change, a human has actually played the
    affected screen or system, per PLAYTEST_AND_ACCEPTANCE.md. Skipped
    only when the work item is explicitly non-player-facing.

□ Acceptance decision recorded
    One of Accepted / Accepted with Notes / Rejected / Deferred is
    recorded, per PLAYTEST_AND_ACCEPTANCE.md, with its required evidence
    and documentation - not inferred from a ledger state or a
    good-looking artifact.

□ Commit completed
    Only accepted (or explicitly accepted-with-notes) work is committed
    as final, following the target repository's own commit and
    ownership-ledger discipline. The work order's status field reflects
    the actual outcome, including Rejected or Deferred.
```

## Notes

- If any box cannot be checked, the work item is not done - it is at whichever step first failed, and should be routed back through `DAILY_WORKFLOW.md` from that point, not forced forward.
- "Repository confirmed" and "Authority confirmed" are listed separately on purpose: confirming *where* something should go is not the same act as confirming *that the target repository actually owns that content area*. Both have failed independently in this project's history (`reports/governance/repository-conflict-analysis.md`).
- This checklist does not replace a work order's own `Acceptance Criteria` - it is a process gate that sits around them, not a substitute for them.

## Review

This document should be revisited if `DAILY_WORKFLOW.md`'s step sequence changes, or if production experience shows a checklist item is consistently unclear or unenforceable in practice.
