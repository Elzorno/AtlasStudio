# Ashford Separately Authored Assembly-Pack Brief

Status: Authorized direction; pack not yet authored or approved  
Authority: `MV-HOM-ASH-001@0.1`, `AVCP-HOM-ASH-001`, selected
`ATLAS-CON-ASH-001@0.2:v2` concept set  
Scope: RPG Maker MZ adapter assemblies only; no map, event, or canon writes

## Purpose and authority boundary

Chris approved a separately authored RPG Maker MZ assembly pack to close the
gaps the accepted Map017 reference cannot safely supply. The pack must realize
the approved Ashford visual direction without pretending concept art proves
tile identity, dimensions, collision, passability, topology, or events.

Requirement labels:

- **Canon:** mandatory MapVision fact or exclusion.
- **Approved operational constraint:** approved AVCP measurement used as a
  falsifiable implementation gate.
- **Provisional design:** selected v2 interpretation that Chris may revise;
  it cannot override canon or runtime safety.

Every authored assembly remains adapter-owned and must receive isolated,
fixture, and in-context human review before reuse. This brief contains no raw
tile IDs.

## Shared building-family subassemblies

These complete components are required before the four role buildings can be
declared reusable:

| Assembly | Authority | Required content | Falsifiable acceptance |
|---|---|---|---|
| Dark roof straight run | Provisional design | Complete left edge, interior run, right edge, ridge/eave relationship, and supported repeat rule | Isolated preview has no cropped edges or missing caps; two widths render without a seam or repeated broken end. |
| Dark roof corner/offset set | Provisional design | All corners and junctions needed for one modest offset or attached volume | Every advertised junction renders closed in a fixture; unsupported junctions are explicitly rejected rather than improvised. |
| Timber/plaster facade run | **Canon** | Timber-dominant wall with restrained pale infill, stone base, complete left/right ends, and no pure-white-plaster variant | Timber is the largest visible facade share; both ends and base terminate cleanly; no clean-metal or white-plaster-dominant result exists. |
| Low entrance bay | **Canon** | Complete entrance surround, visible closed-door overlay, threshold, and path connector | Door is visible in isolation and fixture; connector meets its threshold; facade body from threshold to eave is no more than two map-grid rows. |
| Window bay | Provisional design | Complete timber-framed window compatible with the facade family | Host fixture shows no broken wall edge or floating window; window remains subordinate to entrance. |
| Stone base/end set | **Canon** | Complete base run, left/right endings, and required corners | No base terminates mid-pattern in any approved building width. |
| Repaired-metal accent set | **Canon** | Closed weathered plates, brackets, fittings, and small repair patches | Every piece reads as closed ordinary salvage; zero exposed circuitry, active blue light, modern chain-link, or clean industrial casing. |
| Porch/awning set | Provisional design | Complete posts, roof/awning edge, deck/step, left/right ends, and facade attachment | Both Shop and Inn fixtures attach without floating posts, cropped canopy, or blocked-looking doorway. |
| Chimney/vent cap set | Provisional design | Complete static roof attachment where used | Attachment includes base and cap; no smoke animation or new local system is implied. |

## Role-building inventory

### Elara House

**Authority:** Canon role and material family; provisional silhouette treatment.

Required assembly:

- One complete low domestic building.
- Medium-small footprint relative to Inn and Shop.
- Dark low roof, timber-first facade, restrained plaster, stone base, visible
  entrance, garden-side attachment point, and one or two repaired-metal
  domestic fittings.
- No service sign, public porch, second storey, or monumental frontage.

Acceptance:

1. Total threshold-to-ridge height is no more than five map-grid rows and the
   wall body is no more than two rows (`ASH-BUILD-001`).
2. A blind reviewer identifies it as a home rather than Shop, Inn, or hall.
3. Its silhouette differs from each other canonical building in at least two
   of frontage width, roof outline, porch/yard treatment, or entrance treatment
   (`ASH-BUILD-003`).
