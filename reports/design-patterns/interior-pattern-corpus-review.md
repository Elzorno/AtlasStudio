# Interior Pattern Corpus Review

Status: submitted

Scope: `WO-0025`. Analyzes the seven remaining official RPG Maker MZ interior sample maps not covered by `WO-0024` (House 1, House 2, Inn, Weapon & Armor Shop, Bar, Chief's House 1F, Chief's House 2F), compares each against the existing `interiors/shop.pattern.md` (`PAT-INTERIOR-SHOP`, derived from the Item Shop sample), determines which layout, composition, passability, and event rules recur across the corpus versus which are specific to one building type, and reviews `shop.pattern.md`'s confidence level in light of the new evidence.

This report is analysis and evidence, not implementation guidance. It extracts reusable design patterns for AtlasStudio's standing library; it does not direct any build against `TheLastSwordProtocol-Game` or `TheLastSwordProtocol-Atlas`.

## Source Data

All eight interiors in the corpus (the previously analyzed Item Shop plus the seven analyzed here) live in `TheLastSwordProtocol-Game/data/`, on `tilesetId: 3` ("Inside"), as part of the same official RPG Maker MZ sample project imported into the game's map tree:

| Map | Map Tree Name | Dimensions | Events | Pattern Document |
|---|---|---|---|---|
| `Map018.json` | House 1 | 17x13 | 3 | `interiors/house.pattern.md` |
| `Map019.json` | House 2 | 17x13 | 2 | `interiors/house.pattern.md` |
| `Map020.json` | Inn | 20x17 | 5 | `interiors/inn.pattern.md` |
| `Map021.json` | Item Shop | 17x13 | 2 | `interiors/shop.pattern.md` (existing, `WO-0024`) |
| `Map022.json` | Weapon & Armor Shop | 17x13 | 2 | `interiors/weapon-shop.pattern.md` and `interiors/armor-shop.pattern.md` (shared source) |
| `Map023.json` | Bar | 17x13 | 4 | `interiors/bar.pattern.md` |
| `Map024.json` | Chief's House 1F | 20x17 | 6 | `interiors/chief-house.pattern.md` |
| `Map025.json` | Chief's House 2F | 20x17 | 6 | `interiors/chief-house.pattern.md` (shared building with 1F) |

Extraction was performed directly against each map's JSON tile-layer data and event list, cross-checked against `Tilesets.json` tileset 3 for tile-ID-family boundaries (A1 water, A2 ground autotiles, A3 building autotiles, A4 wall autotiles, A5 single non-auto tiles including the stairs/darkness family, and B/C/D/E overlay objects), following the method in `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`. No standalone per-map extraction report was produced for this work order (unlike `Map021`'s pre-existing `reports/map-analysis/item-shop-analysis.md`); the evidence trail lives in this review and in each pattern document's own `Source`/`Observed Maps` sections, per `PATTERN_EXTRACTION_GUIDE.md`'s citation discipline.

**A note on transfer target map IDs:** every exterior-door transfer event across the corpus points at a numeric map ID from the *original, standalone* RPG Maker sample project (most commonly "map 2"), not at any map ID meaningful within `TheLastSwordProtocol-Game`'s current map tree. `Map021`'s own prior analysis already flagged this ("no current project event transfers into Map021"). This review treats every observed transfer target as a **structural artifact** (proof that a transfer event exists, is player-touch triggered, and is paired with a `Move1` sound effect) and explicitly not as meaningful destination data - consistent with `PATTERN_EXTRACTION_GUIDE.md`'s "What Not to Infer" guidance. No pattern document in this corpus cites a specific numeric transfer target as a rule.

## Recurring Layout Rules

Findings that hold across most or all of the corpus, not just one building type:

