# Repository Conflict Analysis

Repositories reviewed: `AtlasStudio`, `TheLastSwordProtocol-Atlas`, `TheLastSwordProtocol-Game`, and (for chronology only) `rpgmakerLSP`.
Mode: read-only across all four. No file in any repository other than AtlasStudio was modified to produce this report.
Report date: 2026-07-07.

## Method

Findings are drawn from direct inspection: git history (`git log --reverse`) to establish chronology, canonical documents in each repository, `map_ownership.json` and RPG Maker data files in `TheLastSwordProtocol-Game`, and `atlas/planning/workorder_queue.json` in `TheLastSwordProtocol-Atlas`. This builds on `work-orders/WP-03-preflight-map-quality-passability.md`, which first surfaced the conflict, and goes further into chronology and full scope.

## Chronology (Why This Matters)

| Date (first commit) | Repository | Nature |
| --- | --- | --- |
| 2026-06-27 | `rpgmakerLSP` | Original monolithic prototype - RPG Maker project and an early "Atlas" spec folder mixed together. This is the "previous prototype" AtlasStudio's own bridge docs (`map-quality-standard.md`, `passability-rule.md`) already describe as having quality and passability problems. |
| 2026-07-04 | `TheLastSwordProtocol-Atlas` + `TheLastSwordProtocol-Game` | A deliberate clean split of `rpgmakerLSP`'s monolith into a specification repository and an implementation repository. `TheLastSwordProtocol-Atlas`'s own `WO-0017` is literally titled "split-atlas-specification-from-rpg-maker-implementation." |
| 2026-07-05 | `TheLastSwordProtocol-Atlas` | `WO-0029` retires the stale Atlas fork still living inside `rpgmakerLSP`, replacing it with a pointer README naming `TheLastSwordProtocol-Atlas` as canonical. This is a **direct precedent** for the kind of reconciliation this work order performs for AtlasStudio. |
| 2026-07-07 | `AtlasStudio` | A third, independently-started system. Its own vision document describes itself as succeeding a prior "Atlas v1," but shows no awareness that `TheLastSwordProtocol-Atlas` (created three days earlier) already performed that exact succession, cleanly, and was already active and producing real implementation work by the time AtlasStudio began. A repository-wide search of `TheLastSwordProtocol-Atlas` for any mention of "AtlasStudio" returns nothing - the blindness is mutual until this analysis. |

**Conclusion from chronology alone:** AtlasStudio is not the second system in this lineage; it is the third, and it was built without knowledge of the second. `TheLastSwordProtocol-Atlas` had already reached a "Locked v1.0" Project Constitution, a working CLI (validator, exporter, orchestrator), 36 work orders (24+ completed as of this analysis), and real hand-authored RPG Maker maps before AtlasStudio's first commit.

## Ownership Determination (By Area)