4. Timber is the largest facade share and old metal is a subordinate repair
   accent (`ASH-MATERIAL-001/002`).

### Ashford Shop

**Authority:** Canon Shop role and no-new-service exclusions; provisional porch
and supply presentation.

Required assembly:

- One complete single-service Shop building, not a paired Shop/Tavern.
- Low wide frontage with complete Shop sign, door, porch or awning, and
  attachment points for barrels, crates, and sacks.
- Optional small repair shelter may read as ordinary tool storage only.

Acceptance:

1. One and only one service identity is visible; no tavern, blacksmith, forge,
   hammer, weapon service, or second shop is implied.
2. Building meets the five-row total and two-row facade-body limits.
3. At least three related supply props form a functional frontage cluster
   without obscuring the entrance (`ASH-PROP-001`).
4. Roof, porch, facade, sign, door, and base all terminate completely in the
   isolated preview; no tree or unrelated source context is baked in.
5. A blind reviewer distinguishes it from Elara House, Inn, and Elder House
   without metadata.

### Ashford Inn

**Authority:** Canon role, largest-public-building relationship, and Elara-role
boundary; approved AVCP proportions; provisional hospitality dressing.

Required assembly:

- One complete low broad Inn building.
- Broadest public facade, distinct sign and entrance, shallow hospitality
  porch, and attachment points for benches, barrels, or hitching rail.
- Prominence comes from breadth and frontage, never an extra storey or tower.

Acceptance:

1. Visible width-to-total-height ratio is at least 1.6 and no other public
   building is wider (`ASH-BUILD-002`).
2. Total height is no more than five rows and facade body no more than two.
3. Isolated and fixture previews show the complete outer silhouette with no
   cropped annex, tree overlap, or unrelated neighboring building.
4. A blind reviewer identifies hospitality before residence or shop, while
   still reading the building as modest village-scale rather than luxury or
   civic monument.
5. No paid-service implication, new economy, or competition with Elara's
   emotional-home role is introduced.

### Ashford Elder House

**Authority:** Canon enterable residence/council role from `ATLAS-DDR-0007`;
provisional gathering-house frontage.

Required assembly:

- One complete low, grounded elder residence.
- Slightly broader gathering frontage than Elara House, visible unique door,
  modest bench or meeting threshold, and the shared Ashford material family.
- No palace, church, guild, faction, ceremonial, or quest-hub imagery.

Acceptance:

1. Meets the five-row/two-row proportion limits.
2. A blind reviewer reads a modest residence or village meeting house, not a
   service building or seat of power.
3. Differs pairwise from the other three role buildings in at least two
   silhouette attributes.
4. Contains no invented elder name, symbol, faction, quest marker, or event
   behavior.

## Landmark and infrastructure inventory

### Roofed civic well

**Authority:** Canon dominant civic landmark; provisional roof silhouette.

Required assembly:

- Complete well basin, posts/supports, roof, cap/ridge, bucket or winding
  detail if used, collision footprint, and surrounding approach connector.

Acceptance:

1. Isolated preview contains every support, roof edge, base, and cap; no open
   Map017 well substitution.
2. In a neutral plaza fixture, at least two of three blind reviewers rank it
   as the primary landmark without labels (`ASH-LANDMARK-001`).
3. It reads as ordinary stone-and-timber civic infrastructure, not magic,
   shrine, machinery, or decorative gazebo.

### Old-maintenance drainage

**Authority:** Canon allows only subordinate facility drainage and forbids a
dominant natural river; provisional exact visual form.

Required assemblies:

- Straight channel, supported bend, source/outlet termination, bank/ground
  transition, and one complete small crossing if the authored MapPlan requires
  it.

Acceptance:

1. Every advertised segment joins without broken water/edge transitions.
2. Channel remains narrow and subordinate in an Ashford fixture; it does not
   split the settlement, dominate the first camera, or erase any route mouth.
