# Daily CLI Walkthrough

## Purpose

`studio/interface/ATLAS_CLI_SPEC.md`, `COMMAND_REFERENCE.md`, `INTERACTIVE_SHELL.md`, and `USER_EXPERIENCE.md` describe the unified `atlas` command in the abstract. This report walks one complete production session through it end to end, typed command by typed command, so a new contributor can see the interface actually used rather than only read its specification. It is a worked illustration over the unified CLI, in the same spirit as `reports/operations/atlasstudio-day-in-the-life.md` - and it reuses that report's grounding discipline exactly: where a rejected-implementation example is needed, it uses the real, already-documented `BUILD-0043` Ashford Shop precedent rather than inventing a new failure; where an accepted-implementation example is needed, it walks a plausible, in-scope request through the process and says so plainly, rather than implying a commit was actually made today. No file in `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` is created or changed by this report, and no `atlas` command shown here has been run against a real implementation - `atlas` does not exist as code yet (`ATLAS_CLI_SPEC.md`'s Status section).

This walkthrough assumes the future `atlas` entrypoint `ATLAS_CLI_SPEC.md` specifies already exists. Every command shown is written in that target form.

## Start of Day

```text
$ atlas

AtlasStudio v1.0

Project:
The Last Sword Protocol

Studio Health:
Healthy

Journey:
I

atlas>
```

The Interactive Shell (`INTERACTIVE_SHELL.md`) opens with a clean banner. The director runs the full snapshot before doing anything else, per `studio/operations/DAILY_WORKFLOW.md` Steps 1-3:

```text
atlas> today

AtlasStudio - Today (2026-07-08)

Repositories:
  TheLastSwordProtocol-Atlas   clean
  AtlasStudio                  clean
  TheLastSwordProtocol-Game    clean

Studio Health: Healthy (0 structural errors, 8 work orders: 3 accepted, 4 proposed, 1 submitted)

Router: 1 pending_approval, 0 blocked_ambiguous
  - REQ-IMPLEMENT-IMP-HOM-019 (game_implementation, pending_approval)

Top recommendation: "Define RPG Maker implementation targets for Ashford Vale" (must-fix, 80/100)
```

Exit code `0` - nothing here needs urgent attention, but there is one carried-forward item (`IMP-HOM-019`, pending approval from a prior day) that Step 4 (Select Work) must handle before anything new.

## Narrowing a Broad Request

The director's actual starting instruction today is the same broad one `atlasstudio-day-in-the-life.md` already worked through by hand:

```text
atlas> ask "I want to improve Journey I"

This is broad enough that I can't pick a single next step for you.
Interpreted as: atlas today
[today's report reprinted]

Run `atlas next` for a ranked recommendation, or narrow this to a
specific location, defect, or content area.
```

Talking it through narrows the request to something concrete: *"the Ashford Shop's cabinet examine event should show a second flavor-text variant after the shopkeeper's post-Node-Seven dialogue state triggers."* The flavor text already exists in Atlas's dialogue packet `ATLAS-STY-010`; only the event wiring is unbuilt. Per `studio/operations/REPOSITORY_DECISION_TREE.md`, that makes it `game_implementation` against an existing map, governed by an already-existing Atlas source - not a canon request.

## Routing

```text
atlas> route "Wire the Ashford Shop cabinet examine event's second flavor-text variant, gated on the post-Node-Seven switch, per ATLAS-STY-010"

Classification: game_implementation
Target repository: AtlasStudio (pending_approval)
Signals matched:
  - required_capabilities contains rpg-maker-json; scope names Map003 and an existing Atlas dialogue packet
Scheduler recommendation (advisory=True): agent.codex (score 14)
```

Exit code `0` (`routed`/`pending_approval`, not `blocked_ambiguous`). This matches `REPOSITORY_DECISION_TREE.md`'s gated branch exactly: no implementation contract yet names this specific trigger, so the default output is a proposed AtlasStudio-side contract, not a direct write.

## Selecting Work and Assigning an Agent

Two items are now in play: the carried-forward `IMP-HOM-019` item from `atlas today`, and the new cabinet-event item. Per `DAILY_WORKFLOW.md`'s Select Work priority order, the already-`pending_approval` item is handled first - its contract (`ashford-shop-build-contract.md`) already exists and was already reviewed, so today it receives human approval to proceed:

