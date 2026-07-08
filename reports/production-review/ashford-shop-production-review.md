# Ashford Shop Production Review

Status: submitted

Scope: `WO-0028`. Walks the complete production pipeline that produced (and is still producing) `TheLastSwordProtocol-Game/data/Map003.json` (`INT_Ashford_Shop`), stage by stage, against the pipeline diagram in this work order's brief: Creative Authority -> Implementation Packet -> Pattern Resolution -> Pattern-Aware Contract -> Implementation Agent -> Game Repository -> Validation -> Human Playtest.

## Method and a Necessary Correction to the Premise

This work order's Objective states that "AtlasStudio has completed the first full production cycle using the new architecture" and asks this review to evaluate how well that cycle worked. Direct inspection of the actual production history - git history in `TheLastSwordProtocol-Game`, build reports in `rpgmakerLSP`, and the pattern/contract work orders in `AtlasStudio` itself - shows this premise needs one correction before the walkthrough below can be honest: **the Design Pattern Library, Pattern Inheritance Model, Pattern Resolution Rules, and Pattern-Aware Contract format (`WO-0024` through `WO-0027`) did not exist yet when Ashford Shop was actually built.**

The evidence, in order:

- `TheLastSwordProtocol-Game/data/Map003.json`'s final hand-built version was committed `2026-07-08 08:01:51 -0400` (commit `01692cb`, message `"for GPT"`).
- `WO-0024-design-pattern-library.md` through `WO-0027-pattern-aware-implementation-contracts.md` were all authored later the same day, in the session that produced this very review.
- `Map003.json`'s own embedded `note` field, written by whatever process produced this final version, reads in part: *"IMP-HOM-019 original manual build... Status: polish submitted, pending Production Director acceptance (not final accepted)."* It cites `IMP-HOM-019` and Atlas registry IDs directly. It does not cite `reports/implementation-contracts/ashford-shop-build-contract.md`, `WO-0020`, or any AtlasStudio work order.

So the honest scope of this review is two things at once: (1) an accounting of the real pipeline that actually produced Ashford Shop, which ran on Atlas canon and the Implementation Packet alone, without Pattern Resolution or a Pattern-Aware Contract; and (2) an evaluation - using `WO-0027`'s retroactive `ashford-shop-pattern-aware-contract.md` demonstration - of what the newer stages would have contributed had they existed in time. Both are done stage by stage below. Where a stage was not actually exercised, this review says so plainly rather than crediting the architecture with work it did not do.

## Stage 1: Creative Authority

**Purpose:** Establish the non-negotiable narrative and world-design facts this screen must satisfy.

**Inputs:** `atlas/docs/02_World/Screens/Home_Island/SCR_HOM_ASH_003_Ashford_Shop.md`, `atlas/docs/03_Story/Dialogue/Home_Island/Ashford_Dialogue_Packet.md` (`ATLAS-STY-010`), the Home Island Event and Transfer Registries.

**Outputs:** A stable set of canonical requirements - the shopkeeper's role, the two dialogue states (`Intro`, `After Node Seven`), registry IDs `EVT-HOM-008` and `TRN-HOM-003`/`TRN-HOM-004`, the two open questions (antidote stocking; post-Node-Seven inventory change) explicitly left unresolved.

**Successes:** This stage worked cleanly. Every canonical requirement traced through every later stage without distortion. The final map's shopkeeper event carries both dialogue states verbatim in spirit (`STATE_01_INTRO`, `STATE_04_AFTER_NODE07`, gated on switch 16 matching `NPC_Ashford_PostNode07`), and the two open questions remain genuinely open in the artifact - nobody quietly resolved them along the way.

**Weaknesses:** None specific to this stage. It is worth noting this stage's stability is doing a lot of the pipeline's real work - everything downstream that went well, went well because Atlas's own material was already precise and complete.

**Opportunities:** None identified. This stage does not need architectural change.

## Stage 2: Implementation Packet

**Purpose:** Translate Creative Authority into a concrete, buildable technical specification for one screen.

**Inputs:** Stage 1's outputs, plus `atlas/docs/09_Technical/Home_Island_Tileset_Assignment_Matrix.md` and the SVG layout guide.

