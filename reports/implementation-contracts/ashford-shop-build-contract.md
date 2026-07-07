# Ashford Shop Build Contract

**Child contract of:** `reports/implementation-contracts/ashford-village-contract.md`
**Scope:** `SCR-HOM-ASH-003` Ashford Shop Interior, RPG Maker `Map003` (`INT_Ashford_Shop`)
**Type:** Build contract (not verification) - Map003's ledger state is `generated`, not `hand_authored`.

---

## 1. Authoritative Atlas Source Files

| File | Role |
|---|---|
| `atlas/docs/09_Technical/Implementation_Packets/Home_Island/IMP_HOM_019_Manual_Map_Build_Ashford_Shop.md` | **Primary build packet. This contract executes IMP-HOM-019, verbatim in requirements, and does not add to it.** |
| `atlas/docs/02_World/Screens/Home_Island/SCR_HOM_ASH_003_Ashford_Shop.md` | Screen object defining purpose, required elements, and acceptance criteria. |
| `reports/atlas-import/map-guides/SCR-HOM-ASH-003-layout-guide.svg` (`rpgmakerLSP` repo) | Production-source layout guide (633x314, relationship diagram, not tile-accurate). |
| `atlas/docs/09_Technical/Home_Island_Tileset_Assignment_Matrix.md` | Assigns the `Inside` tileset family and counter/shelf collision rules. |
| `atlas/docs/09_Technical/Registries/Home_Island_Event_Registry.md` | Canonical event ID `EVT-HOM-008` (Shopkeeper). |
| `atlas/docs/09_Technical/Registries/Home_Island_Transfer_Registry.md` | Canonical transfers `TRN-HOM-003` (entrance, lives on Map001) and `TRN-HOM-004` (exit, lives on this screen). |
| `atlas/docs/03_Story/Dialogue/Home_Island/Ashford_Dialogue_Packet.md` (`ATLAS-STY-010`) | Source for shopkeeper dialogue text. **This contract owns applying the Shopkeeper's dialogue** - the dialogue-application contract explicitly excludes the Shopkeeper to avoid duplicate ownership. |
| `atlas/docs/09_Technical/Implementation_Packets/Home_Island/IMP_HOM_017_Manual_Map_Build_Ashford_Exterior.md`, `IMP_HOM_018_Manual_Map_Build_Elara_House.md` | Prior packets in this series; same structure and conventions apply. |

## 2. Exact Game Repo Targets

| Target | Action |
|---|---|
| `TheLastSwordProtocol-Game/data/Map003.json` | Build target. Existing auto-generated content (17x13, `tilesetId: 3`) is a rough scaffold only, not the deliverable. |
| `TheLastSwordProtocol-Game/map_ownership.json` | Flip the `"3"` entry's `state` from `"generated"` to `"hand_authored"` **before** opening Map003 in the editor (per `AGENTS.md` rule: flip the moment manual work begins, not after). May be flipped to `"locked"` after acceptance criteria (Section 7) are met. |

No other Game repo file is in scope for this contract.

## 3. Ownership Restrictions

Map003 is the **only** Ashford map whose ledger state (`generated`) currently permits a build contract. This is explicitly different from Map001/Map002 (see `ashford-existing-map-verification-contract.md`), which are `hand_authored` and must never be treated as build targets. Once this contract's build is accepted and the ledger is flipped to `hand_authored` or `locked`, any future work on Map003 requires a new, narrowly-scoped work order - not a silent re-run of this one.

## 4. What May Be Modified

- `TheLastSwordProtocol-Game/data/Map003.json`: tiles, terrain, collision, regions, and events, per Section 5 below.
- `TheLastSwordProtocol-Game/map_ownership.json`: the `"3"` entry's `state` field only.

## 5. What Must Not Be Modified

- `TheLastSwordProtocol-Game/data/Map001.json` or `data/Map002.json`.
- Any Atlas canon file, including `SCR-HOM-ASH-003` itself and `ATLAS-STY-010`.
- The two open questions on `SCR-HOM-ASH-003` (antidote stocking if Marsh Gel poison is enabled; whether inventory changes after Node Seven) - both remain design decisions outside this contract's scope. Build with **one inventory list** until Atlas resolves them.
- Combat database rows - use only IDs that already exist in the clean skeleton (Atlas combat database spec). Do not invent new items.

