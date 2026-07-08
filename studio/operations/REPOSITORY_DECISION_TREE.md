# Repository Decision Tree

## Purpose

`studio/governance/repository-authority.md` defines what each repository owns. `studio/orchestration/work-order-router.md` defines how a request is classified into one of five categories. This document collapses both into a single decision tree a human can walk by hand in seconds, for the one question that starts every work item: **which repository owns this work?**

This document has no independent authority. If it ever disagrees with `repository-authority.md` or `work-order-router.md`, those documents win - this is a navigation aid over them, not a peer.

## The Tree

```text
Does the request name story, characters, world lore, dialogue,
quests, locations, or gameplay philosophy specific to this game?
  |
  YES --> TheLastSwordProtocol-Atlas (canon)
  |         Never drafted in AtlasStudio, even provisionally.
  |
  NO
  |
  v
Does the request require a direct edit to the game's runtime
project - a map file, database entry, event, or final asset?
  |
  YES --> Is there an approved AtlasStudio implementation contract
  |        or Atlas implementation packet already governing this edit?
  |          |
  |          YES --> TheLastSwordProtocol-Game (approved game_implementation)
  |          |        Proceed directly, under the existing contract.
  |          |
  |          NO  --> AtlasStudio (proposed game_implementation)
  |                   File as an implementation contract (WO-0020 pattern)
  |                   pointing at the governing Atlas packet.
  |                   requires_explicit_approval: true.
  |                   Do not write to TheLastSwordProtocol-Game yet.
  |
  NO
  |
  v
Does the request describe importing, diffing, or handing off content
that already lives in a sibling repository, without proposing new
content of its own?
  |
  YES --> AtlasStudio, bridges/ tree (cross_repository_bridge)
  |         Read-only toward both siblings; documents and points,
  |         never writes into either.
  |
  NO
  |
  v
Does the request concern AtlasStudio's own methodology, tooling,
scheduling, governance, or documentation - project-agnostic Atlas
Core work?
  |
  YES --> AtlasStudio (production_orchestration)
  |
  NO
  |
  v
Does the request name content owned by more than one repository, or
fail to name any owned content area specifically enough to match
one of the branches above?
  |
  YES --> STOP. classification: ambiguous, target_repository: none.
           Do not guess. Do not default to AtlasStudio. Return
           routing_status: blocked_ambiguous with the specific missing
           signal, per work-order-router.md's Safety Rules.
```

## Why The Order Matters

The tree asks about canon first, on purpose. A request that touches both canon and something else (an implementation detail, a tooling need) is `ambiguous` by definition per the Work Order Router - but a request that touches canon *and nothing else ambiguous* must never fall through to a later branch just because a later branch would have been easier to act on immediately. Checking canon first is what prevents the exact failure `WO-0018` found: a canon request getting drafted in AtlasStudio because that was the repository already open.

## Common Examples

| Request | Repository | Why |
|---|---|---|
| "Add a sidequest where the Ashford blacksmith asks the player to recover a stolen tool." | `TheLastSwordProtocol-Atlas` | Quest, character, and location nouns - all canon per `repository-authority.md`. |
| "Update the protagonist's backstory to explain the new sidequest." | `TheLastSwordProtocol-Atlas` | Character/story noun, regardless of which other request prompted it. Never accepted into AtlasStudio's canon graph "just for consistency." |
| "Wire the Ashford Shop's transfer event in Map003 per `IMP-HOM-019`." | AtlasStudio first (implementation contract), then `TheLastSwordProtocol-Game` once approved | `game_implementation`, gated - the default output is a contract, not a direct write. |
| "Extend the Planning Engine so it can weight technical-debt work orders differently." | AtlasStudio | `production_orchestration` - AtlasStudio's own tooling. |
| "Build a synchronization report comparing AtlasStudio's imported Atlas entities against Atlas's current export." | AtlasStudio, `bridges/atlas/` | `cross_repository_bridge` - documents a relationship, writes nothing new into either sibling. |
| "Draft the Daily Operations Manual for AtlasStudio." | AtlasStudio | `production_orchestration` - methodology and documentation, project-agnostic to any one screen or quest. |
| "Fix the village." | None - `blocked_ambiguous` | No named location, defect, or content area specific enough to classify. Needs a named location, a named defect, and a stated content area first. |
| "Make the game better." | None - `blocked_ambiguous` | Same failure mode as above, at a larger scale. |

## What To Do When The Tree Stops You

A `blocked_ambiguous` result is not a dead end - it is a request for more information. Ask (or ask the requester):

1. What specific content area does this touch - a named location, character, system, map, or tool?
2. Is that content area owned by exactly one repository per `repository-authority.md`?
3. If it spans two, is it really one request, or two that should be filed separately?

Only re-run the tree once the answer to (2) is yes for a single repository.

## Review

This document should be revisited whenever `repository-authority.md` or `work-order-router.md`'s classification rules change - it has no independent authority and must never drift out of sync with either.
