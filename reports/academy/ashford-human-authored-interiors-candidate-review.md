# Ashford Human-Authored Interiors Candidate Review

Status: submitted

Scope: `TheLastSwordProtocol-Game` commit `d64425f37fa7c4dea40b410d54b91659d312a5fa` (`d64425f Record human-authored Ashford interiors candidate`), covering:

- `data/Map002.json` - `INT_Ashford_ElaraHouse`
- `data/Map003.json` - `INT_Ashford_Shop`
- `map_ownership.json` entries for maps 2 and 3

This is a candidate review, not an acceptance decision and not an Academy reference-source approval. The maps are human-authored candidates pending Atlas review plus human playtest/acceptance.

## Provenance

The reviewed state was committed in `TheLastSwordProtocol-Game` after manual RPG Maker edits to Elara House and Ashford Shop.

`map_ownership.json` marks both maps as:

- `state: hand_authored`
- `implementation_status: human_authored_candidate`
- `review_status: pending_atlas_review`

Map002 also preserves the prior rejected automated build as history under `prior_rejection`; the current human-authored candidate supersedes that failed Codex layout but has not yet been accepted.

## Structural Change Summary

Compared with the previous committed state:

- Map002 kept its `17x13` dimensions and `Inside` tileset, with 148 tile slots changed.
- Map003 kept its `17x13` dimensions and `Inside` tileset, with 131 tile slots changed.
- Map002 moved the player start to `(8,11)`, the keepsake event to `(9,2)`, and several decorative helper events to match the new hand layout.
- Map003 moved the shopkeeper to `(8,3)`, the exit to `(8,8)`, and added or repurposed a reachable counter interaction marker at `(8,5)`.
- `System.json` changed only RPG Maker editor state: `editMapId` and `versionId`.

## Validation Performed

JSON validation:

- All `TheLastSwordProtocol-Game/data/*.json` files parse.
- `map_ownership.json` parses.
- Maps 2 and 3 remain `hand_authored`.

Map metadata:

- Map002 uses tileset `3` (`Inside`), has zero encounters, and has no nonzero region IDs.
- Map003 uses tileset `3` (`Inside`), has zero encounters, and has no nonzero region IDs.

Transfer checks:

- Map001 `TRN-HOM-002 Enter Elara House` sends the player to Map002 `(8,11)`.
- Map002 `TRN-HOM-001 Elara House exit` returns to Map001 `(17,28)`.
- Map001 `TRN-HOM-003 Enter Ashford Shop` sends the player to Map003 `(8,6)`.
- Map003 `TRN-HOM-004 Shop exit` returns to Map001 `(30,19)`.

Passability/reachability was checked against `Tilesets.json` passage flags using an RPG Maker-style directional passage scan, with same-priority non-through events treated as blockers.

Map002 from incoming/player-start tile `(8,11)`:

- PASS: Elara is reachable by adjacent interaction at `(6,5)`.
- PASS: Elara House exit at `(8,12)` is directly reachable.
- PASS: Keepsake shelf at `(9,2)` is reachable by adjacent interaction.

Map003 from incoming tile `(8,6)`:

- PASS: Shop exit at `(8,8)` is directly reachable.
- PASS: Metal cabinet at `(12,3)` is reachable by adjacent interaction.
- PASS: Counter interaction marker at `(8,5)` is directly reachable.
- GAP: The visible shopkeeper event at `(8,3)` is not directly or adjacently reachable from the customer side.

## Findings

### 1. Shopkeeper Interaction Is Not Yet Wired

Map003 appears to use a correct customer-side interaction idea: the shopkeeper remains behind the counter, while a reachable event at `(8,5)` marks where the player should stand to talk across the counter.

However, event `10` (`EVT-HOM-08 Activate Shopkeeper`) currently contains only a comment and no dialogue, shop-processing command, or delegation to the shopkeeper event. The actual shopkeeper event at `(8,3)` still contains the real dialogue and Shop Processing command, but it is not reachable from the player side.

Recommendation: keep the hand-authored counter composition, but move or copy the shopkeeper interaction pages onto the reachable counter event at `(8,5)`, or otherwise wire that event to run the same dialogue and Shop Processing behavior.

### 2. Map002 Keepsake Text Remains Placeholder

Map002's keepsake event is now structurally reachable, but its interaction text remains:

```text
[Placeholder] Examine: Elara Keepsake.
```

Recommendation: either replace this with final lore text before acceptance or explicitly track it as an accepted-with-notes item.

### 3. Visual Tile-Assembly Quality Still Requires Human Review

The prior rejection centered on visual multi-tile assembly: windows, mirrors, rug pieces, and couch/shelf pieces were incomplete. The current candidate was hand edited specifically to address that class of issue, and the structural data changed substantially.

AtlasStudio does not yet have a committed reusable RPG Maker map renderer, so this review does not claim visual acceptance from JSON alone. Human RPG Maker inspection or screenshots should confirm:

- two-tile windows/mirrors are complete;
- rug pieces are complete and aligned;
- couch/shelf left, center, and right pieces are present where intended;
- no event is placed on the visual edge of furniture unless that is intentionally readable;
- the interiors meet the RPG Maker sample-map quality bar.

## Academy Learning Intake

These maps should not become positive Academy reference evidence until a human playtest/acceptance decision is recorded.

If accepted, the hand-authored candidate can become `approved_project_map` evidence for:

- complete multi-tile interior object assembly;
- small-home composition for `INT_Ashford_ElaraHouse`;
- customer-side counter interaction composition for `INT_Ashford_Shop`, once the proxy interaction is wired.

Until then, the actionable learning is diagnostic:

- Atlas-generated or Atlas-assisted map review must check multi-tile object completeness visually, not just tile-ID presence.
- Counter-service layouts need both visual composition and interaction routing; a reachable proxy marker without the shop command is not playable.
- `hand_authored` ownership protects a map from regeneration but does not imply acceptance.

## Review Outcome

Map002 is structurally ready for human visual review and playtest, with the keepsake placeholder as the main known content caveat.

Map003 needs a small implementation revision before acceptance: the reachable counter interaction event must run the shopkeeper dialogue and Shop Processing behavior.

Neither map should be marked accepted or promoted to Academy reference status until those checks are complete.
