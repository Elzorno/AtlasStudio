---
work_order_id: WO-0027
title: Pattern-Aware Implementation Contracts
status: submitted
project: atlasstudio
recommended_agent: claude-code
agent_role: senior-software-architect
risk_level: low
player_facing: false
engine_specific: true
required_capabilities:
  - architecture-review
  - documentation
preferred_capabilities:
  - qa-review
produces:
  - contracts.pattern_contract_spec
  - contracts.pattern_application_checklist
  - report.ashford_shop_pattern_aware_contract
created: 2026-07-08
---

# WO-0027 - Pattern-Aware Implementation Contracts

## Purpose

AtlasStudio now has a Design Pattern Library (`WO-0024`, `WO-0025`), a Pattern Inheritance Model, and Pattern Resolution Rules (`WO-0026`) - but every implementation contract produced so far (`WO-0020`) was written before any of that existed, and consumes only Atlas canon and Atlas implementation packets. This work order upgrades the implementation contract system itself: it defines the next-generation, pattern-aware contract format, a companion application checklist, and demonstrates the format with one worked example against the Ashford Shop - without touching any real contract, any real Atlas file, or any real Game file.

This is a documentation and architecture work order. It does not authorize or perform any implementation work.

## Player-Facing Goal

Indirect. A pattern-aware contract format lets future builds combine Atlas's authoritative narrative/technical decisions with AtlasStudio's accumulated, evidence-graded craft knowledge in one deterministic, traceable document - reducing the chance that an implementing agent either reinvents layout conventions the library already corroborated, or (worse) treats a general pattern as if it silently outranked a specific Atlas decision. This work order itself ships no player-visible content and modifies no game file.

## Background

Review: `work-orders/WO-0020-ashford-village-implementation-contract-from-atlas-handoff.md`, `WO-0024-design-pattern-library.md`, `WO-0025-interior-pattern-corpus.md`, `WO-0026-design-pattern-inheritance-model.md`.

Review: `studio/design-patterns/README.md`, `PATTERN_SCHEMA.md`, `PATTERN_INHERITANCE_MODEL.md`, `PATTERN_RESOLUTION_RULES.md`, `PATTERN_APPLICATION_GUIDE.md`, `PATTERN_CONFIDENCE_MODEL.md`.

Review of the existing implementation contract system: `reports/implementation-contracts/ashford-village-contract.md` (parent contract) and `ashford-shop-build-contract.md` (child build contract), plus the RPG Maker bridge conventions they already follow (`bridges/rpg-maker-mz/handoff-format.md`, `ownership-model.md`, `passability-rule.md`) and the underlying Atlas packet those contracts execute (`IMP-HOM-019`, `atlas/docs/09_Technical/Implementation_Packets/Home_Island/IMP_HOM_019_Manual_Map_Build_Ashford_Shop.md`).

`WO-0020`'s contracts already establish good discipline - exact authoritative sources, exact Game repo targets, ownership-ledger-derived write eligibility, passability requirements, testable acceptance criteria, "point, don't paraphrase" citation of packets. What they have no format for is citing a *pattern* alongside those sources, distinguishing pattern-derived guidance from Atlas-authoritative requirements, or reporting a pattern's confidence separately from the packet's own (unconditional) authority. `WO-0026`'s `PATTERN_RESOLUTION_RULES.md` defines how pattern layers alone combine; this work order extends that into the contract format itself, bracketing the pattern chain with Creative Authority above it and the Implementation Packet as its highest-precedence layer.

## Scope

### In Scope

- Defining the next-generation implementation contract format: section list, section order, and section definitions, extending (not replacing) the structure `WO-0020`'s contracts already use (`studio/contracts/PATTERN_CONTRACT_SPEC.md`).
- Defining exactly how Creative Authority, Environment Pattern, Specialization Pattern, Project Pattern, and Implementation Packet combine into Final Implementation Guidance, using the inheritance model from `WO-0026`.
- Producing a reusable checklist for implementation agents applying this format (`studio/contracts/PATTERN_APPLICATION_CHECKLIST.md`).
- Producing one demonstration contract against the Ashford Shop, showing the format applied to a real, already-contracted build, clearly marked as illustrative and non-authorizing (`reports/implementation-contracts/ashford-shop-pattern-aware-contract.md`).
- Describing how future contracts, a future Pattern Validator, and the existing Work Order Router should consume this format.

