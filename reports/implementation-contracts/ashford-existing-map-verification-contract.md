# Ashford Existing Map Verification Contract

**Child contract of:** `reports/implementation-contracts/ashford-village-contract.md`
**Scope:** `SCR-HOM-ASH-001` Ashford Exterior (`Map001`) and `SCR-HOM-ASH-002` Elara House Interior (`Map002`)
**Type:** Verification / handoff contract - **not** a build contract. Both maps are already hand-built to production quality.

---

## 1. Why This Is Verification, Not Build

Per `reports/ashford-village-implementation-packet-readiness.md` Section 5 and 7: Map001 and Map002 are already built, hand-authored, and production-quality in `TheLastSwordProtocol-Game` - landmarks, collision, transfers, and route cues are implemented and audited, and Map002 already carries Elara's final (non-placeholder) dialogue. **Regenerating either map would destroy hand-authored work and violate the map ownership ledger.** This contract's only authorized action is to confirm the existing build against its packet and screen spec, and to surface any discrepancy as a finding - never to silently patch or regenerate.

## 2. Authoritative Atlas Source Files

| File | Role |
|---|---|
| `atlas/docs/09_Technical/Implementation_Packets/Home_Island/IMP_HOM_017_Manual_Map_Build_Ashford_Exterior.md` | Map001 build packet and acceptance criteria - the verification baseline for Map001. |
| `atlas/docs/09_Technical/Implementation_Packets/Home_Island/IMP_HOM_018_Manual_Map_Build_Elara_House.md` | Map002 build packet and acceptance criteria - the verification baseline for Map002. |
| `atlas/docs/02_World/Screens/Home_Island/SCR_HOM_ASH_001_Ashford_Exterior.md`, `SCR_HOM_ASH_002_Elara_House.md` | Screen objects defining purpose and acceptance criteria (superset of the packets' criteria). |
| `atlas/docs/09_Technical/Registries/Home_Island_Transfer_Registry.md`, `Home_Island_Event_Registry.md` | Canonical transfer/event IDs to verify against. |
| `atlas/docs/03_Story/Dialogue/Home_Island/Ashford_Dialogue_Packet.md` (`ATLAS-STY-010`) | Verification baseline for Elara's already-applied final dialogue on Map002. |

**Execution-side references (read-only, not canon, required for verification accuracy):**

| File | Role |
|---|---|
| `../TheLastSwordProtocol-Game/map_ownership.json` | Confirms both maps' current ledger state (`hand_authored`). |
| `../rpgmakerLSP/reports/atlas-import/wo-0036-gate-a-map001-build-report.md` | Prior implementation report for Map001; route audit `found=258, missing=0, warning=0`. |
| `../rpgmakerLSP/reports/atlas-import/wo-0035-gate-a-map002-build-report.md` | Prior implementation report for Map002; route audit `found=258, missing=0, warning=0`. |
| `reports/rpg-maker-bridge/ashford-village-route-validation.md`, Part A only | AtlasStudio's own prior route-reachability checklist for Map001, confirmed against direct `Map001.json`/`Map002.json` inspection. **Part B of that document is superseded per `WO-0018` and must not be used** - it describes a different, unbuilt canon (Rowan, four-building roster) that does not match what is actually implemented. |

## 3. Exact Game Repo Targets

| Target | Action |
|---|---|
| `TheLastSwordProtocol-Game/data/Map001.json` | Read-only inspection / in-editor playtest for verification. No edit authorized by this contract. |
| `TheLastSwordProtocol-Game/data/Map002.json` | Read-only inspection / in-editor playtest for verification. No edit authorized by this contract. |
| `TheLastSwordProtocol-Game/map_ownership.json` | Read-only. Do not flip either map's state to `locked` under this contract - that requires a recorded human Production Director playtest certification, which is outside this contract's scope. |

## 4. Ownership Restrictions

Both maps are `hand_authored` per `map_ownership.json`. Per `AGENTS.md`: **pipeline scripts and implementing agents must never write these files.** Any defect found during verification must be logged as a finding in the verification report and routed to a separate, narrowly-scoped fix work order - it must not be patched directly under this contract, and it must never be "fixed" by regenerating the map from `IMP-HOM-017`/`IMP-HOM-018` or from `atlas-exports/home-island.json`.

## 5. What May Be Modified

Nothing in `TheLastSwordProtocol-Game`. This contract's only deliverable is a verification report (see Section 9); no map, event, or ledger file is edited under this contract.

## 6. What Must Not Be Modified

- `TheLastSwordProtocol-Game/data/Map001.json` and `data/Map002.json` - no geometry, tiles, collision, events, or transfers.
- `TheLastSwordProtocol-Game/map_ownership.json` - ledger state for these two maps stays `hand_authored` under this contract.
- Any Atlas canon file.
- Elara's already-final dialogue on Map002 - verify it matches `ATLAS-STY-010`, do not rewrite it here even if a phrasing preference arises; a genuine defect goes to a separate fix work order.

## 7. Passability and Route Validation Requirements

Per `bridges/rpg-maker-mz/passability-rule.md`, re-confirm the following (JSON inspection where possible, human playtest where required):

**Map001 (Ashford Exterior):**
- `player_start` on entry from Map002 (`TRN-HOM-001`) is on a passable tile.
- `TRN-HOM-002` (Enter Elara House) is reachable and reciprocal.
- `TRN-HOM-003` (Enter Ashford Shop) is reachable (round-trips with `TRN-HOM-004` once the shop build contract completes).
- `TRN-HOM-005` (Skyreach), `TRN-HOM-007` (Rustshore), `TRN-HOM-015` (Glassfield), `TRN-HOM-027` (Fogfen, optional) are all reachable, with `TRN-HOM-005` correctly gated on `J1_Skyreach_AccessOpen`.
- All required NPC events (Child, Farmer, Skyreach Joker, Dock Messenger, Village Elder placeholder) sit on tiles reachable from `player_start`.
- No wall, roof, cliff, or water tile is walkable unless intended - **requires human playtest**, not verifiable from JSON inspection alone.

**Map002 (Elara House):**
- New-game `player_start` has free movement in all directions.
- Elara (`EVT-HOM-002`) is reachable and reflects the correct one of five story states.
- `TRN-HOM-001` (exit to Ashford Exterior) is reachable and reciprocal with `TRN-HOM-002`.
- Furniture/wall collision blocks correctly; the path from start to Elara and to the exit is clear - **requires human playtest** for final confirmation.

Both maps' prior build reports recorded a route audit of `found=258, missing=0, warning=0` - this contract's verification should reproduce or explicitly reference that audit result rather than re-deriving it from scratch, and should flag clearly if a re-run produces a different result.

## 8. Sample-Map Quality Expectations

Verify against each packet's own acceptance criteria (Sections 9 below), plus:

- SVG guide adjacency: Map001's warm-stone vent and old humming panel near their associated events; Map002's keepsake beside Elara, exit near the bottom, player start and Elara clustered near the top.
- Tone: Map001 reads as a warm, ordinary village with subtle old-world remnants; Map002 reads as small, cozy, and safe (family, safety, memory, quiet warnings).
- Region 0 only, zero random encounters, on both maps.
- Map sizes match or reasonably approximate the packets' recommendations (Map001 ~40x32, Map002 ~17x13) - already satisfied per the existing builds, verify no drift.

## 9. Acceptance Criteria

**Map001, reproduced from `IMP-HOM-017`:**

1. Readability - north exit, south/east exit, shop entrance, and Elara House entrance are identifiable without guesswork.
2. Landmarks present - warm-stone vent and old humming panel visually distinct and correctly placed.
3. Collision correct - houses, fences, and the vent block; all paths/exits walkable; no unintended dead ends.
4. All required events exist and fire correctly, including the hidden item's self-switch.
5. All required transfers exist and are correctly gated.
6. No random encounters.
7. Tone matches `SCR-HOM-ASH-001`'s Purpose section.

**Map002, reproduced from `IMP-HOM-018`:**

1. New game starts here with free movement.
2. Elara is interactable and reflects the correct story state.
3. Landmarks present - keepsake/shelf visually distinct, positioned beside Elara.
4. Collision correct - walls/furniture block; start-to-Elara and start-to-exit paths walkable.
5. Exit works - `TRN-HOM-001` correctly transfers to Ashford Exterior at the corresponding entrance anchor.
6. No random encounters.
7. Tone matches `SCR-HOM-ASH-002`'s Purpose section.

**Contract-level acceptance:**

- A verification report is produced stating pass/fail against every criterion above, citing direct inspection evidence (file/line or event reference) rather than assertion.
- Any discrepancy found is logged as a finding with a recommended follow-up work order, not silently fixed.
- The report explicitly states that human playtest certification for both maps remains outstanding (per `reports/ashford-village-implementation-packet-readiness.md` Section 6, item 5) and is a precondition for flipping either map to `locked`.

## 10. Recommended Implementing Agent

**Claude Code or Codex, in a read-only/audit capacity**, per `studio/agent-roles.md`'s "Tests and audits" and "long-form implementation reasoning" strengths - not a build-capable session. The **human playtest** portion of Section 7/9 cannot be delegated to any AI agent and must be performed by a human before either map is certified `locked`, per the Passability Rule's "Human Playtest Still Required" section and the readiness report's own outstanding-item list.

## 11. Non-Goals

- Does not regenerate Map001 or Map002 under any circumstance.
- Does not modify either map's geometry, events, transfers, or dialogue.
- Does not flip either map's ledger state to `locked` - that is a human Production Director decision outside this contract.
- Does not treat `atlas-exports/home-island.json` as a source for verification data.
- Does not use Part B of `reports/rpg-maker-bridge/ashford-village-route-validation.md` (superseded, describes an unbuilt/incorrect canon).
