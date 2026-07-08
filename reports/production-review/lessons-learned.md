# Lessons Learned

Status: submitted

Scope: `WO-0028`. Synthesizes `ashford-shop-production-review.md` and `pipeline-gap-analysis.md` into forward-looking practice. Where those two documents establish *what happened*, this document is about *what to do differently* - including a standing section, "AtlasStudio Before Journey I," describing the operational practices this review recommends for all future implementation work.

## What Worked Well

**Atlas's canon and technical-packet material was precise enough that nothing downstream had to guess.** Every requirement in `IMP-HOM-019` traced cleanly back to `SCR-HOM-ASH-003` and `ATLAS-STY-010`, and every artifact this review inspected honored that material without distortion. This is not a small thing - it is the foundation everything else in this review sits on, and it is worth stating plainly rather than taking for granted.

**The ownership ledger model held under real pressure.** Across the entire Home Island map set, through multiple automated passes and a ledger-state transition, no pipeline script wrote to protected content. This is the exact failure mode `bridges/rpg-maker-mz/ownership-model.md` exists to prevent, and it did not happen even once. A model that only works in the design document is not the same as a model that holds up in a messy, multi-repository, multi-pass real history - this one did.

**A human-driven playtest review (`BUILD-0043`) correctly stopped a worse outcome before it shipped.** The "NO GO for automatic final map construction" verdict, grounded in actual playtest evidence rather than a process rule invented in the abstract, is why Ashford Shop went through a genuine hand-build pass at all. The feedback loop from playtest to production decision worked, at least once, exactly as intended.

**The Design Pattern Library's confidence discipline held even when it was inconvenient.** `WO-0025`'s corpus review found strong evidence to promote `shop.pattern.md` from Medium to High confidence, and recommended it - but did not apply it, because the work order that found the evidence was not the work order authorized to act on it. `WO-0026` and `WO-0027` then both cited the unpromoted value faithfully, twice, across two more work orders, instead of quietly rounding up. This is a genuine, repeated demonstration that the "recommend, do not silently promote" discipline is not just a rule on paper.

## What Surprised Us

**The architecture was built after the artifact it was meant to validate.** This was not the expected shape of this retrospective. Going in, the natural assumption was that `WO-0024` through `WO-0027` had guided the Ashford Shop build and this review would assess how well that guidance worked. Instead, git history shows the opposite order: the shop was built, then the architecture that was supposed to have built it was designed. This is not a failure of the architecture - a pattern library extracted from official sample maps has no dependency on any one project's build order - but it does mean this review's real subject turned out to be "how did AtlasStudio's *older* systems (Atlas authority, the ownership ledger, `WO-0020`'s contract format) perform on their own," with the newer pattern/contract systems evaluated retroactively rather than in situ.

**A "finished-looking" artifact was not actually finished.** The final `Map003.json` reads, by inspection, like a completed, polished piece of work - real dialogue, working shop mechanics, correct collision, a well-written internal note. It would be easy to mistake it for done. It is not done; its own note says so. The surprise here is less about this one map and more about how easy it is for a good-looking artifact to be treated as accepted by omission, simply because nothing forced the question.

**The two tools built specifically to make future production safer - the Work Order Router and the Agent Scheduler - have never yet been asked to do their actual job.** Both are well-specified, and the router in particular has real automated test coverage. Neither has processed a genuine production request. This is not damning on its own (most tools start this way), but it means neither has been proven under real conditions yet, and this review should not be read as evidence that they have been.

## What Failed

**Traceability from the Game repository artifact back to the AtlasStudio contract that was supposed to govern it.** `ashford-shop-build-contract.md` exists, is well-formed, and correctly translates `IMP-HOM-019`. The final built map does not cite it. This is the review's clearest example of a document existing, being correct, and still not being verifiably connected to the work it was meant to govern.

**Closing the loop on acceptance.** Nothing in this production history failed loudly. Nothing broke. But the final, most important step - a human confirming the work is actually done - simply has not happened, and nothing in the pipeline as currently practiced forced it to happen before the map started looking, from a distance, like finished content.

## What Should Never Happen Again

