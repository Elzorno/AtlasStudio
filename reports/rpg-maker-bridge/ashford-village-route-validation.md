# Ashford Village Route Validation

## Purpose

This document defines the required routes that must always remain traversable in Ashford Village, per `bridges/rpg-maker-mz/passability-rule.md`'s Route Validation section. Because `implementation-preflight.md` identifies an unresolved conflict between AtlasStudio's Ashford Village design and `TheLastSwordProtocol-Atlas`'s already-implemented version, this document validates two things separately: the routes **already implemented and real** in `TheLastSwordProtocol-Game` today, and the routes **AtlasStudio's `WP-03` production package** specified, pending resolution of that conflict.

## Part A - Routes Already Implemented (`TWN_Ashford_Exterior`, Map001)

These routes exist today in the target repository, confirmed by direct inspection of `data/Map001.json`. They are not proposals; they are what is already built and hand-authored.

```text
player_start (Elara House exit, TRN-HOM-002)
  -> village_green_area
      -> ashford_shop (TRN-HOM-003 Enter Ashford Shop)
      -> north_route_to_skyreach (TRN-HOM-005)
      -> southeast_route_to_rustshore (TRN-HOM-007)
      -> east_route_to_glassfield (TRN-HOM-015)
      -> optional_east_route_to_fogfen (TRN-HOM-027)
```

Also present: a "Village Elder Placeholder" event and several NPCs (Child Near Old Panel, Farmer With Warm Stones, Skyreach Joker, Dock Messenger) whose reachability should be re-validated once their final roles are confirmed under whichever canon path is chosen.

**Required validation for this part (can be performed independent of the primary blocker):**

- [ ] `player_start` (Map002 exit, `TRN-HOM-001`) is on a passable tile.
- [ ] `TRN-HOM-002` (Enter Elara House) is reachable and reciprocal (a return transfer exists on Map002 - confirmed: `TRN-HOM-001 Elara House exit`).
- [ ] `TRN-HOM-003` (Enter Ashford Shop) is reachable.
- [ ] `TRN-HOM-005` (North path to Skyreach) is reachable.
- [ ] `TRN-HOM-007` (South/east route to Rustshore) is reachable.
- [ ] `TRN-HOM-015` (Route to Glassfield) is reachable.
- [ ] `TRN-HOM-027` (Optional east route to Fogfen Marsh) is reachable.
- [ ] All five NPC events (Child, Farmer, Skyreach Joker, Dock Messenger, Village Elder Placeholder) sit on tiles reachable from `player_start`.
- [ ] No wall, roof, cliff, or water tile on Map001 is walkable unless intended (requires human playtest per the Passability Rule - not verifiable from JSON inspection alone).

This part requires a human playtest pass in the RPG Maker MZ editor/runtime to confirm; JSON inspection alone confirms event placement and transfer command presence, not actual tile-level passability, per the Passability Rule's own "Human Playtest Still Required" section.

## Part B - Routes Specified By AtlasStudio's `WP-03` Production Package (Pending Blocker Resolution)

These routes come from `projects/the-last-sword-protocol/production/ashford-village-implementation-checklist.md`, produced before this preflight identified the primary blocker. They assume the AtlasStudio Hero/Rowan/Elara/four-building village design and **should not be executed until the primary blocker in `implementation-preflight.md` is resolved**, since they describe a building roster (Rowan's Cottage, General Store, Blacksmith, Inn) that does not match what is already hand-authored in the target repository.

```text
player_start (Rowan's Cottage)
  -> village_green
      -> general_store_door
      -> blacksmith_door
      -> inn_door
      -> village_exit -> ashford_vale_overworld
```

**Required validation for this part, if and when this path is chosen:**

- [ ] `player_start -> village_green`
- [ ] `village_green -> rowan_cottage_door`
- [ ] `village_green -> general_store_door`
- [ ] `village_green -> blacksmith_door`
- [ ] `village_green -> inn_door`
- [ ] `village_green -> village_exit`
- [ ] `village_exit -> ashford_vale_overworld`

## Comparing The Two Route Sets

Both route sets agree on the underlying shape: a single-hub (Green) village with one home, one shop, and outbound routes toward the wider region (Rustshore and Glassfield appear in both). They disagree on hub population (four named buildings vs. one home + one shop + placeholder elder) and on which locations exist at all (Skyreach Hill and Fogfen Marsh are already implemented outbound routes in Part A; AtlasStudio's canon graph has no Skyreach Hill node and treats Fogfen Marsh as optional/deferred content, not an implemented route). Any resolution of the primary blocker should reconcile this route-level disagreement explicitly, not just the character-level one.

## Future Validation Requirements

- **Automated passability validator:** neither AtlasStudio nor the target repository currently has one. `bridges/rpg-maker-mz/passability-rule.md` anticipates this; building it should be a distinct future work order (candidate name: an "RPG Maker Route and Passability Validator" tool under `tools/rpg_maker_bridge/`), reading `Tilesets.json` passability flags and each map's `data` array directly rather than relying on human playtest alone.
- **Cross-repository route consistency check:** once the primary blocker is resolved, a validation step should confirm that AtlasStudio's canon graph (`region.ashford_vale CONTAINS ...` edges) and `TheLastSwordProtocol-Atlas`'s Canonical ID Registry describe the same set of reachable locations, so the two systems cannot silently drift apart again the way they already have.
- **Reciprocal transfer check:** every transfer should be validated as having a matching return transfer on the destination map (confirmed manually for `TRN-HOM-001`/`TRN-HOM-002` in this report; not yet checked for the others in Part A, and not yet applicable to Part B).

## Verification Performed

```bash
# Read-only JSON inspection of TheLastSwordProtocol-Game/data/Map001.json and Map002.json
# No RPG Maker file modified.
python3 tools/atlas_format/format_guard.py --check
```
