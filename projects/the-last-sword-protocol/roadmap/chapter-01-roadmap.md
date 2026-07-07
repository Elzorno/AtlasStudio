# Chapter 01 Roadmap - Journey I: Home Region

## Purpose

This roadmap sequences the First Playable Hour milestone (`projects/the-last-sword-protocol/milestones/first-playable-hour.md`) into an ordered path with pacing, gating, and critical-path/optional distinctions.

"Chapter 01" here is the production term for what `home-region.md` and existing graph query examples call "Journey I." The two terms refer to the same content; this roadmap uses "Chapter 01" to match AtlasStudio's emerging milestone/roadmap vocabulary while preserving the existing canon term in cross-references.

## Critical Path

The critical path is the minimum beat sequence a player must complete to finish the milestone. It mirrors the `UNLOCKS`/`CONTAINS`/`CONNECTED_TO` canon edges exactly - no roadmap ordering decision here contradicts canon.

```text
1. Opening Sequence            (Ashford Village / Elara's House)
     ↓
2. Ashford Village              [location.ashford_village]
     ↓
3. Ashford Vale Overworld       [region.ashford_vale]
     ↓
4. Hidden Cave                  [location.hidden_cave]
     ↓
5. Sword Shrine                 [location.sword_shrine]         -- REWARDS item.last_sword
     ↓
6. Last Sword Acquisition       (return to overworld, world-state unlock)
     ↓                          -- item.last_sword UNLOCKS location.glassfield_ruins
7. Glassfield Ruins             [location.glassfield_ruins]
     ↓
8. First Relay Activation       [infrastructure.first_relay]
     ↓                          -- infrastructure.first_relay UNLOCKS location.rustshore_dock
9. Rustshore                    [location.rustshore_dock]
     ↓
10. Boat Departure
     ↓
11. End of Prototype Credits
```

## Pacing Targets

| Beat | Target Playtime | Cumulative |
| --- | --- | --- |
| 1. Opening Sequence | 3-5 min | 5 min |
| 2. Ashford Village | 5-8 min | 13 min |
| 3. Ashford Vale Overworld (first pass) | 5-7 min | 20 min |
| 4. Hidden Cave | 8-10 min | 30 min |
| 5. Sword Shrine | 2-3 min | 33 min |
| 6. Last Sword Acquisition (return trip) | 3-5 min | 38 min |
| 7. Glassfield Ruins | 10-12 min | 50 min |
| 8. First Relay Activation | 3-4 min | 54 min |
| 9. Rustshore | 3-5 min | 59 min |
| 10. Boat Departure | <1 min | 60 min |
| 11. End of Prototype Credits | 1-2 min | ~61-62 min |

Total target: 55-65 minutes, matching the "45-60 minutes plus light exploration" target in the milestone document. Pacing is a design target for tuning, not an acceptance-blocking hard limit.

## Gating Logic

Every gate below is enforced by an existing canon edge; the roadmap does not invent new gates.

| Gate | Enforced By | Effect |
| --- | --- | --- |
| Enter Sword Shrine | `location.hidden_cave CONTAINS location.sword_shrine` (structural, requires cave traversal) | Player must progress through the cave before reaching the shrine. |
| Enter Glassfield Ruins | `item.last_sword UNLOCKS location.glassfield_ruins` | Ruins entrance is visible but not enterable until the sword is obtained. |
| Enter Rustshore Dock (departure trigger) | `infrastructure.first_relay UNLOCKS location.rustshore_dock` | Dock is visible/reachable as a location earlier, but the departure sequence and Dockmaster's key dialogue should not fire until the relay is restored, so the milestone's climax lands before the region is "closed out." |

Note: `location.ashford_village CONNECTED_TO location.rustshore_dock` means the dock is geographically reachable early. The roadmap treats "reachable" and "narratively ready to depart" as different states - implementation should gate the departure-specific dialogue/event on the relay flag, not on physical access, consistent with the milestone's Beat 9 acceptance criteria.

## Optional / Deferred Content

The following content from `world-model.md` and `home-region.md` is explicitly **out of scope** for the First Playable Hour critical path:

- **Fogfen Marsh** (optional region content per `home-region.md`) - deferred to a later chapter or an optional side-content pass after milestone acceptance.
- **Watchtower / small castle outpost** (optional per `home-region.md`) - deferred; not required to prove the core loop.

These remain valid future canon/production content but are not work-breakdown packages in this roadmap. Including them would violate the "prove the core loop first" intent of a vertical slice.

## Branching Note

The critical path above is linear by design, matching the Work Order Design Standard's preference for small, provable scope. Ashford Vale Overworld (Beat 3) is visited twice (Beats 3 and 6) - this is intentional "open but controlled" design per `home-region.md`, not a separate map or work package.

## Chapter Boundary and What Comes Next

Chapter 01 ends at Beat 11 (End of Prototype Credits). This is the full scope of `work_order.wo_1000`.

Chapter 02 (Journey 2, per `home-region.md`: "Transition to Journey 2") is explicitly **not** planned by this roadmap. Once Chapter 01 is accepted and playtested, AtlasStudio's Planning Engine (`tools/atlas_planner/planner.py`) and Agent Scheduler design (`studio/scheduling/agent-scheduler-design.md`) should be used to recommend and staff the next chapter's master plan, rather than pre-committing to Chapter 02 scope now.

## Relationship to Production Documents

This roadmap defines *order and pacing*. It does not assign agents, estimate implementation size, or define file-level dependencies - see:

- `projects/the-last-sword-protocol/production/implementation-plan.md` for phased execution strategy and multi-provider coordination.
- `projects/the-last-sword-protocol/production/dependency-map.md` for the work-package dependency graph.
- `projects/the-last-sword-protocol/production/work-breakdown.md` for the actual implementation packages.