**Outputs:** `IMP-HOM-019` (`canonical: true`, `owner: Technical Director`) - tileset/terrain/collision requirements, required visual elements, required events with registry IDs, Shop Processing inventory guidance, required transfers, story-state requirements, and nine numbered acceptance criteria.

**Successes:** `IMP-HOM-019` is a genuinely well-formed packet. Every requirement it states is traceable to Stage 1, every requirement is concrete enough to build against without guessing, and its explicit Non-Goals section (no final art, no dialogue authorship, no automatic map construction) prevented scope creep in every downstream artifact this review inspected.

**Weaknesses:** None found in the packet itself. One weakness surfaced only in retrospect: `IMP-HOM-019` was written to be executed by "a human map author (or a guided-agent session under human review)" directly - it was not written assuming an AtlasStudio contract or pattern layer would sit between it and the implementing agent, and in practice, per Stage 4 below, none did.

**Opportunities:** Future packets in this series could note, in their own Traceability table, which AtlasStudio contract (if any) is expected to execute them - closing the gap Stage 5 identifies below before it opens.

## Stage 3: Pattern Resolution

**Purpose (as designed, `WO-0026`):** Combine Environment, Specialization, and Project-specific pattern layers into one resolved set of reusable craft guidance, ready to be layered under an Implementation Packet's authoritative requirements.

**Inputs (as designed):** `studio/design-patterns/interiors/shop.pattern.md`, the virtual `Interior` environment-tier evidence in `reports/design-patterns/interior-pattern-corpus-review.md`, and (had one existed) a Project-specific Ashford Village pattern.

**Outputs (as designed):** A resolved, per-layer-confidence-tagged guidance set, per `PATTERN_RESOLUTION_RULES.md`'s five-step pipeline.

**What actually happened:** Nothing. This stage did not exist yet. `shop.pattern.md` was not authored until `WO-0024`, on `2026-07-08`, after Ashford Shop's final build commit. No pattern resolution of any kind informed the real build.

