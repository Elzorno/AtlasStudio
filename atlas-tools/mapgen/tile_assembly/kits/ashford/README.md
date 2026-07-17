# Ashford TileAssembly Reference Kit

This adapter-owned WO-0070 kit contains complete, source-pinned assemblies
extracted read-only from the accepted RPG Maker MZ Village 1 reference,
`TheLastSwordProtocol-Game/data/Map017.json` (tileset 2, `Outside`). It does not
authorize writing Map001 or copying Map017's layout.

Run from the AtlasStudio repository root:

```sh
PYTHONPATH=atlas-tools/mapgen python3 \
  atlas-tools/mapgen/tile_assembly/kits/ashford/generate_kit.py
```

The generator records exact source coordinates; canonical extracted-region,
map, selected-tileset-entry, and individual tileset-image hashes; collision
masks derived from source tileset flags; complete event-graphic overlays for
doors; isolated previews; two-placement fixtures; and a kit contact sheet.

## Verified contents

- one complete 2x2 broadleaf tree assembly;
- two low cottage variations and one compact timber house, each with its
  source `!Door1` overlay;
- one broad paired-service frontage and one broad Inn exterior;
- Shop and Inn functional frontage clusters;
- a farm-and-fence cluster;
- open-well plaza context;
- bridge-and-banks composition reference;
- complete window and Shop-sign components.

The bridge record is intentionally named `REFERENCE`: it can teach crossing
composition but cannot establish Ashford's maintenance-drainage design.

## Explicit gaps

The accepted source corpus does not safely prove these Ashford-specific
assemblies, so this kit does not invent them:

- a roofed well (Map017 contains a single-tile open well);
- old-maintenance drainage;
- warm-stone vent or humming panel;
- patched-metal Ashford fencing;
- the selected concept set's exact dark-slate timber building family.

Those remain blocked until a matching RPG Maker MZ source/contact-sheet region
is verified or Chris approves a separately authored adapter assembly. Concept
art cannot fill these raw-tile gaps.

## Authority

Raw tile IDs, event graphics, collision masks, hashes, and serialization belong
to AtlasStudio's RPG Maker adapter boundary and ultimately to `rpgmakerLSP` at
write time. Atlas canon contains only abstract intent and references, never
these bindings.