3. At least two of three reviewers identify it as old drainage or ambiguous
   infrastructure rather than a natural river.
4. Map017's natural bridge/banks record is not used as proof or wholesale
   substitution.

### Warm-stone vent

**Authority:** Canon landmark and hidden-item relationship; provisional surface
design.

Required assembly:

- Complete grounded vent body, stone surround, closed weathered fitting,
  collision footprint, and attachment context for a cultivated patch.

Acceptance:

1. Reads as warm ordinary agricultural utility before technology.
2. Contains no exposed electronics, active blue light, clean machinery, smoke
   system, or new animation/event behavior.
3. Complete base/cap is visible; it cannot be mistaken for a cropped pipe.
4. Fixture leaves a visually unambiguous straight clue line for the canonical
   hidden-item relationship; exact map coordinates remain MapPlan authority.

### Humming panel

**Authority:** Canon child-play landmark; provisional panel design.

Required assembly:

- Complete closed panel face, frame, base or wall attachment, weathered repair
  state, and interaction-side marker for downstream use.

Acceptance:

1. Closed and ambiguous: zero visible circuit board, readable modern controls,
   active blue display, or pristine science-fiction surface.
2. Reads as an old metal wall/panel children might treat as ordinary village
   texture.
3. Complete attachment prevents floating or floor-placed wall art.
4. Visual assembly contains no dialogue, switch, sound, or event command.

### Patched-metal fence family

**Authority:** Canon material language and old-world-restraint exclusions;
provisional patch arrangement.

Required assemblies:

- Straight run, end caps, inside/outside corners, gate/opening transition, and
  supported timber/stone-to-metal repair junction.

Acceptance:

1. Every supported run and junction terminates cleanly in an isolated fixture.
2. Metal appears weathered, closed, irregular, and repaired into timber or
   stone; no chain-link, razor wire, powered gate, or continuous industrial
   perimeter.
3. At least one timber-led and one stone-led fixture preserve metal as a
   subordinate accent.
4. Unsupported fence shapes fail closed rather than filling with guessed
   pieces.

## Required functional prop subassemblies

These may reuse already verified atomic components where compatible, but each
new multi-part cluster must remain decomposable and complete:

| Cluster | Minimum authored components | Acceptance |
|---|---|---|
| Elara domestic garden | Low garden boundary, crop/flower patch, firewood or laundry-scale domestic accent | Three related elements read as home use; entrance remains visually clear. |
| Shop supply frontage | Barrel, crate, sack, porch-edge attachment | At least three related items form one supply cluster; no second service is implied. |
| Inn hospitality frontage | Bench, hitching rail or barrel, porch attachment | At least three related elements read as welcome/rest, not commerce or luxury. |
| Warm-vent farming cluster | Vent, cultivated patch, stone/soil transition | All elements read as one agricultural-use story signal. |
| Humming-panel play context | Panel, safe standing/play edge, modest reused-material context | Panel remains visible and ordinary; no literal electronic workstation. |

## Pack-level acceptance

The authored pack may enter human approval only when:

1. Every advertised assembly has an isolated preview and a two-placement
   fixture preview.
2. Every multi-part object has explicit completeness evidence for edges,
   corners, base, cap, roof, and overlay components it claims to support.
3. All four role buildings pass `ASH-BUILD-001`, pairwise
   `ASH-BUILD-003`, and their role-specific tests above.
4. The Inn additionally passes `ASH-BUILD-002`.
5. Every old-world component passes `ASH-MATERIAL-002` with zero prohibited
   literal-technology cues.
6. The five functional clusters satisfy `ASH-PROP-001`.
7. Unsupported transformations and junctions fail closed.
8. Chris reviews and accepts the contact sheet; automated and agent review
   cannot approve subjective Ashford style.

Pack approval would authorize use in disposable candidates only. It would not
authorize a production Map001 write or override structural, event, ownership,
or live RPG Maker gates.
