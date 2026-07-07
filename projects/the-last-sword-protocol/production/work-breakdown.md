# Work Breakdown - First Playable Hour

## Purpose

This document decomposes the First Playable Hour milestone into logical implementation work packages (WPs). Each package is scoped to become one future AtlasStudio work order once its prerequisites are met - this document does not create those work orders.

Per WO-1000's instructions, this is a small set of coherent packages, not a package per map/NPC/asset. Thirteen packages cover the entire milestone.

Capability categories match the task classes defined in `studio/scheduling/agent-scheduler-design.md`: `creative_design`, `architecture`, `implementation`, `repetitive_edit`, `review_qa`, and `canon_decision`.

## Package Table

### WP-01 - Engine Bridge Foundation

- **Covers:** Completing `WO-0005` (RPG Maker Bridge Design) into an actual bridge folder, ownership model, and handoff format that every engine-specific package below depends on.
- **Size:** L
- **Recommended capability:** architecture
- **Suggested providers:** Claude Code (primary - architecture, bridge design), Codex (support - validates handoff format against real RPG Maker MZ constraints)
- **Prerequisites:** None (can start immediately; `WO-0005` is currently `proposed`).
- **Completion definition:** `bridges/rpg-maker-mz/bridge-design.md` and `ownership-model.md` exist, are accepted, and can express every event type this milestone needs (dialogue triggers, world-state flags, sword-key sealed doors, cutscenes/transitions) without leaking engine IDs into core design docs.

### WP-02 - Canon Gap Resolution: Elara's House & Old North Road

- **Covers:** Formalizing the two canon gaps flagged in the milestone document as real graph nodes (and any needed edges) so downstream packages have a stable canon target.
- **Size:** S
- **Recommended capability:** creative_design (drafting) with canon_decision (approval)
- **Suggested providers:** GPT (draft node summaries/descriptions), Human (final canon approval, per the Canon Change Rule in `studio/workflow.md`)
- **Prerequisites:** None (can start immediately, runs parallel to WP-01).
- **Completion definition:** `location.elaras_house` and a route or connection node for Old North Road (or a documented decision that the existing `CONNECTED_TO` edge already suffices) are accepted into canon graph files.

### WP-03 - Ashford Village Town Build

- **Covers:** Beats 1 (partial, Ashford Village portion) and 2. Town map, NPC placement, shop/inn stubs, rumor dialogue wiring.
- **Size:** M
- **Recommended capability:** implementation
- **Suggested providers:** Codex (primary), GitHub Copilot (boilerplate NPC event patterns)
- **Prerequisites:** WP-01, WP-02
- **Completion definition:** Village map is playable, Rowan's dialogue chain points to the Hidden Cave, exit to the overworld is functional.

### WP-04 - Ashford Vale Overworld Build

- **Covers:** Beat 3 and the revisit in Beat 6. Overworld map, encounter zones, landmark visibility/gating for Glassfield Ruins and Rustshore Dock, world-state flag for the sword unlock.
- **Size:** M
- **Recommended capability:** implementation
- **Suggested providers:** Codex (primary)
- **Prerequisites:** WP-01
- **Completion definition:** All four location entrances are correctly visible/reachable per canon edges; Glassfield Ruins entrance is locked until the sword-acquired flag is set; encounter zones are tuned to low difficulty.

### WP-05 - Hidden Cave & Sword Shrine Dungeon

- **Covers:** Beats 4 and 5. Cave interior, traversal puzzle, Sword Shrine chamber, sword recognition cutscene and item grant.
- **Size:** L
- **Recommended capability:** implementation
- **Suggested providers:** Codex (primary), Claude Code (review of the sword-grant event pattern, since it is reused conceptually in WP-06 and WP-11)
- **Prerequisites:** WP-01
- **Completion definition:** Cave is fully traversable with at least one optional side room; Sword Shrine grants `item.last_sword` unmissably; return path to the overworld works.

### WP-06 - Glassfield Ruins & First Relay

- **Covers:** Beats 7 and 8. Ruins interior, sword-key sealed doors, corrupted construct encounters, First Relay chamber and activation sequence.
- **Size:** L
- **Recommended capability:** implementation
- **Suggested providers:** Codex (primary), Claude Code (review of sealed-door/relay event architecture)
- **Prerequisites:** WP-01, WP-05 (sword must exist before ruins can be meaningfully tested end-to-end, though asset/map construction may start earlier)
- **Completion definition:** At least two sword-key sealed doors function; relay activation sequence completes and sets the Rustshore Dock unlock flag; no soft-lock exists if the player saves mid-sequence.

### WP-07 - Rustshore Dock & Boat Departure

