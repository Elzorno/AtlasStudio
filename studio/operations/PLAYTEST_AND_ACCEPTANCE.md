# Playtest and Acceptance

## Purpose

`studio/governance/production-readiness.md` found Playtesting to be AtlasStudio's single `Not Ready` criterion, and `reports/production-review/lessons-learned.md` found that "acceptance is a recorded decision, not an inferred state" is the standing practice this project most needs going forward. This document formalizes that practice: it defines the four possible outcomes of a playtest/acceptance pass, and for each, the evidence, documentation, and follow-up required before a work item can be considered closed.

This document does not create a new gate. `bridges/rpg-maker-mz/passability-rule.md`'s "Human Playtest Still Required" and `ashford-village-contract.md`'s Section 11 already require a human playtest pass; this document is what that pass must actually produce.

## The Four Outcomes

### Accepted

The work is done. Nothing further is required of it before it can move toward `locked` ownership state (per `bridges/rpg-maker-mz/ownership-model.md`) or be treated as shipped content.

**Required evidence:**
- A human actually played the affected screen or system, not merely reviewed the artifact by inspection.
- Automated validation (round-trip, route-audit, or the relevant tooling for the change type) was run against the exact artifact version being accepted - not an earlier scaffold.
- The artifact matches its governing work order's or implementation contract's `Acceptance Criteria` in full.

**Required documentation:**
- A Decision Record (`studio/governance/decision-record-template.md`) for any map or system moving toward `locked` ownership state.
- The work order's `status` updated to `accepted`.
- If the artifact is a `TheLastSwordProtocol-Game` implementation, its embedded note or accompanying Audit Summary (`bridges/rpg-maker-mz/handoff-format.md`) states plainly that the current version is accepted - not merely that a pass occurred.

**Required follow-up:** None, beyond the ordinary commit and status-update steps in `DAILY_WORKFLOW.md`.

### Accepted with Notes

The work is done and may ship, but carries specific, bounded issues worth tracking - cosmetic gaps, minor deviations from a pattern's recommendation tier, or deferred polish that does not block the player experience.

**Required evidence:** Same as Accepted.

**Required documentation:**
- Same Decision Record requirement as Accepted, plus an explicit list of the notes - each one specific and checkable, not a vague "could be better."
- Each note should state whether it is tracked as a future work item or accepted permanently as-is.

**Required follow-up:** Each note either becomes a scoped future work order or is explicitly marked as a permanent, accepted trade-off. A note left unresolved and untracked is functionally the same failure `lessons-learned.md` already found: a good-looking artifact treated as fully settled when it is not.

### Rejected

The work does not meet the bar and must not ship in its current form.

