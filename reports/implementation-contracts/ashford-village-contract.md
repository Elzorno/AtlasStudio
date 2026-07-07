# Ashford Village Implementation Contract

**Parent contract for:** Ashford Village / Home Island opening area (`SCR-HOM-ASH-001/002/003`, `QST-HOM-001`)
**Issued by:** AtlasStudio (`WO-0020`), consuming `TheLastSwordProtocol-Atlas`'s `reports/ashford-village-implementation-packet-readiness.md`
**Status:** Active - governs the three child contracts below

---

## 1. Source Authority

`TheLastSwordProtocol-Atlas` is the sole creative authority for Ashford Village. This contract and its three children do not redesign Ashford Village, do not regenerate Map001 or Map002, and do not create new canon. Every requirement below is derived from an existing, already-approved Atlas source - none is invented here.

Per Atlas's own readiness verdict (`reports/ashford-village-implementation-packet-readiness.md`, Section 7): **Ashford Village may safely receive implementation contracts now for exactly three tasks** - a verification/handoff contract for the two already-built maps, a build contract for the Ashford Shop, and a content-application contract for the remaining placeholder dialogue. No other work is authorized by this contract.

## 2. Authoritative Atlas Source Files

| File | Role |
|---|---|
| `atlas/docs/00_Foundation/Project_Constitution.md` (`ATLAS-PRJ-001`) | Tone/theme law governing all content in this contract. |
| `atlas/docs/05_Characters/Character_Bible.md` (`ATLAS-CHR-001`) | Kai and Grandmother Elara character authority. |
| `atlas/docs/02_World/Screens/Home_Island/SCR_HOM_ASH_001_Ashford_Exterior.md` | Ashford Exterior screen spec. |
| `atlas/docs/02_World/Screens/Home_Island/SCR_HOM_ASH_002_Elara_House.md` | Elara House Interior screen spec. |
| `atlas/docs/02_World/Screens/Home_Island/SCR_HOM_ASH_003_Ashford_Shop.md` | Ashford Shop Interior screen spec. |
| `atlas/docs/03_Story/Quests/Home_Island/QST_HOM_001_Home_Island_Opening.md` | Opening quest authority. |
| `atlas/docs/03_Story/Dialogue/Home_Island/Ashford_Dialogue_Packet.md` (`ATLAS-STY-010`) | Dialogue scaffold/direction for all Ashford NPCs. |
| `atlas/docs/09_Technical/Implementation_Packets/Home_Island/IMP_HOM_017_Manual_Map_Build_Ashford_Exterior.md` | Map001 build/verification packet. |
| `atlas/docs/09_Technical/Implementation_Packets/Home_Island/IMP_HOM_018_Manual_Map_Build_Elara_House.md` | Map002 build/verification packet. |
| `atlas/docs/09_Technical/Implementation_Packets/Home_Island/IMP_HOM_019_Manual_Map_Build_Ashford_Shop.md` | Map003 build packet. |
| `atlas/docs/09_Technical/Registries/Home_Island_Screen_Registry.md`, `Home_Island_Transfer_Registry.md`, `Home_Island_Event_Registry.md` | Canonical ID inventories. |
| `atlas/docs/09_Technical/Playtest/Home_Island_Production_Readiness_Gate.md` (`ATLAS-TEC-061`) | Formal GO decision for Home Island implementation. |
| `atlas/docs/00_Foundation/Canonical_ID_Registry.md` | Confirms `LOC-ASH-001`, `CHR-KAI-001`, `NPC-ELA-001`, `SCR-HOM-ASH-001/002/003` as non-conflicting, Assigned/Reserved IDs. |
| `reports/ashford-village-implementation-packet-readiness.md` | The readiness review this contract is built from. Treat its verdict as binding. |

**Execution-side references (read-only, not canon):**

