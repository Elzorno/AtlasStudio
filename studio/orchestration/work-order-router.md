# Work Order Router

## Purpose

AtlasStudio, `TheLastSwordProtocol-Atlas`, and `TheLastSwordProtocol-Game` are three separate repositories with three separate, already-defined authorities (`studio/governance/repository-authority.md`). Today, a human or agent creating a new work order must already know which of the three repositories should receive it, and must place it there by hand. This document designs a router that takes a single work order request and determines - deterministically and explainably - which repository owns it, without ever performing the write itself and without ever redefining who owns what.

This is a design document. It does not implement the router. Per WO-0011's and WO-0019's precedent, the implementation is scoped separately for Codex (see "Implementation Plan for Codex" below).

## Relationship to Existing Governance

This router does not introduce new ownership rules. It operationalizes rules that already exist:

- `studio/governance/repository-authority.md` defines what each repository owns and states the Change Flow Between Repositories: canon changes happen in `TheLastSwordProtocol-Atlas`, game asset/map/database changes happen in `TheLastSwordProtocol-Game`, and AtlasStudio may *propose* but must not *write* into either sibling repository.
- `bridges/atlas/implementation-handoff.md` (WO-0019) already establishes "point, don't paraphrase" for routing imported Atlas work to a provider. This router extends the same discipline one level up: routing a *new* work order request to the correct *repository*, before any provider is even chosen.
- `studio/orchestration/capability-based-orchestration.md` already establishes that the orchestrator recommends and a human approves; this router inherits that rule rather than introducing a competing one.

If any rule below appears to conflict with `repository-authority.md`, `repository-authority.md` wins - this document is downstream of it, not a peer.

## The Problem This Solves

Without a router, three failure modes recur:

1. A canon request (a new quest, a character detail, a location) gets drafted inside AtlasStudio because that is the repository the requester had open - silently recreating the exact conflict `WO-0018` had to unwind.
2. A game-implementation request (edit a map, wire an event) gets dispatched straight to `TheLastSwordProtocol-Game` without going through Atlas's implementation-packet process, bypassing `map_ownership.json` and Atlas's own authority over that content.
3. A genuinely ambiguous request (spanning canon and implementation, or not clearly belonging to any one repository) gets guessed at instead of stopped, and the guess is wrong often enough to matter.

The router's job is to classify a request, map it to exactly one target repository (or to "blocked, needs a human"), and record that decision - never to make the decision silently or irreversibly.

## Classification Model

Every incoming work order request is classified into exactly one of five categories.

| Classification | Definition | Owning Repository |
|---|---|---|
| `canon` | Story, characters, world lore, dialogue, quests, locations, or gameplay philosophy specific to a game project | `TheLastSwordProtocol-Atlas` |
| `game_implementation` | Direct edits to a game's runtime project - map files, database entries, final assets | `TheLastSwordProtocol-Game`, gated by explicit approval |
| `production_orchestration` | AtlasStudio's own methodology, tooling, scheduling, governance, planning, or documentation - project-agnostic Atlas Core work | AtlasStudio |
| `cross_repository_bridge` | Import, synchronization, or handoff work that *describes* a relationship between repositories but writes into neither sibling repository | AtlasStudio (`bridges/`), read-only toward siblings |
| `ambiguous` | Does not cleanly resolve to exactly one of the above, or resolves to more than one | None - routing stops |

### Signals Used For Classification

The router classifies using the same evidence a human already has when filing a work order: the request's stated capabilities, its scope description, and which repository's owned content it names. No classification may rely on which repository the requester happens to be working in - that is the exact bias that caused the WO-0018 conflict.