```text
atlas> dispatch work-orders/WO-0020-ashford-village-implementation-contract-from-atlas-handoff.md \
  --approved-by "Christopher Zornes" --approved-at 2026-07-08

Classification: game_implementation
Target repository: TheLastSwordProtocol-Game
Routing status: routed (approved by Christopher Zornes, 2026-07-08)
Action: local implementation contract confirmed; Codex may proceed under ashford-shop-build-contract.md.
```

For the new cabinet-event item, `atlas work create` files it as a proposed AtlasStudio-side implementation contract, per the routing decision above:

```text
atlas> work create --title "Wire Ashford Shop cabinet flavor-text variant" --project atlasstudio \
  --purpose "Wire the second flavor-text variant on the cabinet examine event, gated on the post-Node-Seven switch, per ATLAS-STY-010." \
  --scope-in "New event page on the existing cabinet examine event" \
  --capability rpg-maker-json --risk-level low

Classification: game_implementation
Target repository: AtlasStudio
Routing status: pending_approval
Wrote work-orders/WO-0031-wire-ashford-shop-cabinet-flavor-text.md (status: proposed)
```

Per `studio/operations/AGENT_USAGE_GUIDE.md`'s quick reference, this is `implementation` work against an already-scoped, single-file event edit - Codex's strength, not an architecture task. Codex's availability is confirmed (`available`, not `exhausted`) before assignment.

## Reviewing Output and Validating

Codex returns a small, targeted diff: one new event page on the existing cabinet examine event, gated on the same switch the shopkeeper's own dialogue already checks, with the flavor text quoted verbatim from `ATLAS-STY-010` rather than paraphrased. Its submission note cites `ashford-shop-build-contract.md` by name - the specific practice `reports/production-review/lessons-learned.md` found missing from the original Ashford Shop build.

```text
atlas> work review WO-0031

Deliverables match Allowed Changes:        yes (git diff --stat matches declared paths)
Formatting preserved note present:         yes ("Formatting: preserved existing house style...")
Sources cited by path, not paraphrased:    needs human judgment
format_guard.py --check:                   clean
Sibling repositories untouched:            n/a (this item writes to TheLastSwordProtocol-Game directly, per approval)

3 of 5 checks automated and passing. 1 requires human judgment.
```

The human judgment check passes on inspection - the submission does cite `ashford-shop-build-contract.md` by name and quotes `ATLAS-STY-010` verbatim. Validation runs next, against the artifact that will actually ship, not an earlier scaffold:

```text
atlas> validate

validate_graph.py: 0 structural errors
format_guard.py --check: clean
```

The engine bridge's own round-trip and route-audit tooling (`rpgmakerLSP`) is re-run separately against the current `Map003.json`, also clean.

## Playtesting

A human plays the shop after triggering Node Seven, examines the cabinet, and confirms the new flavor text actually appears and reads correctly in context - not just that the event fires. This is the step `studio/governance/production-readiness.md` found completely missing for the original Ashford Shop build; here it happens before any acceptance claim is made or recorded.

## Outcome One: Accepted

```text
atlas> playtest record --work-order WO-0031 --outcome accepted \
  --evidence "Played the shop after Node Seven; new flavor text confirmed rendering in context; format_guard and round-trip audit both clean against the shipped version."

Recorded: WO-0031 -> accepted
studio/workflow.md status updated: proposed -> accepted
```

**This outcome is illustrative.** No commit against `TheLastSwordProtocol-Game` was actually made by this report - it demonstrates the sequence a real accepted implementation follows, ending with:

```text
$ git -C ../TheLastSwordProtocol-Game commit -am "Wire cabinet examine event second flavor-text variant (WO-0031, ATLAS-STY-010)"
```

## Outcome Two: Rejected

Later the same session, a second, unrelated idea comes up: rather than hand-wire the next screen's decorative detail, try the automatic RPG Maker map generator's "landmark decoration" pass on it - the same tool used earlier in Ashford Shop's history.