| Area | Authoritative Repository | Evidence |
| --- | --- | --- |
| Story canon | `TheLastSwordProtocol-Atlas` | `atlas/docs/03_Story/Story_Bible.md`, `Story_Structure_Bible.md`; Project Constitution is `status: Locked, version: 1.0`. |
| Characters | `TheLastSwordProtocol-Atlas` | `atlas/docs/05_Characters/Character_Bible.md` plus individually specified NPCs (`Grandmother_Elara.md`, `Kai.md`, `Vera.md`), each with `atlas_id`, `canonical: true` frontmatter. |
| World lore | `TheLastSwordProtocol-Atlas` | `atlas/docs/02_World/World_and_Location_Bible.md`, `Atlas_Volume_II_World_Atlas.md`, plus per-region/relay/location documents. |
| Dialogue | `TheLastSwordProtocol-Atlas` | `atlas/docs/03_Story/Dialogue/` exists as a dedicated tree; AtlasStudio has never produced scripted dialogue (by design - `WP-03A` explicitly deferred dialogue text). |
| Quests | `TheLastSwordProtocol-Atlas` | `atlas/docs/03_Story/Quests/`, referenced by ID (`QST-HOM-*`) throughout the Character Bible and screen objects. |
| Locations | `TheLastSwordProtocol-Atlas` | `atlas/docs/02_World/Locations/`, `Screens/Home_Island/` - individually specified per screen with SVG layout guides, already implemented for Ashford. |
| Gameplay philosophy | `TheLastSwordProtocol-Atlas` | `atlas/docs/00_Foundation/Studio_Manifesto.md` and `atlas/docs/04_Gameplay/Gameplay_Systems_Bible.md` already state the same Dragon Quest-inspired, hidden-technology design philosophy as AtlasStudio's `jrpg-design-bible.md`, in more detail and tied to a fantasy/hidden-reality/RPG-Maker mapping table. |
| Production planning | `TheLastSwordProtocol-Atlas` | `atlas/planning/Journey_I_Completion_Plan.md`, `workorder_queue.json` (an actively self-generating, auto-deduplicating work order pipeline) - materially more advanced than AtlasStudio's milestone/roadmap/work-breakdown documents for the same content. |
| Implementation planning | `TheLastSwordProtocol-Atlas` | `atlas/docs/09_Technical/Implementation_Packets/Home_Island/` - `IMP-HOM-017` (Ashford Exterior) and `IMP-HOM-018` (Elara House) are completed, SVG-guided, manual map-building packets already used to hand-author real maps. |
| Work orders (this project) | `TheLastSwordProtocol-Atlas` | 36 work orders (`WO-0001`-`WO-0036`) versus AtlasStudio's parallel, independently-numbered series for the same content. |
| Validation | Shared, not exclusive | `TheLastSwordProtocol-Atlas` has `atlas-tools/validator/atlas_validate.py` (schema/referential-integrity validation over its own object model). AtlasStudio has an equivalent-purpose but structurally different validator (`tools/atlas_graph/validate_graph.py`) over its own node/edge graph shape. Neither is a copy of the other; see Conflict 12. |
| Tooling | Shared, not exclusive | See Conflicts 13-15: some AtlasStudio tools (Graph Diff Engine, Immutable Formatting Guard) have no equivalent in `atlas-tools/`; others (orchestrator, work-order generation) are more mature in `TheLastSwordProtocol-Atlas`. |
| Implementation | `TheLastSwordProtocol-Game` | The only repository containing the actual RPG Maker MZ runtime project; already has 17 maps, 168 events, and a populated (if minimal) database, per `WP-02`'s audit. |
| RPG Maker assets | `TheLastSwordProtocol-Game` | `img/`, `audio/`, `effects/`, `fonts/` under this repository; AtlasStudio has never held or referenced binary game assets. |

## Conflicts

Each conflict is classified by type and given an individual recommendation with rationale, per this work order's explicit instruction not to apply a single blanket verdict.

### Conflict 1 - Protagonist Identity

**Type:** CANON
**AtlasStudio:** `character.hero`, generic "the Hero," not royalty or prophecy-based (`canon.nodes.json`).
**TheLastSwordProtocol-Atlas:** Named protagonist **Kai** (`Actors.json` slot 1; `Kai.md` character document).
**Recommendation: KEEP ATLAS.** Kai is a specific, implemented, `Actors.json`-backed identity already visible to a player today. AtlasStudio's generic "the Hero" was never implemented as a database row anywhere. There is nothing to merge - a generic placeholder yields to a specific, already-real name.

### Conflict 2 - Elara's Role

**Type:** CANON
**AtlasStudio:** Elara is "guardian and emotional anchor," implied peer/parental age, co-habits "Rowan's Cottage" per `WP-03A`.
**TheLastSwordProtocol-Atlas:** **Grandmother Elara** (`NPC-ELA-001`), explicitly a grandmother, "keeper of inherited warnings," sole resident of her own house (`INT_Ashford_ElaraHouse`), which is also Kai's starting map.
**Recommendation: KEEP ATLAS.** Grandmother Elara is a fully specified character document with defined relationships (`appears_in`, `related_to` other canonical IDs) and is already the player's starting location. AtlasStudio's version was written without knowledge of this and cannot be merged without contradicting an already-implemented start position.

### Conflict 3 - Rowan (Existence)

**Type:** CANON
**AtlasStudio:** Rowan - village elder and local historian, a fully specified major NPC across `canon.nodes.json`, `player-experience-map.md`, and `WP-03A`.
**TheLastSwordProtocol-Atlas:** No character named Rowan exists anywhere in the repository (confirmed by exhaustive search). Map001 (`TWN_Ashford_Exterior`) contains a "Village Elder Placeholder" event - unnamed and unimplemented.
**Recommendation: MERGE (conditional).** Rowan does not need to be discarded outright - the "Village Elder Placeholder" event is exactly the open slot Rowan could fill. However, this is a creative decision for `TheLastSwordProtocol-Atlas`'s own Creative Director/Production Director to make (per its own governance), not something AtlasStudio can decide for it. Recommend AtlasStudio's Rowan concept (name, personality, historian role, canon misunderstanding of the "First Relay"/ancient tech) be offered to `TheLastSwordProtocol-Atlas` as a proposal for its placeholder elder, through that repository's own work-order process - not adopted unilaterally by either side.

### Conflict 4 - Ashford Village Building Roster

