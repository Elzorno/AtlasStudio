# Ashford Village Event Plan

## Purpose

This is the implementation-requirements list for every RPG Maker event Ashford Village needs, derived from `projects/the-last-sword-protocol/design/ashford-village-experience-specification.md`. It states what each event must do mechanically - trigger, placement, gating, and purpose - not what any NPC says. Dialogue authoring happens separately, against the Dialogue Goals in the specification's Section 4, once these event hooks exist.

## World-State Flag

A single game switch (name to be assigned by Codex during implementation, e.g. `sword_obtained`) gates the "after-sword" state referenced throughout this plan and the specification (`dialogue.ashford_after_sword`). This is the same world-state flag the milestone document (`projects/the-last-sword-protocol/milestones/first-playable-hour.md`, Beat 6) already establishes for unlocking Glassfield Ruins - Ashford Village's after-sword dialogue page should key off the same flag, not a second, redundant one.

**Scope clarification:** the specification's language that Rowan is "at home in the morning, found at the Village Green later in the day" describes personality texture, not a request for a full day/night cycle system. Implement Rowan's (and, if applicable, Elara's) position change using the same before/after-sword flag above (or a single lightweight one-time self-switch triggered the first time the player leaves the cottage), not a time-of-day engine. A full day/night system is out of scope for this village and should not be built here.

## Player Start

- One player start position, inside Rowan's Cottage, on a passable tile near the cottage's interior entrance/bed area, consistent with the "wake at home" opening beat (specification Section 5).
- Configured via the project's standard start-of-game handling (System.json start location or an equivalent New Game event/common event already in use elsewhere in the project) - do not invent a new starting mechanism if the project already has one.

## Transfers

Every transfer is a standard Transfer Player event command, triggered by Player Touch at a door or map-edge tile unless noted otherwise.

- Rowan's Cottage interior -> Ashford Village exterior (front door).
- Ashford Village exterior -> Rowan's Cottage interior (door tile at the cottage's placement).
- Ashford Village exterior -> General Store interior (door tile).
- General Store interior -> Ashford Village exterior (front door).
- Ashford Village exterior -> Blacksmith interior (door tile).
- Blacksmith interior -> Ashford Village exterior (front door).
- Ashford Village exterior -> Inn interior (door tile).
- Inn interior -> Ashford Village exterior (front door).
- Ashford Village exterior -> Ashford Vale Overworld (the single village exit per the map brief's Road Layout section). This transfer must remain unconditional and always available after the opening scene - no flag, item, or dialogue gate blocks it, per the specification's Player Flow and Acceptance Criteria (Section 5, Section 9).

## NPCs

Baseline for every named NPC event, per the reference sample project's convention (see `ashford-village-map-brief.md`'s Reference Study Notes): Action Button trigger, "same as characters" priority, walking animation enabled, unless a specific NPC's function requires a different trigger (noted below).

