# Ashford Authored Candidate Pack

This directory contains adapter-authored, non-production RPG Maker MZ source
material. It is **not reference-extracted evidence**. Every assembly and the kit
index remain disabled with `human_approval_required` until Chris reviews the
generated previews.

`generate_authored_kit.py` deterministically creates an MZ-compatible source
fixture using tileset 2 (`Outside`), extracts each candidate through the generic
TileAssembly adapter, renders isolated and composition previews, projects the
contract records, and builds the contact sheet and index.

Map017 is read-only input. Its verified compact-building columns, complete door
event, open-well component, and bridge/bank components inform the authored
combinations where practical. They do not make those combinations
reference-extracted.

## Outside vocabulary limitations

- There is no verified roofed-well object. The candidate combines a canopy,
  posts, and the verified complete well component.
- There is no verified maintenance-drain object. The candidate broadens the
  bridge/bank vocabulary into a reviewable crossing proxy.
- There are no verified Ashford warm-vent or humming-panel graphics. The
  candidates use visibly mechanical Outside objects as review-only proxies.
- There is no verified patched-metal fence set. The candidate combines Outside
  metal and timber barrier pieces as a silhouette proxy.

These limitations are machine-readable on the affected entries in `index.json`.

## Initial fidelity result

The first proxy pass was rejected internally for black facade voids and literal
machinery. The corrected pass is fully recorded in
`AUTHORED-PACK-FIDELITY-REVIEW.md` and remains disabled:

- Warm-Stone Vent: suitable for Chris's selection.
- Four buildings, Humming Panel, and Patched-Metal Fence: revision required.
- Roofed Well and Maintenance Drainage: impossible with the current default
  `Outside` vocabulary.

## Human review and requested revision

Chris reviewed the corrected contact sheet on 2026-07-15. He approved the four
building directions, requested two wall rows on some buildings, rejected the
Roofed Well, Humming Panel, and Patched-Metal Fence, and corrected the purported
drainage object to a natural Bridge. The Warm-Stone Vent is recorded as
approved after no further objection to its selection recommendation.

The regenerated pack gives Shop and Inn two wall rows while Elara House and
Elder House keep one. The index enables only those four buildings and the vent.
The rejected objects and Bridge remain disabled. Custom source art is still
required for the roofed well, maintenance drainage, panel, and fence.
