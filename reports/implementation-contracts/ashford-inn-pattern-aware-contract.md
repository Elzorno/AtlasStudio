# Ashford Inn - Pattern-Aware Implementation Contract

Status: submitted

> This is a live, authoritative AtlasStudio implementation contract, built under `studio/contracts/PATTERN_CONTRACT_SPEC.md` (`WO-0027`)'s pattern-aware format. Unlike `reports/implementation-contracts/ashford-shop-pattern-aware-contract.md` (an illustrative demonstration layered over an already-existing plain contract), this document is the sole implementation contract for Ashford Inn - no separate WO-0020-era contract exists for this build, since Ashford Inn is new. It does not modify `TheLastSwordProtocol-Game` and does not modify Atlas canon. It executes `IMP-HOM-020`, which now exists in `TheLastSwordProtocol-Atlas`, superseding the earlier draft of this contract that treated `IMP-HOM-020` as missing (see Revision Note below).

**Revision note:** An earlier draft of this contract (same file path) was written before `IMP-HOM-020` existed and correctly refused to invent the missing packet's requirements, gating execution instead. `IMP-HOM-020`, `SCR-HOM-ASH-004`, and `DDR-0005` now exist in `TheLastSwordProtocol-Atlas` (`WO-0044`; renumbered from a duplicate `WO-0038` slot). This revision replaces that draft's provisional content with the real packet's actual, approved requirements.

---

## 1. Project

`the-last-sword-protocol`.

## 2. Implementation Target

| Target | Current state | Contract role |
|---|---|---|
| `TheLastSwordProtocol-Game/data/MapXXX.json` (`INT_Ashford_Inn`, proposed, exact number unassigned) | File does not exist. No map number is reserved in `map_ownership.json` as of 2026-07-08. Tracked product maps occupy `1`-`16`; `50` is `JRN2_Landing_Placeholder`; `17`-`25` are untracked official sample maps (read-only reference, not ledger targets). | Proposed Inn interior build target. This contract does not assign a map number - per `repository-authority.md`'s principle that AtlasStudio does not choose Game-repo file paths (the identical principle `IMP-HOM-020` states on the Atlas side), the next unreserved sequential number is illustrative only, not a decision. Assigning one and adding it to `map_ownership.json` in an explicitly writable state (`generated`) is a Game-repo-side execution step that must happen before any write. |
| `TheLastSwordProtocol-Game/data/MapInfos.json` | No `INT_Ashford_Inn` entry exists | An entry must be added only after a map number is approved and reserved. |
| `TheLastSwordProtocol-Game/map_ownership.json` | No entry for the Inn's future map number | Fail-safe: a missing ledger entry means no write is permitted, per `bridges/rpg-maker-mz/ownership-model.md`. |
| `TheLastSwordProtocol-Game/data/Map001.json` (`TWN_Ashford_Exterior`) | `hand_authored` | Exterior-side Inn entrance transfer (`TRN-HOM-031`) target. Protected: this is additive event work on a `hand_authored` map and requires explicit approval before any edit, per `ownership-model.md`'s `hand-authored` behavior ("request approval before edits"). Existing layout, tiles, protected events, and ownership state must not otherwise change. |
| `TheLastSwordProtocol-Game/data/Map020.json` (`Inn`, official sample) | Official RPG Maker MZ sample map, `Inside` tileset, 20x17 | Read-only pattern evidence for `PAT-INTERIOR-INN`. Not the build target; never written to. |

Ownership restrictions are governed by `bridges/rpg-maker-mz/ownership-model.md` and the live Game-repo ledger, re-checked at execution time, not assumed from this contract's drafting-time snapshot.

## 3. Creative Authority