1. **Architectural shell inside a void border.** Every one of the eight interiors sits inside a rectangular wall/floor shell surrounded by an outer void/darkness margin, on the same `Inside` tileset. This is the single most universal finding in the corpus (8/8) and is already stated in `shop.pattern.md`.
2. **Vertical threshold stack for exterior doors.** Every exterior door in the corpus (7/7 buildings with a ground-level exterior door; the Chief's House 2F correctly has none, see below) uses the same three-tile vertical stack: a stairs-family tile one row above a floor tile carrying the player-touch transfer event, with a shadow value marking the recess. `shop.pattern.md` already states this; the corpus fully corroborates it, with one **scaled variant**: the Chief's House's internal 1F-to-2F staircase uses the same construction widened to three tiles, because it must serve floor-to-floor traffic rather than single-direction egress. This scaled variant is new evidence, captured in `chief-house.pattern.md`.
3. **Shell size families, not a single fixed size.** `shop.pattern.md`'s Layout Rules describe "keep the room compact" without naming a specific size. The corpus shows this compactness comes in (at least) two families: a 17x13 shell (Item Shop, House 1, House 2, Weapon & Armor Shop, Bar) and a 20x17 shell (Inn, Chief's House 1F/2F) for structurally larger, multi-zone buildings. Building scale tracks structural complexity, not narrative importance alone - the Inn and the Chief's House share a shell size despite different social status, because both need room for internal zoning.
4. **Centered entrance is common, not universal.** Four of eight interiors (Item Shop, House 1, House 2, Weapon & Armor Shop) center their single exterior door exactly on the room's horizontal midpoint. Two (Chief's House 1F) center it approximately. Two (Inn, Bar) do not: the Inn's door centers on its common room's own sub-axis rather than the full building's, and the Bar's door is off-center with no structural cause evident from the data - it reads as a legitimate composition choice. `shop.pattern.md` v1.0 already hedges this rule ("unless a specific narrative or spatial reason requires an off-center door"); the corpus confirms the hedge was correctly cautious rather than confirming an unconditional rule.

## Recurring Composition Rules