| File | Role |
|---|---|
| `../TheLastSwordProtocol-Game/map_ownership.json` | Per-map build-state ledger; governs what may be written. |
| `../rpgmakerLSP/reports/atlas-import/wo-0035-gate-a-map002-build-report.md` | Elara House build report (route audit `found=258, missing=0, warning=0`). |
| `../rpgmakerLSP/reports/atlas-import/wo-0036-gate-a-map001-build-report.md` | Ashford Exterior build report (route audit `found=258, missing=0, warning=0`). |

## 3. Stale Data - Do Not Use

`atlas-exports/home-island.json` was generated 2026-07-04 (commit `bc3598b`) and still lists all three Ashford screens as `status: Draft`, `implementation_packet: IMP-HOM-010`. It predates `IMP-HOM-017/018/019` and the real Map001/Map002 builds by two days.

**Rule: stale export data must not override current hand-built Game repo state.** Nothing in this contract or its children may be derived from `atlas-exports/home-island.json`. Where current state is needed, it comes from `map_ownership.json`, the `IMP-HOM-01x` packets, or direct (read-only) inspection of `TheLastSwordProtocol-Game/data/Map00{1,2,3}.json`.

## 4. Game Repo Targets (Village-Wide)

| Target | Current ledger state | Role in this contract set |
|---|---|---|
| `TheLastSwordProtocol-Game/data/Map001.json` (`TWN_Ashford_Exterior`) | `hand_authored` | Verification only - see child contract 4. Also the dialogue-application target for non-Elara NPCs - see child contract 3. |
| `TheLastSwordProtocol-Game/data/Map002.json` (`INT_Ashford_ElaraHouse`) | `hand_authored` | Verification only - see child contract 4. Already carries final Elara dialogue; no dialogue work needed. |
| `TheLastSwordProtocol-Game/data/Map003.json` (`INT_Ashford_Shop`) | `generated` | Build target - see child contract 2. Shopkeeper dialogue is applied as part of this build, not the dialogue-application contract. |
| `TheLastSwordProtocol-Game/map_ownership.json` | n/a | Ledger; may only be edited to flip Map003 from `generated` to `hand_authored`/`locked` per its own rules. Map001/Map002 entries must not change state without a human Production Director playtest certification. |

## 5. Ownership Restrictions (Village-Wide)

Governed by `../TheLastSwordProtocol-Game/AGENTS.md` and `map_ownership.json`:

1. A map may be written by any agent or pipeline **only if its ledger state is `generated`.** Today, that is Map003 alone.
2. `hand_authored` and `locked` maps (Map001, Map002) must never be written by an implementing agent under this contract set.
3. **Fail safe:** if the ledger is missing, unreadable, or a map ID is not listed, treat that map as not writable.
4. Flip a map's ledger state to `hand_authored` the moment manual editor work begins on it - not after.
5. State changes are one-way in normal production (`generated` -> `hand_authored` -> `locked`). Reverting requires a recorded Production Director decision.

## 6. Child Contracts

| Contract | Scope | Type |
|---|---|---|
| `reports/implementation-contracts/ashford-shop-build-contract.md` | Map003 (Ashford Shop Interior), from `IMP-HOM-019` | Build |
| `reports/implementation-contracts/ashford-dialogue-application-contract.md` | Non-Elara Ashford NPC dialogue on Map001, from `ATLAS-STY-010` | Content application |
| `reports/implementation-contracts/ashford-existing-map-verification-contract.md` | Map001 and Map002, against `IMP-HOM-017`/`IMP-HOM-018` | Verification / handoff |

These three contracts are independent and may be executed in any order or in parallel, except that the Ashford Shop build contract owns the Shopkeeper's dialogue (per `IMP-HOM-019`'s own traceability table) and must not be duplicated by the dialogue-application contract.

## 7. What May Be Modified

- `TheLastSwordProtocol-Game/data/Map003.json` (build - see child contract 2).
- `TheLastSwordProtocol-Game/data/Map001.json` event Show Text commands only, for the specific NPCs named in child contract 3.
- `TheLastSwordProtocol-Game/map_ownership.json`, limited to the Map003 entry's state field.

## 8. What Must Not Be Modified

