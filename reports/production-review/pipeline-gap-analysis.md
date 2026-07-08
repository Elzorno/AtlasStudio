# Pipeline Gap Analysis

Status: submitted

Scope: `WO-0028`. Identifies every place the Ashford Shop production history (see `ashford-shop-production-review.md`) shows information duplicated, information missing, an implementing agent guessing, a human having to interpret intent, the pipeline producing ambiguity, or the pipeline actually preventing a mistake. Each finding is prioritized (`Critical`, `High`, `Medium`, `Low`) and, where appropriate, points at a future work order this review recommends without creating one, per this work order's constraints.

Priority is assigned by concrete consequence, not by how interesting the finding is: `Critical` means an unresolved item currently blocks a defensible accept/reject decision; `High` means it will cause a real problem the next time this pattern repeats; `Medium` means it costs time or trust but has a workaround; `Low` means it is worth fixing but nothing is currently at risk.

## Findings: Information Missing

### 1. No human playtest record for Ashford Shop exists anywhere. (Critical)

Per `ashford-shop-production-review.md`, Stage 8: the map's own `note` field states the current build is "pending Production Director acceptance (not final accepted)," and no playtest log, issue report, or certification record specific to this screen was found in any of the three repositories this review searched. This is the review's single highest-priority finding. **Recommend:** a narrowly-scoped work order whose entire purpose is running and recording a human playtest pass against the current `Map003.json`, closing with an explicit accept/reject/revise decision - not a general "improve playtesting" work order, a specific one for this one artifact.

### 2. No automated validation record covers the final build. (Critical)

Every round-trip/route audit found (`build-0025-ashford-shop-blueprint-round-trip-audit.md`, `build-0026-scr-hom-ash-003-blueprint-round-trip-audit.md`) validates the `2026-07-04`/`07-05` blueprint-generated version, not the `2026-07-08` hand-polished version currently live. **Recommend:** re-run the existing route-audit tooling (already built, already proven reliable per the review) against the current file before any acceptance decision is made - this can likely be done as a checklist item inside the same work order as Finding 1, not a separate one.

### 3. No implementing-agent attribution or RPG Maker Audit Summary was filled out for the final build pass. (High)

`bridges/rpg-maker-mz/handoff-format.md`'s "Audit Summary Format" and `ownership-model.md`'s "Reporting Requirement" both specify exactly the information (targets changed, ownership states before/after, verification performed) this review had to reconstruct manually from git history instead of reading from a submitted report. The commit message "for GPT" suggests a handoff occurred, but to whom, from whom, and under what request is not recorded anywhere this review could find. **Recommend:** treat the missing Audit Summary as a defect in this specific build's paperwork, not the format's design - the format already asks for this information; it simply was not supplied. A future work order closing out Ashford Shop's acceptance (Finding 1) should require it retroactively as part of closing the loop.

### 4. No governance Decision Record exists for any Home Island map's acceptance. (Medium)

`studio/governance/decision-record-template.md` and `architectural-decision-log.md` exist and are well-formed, but zero entries reference Ashford Shop, Map001, or Map002 - despite `ashford-village-contract.md` itself flagging human certification as required before any of the three maps can be flipped to `locked`. **Recommend:** the same work order that closes Finding 1 should produce the first Decision Record of this kind, both to accept/reject Ashford Shop and to establish the precedent for Map001/Map002's still-outstanding certification.

## Findings: Information Duplicated

### 5. Creative Authority and Implementation Packet requirements are restated, not cited, across multiple documents. (Low)

`ashford-shop-build-contract.md` and (retroactively) `ashford-shop-pattern-aware-contract.md` both reproduce `IMP-HOM-019`'s nine acceptance criteria in full, following the existing "point, don't paraphrase... except for acceptance criteria" convention already established in `WO-0020`. This is intentional duplication, already justified by precedent, and did not cause any observed problem - listed here for completeness, not as a defect. **No action recommended.**

### 6. The map's build history is scattered across three repositories with no single index. (Medium)

