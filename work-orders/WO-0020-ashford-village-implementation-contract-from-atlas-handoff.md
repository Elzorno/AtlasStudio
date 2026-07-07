---
work_order_id: WO-0020
title: Ashford Village Implementation Contract from Atlas Handoff
status: submitted
project: the-last-sword-protocol
recommended_agent: claude-code
agent_role: senior-software-architect
risk_level: low
player_facing: false
engine_specific: true
required_capabilities:
  - documentation
  - architecture-review
preferred_capabilities:
  - qa-review
produces:
  - contract.ashford_village
  - contract.ashford_shop_build
  - contract.ashford_dialogue_application
  - contract.ashford_existing_map_verification
created: 2026-07-07
---

# WO-0020 - Ashford Village Implementation Contract from Atlas Handoff

## Purpose

`TheLastSwordProtocol-Atlas` produced `reports/ashford-village-implementation-packet-readiness.md`, an authoritative readiness review concluding that Ashford Village may safely move to implementation contracts for three concrete, already-scoped tasks - and only those three. This work order consumes that report (plus `IMP-HOM-019` and a read-only look at the current `TheLastSwordProtocol-Game` state) and produces the implementation contracts themselves, so a future implementing agent can act against `TheLastSwordProtocol-Game` without redesigning Ashford Village, regenerating Map001/Map002, or inventing canon.

## Player-Facing Goal

Indirect. This work order produces documentation only. Its purpose is to make the player-facing work that follows (finishing the Ashford Shop, applying final dialogue) safe to execute without destroying the two already-hand-authored, production-quality maps or contradicting Atlas canon.

## Background

Per `work-orders/WO-0018-repository-authority.md` and `work-orders/WO-0019-atlas-import-bridge.md`, AtlasStudio is no longer the creative authority for The Last Sword Protocol and has an import/bridge posture toward `TheLastSwordProtocol-Atlas`. Atlas's own readiness report confirms Ashford Village is real, canonical, and two-thirds built: Map001 (Ashford Exterior) and Map002 (Elara House) are hand-authored, production-quality, and already carry final dialogue for Elara. Map003 (Ashford Shop) remains an unbuilt `generated` placeholder with a complete, ready-to-build packet (`IMP-HOM-019`). Non-Elara Ashford dialogue is still first-pass scaffold in the live event data. `atlas-exports/home-island.json` is confirmed stale (predates `IMP-HOM-017/018/019` and the actual Map001/Map002 builds by two days) and must not be treated as current.

## Scope

### In Scope

- Reading and citing `reports/ashford-village-implementation-packet-readiness.md` as the authoritative readiness verdict.
- Reading `atlas-exports/home-island.json` only to confirm and document its staleness, not as a data source for the contracts.
- Reading `IMP-HOM-019`, `IMP-HOM-017`, `IMP-HOM-018`, the three `SCR-HOM-ASH-*` screen objects, `Ashford_Dialogue_Packet.md` (`ATLAS-STY-010`), the Home Island Transfer/Event registries, and `map_ownership.json` / `AGENTS.md` in `TheLastSwordProtocol-Game` (read-only).
- Producing four implementation contracts under `reports/implementation-contracts/` that define authoritative sources, exact Game repo targets, ownership restrictions, modification boundaries, passability/route validation requirements, sample-map quality expectations, acceptance criteria, and a recommended implementing agent for each.

### Out of Scope

- Redesigning Ashford Village.
- Regenerating Map001 or Map002.
- Creating new canon, story beats, or NPCs.
- Modifying `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` in any way.
- Executing any of the contracts (building Map003, applying dialogue, or certifying Map001/Map002).

## Inputs

- `../TheLastSwordProtocol-Atlas/reports/ashford-village-implementation-packet-readiness.md`
- `../TheLastSwordProtocol-Atlas/atlas-exports/home-island.json` (consulted only to confirm staleness)
- `../TheLastSwordProtocol-Atlas/atlas/docs/09_Technical/Implementation_Packets/Home_Island/IMP_HOM_017_Manual_Map_Build_Ashford_Exterior.md`
- `../TheLastSwordProtocol-Atlas/atlas/docs/09_Technical/Implementation_Packets/Home_Island/IMP_HOM_018_Manual_Map_Build_Elara_House.md`
- `../TheLastSwordProtocol-Atlas/atlas/docs/09_Technical/Implementation_Packets/Home_Island/IMP_HOM_019_Manual_Map_Build_Ashford_Shop.md`
- `../TheLastSwordProtocol-Atlas/atlas/docs/02_World/Screens/Home_Island/SCR_HOM_ASH_001_Ashford_Exterior.md`, `SCR_HOM_ASH_002_Elara_House.md`, `SCR_HOM_ASH_003_Ashford_Shop.md`
- `../TheLastSwordProtocol-Atlas/atlas/docs/03_Story/Dialogue/Home_Island/Ashford_Dialogue_Packet.md` (`ATLAS-STY-010`)
- `../TheLastSwordProtocol-Game/map_ownership.json`, `../TheLastSwordProtocol-Game/AGENTS.md` (current Game repo state, read-only)
- `bridges/rpg-maker-mz/passability-rule.md`, `studio/agent-roles.md`, `studio/immutable-formatting-rule.md`