- `TheLastSwordProtocol-Game/data/Map001.json` or `data/Map002.json` map geometry, tiles, collision, transfers, or event structure.
- Any file in `TheLastSwordProtocol-Atlas`.
- `ATLAS-STY-010`, any `SCR-HOM-ASH-*` screen object, `QST-HOM-001`, or any other Atlas canon file.
- The two open, explicitly Creative-Director-only questions: whether the Village Elder becomes a named `Character` object, and whether Elara gives Kai a starting item. No implementing agent may resolve these unilaterally.
- The `map_ownership.json` entries for Map001/Map002 (must remain `hand_authored`, not flipped to `locked`, until human playtest certification per Section 10).

## 9. Passability and Route Validation Requirements

Governed by `bridges/rpg-maker-mz/passability-rule.md`. Applies to all three child contracts:

- Use tileset passability flags as engine data; never override without explicit authorization in the relevant child contract.
- Player start, required NPCs, required events, and required transfers must all be reachable.
- Walls, roofs, cliffs, and water must not be walkable unless intended.
- Every transfer must be validated as reciprocal (a matching return transfer exists on the destination map).
- Ashford-local transfers in scope: `TRN-HOM-001` through `TRN-HOM-004` (Elara House <-> Exterior, Shop <-> Exterior), plus Ashford Exterior's route exits `TRN-HOM-005` (Skyreach, gated on `J1_Skyreach_AccessOpen`), `TRN-HOM-007` (Rustshore), `TRN-HOM-015` (Glassfield), `TRN-HOM-027` (Fogfen, optional).
- Automated JSON inspection is necessary but not sufficient - a human playtest pass is required to confirm actual tile-level passability and route feel, per the Passability Rule's "Human Playtest Still Required" section.

## 10. Sample-Map Quality Expectations

- SVG layout guides (`reports/atlas-import/map-guides/SCR-HOM-ASH-*-layout-guide.svg` in the `rpgmakerLSP` repo) are **relationship diagrams, not tile-accurate grids.** Use relative position and adjacency, never pixel-to-tile conversion.
- Map sizes are recommendations, not hard requirements, but existing scaffold sizes should not be enlarged without cause (Map001 ~40x32, Map002 ~17x13, Map003 ~15x11 recommended / 17x13 scaffold acceptable).
- Region 0 only, zero random encounters, across all three Ashford screens.
- Tone must match each screen's Purpose section: Ashford Exterior warm/ordinary-with-old-world-remnants; Elara House safe/personal/family; Ashford Shop practical/economy-introducing.
- A human (Production Director) playtest/certification pass on Map001/Map002 is outstanding and is not a hard blocker to the Shop build or dialogue contracts (both are independent), but must occur before either map is flipped to `locked`.

## 11. Village-Wide Acceptance Criteria

- All three child contracts' individual acceptance criteria are met (see each contract).
- No child contract's execution caused a write to a `hand_authored` map.
- No new Ashford canon, NPC, or story beat was introduced.
- `atlas-exports/home-island.json` was not used as a data source for any change.
- The two open Creative-Director-only questions remain unresolved by implementation.
- A human playtest/certification pass on Map001/Map002 is scheduled or explicitly flagged as still outstanding in any submission record.

## 12. Recommended Implementing Agent (Village-Wide)

Mixed, per `studio/agent-roles.md` - see each child contract for its specific recommendation. In general: Codex (implementation engineer) for RPG Maker map/event/JSON work; Claude Code or a human writer for final dialogue text, per `ATLAS-STY-010`'s own Implementation Notes ("Codex should place placeholder versions of these NPCs... Claude or a human writer can later expand final dialogue while preserving these roles"). No agent recommendation in this contract set authorizes automatic/generated final map construction - `BUILD-0043` recorded a formal NO GO for that workflow across all of Home Island.

## 13. Non-Goals

- This contract does not redesign Ashford Village.
- This contract does not regenerate Map001 or Map002.
- This contract does not create new canon, characters, or locations.
- This contract does not resolve the Village Elder naming question or the Elara starting-item question.
- This contract does not certify Map001/Map002 as `locked` - that requires a human playtest pass outside this contract's scope.
