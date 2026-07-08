# AtlasStudio: A Day in the Life

## Purpose

`studio/operations/DAILY_WORKFLOW.md` describes the daily loop in the abstract. This report walks one realistic day through it end to end, so a new contributor can see the process actually applied rather than only read about it. It is a worked illustration, not a new historical record: where it needs a concrete example of a rejected implementation, it uses the real, already-documented `BUILD-0043` Ashford Shop precedent (`studio/operations/PLAYTEST_AND_ACCEPTANCE.md`); where it needs an example of a successful implementation, it walks a plausible, small, in-scope request through the process without claiming that request was actually filed or built today. No file in `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` is created or changed by this report.

## The Request

The Production Director sits down and says:

> "I want to improve Journey I."

This is exactly the shape of request `studio/operations/REPOSITORY_DECISION_TREE.md` flags as too broad to act on directly - it names no location, no defect, and no single content area. A director walking `DAILY_WORKFLOW.md` correctly does not skip straight to assigning an agent. The first move is to narrow the request enough that the Repository Decision Tree can actually resolve it.

## Start of Day and Studio Health

Before narrowing anything, the day starts where `DAILY_WORKFLOW.md` says it should:

```bash
git -C ../TheLastSwordProtocol-Atlas status --porcelain
git -C ../AtlasStudio status --porcelain
git -C ../TheLastSwordProtocol-Game status --porcelain
python3 tools/atlas_doctor/doctor.py --project the-last-sword-protocol
```

Studio Health comes back clean: no structural graph errors, work orders in a known mix of `accepted`/`proposed`/`submitted`. Nothing here blocks new work today.

## Reviewing Router Recommendations

Next, the existing routing log is checked before drafting anything new:

```bash
cat reports/atlas-router/routing-log.jsonl
```

One relevant entry already exists: a prior request to implement `IMP-HOM-019` (the Ashford Shop packet) is sitting at `routing_status: pending_approval`, classified `game_implementation`, per the router's actual logged history. That is unfinished business from a previous day, not today's "improve Journey I" request - it gets carried forward to Select Work, not conflated with the new ask.

## Narrowing "Improve Journey I"

Talking through the broad request with the Production Director surfaces a concrete, specific ask: *"the Ashford Shop's cabinet examine event should have a second flavor-text variant after the shopkeeper's post-Node-Seven dialogue state triggers, so returning players see something new."*

This is now specific enough to run through the Repository Decision Tree:

- Does it name story, dialogue, or a location? It touches dialogue content, but the *content* of that dialogue is Atlas's canon concern - however, this request is about *wiring an already-approved dialogue variant into an event trigger*, not inventing new dialogue. That distinction matters: if the flavor text itself does not exist yet, the request splits into two - a canon request (write the line) routed to `TheLastSwordProtocol-Atlas`, and an implementation request (wire the trigger) that waits on it.
- For this walkthrough, the flavor text already exists in Atlas's dialogue packet (`ATLAS-STY-010`) but was never wired to the post-Node-Seven state. That makes it cleanly `game_implementation`: a direct edit to an existing `TheLastSwordProtocol-Game` event, governed by an already-existing Atlas source.

Classifying it:

```bash
python3 tools/atlas_router/cli.py wo classify "Wire the Ashford Shop cabinet examine event's second flavor-text variant, gated on the post-Node-Seven switch, per ATLAS-STY-010" --json
```

Result: `classification: game_implementation`, `target_repository: AtlasStudio` (proposed contract first), `requires_explicit_approval: true` - matching `REPOSITORY_DECISION_TREE.md`'s gated branch exactly, since no implementation contract yet exists naming this specific trigger.

## Selecting Work and Assigning an Agent

Two items are now in play: the carried-forward `IMP-HOM-019` item, and the new cabinet-event item. Per `DAILY_WORKFLOW.md`'s Select Work priority order, the `pending_approval` item is handled first - today it gets human approval to proceed as `TheLastSwordProtocol-Game` implementation work, since its contract (`ashford-shop-build-contract.md`) already exists and was already reviewed.

For the new cabinet-event item, `AGENT_USAGE_GUIDE.md`'s quick reference points to Codex: this is `implementation` (a small, already-scoped RPG Maker event edit against an existing map), not `architecture` or `creative_design`. Codex's availability is checked in `studio/scheduling/agent-status.json` before assignment - available, not exhausted. Codex is assigned, with the cited Atlas dialogue packet and the existing `ashford-shop-build-contract.md` as its inputs, per the Work Order Router's "point, don't paraphrase" discipline.

## Reviewing Output and Validating

