# Ashford Shop - Pattern-Aware Implementation Contract (DEMONSTRATION)

> **This is a demonstration document, not a live implementation contract.** It shows what an Ashford Shop build contract looks like under `studio/contracts/PATTERN_CONTRACT_SPEC.md` (`WO-0027`). It does **not** replace, supersede, or authorize execution in place of `reports/implementation-contracts/ashford-shop-build-contract.md` (`WO-0020`), which remains the sole authoritative contract for building `TheLastSwordProtocol-Game/data/Map003.json`. Nothing in this document grants write access to any target, and no map ownership ledger state was checked or changed to produce it. Where this document's content overlaps the real contract's, it is reproduced for illustration, not restated as a second, competing authorization.

---

## 1. Project

`the-last-sword-protocol`.

## 2. Implementation Target

`TheLastSwordProtocol-Game/data/Map003.json` (`INT_Ashford_Shop`).

Ownership state as of `WO-0020`/`ashford-shop-build-contract.md` (`../TheLastSwordProtocol-Game/map_ownership.json`, per `bridges/rpg-maker-mz/ownership-model.md`): `generated` at contract-issue time, to be flipped to `hand_authored` the moment manual editor work begins, per `../TheLastSwordProtocol-Game/AGENTS.md`'s ledger rule. **This demonstration does not re-check the ledger's current live state** - a real contract execution must re-verify it directly before any write, per this specification's own `PATTERN_APPLICATION_CHECKLIST.md` ("Ownership/ledger state is current").

## 3. Creative Authority

| File | Role |
|---|---|
| `atlas/docs/02_World/Screens/Home_Island/SCR_HOM_ASH_003_Ashford_Shop.md` | Screen object: purpose, required elements, acceptance criteria. |
| `atlas/docs/03_Story/Dialogue/Home_Island/Ashford_Dialogue_Packet.md` (`ATLAS-STY-010`) | Shopkeeper dialogue source. |
| `atlas/docs/09_Technical/Registries/Home_Island_Event_Registry.md` | Canonical event ID `EVT-HOM-008` (Shopkeeper). |
| `atlas/docs/09_Technical/Registries/Home_Island_Transfer_Registry.md` | Canonical transfers `TRN-HOM-003` (entrance), `TRN-HOM-004` (exit). |
| `atlas/docs/09_Technical/Home_Island_Tileset_Assignment_Matrix.md` | Tileset family and counter/shelf collision assignment. |

Two open questions remain Atlas-side and are not resolved by this document or by `ashford-shop-build-contract.md`: whether an antidote is stocked (depends on whether early Marsh Gel poison is enabled) and whether the inventory changes after Node Seven. Both stay open here exactly as they do in the real contract.

## 4. Implementation Packet

`atlas/docs/09_Technical/Implementation_Packets/Home_Island/IMP_HOM_019_Manual_Map_Build_Ashford_Shop.md` (`IMP-HOM-019`, `canonical: true`, `owner: Technical Director`).

Per this specification's "point, don't paraphrase" convention, this document does not restate `IMP-HOM-019` at length - its concrete requirements (tileset, terrain, collision, required visual elements, required events, shop processing, required transfers, story states) are cited by reference and pulled into `Implementation Guidance` and `Acceptance Criteria` below only where needed to show how they interact with pattern-derived guidance.

## 5. Environment Pattern

**Interior** - virtual layer. No `studio/design-patterns/interiors/interior.pattern.md` document exists yet (`studio/design-patterns/PATTERN_INHERITANCE_MODEL.md`, "Materialized vs. Virtual Nodes"). Its evidence lives in `reports/design-patterns/interior-pattern-corpus-review.md`'s "Recurring Layout Rules," "Recurring Composition Rules," "Recurring Passability Rules," and "Recurring Event Conventions" sections, corroborated across all eight interiors AtlasStudio has analyzed to date (Item Shop, House 1, House 2, Inn, Weapon & Armor Shop, Bar, Chief's House 1F/2F).

**Confidence: High.** Eight independent corroborating official sample interiors clears `studio/design-patterns/PATTERN_CONFIDENCE_MODEL.md`'s two-or-more-source bar for High by a wide margin, for the specific cross-cutting claims the corpus review states (shell-plus-void construction, the doorway threshold stack, region-free passability, no-NPC-by-default). This matches the treatment already given to this exact citation in `reports/design-patterns/inheritance-examples.md`, Examples 1 and 3 (`WO-0026`).

