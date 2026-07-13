# Comparative JRPG Corpus 001 - The Immediate Classic-JRPG Read

## Purpose

This is a direct visual study of nine maps selected from `references/classic-jrpg-maps/catalog.json`. The Production Director identified this era and corpus as foundational inspiration for The Last Sword Protocol and wants the game to feel immediately like an old JRPG.

The study asks a player-facing question: **what does the player see, understand, and feel in the first seconds of entering these spaces?** It does not copy geometry, tiles, story content, or names. It does not infer hidden implementation details from composite images.

## Evidence Basis

Direct visual inspection on 2026-07-12 of:

- `REF-NES-ZELDA-HYRULE-001` - The Legend of Zelda, First Quest Hyrule
- `REF-NES-FF-CONERIA-001` - Final Fantasy, Coneria
- `REF-NES-FF-MARSH-001` - Final Fantasy, Marsh Cave
- `REF-SNES-FFIV-OVERWORLD-001` - Final Fantasy II/IV, Overworld
- `REF-SNES-FFIV-BARON-001` - Final Fantasy II/IV, Town of Baron
- `REF-SNES-CHRONO-GUARDIA-001` - Chrono Trigger, Guardia Castle
- `REF-SNES-EARTHBOUND-ONETT-001` - EarthBound, Onett
- `REF-SNES-MANA-PANDORA-001` - Secret of Mana, Pandora's Ruins
- `REF-SNES-SMRPG-KERO-001` - Super Mario RPG, Kero Sewers

Images were inspected from their cited external URLs. No image was added to the repository. Composite-map borders, labels, item markers, and disconnected room placement may have been added by the mapper; claims below concern visible game-space composition only.

## 1. Immediate Read

- [Observed Fact] Every studied local map separates traversable space from non-traversable space with strong visual contrast: walls, water, cliffs, trees, void, or constructed edges.
- [Observed Fact] Each town or major interior gives at least one structure disproportionate visual importance: Coneria's central stone plaza, Baron's water-and-building axis, Onett's civic street grid and town hall, Guardia Castle's throne approach, Pandora's central ritual hall.
- [Observed Fact] The overworlds use a small terrain vocabulary in large contiguous regions rather than distributing every terrain type evenly.
- [Inference] The old-JRPG read begins with legibility, not pixel art alone. The player sees a small number of strong nouns - town, road, forest, mountain, throne, sewer channel - before seeing decorative detail.

## 2. Overworld Grammar

- [Observed Fact] Zelda's Hyrule is divided into screen-like terrain cells and corridors, with mountains, water, forests, and graveyard fields forming recognizable regional identities.
- [Observed Fact] Final Fantasy II/IV's overworld uses mountain chains, coastlines, rivers, islands, and large biome fields to separate travel regions; settlements and caves are visually tiny but high-contrast destinations.
- [Observed Fact] Both overworlds contain substantial open travel area, but the open area is bounded and shaped by readable macro-barriers.
- [Inference] A classic overworld should make the next destination understandable while preserving uncertainty about the route, encounter pressure, and what lies beyond the next geographic gate.
- [Inference] Regional identity should come from one dominant landform plus one destination or landmark, not from uniform decorative density.

## 3. Town Grammar

- [Observed Fact] Coneria is compact and nearly symmetrical around a central paved plaza; services sit a short walk from the center, and water divides the settlement without obscuring the main axis.
- [Observed Fact] Town of Baron places a broad north-south route through an asymmetric cluster of buildings, with water and elevation creating small route decisions around a clearly readable civic core.
- [Observed Fact] Onett is larger and less compact, but its pale road grid creates a dominant circulation system, while the town hall, arcade, hospital, houses, cliffs, and forest form visually distinct districts.
- [Observed Fact] In all three, buildings face or closely relate to an obvious path. Large natural borders frame the town and prevent the traversable area from reading as an editor rectangle.
- [Inference] A town feels classically JRPG-like when the player can quickly answer: where is the center, what is important, where do roads go, and which edge leads back to danger?
- [Inference] Service convenience and world fiction coexist: services are clustered for the player, while water, walls, yards, trees, and elevation make the settlement feel inhabited.

## 4. Dungeon Grammar

