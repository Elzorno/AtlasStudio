# DEC-0001 - Ashford Shop (Map003) Rejected at Human Playtest

## Status

Accepted (as a rejection - the map is not accepted; this record closes the open playtest question, it does not close the map's production).

## Date

2026-07-08

## Record Type

This is a **production content decision**, not an Atlas Core architectural decision. It follows `studio/governance/decision-record-template.md`'s shape but is filed under `studio/governance/decisions/` rather than as an `ADR-NNNN` entry in `studio/governance/architectural-decision-log.md`, because it does not meet any of `atlas-principles.md`'s "When Atlas Core Changes Require an ADR" triggers (schema change, governance boundary, QA gate behavior, assignment model, supersession). It records a human decision about one piece of game content, using the same discipline the ADR log applies to architecture: dated, reasoned, never silently deleted or overwritten if reversed.

## Context

`reports/production-review/ashford-shop-production-review.md` and `pipeline-gap-analysis.md` (`WO-0028`, 2026-07-08) found that `TheLastSwordProtocol-Game/data/Map003.json` (`INT_Ashford_Shop`) had been hand-built to satisfy `IMP-HOM-019`'s functional requirements (working shopkeeper interaction, correct collision, correct transfers, both dialogue states) but had never received the human playtest and Production Director acceptance pass that `bridges/rpg-maker-mz/passability-rule.md` and `ashford-village-contract.md` both require before a map can be treated as done. That review's own map inspection found the artifact's embedded `note` field already flagged this: *"Status: polish submitted, pending Production Director acceptance (not final accepted)."* `pipeline-gap-analysis.md` Finding 1 named closing this open question as the review's single highest-priority, `Critical` item, and `studio/governance/production-readiness.md`'s backlog listed it first under `Immediate`.

This record is the human playtest/acceptance decision that finding called for.

## Decision

**Rejected.** The Production Director's verdict, delivered 2026-07-08: *"Map satisfies functional requirements but fails visual composition and environmental quality standards. Requires human art direction or pattern-guided reconstruction before acceptance."*

This is a **functional pass, composition-and-quality fail.** It is not a rejection of `IMP-HOM-019`'s requirements, the shopkeeper event, the dialogue, the transfers, or the collision - `ashford-shop-production-review.md` Stage 5 already found those sound, and this decision does not disturb that finding. It is a rejection of the room's visual composition and environmental quality against `bridges/rpg-maker-mz/map-quality-standard.md`'s bar ("Would this be believable as a polished RPG Maker MZ sample map adapted to The Last Sword Protocol's story?") and, implicitly, against `studio/design-patterns/interiors/shop.pattern.md`'s Composition Rules - the pattern layer that existed at review time but, per `ashford-shop-production-review.md` Stage 3, was never actually consulted during the real build.

Two remediation paths are named, not mutually exclusive:

1. **Human art direction** - a human artist or designer reworks the room's composition directly.
2. **Pattern-guided reconstruction** - a genuine, live application of `studio/contracts/PATTERN_CONTRACT_SPEC.md` (`WO-0027`) against `shop.pattern.md` and the `Interior` environment-tier evidence, executed for real this time rather than demonstrated retroactively.

This record does not choose between the two paths. That choice is deferred to whoever scopes the follow-up work.

## Consequences

- `TheLastSwordProtocol-Game/data/Map003.json`'s ledger state remains `hand_authored`, per `map_ownership.json`. This decision does not flip it to `locked` - a rejected map must not be locked, since `locked` means "frozen, nobody writes without a Production Director decision" and further work is now expected. It also does not revert it to `generated` - reverting a ledger state deliberately discards hand work and requires its own recorded Production Director decision per `AGENTS.md`, which this record does not make; the existing hand-built content (dialogue, events, transfers) is not being discarded, only its composition/environmental polish.
- `pipeline-gap-analysis.md` Finding 1 and `production-readiness.md`'s Playtesting rating (`Not Ready`) are now partially addressed: the open question is closed (a human decision was recorded), but the underlying map is not yet accepted, so `production-readiness.md`'s overall Playtesting rating should not move to `Ready` on the strength of this record alone - it should move only once a subsequent playtest accepts a revised build.
- Whichever remediation path is chosen, the resulting artifact should re-enter the same validation and playtest stages `ashford-shop-production-review.md` Stages 7-8 already described, not skip them a second time - this decision does not grant a shortcut past re-validation.

## Alternatives Considered

- **Accept as-is, treat visual composition as a future polish pass.** Rejected by the Production Director - functional correctness alone does not meet `bridges/rpg-maker-mz/map-quality-standard.md`'s stated bar, and accepting now would set a precedent that composition quality is optional at first submission.
- **Revert Map003 to `generated` and let a future pipeline pass regenerate it from scratch.** Not chosen. The existing hand-authored content (real dialogue for both story states, working Shop Processing, correct collision) is sound and traceable to `IMP-HOM-019`; discarding it to start over would lose real, validated work to fix a composition problem that does not require discarding the underlying event logic.

## Related

- Work order: `WO-0028-production-pipeline-validation.md` (the review that surfaced this open question).
- Related documents: `reports/production-review/ashford-shop-production-review.md`, `pipeline-gap-analysis.md`, `lessons-learned.md`; `studio/governance/production-readiness.md`; `reports/implementation-contracts/ashford-shop-build-contract.md`, `ashford-shop-pattern-aware-contract.md`; `studio/design-patterns/interiors/shop.pattern.md`; `bridges/rpg-maker-mz/map-quality-standard.md`.
- Follow-up: not yet scoped as of this record. See the next entry in this directory, if one is filed, for whichever remediation path is chosen.

## Governance Note

Not an Atlas Core architecture change - no ADR trigger applies. Filed as the first entry under `studio/governance/decisions/` specifically because no prior convention existed for recording a production content decision at this level of formality; `production-readiness.md`'s backlog (`Immediate`, item 3) anticipated exactly this gap for Ashford Shop and, by the same reasoning, for Map001/Map002's still-outstanding certification.