### Out of Scope

- Modifying `TheLastSwordProtocol-Atlas` in any way.
- Modifying `TheLastSwordProtocol-Game` in any way.
- Modifying any existing implementation contract (`ashford-village-contract.md`, `ashford-shop-build-contract.md`, `ashford-dialogue-application-contract.md`, `ashford-existing-map-verification-contract.md`) - all four remain byte-for-byte as `WO-0020` left them.
- Replacing or superseding `ashford-shop-build-contract.md` as the authoritative contract for Map003 - the demonstration contract this work order produces is explicitly non-authorizing.
- Promoting any pattern's confidence value, including `shop.pattern.md`'s Medium-to-High recommendation from `WO-0025`'s corpus review, which this work order cites accurately but does not apply.
- Inventing evidence for any pattern layer - every confidence value cited anywhere in this work order's deliverables matches an existing pattern document's actual current frontmatter, or is explicitly marked as not-yet-existing (the Ashford Village Project Pattern layer).
- Modifying the Design Pattern Library itself (`studio/design-patterns/`) - this work order builds a consumer of that library, not a change to it.
- Building the Pattern Validator named in "Future Integration" - named and scoped, not implemented.
- Writing or modifying any code.

## Inputs

- `work-orders/WO-0020-ashford-village-implementation-contract-from-atlas-handoff.md`, `WO-0024-design-pattern-library.md`, `WO-0025-interior-pattern-corpus.md`, `WO-0026-design-pattern-inheritance-model.md`.
- `studio/design-patterns/README.md`, `PATTERN_SCHEMA.md`, `PATTERN_INHERITANCE_MODEL.md`, `PATTERN_RESOLUTION_RULES.md`, `PATTERN_APPLICATION_GUIDE.md`, `PATTERN_CONFIDENCE_MODEL.md`, `interiors/shop.pattern.md`.
- `reports/design-patterns/interior-pattern-corpus-review.md`, `inheritance-examples.md`.
- `reports/implementation-contracts/ashford-village-contract.md`, `ashford-shop-build-contract.md` (read-only, comparison baseline).
- `atlas/docs/09_Technical/Implementation_Packets/Home_Island/IMP_HOM_019_Manual_Map_Build_Ashford_Shop.md` (`TheLastSwordProtocol-Atlas`, read-only).
- `bridges/rpg-maker-mz/handoff-format.md`, `ownership-model.md`, `passability-rule.md`.

## Deliverables

- `studio/contracts/PATTERN_CONTRACT_SPEC.md`
- `studio/contracts/PATTERN_APPLICATION_CHECKLIST.md`
- `reports/implementation-contracts/ashford-shop-pattern-aware-contract.md`
- `work-orders/WO-0027-pattern-aware-implementation-contracts.md`

## Acceptance Criteria