## Deliverables

- `reports/implementation-contracts/ashford-village-contract.md`
- `reports/implementation-contracts/ashford-shop-build-contract.md`
- `reports/implementation-contracts/ashford-dialogue-application-contract.md`
- `reports/implementation-contracts/ashford-existing-map-verification-contract.md`

## Acceptance Criteria

- Every contract cites its authoritative Atlas source files by exact path and, where applicable, canonical ID.
- Every contract names exact `TheLastSwordProtocol-Game` file targets, not general areas.
- Every contract states ownership restrictions (map ownership ledger state, hand-authored vs. generated) and derives what may/must not be modified from that ledger rather than asserting it independently.
- Every contract states passability and route validation requirements grounded in `bridges/rpg-maker-mz/passability-rule.md` and, where relevant, the packet's own collision/route requirements.
- Every contract states sample-map or sample-content quality expectations (map size discipline, SVG-guide-as-relationship-diagram caveat, tone rules, or dialogue tone rules, as applicable).
- Every contract states concrete, testable acceptance criteria drawn from the underlying Atlas packet/screen object, not invented independently.
- Every contract recommends an implementing agent with reasoning tied to `studio/agent-roles.md`.
- No contract authorizes regenerating Map001 or Map002, inventing new Ashford canon, or treating `atlas-exports/home-island.json` as current.
- No file in `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` is modified.

## Verification Steps

```bash
find reports/implementation-contracts -name "*.md"
git diff --stat -- projects/the-last-sword-protocol/graph
# expect no output: this work order does not touch canon or graph structure
python3 tools/atlas_format/format_guard.py --check
```

## Allowed Changes

- `reports/implementation-contracts/ashford-village-contract.md`
- `reports/implementation-contracts/ashford-shop-build-contract.md`
- `reports/implementation-contracts/ashford-dialogue-application-contract.md`
- `reports/implementation-contracts/ashford-existing-map-verification-contract.md`
- `work-orders/WO-0020-ashford-village-implementation-contract-from-atlas-handoff.md`

## Protected Areas

- Do not modify `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game`.
- Do not modify canon (Atlas's or AtlasStudio's).
- Do not generate or regenerate maps.
- Do not redesign Ashford Village.
- Preserve the Immutable Formatting Rule.

## Notes for Assigned Agent

Treat `reports/ashford-village-implementation-packet-readiness.md` as the single authoritative verdict - it has already done the conflict/staleness analysis. This work order's job is to translate that verdict into contracts an implementing agent can execute against, not to re-litigate it. Map001 and Map002 get a verification/handoff contract, never a build contract; Map003 gets a build contract because its ledger state is `generated`, not `hand_authored`. Dialogue application is scoped to the NPCs still on placeholder text (Elder, Child, Farmer, Skyreach Joker, Dock Messenger, tremor scene) on Map001 - Elara (Map002) is already final and the Shopkeeper (Map003) belongs to the shop build contract per `IMP-HOM-019`'s own traceability table, to avoid two contracts claiming the same event.

## Submission Record

Submitted 2026-07-07 by Claude Code.

Delivered:

- `reports/implementation-contracts/ashford-village-contract.md` - parent contract establishing Atlas source authority, the full authoritative-source table, the confirmed staleness of `atlas-exports/home-island.json`, the village-wide ownership ledger, and a routing table to the three child contracts.
- `reports/implementation-contracts/ashford-shop-build-contract.md` - build contract for Map003 from `IMP-HOM-019`, the only Ashford map whose ledger state (`generated`) permits a build rather than a verification contract.
- `reports/implementation-contracts/ashford-dialogue-application-contract.md` - content-application contract for the remaining placeholder Ashford NPCs on Map001 (Elder, Child, Farmer, Skyreach Joker, Dock Messenger, tremor scene), sourced from `ATLAS-STY-010`, explicitly excluding Elara (already final) and the Shopkeeper (owned by the shop build contract).
- `reports/implementation-contracts/ashford-existing-map-verification-contract.md` - verification/handoff contract for Map001 and Map002 against `IMP-HOM-017`/`IMP-HOM-018`, explicitly prohibiting regeneration and requiring human playtest certification before either map is flipped to `locked`.

No file in `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` was modified - verified directly (read-only inspection only). No AtlasStudio canon file was modified. No map was generated or regenerated. No new Ashford canon was created.

Formatting: preserved existing house style; no existing file was reformatted.

Verification performed:

```bash
find reports/implementation-contracts -name "*.md"
git diff --stat -- projects/the-last-sword-protocol/graph
python3 tools/atlas_format/format_guard.py --check
```