**Type:** CANON / IMPLEMENTATION
**AtlasStudio:** Four buildings - Rowan's Cottage (home), General Store, Blacksmith, Inn (`WP-03A`).
**TheLastSwordProtocol-Atlas:** Three Ashford screens implemented or packeted - Elara House (Map002), Ashford Shop (Map003, one combined shop, not separate General Store/Blacksmith), and the Village Elder Placeholder is an event on the exterior map, not a separate building. No Inn found among Ashford's screens.
**Recommendation: KEEP ATLAS.** Map001 and Map002 are already hand-authored; Map003 is already generated and packeted. AtlasStudio's four-building roster describes a village that does not match what already exists in the implementation target. Building it as specified in `WP-03A` would either duplicate or directly conflict with real, in-progress work.

### Conflict 5 - Starting Location

**Type:** CANON / IMPLEMENTATION
**AtlasStudio:** Opening sequence at "Rowan's Cottage" (`player-experience-map.md`, `WP-03A`).
**TheLastSwordProtocol-Atlas / Game:** `System.json` sets `startMapId: 2` (`INT_Ashford_ElaraHouse`) at position (8, 6); Map002 already contains a `EVT-HOM-001 Player Start` autorun event.
**Recommendation: KEEP ATLAS.** The start position is already a live, working engine setting. There is no ambiguity to resolve by merging - the game already starts somewhere specific, and it is not "Rowan's Cottage."

### Conflict 6 - First Playable Hour Scope And Sequence

