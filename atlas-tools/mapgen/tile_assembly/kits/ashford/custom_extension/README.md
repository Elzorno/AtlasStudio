# Ashford Custom Tileset Extension

This human-gated adapter asset pack supplies the four visual concepts that the
default RPG Maker MZ Outside vocabulary could not represent faithfully:

- roofed civic well;
- old-facility maintenance drainage outlet;
- humming utility panel; and
- patched metal fence.

`Ashford_Custom_B.png` is a 16 by 16 RPG Maker B-sheet at 48 pixels per tile.
Nothing in this extension is enabled for compilation or production placement
until Chris approves the rendered review sheet. Chris approved the Panel and
Fence after the first scale pass, then approved the Well and Drainage after
their 2x2 revision. All four bindings and the extension are now human-approved.
The production Game repository is not modified by this pack.

The generated master artwork is preserved unchanged. Version 2 changes only
the deterministic grid binding: Well and Drainage are 2x2, Panel is 1x2, and
Fence is a 6x2 modular run with a roughly 1.4-tile visible height. The scale
context preview places them on one continuous 48-pixel grid beside the approved
Elara House, approved vent, and a one-tile actor sprite.

The source was produced with OpenAI's built-in image-generation tool using the
approved Ashford authored contact sheet as a style-and-scale reference, then
chroma-keyed, cropped, and aligned to the 48-pixel grid by
`build_extension.py`. The unmodified chroma source, alpha-converted source,
hashes, crop bindings, and review state are retained for provenance.