| File | Role |
|---|---|
| `../TheLastSwordProtocol-Atlas/atlas/docs/09_Technical/Implementation_Packets/Home_Island/IMP_HOM_020_Manual_Map_Build_Ashford_Inn.md` (`IMP-HOM-020`) | **Primary authoritative implementation packet.** Exists, `canonical: true`, `owner: Technical Director`. |
| `../TheLastSwordProtocol-Atlas/atlas/docs/02_World/Screens/Home_Island/SCR_HOM_ASH_004_Ashford_Inn.md` (`SCR-HOM-ASH-004`) | Screen object: purpose, map intent, required elements, acceptance criteria. |
| `../TheLastSwordProtocol-Atlas/atlas/docs/99_Reference/Decision_Records/DDR-0005_Ashford_Inn.md` (`DDR-0005`) | Decision Record authorizing the Inn's existence, its building-submap shape, and its free-rest design. |
| `../TheLastSwordProtocol-Atlas/atlas/docs/03_Story/Dialogue/Home_Island/Ashford_Dialogue_Packet.md` (`ATLAS-STY-010`) | Innkeeper dialogue source (Intro / After Tremor / After Node Seven). |
| `../TheLastSwordProtocol-Atlas/atlas/docs/09_Technical/Registries/Home_Island_Event_Registry.md` | Canonical event ID `EVT-HOM-032` (Innkeeper). |
| `../TheLastSwordProtocol-Atlas/atlas/docs/09_Technical/Registries/Home_Island_Transfer_Registry.md` | Canonical transfers `TRN-HOM-031` (entrance), `TRN-HOM-032` (exit). |
| `../TheLastSwordProtocol-Atlas/atlas/docs/09_Technical/Asset_Mapping/Home_Island_Tileset_Assignment_Matrix.md` | Tileset family (`Inside`) and counter/bed-alcove collision assignment for `SCR-HOM-ASH-004`. |
| `../TheLastSwordProtocol-Atlas/atlas/docs/05_Characters/NPCs/Home_Island/Ashford_NPC_Roster.md` | Canon placeholder NPC ID `NPC-ASH-INN-001` (Innkeeper), unnamed. |

No Atlas canon file is changed by this contract. `NPC-ASH-INN-001` remains unnamed per Atlas's own roster; see Section 7 for how this reconciles with AtlasStudio's own pre-existing, explicitly non-canon production label "Tomas."

## 4. Implementation Packet

`../TheLastSwordProtocol-Atlas/atlas/docs/09_Technical/Implementation_Packets/Home_Island/IMP_HOM_020_Manual_Map_Build_Ashford_Inn.md` (`IMP-HOM-020`).

Per this specification's "point, don't paraphrase" convention, this document does not restate `IMP-HOM-020` at length - its concrete requirements (tileset, size, required visual elements, required events, rest processing, required transfers, story states, ownership expectations) are cited by reference and pulled into `Implementation Guidance` and `Acceptance Criteria` below only where needed to show how they interact with pattern-derived guidance.

`IMP-HOM-020` itself notes two open items this contract inherits rather than resolves: no SVG layout guide yet exists for `SCR-HOM-ASH-004`, and no Game-repo map number is yet reserved. Both remain execution prerequisites, not blockers to writing this contract.

## 5. Environment Pattern

**Interior** - virtual layer. No `studio/design-patterns/interiors/interior.pattern.md` document exists yet (`PATTERN_INHERITANCE_MODEL.md`, "Materialized vs. Virtual Nodes"). Its evidence lives in `reports/design-patterns/interior-pattern-corpus-review.md`'s recurring-findings sections, corroborated across all eight interiors analyzed to date (Item Shop, House 1, House 2, Inn, Weapon & Armor Shop, Bar, Chief's House 1F/2F) - including the `Inn` sample itself, which contributes to both this Environment layer and Section 6's Specialization layer.

**Confidence: High**, per the same eight-source corroboration `ashford-shop-pattern-aware-contract.md` already cites for this layer.

## 6. Specialization Pattern

**Inn** - `studio/design-patterns/interiors/inn.pattern.md` v1.0 (`PAT-INTERIOR-INN`).

**Confidence: Medium**, matching the pattern's own current frontmatter (one corroborating official sample map, `Map020.json`). This contract does not promote it.

**Required Conditions check (per `PATTERN_APPLICATION_GUIDE.md`'s citation discipline and `PATTERN_APPLICATION_CHECKLIST.md`'s "Pattern conflicts checked" / "Exceptions documented" items):** `inn.pattern.md`'s Required Conditions state the pattern applies only to an interior "larger than a single small room" that "combines at least two functionally distinct zones under one roof," explicitly adding: "If the building is a genuinely single-room space, use `shop.pattern.md` or `house.pattern.md` instead." `IMP-HOM-020` approves a single common room with bed alcoves implying privacy, explicitly stating "do not build a multi-room inn with separate private bedrooms." **This build does not satisfy `PAT-INTERIOR-INN`'s Required Conditions.** See Section 7 for how this exception is recorded and resolved.

