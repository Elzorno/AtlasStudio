# RPG Maker Implementation Preflight

Project: `the-last-sword-protocol`
Target repository: `TheLastSwordProtocol-Game` (read-only inspection)
Report date: 2026-07-07
Mode: read-only, documentation only - no game repository, canon, or map file was modified.

## Executive Summary - Read This First

**AtlasStudio does not currently have enough information to responsibly finalize WP-03B guidance for Ashford Village.** This is not a tileset or passability problem. It is a governance problem: a second, independently canonical design system - `TheLastSwordProtocol-Atlas`, a sibling repository - has already been actively implementing Ashford Village under its own canon, its own work order series, and its own hand-authored RPG Maker maps, and it uses a different protagonist, a different Elara, and no Rowan at all. See "Primary Blocker" below. Every other finding in this report (tilesets, passability, event conventions, route validation) is accurate and usable, but none of it should be handed to Codex for Ashford Village specifically until the primary blocker is resolved by human/Production Director decision.

## Primary Blocker: Two Independently Canonical Design Systems Target The Same Village

### What Was Found

`TheLastSwordProtocol-Game/AGENTS.md` states plainly: "Atlas IDs are canonical. All design truth... comes from the sibling repo `../TheLastSwordProtocol-Atlas/`." That repository (`TheLastSwordProtocol-Atlas`) is a separate, mature production system with its own 36-entry work order series, its own Creative/Story/Character/World bibles, its own orchestrator and agent-assignment policy, and its own Canonical ID Registry - entirely independent of AtlasStudio (this repository).

It has already produced, for Ashford Village specifically:

- `WO-0025` / `IMP-HOM-017` - a completed manual map-building packet for Ashford Exterior.
- `WO-0026` / `IMP-HOM-018` - a completed manual map-building packet for Elara House Interior.
- `WO-0035` and `WO-0036` - open "Build Gate A" work orders to execute those packets as production maps, currently awaiting execution.
- Real, hand-authored RPG Maker data: `map_ownership.json` already marks `data/Map001.json` (`TWN_Ashford_Exterior`) and `data/Map002.json` (`INT_Ashford_ElaraHouse`) as `hand_authored`, meaning pipeline scripts must never write them. Map001 already has 23 events; Map002 already has 10.

Its canon differs from AtlasStudio's in ways that directly conflict with `WP-03A`'s Ashford Village Experience Specification:

