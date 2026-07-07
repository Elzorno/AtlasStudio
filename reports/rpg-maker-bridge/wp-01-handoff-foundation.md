# RPG Maker MZ Implementation Handoff Checklist

Project: `the-last-sword-protocol`
Target repo: `TheLastSwordProtocol-Game`
Generated: 2026-07-07
Mode: read-only handoff generation

## Bridge Inputs

- bridge_design: `/Users/christopherzornes/Documents/GitHub/AtlasStudio/bridges/rpg-maker-mz/bridge-design.md`
- ownership_model: `/Users/christopherzornes/Documents/GitHub/AtlasStudio/bridges/rpg-maker-mz/ownership-model.md`
- ownership states: `generated`, `agent-drafted`, `human-edited`, `hand-authored`, `locked`
- handoff_format: `/Users/christopherzornes/Documents/GitHub/AtlasStudio/bridges/rpg-maker-mz/handoff-format.md`
- handoff template sections: Purpose, Player-Facing Goal, Source Design, RPG Maker Targets, Allowed Changes, Protected Areas, Implementation Notes, Acceptance Criteria, Verification Steps

## Guardrails

- Do not modify RPG Maker repositories during handoff generation.
- Treat unknown ownership as human-edited until audited.
- Do not change AtlasStudio canon from an RPG Maker implementation task.
- Do not run broad formatters over RPG Maker JSON.

## WP-03 - Ashford Village Town Build

- Source work order: `WO-1000`
- Recommended agent: `codex`
- Capability: implementation
- Suggested providers: Codex (primary), GitHub Copilot (boilerplate NPC event patterns)
- Prerequisites: WP-01, WP-02
- Completion definition: Village map is playable, Rowan's dialogue chain points to the Hidden Cave, exit to the overworld is functional.

### Source Graph Nodes

- `location.ashford_village` (ok)
- `character.rowan` (ok)

### RPG Maker Targets

| Target | Ownership | Allowed Change | Rule |
|---|---|---|---|
| `data/MapXXX.json` | unknown | Audit village exterior/interior map IDs before edit. | Audit before edit; do not overwrite existing content. |
| `data/CommonEvents.json` | unknown | Add only approved shared dialogue/event helpers. | Audit before edit; do not overwrite existing content. |

### Protected Areas

- Existing human-authored village maps and NPC events.

### Implementation Checklist

- [ ] Confirm human approval for the implementation work order before touching the RPG Maker repo.
- [ ] Inspect target RPG Maker files read-only and record ownership before edits.
- [ ] Reserve or confirm map, event, switch, variable, database, plugin, and asset ranges.
- [ ] Prefer additive edits; do not rewrite existing RPG Maker JSON blobs.
- [ ] Run file-level validation and a player-facing manual test after implementation.
- [ ] Record changed targets and ownership states in the submission report.

### Verification Steps

- [ ] Open RPG Maker project without JSON parse errors.
- [ ] Confirm no protected map/event/database target was overwritten.
- [ ] Run the exact player-facing route for this package.

## WP-04 - Ashford Vale Overworld Build

- Source work order: `WO-1000`
- Recommended agent: `codex`
- Capability: implementation
- Suggested providers: Codex (primary)
- Prerequisites: WP-01
- Completion definition: All four location entrances are correctly visible/reachable per canon edges; Glassfield Ruins entrance is locked until the sword-acquired flag is set; encounter zones are tuned to low difficulty.

### Source Graph Nodes

- `region.ashford_vale` (ok)
- `location.ashford_village` (ok)
- `location.hidden_cave` (ok)
- `location.glassfield_ruins` (ok)
- `location.rustshore_dock` (ok)

### RPG Maker Targets

| Target | Ownership | Allowed Change | Rule |
|---|---|---|---|
| `data/MapXXX.json` | unknown | Audit overworld map ID before edit. | Audit before edit; do not overwrite existing content. |
| `data/Troops.json` | unknown | Use only approved encounter rows after audit. | Audit before edit; do not overwrite existing content. |