## 7. Project Pattern

No project-specific `the-last-sword-protocol` pattern currently exists under `studio/design-patterns/projects/`.

**Project-specific exception, recorded here per `PATTERN_RESOLUTION_RULES.md`'s "Exceptions" rule** ("a layer whose Required Conditions are unmet is skipped entirely, not partially applied... the citation must either choose a different pattern or explicitly document why the mismatch is acceptable for this one build"):

`IMP-HOM-020`'s approved single-room design does not meet `PAT-INTERIOR-INN`'s Required Conditions (see Section 6). `house.pattern.md` is not a better-fitting substitute either - its own Required Conditions exclude "commerce, lodging-for-hire" explicitly, and an inn is lodging-for-hire by definition. **No Specialization-tier pattern currently in the library matches "single-room lodging-for-hire."** Rather than force a citation that does not resolve, this contract:

- Names `Inn` as the closest-by-function Specialization pattern for traceability, but does **not** apply its Layout/Composition/Passability Rules that depend on the two-zone (common room + guest wing + spine corridor) structure - those rules are skipped entirely, per the Exceptions rule, not partially applied.
- Draws on `Inn`'s non-zone-dependent observations (the wall-mounted decorative flame convention; general lodging tone) only as non-binding **Implementation Recommendations** in Section 9, exactly as `ashford-shop-pattern-aware-contract.md` already does when citing `Inn` illustratively without treating it as a governing layer.
- Flags this as a genuine Design Pattern Library gap worth a future `WO-0025`-style corpus extension: Ashford Inn is unlikely to be the last small, single-room lodging interior this project needs, and no existing pattern currently covers that shape.

AtlasStudio's own pre-existing production package for Ashford Village (`projects/the-last-sword-protocol/production/ashford-village-event-plan.md`, `ashford-village-map-brief.md`, from `WP-03`) independently envisioned a fuller, two-zone Inn matching `PAT-INTERIOR-INN`'s Required Conditions more closely, with a production-only (explicitly "not yet canon") Innkeeper name, **Tomas**. That package predates `IMP-HOM-020` and is not Atlas canon; per this project's repository authority (Atlas is sole creative/technical authority for game content), `IMP-HOM-020`'s actual approved single-room design controls this contract wherever the two differ - the two-zone vision is not implemented. "Tomas" is retained here only as AtlasStudio's own non-canon production label for `NPC-ASH-INN-001` (see Section 9), not as a claim that Atlas has named the character. A future work order should reconcile `WP-03`'s production package against `IMP-HOM-020` now that the latter exists, since the production package is now stale on this point - out of scope for this contract to fix.

## 8. Pattern Resolution

```text
Creative Authority (IMP-HOM-020, SCR-HOM-ASH-004, DDR-0005, ATLAS-STY-010, registries)
    |
    v
Environment Pattern: Interior (virtual, High) - resolves normally
    |
    v
Specialization Pattern: Inn (PAT-INTERIOR-INN v1.0, Medium) - Required Conditions unmet, SKIPPED per recorded exception (Section 7)
    |
    v
Project Pattern: none authored - layer skipped; exception recorded here instead
    |
    v
Implementation Packet: IMP-HOM-020 - applied last, controls throughout
    |
    v
Final Implementation Guidance
```