- `PATTERN_CONTRACT_SPEC.md` specifies exactly thirteen sections in order: `Project`, `Implementation Target`, `Creative Authority`, `Implementation Packet`, `Environment Pattern`, `Specialization Pattern`, `Project Pattern`, `Pattern Resolution`, `Implementation Guidance`, `Passability Rules`, `Validation Requirements`, `Acceptance Criteria`, `References`.
- `PATTERN_CONTRACT_SPEC.md`'s `Pattern Resolution` section describes an assembly order matching `Creative Authority -> Environment Pattern -> Specialization Pattern -> Project Pattern -> Implementation Packet -> Final Implementation Guidance`, states this as increasing precedence (not merely a flat sequence), and explicitly reconciles this with `studio/design-patterns/PATTERN_RESOLUTION_RULES.md`'s pattern-only resolution procedure rather than contradicting it.
- `PATTERN_CONTRACT_SPEC.md` requires `Implementation Guidance` to separate Authoritative requirements, Pattern-derived guidance, and Implementation recommendations into three distinct, labeled categories.
- `PATTERN_CONTRACT_SPEC.md` states that this format uses `studio/design-patterns/PATTERN_CONFIDENCE_MODEL.md` exactly as written, with no new confidence tier and no unilateral promotion by a citing contract.
- `PATTERN_CONTRACT_SPEC.md` includes a "Future Integration" section describing how future implementation contracts, the Pattern Library, Pattern Inheritance, Pattern Resolution, a future Pattern Validator, and the existing Work Order Router (`tools/atlas_router/`) should interact.
- `PATTERN_APPLICATION_CHECKLIST.md` includes, at minimum, every checklist item named in this work order's brief (creative authority identified, implementation packet identified, required patterns resolved, pattern conflicts checked, exceptions documented, passability reviewed, pattern confidence recorded, validation plan defined, acceptance criteria confirmed), each tied to the specific `PATTERN_CONTRACT_SPEC.md` section or pattern-framework document it verifies.
- `ashford-shop-pattern-aware-contract.md` carries a clear, prominent notice that it is a demonstration and does not replace or supersede `ashford-shop-build-contract.md`.
- `ashford-shop-pattern-aware-contract.md` cites `Environment Pattern: Interior`, `Specialization Pattern: Shop`, and states plainly that no `Project Pattern` for Ashford Village currently exists, per this work order's Success Criteria.
- `ashford-shop-pattern-aware-contract.md` cites `Implementation Packet: IMP-HOM-019` and separates Authoritative requirements, Pattern-derived guidance, and Implementation recommendations distinctly in its `Implementation Guidance` section.
- `ashford-shop-pattern-aware-contract.md` reports confidence separately per pattern layer (`Interior`: High, per the corpus review's 8/8 corroboration; `Shop`: Medium, matching `shop.pattern.md`'s actual current frontmatter unchanged; `Project Pattern`: not applicable, since the layer does not exist) - never merging them into one value.
- No existing implementation contract under `reports/implementation-contracts/` is modified.
- No pattern document's confidence value is modified anywhere in the library, including `shop.pattern.md`.
- No file under `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` is modified.
- Documentation only: no code is added or modified.
- The Immutable Formatting Rule is preserved: no existing file is reformatted.
- This work order is marked `submitted`.

## Verification Steps

```bash
find studio/contracts -name "PATTERN_CONTRACT_SPEC.md" -o -name "PATTERN_APPLICATION_CHECKLIST.md"
find reports/implementation-contracts -name "ashford-shop-pattern-aware-contract.md"
find work-orders -name "WO-0027-pattern-aware-implementation-contracts.md"
git diff --stat -- reports/implementation-contracts/ashford-village-contract.md reports/implementation-contracts/ashford-shop-build-contract.md reports/implementation-contracts/ashford-dialogue-application-contract.md reports/implementation-contracts/ashford-existing-map-verification-contract.md
# expect no output: no existing implementation contract is modified
git diff --stat -- studio/design-patterns
# expect no output: no pattern document is modified, including confidence values
grep -c "confidence: high" studio/design-patterns/interiors/shop.pattern.md
# expect 0: shop.pattern.md's confidence remains medium
python3 tools/atlas_format/format_guard.py --check
git -C ../TheLastSwordProtocol-Atlas status --porcelain
git -C ../TheLastSwordProtocol-Game status --porcelain
```

## Allowed Changes

- `studio/contracts/PATTERN_CONTRACT_SPEC.md`
- `studio/contracts/PATTERN_APPLICATION_CHECKLIST.md`
- `reports/implementation-contracts/ashford-shop-pattern-aware-contract.md`
- `work-orders/WO-0027-pattern-aware-implementation-contracts.md`

## Protected Areas

- Do not modify `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game`.
- Do not modify AtlasStudio canon.
- Do not modify any existing implementation contract under `reports/implementation-contracts/`.
- Do not modify any file under `studio/design-patterns/` - this work order consumes the pattern library, it does not change it.
- Do not promote, demote, or otherwise alter any pattern's confidence value.
- Do not invent evidence for any pattern citation.
- Do not write or modify code.
- Preserve the Immutable Formatting Rule.

## Notes for Assigned Agent