**Successes:** None to report for the real cycle - the stage did not run. Evaluated retroactively (per `WO-0027`'s demonstration, `Pattern Resolution` section of `ashford-shop-pattern-aware-contract.md`): had this stage existed, it would have added craft guidance the real build already happened to get right by other means - wall-anchored stock, a centerline from door to counter, dense-perimeter/light-center rhythm. The real build satisfies nearly all of it, which is a point in favor of `IMP-HOM-019` and ordinary craft judgment being sufficient on their own for a build this size, not necessarily a point in favor of the pattern layer being load-bearing.

**Weaknesses:** The stage's complete absence from a "first full production cycle" is itself the weakness this review must record plainly - see "Method and a Necessary Correction to the Premise" above.

**Opportunities:** The next screen built after this review - not Ashford Shop retroactively - is the correct test case for whether Pattern Resolution changes an outcome, a decision, or a review conversation in practice. See `pipeline-gap-analysis.md` and the backlog in `studio/governance/production-readiness.md`.

## Stage 4: Pattern-Aware Contract

**Purpose (as designed, `WO-0027`):** Assemble Creative Authority, Implementation Packet, and resolved pattern guidance into one contract, with guidance explicitly split into Authoritative / Pattern-derived / Recommendations.

**Inputs (as designed):** Stages 1-3's outputs.

**Outputs (as designed):** A contract an implementing agent can execute directly.

**What actually happened:** The real build used the older, non-pattern-aware contract format instead - or, per the artifact's own citations, arguably neither: `ashford-shop-build-contract.md` (`WO-0020`) exists and correctly translates `IMP-HOM-019` into AtlasStudio's contract format, but the final `Map003.json` does not cite it anywhere in its own embedded comments. It cites `IMP-HOM-019` and Atlas registry IDs directly. This review cannot confirm from the artifact alone whether the implementing agent read `ashford-shop-build-contract.md` at all, or worked straight from the Atlas packet.

**Successes:** Evaluated retroactively (`ashford-shop-pattern-aware-contract.md`): the format itself produces a clear three-way split and correctly resolves that `IMP-HOM-019`'s specific requirements (counter as centerpiece, ~15x11/17x13 sizing, cabinet placement) outrank the generic `shop.pattern.md` guidance they overlap with. This is a real, checkable design success of `WO-0027`'s format, independent of whether it was used here.

**Weaknesses:** Not exercised on a real build. Also exposes the traceability gap named in Stage 5: even the *older* contract format's real-world influence on this specific artifact cannot be confirmed by inspection.

**Opportunities:** See `pipeline-gap-analysis.md`, "Traceability from contract to artifact."

## Stage 5: Implementation Agent

**Purpose:** Turn a contract (or, as happened here, a packet read directly) into RPG Maker MZ map data.

**Inputs:** `IMP-HOM-019`, and whatever intermediate contract, if any, the implementing agent actually consulted.

**Outputs:** `data/Map003.json`, built across several distinct passes (see below).

**Successes:** The final output is good work by direct inspection. The shopkeeper event carries real, in-voice dialogue for both story states (not placeholder text), a working Shop Processing command (`Potion`, item 1, 50G), correct collision landmarks matching `IMP-HOM-019`'s "counter blocks on every side except the shopkeeper's interaction side" requirement, a correctly round-tripping exit transfer, and an optional cabinet examine event exactly where the SVG guide places it. The map's own `note` field is unusually good practice: it records what changed, why, and its own acceptance status in plain language, directly in the artifact - a form of self-documentation none of AtlasStudio's format specifications currently require but arguably should (see `lessons-learned.md`).

**Weaknesses:** Three, all specific and checkable:

1. **The build ran in at least three visibly different passes with three different levels of rigor**, none clearly labeled as superseding the last except by the artifact's own `note` field: an automatic blueprint-generated placeholder (`BUILD-0025`, `2026-07-04`, `rpgmakerLSP`'s `generate_map_from_blueprint.py`); two further automated "landmark decoration" passes while the map's ledger state was still legitimately `generated` (`2026-07-05`); and a final hand-authored polish pass (`2026-07-08`) that replaced the decorative-landmark version wholesale. A reader without git archaeology access has no way to know this history from the Game repository alone.
2. **The final pass does not identify its own implementing agent.** The commit author is a human account; the commit message ("for GPT") suggests a handoff for review rather than a closed, attributed piece of work. Neither `bridges/rpg-maker-mz/handoff-format.md`'s "Audit Summary Format" nor `ownership-model.md`'s "Reporting Requirement" - both of which ask for exactly this information - appear to have been filled out anywhere this review could find.
3. **No visible citation of the AtlasStudio contract layer**, as noted in Stage 4.

**Opportunities:** Require the RPG Maker Audit Summary (`bridges/rpg-maker-mz/handoff-format.md`) as a literal deliverable, not an optional convention, for any future hand-build pass - see `pipeline-gap-analysis.md`.

## Stage 6: Game Repository

**Purpose:** Hold the accepted, canonical implementation state.

**Inputs:** Stage 5's output.

**Outputs:** `data/Map003.json` at `hand_authored` ledger state (`map_ownership.json`, flipped `2026-07-06`, per `WO-0031` in the Game repository).

**Successes:** The ownership ledger model worked exactly as designed throughout this entire history. The two automated "landmark decoration" passes on `2026-07-05` were legitimate, because Map003 was still `generated` at that time - no pipeline script wrote to a `hand_authored` or `locked` map at any point this review could find, across the entire Home Island map set, not just Map003. This is a genuinely strong result for `bridges/rpg-maker-mz/ownership-model.md` and the `AGENTS.md` ledger rule: the single hardest failure mode that model exists to prevent (an automated pass silently destroying hand-authored work) did not happen.

**Weaknesses:** The ledger's `hand_authored` label and the artifact's own `note` field disagree on what "done" means: the ledger presents Map003 as settled, hand-owned content; the note says the current content is "pending Production Director acceptance (not final accepted)." A ledger state of `hand_authored` currently conflates "a human/guided pass has started or completed work here" with "this content is accepted" - `AGENTS.md`'s own rule (flip to `hand_authored` "the moment manual editor work begins - not after") makes clear the former is the correct reading, but nothing in the ledger schema itself distinguishes an in-progress hand-authored map from an accepted one the way `locked` does for a fully certified map. A reader consulting only the ledger, not the artifact's own `note` field, would reasonably but incorrectly conclude Map003 is finished.

