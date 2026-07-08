# User Experience

## Purpose

`ATLAS_CLI_SPEC.md` specifies what each command does. This document describes what it feels like to use them - the six example requests this work order's brief names, in the words a Production Director would actually say, and exactly how `atlas` responds to each. It exists so a developer unfamiliar with AtlasStudio can read one document and understand the intended day-to-day experience, not just the command syntax.

Every response shown below is produced by `atlas ask`'s deterministic interpretation table (`ATLAS_CLI_SPEC.md`), never by a call to an external model. `ask` recognizes a request's *shape*, not its exact wording - the phrasings below are representative, not the only strings that work.

## "I want to continue Journey I."

This is exactly the shape `studio/operations/REPOSITORY_DECISION_TREE.md` and `reports/operations/atlasstudio-day-in-the-life.md` already flag as too broad to act on directly - it names no location, defect, or content area. `atlas ask` does not guess at what "continue" means; it responds by narrowing, not by picking something:

```text
$ atlas ask "I want to continue Journey I"

This is broad enough that I can't pick a single next step for you.
Here's what's true right now:

Interpreted as: atlas today
```

`atlas today` runs immediately (it's read-only), showing repository state, Studio Health, and the router's pending items. The response ends by pointing at `atlas next` for the Planning Engine's top recommendation, and reminding the director that a concrete ask - a location, a defect, a specific screen - is what actually resolves through the Repository Decision Tree, the same narrowing conversation `atlasstudio-day-in-the-life.md` already walks through by hand.

## "I have one hour tonight."

A time-boxed request. `ask` maps this to `atlas next`, filtered to recommendations that are actually scoped for a single short session:

```text
$ atlas ask "I have one hour tonight"

Interpreted as: atlas next (filtered: risk_level low or medium, single-session scope)

Next: "Wire the Ashford Shop cabinet examine event's second flavor-text variant"
  Priority: should-do
  Recommended agents: codex
  Evidence:
    - Flavor text already exists in ATLAS-STY-010; only the trigger wiring is unbuilt.
    - Small, single-file RPG Maker event edit against an existing map.
```

The filter is advisory, not a new Planning Engine feature - it re-ranks the same recommendation list `atlas planner` already produces, preferring items whose evidence and recommended agent suggest a short, contained edit over a multi-day architecture item. If nothing in the current backlog fits a short session, `ask` says so plainly (`atlas next` returns exit `9`, "nothing found") rather than stretching a big item to look small.

## "What should Codex work on?"

An agent-specific question. `ask` maps this directly to `atlas next --agent codex`:

```text
$ atlas ask "What should Codex work on?"

Interpreted as: atlas next --agent codex

Next: "Define RPG Maker implementation targets for Ashford Vale"
  Priority: must-fix (80/100)
  Recommended agents: codex, claude-code
```

This is read-only and runs immediately - no confirmation needed, since it recommends rather than assigns. Per `studio/operations/AGENT_USAGE_GUIDE.md` and the Agent Scheduler's scoring model, the answer still respects Codex's actual current availability (`studio/scheduling/agent-status.json`); if Codex is `exhausted`, the response says so and names the fallback agent instead of recommending work to an agent that can't take it.

## "What's blocking production?"

`ask` maps this to `atlas today`, but reads its output back specifically for blockers rather than the full snapshot:

```text
$ atlas ask "What's blocking production?"

Interpreted as: atlas today

Blocking:
  - REQ-IMPLEMENT-IMP-HOM-019 is pending_approval - needs a human approval decision before Codex can act on it.

Not blocking:
  - Studio Health: Healthy (0 structural errors).
  - No blocked_ambiguous items.
  - All three repositories clean.
```

This is the daily-loop question `DAILY_WORKFLOW.md` Step 3 (Review Router Recommendations) already asks by hand; `ask` just answers it in one line instead of requiring the director to read the full router log and mentally filter it.

## "Prepare a Claude work order."

A write-shaped request - this is where `ask` stops short of acting on its own interpretation. It drafts the exact command it would run and requires confirmation:

```text
$ atlas ask "Prepare a Claude work order for extending the Planning Engine's scoring"

Interpreted as:
  atlas work create --title "Extend Planning Engine scoring" --project atlasstudio \
    --purpose "Add a technical-debt weighting dimension to the Planning Engine." \
    --capability architecture-review --risk-level medium

This would create a new file. Not run without confirmation.
Run again with --yes, or run the command above directly.
```

`ask` chose `architecture-review` and a `claude-code`-shaped classification because "Claude" plus "extending the Planning Engine" matches the same `production_orchestration` signals `studio/orchestration/work-order-router.md` already uses (scope names AtlasStudio's own tooling). It never silently writes a work order on the strength of a natural-language guess, per `ATLAS_CLI_SPEC.md`'s "Non-Goals" - a draft work order is easy to review and cheap to discard; a silently created one is not.

## "Review today's progress."

`ask` maps this to bare `atlas review` - the day-level rollup, not `atlas work review`'s single-item check:

```text
$ atlas ask "Review today's progress"

Interpreted as: atlas review

Work orders updated today:
  WO-0031  accepted        "Wire Ashford Shop cabinet flavor text"
  WO-0032  needs_revision  "Automated landmark decoration pass - REJECTED"

Studio Health: Healthy
Router: 0 pending_approval, 0 blocked_ambiguous
```

This is `DAILY_WORKFLOW.md` Step 11 (Update Production Status) turned into a single readback at the end of a session - see `reports/interface/daily-cli-walkthrough.md` for the full session this example is drawn from, including how `WO-0031` and `WO-0032` each got to their recorded outcome via `atlas playtest record`.

## What Ties These Together

Every example above resolves to one of two shapes: a read-only situational-awareness command that `ask` just runs (`today`, `next`, `review`), or a write-shaped command that `ask` only ever proposes (`work create`, and by extension `dispatch` and `playtest record`, which `ask` does not attempt to interpret toward directly since they require evidence and approval `ask` cannot supply on a user's behalf). No example above required the director to remember whether the underlying tool was `doctor.py`, `planner.py`, or `router.py` - that is the success criterion this work order's brief states directly: `atlas` becomes the single conceptual entry point, and the six individual tools underneath it become an implementation detail a director no longer needs to hold in their head.