| Signal | Examples | Points toward |
|---|---|---|
| `required_capabilities` contains `canon-design`, `creative-writing`, `final-canon` | "design a new sidequest", "write dialogue" | `canon` |
| Scope names story/character/location/lore nouns owned per `repository-authority.md` | "protagonist", "Ashford Village lore", "quest reward" | `canon` |
| `required_capabilities` contains `rpg-maker-json` and scope names a specific map, tileset, or database file inside `TheLastSwordProtocol-Game` | "wire the Map003 shop transfer event" | `game_implementation` |
| `required_capabilities` contains `architecture-review`, `schema-design`, `graph-analysis`, and scope names AtlasStudio's own `tools/`, `studio/`, `schemas/`, or the Atlas Graph | "extend the Planning Engine's scoring" | `production_orchestration` |
| Scope explicitly describes importing, diffing, or handing off content that already lives in a sibling repository, without proposing new content | "build a handoff contract for IMP-HOM-020" | `cross_repository_bridge` |
| Scope names content owned by more than one repository, or does not name any owned content clearly enough to match a single row above | "fix the village", "improve the game" | `ambiguous` |

A request may match more than one signal row. If every matched row agrees on classification, proceed. If matched rows disagree (e.g., a request asks to both invent a new quest reward *and* wire its map event), the request is `ambiguous` by definition - see Safety Rules. The router does not average or pick a majority; a split verdict is a stop condition, not a tiebreak.

## Routing Rules

1. **Canon work goes to `TheLastSwordProtocol-Atlas`.** The router never authors canon content itself. It produces a routing record pointing the requester to file the request through Atlas's own work-order process (per `repository-authority.md`'s Change Flow), the same way `bridges/atlas/implementation-handoff.md` already refuses to paraphrase Atlas content.
2. **Production and orchestration work goes to AtlasStudio.** This includes the router's own future maintenance, per `repository-authority.md`'s "Retains" list of project-agnostic tooling.
3. **Game implementation work goes to `TheLastSwordProtocol-Game` only when explicitly approved.** The default routing outcome for `game_implementation` is not a direct write - it is an AtlasStudio-authored implementation contract (the same shape as `WO-0020`), which itself points at an Atlas implementation packet. A human must separately approve before any agent acts directly against `TheLastSwordProtocol-Game`.
4. **Cross-repository bridge work stays in AtlasStudio's `bridges/` tree**, and is never used as a channel to write into a sibling repository - it documents and points, per WO-0019's "point, don't paraphrase" rule.
5. **Ambiguous work orders stop and request classification.** The router returns `routing_status: blocked_ambiguous` with the specific reason (which signals conflicted, or what information is missing) rather than guessing. See Safety Rules.

## Target Repository / Path Mapping

| Classification | Target Repository | Where it lands |
|---|---|---|
| `canon` | `TheLastSwordProtocol-Atlas` | That repository's own `atlas/workorders/` and `atlas/planning/workorder_queue.json` - AtlasStudio only proposes, per `repository-authority.md`; it does not choose Atlas's internal path. |
| `game_implementation` (proposed, not yet approved) | AtlasStudio | `work-orders/WO-NNNN-*.md`, framed as an implementation contract (`WO-0020` pattern), pointing at the relevant Atlas implementation packet. |
| `game_implementation` (approved) | `TheLastSwordProtocol-Game` | That repository's own runtime project paths, governed entirely by its own `map_ownership.json` and `AGENTS.md` - the router does not choose file paths there. |
| `production_orchestration` | AtlasStudio | `work-orders/WO-NNNN-*.md`, plus whatever `studio/`, `tools/`, or `schemas/` paths the work order's own Allowed Changes section names. |
| `cross_repository_bridge` | AtlasStudio | `bridges/<bridge-name>/`, per the existing `bridges/atlas/` precedent. |
| `ambiguous` | None | Held as `routing_status: blocked_ambiguous`; not filed in any repository until a human reclassifies it. |

## Frontmatter and Schema Proposal

The router needs a small, additive extension to the existing work order frontmatter defined in `studio/work-order-format.md`. All four fields are optional and default conservatively when absent, so every existing work order in this repository remains valid without edits.