**Opportunities:** See `pipeline-gap-analysis.md`, "Missing: an in-progress vs. accepted distinction in the ownership ledger."

## Stage 7: Validation

**Purpose:** Confirm the implementation is structurally correct before it is treated as done.

**Inputs:** Stage 6's output at each pass.

**Outputs:** `rpgmakerLSP/reports/atlas-import/build-0025-ashford-shop-blueprint-round-trip-audit.md` (found 25, missing 0, warning 0), `build-0026-scr-hom-ash-003-blueprint-round-trip-audit.md`, and the `build-00NN-all-map-route-audit.md` series.

**Successes:** The automated validation tooling that exists is real, was actually run repeatedly (dozens of dated build reports), and reports clean results with specific, checkable counts rather than vague pass/fail statements - a strong pattern worth preserving.

**Weaknesses:** Every round-trip and route audit this review found for Ashford Shop validates the `2026-07-04`/`2026-07-05` blueprint-generated and decorated version. **No automated validation report was found covering the final `2026-07-08` hand-polished version** - the actual current content of `Map003.json`. The most recently changed, most load-bearing version of the deliverable is the one version this review could not find a corresponding validation record for.

**Opportunities:** Re-run the existing route/round-trip audit tooling against the current `Map003.json` before any acceptance decision - see `pipeline-gap-analysis.md`, flagged as an immediate item.

## Stage 8: Human Playtest

**Purpose:** Confirm, by an actual human playing the screen, what automated validation cannot check - movement feel, readability, whether the room reads as intended.

**Inputs:** A built, validated map.

**Outputs (expected):** A recorded playtest result and a Production Director acceptance decision, per `bridges/rpg-maker-mz/passability-rule.md`'s "Human Playtest Still Required" and `ashford-village-contract.md`'s Section 11 ("A human playtest/certification pass on Map001/Map002 is outstanding").

**What actually happened:** No playtest record specific to Ashford Shop was found anywhere in `TheLastSwordProtocol-Game`, `rpgmakerLSP`, or `AtlasStudio`. `rpgmakerLSP/reports/atlas-import/build-0043-guided-map-runtime-review.md` - the most recent general runtime-review record found - predates the final hand-build (`2026-07-05` vs. `2026-07-08`) and does not mention the shop at all. The map's own `note` field is the only place this review found an explicit acceptance status, and it states the pass is **not yet accepted**.

**Successes:** None to report - the stage has not yet run for this artifact. One adjacent success is worth naming: `BUILD-0043`'s general runtime review (which did happen, for other maps) is a real example of playtest evidence driving a production decision (the "NO GO for automatic final map construction" verdict that `IMP-HOM-019` and `ashford-shop-build-contract.md` both correctly inherit) - the mechanism works when it runs; it simply has not run for this specific artifact yet.

**Weaknesses:** This is the review's single most important open item. Per this work order's own Success Criteria, this review exists specifically to determine "where the architecture succeeded, where it required human intervention, and what should be improved before large-scale production begins" - and the honest answer for Ashford Shop's final state, right now, is that the human intervention this pipeline is designed to require **has not happened yet.**

**Opportunities:** See `pipeline-gap-analysis.md` and `studio/governance/production-readiness.md`, both of which treat this as the review's top-priority, immediate finding.

## Summary Table

| Stage | Actually exercised for Ashford Shop? | Result |
|---|---|---|
| Creative Authority | Yes | Clean, stable, no distortion downstream. |
| Implementation Packet | Yes | Well-formed; correctly executed in spirit. |
| Pattern Resolution | No - did not exist yet | Retroactively evaluated only. |
| Pattern-Aware Contract | No - did not exist yet | Retroactively evaluated only. |
| Implementation Agent | Yes | Good output; unattributed; unclear contract citation; multi-pass history not self-evident. |
| Game Repository | Yes | Ownership ledger held correctly throughout; ledger/note status mismatch found. |
| Validation | Partially | Strong tooling; not yet re-run against the final version. |
| Human Playtest | No | Not yet performed; artifact itself says so. |

See `pipeline-gap-analysis.md` for prioritized findings and `studio/governance/production-readiness.md` for the go/no-go assessment this summary feeds into.
