# Dependency Map - First Playable Hour

## Purpose

This document maps dependencies between the work packages defined in `projects/the-last-sword-protocol/production/work-breakdown.md`, plus external dependencies on canon, tooling, and the RPG Maker bridge. It is the reference for sequencing and for identifying what can run in parallel.

## Dependency Graph

```text
WP-01 Engine Bridge Foundation ─────┬─→ WP-03 Ashford Village Town Build
                                     ├─→ WP-04 Ashford Vale Overworld Build
                                     ├─→ WP-05 Hidden Cave & Sword Shrine
                                     ├─→ WP-06 Glassfield Ruins & First Relay
                                     ├─→ WP-07 Rustshore Dock & Boat Departure
                                     ├─→ WP-09 Monster & Encounter Implementation
                                     └─→ WP-10 Music & Audio Integration (event hooks only)

WP-02 Canon Gap Resolution ─────────→ WP-03 Ashford Village Town Build
                                     └─→ WP-08 NPC & Dialogue Content (Elara's House-linked content only)

WP-05 Hidden Cave & Sword Shrine ───→ WP-06 Glassfield Ruins & First Relay
                                       (sword must exist to fully test ruins gating end-to-end)

WP-06 Glassfield Ruins & First Relay → WP-07 Rustshore Dock & Boat Departure
                                       (departure dialogue gates on the relay-restored flag)

WP-03 Ashford Village Town Build ───→ WP-11 Opening Sequence & Credits Scripting
WP-07 Rustshore Dock & Boat Departure → WP-11 Opening Sequence & Credits Scripting

WP-03, WP-04, WP-05, WP-06, WP-07,
WP-08, WP-09, WP-10, WP-11 ─────────→ WP-12 Consistency & QA Pass

WP-12 Consistency & QA Pass ────────→ WP-13 Milestone Acceptance & Prototype Ship
```

`WP-08` (NPC & Dialogue Content) and `WP-09` (Monster & Encounter Implementation) and `WP-10` (Music & Audio Integration) have no dependency on each other and only a soft dependency on `WP-01` (for final wiring, not for content creation). They can start immediately alongside `WP-01`.

## External Dependencies

### RPG Maker Bridge (Blocking)

`WO-0005` (RPG Maker Bridge Design) is currently `proposed`, not `accepted`, in the production graph. `WP-01` in this breakdown is the work that would complete it. **No engine-specific package (`WP-03` through `WP-07`, `WP-09`, `WP-10` wiring, `WP-11`) can begin real implementation until the bridge exists**, because `studio/workflow.md`'s Engine Bridge Rule requires engine-specific details to live in the bridge, not in core design docs. Content creation that does not require engine wiring (dialogue drafts in `WP-08`, monster design docs in `WP-09`, track sourcing in `WP-10`) can proceed before the bridge lands.

### Canon Gaps (Soft-Blocking)

Two canon gaps are flagged in the milestone document: Elara's House and Old North Road. `WP-02` resolves them. `WP-03` should not be marked complete until `WP-02` lands, since the Opening Sequence beat requires Elara's House as a real location. This is a small, fast package and should not meaningfully delay the schedule if started early.

### Existing Tooling (Non-Blocking, Already Available)

These AtlasStudio tools already exist and require no further work before use:

- `tools/atlas_graph/validate_graph.py`, `query_graph.py`, `diff_graph.py` - graph integrity and change review.
- `tools/atlas_doctor/doctor.py` - project health reporting.
- `tools/atlas_lint/canon_lint.py` - canon QA.
- `tools/atlas_planner/planner.py` - next-work recommendation (useful after this milestone, for Chapter 02 planning).
- `tools/atlas_format/format_guard.py` - formatting-churn detection for all graph JSON edits made while executing this breakdown.
- `studio/scheduling/agent-scheduler-design.md` - the capability/task-class model this breakdown's provider suggestions are drawn from.

### Canon Dependencies (None Blocking)

All core locations, characters, items, and concepts needed for the critical path already exist as canon graph facts (see the milestone document's Canon Basis section). No new canon is required to begin implementation planning; only the two gaps above are needed before full completion.

## Critical Path Through the Dependency Graph

The longest dependency chain that must complete serially:

```text
WP-01 → WP-05 → WP-06 → WP-07 → WP-11 → WP-12 → WP-13
```

`WP-02`, `WP-03`, `WP-04`, `WP-08`, `WP-09`, and `WP-10` all have slack relative to this chain and should be scheduled to fill provider capacity around it, not treated as later add-ons.

## Risk Notes

- If `WP-01` slips, every engine-specific package slips with it. It should be the first package staffed and the first to receive Claude Code's attention per the Agent Scheduler design's architecture routing.
- If `WP-02` is skipped or delayed past `WP-03`'s start, `WP-03` risks building the Opening Sequence against a non-canon placeholder location, creating rework. Flag this explicitly to whoever picks up `WP-03`.
- `WP-06`'s dependency on `WP-05` is about testing/validation, not file-level blocking - ruins map construction can start in parallel with the cave, but end-to-end gating verification cannot happen until the sword exists.