The central design decision this work order requires is reconciling `PATTERN_RESOLUTION_RULES.md`'s pure pattern-hierarchy precedence (Environment < Category < Specialization < Project-specific, most specific wins) with the brief's contract-level assembly order, which places `Implementation Packet` *after* `Project Pattern` and gives it the final say. Resolve this by treating Creative Authority and the Implementation Packet as sitting outside the pattern precedence chain entirely: Creative Authority is an unconditional validity boundary, and the Implementation Packet - though not itself a pattern - is Atlas's own concrete, already-approved technical decision for this one build, and so outranks every pattern layer's generic guidance wherever the two overlap. State this reasoning explicitly in `PATTERN_CONTRACT_SPEC.md` rather than leaving the brief's ordering unexplained.

The demonstration contract is the highest-risk deliverable for accidentally implying authorization it doesn't have. Put the non-authorizing notice at the very top, before any content, and cross-reference the real `ashford-shop-build-contract.md` by name wherever the two documents' content overlaps, so a reader cannot mistake this for a second, competing build authorization for the same map.

## Submission Record

Submitted 2026-07-08 by Claude Code.

Delivered:

- `studio/contracts/PATTERN_CONTRACT_SPEC.md` - the thirteen-section format, a mapping table showing how each existing `WO-0020` contract concept maps onto the new sections, the `Pattern Resolution` procedure explaining precisely why `Implementation Packet` outranks every pattern layer while `Creative Authority` sits outside the precedence chain as a validity boundary, a `Confidence Model` section reusing `PATTERN_CONFIDENCE_MODEL.md` exactly, and a `Future Integration` section covering Implementation Contracts, the Pattern Library, Pattern Inheritance, Pattern Resolution, a future Pattern Validator, and the Work Order Router.
- `studio/contracts/PATTERN_APPLICATION_CHECKLIST.md` - every checklist item named in the brief, each tied to a specific governing document, plus three additional items specific to this format (the three-way `Implementation Guidance` split, current ledger state, and no-existing-contract-modified), and explicit guidance that the checklist is a gate, not a formality.
- `reports/implementation-contracts/ashford-shop-pattern-aware-contract.md` - a full thirteen-section demonstration contract against the real Ashford Shop build, carrying a prominent non-authorizing notice at the top and cross-referencing `ashford-shop-build-contract.md` throughout. Cites `Environment Pattern: Interior` (virtual, High confidence per the corpus review's 8/8 corroboration), `Specialization Pattern: Shop` (`shop.pattern.md` v1.0, Medium confidence, unpromoted), and states plainly that no Ashford Village Project Pattern exists yet. Separates `IMP-HOM-019`'s authoritative requirements from `Interior`/`Shop`-derived guidance from two softer implementation recommendations, and reports all three pattern-layer confidence values separately rather than merged.
- This work order, marked `submitted`.

No existing implementation contract was modified - confirmed directly (not present in this work order's diff). No pattern document was modified, and no pattern's confidence value was promoted, demoted, or otherwise altered - `shop.pattern.md` remains `confidence: medium`, confirmed directly. No file in `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` was modified - `IMP-HOM-019` was read-only reference material. No AtlasStudio canon file was modified. No code was written or modified.

Formatting: preserved existing house style; no existing file was reformatted. All deliverables are new files.

Verification performed:

```bash
find studio/contracts -name "PATTERN_CONTRACT_SPEC.md"
find studio/contracts -name "PATTERN_APPLICATION_CHECKLIST.md"
find reports/implementation-contracts -name "ashford-shop-pattern-aware-contract.md"
git diff --stat -- reports/implementation-contracts/ashford-village-contract.md reports/implementation-contracts/ashford-shop-build-contract.md reports/implementation-contracts/ashford-dialogue-application-contract.md reports/implementation-contracts/ashford-existing-map-verification-contract.md
git diff --stat -- studio/design-patterns
grep -c "confidence: high" studio/design-patterns/interiors/shop.pattern.md
git -C ../TheLastSwordProtocol-Atlas status --porcelain
git -C ../TheLastSwordProtocol-Game status --porcelain
```
