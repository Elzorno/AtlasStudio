# Player Experience Map - First Playable Hour

## Purpose

This document maps the intended emotional and experiential flow of the first playable hour.

It is not a world map, implementation map, or story script.

It exists to keep implementation aligned with what the player should feel while exploring Ashford Vale.

## Design Rule

Every segment should eventually become playable.

This document should unlock implementation work rather than becoming a standalone artifact.

## Experience Arc

| Segment | Intended Emotion | Player Question | Playable Expression |
|---|---|---|---|
| Rowan's Cottage | Comfort | Where am I? | Warm home interior, familiar objects, optional inspection. |
| Ashford Village | Belonging | Who lives here? | NPCs, shops, well, children, animals, village green. |
| Village Rumors | Curiosity | What is everyone hinting at? | Optional conversations about ridge, cave, weather, old stories. |
| Leaving Town | Gentle Freedom | Can I just go explore? | South/east/north exits visible, overworld access without heavy tutorial. |
| First Overworld | Wonder | What's over there? | Windmill, fields, ridge, cave silhouette, blocked paths, visible landmarks. |
| First Encounter | Surprise | Are the roads safe? | First low-risk battle after a short exploration delay. |
| Cave Entrance | Mild Disappointment | Is this really the famous cave? | Ordinary-looking entrance, no spectacle. |
| Cave Descent | Unease | Why does this place feel wrong? | Natural cave gradually shifts into impossible geometry. |
| Sword Shrine | Awe | What did I find? | Quiet chamber, sword response, subtle activation. |
| Walk Home | Doubt | Did anything actually happen? | Changed ambience, NPC noticing player looks pale, Rowan concern. |
| Night Sequence | Mystery | Was that a dream? | Fragmented vision, no full explanation. |
| Morning After | Anticipation | What changed? | New reactions, sword relevance begins, path to ruins opens. |
| Glassfield Ruins | Discovery | What was hidden here? | Sword opens sealed site, first access-control metaphor. |
| First Relay | Consequence | What did I wake up? | Relay activation changes world state. |
| Rustshore | Release | Where can I go now? | Lighthouse/dock departure, wider world implied. |
| Prototype Credits | Completion | What comes next? | End of Chapter 1 prototype message. |

## Dragon Quest Alignment

The player should discover objectives through curiosity, visible geography, and rumors rather than direct UI instruction.

The early flow should be:

```text
Home
  ↓
Town
  ↓
Overworld
  ↓
Landmark
  ↓
Cave
  ↓
Return
  ↓
New access
  ↓
Departure
```

This must not collapse into a Zelda-style chain of adjacent puzzle screens.

## Implementation Implications

The first implementation packages should produce player-visible results in this order:

1. Rowan's Cottage interior
2. Ashford Village exploration shell
3. Ashford Vale overworld shell
4. Hidden Cave entrance and first rooms
5. Sword Shrine event
6. Return-home state change
7. Glassfield Ruins access
8. First Relay activation
9. Rustshore departure

## Immediate Next Player-Visible Target

The next player-facing design package should be:

```text
Ashford Village Experience Specification
```

It should define:

- village layout
- NPC list
- interactable objects
- rumors
- shops/services
- initial player path options
- secrets
- implementation acceptance criteria

That specification should be followed immediately by an implementation work package.