- **A build should never be treated as complete by its ledger state alone.** `hand_authored` currently means "a human/guided pass has touched this," not "this is accepted." Conflating the two nearly happened in the course of writing this very review - the ledger alone would have said Ashford Shop was fine.
- **An implementation pass should never ship without an Audit Summary.** `bridges/rpg-maker-mz/handoff-format.md` already requires one. It was skipped here, and this review had to reconstruct the same information by hand, at higher cost and lower confidence than reading a submitted report would have taken.
- **A retrospective should never be allowed to quietly assume its own premise.** This review's brief stated, as background fact, that a "first full production cycle using the new architecture" had been completed. It had not. A retrospective that had not checked this directly would have produced a confident, well-organized, and wrong account of what happened.

## What Should Become Standard Practice

- **Every hand-build or polish pass records who (or what) did the work, under what request, and files an Audit Summary** - not as an aspiration in a bridge document, but as a checked item before a build is considered submitted.
- **Every implementation artifact cites the specific AtlasStudio contract it executed**, not only the Atlas packet, directly in its own comments - closing Finding 7 from `pipeline-gap-analysis.md` for every future build, not just this one.
- **Acceptance is a recorded decision, not an inferred state.** A Decision Record (`studio/governance/decision-record-template.md`) should exist for every map that moves toward `locked`, the same way one already should have existed - and did not - for Ashford Shop.
- **A retrospective checks its own premise against primary evidence before writing anything else.** This review's most useful early step was git archaeology, not reading the pattern library's own documentation about itself.

## AtlasStudio Before Journey I

This section describes the operational practices this review recommends be in place for every implementation work order from this point forward, ahead of Journey I's larger production push. It is written as standing guidance, not as a list of one-off fixes.

1. **Every new screen's implementation contract - pattern-aware or not - is the document an implementing agent actually opens first, and the built artifact says so.** If a future build again cites only the Atlas packet with no contract reference, treat that as a process gap to close before the build is accepted, not an acceptable shortcut.
2. **Every hand-build pass ends with a filled-out Audit Summary (`bridges/rpg-maker-mz/handoff-format.md`) and, where the ownership ledger changed, an explicit before/after state note**, per `ownership-model.md`'s Reporting Requirement. This is not new policy - both documents already ask for this. What changes is enforcement: a submission without one is incomplete, not merely under-documented.
3. **A map does not move toward `locked`, and is not described in any report as "complete," until a Decision Record exists recording a human acceptance or rejection.** Until the ownership model gains a dedicated in-progress-vs-accepted ledger state (`pipeline-gap-analysis.md`, Finding 8), the map's own embedded note is the interim mechanism for signaling this, and every hand-build pass should include one, the way Ashford Shop's final pass happened to.
4. **Automated validation is re-run against the artifact that will actually ship, not only against an earlier scaffold.** `pipeline-gap-analysis.md`'s Finding 2 exists because this did not happen for Ashford Shop; the tooling to do it already exists and already works.
5. **The Design Pattern Library's confidence discipline (recommend, never silently promote) is treated as load-bearing, not aspirational**, exactly as it held across `WO-0025` through `WO-0027`. Any future work order that finds grounds to change a pattern's confidence should record the recommendation and leave the change itself to a dedicated, visible action.
6. **The Work Order Router and Agent Scheduler are used on the next real request, not exercised only in their own test suites.** Their design and test coverage are sound; what they lack is production mileage, and that can only be gained by routing something real through them and watching what happens.
7. **A retrospective, whenever the next one is commissioned, starts by checking its own assumed premise against primary evidence** - git history, ledger state, and the artifact itself - before trusting any prior document's framing, including this one's.

## References

- `reports/production-review/ashford-shop-production-review.md`
- `reports/production-review/pipeline-gap-analysis.md`
- `studio/governance/production-readiness.md`
- `bridges/rpg-maker-mz/ownership-model.md`, `handoff-format.md`, `passability-rule.md`
- `studio/governance/decision-record-template.md`
- `studio/design-patterns/PATTERN_CONFIDENCE_MODEL.md`, `PATTERN_REVIEW_PROCESS.md`
- Created by `work-orders/WO-0028-production-pipeline-validation.md`
