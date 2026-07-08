# Pattern Resolution Rules

## Purpose

`PATTERN_INHERITANCE_MODEL.md` defines the hierarchy patterns live in. This document defines the procedure for turning a citation of that hierarchy - an Environment layer, a Specialization layer, and optionally a Project-specific layer, as named in a citing implementation contract - into one resolved set of implementation guidance. Two agents resolving the same citation must reach the same resolved guidance; this document is what makes that deterministic rather than a matter of individual judgment.

## The Resolution Pipeline

Given a citation naming a chain of patterns from most general to most specific (for example: Environment `Interior`, Specialization `Item Shop`, Project `Ashford Village`), resolution proceeds in five steps:

1. **Walk the chain.** Starting from the most specific named layer, follow `parent_pattern` links upward until reaching a layer with no parent (a category-tier root) or an explicitly virtual layer (see `PATTERN_INHERITANCE_MODEL.md`, "Materialized vs. Virtual Nodes"). This produces the ordered list of layers actually in play, general to specific.
2. **Collect each layer's local rules.** For each layer, take its `local_rules` (the rules stated in that pattern's own Layout/Composition/Passability/Event Rules sections that are not simply restatements of an inherited rule - see `schemas/design-pattern.schema.json`).
3. **Apply layers in order, general to specific.** Start with the most general layer's local rules as the base. For each more specific layer, add its local rules to the accumulated set. Where a more specific layer's local rule is marked as an explicit override of a named rule from a more general layer (per `PATTERN_INHERITANCE_MODEL.md`'s "Vertical override" relationship), the more specific rule replaces the one it names; it does not merely sit alongside it.
4. **Apply cross-branch clarifications, if cited.** If the citation also names a cross-branch clarification (per `PATTERN_INHERITANCE_MODEL.md`'s second relationship type - a pattern outside the direct ancestor chain stating that a rule does not apply), apply it after the vertical chain, and record which general rule it scopes away for this citation specifically. This is rarer than a vertical override and must be named explicitly in the citation - it is never inferred.
5. **Report the resolved set with per-layer provenance.** The output is not a single flattened list with the layers forgotten - every rule in the resolved guidance keeps a record of which layer it came from, so a build report or reviewer can trace any specific requirement back to its source pattern and that pattern's own confidence and evidence.

## Precedence

More specific beats more general, **only when an explicit override or clarification is stated.** Precedence is not "the most specific layer always wins on every point" - it is "every layer's rules apply unless a more specific layer explicitly names and replaces one of them." A Specialization layer that says nothing about doorway placement does not silently override its Category's doorway rule; it inherits it unchanged.

Ranked from lowest to highest precedence when an explicit conflict is declared:

1. Environment tier (lowest - broadest, most general).
2. Category tier.
3. Specialization tier.
4. Project-specific tier (highest - narrowest, most specific).

## Conflict Resolution

Three distinct situations can arise, and they are not resolved the same way:

- **Declared vertical override.** A child pattern explicitly names a parent rule it replaces and states why. Resolution: the child's version wins, per Precedence above. This is the normal, healthy case and requires no escalation.
- **Declared cross-branch clarification.** A pattern outside the ancestor chain explicitly states that a named rule from elsewhere does not apply to it (e.g. `bar.pattern.md` on `shop.pattern.md`'s wall-anchoring rule - see `PATTERN_INHERITANCE_MODEL.md`). Resolution: honor the clarification for citations of the clarifying pattern; the original rule remains fully in force for citations that do not include the clarifying pattern in their chain.
- **Undeclared contradiction.** Two patterns in the same citation chain state incompatible rules and neither one names the other as an override or clarification. **This is not resolved at citation time.** Per `PATTERN_INHERITANCE_MODEL.md`'s Override Behavior section, an undeclared contradiction is a review defect, not a resolution puzzle. Resolution must fail closed: stop, do not guess which rule wins, and route the contradiction back through `PATTERN_REVIEW_PROCESS.md` before the citation can be used. This mirrors `studio/orchestration/work-order-router.md`'s "ambiguous requests stop and request classification" rule (`WO-0021`) - AtlasStudio's tooling does not silently pick a winner when its own source documents disagree.

A fourth situation - **sibling-vs-sibling citation without a chosen specialization** (for example, a contract that names both `Shop` and `Bar` for the same build without picking one) - is also a fail-closed case, but for a different reason: it is not a rule conflict, it is an ambiguous request. A build must resolve to exactly one path down the tree per environment; citing two unrelated category-tier siblings for the same physical space is a request-shaping error to fix before resolution runs, not something resolution should paper over by merging both.

## Overrides

An override is only valid when it is explicit. Per `PATTERN_INHERITANCE_MODEL.md`, this means:

- The overriding pattern names the exact rule being replaced (quoting or closely paraphrasing the parent's own wording), not just describing a difference in outcome.
- The overriding pattern states why - the evidence or reasoning that justifies deviating from the inherited default.
- The override is scoped to the overriding pattern and its own descendants only. It does not retroactively change what the parent rule means for the parent pattern itself or for the parent's other children. `weapon-shop.pattern.md` deviating from a future `shop.pattern.md` rule (if one is ever added) would not change what that rule means for `armor-shop.pattern.md`.

An override recorded in a pattern's `exceptions` field (`schemas/design-pattern.schema.json`) is the machine-checkable anchor for this requirement - a future Pattern Validator (see "Future Integration" below) can confirm every entry in `exceptions` names a real ancestor rule and isn't dangling.

## Exceptions

Separately from overrides, a pattern's `Required Conditions` (prose) / `applicable_conditions` (schema field) act as gating exceptions during resolution, not partial-application points:

- If the physical space a contract describes does not satisfy a layer's `applicable_conditions`, that layer is **skipped entirely** in resolution - its rules do not partially apply. A multi-room shop-plus-back-office building does not get `shop.pattern.md`'s single-room rules "half-applied"; the pattern simply does not resolve for that space, and the citation must either choose a different pattern or explicitly document why the mismatch is acceptable for this one build (a project-specific exception, recorded at the Project-specific tier).
- A citation that knowingly proceeds despite an unmet condition must record the deviation as a project-specific exception, not silently ignore the mismatch. This keeps `PATTERN_REVIEW_PROCESS.md`'s "every override and exception must be explicit" discipline intact even for one-off, project-specific breaks from a pattern's stated conditions.

## Confidence Interactions

Confidence values from different layers are **never merged, averaged, or reduced to a single number.** Each layer keeps and reports its own confidence, per `PATTERN_CONFIDENCE_MODEL.md`, which already defines confidence per pattern document, not per resolved guidance. Resolution therefore reports confidence as a **per-layer sequence**, matching `PATTERN_APPLICATION_GUIDE.md`'s citation format (for example, `High / Medium / High` for an Environment / Specialization / Project-specific chain).

This matters because a resolved guidance's overall trustworthiness is not one fact - different rules within it come from different layers with different evidentiary strength:

- A rule inherited from a **High**-confidence layer should be treated as safe to apply without further justification, even if a more specific layer in the same chain is only **Medium** or **Low**.
- A rule stated locally at a **Medium**-confidence layer (single-source, per `PATTERN_CONFIDENCE_MODEL.md`) should be flagged as such in any build report that applies it, exactly as `shop.pattern.md`'s own Common Mistakes section already requires for citations of itself alone.
- A **Low**-confidence Project-specific layer (the common case, since project preferences are typically not sample-derived) does not weaken the Environment or Specialization layers beneath it - it simply means the project-specific additions or overrides carry less independent weight than the reusable layers they sit on top of.
- Citing a **virtual** layer (see `PATTERN_INHERITANCE_MODEL.md`) requires stating where that layer's confidence claim comes from, since no dedicated pattern document backs it yet. For the `Interior` environment tier specifically, that source is `reports/design-patterns/interior-pattern-corpus-review.md`'s recurring-findings sections, and the confidence value cited for that layer must be justified against that report's actual corroboration count (per `PATTERN_CONFIDENCE_MODEL.md`'s ordinary bars), not asserted freely.

`evidence_count` (`schemas/design-pattern.schema.json`) exists specifically to make this checkable: a future Pattern Validator can confirm a cited confidence level is consistent with the stated `evidence_count` for that layer, without a human having to re-derive it from prose each time.

## Worked Summary

Given a citation chain `[Environment: Interior] -> [Specialization: Item Shop] -> [Project: Ashford Village]`:

1. Walk the chain: `Interior` (virtual, evidence via the corpus review) -> `Shop` (`shop.pattern.md`, since `Item Shop` currently collapses onto it - see `PATTERN_INHERITANCE_MODEL.md`) -> `Ashford Village` (hypothetical, illustrative only - no such pattern exists yet).
2. Collect local rules at each layer.
3. Apply general-to-specific, honoring any explicit override the Ashford Village layer states.
4. Apply any cited cross-branch clarification (none in this example).
5. Report the resolved rule set with, for each rule, which of the three layers it came from and that layer's own confidence.

`reports/design-patterns/inheritance-examples.md` works through this and several other chains in full, including one entirely within the currently-materialized part of the library (`Shop -> Weapon Shop`, no hypothetical layers required).

## Future Integration

See `PATTERN_INHERITANCE_MODEL.md` and `PATTERN_APPLICATION_GUIDE.md` for the full discussion of how Implementation Contracts, a future Pattern Validator, and a future Pattern Extraction Engine should consume this document; in short, a Pattern Validator's core job is to run Steps 1-5 above mechanically and flag any undeclared contradiction or unjustified confidence claim it finds along the way, rather than requiring a human to trace `parent_pattern` chains and evidence counts by hand.

## References

- `studio/design-patterns/PATTERN_INHERITANCE_MODEL.md` - the hierarchy this document resolves citations against.
- `studio/design-patterns/PATTERN_CONFIDENCE_MODEL.md` - the per-pattern confidence definitions this document treats as immutable per layer.
- `studio/design-patterns/PATTERN_REVIEW_PROCESS.md` - where undeclared contradictions and exceptions must be routed instead of resolved silently.
- `studio/design-patterns/PATTERN_APPLICATION_GUIDE.md` - the citation format implementation contracts use to invoke this resolution procedure.
- `schemas/design-pattern.schema.json` - the machine-checkable fields (`parent_pattern`, `exceptions`, `applicable_conditions`, `inherited_rules`, `local_rules`, `evidence_count`) this procedure operates on.
- `studio/orchestration/work-order-router.md` (`WO-0021`) - precedent for AtlasStudio's "fail closed on ambiguity, do not silently guess" discipline, reused here for undeclared contradictions.
- `reports/design-patterns/inheritance-examples.md` - full worked examples of this resolution procedure.
- Created by `work-orders/WO-0026-design-pattern-inheritance-model.md`.
