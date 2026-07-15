# Dragon Quest Town Grammar 001 — What Makes a Town Read as Dragon Quest

## Purpose

Chris's stated bar is specific and stricter than "generic classic JRPG": *"these can not pass unless a human would instantly think Dragon Quest or Final Fantasy when seeing these maps."* `comparative-jrpg-corpus-001.md` (this Academy's first comparative study) is real and useful, but it draws its town examples from Final Fantasy (NES), Final Fantasy IV, EarthBound, and Secret of Mana (all SNES) — **it contains zero Dragon Quest references**, despite Dragon Quest being named repeatedly as the target (`WO-0047`'s human playtest feedback, and this request). `references/classic-jrpg-maps/catalog.json` had the same gap. This study closes it directly: a focused visual study of four original Dragon Warrior (Dragon Quest I, NES, 1986/1989 English localization) settlement maps, chosen specifically because `WO-0064`'s independent review of `WO-0063`'s generated settlement found it reading as a generic road-and-building diagram with no specific game's fingerprint — this study asks what fingerprint was actually missing.

## Evidence Basis

Direct visual inspection on 2026-07-13 of four labeled composite maps (background plus sprite/NPC overlay, with in-game shop price-list annotations added by the map's original cataloger, Chiasm/2006):

- `REF-NES-DW-BRECCONARY-001` — Dragon Warrior, Brecconary (starting town)
- `REF-NES-DW-CANTLIN-001` — Dragon Warrior, Cantlin (large desert city)
- `REF-NES-DW-RIMULDAR-001` — Dragon Warrior, Rimuldar (large water-moated city)
- `REF-NES-DW-TANTEGEL-001` — Dragon Warrior, Tantegel Castle

Images were inspected transiently from their cited URLs (downloaded to a local scratch directory for viewing, then deleted — never added to this repository), identical in discipline to `comparative-jrpg-corpus-001.md`'s own methodology. No asset was copied into the project. The price-list and item-name overlays visible in these particular composite images are the cataloger's own added annotations, not necessarily literal always-on-screen game UI — noted so this study's claims stay to visible game-space composition, not misread annotation as gameplay.

## 1. The Finding That Explains the Complaint

**Every single one of the four maps is fully enclosed by a continuous built or natural perimeter** — a brick/stone wall ring (Brecconary, Cantlin, Tantegel) or a water moat (Rimuldar, and a secondary moat inside Tantegel's own grounds). There is no example of a Dragon Quest settlement sitting in open, unbounded field the way `WO-0063`'s generated candidate does (a flat 40x30 grass rectangle with buildings and a road, no boundary at all). This is the single most load-bearing, most mechanically simple difference between "reads as Dragon Quest" and "reads as a road diagram," and it is exactly the gap `WO-0064`'s F4-F6 findings pointed at without yet naming the fix this specifically.

## 2. Town Grammar (Dragon Quest-Specific)

- [Observed Fact] All four maps use a **closed perimeter** (wall or water) with a small number of controlled openings (gates, bridges, path breaks) rather than an open edge the player can wander off in any direction. Brecconary's wall has a stepped, irregular outline (not a clean rectangle) with small walled sub-areas (a "Fairy Water" alcove, a small southern building) bumping outward from the main block.
- [Observed Fact] **Paths inside the wall are organic dirt/brick corridors that branch and vary in width**, shaped by building placement, not a single uniform paved geometric cross. No map shows one continuous straight spine road; all show multiple branching corridor segments of different lengths meeting at irregular junctions.
- [Observed Fact] **Buildings vary substantially in footprint, not just signage.** Within one town, structures range from small single-room houses to larger multi-room shops/inns to distinct special buildings (temple/"Curse Lifter", stone-walled compounds). No town reuses one building shell three times with only a sign swapped.
- [Observed Fact] **Trees and terrain texture cluster densely at wall interiors, path edges, and courtyard breaks** — Brecconary's walls are lined almost solid with pine trees; Tantegel's brick maze breaks for small grass-and-tree pockets and pools of water inside the castle grounds itself. Decoration is not spread thin and uniform; it concentrates at boundaries and breathing-room pockets.
- [Observed Fact] **Regional/material contrast is strong and instant between towns.** Brecconary is green-grass-and-timber. Cantlin is almost entirely brick/stone with no grass visible inside its walls at all — a genuinely different building material for a genuinely different place, not a re-tinted ground texture under the same buildings. Rimuldar is defined by its encircling moat. Each town is identifiable from its material alone, before any label is read.
- [Observed Fact] **Reward/treasure objects cluster in dedicated pockets**, not as single isolated markers. Tantegel Castle has a small room containing many visible treasure chests together ("6-18 GP Each") — a concentrated reward cluster, not one lone unstyled marker in an empty field the way `WO-0063`'s curiosity-garden anchor renders.
- [Observed Fact] **NPCs are distributed throughout the walked space at moderate, consistent density** — townsfolk and guards appear along corridors and inside building footprints, not only clustered at entrances.
- [Inference] A Dragon Quest settlement's identity comes first from **being a defended, bounded place** (wall or water reads as "settlement" before any building is even parsed), second from **material identity** (what it's built from), and only third from labeled buildings. `WO-0063`'s candidate supplies the third without the first two, which is consistent with it reading as "a diagram of a town" rather than "a town."

## 3. Direct Comparison to `WO-0063`'s Generated Settlement

| Dragon Quest town grammar (this study) | `WO-0063` generated settlement (per `WO-0064`'s review) |
|---|---|
| Closed perimeter (wall or moat), always | No boundary at all — open flat field |
| Organic branching dirt/brick paths | One uniform grey paved cross-road |
| Building footprints vary per structure | One repeated building shell, differentiated only by sign (House has none) |
| Dense tree/terrain clustering at walls and pockets | Four corner trees only, otherwise empty |
| Strong per-town material identity | Ground-color-only distinction between temperate/coastal |
| Treasure clusters (multiple chests together) | One bare, unstyled event-marker for the "curiosity hook" |
| NPCs distributed through the space | None present in the reviewed candidates |

This table is the direct input to the settlement archetype remediation this finding motivates.

## 4. What This Study Does Not Cover

- **Building interiors.** These composite overworld-style maps do not show separate interior floor plans (Dragon Warrior's original engine reveals a small interior room only once the player steps inside the same map cell; composite mappers generally do not capture that as a separate view). This study makes no claim about Dragon Quest interior room layout and does not supersede `PAT-INTERIOR-SHOP`/`PAT-INTERIOR-INN`/`PAT-INTERIOR-HOUSE` (still grounded in the RPG Maker MZ official sample project, the best available room-scale reference).
- **Searchable pot/drawer object density.** The "DQ towns are full of things to find" convention Chris raised in `WO-0047`'s playtest feedback is real, but is more associated with later Dragon Quest entries (SNES-and-later titles and remakes) than this original 1986 NES title, which predates that convention. Not contradicted by this study, just not evidenced by it — worth a follow-up study against a later Dragon Quest title if that specific density convention needs its own citation.
- This study used 4 of a possible many Dragon Warrior I locations; corroboration from a second Dragon Quest title (II or III, also NES) would raise confidence from the single-title level this study currently supports.

## 4a. Addendum (2026-07-14): Village 1, Coneria Refresh, and Dragon Quest II Towns

Chris asked directly for a comparison against `Map017` ("Village 1," this
project's own accepted human-authored map) and against more Dragon Quest
towns (Kol; and Hamlin/Leftwyne, two separate Dragon Quest II towns). New
evidence, same transient-view/no-asset-copy discipline as above:

- `Map017` (rendered directly from this project, no fetch needed): **no literal wall** — a river plus dense tree-line forms a soft boundary instead. This is an important correction to §1 above: enclosure does not have to mean a *built* wall or moat; a strong natural edge (water + tree density) is an equally valid closed-perimeter reading. §5 item 1 is revised accordingly. `Map017` also shows genuinely curved branching paths (stronger than "branches at right angles"), 5-6 buildings of visibly different massing (not just size), and a much larger scattered prop vocabulary (farm plot, individually placed barrels, ivy, stumps, lily pads) than any single Dragon Quest reference viewed so far.
- `REF-NES-FF-CONERIA-001` (Coneria, re-viewed fresh rather than relying on old notes): reconfirms the wall-perimeter finding from an independent series. Also shows that **icon-differentiated, structurally uniform buildings** (same rectangular shell, different roof-top icon) is itself a legitimate, separately-attested pattern — not a shortcut for skipping real footprint variety, but a real alternative to it. Coneria also uses an internal water channel as a *divider requiring a bridge crossing*, not only a boundary.
- `REF-NES-DW-KOL-001` (Kol, new): the town's open plaza is an **organically rounded clearing**, not a paved rectangle.
- `REF-NES-DW2-HAMLIN-001` (Hamlin, Dragon Quest II, new): the dominant landmark is a **circular pond with a small tree-ringed island**, not a well — water functions as a landmark in its own right, not only as a boundary. Interior paths read as warm brick/dirt-toned rather than grey stone. Trees are scattered **densely throughout the walkable interior**, not concentrated only at a boundary ring — this independently corroborates the same finding from `Map017`, raising it from a single-source observation to a corroborated one.
- `REF-NES-DW2-LEFTWYNE-001` (Leftwyne, Dragon Quest II, new): a small central pond at the main crossroads (water-as-landmark again, a second corroboration), and a **row of small uniform building stalls** — a market-row arrangement not seen in the Dragon Quest I towns.

This addendum also **raises this study's own confidence**: the interior-decoration-density finding is now corroborated by two independent sources (`Map017`, an RPG Maker MZ sample map, and Hamlin, a Dragon Quest II NES town), and the perimeter-framing finding now holds across two Dragon Quest titles (I and II) plus an independent NES JRPG (Final Fantasy). See Confidence and Boundary below.

## 5. Academy Application

Any future settlement/town archetype claiming a Dragon Quest-recognizable target should be checked against:

1. Is the settlement fully enclosed by a wall, moat, dense tree-line, or equally strong readable boundary (built or natural) — not an open field?
2. Do paths branch organically (curving, not just right-angled) around buildings rather than forming one uniform geometric spine?
3. Do building footprints actually differ from each other in massing, or are they uniform-but-icon-differentiated (both are legitimate; an undifferentiated repeated shell with no icon is not)?
4. Does decoration scatter throughout the walkable interior as well as concentrate at walls/path edges/courtyard pockets — not just a thin ring at the boundary?
5. Does the settlement have its own distinct build material/palette identity, not just a re-tinted ground?
6. Are reward/curiosity objects presented as a dressed cluster, not a bare unstyled marker?
7. Is the plaza/open square organically shaped, or at least not a hard, obviously-rectangular paved box?
8. Does at least one landmark use water (pond, fountain) as well as, or instead of, a well or statue?

If a generated settlement cannot answer these against a real render, it has not demonstrated the Dragon Quest target specifically, even if it passes the more general classic-JRPG Review Gate in `classic-jrpg-feel.md`.

## Confidence and Boundary

Originally a single-title (Dragon Warrior I), four-location finding. The
2026-07-14 addendum adds a second Dragon Quest title (Dragon Quest II: Hamlin,
Leftwyne), a fresh independent-series re-check (Coneria, Final Fantasy), and
this project's own accepted human-authored map (`Map017`) — six additional
locations across three sources. Two findings (interior decoration density,
water-as-landmark) are now corroborated by more than one independent source
and should be treated with correspondingly higher confidence than the rest
of this document, which remains `low` per this Academy's existing confidence
model. Still not sufficient to claim exhaustive "Dragon Quest series"
authority (three titles/sources total, not a systematic survey). Does not
override Atlas canon, Creative Authority, accepted RPG Maker patterns,
collision validation, or playtest evidence. Establishes a creative north star
and a specific, falsifiable checklist — not permission to reproduce any
source layout or asset.