## 6. Passability and Route Validation Requirements

Per `bridges/rpg-maker-mz/passability-rule.md` and `IMP-HOM-019`:

- Tileset family: `Inside`. Terrain: shop floor/walls, counter, shelves, crates/barrels, metal cabinet placeholder.
- Collision: the counter blocks on every side **except** the shopkeeper interaction side; shelves and the cabinet block; the exit tile is clear.
- Regions: Region 0 only. Encounters: none - zero random encounters.
- Reachability: clear sightline from the door to the shopkeeper; the path from door to counter is clear; the player cannot walk behind the counter except where the design intends.
- Reciprocal transfer check: `TRN-HOM-003` (entrance, on Map001, built under `IMP-HOM-017`) and `TRN-HOM-004` (exit, this map) must round-trip correctly.
- Automated JSON inspection confirms event/transfer placement, not actual tile-level walkability - a human playtest pass is still required before this map is accepted.

## 7. Sample-Map Quality Expectations

- The SVG guide is a relationship diagram (shopkeeper at the counter mid-room, cabinet against the back wall to the right, door at the bottom on the shopkeeper's axis) - do not convert its pixel coordinates into tile coordinates.
- Map size: SCR-HOM-ASH-003 recommends ~15x11 tiles; the existing scaffold is 17x13. Either is acceptable. **Do not enlarge beyond the scaffold size.**
- Landmark adjacency must match the guide: cabinet on the back wall, up-right of the shopkeeper; counter as the room's centerpiece; shelves/barrels/crates forming a stock cluster along the left wall.
- Shop Processing inventory, first pass: one minor healing item, an antidote or equivalent only if early poison is enabled, one basic utility item if available, no expensive gear. If the final inventory is undecided, wire the minor healing item alone rather than leaving the shopkeeper dialogue-only.

## 8. Acceptance Criteria

Reproduced from `IMP-HOM-019`. A hand-built Ashford Shop Interior map passes when all of the following are true:

1. Entry works - `TRN-HOM-003` places the player inside the shop near the door.
2. Shopkeeper is interactable across the counter - `EVT-HOM-008` fires from the customer side; the counter blocks movement but not interaction.
3. Shop menu opens - Shop Processing runs with the first-pass inventory, or an explicit placeholder message states the shop is not yet stocked. A silent or broken shop command is a fail.
4. Inventory is early-game safe - nothing sold breaks early-game balance.
5. Landmarks present - counter, shelf/crate cluster, and the metal cabinet are visually distinct and match the SVG guide's adjacency.
6. Collision correct - counter/shelves/cabinet block; door-to-counter path is clear.
7. Exit works - `TRN-HOM-004` returns the player to Ashford Exterior at the shop-door landmark, round-tripping with `TRN-HOM-003`.
8. No random encounters - zero encounters from Region assignment.
9. Story states - shopkeeper dialogue reflects Intro vs. After Node Seven per `J1_Node07_Offline` and `NPC_Ashford_PostNode07`.

## 9. Recommended Implementing Agent

**Codex** (implementation engineer), per `studio/agent-roles.md` ("RPG Maker implementation... JSON transformations... Applying work orders to a codebase"). This matches the precedent set by `WO-0035`/`WO-0036`, the build reports for Map001/Map002, which followed the same `IMP-HOM-01x` packet pattern. Shopkeeper dialogue text should be copied from `ATLAS-STY-010` as-is, not rewritten - if Codex is uncertain how to translate a scaffold line into an event command, escalate rather than paraphrase creatively.

## 10. Non-Goals

- Does not produce final art assets - build against existing/placeholder tiles only.
- Does not resolve the antidote-stocking or post-Node-Seven-inventory open questions.
- Does not author new shopkeeper dialogue - `ATLAS-STY-010` is the source, used verbatim.
- Does not reintroduce automatic final map construction as a production path - the existing auto-generated Map003.json may be used as a rough starting scaffold only.
- Does not change story canon, dialogue text outside the Shopkeeper, quests, or NPC roster.