- **Rowan** - placed in Rowan's Cottage (before the player first leaves) and at the Village Green near the well (after the player first leaves), per the World-State Flag section above. Two-page event: page 1 (default/before-first-exit) at the cottage, page 2 (after-first-exit or after-sword, whichever flag Codex selects for consistency) at the Green. Delivers the Hidden Cave rumor (dialogue content only, see event plan's Dialogue Hooks below).
- **Elara** - placed in Rowan's Cottage (default) with a secondary placement near the garden/flowerbed during the day, using the same flag pattern as Rowan if a two-location placement is implemented, or a single fixed placement if simpler - Codex's discretion, since the specification does not require two-location placement for Elara as strictly as it does for Rowan's rumor delivery. Must include the after-sword dialogue page (visible concern per specification Section 3).
- **Garrick** (Blacksmith) - fixed placement inside the Blacksmith interior, near the forge. Triggers the Blacksmith shop (see Shops below) and optional flavor dialogue on a separate interaction path if the project's event structure supports both (e.g., "Talk" vs. "Shop" branching on a single event, or two adjacent events - Codex's discretion).
- **Mabel** (General Store) - fixed placement inside the General Store interior, behind the counter. Triggers the General Store shop; independent second source for the Hidden Cave rumor (specification Section 5's redundant-hints requirement).
- **Tomas** (Inn) - fixed placement inside the Inn interior, behind the counter. Triggers the rest/save interaction (see Save Point below) and seeds the Rustshore/wider-world rumor.
- **Background villagers** (children, elderly villager, farmer/field worker, optional wandering peddler) - fixed placements per the specification's Section 3 locations (Green/well area for children and the elder; village edge for the farmer; near the Inn for the optional peddler). Simpler event pages are acceptable here (no two-page gating required) since none of these carry required progression information.

## Signs

- One examine-only sign event at each of the three commercial buildings (General Store, Blacksmith, Inn), Action Button trigger, showing a short flavor/name text. No shop or dialogue logic attached to the sign itself - the sign is separate from the NPC/shop event.

## Bookshelves

- One examine event on the bookshelf inside Rowan's Cottage. First interaction shows a flavor/history message (per specification Section 6). A second interaction (or an interaction gated behind having already seen the first, using a self-switch) surfaces the hidden journal page secret (specification Section 7) - implement as a self-switch-gated second event page, not a repeatable random reveal.

## Save Point

- The Inn's rest/save function should default to the project's existing save policy (standard RPG Maker MZ save-anywhere via the system menu) unless the broader project has already established restricted, location-based saving elsewhere - this plan does not introduce a new restricted-save system. Implement a bed/counter interaction at the Inn (Tomas or an adjacent object) that restores party HP/MP as a "rest" action; treat this as distinct from whatever the project's existing save mechanism is.

## Shop

- **General Store:** standard Shop Processing event command triggered by talking to Mabel, stocked with basic consumables only (no equipment), per specification Section 2. Exact item IDs and prices are not specified here - use the project's existing lowest-tier consumable database entries; if none exist yet, flag back to design/production rather than inventing new items ad hoc.
- **Blacksmith:** standard Shop Processing event command triggered by talking to Garrick, stocked with basic weapon/armor only, per specification Section 2. Same item-ID caveat as above applies.

## Inn

- Covered under Save Point above (rest function) and NPCs above (Tomas). No additional event beyond the rest interaction and Tomas's dialogue/rumor trigger is required.

## Ambient Events

- Background villager idle movement (short "random" or "custom route" movement type per event page, non-blocking, low-key) for children near the well and any other background villager where light motion reinforces the "lived-in" goal.
- Ambient audio (BGS autoplay appropriate to the village exterior - wind, birds, distant activity) configured at the map level, not as a separate event.
- The well's "funny echo" detail (specification Section 6/8) is implemented as part of the well's own interactable event (see Interactables below), not as a separate ambient event.

## Interactables (Non-NPC)

- **Village Well:** Action Button trigger, examine message including the "off" echo detail (hidden-systems hint, specification Section 8).
- **Village Memorial:** Action Button trigger, examine message reinforcing local history (specification Section 6/8).
- **Fireplace (Rowan's Cottage):** Action Button trigger, short comfort-flavor examine message.
- **Barrels/crates (near General Store and Blacksmith):** Action Button trigger; at least one of these is the Hidden Coin secret (see Secrets below), the rest are flavor-only examine messages.

## Secrets

Each implemented as a one-time reveal using a self-switch (or independent local switch per event) so repeated interaction after collection does not re-trigger the reward - no mandatory secret blocks any required path, per specification Section 7 and the bible's "no mandatory secrets" rule.

- **Hidden Herb:** item-grant event in Elara's garden/flowerbed near Rowan's Cottage, self-switch gated after first pickup.
- **Rowan's Bookshelf journal page:** covered under Bookshelves above.
- **Optional Viewpoint:** examine-only event (no item) at the village's edge, showing a short message plus framing at least one overworld landmark silhouette visually (map composition, not event logic) per the map brief's Landmarks section.
- **Hidden Coin (Barrel):** item/gold-grant event on one specific barrel/crate near the shops, self-switch gated after first pickup.

## Future Expansion Hooks

- The world-state flag pattern (see World-State Flag above) is the primary expansion hook - any future beat that needs Ashford Village to react (beyond the after-sword state already required here) should reuse the same flag-gated two-page event pattern already established for Rowan, Elara, Garrick, and Mabel, rather than introducing a new mechanism.
- No additional NPCs, buildings, or systems (day/night, weather, relationship/affinity tracking) should be added speculatively - if a future work order needs one of these, it should specify it explicitly against this same event plan structure.

## Explicitly Not In This Plan

Per WP-03's constraints, this plan defines requirements only. It does not write dialogue text, does not specify exact tile coordinates, does not assign concrete switch/variable ID numbers (Codex's implementation discretion, consistent with the project's existing numbering conventions), and does not specify exact shop item/price lists beyond "basic consumables" and "basic weapon/armor."