```text
atlas> work create --title "Automated landmark decoration pass" --project atlasstudio \
  --purpose "Evaluate automatic landmark decoration for the next interior screen." \
  --capability rpg-maker-json --risk-level medium

Wrote work-orders/WO-0032-automated-landmark-decoration-pass.md (status: proposed)
```

Validation comes back clean - round-trip results pass. But this is the real `BUILD-0043` case, walked through here rather than invented fresh: the human playtest found that automatically generated map detail produced no meaningful visible runtime improvement, and recorded the verdict plainly:

> "NO GO for automatic final map construction... it is not ready to produce final or near-final maps."

```text
atlas> playtest record --work-order WO-0032 --outcome rejected \
  --reason "NO GO for automatic final map construction; no meaningful visible runtime improvement." \
  --evidence "Human playtest against the generated build; round-trip audit was clean, but playtest verdict overrides a clean automated pass."

Recorded: WO-0032 -> needs_revision
studio/workflow.md status updated: proposed -> needs_revision
```

Per `studio/operations/PLAYTEST_AND_ACCEPTANCE.md`'s Rejected outcome: the automatically decorated version is not committed as final; the runtime issue is filed naming the specific failure; production redirects toward manual, guided map building for that screen instead of retrying the same automated pass unchanged.

## Recording the Day

```text
atlas> review

Work orders updated today:
  WO-0031  accepted        "Wire Ashford Shop cabinet flavor text"
  WO-0032  needs_revision  "Automated landmark decoration pass - REJECTED"

Studio Health: Healthy
Router: 0 pending_approval, 0 blocked_ambiguous
```

`atlas review`'s rollup confirms both status changes landed before the session ends, closing `DAILY_WORKFLOW.md` Step 11 without the director having to open either work order file by hand.

## Commit

Only the accepted work is committed, following `TheLastSwordProtocol-Game`'s own commit and `map_ownership.json` ledger discipline:

```text
$ git -C ../TheLastSwordProtocol-Game status --porcelain
 M data/Map003.json
 M map_ownership.json

$ git -C ../TheLastSwordProtocol-Game commit -am "Wire Ashford Shop cabinet flavor-text variant (WO-0031)"
```

The rejected item (`WO-0032`) is never committed as final - `map_ownership.json` reflects that the generated decoration is not the current accepted state, and the work order stays visibly `needs_revision` for a future session to pick up through `atlas today`'s Router summary.

**Successful implementation committed.**

## Session Summary

| Step | Command | Result |
|---|---|---|
| Start of day | `atlas today` | Clean repos, healthy studio, one carried-forward pending item |
| Narrow a broad ask | `atlas ask "..."` | Pointed at `atlas today`/`atlas next`; request narrowed by conversation |
| Route | `atlas route "..."` | `game_implementation`, pending approval |
| Assign (carried-forward item) | `atlas dispatch ... --approved-by` | `WO-0020` approved to proceed |
| Assign (new item) | `atlas work create` | `WO-0031` filed as a proposed contract, Codex assigned |
| Review output | `atlas work review WO-0031` | 3/5 automated checks passed; 1 human judgment check passed on inspection |
| Validate | `atlas validate` | Clean |
| Playtest + accept | `atlas playtest record --outcome accepted` | `WO-0031` -> `accepted` (illustrative) |
| Second item, playtest + reject | `atlas playtest record --outcome rejected` | `WO-0032` -> `needs_revision` (real `BUILD-0043` precedent) |
| Record the day | `atlas review` | Both status changes confirmed |
| Commit | `git commit` (Game repo) | Accepted work only |

## References

- `studio/interface/ATLAS_CLI_SPEC.md`, `COMMAND_REFERENCE.md`, `INTERACTIVE_SHELL.md`, `USER_EXPERIENCE.md`
- `studio/operations/DAILY_WORKFLOW.md`, `PRODUCTION_CHECKLIST.md`, `PLAYTEST_AND_ACCEPTANCE.md`, `REPOSITORY_DECISION_TREE.md`, `AGENT_USAGE_GUIDE.md`
- `reports/operations/atlasstudio-day-in-the-life.md`
- `rpgmakerLSP/reports/atlas-import/build-0043-guided-map-runtime-review.md`
- Created by `work-orders/WO-0030-atlasstudio-interactive-cli.md`
