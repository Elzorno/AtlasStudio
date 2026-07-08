# Atlas Command Reference

Concise, example-driven reference. For full Purpose/Inputs/Outputs/Underlying tools/Exit codes/Failure behavior per command, see `ATLAS_CLI_SPEC.md`. Every invocation below is the target `atlas <command>` form; until a real `atlas` entrypoint exists, replace `atlas` with the long-form script it forwards to per `ATLAS_CLI_SPEC.md`'s "Underlying tools invoked" rows.

## Situational Awareness

```bash
atlas today
```
Start-of-day snapshot: repository cleanliness, Studio Health, Router pending items, top recommendation teaser.

```bash
atlas next
```
The single top Planning Engine recommendation.

```bash
atlas next --agent codex
```
The top recommendation whose `Recommended agents` includes Codex.

```bash
atlas status
```
One-screen Studio Health snapshot (the Interactive Shell's banner).

```bash
atlas doctor
```
Full AtlasStudio health report.

```bash
atlas history --work-order WO-0020
```
Everything recorded about one work order: routing decisions, status transitions, Decision Records.

## Natural-Language Front Door

```bash
atlas ask "Improve Journey I"
```
Too broad to act on directly - `ask` reports that and points at `atlas today` / `atlas next` to narrow it, per `USER_EXPERIENCE.md`.

```bash
atlas ask "What should Codex work on?"
```
Interpreted as `atlas next --agent codex`, run directly (read-only).

```bash
atlas ask "What's blocking production?"
```
Interpreted as `atlas today`, run directly.

```bash
atlas ask "Prepare a Claude work order for extending the Planning Engine"
```
Interpreted as `atlas work create --title "Extend Planning Engine" ...` - printed, not run, until confirmed with `--yes`.

## Routing and Work Management

```bash
atlas route "Wire the Ashford Shop's transfer event in Map003 per IMP-HOM-019"
```
Classification only: `game_implementation`, `AtlasStudio` (proposed contract first), `requires_explicit_approval: true`.

```bash
atlas work create --title "Extend Planning Engine scoring" --project atlasstudio \
  --purpose "Add a technical-debt weighting dimension." --capability architecture-review
```
Classifies and, for an AtlasStudio-owned target, writes a new `proposed` work order.

```bash
atlas work review WO-0023
```
Mechanically checkable pass over a submitted work order: Allowed Changes match, formatting note present, `format_guard.py --check` clean, sibling repositories untouched.

```bash
atlas work list --status pending_approval
```
Every work order currently waiting on human approval.

```bash
atlas work show WO-0020
```
One work order's frontmatter, Purpose, current status, latest router entry, and graph node status.

```bash
atlas dispatch work-orders/WO-0021-cross-repository-work-order-router.md
```
Runs the full routing pipeline, including the real file write or GitHub issue.

## Quality Gates

```bash
atlas review
```
Today's rollup: which work orders changed status, accepted/rejected counts, fresh Studio Health.

```bash
atlas review --work-order WO-0031
```
Alias for `atlas work review WO-0031`.

```bash
atlas playtest record --work-order WO-0031 --outcome accepted \
  --evidence "Played the shop after Node Seven; new flavor text confirmed in context; format_guard clean."
```
Records an Accepted decision; moves the work order's `status` to `accepted`.

```bash
atlas playtest record --work-order WO-0032 --outcome rejected \
  --reason "NO GO for automatic final map construction; no meaningful visible runtime improvement." \
  --evidence "Playtest + round-trip audit against the generated build."
```
Records a Rejected decision; moves the work order's `status` to `needs_revision`.

```bash
atlas validate
```
`validate_graph.py` then, only if clean, `format_guard.py --check`.

## Knowledge and Graph

```bash
atlas graph get work_order.wo_0021
```
A node with its incoming/outgoing edges.

```bash
atlas graph path region.ashford_village work_order.wo_0021
```
Shortest undirected path between two graph nodes.

```bash
atlas planner
```
The full ranked Planning Engine report (alias: `atlas plan`).

## Production Milestones

```bash
atlas release
```
Dry-run readiness report: accepted work since the last milestone, Studio Health gate, `atlas validate` gate.

```bash
atlas release --confirm
```
Prints the exact `studio/STATUS.md` diff for a human to apply - never writes it automatically.

## Interactive Shell

```bash
atlas
```
No arguments launches the Interactive Shell. See `INTERACTIVE_SHELL.md`. Inside the shell, drop the `atlas` prefix - type `today`, `next`, `ask "..."`, and so on directly at the `atlas>` prompt.
