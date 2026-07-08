# Pattern-Aware Implementation Contract Specification

## Purpose

Every implementation contract produced so far (`ashford-village-contract.md`, `ashford-shop-build-contract.md`, `ashford-dialogue-application-contract.md`, `ashford-existing-map-verification-contract.md`, all from `WO-0020`) is built entirely from Atlas canon and Atlas implementation packets. That is correct as far as it goes - Atlas is the sole creative authority (`studio/design-patterns/README.md`, "Relationship to Atlas") - but it means every contract re-derives layout and composition craft from scratch, or leaves it to the implementing agent's judgment, because nothing in the contract format has a place to cite reusable design knowledge. AtlasStudio now has that knowledge: the Design Pattern Library (`WO-0024`, `WO-0025`), its inheritance model (`WO-0026`), and a deterministic resolution procedure (`PATTERN_RESOLUTION_RULES.md`). This document defines the next-generation implementation contract format that consumes them.

This is a format specification. It does not itself replace any existing contract - see `reports/implementation-contracts/ashford-shop-pattern-aware-contract.md` for a demonstration built under this format, explicitly marked as an example rather than a live authorization.

## Relationship to the Existing Contract Format

The existing contracts (`WO-0020`) are not wrong; they simply predate the pattern library. Their structure - authoritative source table, exact Game repo targets, ownership restrictions, passability requirements, acceptance criteria, recommended agent - remains sound and is preserved here under renamed or folded sections (see the mapping table below). What this specification adds is three new sections (`Environment Pattern`, `Specialization Pattern`, `Project Pattern`) and a `Pattern Resolution` section that makes explicit how those layers combine with the Atlas-authoritative material the existing format already required.

| Existing contract concept | This specification |
|---|---|
| Authoritative Atlas Source Files table | `Creative Authority` |
| Exact Game Repo Targets table | `Implementation Target` |
| Build packet citation (e.g. `IMP-HOM-019`) | `Implementation Packet` |
| (none - new) | `Environment Pattern`, `Specialization Pattern`, `Project Pattern` |
| (none - new) | `Pattern Resolution` |
| Build Requirements / What May Be Modified | `Implementation Guidance` |
| Passability and Route Validation Requirements | `Passability Rules` |
| Verification Steps | `Validation Requirements` |
| Acceptance Criteria | `Acceptance Criteria` (unchanged in spirit) |
| Various citation lists | `References` |

Ownership-ledger state and modification boundaries (`bridges/rpg-maker-mz/ownership-model.md`) are not a separate section in this specification, unlike some existing contracts' standalone "What May Be Modified" section - they are folded into `Implementation Target`, since ownership state is a property of the target being identified, not a separate concern. A contract author who wants a more elaborate ownership breakdown may still add one; this specification defines the required minimum, not a ceiling.

## Section Order

A pattern-aware implementation contract contains the following sections, in this order:

1. `Project`
2. `Implementation Target`
3. `Creative Authority`
4. `Implementation Packet`
5. `Environment Pattern`
6. `Specialization Pattern`
7. `Project Pattern`
8. `Pattern Resolution`
9. `Implementation Guidance`
10. `Passability Rules`
11. `Validation Requirements`
12. `Acceptance Criteria`
13. `References`

## Section Definitions

### 1. Project

Which project this contract belongs to (e.g. `the-last-sword-protocol`), matching `studio/work-order-format.md`'s `project` frontmatter field. One line.

### 2. Implementation Target

The exact file(s) this contract concerns, by path - not a general area. State the current ownership/ledger state per `bridges/rpg-maker-mz/ownership-model.md` (e.g. `generated`, `hand_authored`, `locked`) as of the contract's writing, and cite where that state is authoritative (typically `map_ownership.json` in the target repository). If the target's ledger state does not permit the kind of work this contract describes, say so here rather than proceeding - this mirrors the existing contracts' practice of deriving write-eligibility from the ledger rather than asserting it independently (`ashford-shop-build-contract.md`, Section 3).

### 3. Creative Authority

The Atlas canon this build must satisfy - screen objects, dialogue packets, character bibles, quest specs, whatever narrative or world-design source applies. This is the ceiling every other section operates under: nothing in `Environment Pattern`, `Specialization Pattern`, `Project Pattern`, or even `Implementation Packet` may contradict what is stated here. Cite by exact path and, where applicable, canonical ID, matching the existing contracts' "Authoritative Atlas Source Files" convention.

### 4. Implementation Packet

