# Ashford Dialogue Application Contract

**Child contract of:** `reports/implementation-contracts/ashford-village-contract.md`
**Scope:** Non-Elara, non-Shopkeeper Ashford NPC dialogue on Map001 (Ashford Exterior), plus the tremor-event scene
**Type:** Content-application contract - applies existing Atlas-authoritative scaffold text; does not write new dialogue.

---

## 1. Authoritative Atlas Source Files

| File | Role |
|---|---|
| `atlas/docs/03_Story/Dialogue/Home_Island/Ashford_Dialogue_Packet.md` (`ATLAS-STY-010`) | **Sole dialogue source.** Provides scaffold lines, by story state, for every NPC in scope. No line may be written that is not derived from this packet. |
| `atlas/docs/03_Story/Quests/Home_Island/QST_HOM_001_Home_Island_Opening.md` | Confirms switch/story-state scope this dialogue must respect. |
| `atlas/docs/09_Technical/Registries/Home_Island_Event_Registry.md` | Canonical event IDs `EVT-HOM-003` (Child), `EVT-HOM-004` (Farmer), `EVT-HOM-005` (Skyreach Joker), `EVT-HOM-006` (Dock Messenger), `EVT-HOM-009` (Tremor Trigger), and the placeholder Village Elder event. |
| `atlas/docs/02_World/Screens/Home_Island/SCR_HOM_ASH_001_Ashford_Exterior.md` | Confirms NPC roster and placement this dialogue applies to. |
| `atlas/docs/09_Technical/Implementation_Packets/Home_Island/IMP_HOM_017_Manual_Map_Build_Ashford_Exterior.md` | Confirms these events already exist on Map001 and their story-state gating pattern. |

**Precedent to follow exactly:** Elara's dialogue on Map002 is already applied from `ATLAS-STY-010` as final text (not placeholder) - per `reports/ashford-village-implementation-packet-readiness.md` Section 5. This contract reproduces that same pattern for the remaining NPCs; it does not invent a new process.

## 2. Explicit Scope Boundary (Read Before Starting)

This contract applies to exactly these NPCs and events, all on Map001:

- Village Elder (placeholder event, no assigned `EVT` ID yet)
- Child Near Old Panel (`EVT-HOM-003`)
- Farmer With Warm Stones (`EVT-HOM-004`)
- Skyreach Joker (`EVT-HOM-005`)
- Dock Messenger (`EVT-HOM-006`)
- The tremor-event scene (`EVT-HOM-009` and any Show Text commands it triggers)

**Explicitly out of scope:**

- **Elara** (Map002) - already final; do not re-touch unless a defect is found, in which case raise a separate fix.
- **Shopkeeper** (`EVT-HOM-008`, Map003) - owned by `ashford-shop-build-contract.md` per `IMP-HOM-019`'s own traceability table. Do not duplicate this work here.

## 3. Exact Game Repo Targets

| Target | Action |
|---|---|
| `TheLastSwordProtocol-Game/data/Map001.json` | Modify Show Text event command content only, for the six items listed in Section 2. |

No other Game repo file is in scope for this contract.

## 4. Ownership Restrictions

Map001 is `hand_authored` in `map_ownership.json`. This contract is explicitly authorized to make narrowly-scoped Show Text edits within existing event pages despite that ledger state - it is not a pipeline/generator write and does not touch map geometry, tiles, collision, transfers, or event page structure. Any edit outside "replace placeholder Show Text with `ATLAS-STY-010` text" is not authorized by this contract.

## 5. What May Be Modified

- Show Text event command content on the six in-scope events on Map001.
- Nothing else.

## 6. What Must Not Be Modified

- Map001 geometry, tiles, collision, regions, transfers, or event page/switch/self-switch structure. Preserve switch and self-switch logic exactly; only the displayed text changes.
- Elara's dialogue on Map002 (already final; out of scope).
- Shopkeeper dialogue on Map003 (owned by the shop build contract).
- `ATLAS-STY-010` or any other Atlas canon file.
- No new story beats beyond the existing `QST-HOM-001` / Ashford Dialogue Packet scope. Do not invent lines, states, or NPC reactions not present in `ATLAS-STY-010`.
- Do not duplicate the Elara tremor/warning beat in any Skyreach or Hidden Cave file - it belongs to Ashford only.
- The two open questions in `ATLAS-STY-010` (should the Village Elder become a named Character object; should the dock messenger be reused at Rustshore Docks; should Elara give Kai a starting item) are Creative Director calls. Do not resolve them - implement the NPCs exactly as scaffolded, unnamed and functional.

## 7. Passability and Route Validation Requirements

This is a text-only contract; it must not change event placement or reachability. Confirm before and after that:

- All six in-scope events remain on the same tiles they occupy today (no placement change).
- No event's Show Text edit introduces a new page, trigger type, or movement route that could change passability.
- If `ashford-village-route-validation.md`'s Part A checklist was previously passing for these events' reachability, it must still pass unchanged after this contract's edits, since no placement changed.

## 8. Sample-Content Quality Expectations

Per `ATLAS-STY-010`'s Tone Rules, apply verbatim to every line written:

1. Keep lines short enough for RPG Maker message boxes.
2. Avoid modern technical vocabulary early.
3. Let villagers misinterpret technology naturally.
4. Use warmth and humor beside mystery.
5. NPCs should change after major events (state-gated text, not a single static line).

Each NPC's scaffold lines in `ATLAS-STY-010` are directional, not necessarily final word-for-word text - light editorial polish to fit message-box constraints is expected, but the meaning, tone, and story beat per state must not change. When in doubt, prefer the scaffold text as-written over paraphrasing.

## 9. Acceptance Criteria

- No visible `[Placeholder]` text remains on any of the six in-scope events, except any explicitly marked noncritical in a future Atlas dialogue-packet revision.
- Every in-scope NPC's dialogue reflects the correct state per its defined switches (at minimum Intro vs. After Tremor/After Sword/After Node Seven, per each NPC's scaffold in `ATLAS-STY-010`).
- Switch and self-switch logic and event page structure are unchanged from before this contract's execution - only Show Text content differs.
- The Elara tremor/warning beat appears in Ashford only, not duplicated elsewhere.
- No new NPC, story beat, or dialogue state was introduced beyond what `ATLAS-STY-010` already scaffolds.

## 10. Recommended Implementing Agent

**Claude Code, or a human writer** - not Codex for the writing step. Per `ATLAS-STY-010`'s own Implementation Notes: "Codex should place placeholder versions of these NPCs in Ashford and create event pages by story switch. Claude or a human writer can later expand final dialogue while preserving these roles." That placeholder-placement step is already done (per `reports/ashford-village-implementation-packet-readiness.md` Section 5); this contract is exactly the "expand final dialogue" step the packet reserves for Claude or a human. Codex may still perform the mechanical event-command edit once final text is chosen, per `studio/agent-roles.md`'s guidance on applying work orders to a codebase - but text selection/editing should not be delegated to Codex alone.

## 11. Non-Goals

- Does not write new dialogue beyond what `ATLAS-STY-010` scaffolds.
- Does not touch Elara (Map002) or the Shopkeeper (Map003).
- Does not change map geometry, event placement, or transfer logic.
- Does not resolve the Village Elder naming, Dock Messenger reuse, or Elara starting-item open questions.
- Does not promote any unnamed NPC to a registered Character object.