## 6. Specialization Pattern

**Shop** - `studio/design-patterns/interiors/shop.pattern.md` v1.0.

Per `PATTERN_INHERITANCE_MODEL.md`, "The Shop / Item Shop Double Duty": this pattern currently occupies both the Category-tier `Shop` node and the (unmaterialized) Specialization-tier `Item Shop` node, since its entire evidence base is the Item Shop sample and it has no local rules beyond what `Shop` itself states. This contract cites it as `Shop`, matching this work order's own Success Criteria wording, and does not fabricate a separate `Item Shop` document.

**Confidence: Medium**, exactly as `shop.pattern.md`'s own frontmatter currently states (`confidence: medium`, one corroborating official sample map). `WO-0025`'s corpus review recommended - but explicitly did not apply - promoting this to High on the strength of a second corroborating sample (`Map022`, Weapon & Armor Shop). **This document does not apply that promotion either.** It is cited here at its actual, current, unpromoted value, per this work order's explicit constraint.

## 7. Project Pattern

**No Project Pattern currently exists for Ashford Village.** No file exists under `studio/design-patterns/projects/` for this or any other project - the Project-specific tier described in `PATTERN_INHERITANCE_MODEL.md` is entirely unpopulated as of this document. This section is stated explicitly, per `PATTERN_CONTRACT_SPEC.md` Section 7, rather than left blank or silently skipped. If a future `studio/design-patterns/projects/the-last-sword-protocol/ashford-village.pattern.md` is ever authored, it would slot in here, and this section would then state its `parent_pattern` (`PAT-INTERIOR-SHOP`) and its own confidence.

## 8. Pattern Resolution

Applying `PATTERN_CONTRACT_SPEC.md`'s assembly order to this contract's cited layers:

```text
Creative Authority (SCR-HOM-ASH-003, ATLAS-STY-010, registries)
    |
    v
Environment Pattern: Interior (virtual, High)
    |
    v
Specialization Pattern: Shop (shop.pattern.md v1.0, Medium)
    |
    v
Project Pattern: none authored - layer skipped
    |
    v
Implementation Packet: IMP-HOM-019
    |
    v
Final Implementation Guidance
```