- **Creative Authority** is a boundary condition. No pattern layer or recommendation in this contract may contradict `IMP-HOM-020`, `SCR-HOM-ASH-004`, or `DDR-0005`. No conflict was found.
- **Environment Pattern (Interior)** contributes the operative pattern-derived guidance for this build, since the Specialization layer does not resolve: compact shell inside a void border, the stairs-tile-plus-transfer-event threshold construction, region-free passability with zero encounters.
- **Specialization Pattern (Inn)** does not resolve for this build (Section 6/7). Its zone-dependent rules are not applied. Its non-zone-dependent observations are cited only as non-binding recommendations.
- **Project Pattern** contributes nothing beyond the recorded exception itself.
- **Implementation Packet (IMP-HOM-020)** is layered last and wins wherever it states something more specific than the (reduced) pattern chain: the exact 16x12 size, the counter/bed-alcove/warm-stone-vent element list, the free Rest/Talk choice on `EVT-HOM-032`, the three named story states on already-existing switches, and the explicit non-goal against adding a shop, inventory, or gold cost.
- No undeclared contradiction was found between Creative Authority and the Environment layer. The one real tension found (Specialization layer's Required Conditions) is declared, not silently resolved, per this project's checklist discipline.

## 9. Implementation Guidance

**Authoritative requirements** (from `IMP-HOM-020` / `SCR-HOM-ASH-004` - non-negotiable):

- Map size ~16x12 tiles.
- Reception counter near the entrance, on the Innkeeper's interaction axis; blocks on every side except that side.
- Two to three bed alcoves along a back or side wall, implying private rooms without building them - explicitly not a multi-room build.
- A warm-stone vent or small hearth, per Ashford's established village motif.
- `EVT-HOM-032` (Innkeeper, `NPC-ASH-INN-001`): dialogue plus a two-option choice, **Rest** (free full-party HP/MP restore, no gold cost, no Shop Processing) or **Talk** (dialogue only).
- `TRN-HOM-031` (Map001 → Inn, entrance) and `TRN-HOM-032` (Inn → Map001, exit), round-tripping at a landmark distinct from the Shop and Elara House doors.
- Story states `Intro` / `After Tremor` / `After Node Seven`, driven by already-existing switches `J1_Tremor_Event`, `J1_Node07_Offline`, `NPC_Ashford_PostNode07` - no new switch is introduced.
- Tileset family `Inside`; Region 0 only; zero random encounters.
- Explicit non-goals from `IMP-HOM-020`: no shop, no inventory, no gold cost on Rest; no SVG guide fabricated if none exists yet; no automatic final map construction.

**Pattern-derived guidance** (from `Interior` only, the sole pattern layer that resolves - binding by default, lower precedence than the above where they overlap, revisable through `PATTERN_REVIEW_PROCESS.md`):

- Compact architectural shell inside a void/darkness border.
- Visible threshold tile (stairs-family) one row above the floor tile carrying the exit transfer event, shadow value marking the recess.
- Player spawn one tile inside the doorway on entry.
- Region-free passability outside the counter/alcove furniture; zero encounters (already stated as authoritative above; the pattern layer independently corroborates it).

**Implementation recommendations** (non-binding; deviate freely with a stated reason):

- A single wall-mounted decorative flame near the bed alcoves, borrowed illustratively from `inn.pattern.md`'s wall-sconce composition observation - not binding, since the Specialization layer does not resolve for this build, but a reasonable way to add atmosphere consistent with the pattern corpus's general lodging tone.
- For AtlasStudio-internal production tracking only (not a canon or build requirement): the placeholder Innkeeper may be referred to informally as "Tomas," matching `projects/the-last-sword-protocol/design/ashford-village-experience-specification.md`'s existing, explicitly non-canon production label for this same role. The binding canon ID remains `NPC-ASH-INN-001`, unnamed, per `Ashford_NPC_Roster.md`. Do not surface "Tomas" in any player-facing text or event without a future Atlas naming decision.
- An optional background "passing traveler" NPC in the common room, per `ashford-village-event-plan.md`'s optional suggestion - not required by `IMP-HOM-020`, and only worth adding if it does not complicate the single-room reachability/passability requirements above.

## 10. Passability Rules

Combining `IMP-HOM-020`'s explicit collision statement with the `Interior` layer's general connectivity rule, per `bridges/rpg-maker-mz/passability-rule.md`:

- Tileset family `Inside`; Region 0 only; zero encounters (`IMP-HOM-020`, authoritative).
- Counter blocks on every side except the Innkeeper's interaction side (`IMP-HOM-020`, authoritative).
- Bed alcoves block; exit tile clear (`IMP-HOM-020`, authoritative).
- Full walkable set forms a single connected area reachable from the entrance, door-to-counter path clear (`IMP-HOM-020` requirement, reinforced by the `Interior` layer's general connectivity rule).
- Reciprocal transfer check: `TRN-HOM-031` (entrance) and `TRN-HOM-032` (exit) round-trip correctly (`IMP-HOM-020`, authoritative).
- Do not edit `Tilesets.json` or override default tileset passability, per `passability-rule.md`'s Core Rule.

Required route validation, per `passability-rule.md`, "Route Validation":

```text
exterior_inn_door -> inn_arrival_tile
inn_arrival_tile -> counter (Innkeeper interaction side)
counter -> bed_alcove_area (reachable, not necessarily interactable)
counter -> inn_exit_transfer
inn_exit_transfer -> exterior_return_tile
```

## 11. Required Transfers, Events, and NPCs

| ID | Location | Requirement |
|---|---|---|
| `TRN-HOM-031` | `Map001` exterior, Inn door | Player-touch transfer from Ashford Exterior into the Inn map. Protected: `Map001` is `hand_authored`; requires explicit additive-event approval before implementation. Landmark distinct from the Shop and Elara House doors. |
| `TRN-HOM-032` | Inn map, door/threshold | Player-touch transfer from Inn back to Ashford Exterior. Must round-trip with `TRN-HOM-031`. |
| `EVT-HOM-032` | Inn map, at the reception counter | Innkeeper (`NPC-ASH-INN-001`), fixed placement, Action Button interaction. Offers Rest (free full-party HP/MP restore) or Talk (dialogue by story state, text from `ATLAS-STY-010`). |
| Decorative flame (optional) | Inn map, near bed alcoves | Atmosphere only, no gameplay commands - Implementation Recommendation, not required. |
| Passing traveler NPC (optional) | Inn map, common area | Optional background texture per `ashford-village-event-plan.md` - Implementation Recommendation, not required by `IMP-HOM-020`. |

Final RPG Maker event numbers are implementation detail and should not replace these Atlas/AtlasStudio IDs in any report, per `Home_Island_Event_Registry.md`'s own Validation Rules.

## 12. Validation Requirements

```bash
# Confirm live state before any write is attempted:
git -C ../TheLastSwordProtocol-Game status --porcelain
python3 -c "import json; d=json.load(open('../TheLastSwordProtocol-Game/map_ownership.json')); print(sorted(int(k) for k in d['maps']))"
```

- Confirm the Inn's map number is reserved in `map_ownership.json` in an explicitly writable state (`generated`) before any write, per `ownership-model.md`.
- Confirm no protected `Map001` tile, layout, or event was changed except the approved additive `TRN-HOM-031` entrance transfer.
- Route validation at minimum for every route listed in Section 10, per `passability-rule.md`, "Route Validation."
- Automated JSON inspection confirms structural placement, not tile-level walkability feel - **a human playtest pass is still required** before acceptance, per `passability-rule.md`, "Human Playtest Still Required": enter from Ashford Exterior, confirm the Innkeeper's Rest and Talk choices both work, walk the room, exit, and confirm visual boundaries match collision.
- Re-check, at execution time, that `inn.pattern.md`'s frontmatter still reads `confidence: medium`, that `IMP-HOM-020`'s content has not changed since this contract was drafted, and that no `studio/design-patterns/projects/` pattern for Ashford Village or the-last-sword-protocol has since been authored - all three could change between this document being written and any future execution, per `PATTERN_APPLICATION_CHECKLIST.md`, "Pattern confidence recorded."

## 13. Acceptance Criteria

Reproduced from `IMP-HOM-020` (authoritative):

1. Entry works - `TRN-HOM-031` places the player inside the Inn near the door.
2. Innkeeper is interactable across the counter - `EVT-HOM-032` fires from the customer side; the counter blocks movement but not interaction.
3. Rest choice works - fully restores the party's HP/MP with no gold cost, or an explicit placeholder message if not yet wired. A silent or broken Rest choice is a fail.
4. Talk choice works - shows current story-state dialogue without altering party state.
5. Landmarks present - counter, bed alcoves, warm-stone vent/hearth visually distinct.
6. Collision correct - counter/alcoves block; door-to-counter path clear.
7. Exit works - `TRN-HOM-032` returns the player to Ashford Exterior, round-tripping with `TRN-HOM-031`.
8. No random encounters.
9. Story states - Innkeeper dialogue reflects Intro / After Tremor / After Node Seven.

**This contract's additional execution gates** (not in `IMP-HOM-020`, required by this contract before Section 13's criteria can even be tested):

10. A map number is reserved for the Inn in `map_ownership.json` and `MapInfos.json`, in an explicitly writable state, before any write.
11. `TRN-HOM-031`'s addition to `Map001` is explicitly approved as additive work against a `hand_authored` map, per `ownership-model.md`.

## 14. Recommended Implementation Agent

**Codex** (`implementation-engineer`).

Rationale, per `studio/operations/AGENT_USAGE_GUIDE.md`: this is a well-scoped, already-specified RPG Maker map/event build (one new interior map plus one additive transfer on an existing hand-authored map), matching the exact shape of Codex's prior Ashford Shop assignment (`IMP-HOM-019`/`WO-0023`-family work) - a fully scoped implementation contract exists to execute against, not an open-ended design task. `risk_level: medium` reflects the `Map001` additive-edit approval gate (Section 11, item 11), not the Inn map's own build, which is low-risk and fully specified. Any dialogue expansion beyond `ATLAS-STY-010`'s scaffold, or any decision to name the Innkeeper, routes back to Atlas/human review rather than being decided by Codex inside the Game repo.

## 15. References

**Atlas:**

- `atlas/docs/09_Technical/Implementation_Packets/Home_Island/IMP_HOM_020_Manual_Map_Build_Ashford_Inn.md` (`IMP-HOM-020`)
- `atlas/docs/02_World/Screens/Home_Island/SCR_HOM_ASH_004_Ashford_Inn.md` (`SCR-HOM-ASH-004`)
- `atlas/docs/99_Reference/Decision_Records/DDR-0005_Ashford_Inn.md` (`DDR-0005`)
- `atlas/docs/03_Story/Dialogue/Home_Island/Ashford_Dialogue_Packet.md` (`ATLAS-STY-010`)
- `atlas/docs/09_Technical/Registries/Home_Island_Event_Registry.md`, `Home_Island_Transfer_Registry.md`, `Home_Island_Screen_Registry.md`
- `atlas/docs/09_Technical/Asset_Mapping/Home_Island_Tileset_Assignment_Matrix.md`
- `atlas/docs/05_Characters/NPCs/Home_Island/Ashford_NPC_Roster.md`

**Patterns and contract format:**

- `studio/contracts/PATTERN_CONTRACT_SPEC.md`, `PATTERN_APPLICATION_CHECKLIST.md`
- `studio/design-patterns/PATTERN_INHERITANCE_MODEL.md`, `PATTERN_RESOLUTION_RULES.md`, `PATTERN_APPLICATION_GUIDE.md`, `PATTERN_CONFIDENCE_MODEL.md`
- `studio/design-patterns/interiors/inn.pattern.md` v1.0, `house.pattern.md` v1.0 (evaluated, not cited - see Section 7)
- `reports/design-patterns/interior-pattern-corpus-review.md`

**RPG Maker bridge and Game-state sources:**

- `bridges/rpg-maker-mz/ownership-model.md`, `passability-rule.md`, `map-quality-standard.md`
- `../TheLastSwordProtocol-Game/map_ownership.json`, `data/MapInfos.json` (read-only)
- `../TheLastSwordProtocol-Game/data/Map020.json` (read-only sample pattern evidence)

**AtlasStudio production context (non-canon, referenced not followed where it conflicts with IMP-HOM-020):**

- `projects/the-last-sword-protocol/design/ashford-village-experience-specification.md`
- `projects/the-last-sword-protocol/production/ashford-village-map-brief.md`, `ashford-village-event-plan.md`, `ashford-village-implementation-checklist.md`

**Related contracts/work orders:**

- `reports/implementation-contracts/ashford-shop-pattern-aware-contract.md` - the illustrative demonstration this format was proven against.
- `work-orders/WO-0027-pattern-aware-implementation-contracts.md` - defined this contract format.
- `work-orders/WP-ASHFORD-INN-contract.md` - this contract's own work order wrapper.
