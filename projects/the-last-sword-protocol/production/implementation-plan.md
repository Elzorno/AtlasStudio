# Implementation Plan - First Playable Hour

## Purpose

This document defines how AtlasStudio will actually coordinate production of the First Playable Hour milestone (`work_order.wo_1000`), using the tooling and agent model already built (Studio Doctor, Atlas Graph Validator/Query/Diff, Canon Linter, Immutable Formatting Guard, Planning Engine, Agent Scheduler design), and explicitly supporting multiple providers working simultaneously.

This is the master implementation roadmap for Milestone 1. Future milestones should follow this same phase structure rather than reinventing it.

## Phases

### Phase 0 - Design Lock (Complete as of this work order)

The milestone document, roadmap, dependency map, and work breakdown are the locked design targets. No further design work is needed before implementation begins, except:

- `WP-02` Canon Gap Resolution (Elara's House, Old North Road) - small, should run immediately.

Design Lock does not mean design is frozen forever. If implementation reveals a real design problem, the Canon Change Rule in `studio/workflow.md` applies: request a canon revision, record the decision, then proceed.

### Phase 1 - Engine Bridge Foundation

`WP-01` alone. This phase is intentionally narrow and serial: nothing engine-specific can be verified end-to-end until the bridge exists. Claude Code should own this phase, with Codex validating the handoff format against real RPG Maker MZ constraints before sign-off.

Phase 1 and `WP-02` (Canon Gap Resolution) can run at the same time - they touch entirely different files (`bridges/` vs. graph JSON) and different agents (Claude Code / Codex vs. GPT / Human).

### Phase 2 - Parallel Content Production

This is the phase where multiple providers work simultaneously. Once `WP-01` lands, the following packages have no dependency on each other and should be staffed concurrently:

| Package | Provider | Files Touched |
| --- | --- | --- |
| WP-03 Ashford Village Town Build | Codex | Village map/events (bridge) |
| WP-04 Ashford Vale Overworld Build | Codex (second session, or a second Codex-class agent if available) | Overworld map/events (bridge) |
| WP-05 Hidden Cave & Sword Shrine | Codex | Cave/shrine map/events (bridge) |
| WP-06 Glassfield Ruins & First Relay | Codex | Ruins map/events (bridge) - map construction can start now; gating verification waits on WP-05 |
| WP-07 Rustshore Dock & Boat Departure | Codex | Dock map/events (bridge) |
| WP-08 NPC & Dialogue Content | GPT | Dialogue text files, no engine files |
| WP-09 Monster & Encounter Implementation | Codex + GitHub Copilot | Monster data files, no map overlap with WP-03 through WP-07 |
| WP-10 Music & Audio Integration | Human/GPT (sourcing) + Codex/Copilot (wiring) | Audio assets and hook points, no map overlap |

Because each engine-specific package owns a distinct map/file set inside the bridge's ownership model (`WP-01` deliverable), simultaneous Codex sessions do not collide. `WP-08`, `WP-09`, and `WP-10` touch no engine files at all until final wiring, so they can proceed fully in parallel with everything else, including Phase 1.

Ollama can run continuous low-cost consistency scans across whatever content lands during this phase, rather than waiting for Phase 4 - it does not need to be gated, since its job is read-only review.

### Phase 3 - Event & Sequence Scripting

`WP-11` (Opening Sequence & Credits Scripting). This phase is serial relative to Phase 2 because it needs the Village/House maps (`WP-03`) and the Dock (`WP-07`) to exist first. It also formalizes the cutscene pattern reused by the Sword Shrine (`WP-05`), Relay Activation (`WP-06`), and Boat Departure (`WP-07`) events - those packages should implement a first pass of their own cutscene using placeholder pacing, then `WP-11` unifies the pattern rather than each package inventing its own.

GPT leads scene scripting/pacing; Codex leads technical execution.

### Phase 4 - Integration & Playtest

`WP-12` (Consistency & QA Pass). Ollama's continuous scans from Phase 2 are consolidated here into a final report. Claude Code spot-checks event-gating correctness against the roadmap's Gating Logic table. A human plays the full hour start to finish.

Run, in order:

```bash
python3 tools/atlas_graph/validate_graph.py
python3 tools/atlas_graph/query_graph.py missing-sources
python3 tools/atlas_lint/canon_lint.py --project the-last-sword-protocol
python3 tools/atlas_doctor/doctor.py --project the-last-sword-protocol
python3 tools/atlas_graph/diff_graph.py --base <chapter-01-start-commit> --head HEAD
```

The diff command gives reviewers a single readable summary of everything the chapter added, per WO-0010's Graph Diff Engine, distinguishing canon changes (should be limited to `WP-02`) from production changes (everything else).

### Phase 5 - Acceptance

`WP-13`. Human-only, per `studio/agent-roles.md`'s ownership of final creative judgment. On acceptance, update `work_order.wo_1000` to `accepted` in the production graph, following the same pattern used for `WO-0007`, `WO-0008`, and `WO-0012`.

## Multi-Provider Coordination Rules

1. **File ownership prevents collision, not agent identity.** Two Codex sessions working on `WP-04` and `WP-05` simultaneously is safe because they own different map files under the bridge's ownership model. The bridge's ownership states (generated / agent-drafted / human-edited / hand-authored / locked, per `studio/workflow.md`) are the mechanism that makes this safe - `WP-01` must define these clearly enough that concurrent packages never guess at ownership.
2. **Non-engine content has no serialization requirement.** Dialogue (`WP-08`), monster design (`WP-09`), and music sourcing (`WP-10`) can start on day one, in parallel with `WP-01`, because they produce content, not engine wiring. Wiring happens once, at the point each depends on the bridge.
3. **Reviewers do not block producers.** Ollama's consistency scans and Claude Code's architecture spot-checks run continuously during Phase 2-4 and produce findings, not gates. Only `WP-12`'s formal QA pass and `WP-13`'s human acceptance are hard gates.
4. **Canon changes are always serialized through the human.** `WP-02` is the only package that touches canon files. No other package may modify `canon.nodes.json` or `canon.edges.json` regardless of how many providers are active, per the Canon Change Rule.
5. **Formatting discipline applies regardless of parallelism.** Every package touching graph JSON must run `python3 tools/atlas_format/format_guard.py --check` before submission, per `studio/immutable-formatting-rule.md`, so concurrent diffs stay reviewable.

## Provider Role Summary

Matches the capability model in `studio/scheduling/agent-scheduler-design.md`:

- **Claude Code** - architecture (`WP-01` bridge design), review (spot-checks during Phase 2/4), graph evolution (production graph updates as packages complete).
- **Codex** - implementation (`WP-03` through `WP-07`, `WP-09` engine wiring, `WP-10` technical integration), tooling/automation support, applying work orders to the codebase.
- **GPT** - dialogue and story content (`WP-08`), quest/scene pacing (`WP-11` scripting), documentation support.
- **GitHub Copilot** - boilerplate and repetitive implementation (monster variant recolors in `WP-09`, repetitive event patterns in `WP-03` through `WP-07`).
- **Ollama** - offline consistency scans across all content during Phase 2-4, summaries for human review, low-risk review assistance.
- **Human** - canon approval (`WP-02`), creative direction throughout, final acceptance (`WP-13`), and any high-risk or irreversible call the Agent Scheduler design routes to `canon_decision`.

## Relationship to Existing AtlasStudio Tooling

This plan does not require new tooling. Every verification step above uses tools already delivered by prior work orders (`WO-0008`, `WO-0009`, `WO-0010`, `WO-0013`, `WO-0014`). The Planning Engine (`WO-0011`) and Agent Scheduler design (`WO-0012`) should be used *after* this milestone ships, to recommend and staff Chapter 02, rather than being re-derived here.