The specific Atlas implementation packet (`IMP-*`) this contract executes, if one exists. An implementation packet is itself Atlas-authored, technical, and already-approved (see, for example, `IMP-HOM-019`'s own frontmatter: `canonical: true`, `owner: Technical Director`) - it is not a pattern, and it is not subordinate to one. State its exact path, and per `bridges/atlas/implementation-handoff.md`'s "point, don't paraphrase" convention, cite its concrete requirements rather than restating them at length here; a full reproduction belongs in `Implementation Guidance` or `Acceptance Criteria` where the existing contracts already do this (`ashford-shop-build-contract.md`, "Reproduced from IMP-HOM-019").

If no implementation packet exists yet for this build, say so explicitly - a contract may still cite pattern layers without one, though `Pattern Resolution`'s final step (see below) will then have nothing to layer on top of the pattern chain.

### 5. Environment Pattern

The Environment-tier pattern this build's location type belongs to (`interior`, `town`, `overworld`, `dungeon`), per `studio/design-patterns/PATTERN_INHERITANCE_MODEL.md`. State whether this layer is materialized (an actual `.pattern.md` file) or virtual (evidence exists, but no dedicated document yet - see that document's "Materialized vs. Virtual Nodes"). For a virtual layer, cite exactly where its evidence lives (typically `reports/design-patterns/interior-pattern-corpus-review.md`'s recurring-findings sections, for the `interior` environment). State this layer's confidence per `studio/design-patterns/PATTERN_CONFIDENCE_MODEL.md`.

### 6. Specialization Pattern

The Category- or Specialization-tier pattern that most specifically matches this build (e.g. `Shop`, `House`, `Weapon Shop`). Name the exact pattern document and version, state its `parent_pattern` per `PATTERN_INHERITANCE_MODEL.md`, and state its confidence. If the most specific existing pattern is a Category (not a further Specialization) - as is currently the case for `Shop`, whose `Item Shop` specialization has not been split out (`PATTERN_INHERITANCE_MODEL.md`, "The Shop / Item Shop Double Duty") - say so, rather than inventing a specialization document that does not exist.

### 7. Project Pattern

The Project-specific pattern layer, if one exists, per `PATTERN_INHERITANCE_MODEL.md`'s fourth tier (`studio/design-patterns/projects/<project-slug>/`). **Most contracts written today will find this layer does not exist yet.** State that plainly - "No Project Pattern currently exists for this location" - rather than fabricating one or leaving the section silently blank. This section existing with an honest "not yet authored" statement is itself useful: it tells a future pattern author exactly where a Project-specific pattern for this location would slot in.

### 8. Pattern Resolution

How `Creative Authority`, `Environment Pattern`, `Specialization Pattern`, `Project Pattern`, and `Implementation Packet` combine into the guidance actually given to the implementing agent. See "Pattern Resolution" below for the procedure every contract must follow here - this section states the *result* of applying that procedure to this specific contract's cited layers, not a restatement of the procedure itself (which lives in this document and in `PATTERN_RESOLUTION_RULES.md`).

### 9. Implementation Guidance

The assembled, resolved guidance itself, **explicitly separated into three categories**:

- **Authoritative requirements** - things Creative Authority or the Implementation Packet require. Non-negotiable; deviating requires an Atlas canon revision or a new packet, not an implementing agent's judgment call.
- **Pattern-derived guidance** - things the Environment, Specialization, or Project pattern layers state. Binding by default (per `PATTERN_RESOLUTION_RULES.md`'s ordinary precedence), but explicitly lower-precedence than an Authoritative requirement that conflicts with it, and revisable through the pattern review process (`PATTERN_REVIEW_PROCESS.md`) rather than through this one contract alone.
- **Implementation recommendations** - softer suggestions that follow from applying the above to this specific build, but that are not themselves stated as a rule by any cited authority or pattern. An implementing agent may deviate from a recommendation with a stated reason, more freely than from the first two categories.

This three-way separation is the format's central requirement, per this work order's brief: a reader must always be able to tell which category a given line of guidance belongs to.

### 10. Passability Rules

Grounded in `bridges/rpg-maker-mz/passability-rule.md`, combining whatever the Implementation Packet states about collision/regions/encounters with whatever the cited pattern layers' own Passability Rules sections add (per `PATTERN_SCHEMA.md`). Where the packet is silent, the pattern layers fill the gap; where they conflict, the packet wins (see "Pattern Resolution").

### 11. Validation Requirements

What must be checked before this contract's work is accepted - route validation (per `bridges/rpg-maker-mz/passability-rule.md`, "Route Validation"), any automated check available, and a note that automated inspection is necessary but not sufficient (a human playtest is still required, per that same document's "Human Playtest Still Required"). A pattern-aware contract should also require confirming that every pattern citation's stated confidence still matches the cited pattern document's actual current frontmatter at execution time - patterns can be revised between when a contract is written and when it is executed.

### 12. Acceptance Criteria

Concrete, testable conditions, drawn from the Implementation Packet where one exists (reproduced, not paraphrased, per existing practice) and supplemented by any pattern-derived criteria the `Implementation Guidance` section introduced. Every acceptance criterion should be traceable to a specific line in `Creative Authority`, `Implementation Packet`, or a cited pattern - not invented independently by this contract.

### 13. References

Every document this contract cites, grouped for clarity: Atlas sources, the implementation packet, pattern documents (with version), bridge documents, and any prior work order or contract this one builds on or supersedes.

## Pattern Resolution

This is the procedure every `Pattern Resolution` section must apply. It extends `studio/design-patterns/PATTERN_RESOLUTION_RULES.md`'s five-step pipeline (which governs how pattern layers alone combine) by adding Creative Authority and the Implementation Packet as the two non-pattern layers a contract must also account for.

```text
Creative Authority
    |
    v
Environment Pattern
    |
    v
Specialization Pattern
    |
    v
Project Pattern
    |
    v
Implementation Packet
    |
    v
Final Implementation Guidance
```

Read this diagram as an **assembly order with increasing precedence**, not a flat sequence of equally-weighted inputs:

1. **Creative Authority sits outside the precedence chain, as a validity boundary.** It is not "layer one of five, later overridden by later layers." Nothing assembled in steps below may contradict it. If a pattern or the packet appears to conflict with Creative Authority, Creative Authority wins, unconditionally, and the conflict is a defect in the pattern or packet to be corrected through its own review process - never resolved by quietly picking the pattern's answer.
2. **Environment Pattern is applied first among the pattern layers**, contributing the broadest, most reusable rules (per `PATTERN_RESOLUTION_RULES.md`'s Step 1-3, general-to-specific).
3. **Specialization Pattern is layered on top**, per the same inheritance procedure - it may add to or, if it explicitly says so, override a named Environment-tier rule.
4. **Project Pattern is layered on top of that**, if one exists - the narrowest pattern-tier layer, most often filed at Low confidence (`PATTERN_CONFIDENCE_MODEL.md`) since it is typically a project preference rather than sample-derived.
5. **Implementation Packet is applied last, above the entire pattern chain**, because it is not a pattern at all - it is Atlas's own concrete, already-approved technical specification for this exact build. Where the packet states a concrete requirement that a pattern layer only suggests generically (for example, a pattern's "keep the room compact" versus a packet's specific "~15x11 tiles recommended, do not enlarge beyond the 17x13 scaffold"), **the packet's specific statement wins**, and the pattern's generic guidance is understood as already satisfied by it, not as a second, competing requirement.
6. **Final Implementation Guidance** is the result: every rule from every layer that was not overridden by a higher-precedence layer, each retaining a record of which layer it came from (per `PATTERN_RESOLUTION_RULES.md`'s Step 5), split into the three `Implementation Guidance` categories defined above.

This ordering exists because a pattern - however well-corroborated - is general craft knowledge extracted from official sample maps or accumulated project experience. An implementation packet is a specific, Atlas-approved decision about *this* screen. General craft knowledge should fill gaps a specific decision leaves open; it should never override the specific decision itself. This is the same principle `studio/design-patterns/README.md`'s "Relationship to Atlas" already states for patterns versus canon, extended here to cover patterns versus the technical (not narrative) authority of an implementation packet.

Confidence is reported per layer throughout, exactly as `PATTERN_RESOLUTION_RULES.md`'s "Confidence Interactions" already requires - Creative Authority and the Implementation Packet are not pattern documents and do not carry a `PATTERN_CONFIDENCE_MODEL.md` confidence value at all; they are simply authoritative. Only the three pattern layers (`Environment Pattern`, `Specialization Pattern`, `Project Pattern`) report a confidence value, and those values are never merged into a single number for the whole contract.

## Confidence Model

This specification uses `studio/design-patterns/PATTERN_CONFIDENCE_MODEL.md` exactly as written - High, Medium, Low, Experimental, with the same promotion/demotion rules. A pattern-aware contract must not invent a new confidence tier, must not promote a cited pattern's confidence beyond what that pattern's own frontmatter currently states, and must not assert confidence for evidence the cited pattern does not actually have. If a contract author believes a pattern's confidence should change, that is a proposal to route through `PATTERN_REVIEW_PROCESS.md` on the pattern itself - not something a citing contract may adjust unilaterally.

## Future Integration

### Implementation Contracts

Once a Pattern Validator (below) exists, an implementing agent drafting a new pattern-aware contract should be able to name the `Environment Pattern` / `Specialization Pattern` / `Project Pattern` layers and have the tool populate `Pattern Resolution` and the pattern-derived portion of `Implementation Guidance` automatically, leaving the agent to supply only `Creative Authority`, `Implementation Packet`, and project-specific `Implementation Recommendations`. Until then, this specification is applied manually, the way `PATTERN_APPLICATION_GUIDE.md`'s citation format is applied manually today.

### Pattern Library

The Design Pattern Library (`studio/design-patterns/`) is the source every `Environment Pattern` and `Specialization Pattern` section cites. As the library grows (more interiors, then towns, overworlds, and dungeons per `PATTERN_INHERITANCE_MODEL.md`'s "Future Extensibility"), more contracts will have a materialized rather than virtual layer to cite, and citations should be updated to point at the newly materialized document rather than at its prior evidence-only source.

### Pattern Inheritance

`PATTERN_INHERITANCE_MODEL.md`'s hierarchy is what lets a contract's `Environment Pattern` and `Specialization Pattern` sections be filled in mechanically once a build's location type is known: the environment tier follows from the target's `category`, and the specialization follows from matching the target's `Required Conditions` / `applicable_conditions` against the library's existing patterns. A future tool could suggest both sections automatically from a target file path and a one-line description of the space.

### Pattern Resolution

`PATTERN_RESOLUTION_RULES.md`'s five-step pipeline, extended by this document's Creative-Authority-and-Packet bracketing, is designed to be executed identically by a human contract author today and by automated tooling later - the same rules, the same precedence, the same fail-closed behavior on undeclared contradictions. Nothing in this specification requires different resolution logic depending on who or what runs it.

### Pattern Validator (future tool, not built by this work order)

A future Pattern Validator, already named in `PATTERN_APPLICATION_GUIDE.md`'s "Future Integration," should additionally validate pattern-aware *contracts* (not just patterns): confirming every cited pattern's confidence in the contract matches that pattern's current frontmatter, confirming `Pattern Resolution`'s stated result is actually consistent with running the procedure in this document, and confirming `Implementation Guidance`'s three-way split does not misclassify a pattern-derived rule as an authoritative requirement or vice versa.

### Work Order Router

`tools/atlas_router/` (`WO-0021`-`WO-0023`) already classifies requests as `game_implementation` and routes them toward implementation contracts with `requires_explicit_approval`. A future router enhancement could, once a `game_implementation` request is classified, automatically look up the target's `category` and check the Design Pattern Library for a matching `Environment Pattern` / `Specialization Pattern` pair, pre-filling those two sections of a new pattern-aware contract before a human or agent drafts the rest - shortening the manual lookup this specification currently assumes a contract author performs by hand.

## References

- `studio/design-patterns/README.md`, `PATTERN_SCHEMA.md`, `PATTERN_INHERITANCE_MODEL.md`, `PATTERN_RESOLUTION_RULES.md`, `PATTERN_APPLICATION_GUIDE.md`, `PATTERN_CONFIDENCE_MODEL.md`, `PATTERN_REVIEW_PROCESS.md`.
- `studio/contracts/PATTERN_APPLICATION_CHECKLIST.md` - the companion checklist for applying this specification.
- `work-orders/WO-0020-ashford-village-implementation-contract-from-atlas-handoff.md` - the existing contract system this specification extends.
- `reports/implementation-contracts/ashford-shop-build-contract.md`, `ashford-village-contract.md` - existing contracts whose structure this specification's section mapping table is drawn from.
- `bridges/rpg-maker-mz/handoff-format.md`, `ownership-model.md`, `passability-rule.md`, `map-quality-standard.md`.
- `bridges/atlas/implementation-handoff.md` - source of the "point, don't paraphrase" convention this specification reuses for citing implementation packets.
- `reports/implementation-contracts/ashford-shop-pattern-aware-contract.md` - the demonstration contract built under this specification.
- Created by `work-orders/WO-0027-pattern-aware-implementation-contracts.md`.