### Protected Areas

- Existing overworld map layout if human-edited or hand-authored.

### Implementation Checklist

- [ ] Confirm human approval for the implementation work order before touching the RPG Maker repo.
- [ ] Inspect target RPG Maker files read-only and record ownership before edits.
- [ ] Reserve or confirm map, event, switch, variable, database, plugin, and asset ranges.
- [ ] Prefer additive edits; do not rewrite existing RPG Maker JSON blobs.
- [ ] Run file-level validation and a player-facing manual test after implementation.
- [ ] Record changed targets and ownership states in the submission report.

### Verification Steps

- [ ] Open RPG Maker project without JSON parse errors.
- [ ] Confirm no protected map/event/database target was overwritten.
- [ ] Run the exact player-facing route for this package.

## WP-05 - Hidden Cave & Sword Shrine Dungeon

- Source work order: `WO-1000`
- Recommended agent: `codex`
- Capability: implementation
- Suggested providers: Codex (primary), Claude Code (review of the sword-grant event pattern, since it is reused conceptually in WP-06 and WP-11)
- Prerequisites: WP-01
- Completion definition: Cave is fully traversable with at least one optional side room; Sword Shrine grants `item.last_sword` unmissably; return path to the overworld works.

### Source Graph Nodes

- `location.hidden_cave` (ok)
- `location.sword_shrine` (ok)
- `item.last_sword` (ok)

### RPG Maker Targets

| Target | Ownership | Allowed Change | Rule |
|---|---|---|---|
| `data/MapXXX.json` | unknown | Audit cave and shrine map IDs before edit. | Audit before edit; do not overwrite existing content. |
| `data/Weapons.json` | unknown | Reserve Last Sword database row before edit. | Audit before edit; do not overwrite existing content. |
| `data/CommonEvents.json` | unknown | Add sword-grant event only in approved range. | Audit before edit; do not overwrite existing content. |

### Protected Areas

- Existing item/database rows outside approved ranges.

### Implementation Checklist

- [ ] Confirm human approval for the implementation work order before touching the RPG Maker repo.
- [ ] Inspect target RPG Maker files read-only and record ownership before edits.
- [ ] Reserve or confirm map, event, switch, variable, database, plugin, and asset ranges.
- [ ] Prefer additive edits; do not rewrite existing RPG Maker JSON blobs.
- [ ] Run file-level validation and a player-facing manual test after implementation.
- [ ] Record changed targets and ownership states in the submission report.

### Verification Steps

- [ ] Open RPG Maker project without JSON parse errors.
- [ ] Confirm no protected map/event/database target was overwritten.
- [ ] Run the exact player-facing route for this package.

## WP-06 - Glassfield Ruins & First Relay

- Source work order: `WO-1000`
- Recommended agent: `codex`
- Capability: implementation
- Suggested providers: Codex (primary), Claude Code (review of sealed-door/relay event architecture)
- Prerequisites: WP-01, WP-05 (sword must exist before ruins can be meaningfully tested end-to-end, though asset/map construction may start earlier)
- Completion definition: At least two sword-key sealed doors function; relay activation sequence completes and sets the Rustshore Dock unlock flag; no soft-lock exists if the player saves mid-sequence.

### Source Graph Nodes

- `location.glassfield_ruins` (ok)
- `infrastructure.first_relay` (ok)
- `item.last_sword` (ok)

### RPG Maker Targets

| Target | Ownership | Allowed Change | Rule |
|---|---|---|---|
| `data/MapXXX.json` | unknown | Audit ruins and relay map IDs before edit. | Audit before edit; do not overwrite existing content. |
| `data/CommonEvents.json` | unknown | Add relay activation helper only if approved. | Audit before edit; do not overwrite existing content. |
| `data/System.json` | human-edited | Do not rewrite global system data. | Audit before edit; do not overwrite existing content. |

### Protected Areas

- Existing relay/ruins events; global system settings.

### Implementation Checklist

