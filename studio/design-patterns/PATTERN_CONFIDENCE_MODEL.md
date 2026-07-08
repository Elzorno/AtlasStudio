# Pattern Confidence Model

## Purpose

Not every pattern deserves the same trust. A rule observed in five official RPG Maker sample maps is not the same kind of claim as a rule one AtlasStudio agent liked the look of once. The confidence model makes that difference explicit and machine/agent-checkable, so an implementing agent citing `Confidence: High` in a contract (see `README.md`, "Future Integration") knows exactly how much scrutiny that rule has actually survived - and so a reviewer can tell, at a glance, whether a pattern is safe to apply without further justification or needs a second look first.

## Confidence Levels

### High

**Definition:** Observed repeatedly, in more than one official RPG Maker sample map, with consistent results.

**What it means for use:** An implementing agent may apply a High-confidence pattern without additional justification. Deviating from a High-confidence rule requires an explicit, stated reason in the implementation contract.

**Bar to reach it:** At least two independent official sample maps corroborating the same rule, or one official sample map plus one AtlasStudio-accepted build that confirmed the rule in production (see "How Confidence Changes Over Time").

### Medium

**Definition:** Observed once, in a single official RPG Maker sample map, with no corroborating second source yet.

**What it means for use:** An implementing agent should apply a Medium-confidence pattern by default, but should flag in the build report which rules came from a single-source pattern, so a future reviewer knows where corroboration would be most valuable.

**Bar to reach it:** One official sample map extraction (per `PATTERN_EXTRACTION_GUIDE.md`) with a rule stated as a `Reusable Design Rule`. This is the starting confidence for any newly accepted pattern derived from a single map - see `interiors/shop.pattern.md`, which is filed at Medium precisely because it is derived from one sample map (`Map021`, the official Item Shop) with no second source yet. It is eligible for promotion to High the moment a second official sample map, or one accepted and playtested AtlasStudio build, corroborates its rules (see "How Confidence Changes Over Time" below).

### Low

**Definition:** Project preference. Not derived from official RPG Maker sample data at all - instead, a house rule AtlasStudio or a Production Director has adopted for `The Last Sword Protocol` specifically.

**What it means for use:** Usable, but an implementing agent must treat it as a project-specific override, not a general RPG Maker design truth. A Low-confidence pattern must state which project(s) it applies to and should never claim official-sample support it does not have.

**Bar to reach it:** A recorded decision (e.g. a Decision Record per `studio/governance/decision-record-template.md`, or an explicit statement in the work order that proposed the pattern) establishing the preference. No sample-map citation is required, but the absence of one must be stated, not implied.

### Experimental

**Definition:** Unverified idea. A hypothesis about what might work well, not yet checked against any official sample map or any accepted build.

**What it means for use:** Must not be applied to player-facing work without explicit sign-off in the citing contract. An Experimental pattern existing in the library is an invitation to test it, not an instruction to build with it.

**Bar to reach it:** Any proposal that has cleared the minimum bar to be filed at all (see `PATTERN_REVIEW_PROCESS.md`, "How Patterns Are Proposed") but has not yet been checked against source data.

## How Confidence Changes Over Time

Confidence is not static. It should be reassessed whenever new evidence appears, and the reassessment itself is a reviewable event under `PATTERN_REVIEW_PROCESS.md`.

**Upward movement:**

- Experimental to Low: a Production Director or work order formally adopts the idea as a project preference, even without sample-map corroboration.
- Experimental to Medium: the idea is checked against an official sample map and the map corroborates it.
- Medium to High: a second official sample map (or one accepted, playtested AtlasStudio build using the pattern) corroborates the same rule. Every corroborating map must be added to the pattern's `observed_maps` frontmatter field (`PATTERN_SCHEMA.md`).
- Low to High: this path requires *both* a formally adopted project preference *and* independent official-sample corroboration - a Low-confidence rule does not become High just because a team likes it more over time.

**Downward movement:**

- Any level to Deprecated-pending-review: a build using the pattern fails acceptance criteria (per the citing implementation contract) in a way traceable to the pattern's own rule, not to an unrelated implementation error.
- High to Medium: a second official sample map is found to contradict a previously corroborating one, and the contradiction cannot be resolved by narrowing `Required Conditions` (`PATTERN_SCHEMA.md`).
- Any level to Deprecated: see `PATTERN_REVIEW_PROCESS.md`, "Deprecated." Confidence demotion and deprecation are related but distinct - a pattern can be demoted and still remain `status: accepted` at a lower confidence, or it can be fully deprecated if the underlying rule is no longer sound at all.

**What does not change confidence:**

- Aesthetic disagreement alone, without a failed acceptance criterion or contradicting sample-map evidence, does not lower confidence. It is grounds for a *new* competing pattern proposal (see `PATTERN_REVIEW_PROCESS.md`), not a downgrade of the existing one.
- Time alone does not raise or lower confidence. A pattern sitting unused for a long period stays at its last-assessed level until new evidence arrives.

## Confidence and Category Interact

A pattern's confidence is scoped to its `applicable_genres` and `required_conditions` (`PATTERN_SCHEMA.md`). A High-confidence interior-shop pattern says nothing about confidence for exterior town squares - each pattern's confidence is independent, even within the same category directory, and must not be assumed to transfer.

## Recording Confidence Changes

Every confidence change must be recorded in the pattern document itself (update `confidence` in frontmatter, update the `Confidence` body section with the new justification and the corroborating or contradicting evidence, and update `last_reviewed`), and must go through the same review path as any other pattern change - see `PATTERN_REVIEW_PROCESS.md`.
