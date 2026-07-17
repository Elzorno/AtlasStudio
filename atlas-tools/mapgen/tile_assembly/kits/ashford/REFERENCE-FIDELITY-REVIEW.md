# Ashford TileAssembly Reference-Fidelity Review

Reviewer: Claude Code  
Date: 2026-07-15  
Authority checked: approved `MV-HOM-ASH-001@0.1`, approved
`AVCP-HOM-ASH-001`, and selected Ashford v2 concept set

## Scope and verdict

This is a reference-fidelity and Ashford-fit review, not schema validation,
production approval, or permission to write a map. The contact sheet, isolated
previews, JSON coordinates, event overlays, and hashes were inspected. The
13-test TileAssembly suite passes, but that proves rectangular extraction,
provenance integrity, overlay presence, and one exact tree signature—not that
every extracted rectangle is a semantically complete or Ashford-compatible
object.

The contract/tooling is a sound provenance boundary. The current kit is a
useful reference-study kit, but it is **not yet a complete reusable Ashford
production kit**. Only the tree, window, and Shop sign are verified reusable as
presented. Most other records must be classified as study-only; two building
records and all explicitly missing Ashford-specific assemblies remain blocked.

## Per-assembly disposition

| Assembly | Disposition | Reference-fidelity finding | Ashford use |
|---|---|---|---|
| `TASM-ASHFORD-TREE-BROADLEAF-01` | **Verified reusable** | Contact sheet shows the complete canopy and trunk/base. Layer-three signature is exactly `176,177 / 184,185`; the dedicated test rejects the former half-tree failure. Hashes and coordinates match Map017. | Approved reusable tree assembly, subject to downstream placement/collision review. |
| `TASM-ASHFORD-COTTAGE-LOW-A` | **Study-only** | The full source rectangle and `!Door1` overlay are preserved, but the isolated result is a very narrow, steep brown-roof cottage. It fits the provisional height cap but does not match the selected v2 family's low broad dark-roof silhouette. | May teach complete door/roof extraction; must not define Elara House, Elder House, or the Ashford cottage family. |
| `TASM-ASHFORD-COTTAGE-LOW-B` | **Study-only** | Same complete-overlay strength and same proportion/style mismatch as Cottage A; its visible silhouette is nearly identical rather than a materially differentiated family member. | Variation study only. |
| `TASM-ASHFORD-HOUSE-COMPACT-01` | **Study-only** | Compact rectangle and door overlay are complete, but the potion/service sign makes it a role-marked service facade rather than a neutral residence. Brown roof and narrow vertical mass do not prove the selected Ashford family. | Can teach compact service-house composition; blocked as a canonical Ashford residence. |
| `TASM-ASHFORD-SHOP-TAVERN-FRONTAGE` | **Blocked for Ashford** | The rectangle begins inside a larger Map017 composition. The contact sheet contains tree crowns across its roof edge and presents two service doors/signs, including a tavern role Ashford does not authorize here. It is a frontage slice, not a complete Shop building. | Do not place as Ashford Shop or treat it as a complete building assembly. Re-extract or author a verified single-Shop assembly. |
| `TASM-ASHFORD-INN-BROAD-01` | **Blocked for Ashford** | The contact sheet shows a cropped irregular portion of Map017's larger southeast building, including tree overlap and attached roof/facade context. At seven rows high it also exceeds approved `ASH-BUILD-001`'s five-row operational cap. Door and Inn sign are preserved, but the whole is not the low broad selected v2 Inn. | Useful source study only; cannot satisfy the Ashford Inn assembly gate. |
| `TASM-ASHFORD-FARM-FENCE-CLUSTER` | **Study-only** | Source fidelity is strong, but the rectangle includes water edge and an unrelated roof fragment alongside crops, fence, scarecrow, barrel, and well. It is a contextual crop rather than one portable farm module. | Mine smaller verified crop/fence/prop subassemblies before placement. |
| `TASM-ASHFORD-WELL-OPEN-CONTEXT` | **Study-only / blocked for landmark role** | Correctly preserves Map017's open single-tile well and surrounding vegetation. It is not the selected roofed civic well. | Composition study only; cannot fill Ashford's dominant roofed-well requirement. |
| `TASM-ASHFORD-BRIDGE-BANKS-REFERENCE` | **Study-only / blocked for drainage role** | Correctly labeled as a natural river bridge reference. It proves a crossing composition, not maintenance drainage. | Never substitute it for Ashford's old-facility drainage assembly. |
| `TASM-ASHFORD-SHOP-PROP-CLUSTER` | **Study-only** | Exact Map017 frontage crop with two doors and mixed service roles. Props and signage are useful functional-cluster evidence, but the slice is coupled to the rejected paired frontage. | Extract barrels/crates/porch dressing as smaller components; do not place wholesale. |
| `TASM-ASHFORD-INN-PROP-CLUSTER` | **Study-only** | Door/sign overlay and hospitality details are preserved, but the crop remains attached to Map017's tall/cropped building and pipe context. | Hospitality frontage study only. |
| `TASM-ASHFORD-WINDOW-01` | **Verified reusable** | Atomic component is complete, source-pinned, and visually compatible with timber/plaster construction. | Reusable wall attachment after host-facade compatibility validation. |
| `TASM-ASHFORD-SIGN-SHOP-01` | **Verified reusable** | Atomic Shop role marker is complete and source-pinned. | Reusable Shop sign if Chris accepts the icon and the host facade remains Ashford-compatible. |