```yaml
# Proposed additions to studio/work-order-format.md's frontmatter block
classification: production_orchestration   # canon | game_implementation | production_orchestration | cross_repository_bridge | ambiguous
target_repository: AtlasStudio             # AtlasStudio | TheLastSwordProtocol-Atlas | TheLastSwordProtocol-Game | none
routing_status: routed                     # routed | pending_approval | blocked_ambiguous
requires_explicit_approval: false          # true only for game_implementation direct-write routing
```

Default when these fields are absent: `classification: production_orchestration`, `target_repository: AtlasStudio`, `routing_status: routed` - i.e., every work order filed in this repository before this router existed is treated as already correctly routed to AtlasStudio, since that is where it was filed and accepted. The router is not retroactive; it does not reclassify history.

The machine-readable routing decision itself - the record a future router tool produces each time it classifies a request - is defined by `schemas/work-order-routing.schema.json`, proposed alongside this document. It is a standalone record (analogous to `schemas/agent-status.schema.json`), not a replacement for the frontmatter fields above; the frontmatter is the human-facing summary embedded in the work order, and the schema is the router's own audit trail, keyed by `work_order_id`, so a routing decision can be reviewed independently of the work order document.

## Safety Rules

- **The router must never silently move canon into AtlasStudio.** Any request classified `canon` is never filed as an AtlasStudio work order, drafted as AtlasStudio canon, or added to AtlasStudio's canon graph - even provisionally, even as a "draft to be moved later." It is routed to Atlas's own process, full stop, per `repository-authority.md`.
- **The router must preserve repository authority from `WO-0018`.** It does not reassign ownership of any content area; it only reads the ownership boundaries already recorded in `repository-authority.md` and applies them. If `repository-authority.md` is ever revised, the router's classification table must be revised to match - it has no independent authority of its own.
- **Game implementation is gated, not blocked.** `game_implementation` requests are always routable, but the router's default output is an AtlasStudio-side implementation contract proposal, not a direct write. Direct action against `TheLastSwordProtocol-Game` requires a separate, explicit human approval step recorded in `approved_by` / `approved_at` on the routing record - the same explicit-approval discipline `WO-0020` already used for Ashford Village.
- **Ambiguous work orders stop.** `blocked_ambiguous` is a terminal state until a human supplies the missing classification signal. The router does not default an ambiguous request to any repository, including AtlasStudio - defaulting to AtlasStudio would itself be a silent-canon-leak risk if the ambiguity involved canon content.
- **The router recommends; it does not dispatch.** Per `capability-based-orchestration.md`'s existing design rule, producing a routing record is not the same as creating the work order in the target repository, and it is never the same as writing content into `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game`. A human (or, for AtlasStudio-internal work, AtlasStudio's own accepted process) performs the actual filing.
- **Every routing decision is recorded, not just acted on.** Each decision produces a routing record (`schemas/work-order-routing.schema.json`) with a `rationale` and the `signals_matched` that produced it, so a wrong classification can be audited and corrected rather than silently repeated.
- **The router does not gain write access to sibling repositories as a side effect of existing.** Exactly as stated in `bridges/atlas/implementation-handoff.md`, whatever access model `TheLastSwordProtocol-Atlas` and `TheLastSwordProtocol-Game` already use governs their own writes, independent of anything this router does.

## Worked Examples

1. **"Add a new sidequest where the blacksmith in Ashford Village asks the player to recover a stolen tool."**
   Signals: quest, character (blacksmith), location (Ashford Village) - all canon nouns owned by Atlas per `repository-authority.md`.
   Classification: `canon`. Target: `TheLastSwordProtocol-Atlas`. AtlasStudio does not draft this quest even provisionally.

