# Pattern Review Process

## Purpose

Patterns are standing production knowledge that implementation contracts will cite by name and version. That only works if the library's contents are trustworthy over time - which means changes to it need the same kind of accountable review path AtlasStudio already uses for canon and tooling changes, not silent edits. This document describes how a pattern is proposed, reviewed, accepted, deprecated, versioned, and referenced by implementation contracts.

## How Patterns Are Proposed

A pattern proposal originates from one of two paths:

1. **Extraction-driven.** An agent completes an official-sample-map extraction per `PATTERN_EXTRACTION_GUIDE.md`, producing an analysis report with a `Reusable Design Rules` (or equivalently named) section. The proposer then drafts a pattern document following `PATTERN_SCHEMA.md`, citing that report as `source_report`.
2. **Project-preference-driven.** A Production Director or work order records an explicit house-rule decision (e.g. via `studio/governance/decision-record-template.md`) that is not derived from official sample data. The proposer drafts the pattern at `confidence: low` per `PATTERN_CONFIDENCE_MODEL.md` and states the decision it comes from.

Either path produces a pattern document with `status: proposed` in frontmatter, filed in the appropriate `studio/design-patterns/<category>/` directory. A proposed pattern must satisfy every required section of `PATTERN_SCHEMA.md` before it can be reviewed - an incomplete draft is not eligible for review.

Proposing a pattern is done under a work order, the same way any other AtlasStudio standing-document change is (see `studio/work-order-format.md`). The work order's `Deliverables` should name the exact pattern file path.

## How Patterns Are Reviewed

Review checks three things, corresponding to the three ways a pattern can fail:

1. **Schema completeness.** Every section in `PATTERN_SCHEMA.md` is present and non-empty; frontmatter is valid; `observed_maps` and `source_report` actually exist and actually say what the pattern claims.
2. **Extraction discipline.** Per `PATTERN_EXTRACTION_GUIDE.md`, objective and subjective observations are distinguished, no coordinate from the source map is presented as a prescriptive instruction (`PATTERN_SCHEMA.md`, "Format Discipline"), and no rule outruns what the cited evidence actually supports.
3. **Confidence accuracy.** The `confidence` field matches what `PATTERN_CONFIDENCE_MODEL.md` says it should be given the evidence on file - a single-sample-map pattern claiming `high` fails review; a project-preference pattern claiming sample-map backing it does not have fails review.

A reviewer who is not the proposing agent should perform this check where feasible (matching the general AtlasStudio pattern of QA/review as a `preferred_capability` on documentation work orders - see `studio/agent-roles.md` and the `preferred_capabilities: [qa-review]` convention used in `WO-0020`-`WO-0023`). Where a second agent is not available, the proposing agent must explicitly self-certify against all three checks in the work order's submission record.

## How Patterns Are Accepted

A pattern moves from `status: proposed` to `status: accepted` when:

- All three review checks above pass.
- The work order that proposed it reaches `submitted` (or `accepted`, per `studio/work-order-format.md`'s status values) with the pattern file listed as a delivered artifact.
- No open contradiction exists with an already-accepted pattern in the same category and `applicable_genres` scope. If one is found, resolve it before acceptance - either by narrowing `Required Conditions` on one or both patterns so they no longer overlap, or by escalating to a Production Director decision if they are genuinely incompatible.

Acceptance is recorded by updating the pattern's own frontmatter (`status: accepted`, `last_reviewed` set) - not by a separate acceptance ledger. The pattern document is its own record.

## How Patterns Are Deprecated

A pattern is marked `status: deprecated` when:

- A build that correctly applied the pattern's rules failed its citing implementation contract's acceptance criteria, and the failure traces to the pattern's own rule rather than to an implementation error (see `PATTERN_CONFIDENCE_MODEL.md`, "Downward movement").
- A newer pattern in the same category and scope supersedes it (see "Versioning" below - this is usually a version bump on the same pattern, not a separate deprecation, unless the change is a full replacement of approach rather than a refinement).
- The `applicable_genres` or `required_conditions` it was written for no longer apply to any active AtlasStudio project.

Deprecation never deletes the file. A deprecated pattern remains in place with `status: deprecated`, a stated reason, and a pointer (via `References`, `PATTERN_SCHEMA.md`) to whatever superseded it, if anything did. Implementation contracts must not cite a deprecated pattern; if one is cited by an in-flight contract at the moment of deprecation, that contract's owner must be notified and the citation revisited before the contract proceeds.

## Versioning

Patterns use `MAJOR.MINOR` versioning in frontmatter (`PATTERN_SCHEMA.md`).

- **MINOR bump** (`1.0` to `1.1`): confidence-level changes, added `observed_maps` corroboration, clarified wording, added `Common Mistakes` entries, or narrowed `Required Conditions` that do not change how an already-compliant build would have been built.
- **MAJOR bump** (`1.0` to `2.0`): a change to `Layout Rules`, `Composition Rules`, `Passability Rules`, or `Event Rules` that would change what a compliant build looks like. A build made correctly under `v1.0` is not guaranteed to satisfy `v2.0`.
- Every version bump updates `last_reviewed` and goes through the same review path as a new proposal (schema completeness, extraction discipline, confidence accuracy), scoped to the changed sections.
- Old versions are not deleted from history - git history is the record of prior versions; the file itself always reflects the current version. A contract that cites an old version number (e.g. `Shop v1.0` after `v2.0` ships) is citing a stale pattern and should be updated to reference the current version, unless the work order has a specific reason to pin to the old one.

This mirrors the Immutable Formatting Rule's underlying goal (`studio/immutable-formatting-rule.md`): a version bump should make the meaningful change to the pattern obvious in the diff, not bury it in a full-document rewrite.

## How Patterns Are Referenced by Implementation Contracts

An implementation contract that wants to use a pattern must:

1. Cite it explicitly, by name and version, in the form shown in `README.md`'s "Future Integration" section (`Apply: <Pattern Name> v<version>` / `Confidence: <level>`).
2. State the confidence level as it currently reads in the pattern's frontmatter at the time the contract is written - not a level the contract author wishes it had.
3. Treat every `Required Condition`, `Layout Rule`, `Composition Rule`, `Passability Rule`, and `Common Mistake` in the cited pattern as binding unless the contract explicitly states an override and the reason for it, the same way `ashford-shop-build-contract.md` explicitly states its own deviations from `IMP-HOM-019` where they exist.
4. Not restate the pattern's rules inline at length - cite the file. This keeps the pattern the single source of truth and avoids the contract silently drifting out of sync with a later pattern version.

If no pattern exists yet for the kind of space a contract is building, the contract proceeds without one - the pattern library is additive guidance, not a blocking gate. A missing pattern is a signal for a future extraction/proposal work order, not a reason to stall an implementation contract that Atlas has already scoped.

## Relationship to Other AtlasStudio Review Processes

This process is deliberately parallel to, and does not replace, `work-orders/WO-0021`'s routing rules or `studio/governance/repository-authority.md`'s ownership boundaries. A pattern proposal or revision is always AtlasStudio-owned production knowledge (per `README.md`, "Relationship to AtlasStudio") and never routes to `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` - it has no canon content and modifies no game file.