## Door-overlay review

The five building/frontage records correctly preserve nonblank `!Door1`
event-graphic overlays at in-bounds local coordinates with matching source
coordinates. The dedicated test verifies presence. This closes the former risk
of extracting a facade while silently losing its visible door.

Door completeness does **not** make the surrounding building complete. The
current tests do not detect that the Shop record is only a frontage slice or
that the Inn rectangle is a cropped mixed composition.

## Proportion and selected-style review

The contact sheet does not meet the approved building-family gate:

- Cottage A/B and Compact House are narrow, steep-roofed, brown timber sample
  forms rather than the selected low, broad, dark-slate Ashford family.
- Shop/Tavern is a paired frontage with extra role semantics and roof-edge tree
  overlap, not one complete Shop.
- Inn is seven rows high and visually cropped, failing the approved operational
  proportion cap and selected v2 silhouette.
- The kit contains no verified Elara House, Elder House, or complete Ashford
  Shop/Inn family that differs pairwise in the required silhouette attributes.

Map017 remains valid accepted evidence for complete-source composition. Its
style cannot be relabeled as the selected Ashford v2 style merely because the
tileset and hashes match.

## Explicit blocked gaps

The README accurately records these unsupported assemblies; inspection found
no hidden evidence that closes them:

| Required assembly | Status | Reason |
|---|---|---|
| Roofed civic well | **Blocked** | Source proves only an open single-tile well. |
| Old-maintenance drainage | **Blocked** | Natural river/bridge cannot establish factory drainage. |
| Warm-stone vent | **Blocked** | No accepted source assembly. |
| Humming panel | **Blocked** | No accepted source assembly. |
| Patched-metal Ashford fence | **Blocked** | Farm record proves timber fence only. |
| Exact dark-slate timber family | **Blocked** | Concept art supplies direction, not tile binding; current brown-roof Map017 buildings do not match it. |
| Complete Ashford Shop | **Blocked** | Current record is a paired frontage slice with an unauthorized extra service role. |
| Complete low broad Ashford Inn | **Blocked** | Current record is cropped and exceeds the approved height cap. |

## Tooling finding

Schema and semantic validation currently define “complete” as one rectangular
cell record per local coordinate plus valid overlays and hashes. That is
necessary but insufficient for semantic object completeness. Only the tree has
an object-specific signature assertion. Before buildings can be labeled
verified reusable, add evidence or tests for:

1. source bounds containing the complete intended silhouette;
2. absence of unrelated tree/building/context cells inside the object record;
3. required roof-edge, facade-edge, base, and door signatures;
4. approved proportion bands; and
5. explicit `verified_reusable`, `study_only`, or `blocked_for_target` review
   state in the kit index.

## Reviewer recommendation

Retain all records as auditable extraction evidence. Promote only Tree,
Window, and Shop Sign to reusable status. Reclassify the contextual records as
study-only, block the current Shop and Inn for Ashford, and keep every explicit
gap blocked until contact-sheet/source evidence or a separately human-approved
adapter assembly exists.

This review does not approve WO-0070 or any assembly on Chris's behalf.

## Post-review hardening

Codex implemented the recommendation after this review. `index.json` now gives
every record an explicit `review_state`, `downstream_generation_allowed`, and
reason. Only Tree, Window, and Shop Sign are enabled; all study-only and blocked
records fail closed for downstream selection. Dedicated tests assert that exact
allowlist plus the tree, window, sign, and door-overlay signatures. The focused
TileAssembly suite now contains 15 passing tests.