Codex returns a small, targeted diff: one new event page on the existing cabinet examine event, gated on the same switch check the shopkeeper's own dialogue already uses, with the flavor text quoted verbatim from `ATLAS-STY-010` rather than paraphrased. The submission cites `ashford-shop-build-contract.md` by name in its own note field - the specific practice `reports/production-review/lessons-learned.md` found missing from the original Ashford Shop build, applied correctly this time.

Validation runs before playtest, against the actual current map version:

```bash
python3 tools/atlas_format/format_guard.py --check
```

Clean. The engine bridge's round-trip and route-audit tooling is re-run against the current `Map003.json` - also clean, with a specific finding count rather than a vague pass.

## Playtesting

A human plays the shop after triggering Node Seven, examines the cabinet, and confirms the new flavor text actually appears and reads correctly in context - not just that the event fires. This is the step `production-readiness.md` found completely missing for the original Ashford Shop build; here, it happens before any acceptance claim is made.

## Outcome One: Accepted

The cabinet-event change passes every check in `PRODUCTION_CHECKLIST.md`. Per `PLAYTEST_AND_ACCEPTANCE.md`, this is recorded as **Accepted**: evidence is a real playtest plus a fresh validation run against the shipped version; documentation is a short Decision Record noting the change and its citation of the governing contract; the work order moves to `accepted`; the change is committed in `TheLastSwordProtocol-Game` under its own commit discipline.

## Outcome Two: Rejected

Later the same day, a second, unrelated idea comes up: rather than hand-wire the next screen's decorative detail, try the automatic RPG Maker map generator's "landmark decoration" pass on it, the same tool used earlier in Ashford Shop's history. It is validated with clean round-trip results. But the playtest pass tells a different story - exactly as it did for the real precedent this walkthrough is grounded in.

This is the real `BUILD-0043` case, walked through here as the day's second outcome rather than invented fresh: a human playtest review found that automatically generated map detail produced no meaningful visible runtime improvement, and recorded the verdict plainly:

> "NO GO for automatic final map construction... it is not ready to produce final or near-final maps."

Per `PLAYTEST_AND_ACCEPTANCE.md`'s Rejected outcome: the automatically decorated version is not committed as final; a runtime issue is filed naming the specific failure; the work order is routed to `needs_revision`; and production redirects toward manual, guided map building for that screen instead of retrying the same automated pass unchanged. The day ends with this item still open, correctly, rather than quietly shipped.

## Recording the Day

Both work orders are updated before the session closes:

- The cabinet-event work order: `accepted`.
- The automated-decoration attempt: `needs_revision`, with the rejection reason and the filed runtime issue linked directly in the work order, not left in a report only today's director has read.

Studio Health is checked once more, confirming both status changes are reflected before the day ends.

## How AtlasStudio Evolves

This walkthrough deliberately does not invent a need for new AtlasStudio tooling to make either outcome work - the Router, the Scheduler, the Pattern Library, and the ownership ledger that already exist were sufficient for both the accepted and the rejected path. That is intentional, and it is the standing rule this document closes on:

**Future AtlasStudio features should originate from real production experience, not speculative architecture.**

`studio/STATUS.md` already states this as a governing principle - AtlasStudio Core is frozen at v1.0.0, and new features should be added only when they directly improve production or solve a demonstrated implementation problem. `reports/production-review/lessons-learned.md` reached the same conclusion from a different direction: the newest parts of AtlasStudio's architecture (Pattern Resolution, Pattern-Aware Contracts) were, at the time of that review, well-designed but unproven, because they had not yet governed a real build. The fix was never to design more speculatively - it was to run one more real production cycle and let the results say what, if anything, needed to change.

This day-in-the-life exists for the same reason. If a future day's actual experience reveals that a step in `DAILY_WORKFLOW.md` is consistently skipped, that `PLAYTEST_AND_ACCEPTANCE.md`'s four outcomes are missing a fifth real case, or that the Repository Decision Tree fails to resolve some recurring request cleanly, that is the correct trigger for revising this operations manual - not a hypothetical gap noticed in the abstract. AtlasStudio's operating documents should stay downstream of what actually happens at the keyboard, the same way `repository-authority.md` stays downstream of an actual conflict it had to correct, and the Pattern Library stays downstream of actual sample-map evidence rather than invented rules.

## References

- `studio/operations/DAILY_WORKFLOW.md`
- `studio/operations/PRODUCTION_CHECKLIST.md`
- `studio/operations/AGENT_USAGE_GUIDE.md`
- `studio/operations/PLAYTEST_AND_ACCEPTANCE.md`
- `studio/operations/REPOSITORY_DECISION_TREE.md`
- `reports/production-review/ashford-shop-production-review.md`, `lessons-learned.md`
- `rpgmakerLSP/reports/atlas-import/build-0043-guided-map-runtime-review.md`
- `studio/STATUS.md`
- Created by `work-orders/WO-0029-atlasstudio-daily-operations.md`