- [ ] Confirm human approval for the implementation work order before touching the RPG Maker repo.
- [ ] Inspect target RPG Maker files read-only and record ownership before edits.
- [ ] Reserve or confirm map, event, switch, variable, database, plugin, and asset ranges.
- [ ] Prefer additive edits; do not rewrite existing RPG Maker JSON blobs.
- [ ] Run file-level validation and a player-facing manual test after implementation.
- [ ] Record changed targets and ownership states in the submission report.
- [ ] Confirm sword-acquired and relay-restored flags are named and reserved before wiring gates.

### Verification Steps

- [ ] Open RPG Maker project without JSON parse errors.
- [ ] Confirm no protected map/event/database target was overwritten.
- [ ] Run the exact player-facing route for this package.

## WP-07 - Rustshore Dock & Boat Departure

- Source work order: `WO-1000`
- Recommended agent: `codex`
- Capability: implementation
- Suggested providers: Codex (primary)
- Prerequisites: WP-01, WP-06 (departure dialogue should gate on the relay-restored flag per the roadmap's gating logic)
- Completion definition: Dockmaster dialogue and boarding trigger only become available after the relay flag is set; departure transition runs under 30 seconds; player can freely leave and return before boarding.

### Source Graph Nodes

- `location.rustshore_dock` (ok)
- `infrastructure.first_relay` (ok)

### RPG Maker Targets

| Target | Ownership | Allowed Change | Rule |
|---|---|---|---|
| `data/MapXXX.json` | unknown | Audit dock map ID before edit. | Audit before edit; do not overwrite existing content. |
| `data/CommonEvents.json` | unknown | Add departure transition only in approved range. | Audit before edit; do not overwrite existing content. |

### Protected Areas

- Existing dock events and transfer routes.

### Implementation Checklist

- [ ] Confirm human approval for the implementation work order before touching the RPG Maker repo.
- [ ] Inspect target RPG Maker files read-only and record ownership before edits.
- [ ] Reserve or confirm map, event, switch, variable, database, plugin, and asset ranges.
- [ ] Prefer additive edits; do not rewrite existing RPG Maker JSON blobs.
- [ ] Run file-level validation and a player-facing manual test after implementation.
- [ ] Record changed targets and ownership states in the submission report.
- [ ] Confirm dock departure remains locked until the relay-restored flag is set.

### Verification Steps

- [ ] Open RPG Maker project without JSON parse errors.
- [ ] Confirm no protected map/event/database target was overwritten.
- [ ] Run the exact player-facing route for this package.

## WP-09 - Monster & Encounter Implementation

- Source work order: `WO-1000`
- Recommended agent: `codex`
- Capability: implementation
- Suggested providers: Codex (primary), GitHub Copilot (recolor/variant boilerplate)
- Prerequisites: WP-01
- Completion definition: All six monster families are implemented and balanced across the overworld, cave, and ruins encounter tables; difficulty curve rises Cave → Ruins as specified in the milestone.

### Source Graph Nodes

- `region.ashford_vale` (ok)
- `location.hidden_cave` (ok)
- `location.glassfield_ruins` (ok)

### RPG Maker Targets

| Target | Ownership | Allowed Change | Rule |
|---|---|---|---|
| `data/Enemies.json` | unknown | Reserve enemy rows for six early monster families. | Audit before edit; do not overwrite existing content. |
| `data/Troops.json` | unknown | Reserve troop rows after enemy rows are known. | Audit before edit; do not overwrite existing content. |
| `img/enemies/` | unknown | Add or reference assets only after ownership audit. | Audit before edit; do not overwrite existing content. |

### Protected Areas

- Existing enemy/troop rows and existing image assets.

### Implementation Checklist

- [ ] Confirm human approval for the implementation work order before touching the RPG Maker repo.
- [ ] Inspect target RPG Maker files read-only and record ownership before edits.
- [ ] Reserve or confirm map, event, switch, variable, database, plugin, and asset ranges.
- [ ] Prefer additive edits; do not rewrite existing RPG Maker JSON blobs.
- [ ] Run file-level validation and a player-facing manual test after implementation.
- [ ] Record changed targets and ownership states in the submission report.

### Verification Steps

- [ ] Open RPG Maker project without JSON parse errors.
- [ ] Confirm no protected map/event/database target was overwritten.
- [ ] Run the exact player-facing route for this package.
- [ ] Verify encounter tables reference implemented enemy and troop rows.

## WP-10 - Music & Audio Integration

- Source work order: `WO-1000`
- Recommended agent: `codex`
- Capability: implementation / repetitive_edit (integration once tracks are sourced)
- Suggested providers: Human or GPT (sourcing/brief for composition, if externally commissioned), Codex or GitHub Copilot (technical wiring into maps/events)
- Prerequisites: WP-01 (for the event/map hooks tracks attach to); track sourcing itself can start immediately in parallel.
- Completion definition: Every required music cue in the milestone document is present and correctly triggered in-engine.

### Source Graph Nodes

- `region.ashford_vale` (ok)

### RPG Maker Targets

| Target | Ownership | Allowed Change | Rule |
|---|---|---|---|
| `audio/bgm/` | unknown | Add approved music tracks only. | Audit before edit; do not overwrite existing content. |
| `audio/se/` | unknown | Add approved sound effects only. | Audit before edit; do not overwrite existing content. |
| `data/MapXXX.json` | unknown | Wire cues only after map ownership is known. | Audit before edit; do not overwrite existing content. |

### Protected Areas

- Existing audio assets and map event pages.

### Implementation Checklist

- [ ] Confirm human approval for the implementation work order before touching the RPG Maker repo.
- [ ] Inspect target RPG Maker files read-only and record ownership before edits.
- [ ] Reserve or confirm map, event, switch, variable, database, plugin, and asset ranges.
- [ ] Prefer additive edits; do not rewrite existing RPG Maker JSON blobs.
- [ ] Run file-level validation and a player-facing manual test after implementation.
- [ ] Record changed targets and ownership states in the submission report.

### Verification Steps

- [ ] Open RPG Maker project without JSON parse errors.
- [ ] Confirm no protected map/event/database target was overwritten.
- [ ] Run the exact player-facing route for this package.
- [ ] Verify every new cue plays from the intended map or event hook.

## WP-11 - Opening Sequence & Credits Scripting

- Source work order: `WO-1000`
- Recommended agent: `codex`
- Capability: creative_design (scripting/pacing of scenes) + implementation (technical execution)
- Suggested providers: GPT (scene scripting/pacing), Codex (technical cutscene implementation)
- Prerequisites: WP-03 (opening needs the village/house maps to exist), WP-07 (credits caps off the departure sequence)
- Completion definition: Opening sequence and credits both play start-to-finish without manual intervention; the shared cutscene pattern is documented once and reused, not reimplemented per beat.

### Source Graph Nodes

- `location.ashford_village` (ok)
- `location.rustshore_dock` (ok)

### RPG Maker Targets

| Target | Ownership | Allowed Change | Rule |
|---|---|---|---|
| `data/MapXXX.json` | unknown | Audit opening and credits map/event targets before edit. | Audit before edit; do not overwrite existing content. |
| `data/CommonEvents.json` | unknown | Add shared cutscene pattern only in approved range. | Audit before edit; do not overwrite existing content. |

### Protected Areas

- Existing cutscene events and transfer events.

### Implementation Checklist

- [ ] Confirm human approval for the implementation work order before touching the RPG Maker repo.
- [ ] Inspect target RPG Maker files read-only and record ownership before edits.
- [ ] Reserve or confirm map, event, switch, variable, database, plugin, and asset ranges.
- [ ] Prefer additive edits; do not rewrite existing RPG Maker JSON blobs.
- [ ] Run file-level validation and a player-facing manual test after implementation.
- [ ] Record changed targets and ownership states in the submission report.

### Verification Steps

- [ ] Open RPG Maker project without JSON parse errors.
- [ ] Confirm no protected map/event/database target was overwritten.
- [ ] Run the exact player-facing route for this package.
