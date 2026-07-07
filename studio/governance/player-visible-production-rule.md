# Player-Visible Production Rule

## Purpose

AtlasStudio exists to help build playable experiences, not merely artifacts about those experiences.

The first Atlas prototype produced useful documents and scaffolds, but it drifted toward artifact production instead of game production. AtlasStudio must explicitly prevent that failure mode.

## Rule

Every implementation cycle should end with something the player can see, hear, interact with, or feel.

Planning artifacts are allowed only when they unlock a concrete implementation path.

## 1:1 Production Rule

For every planning artifact created during active game production, AtlasStudio should identify the implementation work it enables.

```text
Design
  ↓
Implementation
  ↓
Validation
  ↓
Playable Experience
```

Avoid this pattern:

```text
Design
  ↓
Design
  ↓
Design
  ↓
Maybe implementation later
```

## Player-Visible Field

Future work orders and work packages should include:

```yaml
player_visible: true|false
```

Use `true` when the work directly creates or improves something the player can experience.

Examples:

- map implementation
- NPC dialogue in game
- battle encounter
- item behavior
- music or sound
- event sequence
- save point
- shop interaction

Use `false` when the work supports production but is not directly player-facing.

Examples:

- tooling
- bridge design
- graph maintenance
- documentation-only work
- validation scripts

## Produces Field

Future implementation work should include:

```yaml
produces:
  - map.ashford_village
  - npc.rowan
  - event.obtain_last_sword
```

The `produces` field records which player-facing or implementation assets a work package creates or materially changes.

This allows AtlasStudio to answer:

- Who produced this asset?
- What work package owns this event?
- Which playable beats are complete?
- What remains unimplemented?

## Playability Metric

AtlasStudio should eventually report playability alongside graph, canon, production, and bridge health.

Example:

```text
Playability
  Opening Sequence: incomplete
  Ashford Village: incomplete
  Ashford Vale Overworld: incomplete
  Hidden Cave: incomplete
  Sword Shrine: incomplete
  Glassfield Ruins: incomplete
  Rustshore Departure: incomplete
```

The initial metric may be simple and checklist-based. It does not need to be a perfect measure of fun.

## Governance

Atlas Core work remains allowed, but new core features should be demand-driven by production needs.

Before approving additional infrastructure work, ask:

1. What player-visible work does this unlock?
2. Is this blocking implementation?
3. Can this wait until the game exposes a real need?

## Design Principle

Atlas proposes. Humans approve. Players experience.

If the player never experiences the result, the work must justify why it was necessary.
