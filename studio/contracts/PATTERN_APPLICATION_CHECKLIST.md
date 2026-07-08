# Pattern Application Checklist

## Purpose

`PATTERN_CONTRACT_SPEC.md` defines the format a pattern-aware implementation contract takes. This checklist is what an implementing agent (or the contract author) actually works through, in order, to know the format has been applied correctly - a fast, concrete complement to that longer specification document. Use it when drafting a pattern-aware contract, and again before marking one accepted.

Each item below names what "done" means and which document governs the check. Check every item; do not skip one because it seems obvious for a small build - the checklist exists precisely because "obvious" is where undeclared contradictions and confidence over-claims slip through.

## The Checklist

```text
□ Creative authority identified
```
Every Atlas source this build must satisfy is named by exact path and canonical ID, per `PATTERN_CONTRACT_SPEC.md` Section 3 (`Creative Authority`). If any required element is still an open Atlas question (an unresolved design decision, not yet an Atlas-side answer), it is named as open here, not silently assumed either way.

```text
□ Implementation packet identified
```
The exact `IMP-*` packet this contract executes is named, or its absence is stated explicitly, per `PATTERN_CONTRACT_SPEC.md` Section 4. A contract with no packet is valid but should say so, not leave the section blank.

```text
□ Required patterns resolved
```
`Environment Pattern`, `Specialization Pattern`, and `Project Pattern` are each named (or explicitly marked not-yet-authored / virtual), per `PATTERN_CONTRACT_SPEC.md` Sections 5-7 and `studio/design-patterns/PATTERN_INHERITANCE_MODEL.md`. A virtual layer names exactly where its evidence lives instead of a document path.

```text
□ Pattern conflicts checked
```
Every rule pulled from more than one cited layer has been checked for contradiction, per `studio/design-patterns/PATTERN_RESOLUTION_RULES.md`'s "Conflict Resolution." A declared vertical override or cross-branch clarification is fine and expected; an *undeclared* contradiction between two cited layers is not - if one is found, resolution stops and the contradiction is routed to `PATTERN_REVIEW_PROCESS.md` before this contract proceeds, per that document's fail-closed rule.

```text
□ Exceptions documented
```
Every point where this contract deviates from a cited pattern's stated rule - because the Implementation Packet requires something different, because Creative Authority requires something different, or because the build genuinely doesn't meet a pattern's `Required Conditions` - is recorded explicitly in `Pattern Resolution` or `Implementation Guidance`, naming the rule and the reason, per `PATTERN_RESOLUTION_RULES.md`'s "Overrides" and "Exceptions." A silent deviation is a defect, not a valid contract.

```text
□ Passability reviewed
```
`Passability Rules` combines the Implementation Packet's collision/region/encounter requirements with the cited patterns' own Passability Rules sections, per `bridges/rpg-maker-mz/passability-rule.md`. Where they conflict, the packet's specific statement wins, per `PATTERN_CONTRACT_SPEC.md`'s "Pattern Resolution."

```text
□ Pattern confidence recorded
```
Every cited pattern layer's confidence is stated **separately**, matching that pattern's own current frontmatter (`studio/design-patterns/PATTERN_CONFIDENCE_MODEL.md`) - never merged into one number for the whole contract, per `PATTERN_RESOLUTION_RULES.md`'s "Confidence Interactions." If a cited pattern's confidence looks stale (the pattern has been revised since this contract was drafted), re-check the pattern document directly before finalizing.

```text
□ Validation plan defined
```
`Validation Requirements` states both automated checks (route validation, JSON inspection where applicable) and the human-playtest requirement `bridges/rpg-maker-mz/passability-rule.md` always requires in addition, per `PATTERN_CONTRACT_SPEC.md` Section 11.

```text
□ Acceptance criteria confirmed
```
Every line in `Acceptance Criteria` traces back to a specific statement in `Creative Authority`, `Implementation Packet`, or a cited pattern - none is invented independently by this contract, per `PATTERN_CONTRACT_SPEC.md` Section 12.

## Additional Items Specific to This Format

```text
□ Implementation Guidance is split into three labeled categories
```
Authoritative requirements, pattern-derived guidance, and implementation recommendations are visibly distinct - a reader should never have to guess which category a line of guidance belongs to, per `PATTERN_CONTRACT_SPEC.md` Section 9. This is the format's central new requirement and the item most likely to be done sloppily under time pressure; check it last, deliberately, after everything else.

```text
□ Ownership/ledger state is current
```
`Implementation Target`'s stated ownership state (`bridges/rpg-maker-mz/ownership-model.md`) was checked against the live ledger (`map_ownership.json` in the target repository) at drafting time, not assumed from a prior contract or memory - ledgers change as other work proceeds.

```text
□ No existing contract was modified or replaced
```
If this contract's subject overlaps an existing contract's scope, that existing contract is referenced, not edited or silently superseded. A pattern-aware contract that duplicates an existing contract's authority without saying so creates exactly the two-contracts-claiming-the-same-event risk `ashford-shop-build-contract.md` (Section 19 note) and `ashford-village-contract.md` (Section 6) already guard against.

## Using This Checklist

- Run it once while drafting, to catch missing sections early.
- Run it again immediately before a contract's status moves to a state that authorizes execution - the checklist is a gate, not just a drafting aid.
- A checklist item that cannot honestly be checked is not a formality to route around - it means the contract is not ready. Fix the underlying gap (missing citation, undeclared conflict, stale confidence) rather than checking the box regardless.

## References

- `studio/contracts/PATTERN_CONTRACT_SPEC.md` - the format this checklist verifies.
- `studio/design-patterns/PATTERN_RESOLUTION_RULES.md`, `PATTERN_REVIEW_PROCESS.md`, `PATTERN_CONFIDENCE_MODEL.md`, `PATTERN_INHERITANCE_MODEL.md`.
- `bridges/rpg-maker-mz/passability-rule.md`, `ownership-model.md`.
- `reports/implementation-contracts/ashford-shop-pattern-aware-contract.md` - a demonstration contract this checklist was run against.
- Created by `work-orders/WO-0027-pattern-aware-implementation-contracts.md`.