- **Covers:** Beats 9 and 10. Dock map, Dockmaster dialogue, boarding cutscene, departure transition.
- **Size:** S/M
- **Recommended capability:** implementation
- **Suggested providers:** Codex (primary)
- **Prerequisites:** WP-01, WP-06 (departure dialogue should gate on the relay-restored flag per the roadmap's gating logic)
- **Completion definition:** Dockmaster dialogue and boarding trigger only become available after the relay flag is set; departure transition runs under 30 seconds; player can freely leave and return before boarding.

### WP-08 - NPC & Dialogue Content

- **Covers:** All dialogue writing across every beat - Elara, Rowan, Village Elder, Dockmaster, and any flavor NPCs. Cross-cutting, not tied to one beat.
- **Size:** M
- **Recommended capability:** creative_design
- **Suggested providers:** GPT (primary - all dialogue drafting), Human (approval of tone/content), Ollama (consistency pass across all NPC voices)
- **Prerequisites:** WP-02 (for any NPC tied to the two canon gaps); otherwise can start immediately and run fully parallel to WP-01, WP-03 through WP-07.
- **Completion definition:** Every NPC listed in the milestone document has a complete, reviewed dialogue tree ready for wiring into its map.

### WP-09 - Monster & Encounter Implementation

- **Covers:** All six monster families from `home-region.md` (Gel Wisps, Cave Flutterers, Pebble Constructs, Rust Stingers, Archive Husks, Bit Wraiths) with stats, sprites/recolors, and encounter tables for their respective maps.
- **Size:** M
- **Recommended capability:** implementation
- **Suggested providers:** Codex (primary), GitHub Copilot (recolor/variant boilerplate)
- **Prerequisites:** WP-01
- **Completion definition:** All six monster families are implemented and balanced across the overworld, cave, and ruins encounter tables; difficulty curve rises Cave → Ruins as specified in the milestone.

### WP-10 - Music & Audio Integration

- **Covers:** All required tracks across every beat (opening, village, overworld, cave, shrine fanfare, ruins, relay activation, dock/departure, credits) - sourcing/composition and technical integration.
- **Size:** M
- **Recommended capability:** implementation / repetitive_edit (integration once tracks are sourced)
- **Suggested providers:** Human or GPT (sourcing/brief for composition, if externally commissioned), Codex or GitHub Copilot (technical wiring into maps/events)
- **Prerequisites:** WP-01 (for the event/map hooks tracks attach to); track sourcing itself can start immediately in parallel.
- **Completion definition:** Every required music cue in the milestone document is present and correctly triggered in-engine.

### WP-11 - Opening Sequence & Credits Scripting

- **Covers:** Beats 1 (opening) and 11 (credits), plus the shared cutscene-scripting technique reused for the sword recognition (Beat 5), relay activation (Beat 8), and boat departure (Beat 10) events.
- **Size:** S/M
- **Recommended capability:** creative_design (scripting/pacing of scenes) + implementation (technical execution)
- **Suggested providers:** GPT (scene scripting/pacing), Codex (technical cutscene implementation)
- **Prerequisites:** WP-03 (opening needs the village/house maps to exist), WP-07 (credits caps off the departure sequence)
- **Completion definition:** Opening sequence and credits both play start-to-finish without manual intervention; the shared cutscene pattern is documented once and reused, not reimplemented per beat.

### WP-12 - Consistency & QA Pass

- **Covers:** Full-hour playtest, Studio Doctor and Canon Linter runs, cross-beat consistency check (naming, tone, difficulty curve, gating correctness).
- **Size:** S
- **Recommended capability:** review_qa
- **Suggested providers:** Ollama (primary - offline consistency scans and summaries), Claude Code (spot-check architecture/event-gating correctness), Human (final playtest)
- **Prerequisites:** WP-03 through WP-11 substantially complete.
- **Completion definition:** `python3 tools/atlas_doctor/doctor.py`, `python3 tools/atlas_graph/validate_graph.py`, and `python3 tools/atlas_lint/canon_lint.py` all run clean; one uninterrupted human playtest of the full hour is logged with no blocking bugs.

### WP-13 - Milestone Acceptance & Prototype Ship

- **Covers:** Final human review against the milestone's acceptance criteria and formally marking the milestone accepted.
- **Size:** S
- **Recommended capability:** canon_decision
- **Suggested providers:** Human (only - final creative and production authority per `studio/agent-roles.md`)
- **Prerequisites:** WP-12
- **Completion definition:** Human confirms all milestone-level acceptance criteria are met; `work_order.wo_1000` and any downstream implementation work orders are marked `accepted` in the production graph.

## Sizing Legend

- **S** - fits comfortably in one focused agent session.
- **M** - may span 2-3 sessions or require checkpointed sub-steps.
- **L** - substantial scope; should be monitored for further splitting into work orders once assigned, per the Work Order Design Standard in `studio/work-order-format.md`.

## Parallelization Summary

See `projects/the-last-sword-protocol/production/implementation-plan.md` for the full multi-provider execution strategy. In short: WP-01 and WP-02 can run simultaneously; WP-08, WP-09, and WP-10 (dialogue, monsters, music) can all run in parallel with each other and with WP-03 through WP-07 once WP-01 lands, because they touch distinct files and asset domains. WP-11, WP-12, and WP-13 are necessarily serial, each depending on the bulk of what precedes it.