Reconstructing Stage 5's three-pass history (`rpgmakerLSP` blueprint generation, `rpgmakerLSP` decoration passes, `TheLastSwordProtocol-Game` hand-polish) required cross-referencing git logs in two separate repositories plus reading the target file's own embedded `note` field, because no single document lists "here is everything that has happened to Map003, in order." **Recommend:** a lightweight per-map production log convention (could be as simple as a running section in the map's own ownership ledger entry, or a `reports/production-review/` per-map file) that future work orders append to rather than requiring git archaeology to reconstruct.

## Findings: An Implementation Agent Had to Guess

### 7. The final build pass had no visible contract to execute against, and its author is not identified. (High)

Per Stage 4 and Stage 5 of the production review: the final `Map003.json` cites `IMP-HOM-019` directly, not `ashford-shop-build-contract.md`. Either the implementing agent read the Atlas packet directly and produced excellent work without the AtlasStudio contract layer's help, or the contract was consulted but left no citation trail. This review cannot distinguish the two from the artifact alone, which is itself the finding: **the contract layer's actual influence on a real build is currently unverifiable.** **Recommend:** require every implementation artifact's embedded comments (or an accompanying Audit Summary) to name the specific AtlasStudio contract it executed, not only the Atlas packet - this is a small, additive convention, not a new system.

## Findings: A Human Had to Interpret Intent

### 8. "hand_authored" and "accepted" are conflated in the ownership ledger. (High)

Per Stage 6: `map_ownership.json` presents Map003 as settled, `hand_authored` content. Only the artifact's own `note` field reveals it is not yet accepted. A reader who trusts the ledger alone - which is exactly what `AGENTS.md` tells every agent to do - would reasonably conclude the map is finished when it is not. **Recommend:** either a documented convention that `hand_authored` maps must carry an explicit acceptance-status note (formalizing what this build already happened to do informally), or a fourth ledger state between `hand_authored` and `locked` for "hand-authored, pending certification." This is a real gap in `bridges/rpg-maker-mz/ownership-model.md`'s state model, not just a one-off oversight - the model's five states (`generated`, `agent-drafted`, `human-edited`, `hand-authored`, `locked`) have no state that means "a human/guided pass is complete and awaiting sign-off," which is exactly Ashford Shop's actual current status.

## Findings: The Pipeline Produced Ambiguity

### 9. "First full production cycle using the new architecture" is not what actually happened. (Critical, addressed by this review's own framing)

This work order's own Objective states a premise this review found to be inaccurate: the pattern library and pattern-aware contract format postdate the actual build by several days. This is not a defect in any single document - it is a natural consequence of work orders being planned and executed in a fast-moving sequence - but it means any future reader citing "the Ashford Shop production cycle" as evidence that the new architecture works in practice would be citing evidence that does not exist yet. **Recommend:** the next screen built after this review (not a retroactive one) should be the actual first full-architecture production cycle, and should be tracked as such explicitly from its own first work order, so this ambiguity does not recur.

### 10. The Work Order Router and Agent Scheduler have design and test coverage but no production usage history. (Medium)

`reports/atlas-router/routing-log.jsonl` contains twelve entries; all twelve match the exact example invocations from `WO-0023`'s own Verification Steps (`"Write shopkeeper dialogue"`, `"Implement IMP-HOM-019"`, `"Create a graph diff tool"`) - self-test traffic, not a real routing decision for a real request. `studio/scheduling/` contains only a design document and one example JSON file, with no corresponding usage log. Neither tool has been exercised against a genuine production request yet, which this review's Background list ("Router," "Scheduler") asked it to check. **Recommend:** no new work order specifically for this - it is naturally resolved the same way as Finding 9, by routing the *next* real request through the router instead of around it, and observing whether it holds up.

## Findings: The Pipeline Prevented Mistakes

These are successes, recorded with the same rigor as the failures above, because a retrospective that only lists problems is as misleading as one that only lists successes.

### 11. The ownership ledger prevented every regeneration-over-hand-work failure mode it exists to prevent. (Success - Confirms model is sound)

Across the entire Home Island map set, including the two automated "landmark decoration" passes that touched Map003 while other maps were also mid-pipeline, this review found zero instances of a pipeline script writing to a `hand_authored` or `locked` map. The ledger's fail-safe design worked exactly as `bridges/rpg-maker-mz/ownership-model.md` and `AGENTS.md` specify. **No action needed - this is working. Do not weaken it while addressing Finding 8.**

### 12. The two Atlas-side open questions (antidote stocking, post-Node-Seven inventory) were never silently resolved by an implementing agent. (Success)

Both `IMP-HOM-019` and every downstream artifact this review inspected leave these two questions genuinely open, exactly as `ashford-shop-build-contract.md` Section 5 requires. This is a real, checkable instance of a contract's explicit "must not resolve" boundary holding under actual implementation pressure. **No action needed.**

### 13. `BUILD-0043`'s runtime review correctly blocked automatic final map construction before it could produce a low-quality Ashford Shop. (Success)

The "NO GO for automatic final map construction" verdict, based on real playtest evidence, is exactly why Ashford Shop went through a genuine hand-build pass instead of shipping the `BUILD-0025` auto-generated placeholder as final. This is the pipeline's playtest-feedback loop working as designed, even though (per Finding 1) it has not yet closed the loop for this specific artifact. **No action needed on the mechanism itself; see Finding 1 for the specific artifact.**

## Priority Summary

| # | Finding | Priority |
|---|---|---|
| 1 | No human playtest record for Ashford Shop | Critical |
| 2 | No automated validation of the final build | Critical |
| 9 | "First full production cycle" premise is inaccurate | Critical (framing, addressed by this review) |
| 3 | No implementing-agent attribution / Audit Summary | High |
| 7 | Final build's contract citation is unverifiable | High |
| 8 | `hand_authored` conflates "done" with "accepted" | High |
| 4 | No governance Decision Record for any Home Island map | Medium |
| 6 | Build history scattered across three repositories | Medium |
| 10 | Router and Scheduler have no production usage history | Medium |
| 5 | Acceptance-criteria duplication (intentional, precedented) | Low |
| 11 | Ownership ledger held correctly throughout | Success |
| 12 | Open questions never silently resolved | Success |
| 13 | Runtime review correctly blocked low-quality auto-generation | Success |

See `lessons-learned.md` for the narrative synthesis of these findings and `studio/governance/production-readiness.md` for how they roll up into a go/no-go assessment and prioritized backlog.
