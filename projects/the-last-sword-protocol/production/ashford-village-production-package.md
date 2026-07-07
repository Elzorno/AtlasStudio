# Ashford Village Production Package

## Purpose

Ashford Village has been fully designed (`projects/the-last-sword-protocol/design/ashford-village-experience-specification.md`). This package does not redesign it. It bridges that approved design into an implementation contract - the final production package before RPG Maker implementation (WP-03B) begins.

This document summarizes and indexes three companion documents, each a required part of the contract:

- `ashford-village-map-brief.md` - what the maps must look like and contain.
- `ashford-village-event-plan.md` - what every required event must do.
- `ashford-village-implementation-checklist.md` - how completion is verified.

Together, these four documents should let an implementation agent build Ashford Village with minimal creative interpretation. If a creative decision is still required after reading all four, that is a gap in this package, not a decision the implementation agent should make unilaterally.

## Reference Materials Used

- `ATLAS_CORE_1.0.md` and `studio/governance/atlas-principles.md` (constitution and governance).
- `projects/the-last-sword-protocol/design/jrpg-design-bible.md` and its companions (`exploration-principles.md`, `pacing-guidelines.md`, `anti-patterns.md`).
- `projects/the-last-sword-protocol/design/player-experience-map.md`.
- `projects/the-last-sword-protocol/design/ashford-village-experience-specification.md`.
- `bridges/rpg-maker-mz/bridge-design.md`, `ownership-model.md`, `handoff-format.md`.
- `bridges/rpg-maker-mz/map-quality-standard.md` and `passability-rule.md`.
- `references/rpg-maker-mz-samples/official sample project/` - studied for composition, environmental density, building spacing, event organization, JSON structure, map scale, and passability assumptions only. No map, event, or dialogue content was copied from it; only quality and structure were matched.

## Known Open Dependency: Map Quality And Passability Preflight

`work-orders/WP-03-preflight-map-quality-passability.md` is the designated read-only inspection of `TheLastSwordProtocol-Game`'s actual tileset and passability data, and is still `status: proposed` as of this package. This production package specifies tileset *roles* and passability *requirements* without asserting verified, concrete tileset IDs from the real game repository, because that verification is explicitly the preflight package's job, not this one's. **WP-03B should not assign final numeric tileset IDs until the preflight is completed or its equivalent inspection is otherwise performed.** Everything else in this package (map brief targets, event requirements, checklist) is independent of that gap and can be used immediately.

## What Codex Needs

- All three companion documents (map brief, event plan, checklist) as the primary implementation contract.
- The experience specification for narrative/character grounding of every interaction.
- Read access to `TheLastSwordProtocol-Game`'s current tileset and database data (items/weapons/armors for the shops), ideally via the WP-03-preflight findings once available, to translate brief targets into actual tile and event data.
- The bridge's ownership model (`bridges/rpg-maker-mz/ownership-model.md`) to correctly mark new maps/events as agent-drafted rather than accidentally overwriting anything already present.

## What Copilot Can Help With

- Repetitive event boilerplate: duplicating the two-page NPC event pattern across Rowan, Elara, Garrick, and Mabel once the pattern is established for one of them.
- Background villager event scaffolding (children, elder, farmer, peddler) - these are simpler, repeatable patterns per the event plan.
- Self-switch-gated secret events (Hidden Herb, Hidden Coin) - structurally identical to each other.
- Shop-processing event boilerplate for the General Store and Blacksmith once item lists are confirmed.

## What GPT Should Review

- The actual dialogue text once Codex has event hooks scaffolded, checked against the specification's Section 4 Dialogue Goals - GPT does not build maps or events, but should author and/or review the words themselves.
- Whether the finished village still reads as curiosity-driven and community-like (bible Sections 3 and 5) rather than mechanical, once it is playable - a creative-feel check, not a technical one.

## What Atlas Validates

- `python3 tools/atlas_graph/validate_graph.py` - structural integrity of any new production/bridge graph facts this package or WP-03B introduces.
- `python3 tools/atlas_lint/canon_lint.py --project the-last-sword-protocol` - confirms no canon drift occurred, since this package and WP-03B should not touch canon.
- `python3 tools/atlas_format/format_guard.py --check` - confirms no formatting-only churn is hiding in any graph JSON change.
- Passability and route validation per `bridges/rpg-maker-mz/passability-rule.md` - note that AtlasStudio does not yet have an automated passability validator built (the Passability Rule anticipates one; `WP-03-preflight` was the package positioned to recommend it). Until such a validator exists, the Passability Rule's own fallback applies: **a human playtest is still required** and is not optional, regardless of how thorough the checklist review is.

## What Requires Human Approval

- Final map quality acceptance against the sample-map quality bar (`bridges/rpg-maker-mz/map-quality-standard.md`'s Acceptance section) - this is a judgment call, not a deterministic gate.
- Promoting Garrick, Mabel, or Tomas from production-only names to canon characters, if a future work order proposes that.
- Any new shop item/price database entries, if the project's existing consumable/equipment tiers are insufficient for the General Store or Blacksmith.
- Final acceptance of Ashford Village as a complete, playable beat of the First Playable Hour milestone.

## Constraints Honored By This Package

This package does not redesign gameplay or story, does not modify canon, does not modify `TheLastSwordProtocol-Game` or any other RPG Maker repository, and does not generate maps or events itself - it prepares the contract implementation agents will execute. The Immutable Formatting Rule is preserved: no existing file in this repository was reformatted to produce this package.