**Required evidence:**
- A specific, recorded reason the work failed - grounded in an actual playtest or validation result, not a general impression. "NO GO for automatic final map construction" (`BUILD-0043`, see Case Study below) is the model: a stated verdict backed by a specific runtime finding, not just a feeling that something was off.
- Whichever runtime issue, validation failure, or design-pattern departure caused the rejection, filed as its own record (e.g. `rpgmakerLSP`'s `runtime-issues/RT-*` convention) so the reason is traceable later.

**Required documentation:**
- The work order's `status` moved to `needs_revision`, with the rejection reason stated in the work order itself, not only in a separate report a future reader might not find.
- If the rejection reveals a systemic issue (a tool, a pattern, or a process producing bad results repeatedly, not just one bad build), that finding is escalated to `studio/governance/production-readiness.md`'s backlog rather than only fixed locally.

**Required follow-up:**
- The rejected artifact is never committed as final, and never left ambiguous about whether it is the current accepted state - `map_ownership.json` or the equivalent ledger must reflect that it is not.
- A follow-up work item is opened (or an existing one revised) addressing the specific rejection reason, routed back through `DAILY_WORKFLOW.md` Step 4.
- If the rejection was caused by a specific tool or automated process (as in the Case Study below), that process is paused or scoped down for the affected content type until the reason for rejection is addressed - not silently retried unchanged.

### Deferred

The work is not being judged yet - it is real, in-flight, and awaiting either more evidence, a scheduling decision, or a human's availability, and should not be read as either accepted or rejected in the meantime.

**Required evidence:**
- A stated reason the decision is deferred (missing playtest, awaiting a dependent work order, awaiting Production Director availability) - not silence.
- The artifact's own note or accompanying documentation states its status honestly as pending, exactly as `Map003.json`'s embedded note does ("pending Production Director acceptance (not final accepted)") - this is the interim mechanism for signaling in-progress-vs-accepted until the ownership model itself gains a dedicated state (`production-readiness.md`, Traceability finding).

**Required documentation:**
- The work order's `status` remains at whatever stage reflects reality (`submitted`, `qa_review`) - never advanced to `accepted` to make the day's status look more finished than it is.
- What specifically is being waited on, and who or what resolves it.

**Required follow-up:**
- The deferred item is re-checked at the start of a future `DAILY_WORKFLOW.md` Step 2 (Check Studio Health) or Step 3 (Review Router Recommendations) - it does not simply age silently until someone happens to remember it.
- A Deferred item that has aged past a reasonable point (the Production Director's judgment call, not a fixed rule) should be escalated rather than left open indefinitely.

## Case Study: The Ashford Shop Rejection

This case study traces one real, evidenced production thread through two of the four outcomes above - a genuine Rejected decision, followed by the same content's current, ongoing Deferred status - because both actually happened and both are fully documented in this project's history.

### The Rejection: Automated Map Construction

Early in Ashford Shop's production, `rpgmakerLSP`'s automatic RPG Maker map generator produced a blueprint-generated, then decoratively "landmark-enhanced," version of `Map003.json` (`BUILD-0025`, `BUILD-0026`, decorated further on `2026-07-05`). Automated round-trip and route-audit tooling passed cleanly against these versions. But automated validation only confirms structural correctness - it cannot confirm the room reads right to an actual player.

A human playtest review (`BUILD-0043`, `rpgmakerLSP/reports/atlas-import/build-0043-guided-map-runtime-review.md`) found the opposite of what the clean audits suggested: the automatically generated map detail produced no meaningful visible runtime improvement. The review's recorded verdict:

> **NO GO for automatic final map construction.** ... The automatic RPG Maker map generator remains useful for scaffolding, transfer/event placement, and validation, but it is not ready to produce final or near-final maps.

This is a real Rejected outcome by the definition above:

- **Evidence:** an actual human playtest pass, not an inspection - and a specific, filed runtime issue (`RT-20260705-005-generated-map-detail-not-visible.md`) naming exactly what failed.
- **Documentation:** the verdict was recorded directly in `BUILD-0043`'s own report, in plain language, not buried in a status field.
- **Follow-up:** production for Ashford Shop (and Home Island generally) was redirected away from automatic final map construction and toward manual, guided map building from Atlas's own SVG layout guides - exactly the "pause or scope down the responsible process" requirement above. This is why Ashford Shop went through a genuine hand-authored rebuild pass at all, rather than shipping the automatically generated version.

### The Current Deferred Status

The hand-authored rebuild that followed (`data/Map003.json`, final commit `2026-07-08`, `01692cb`) is good work by direct inspection - real dialogue for both story states, a working shop command, correct collision - but it is not yet an Accepted outcome. Its own embedded note says so directly: *"polish submitted, pending Production Director acceptance (not final accepted)."* No playtest record specific to this final version exists in any of the three repositories (`reports/production-review/ashford-shop-production-review.md`, Stage 8).

This is a textbook Deferred case, not a silent Accepted one:

- **Evidence:** the note itself states the pending status; no playtest evidence exists yet either way.
- **Documentation:** the map_ownership.json ledger currently reads `hand_authored`, which - per this document's own Deferred requirements - must not be read as a stand-in for acceptance. `hand_authored` means a human/guided pass has occurred, not that it was accepted (`AGENTS.md` in `TheLastSwordProtocol-Game`; `ashford-shop-production-review.md`, Stage 6).
- **Required follow-up:** a human playtest pass against the current `Map003.json`, followed by an explicit Accept/Reject/Accepted-with-Notes decision and a Decision Record - the single highest-priority backlog item in `studio/governance/production-readiness.md`.

The lesson this case study exists to carry forward: a rejection can be real, evidenced, and correctly acted on (as the automated-generation NO GO was) while the very next stage of the same content's history quietly drifts into an unrecorded, assumed-accepted state if nobody applies this document's Deferred requirements to it. Treat both halves of this case study as one continuous discipline, not two unrelated stories.

## Review

This document should be revisited once a Decision Record actually closes the Deferred Ashford Shop case above - at which point this case study should be updated to reflect the closed outcome rather than left describing a still-open item indefinitely.