**Type:** PRODUCTION
**AtlasStudio:** `work-orders/WO-1000-first-playable-hour-master-plan.md` and its milestone/roadmap/work-breakdown documents define an eleven-beat first hour (opening, village, overworld, cave, shrine, sword, ruins, relay, Rustshore, departure, credits).
**TheLastSwordProtocol-Atlas:** `atlas/planning/Journey_I_Completion_Plan.md` defines the equivalent "Journey I" production plan, already broken into implementation packets and Build Gates, already partially executed (Ashford screens) and validated with a working CLI.
**Recommendation: DEPRECATE (AtlasStudio's version).** Both describe essentially the same beat sequence (Village, Overworld, Hidden Cave, Sword Shrine, Glassfield Ruins, Relay, Rustshore, Departure) with different character names and different production tooling. `TheLastSwordProtocol-Atlas`'s plan is further along and already the one the actual game repo is built against. AtlasStudio's `WO-1000` and its production documents should be marked historical/deprecated for this project rather than treated as a live plan - see `atlas-v1-to-atlas-v2-migration.md`.

### Conflict 7 - Skyreach Hill / Fogfen Marsh Geography

**Type:** CANON
**AtlasStudio:** Canon graph has no Skyreach Hill node at all. Fogfen Marsh is documented in `world-model.md`/`home-region.md` as explicitly optional/deferred content, not an implemented route.
**TheLastSwordProtocol-Atlas:** Skyreach Hill is an implemented dungeon/path screen (`SCR-HOM-SKY-001`, Map004) with a live transfer from Ashford Exterior (`TRN-HOM-005`). Fogfen Marsh is also implemented (`SCR-HOM-FOG-001/002`, Maps 15-16), reachable via an "optional" transfer (`TRN-HOM-027`) already present on Map001.
**Recommendation: KEEP ATLAS.** AtlasStudio simply has an incomplete picture of the region's geography relative to what already exists and is playable. There is no competing claim to adjudicate - AtlasStudio's canon graph should be updated (as historical documentation, not active canon) to acknowledge this gap rather than presented as if it were complete.

### Conflict 8 - Map Ownership / Ledger Authority

**Type:** IMPLEMENTATION
**AtlasStudio:** `bridges/rpg-maker-mz/ownership-model.md` defines its own generated/agent-drafted/human-edited/hand-authored/locked ownership states, designed independently.
**TheLastSwordProtocol-Atlas / Game:** `map_ownership.json` in the game repository is the real, already-enforced ledger (`generated`, `hand_authored`, `locked`), consulted by write-capable pipeline scripts today, with a documented one-way state-transition rule and a fail-safe default.
**Recommendation: KEEP ATLAS (for this project).** The real ledger already exists and is already load-bearing; AtlasStudio's parallel ownership model, while conceptually compatible (both use a generated/hand-authored/locked-style spectrum), was never connected to it and should not be treated as authoritative for `TheLastSwordProtocol-Game`. AtlasStudio's ownership-model document remains useful as a general Atlas Core methodology reference for future projects, but should not be cited as governing this game's actual maps.

### Conflict 9 - Completed Work Orders (Numbering And Content)

**Type:** PRODUCTION / DOCUMENTATION
**AtlasStudio:** `WO-0001` through `WO-0018` (this one), independently numbered.
**TheLastSwordProtocol-Atlas:** `WO-0001` through `WO-0036`, independently numbered, already tracking 24+ completed and several open.
**Recommendation: KEEP ATLAS (for this project's execution record), ARCHIVE AtlasStudio's series as this-project history.** The two numbering series are not comparable or mergeable - they are different systems' independent histories. `TheLastSwordProtocol-Atlas`'s series is the real execution record for the actual game. AtlasStudio's series remains a valid historical record of what this repository did, but should not be read as a parallel or competing production history for the shipped game going forward.

### Conflict 10 - Gameplay Philosophy Documents

**Type:** DOCUMENTATION
**AtlasStudio:** `jrpg-design-bible.md`, `exploration-principles.md`, `pacing-guidelines.md`, `anti-patterns.md`.
**TheLastSwordProtocol-Atlas:** `Studio_Manifesto.md` (explicit "We Respect Dragon Quest Without Copying It" section) and `Gameplay_Systems_Bible.md` (fantasy/hidden-reality/RPG-Maker mapping table).
**Recommendation: MERGE, in spirit, but no file action required now.** Both documents independently arrived at nearly identical design philosophy (Dragon Quest as principle-source, not mechanic-source; hidden technology beneath fantasy; avoid copying Dragon Quest directly). This is a case of convergent design instinct, not real disagreement. `TheLastSwordProtocol-Atlas`'s version should be treated as authoritative for this project since it is already tied into its Gameplay Systems Bible's implementation mapping. AtlasStudio's documents remain valid, well-written, project-agnostic design methodology and may be offered as a proposal to strengthen `TheLastSwordProtocol-Atlas`'s own manifesto, but that is a future, separate, cross-repository proposal - not an action this work order takes.

### Conflict 11 - Cybersecurity Metaphor Framing

**Type:** DOCUMENTATION / CANON
**AtlasStudio:** `game-vision.md`'s "Cybersecurity Fantasy Layer" and `anti-patterns.md`'s "Cybersecurity Integration" section describe authentication, access control, trust, and recovery metaphors in general terms.
**TheLastSwordProtocol-Atlas:** `atlas/docs/09_Technical/Cybersecurity_Layer_Bible.md` - a dedicated, presumably more detailed bible for exactly this layer, tied to specific relays, states (`Signal-Slick`, `Pulse Guard`, `Charging` are already implemented `States.json` rows), and named systems.
**Recommendation: KEEP ATLAS.** The dedicated Cybersecurity Layer Bible is more specific and already tied to implemented database rows. AtlasStudio's framing remains a valid general statement of intent but should defer to the dedicated bible for this project's specifics.

### Conflict 12 - Validation Tooling Approach

**Type:** TOOLING
**AtlasStudio:** `tools/atlas_graph/validate_graph.py` validates a JSON node/edge graph (required fields, unique IDs, resolvable edges, source paths).
**TheLastSwordProtocol-Atlas:** `atlas-tools/validator/atlas_validate.py` validates a frontmatter-embedded object model (`atlas_id`, `dependencies`, `related`, `canonical`, `status` fields inside Markdown documents), with an active referential-integrity upgrade in progress (`WO-0034`).
**Recommendation: KEEP BOTH (not a real conflict).** These validate structurally different representations of canon (a separate JSON graph vs. frontmatter-embedded relationships) and neither is a copy of the other. For this project, `TheLastSwordProtocol-Atlas`'s validator is authoritative because its representation is the one actually governing implemented canon. AtlasStudio's validator remains legitimate Atlas Core tooling for any project that chooses AtlasStudio's separate-JSON-graph representation in the future.

### Conflict 13 - Graph Diff / Change Review Tooling

**Type:** TOOLING
**AtlasStudio:** `tools/atlas_graph/diff_graph.py` - compares two graph states and reports added/removed/changed facts by scope.
**TheLastSwordProtocol-Atlas:** No equivalent tool found in `atlas-tools/`.
**Recommendation: KEEP ATLASSTUDIO, propose for adoption.** This is a genuine, non-redundant AtlasStudio contribution. It has no counterpart in `TheLastSwordProtocol-Atlas`'s toolchain. Recommend it be offered as a proposal to that repository's own Production Director for potential adoption against its frontmatter-object-model representation - a future, separate cross-repository proposal, not a unilateral port performed here.

### Conflict 14 - Immutable Formatting Guard

**Type:** TOOLING
**AtlasStudio:** `tools/atlas_format/format_guard.py` - detects formatting-only churn vs. semantic change in graph JSON.
**TheLastSwordProtocol-Atlas:** No equivalent tool found; its canon lives in Markdown frontmatter, where this specific JSON-churn detection approach would need adaptation, not direct reuse.
**Recommendation: KEEP ATLASSTUDIO, propose for adaptation.** Same reasoning as Conflict 13 - genuine, non-redundant, but any adoption requires adapting the detection approach to Markdown/frontmatter rather than porting the tool as-is.

### Conflict 15 - Work-Order Generation And Orchestration

**Type:** TOOLING / PRODUCTION
**AtlasStudio:** `tools/atlas_planner/` (recommends next work, evidence-scored, never auto-creates) and a capability-based orchestration *design* (`studio/orchestration/`, `atlas-core/capabilities/`, `atlas-core/providers/` - documented but not executable).
**TheLastSwordProtocol-Atlas:** `atlas-tools/generators/workorder_next.py` (auto-generates work orders from a candidate queue, with duplicate detection - already caused and self-corrected a real duplicate-generation incident, per `workorder_queue.json`'s own completion notes) and `atlas-tools/orchestrator/` (`recommend_assignment.py`, `audit_workorders.py`, `session_report.py` - an actually-executable orchestrator, not just a design).
**Recommendation: KEEP ATLAS for this project; KEEP ATLASSTUDIO's design as a governance reference.** `TheLastSwordProtocol-Atlas`'s orchestrator is more mature (executable, already in production use) for this project. AtlasStudio's capability-based orchestration design is more explicit about *why* (the ADR-tracked shift from named-agent scheduling to capability-first routing) and remains valuable as governance methodology, independent of which tool executes it.

### Conflict 16 - "Atlas v1" Terminology Confusion

**Type:** DOCUMENTATION
**AtlasStudio:** `README.md` and `studio/vision.md` describe AtlasStudio as succeeding a single prior "Atlas v1," implying a clean, one-step lineage.
**Reality (per chronology above):** there were two prior systems - `rpgmakerLSP` (the true original monolith) and `TheLastSwordProtocol-Atlas`/`TheLastSwordProtocol-Game` (an already-completed clean split of that monolith, itself unaware of AtlasStudio). AtlasStudio's "Atlas v1" framing conflates or omits the intermediate, already-successful split.
**Recommendation: UPDATE AtlasStudio's own documentation** (not the other repositories) to correct this framing - see `atlas-v1-to-atlas-v2-migration.md`, which uses precise names (Legacy Prototype, Atlas, AtlasStudio) instead of an ambiguous "v1"/"v2" shorthand going forward.

## Summary Table

| # | Conflict | Type | Recommendation |
| --- | --- | --- | --- |
| 1 | Protagonist identity | CANON | KEEP ATLAS |
| 2 | Elara's role | CANON | KEEP ATLAS |
| 3 | Rowan (existence) | CANON | MERGE (conditional, via Atlas's own process) |
| 4 | Ashford building roster | CANON/IMPLEMENTATION | KEEP ATLAS |
| 5 | Starting location | CANON/IMPLEMENTATION | KEEP ATLAS |
| 6 | First Playable Hour scope/sequence | PRODUCTION | DEPRECATE (AtlasStudio's) |
| 7 | Skyreach Hill / Fogfen Marsh geography | CANON | KEEP ATLAS |
| 8 | Map ownership/ledger authority | IMPLEMENTATION | KEEP ATLAS (for this project) |
| 9 | Completed work orders (numbering) | PRODUCTION/DOCUMENTATION | KEEP ATLAS (execution record); ARCHIVE AtlasStudio's series |
| 10 | Gameplay philosophy documents | DOCUMENTATION | MERGE in spirit; KEEP ATLAS authoritative |
| 11 | Cybersecurity metaphor framing | DOCUMENTATION/CANON | KEEP ATLAS |
| 12 | Validation tooling approach | TOOLING | KEEP BOTH (not a real conflict) |
| 13 | Graph diff/change review tooling | TOOLING | KEEP ATLASSTUDIO, propose adoption |
| 14 | Immutable Formatting Guard | TOOLING | KEEP ATLASSTUDIO, propose adaptation |
| 15 | Work-order generation/orchestration | TOOLING/PRODUCTION | KEEP ATLAS (execution); keep AtlasStudio design as reference |
| 16 | "Atlas v1" terminology confusion | DOCUMENTATION | UPDATE AtlasStudio's own docs |

No conflict above was resolved by silently picking a side without evidence; each cites the specific file, field, or implemented state that grounds the recommendation.