- [Observed Fact] Marsh Cave alternates irregular passages with rectangular rooms and uses disconnected floors or sections. Treasure rooms and dead ends make route choice visible in the composite.
- [Observed Fact] Guardia Castle alternates narrow connectors with larger ceremonial rooms. Repeated stone-and-carpet language unifies the complex, while throne rooms, stairs, dining spaces, and bedrooms remain distinct.
- [Observed Fact] Pandora's Ruins uses a central axial hall as a dominant landmark, then shifts into narrower turning corridors and smaller chambers before returning to strongly staged rooms.
- [Observed Fact] Kero Sewers uses room-scale modules connected through pipes, doors, water channels, and vertical changes; individual rooms often contain a single memorable interaction or traversal idea.
- [Inference] Classic dungeons are remembered as sequences of room ideas, not as a continuous undifferentiated floor mask.
- [Inference] Compression and release are essential: corridor, chamber, decision, reward or threat, then connector. A dungeon made only of corridors feels procedural; a dungeon made only of open chambers lacks tension.

## 5. Landmark and Hierarchy Findings

- [Observed Fact] Landmarks are frequently functional: plaza, bridge, fountain, throne, staircase, pipe, water channel, large civic building, or ritual dais.
- [Observed Fact] Major landmarks often align with an approach path and occupy more space, stronger contrast, or a more symmetrical composition than ordinary surroundings.
- [Inference] A player should encounter one dominant visual statement before being asked to interpret smaller details.
- [Inference] Decorative landmarks are weaker than functional landmarks when they do not change navigation, interaction, anticipation, or story meaning.

## 6. Density and Negative Space

- [Observed Fact] NES maps use sparse tile vocabularies and repeated patterns, yet preserve strong region and room identity through silhouette and placement.
- [Observed Fact] SNES maps add texture, elevation, props, and palette variation without surrendering the primary route silhouette.
- [Observed Fact] Open floor concentrates on travel axes, plazas, ceremonial approaches, and encounter rooms; detail more often gathers at edges, around structures, or in localized clusters.
- [Inference] The target is not maximum detail. The target is selective richness around a route the player can read immediately.
- [Inference] Empty space earns its place when it stages a landmark, enables movement, creates threat exposure, or provides relief after compression.

## 7. What Creates the Old-JRPG Feeling

The corpus supports the following synthesis as an Atlas interpretation:

1. **Readable nouns first.** The screen should immediately communicate what kind of place this is.
2. **One dominant landmark.** Every important map or major sub-area needs a memorable anchor.
3. **Compact purpose.** Travel between meaningful decisions should be short unless danger or anticipation makes the distance meaningful.
4. **Strong edges.** Water, cliffs, walls, forests, counters, and elevation should make route boundaries visually obvious.
5. **Small choices.** The main path stays legible while side routes offer treasure, character, risk, or shortcuts.
6. **Compression and release.** Narrow connectors alternate with rooms, plazas, vistas, or arenas.
7. **Functional decoration.** Props and terrain cluster around use, ownership, story, or navigation.
8. **Regional contrast.** A small vocabulary used consistently creates stronger identity than using every available tile.
9. **Visible destination logic.** Important buildings, doors, stairs, and landmarks relate to the path that serves them.
10. **Restraint.** Pixel-era character comes from clear abstraction and authored selection, not from simulated age, noise filters, or excessive clutter.

## 8. Anti-Patterns for The Last Sword Protocol

- Large rectangular maps whose outer dimensions are more apparent than their in-world boundaries.
- Long traversal with no landmark, decision, encounter pressure, or changing view.
- Uniform decoration spread that weakens focal points.
- Buildings or doors unrelated to roads and circulation.
- Dungeons built from one repeated corridor width and interchangeable rooms.
- Every biome or terrain type appearing in one local area.
- Secrets with no visual suspicion cue.
- Modern spaciousness that leaves services and story nodes far apart without experiential purpose.
- Pixel-art styling used to disguise weak hierarchy or route composition.

## 9. Academy Application

Every future map review that claims a classic-JRPG target should answer:

1. What does the player understand in the first three seconds?
2. What is the dominant landmark?
3. Where is the main route, and what makes it visually legible?
4. What is the first meaningful choice or curiosity hook?
5. Where does the map compress, and where does it release?
6. Which empty spaces have a player-facing job?
7. Which region or room has a distinct identity, and what limited vocabulary creates it?
8. What would the player remember well enough to describe after leaving?

If a review cannot answer these from a render or playtest, the map has not yet demonstrated the requested classic-JRPG feel.

## Confidence and Boundary

These are comparative player-experience findings from released-game composite maps. They have `low` confidence for implementation details and may influence implementation contracts only as comparative context. They do not override Atlas canon, Creative Authority, accepted RPG Maker patterns, collision validation, or playtest evidence.

This corpus establishes a creative north star, not permission to reproduce any source layout or asset.