| Element | AtlasStudio (`WP-03A`) | `TheLastSwordProtocol-Atlas` (already implemented) |
| --- | --- | --- |
| Protagonist | "The Hero" (generic, `character.hero`) | **Kai** (`Actors.json` slot 1; named throughout) |
| Guardian | Elara - "guardian and emotional anchor," implied peer/parental age | **Grandmother Elara** (`NPC-ELA-001`) - explicitly a grandmother, keeper of "inherited warnings" and "old-world safety procedures as family tradition" |
| Village elder/historian | **Rowan** - named, fully specified in `WP-03A` | No character named Rowan exists anywhere in `TheLastSwordProtocol-Atlas` (confirmed by repository-wide search). Map001 has a "Village Elder Placeholder" event - unnamed, unimplemented |
| Home | "Rowan's Cottage," shared household (`WP-03A`'s household-consolidation resolution) | **Elara House** (`INT_Ashford_ElaraHouse`, Map002) - Elara's home alone; Kai's start position is here (`System.json startMapId: 2`) |
| Shops | General Store + Blacksmith (two buildings, `WP-03A`) | One "Ashford Shop" (`INT_Ashford_Shop`, Map003) |
| Inn | Named NPC Tomas, dedicated building (`WP-03A`) | No Inn building found among Ashford's three Map001-003 screens |
| Additional NPCs already placed | Garrick, Mabel, Tomas, background villagers (`WP-03A`, all production-only names) | Child Near Old Panel, Farmer With Warm Stones, "Skyreach Joker," Dock Messenger, Village Elder Placeholder (Map001) |
| Region geography | Ashford Vale only, per AtlasStudio canon graph | Includes **Skyreach Hill** (`SCR-HOM-SKY-001`, a dungeon/path screen) - a location with no equivalent anywhere in AtlasStudio's canon graph |

Overlapping elements that do agree between the two systems: Hidden Cave, Glassfield Ruins, a Sealed Node/First Relay-equivalent, Rustshore, and an optional Fogfen Marsh - suggesting both systems descend from a common earlier design, but diverged at the character and settlement-structure level.

### Why This Matters Now, Not Later

`work-orders/WP-02-implementation-target-readiness-audit.md` already surfaced part of this in its "Manual Setup Still Required" section: *"Decide whether the target project follows the older `TheLastSwordProtocol-Atlas` Home Island export, the current AtlasStudio first-playable-hour plan, or a merged transition plan."* That decision was never made. `WP-03A` and `WP-03` were subsequently completed as if Ashford Village were an unclaimed, empty design space. It is not - it is already the most actively-implemented location in the entire target repository.

Proceeding with `WP-03B` against AtlasStudio's current production package as-is risks one of two failures: either implementation agents overwrite or duplicate already-in-progress hand-authored work (`map_ownership.json` forbids this outright for Maps 1-2), or they build a second, contradictory "Ashford Village" alongside the real one, which would actively work against the studio's own Player-Visible Production Rule rather than serve it.

### What This Report Does Not Do

This report does not decide which system governs Ashford Village going forward, does not merge the two canons, and does not modify either repository's design or graph data. That decision requires human/Production Director judgment - it is a "human approval for canon"-class decision (`studio/governance/atlas-principles.md`), not an implementation detail. See "Recommendation" below for the concrete choices available.

## Implementation Blockers (Full List)

1. **Primary (see above):** unresolved conflict between AtlasStudio's Ashford Village design and `TheLastSwordProtocol-Atlas`'s already-in-progress implementation of the same location.
2. `data/Map001.json`, `data/Map002.json`, `data/System.json`, and `map_ownership.json` all show uncommitted, in-progress modifications in the target repository as of this inspection (consistent with `WP-02`'s prior finding) - these should be reviewed and either committed or intentionally parked by their owner before any further handoff work references them.
3. No automated RPG Maker passability validator exists yet in AtlasStudio's tooling; the Passability Rule's fallback (mandatory human playtest) remains the only current enforcement mechanism.
4. The toolchain that writes to `TheLastSwordProtocol-Game` (`../rpgmakerLSP/tools/atlas-import/`) lives outside both AtlasStudio and the game repository; any handoff must name this host explicitly and state read/write status per command.

## Recommended Tilesets

The target repository's actual `Tilesets.json` defines five populated tilesets, all `mode: 1`:

| ID | Name | Observed Use |
| --- | --- | --- |
| 2 | Outside | Map001 (`TWN_Ashford_Exterior`, 40x32) |
| 3 | Inside | Map002/Map003 (`INT_Ashford_ElaraHouse`, `INT_Ashford_Shop`, both 17x13) |
| 4 | Dungeon | Cave/ruin-type screens (by naming convention, not individually re-verified in this pass) |
| 5 | SF Outside | Ancient-tech/exterior "science-fantasy" areas (Sealed Node family, by naming convention) |
| 6 | SF Inside | Ancient-tech/interior areas |

**Recommendation:** any future Ashford Village work should use tileset **2 (Outside)** for the exterior and **3 (Inside)** for interiors, matching what is already in use for Map001-003, rather than the generic "exterior/interior tileset role" language used in `WP-03`'s map brief (written before this concrete data was available). `ashford-village-map-brief.md` should be updated to cite these concrete IDs once the primary blocker is resolved and it is confirmed AtlasStudio's brief still applies to this location at all.

## Passability Assumptions

- Default RPG Maker MZ tileset passability (as shipped with tilesets 2-6) appears usable as-is; no evidence of custom passability overrides was found in the maps inspected.
- Per `bridges/rpg-maker-mz/passability-rule.md`, default passability should remain unchanged unless a work order explicitly authorizes an override - nothing in this inspection suggests an override is needed for Ashford Village specifically.
- No automated validator currently checks these assumptions (see Blockers, item 3) - manual/human playtest remains required regardless of any future implementation path chosen.

## Engine Constraints

- Engine: RPG Maker MZ 1.10.0 (`game.rmmzproject`, confirmed in `js/rmmz_core.js`).
- Screen: 1920x1080. Party: 1 actor (Kai). Battle mode: side-view.
- Switch slots: 200 (reserved ranges: 1-49 Journey 1, 50-79 trials, 80-99 Home Island optional, 100-149 combat, 150-199 debug, per `atlas_skeleton_manifest.json`).
- Variable slots: 150 (parallel reservation scheme).
- No plugins are currently configured (`js/plugins.js` has an empty `$plugins` array) - low technical risk today, but any future plugin introduction needs an explicit bridge-owned decision, since `js/plugins.js` is a shared global file.
- Common Events 1-6 are already populated (archive message, sword authentication, relay resolution, transitions, trial helpers) and reserved 1-49 for this pipeline - any AtlasStudio-originated common event work must not collide with these.

## Event Conventions (Observed In The Real Target Repository)

From direct inspection of `data/Map001.json` and `data/Map002.json` (not the sample project - this is the actual target repo's own convention):

- **NPC events:** Action Button trigger (`trigger: 0`), "same as characters" priority (`priorityType: 1`), typically single-page unless the NPC has conditional content.
- **Transfer events:** Player Touch trigger (`trigger: 1`), "below characters" priority (`priorityType: 0`), named with a traceable ID prefix, e.g. `TRN-HOM-002 Enter Elara House`, `TRN-HOM-007 South/east route to Rustshore`.
- **Decorative/environmental events:** Action Button trigger, "below characters" priority, named with a `DEC-SCR-HOM-<screen>-<description>` convention, e.g. `DEC-SCR-HOM-ASH-001-GARDEN-PATCH`.
- **Ambient/story triggers:** Autorun (`trigger: 3`) for one-time story beats, e.g. `Tremor Trigger` (2 pages, autorun) and the `EVT-HOM-001 Player Start` event on Map002.
- **Secrets:** implemented as multi-page events (e.g. `Hidden Item`, 2 pages) - consistent with the self-switch-gated pattern AtlasStudio's own `WP-03` event plan independently recommended, which is a reassuring convergence.
- **Interior environmental storytelling objects:** named individually and specifically, e.g. `INT-ASH-ELARA-KEEPSAKE Keepsake Shelf`, `INT-ASH-WARM-STONE-VENT`, `INT-ASH-OLD-PANEL` - notably, a "Keepsake Shelf" in Elara House already fills a narratively similar role to `WP-03A`'s proposed "Rowan's Bookshelf" secret, another point of convergent design instinct despite the character-roster conflict.

## Transfer Conventions

Every transfer observed carries a traceable `TRN-HOM-NNN` identifier tied to the Canonical ID Registry in `TheLastSwordProtocol-Atlas`, referenced directly in the event's in-editor name (not just a comment). AtlasStudio's own bridge conventions (`bridges/rpg-maker-mz/handoff-format.md`) do not currently require this level of ID traceability in event names - this is a stronger, more auditable convention than AtlasStudio has documented, and is worth adopting regardless of how the primary blocker resolves.

## Is Any Existing Implementation Reusable?

Yes, substantially - but note this is explicitly not a case of "old Zelda-style layouts being preserved just because they exist." Map001 (`TWN_Ashford_Exterior`) is 40x32 on the Outside tileset with 23 events already covering NPCs, transfers to five other screens (Elara House, Shop, Skyreach, Rustshore, Glassfield, and optional Fogfen Marsh), decorative environmental storytelling, and a tremor story trigger - this is overworld-connected town design, consistent with the Dragon Quest regional architecture AtlasStudio's own `jrpg-design-bible.md` calls authoritative, not a disconnected screen-chain. There is no evidence of a Zelda-style layout to reject here; the existing implementation already appears to follow the correct architectural model. The open question is entirely about *which characters and buildings* populate that architecture, not about the map's structural style.

## Implementation Recommendations

1. **Do not proceed with `WP-03B` implementation guidance for Ashford Village until a human/Production Director makes an explicit choice** between: (a) adopting `TheLastSwordProtocol-Atlas`'s already-implemented Kai/Grandmother Elara version as authoritative and revising AtlasStudio's canon graph and `WP-03A` specification to match it; (b) treating AtlasStudio's Hero/Rowan/Elara version as authoritative and formally superseding/replacing the in-progress `TheLastSwordProtocol-Atlas` work (with the real cost of discarding already-completed `WO-0025`/`WO-0026`/hand-authored map work); or (c) a merged plan reconciling both, which would itself need its own design work order.
2. Once that decision is made, update `ashford-village-map-brief.md` to reference the concrete tileset IDs (2 = Outside, 3 = Inside) confirmed in this report, rather than generic tileset-role language.
3. Adopt the `TRN-HOM-NNN`-style traceable ID convention observed in the real target repo for any future AtlasStudio-originated transfer events, regardless of which canon path is chosen.
4. Resolve the target repo's outstanding uncommitted changes (Map001, Map002, System.json, `map_ownership.json`) with their owner before any further handoff work is planned against them.
5. Continue treating Maps 1 and 2 as protected/hand-authored in all bridge handoffs, per the ownership ledger, regardless of which canon path is chosen - overwriting them without an explicit Production Director decision would violate the ownership model in both `AtlasStudio` and `TheLastSwordProtocol-Atlas`.

## Verification Performed

```bash
# AtlasStudio side
python3 tools/atlas_graph/validate_graph.py
python3 tools/atlas_doctor/doctor.py
python3 tools/atlas_lint/canon_lint.py --project the-last-sword-protocol
python3 tools/atlas_format/format_guard.py --check

# Read-only inspection (no writes performed)
# TheLastSwordProtocol-Game/data/*.json parsed and inspected directly
# TheLastSwordProtocol-Atlas/atlas/ read for character, screen, and work-order-queue context
```

No file in `TheLastSwordProtocol-Game` or `TheLastSwordProtocol-Atlas` was modified during this inspection.
