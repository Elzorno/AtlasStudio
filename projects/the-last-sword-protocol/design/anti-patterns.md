# Anti-Patterns

## Purpose

`jrpg-design-bible.md` states what The Last Sword Protocol should feel like. This document states what to explicitly avoid, and why each anti-pattern would break that feel. Naming failure modes exists because a design standard stated only in positives is easy to violate by accident - it is much harder to accidentally build "a giant empty overworld" if the term itself is a known red flag during review.

## The Anti-Patterns

### Zelda-Style Screen Progression

**What it looks like:** locations modeled as a chain of discrete, disconnected screens entered and exited in a fixed sequence, with no continuous overworld geography connecting them.

**Why it breaks the feel:** it directly contradicts `world-model.md`'s core design rule and the bible's Section 1 - the overworld stops being a gameplay system and becomes a menu of screens. This was explicitly identified as Atlas v1's failure mode in `story-reset.md` ("stop treating each location as a Zelda-style room progression") and is the single anti-pattern this whole design line exists to prevent from recurring.

### Objective-Marker-Driven Design

**What it looks like:** a UI marker, quest arrow, or highlighted map pin tells the player exactly where to go next, replacing rumors, visible landmarks, and world geography as the source of direction.

**Why it breaks the feel:** it inverts the Dragon Quest Philosophy's "curiosity over objective markers" principle. A player following a marker is not exploring; they are executing a pathfinding instruction. See `exploration-principles.md` for how to keep curiosity-driven design legible without falling back on markers.

### Tutorial Overload

**What it looks like:** the opening hour front-loads explicit tutorial text, forced menu walkthroughs, or more than 2-3 new mechanical concepts in a single beat.

**Why it breaks the feel:** it contradicts the Journey Principle's sense of discovery and the pacing guidance's "teach 2-3 ideas at once, maximum" rule for the first dungeon. A player being lectured through menus is not being invited to explore; the classroom-style exposition problem named in the bible's Section 8 applies to mechanics tutorials just as much as it applies to cybersecurity metaphors.

### Excessive Fast Travel

**What it looks like:** unlocking free, instant travel between most or all discovered locations early in the game, removing the overworld from routine play.

**Why it breaks the feel:** it directly undermines the Journey Principle - if the trip can always be skipped, the trip was never really part of the design, only a one-time cost paid before fast travel unlocks. Fast travel is not banned outright, but it should never be granted so early or so broadly that overworld traversal stops being a normal part of play during the region it was designed for.

### Empty Overworld Maps

**What it looks like:** overworld stretches with no encounter zones, landmarks, branching paths, or visible destinations - distance for its own sake.

**Why it breaks the feel:** `exploration-principles.md`'s density rule exists specifically to catch this. Empty distance reads as padding, not exploration, and actively works against the "meaningful overworld traversal" principle.

### Filler Content

**What it looks like:** rooms, NPCs, encounters, or dialogue that exist only to extend playtime, with no narrative purpose, gameplay purpose, or connection to the region's identity.

**Why it breaks the feel:** every dungeon (bible Section 6) and every region (bible Section 4) is defined by having a purpose and identity. Content added purely to pad length dilutes that identity and trains the player to stop paying attention to their surroundings, which undermines curiosity-driven discovery for everything that follows.

### Arbitrary Fetch Quests

**What it looks like:** "bring me N of item X" or "go retrieve this thing for no reason beyond the request itself" quests with no connection to world state, character motivation, or the region's identity.

**Why it breaks the feel:** it substitutes a checklist for the Dragon Quest Philosophy's "towns as communities" principle - an NPC who exists only to hand out a fetch request is a quest dispenser, not a community member. Any fetch-shaped quest that does appear should be justified by a specific, stated in-fiction reason tied to that NPC or location, not used as generic content filler.

### Plugin-First Solutions

**What it looks like:** reaching for a third-party RPG Maker plugin to solve a design problem before considering whether the underlying design should be simpler, or whether the engine bridge's existing tools already cover it.

**Why it breaks the feel:** this is specifically a production anti-pattern rather than a player-facing one. Per `studio/workflow.md`'s Engine Bridge Rule and `bridges/rpg-maker-mz/bridge-design.md`, engine-specific implementation details (including plugin dependencies) should be deliberate bridge-layer decisions, not ad hoc additions that accumulate hidden dependencies and ownership ambiguity outside the bridge's ownership model. A plugin dependency also risks locking design decisions to implementation convenience rather than to what the design bible actually calls for.

## Future Integration: Recommended Atlas Lint Rules

The Canon Linter (`tools/atlas_lint/`) currently checks deterministic graph-structural properties (`tools/atlas_lint/rules/canon_lint_rules.json`: Structure, Completeness, Consistency, Coverage, Production, Bridge categories, using rule `kind: required_relationship` over the Atlas Graph). Several anti-patterns above are graph-checkable today or with a small new rule `kind`; others are not graph-shaped and should stay human/AI creative review instead. This section recommends specific future work, not an implementation - building these rules is out of scope for this documentation-only work order.

**Graph-checkable now, as new rule entries under existing `required_relationship` kind:**

- A new category, **Design**, alongside Structure/Completeness/Consistency/Coverage/Production/Bridge, for JRPG-design-bible-derived checks.
- `design.region_has_adventure_site` - regions should contain at least one `location` with an adventure-site subtype, mirroring the existing `structure.region_contains_settlement` rule shape, to catch a region that never got its adventure site modeled.
- `design.quest_not_bare_fetch` - flag `quest` nodes whose only edges are `REQUIRES`/`REWARDS` with no `APPEARS_IN` or narrative-context edge to a character or story beat, as a heuristic proxy for the Arbitrary Fetch Quest anti-pattern (a real fetch quest tied to a character and motivation would have that context edge; a placeholder one likely would not).

**Graph-checkable with a new rule `kind` (recommended for design in a future work order, not specified in full here):**

- A `kind: node_count_range` rule shape, to flag a region node whose contained landmark/adventure-site count is disproportionate to typical overworld traversal time - a rough, heuristic proxy for Empty Overworld Maps, acknowledging that true "emptiness" is a playtest/production concern the graph alone cannot fully measure.
- A `kind: pacing_budget` rule shape that cross-references `pacing-guidelines.md`'s target minutes (once expressed as graph-attached metadata, e.g. a `target_minutes` field on beat-representing nodes) against actual playtest-logged durations recorded as production graph facts, to flag pacing drift automatically rather than only through manual review.

**Not graph-checkable - remain human/AI creative review, not lint rules:**

- Zelda-Style Screen Progression, Tutorial Overload, Filler Content, and Plugin-First Solutions are judgments about *how* content is built and *why* it exists, not facts a graph schema can represent without heavy subjective tagging. These stay in the domain of design review against this document and the bible, using human judgment plus GPT/Claude Code creative and architectural review, not a deterministic gate. Attempting to force these into lint rules would violate the "deterministic systems before opaque AI" principle in the wrong direction - turning a subjective creative judgment into a false-precision automated check.

Any future work order that implements new Canon Linter rules from this list should follow the existing pattern in `tools/atlas_lint/rules/canon_lint_rules.json` (reviewable JSON rule definitions, warning severity by default, never modifying canon) and should itself be reviewed against `studio/governance/atlas-principles.md`'s "Deterministic systems before opaque AI" principle before being accepted.