2. **"Extend the Planning Engine so it can weight technical-debt work orders differently."**
   Signals: `required_capabilities: architecture-review`, scope names `tools/atlas_planner/` (AtlasStudio's own tooling).
   Classification: `production_orchestration`. Target: AtlasStudio, filed as a normal `work-orders/WO-NNNN-*.md`.

3. **"Wire the Ashford Shop's transfer event in Map003 per `IMP-HOM-019`."**
   Signals: `required_capabilities: rpg-maker-json`, scope names a specific `TheLastSwordProtocol-Game` map file, and an already-existing Atlas implementation packet.
   Classification: `game_implementation`. Default target: AtlasStudio, as an implementation contract pointing at `IMP-HOM-019` (the `WO-0020` pattern) with `requires_explicit_approval: true`. It is only routed to `TheLastSwordProtocol-Game` directly once a human sets `routing_status: pending_approval` to approved.

4. **"Build a synchronization report comparing AtlasStudio's imported Atlas entities against Atlas's current export."**
   Signals: describes comparing already-imported content, writes nothing new into either sibling repository.
   Classification: `cross_repository_bridge`. Target: AtlasStudio, `bridges/atlas/`.

5. **"Update the protagonist's backstory to explain the new sidequest."**
   Signals: character/story noun (protagonist, backstory) - canon, regardless of which sidequest prompted it.
   Classification: `canon`. Target: `TheLastSwordProtocol-Atlas`. Flag: this must not be accepted into AtlasStudio's canon graph even as a "just for consistency" edit - `WO-0018` already found and corrected exactly this failure mode.

6. **"Fix the village."**
   Signals: no named repository-owned content area is specific enough to match any single row (could mean a canon detail, a map bug, or an AtlasStudio bridge report).
   Classification: `ambiguous`. Target: none. Routing record states `routing_status: blocked_ambiguous` with rationale "no signal distinguishes canon, implementation, or orchestration scope; request needs a named location, a named defect, and a stated content area before classification."

## Implementation Plan for Codex

Following the `WO-0011` precedent (design work order specifies intent; Codex implements the deterministic tool), a future implementation work order should scope:

1. **`tools/atlas_router/router.py`** - a deterministic classifier, not a model call. It reads a work order's frontmatter (`required_capabilities`, `scope`) and body text, matches it against the signal table above, and emits a routing record matching `schemas/work-order-routing.schema.json`. Ties or missing signals produce `blocked_ambiguous`, never a best-guess default.
2. **CLI shape**: `python3 tools/atlas_router/router.py work-orders/WO-NNNN-*.md --json`, writing (or printing, in a dry-run mode) the routing record. A `--check` mode should exit non-zero when a request classified `canon` or `game_implementation` (unapproved) has already been filed as a plain AtlasStudio production work order - catching a canon-leak after the fact, the same way `format_guard.py --check` catches formatting churn after the fact.
3. **Integration points**: wire `--check` into the same pre-submission review step that already runs `format_guard.py` and `atlas_doctor/doctor.py` (per `WO-0011`'s and `WO-0018`'s verification steps), so misrouted work orders are caught before submission, not after.
4. **Human correction logging**: when a human overrides a routing decision, log the override (original classification, corrected classification, reason) to a plain file under `reports/atlas-router/` for future signal-table tuning. This is a logging step only - the router does not retrain or auto-adjust its own signal table from these logs; any signal-table change is a human-reviewed edit to this document and to `router.py`, mirroring the ADR discipline in `studio/governance/architectural-decision-log.md`.
5. **Non-goals for the implementation**: the tool must not gain filesystem write access to `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` paths, must not auto-create work orders in any repository, and must not attempt natural-language canon judgment beyond the keyword/capability signal table - anything the signal table cannot resolve is exactly what `blocked_ambiguous` is for.

## What This Document Does Not Do

It does not redefine any repository's ownership - `repository-authority.md` remains the sole authority for that. It does not implement the router. It does not grant any agent or tool new write access to `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game`. It does not resolve WO-0020-style implementation contracts on its own judgment; approval remains a separate, explicit human step.

## Review

This document should be revisited if `repository-authority.md` is revised, if a fourth active repository is introduced, or if the future `tools/atlas_router/router.py` implementation finds signal-table gaps that require a documented update here first.