- **Creative Authority** is checked as a boundary condition, not layered: nothing below may contradict `SCR-HOM-ASH-003` or `ATLAS-STY-010`. No conflict was found between them and any cited pattern.
- **Environment Pattern (Interior)** contributes: compact shell inside a void border, centered-or-justified threshold with a stairs-tile-plus-transfer-event construction, region-free passability with zero encounters, and no assumed shopkeeper NPC by default.
- **Specialization Pattern (Shop)** adds, on top of the above: bilateral organization around the primary axis, wall-anchored storage furniture, a direct centerline from entrance to focal point, dense-perimeter/light-center composition rhythm, a floor accent marking the browse zone, and the reachability-ring requirement for intended interactables.
- **Project Pattern** contributes nothing - the layer is skipped, not silently assumed empty by omission.
- **Implementation Packet (IMP-HOM-019)** is layered last and wins wherever it states something more specific than the pattern chain: the counter as the room's literal centerpiece with the shopkeeper positioned at it (more specific than `Shop`'s generic "focal point"), the metal cabinet as a specific named landmark (a piece of required content the pattern chain has no way to know about), the ~15x11 recommended / 17x13-scaffold-acceptable size ceiling (more specific than `Shop`'s generic "keep it compact"), and the requirement that the counter block on every side except the shopkeeper's interaction side (more specific than `Shop`'s generic reachability-ring rule, which this instance satisfies exactly).
- No undeclared contradiction was found between any two cited layers. No cross-branch clarification applies (`Bar`'s wall-anchoring clarification, per `reports/design-patterns/inheritance-examples.md` Example 4, is not relevant here - this is a `Shop` citation, not `Bar`).

## 9. Implementation Guidance

**Authoritative requirements** (from Creative Authority / `IMP-HOM-019` - non-negotiable):

- Counter is the room's centerpiece; shopkeeper (`EVT-HOM-008`) interacts across it.
- Metal storage cabinet (`INT-ASH-SHOP-CABINET`) present on the back wall, up-right of the shopkeeper, treated as ordinary furniture.
- Shelves/barrels/crates forming a stock cluster along the left wall, per the SVG guide's adjacency.
- Door/exit transfer (`TRN-HOM-004`) at the bottom of the room, on the shopkeeper's axis, clear sightline from door to shopkeeper.
- Shop Processing wired with the first-pass inventory (one minor healing item at minimum; antidote/utility item conditional on open questions), or an explicit placeholder if inventory is undecided - never silently absent.
- Counter blocks on every side except the shopkeeper's interaction side; shelves and cabinet block; exit tile clear; Region 0 only, zero encounters.
- Map size ~15x11 recommended, 17x13 scaffold acceptable, do not enlarge beyond it.
- Shopkeeper dialogue reflects `Intro` vs. `After Node Seven` per `J1_Node07_Offline` / `NPC_Ashford_PostNode07`, text from `ATLAS-STY-010`.

**Pattern-derived guidance** (from `Interior` and `Shop` - binding by default, lower precedence than the above where they overlap, revisable through `PATTERN_REVIEW_PROCESS.md` rather than through this contract):

- Compact architectural shell inside a void/darkness border (`Interior`).
- Visible threshold tile (stairs-family) one row above the floor tile carrying the exit transfer event, shadow value marking the recess (`Interior`).
- Player spawn one tile inside the doorway on entry (`Shop`).
- Bilateral organization around the entrance-to-focal-point centerline; left/right merchandise mass counterbalanced without exact mirroring (`Shop`).
- Shelves/storage anchored to a wall, never floating in open floor, terminating cleanly into the wall (`Shop`) - the required left-wall stock cluster (an Authoritative requirement above) should be built following this construction convention.
- A floor accent (rug or similar) marking the primary browse zone (`Shop`) - not required by `IMP-HOM-019`, but a reasonable way to satisfy its general "clear sightline" and "landmarks present" acceptance criteria with more visual polish than a bare floor would.
- Dense-perimeter, light-center decoration rhythm; at least one small decorative animated detail such as a flame (`Interior`/`Shop`).
- Reachability ring for every intended interactable display object - the shelf/crate stock cluster's individual pieces should each have an adjacent walkable tile if any are meant to be examinable, per `Shop`'s Passability Rules.

**Implementation recommendations** (softer - not stated as a rule by any cited authority or pattern; deviate freely with a stated reason):

- Use the floor-accent convention specifically in front of the counter, since that is where the packet already places the room's main activity (the shopkeeper interaction), giving the rug a functional as well as decorative role.
- Consider a single wall-mounted decorative flame near the cabinet (an `Inn`-style convention, `studio/design-patterns/interiors/inn.pattern.md`, not itself cited as a governing layer for this contract) rather than a floor-adjacent one, since the cabinet is explicitly meant to read as "an old-world oddity in plain sight, not highlighted" (`IMP-HOM-019`) - a subtler light source may suit that framing better than the `Shop` pattern's default floor-adjacent placement. This is offered as a recommendation precisely because neither `Shop` nor `IMP-HOM-019` states a flame-placement rule strong enough to make it more than a suggestion.

## 10. Passability Rules

Combining `IMP-HOM-019`'s explicit collision statement with `shop.pattern.md`'s Passability Rules, per `bridges/rpg-maker-mz/passability-rule.md`:

- Tileset family `Inside`; Region 0 only; zero encounters (`IMP-HOM-019`, authoritative).
- Counter blocks on every side except the shopkeeper's interaction side (`IMP-HOM-019`, authoritative - more specific than `Shop`'s generic "structural furniture blocks by default" rule, and controlling where the two would otherwise leave the interaction side's collision ambiguous).
- Shelves and cabinet block; exit tile clear (`IMP-HOM-019`, authoritative).
- The full walkable set forms a single connected area reachable from the entrance, with the door-to-counter path clear (`IMP-HOM-019` requirement 6, reinforced by `Shop`'s general connectivity rule).
- Every intended interactable display object (shelf/crate pieces meant to be examinable, if any) satisfies the reachability ring - at least one adjacent walkable tile (`Shop`, filling a gap `IMP-HOM-019` does not itself specify at that level of detail).
- Reciprocal transfer check: `TRN-HOM-003` (entrance) and `TRN-HOM-004` (exit) round-trip correctly (`IMP-HOM-019`, authoritative).

## 11. Validation Requirements

```bash
# Automated (necessary, not sufficient - see below)
# Confirm event/transfer placement, collision flags, and region assignment
# against IMP-HOM-019's stated requirements, per bridges/rpg-maker-mz/passability-rule.md.
```

- Route validation at minimum: `entrance -> counter`, `counter -> shelf/crate cluster`, `counter -> exit`, per `bridges/rpg-maker-mz/passability-rule.md`, "Route Validation."
- Automated JSON inspection confirms structural placement, not tile-level walkability feel - **a human playtest pass is still required** before acceptance, per that document's "Human Playtest Still Required" (this demonstration does not perform one; a real execution must).
- Re-check, at execution time, that `shop.pattern.md`'s frontmatter still reads `confidence: medium` and that no `studio/design-patterns/projects/` pattern for Ashford Village has since been authored - both could have changed between this document being written and any future execution, per `PATTERN_APPLICATION_CHECKLIST.md`, "Pattern confidence recorded."

## 12. Acceptance Criteria

Reproduced from `IMP-HOM-019` (authoritative; identical to `ashford-shop-build-contract.md`'s own Section 8, shown here to demonstrate that a pattern-aware contract does not weaken or replace packet-derived acceptance criteria):

1. Entry works - `TRN-HOM-003` places the player inside the shop near the door.
2. Shopkeeper is interactable across the counter - `EVT-HOM-008` fires from the customer side; the counter blocks movement but not interaction.
3. Shop menu opens - Shop Processing runs with the first-pass inventory, or an explicit placeholder message states the shop is not yet stocked.
4. Inventory is early-game safe.
5. Landmarks present - counter, shelf/crate cluster, and the metal cabinet are visually distinct and match the guide's adjacency.
6. Collision correct - counter/shelves/cabinet block; door-to-counter path is clear.
7. Exit works - `TRN-HOM-004` returns the player to Ashford Exterior, round-tripping with `TRN-HOM-003`.
8. No random encounters.
9. Story states - shopkeeper dialogue reflects Intro vs. After Node Seven.

**Pattern-derived acceptance addition** (not in `IMP-HOM-019`, added by the `Shop` pattern layer, non-blocking relative to the above): the shelf/crate stock cluster is anchored to the wall rather than floating in open floor, and at least one intended-interactable stock piece (if any exist) satisfies the reachability ring.

## 13. References

**Atlas:**
- `atlas/docs/02_World/Screens/Home_Island/SCR_HOM_ASH_003_Ashford_Shop.md`
- `atlas/docs/03_Story/Dialogue/Home_Island/Ashford_Dialogue_Packet.md` (`ATLAS-STY-010`)
- `atlas/docs/09_Technical/Implementation_Packets/Home_Island/IMP_HOM_019_Manual_Map_Build_Ashford_Shop.md`
- `atlas/docs/09_Technical/Registries/Home_Island_Event_Registry.md`, `Home_Island_Transfer_Registry.md`
- `atlas/docs/09_Technical/Home_Island_Tileset_Assignment_Matrix.md`

**Patterns:**
- `studio/design-patterns/interiors/shop.pattern.md` v1.0
- `reports/design-patterns/interior-pattern-corpus-review.md` (Environment/`Interior` evidence)
- `studio/design-patterns/PATTERN_INHERITANCE_MODEL.md`, `PATTERN_RESOLUTION_RULES.md`, `PATTERN_APPLICATION_GUIDE.md`, `PATTERN_CONFIDENCE_MODEL.md`

**Format and bridge documents:**
- `studio/contracts/PATTERN_CONTRACT_SPEC.md`, `PATTERN_APPLICATION_CHECKLIST.md`
- `bridges/rpg-maker-mz/passability-rule.md`, `ownership-model.md`

**Prior contracts (not replaced by this document):**
- `reports/implementation-contracts/ashford-shop-build-contract.md` - the real, authoritative contract for this build.
- `reports/implementation-contracts/ashford-village-contract.md` - parent contract governing all Ashford Village work.

**Work orders:**
- `work-orders/WO-0020-ashford-village-implementation-contract-from-atlas-handoff.md`
- `work-orders/WO-0024-design-pattern-library.md`, `WO-0025-interior-pattern-corpus.md`, `WO-0026-design-pattern-inheritance-model.md`
- Created by `work-orders/WO-0027-pattern-aware-implementation-contracts.md`