1. **No universal wall-anchoring rule.** `shop.pattern.md` states "anchor all shelving and heavy storage furniture directly against a wall... do not leave shelf-type objects floating in open floor" as a Layout Rule and lists floating furniture as a Common Mistake. The corpus shows this is a **display/storage-specific convention, not a universal interior rule**: `house.pattern.md` and `weapon-shop.pattern.md` corroborate it for storage furniture, but `bar.pattern.md` is a direct, clear counterexample - the Bar's furniture is overwhelmingly scattered as small floating islands across the open floor, which is correct and intentional for a social/seating space. This is the single most important correction this corpus makes to the existing pattern set: **wall-anchoring applies to merchandise/storage furniture; social/seating furniture is expected to float.** Any future revision of `shop.pattern.md` should consider narrowing this rule's stated scope explicitly (see Recommendations below) rather than leaving it phrased as if universal.
2. **Decoration density scales with function, not just size.** Two same-size buildings can carry very different furniture density: `house.pattern.md` (17x13) is sparsely furnished (one back-wall shelf run plus at most one small accent), while `shop.pattern.md`, `weapon-shop.pattern.md`/`armor-shop.pattern.md`, and `bar.pattern.md` (also 17x13) are all much denser. Density tracks what the room is *for* - dwelling versus browsing versus socializing - not footprint.
3. **Flame count and placement scale with zoning, not room size alone.** Single-zone rooms use one to two decorative flames near the top wall (Item Shop: 1, House 2: 1, House 1: 2 bilateral, Weapon & Armor Shop: 1). Multi-zone buildings use more, distributed per zone (Inn: 4 across two zones, including the corpus's first wall-mounted sconce; Bar: 3 spread across one large room; Chief's House: 2 on 1F, 3 on 2F, including the corpus's first interior hearth-style flame). This is a clean, well-corroborated recurring rule: **flame count should track the number of zones/functional areas a room has, not its raw tile area.**
4. **Wall stock continuity varies by what is displayed.** `house.pattern.md`'s shelving is a continuous, unbroken run; `weapon-shop.pattern.md`'s wall stock is individually spaced with visible gaps. Both are "anchored to a wall," but continuity differs by whether the goods are meant to read as uniform stacked stock (continuous) or individually notable pieces (spaced). This refines rather than contradicts `shop.pattern.md`'s wall-anchoring rule.

## Recurring Passability Rules

1. **Reachability ring holds everywhere it was checked.** Every intended interactable display object checked across the corpus (Item Shop's prior analysis, and this review's direct check of the Weapon & Armor Shop's back-wall and side-wall stock) has at least one adjacent walkable tile, and deep, boxed-in stock with zero adjacent walkable tiles is treated as pure visual mass rather than a broken interactable - confirming `shop.pattern.md`'s existing distinction between "reachable display" and "background stock" is sound and reusable, not an artifact of one map.
2. **No region/encounter data anywhere in the corpus.** Every map checked has region ID 0 across its entire tile grid. This corroborates `shop.pattern.md`'s "Regions: none, zero encounters" finding (originally specific to the Item Shop) as a corpus-wide convention: **no interior in this official sample set uses encounter regions.**
3. **Zone connections use deliberate chokepoints, not open boundaries.** Where a building has more than one zone (Inn, Chief's House 2F), the zones never share a wide-open boundary - they connect through a single narrow corridor or doorway gap. The Inn uses a two-tile-wide spine; the Chief's House 2F uses a corridor spine connecting several fully walled chambers, a step further than the Inn's partition-only zoning. This is new evidence beyond what `shop.pattern.md` (a single-zone building) could establish.
4. **Multi-tile transfer surfaces exist for higher-traffic connections.** The Chief's House's internal staircase repeats the same touch-transfer event across all three stair tiles, rather than the single-tile transfer used at every ordinary exterior door in the corpus. This is a legitimate, evidenced scaling of the threshold convention, not a deviation from it.

## Recurring Event Conventions

1. **Zero shopkeeper, innkeeper, bartender, resident, or any other NPC event anywhere in the corpus.** This is the strongest, most universal finding in the entire review: **all eight interiors, across every building type, ship with zero character/NPC events.** `shop.pattern.md`'s existing claim that "this sample teaches atmosphere/layout, not commerce mechanics" is not a one-map observation - it is a corpus-wide convention of the official sample set. Every new pattern document in this corpus restates this explicitly rather than assuming a future implementer will infer it.
2. **Decorative events never carry gameplay commands.** Every `!Flame`-image event across the corpus has an empty command list. Purely decorative.
3. **Exactly one player-touch transfer event per direction of travel at every ordinary threshold**, paired with a `Move1` sound effect, confirmed at every single-tile doorway in the corpus.
4. **No secondary transfer between zones within one building**, except where an actual floor change occurs (Chief's House). The Inn's common room and guest wing connect by walkable corridor, not by a transfer event - zoning within one floor is a passability/layout fact, not an event.

## Comparison Table: New Patterns Against `shop.pattern.md`

| Pattern | Shell | Confidence | Primary deviation from `shop.pattern.md` |
|---|---|---|---|
| `house.pattern.md` | 17x13 (same family) | High (2 independent maps) | Much lower decoration density; no bilateral side clusters; continuous back-wall shelf only. |
| `inn.pattern.md` | 20x17 (larger family) | Medium | Multi-zone building; off-center door aligned to a sub-zone axis; wall-mounted sconce flame; zone chokepoint connection. |
| `weapon-shop.pattern.md` | 17x13 (same family, shared source with armor-shop) | Medium (shared-source caveat) | Individually spaced wall-mounted rack stock instead of continuous shelving; taller/deeper wall cluster. |
| `armor-shop.pattern.md` | 17x13 (same family, shared source with weapon-shop) | Medium (shared-source caveat) | Compact secondary counter/table display instead of a dominant wall or central feature. |
| `bar.pattern.md` | 17x13 (same family, wider interior shell) | Medium | Directly overrides the wall-anchoring composition rule; floating furniture islands; off-center door with no structural cause; no single centerline aisle. |
| `chief-house.pattern.md` | 20x17 (larger family) | Medium (same-building two-floor caveat) | Only multi-floor interior in the corpus; internal multi-tile staircase; true multi-room chamber layout on the upper floor; stricter bilateral hall symmetry. |

## Confidence Review: `interiors/shop.pattern.md`

**Current state:** `shop.pattern.md` v1.0 is filed at `confidence: medium`, corroborated by exactly one official sample map (`Map021`, Item Shop), per `PATTERN_CONFIDENCE_MODEL.md`'s Medium bar ("observed once, in a single official RPG Maker sample map, with no corroborating second source yet").

**New evidence available:** this review's direct extraction and check of `Map022` ("Weapon & Armor Shop") against `shop.pattern.md`'s own stated rules. Unlike `weapon-shop.pattern.md` and `armor-shop.pattern.md` (which each describe only a zone of `Map022`), the *whole* Weapon & Armor Shop map independently satisfies `shop.pattern.md`'s Required Conditions (single room, one entrance, retail browsing function, town-embedded) and was checked rule-by-rule against `shop.pattern.md`'s Layout, Composition, Passability, and Event Rules:

| `shop.pattern.md` rule | Result against `Map022` |
|---|---|
| Compact shell, small playable footprint inside a larger map | Match - identical 17x13 shell, same architectural bounds as Item Shop. |
| Centered entrance on primary axis | Match - identical door position (x8 of 17). |
| Spawn one tile inside doorway | Match - identical threshold construction. |
| Visible threshold + player-touch transfer | Match - identical stairs-tile-plus-floor-tile-plus-event construction. |
| Direct centerline from entrance to focal point | Match, and reinforced - the centerline terminates exactly at a back-wall focal display item, an even tighter read than the Item Shop's open centerline. |
| One-tile-plus customer lane, widening at branches | Match - open floor from the threshold through the main aisle. |
| Shelving/storage anchored to a wall, never floating | Match on the underlying invariant (all stock touches a wall); the specific continuity style (individually spaced rather than continuous) is a legitimate variant, not a violation - captured as a refinement in `weapon-shop.pattern.md`, not a contradiction of `shop.pattern.md`. |
| Goods clustered by surface/purpose | Match - a distinct wall-rack cluster and a distinct counter cluster, not scattered. |
| Dense perimeter, light center | Match - furniture concentrated at back and side walls, open through the middle. |
| At least one decorative animated flame | Match - one `!Flame` event present. |
| No shopkeeper/NPC assumed by default | Match - zero NPC events. |
| Reachability ring for intended interactables | Match, checked directly - every back-wall and side-wall item has at least one adjacent walkable tile except one deep corner tile, which is correctly treated as background visual mass rather than a broken interactable, consistent with `shop.pattern.md`'s own stated exception. |
| Region-free passability | Match - region ID 0 throughout. |

Every rule in `shop.pattern.md` was checked against this second map and found to hold, with only the wall-stock-continuity detail showing a stylistic (not structural) variant, which this review resolves by treating "anchored to a wall" as the corroborated invariant and "continuous vs. spaced" as a legitimate sub-choice - not evidence against the pattern.

**Recommendation: promote to High is justified, but is not applied by this work order.**

The evidence meets `PATTERN_CONFIDENCE_MODEL.md`'s stated bar for Medium-to-High promotion: "a second official sample map... corroborates the same rule[s]." `Map022` is a second, independent official sample map (not a second floor of the same building, and not merely a second zone of an already-cited map) that satisfies `shop.pattern.md`'s own Required Conditions and confirms its Layout, Composition, Passability, and Event Rules without contradiction. Per `PATTERN_CONFIDENCE_MODEL.md`, this is exactly the corroboration threshold High confidence describes.

**However, per this work order's explicit instruction ("Do not automatically promote confidence"), this review does not itself edit `shop.pattern.md`.** `shop.pattern.md` is not among `WO-0025`'s listed deliverables or Allowed Changes, and `PATTERN_REVIEW_PROCESS.md` treats a confidence change as its own reviewable event with its own version bump - not a side effect to fold silently into a different work order's file list. The recommendation stands as follows, for action by a follow-up work order or explicit maintainer decision:

- Update `shop.pattern.md` frontmatter: `confidence: high`; add `Map022.json` ("Weapon & Armor Shop") to `observed_maps`; bump `version` to `1.1` (a confidence-level change with added corroboration is a MINOR bump per `PATTERN_REVIEW_PROCESS.md`, since no Layout/Composition/Passability/Event Rule text itself needs to change - the new evidence confirms the existing rules rather than altering them); update `last_reviewed`.
- Update the `Confidence` body section to state the second corroborating source and reference this review as the evidence trail.
- Update the `Common Mistakes` entry that currently warns against treating the pattern's "Medium confidence as High... it has one corroborating source, not two" - this specific warning becomes stale the moment promotion is applied and should be removed or rewritten.

## Recommendations for Future Work

- A future revision of `shop.pattern.md` (independent of the confidence promotion above) should consider narrowing its wall-anchoring Layout Rule and Common Mistake to state explicitly that it applies to display/storage furniture, given `bar.pattern.md`'s direct counterexample. This review flags it; it does not apply the edit, since `shop.pattern.md` is out of this work order's scope.
- `weapon-shop.pattern.md` and `armor-shop.pattern.md` remain the corpus's weakest-evidenced patterns, both tracing to zones of one shared map. If a future extraction ever finds a dedicated, standalone weapon-only or armor-only official sample map, re-run this comparison to determine whether either pattern can be promoted independently of the other.
- `chief-house.pattern.md` would benefit from a genuinely independent second notable's-residence sample, should one become available, to move past its same-building-two-floor Medium caveat.
- No other category (exteriors, dungeons, towns, transitions) has been analyzed under this work order. The Design Pattern Library's directory structure (`studio/design-patterns/README.md`) already anticipates these as future categories.

## Constraints Observed

- Documentation only. No code was written or modified.
- `TheLastSwordProtocol-Atlas` was not read or modified.
- `TheLastSwordProtocol-Game` was read-only (map JSON and tileset data inspected; nothing written).
- No implementation contract under `reports/implementation-contracts/` was read, referenced as a build target, or modified - this review produces no implementation guidance for `The Last Sword Protocol`, per the work order's explicit instruction.
- `shop.pattern.md` was reviewed and compared but not edited, per the reasoning in the Confidence Review section above.
- The Immutable Formatting Rule (`studio/immutable-formatting-rule.md`) was preserved: this is a new report; no existing file was reformatted.
