# Atlas Principles

## Purpose

`ATLAS_CORE_1.0.md` states the core philosophy as a short list of beliefs. This document explains why each belief exists, what it costs to violate it, and how to resolve the cases where two principles pull in different directions. It is the reference to consult when a work order's instructions are ambiguous and the constitution's summary isn't enough.

## The Principles, In Depth

### Planning should be explainable

The Planning Engine (`tools/atlas_planner/`) never returns a bare recommendation. Every score has named components - milestone impact, dependency value, technical debt, player value, core platform value - and evidence lines. This exists because a recommendation nobody can audit is indistinguishable from a guess, and guesses erode trust in the tooling faster than a wrong-but-explainable answer does.

**Why it matters:** the moment a human stops trusting the Planning Engine's output, they start ignoring it, and AtlasStudio degrades back into ad hoc prioritization.

**How to apply:** any new scoring or recommendation system (planning, orchestration, QA severity) must expose its components, not just its conclusion.

### Deterministic systems before opaque AI

The Validator, Canon Linter, Graph Diff Engine, and Immutable Formatting Guard are all plain scripts with explicit, reviewable rules - not model calls. This is deliberate: QA gates need to produce the same answer for the same input every time, and a rule set in `tools/atlas_lint/rules/canon_lint_rules.json` can be read, argued with, and amended by a human in a way an LLM's judgment cannot.

**Why it matters:** if the gate that decides whether canon is coherent is itself non-deterministic, two runs of the same check can disagree, and nobody can tell whether a failure is a real problem or noise.

**How to apply:** creative work (dialogue, story, scene pacing) is exactly where opaque AI reasoning belongs. QA and validation gates are exactly where it does not. When in doubt, ask: "would I be upset if this check gave a different answer tomorrow on unchanged input?" If yes, it needs to be deterministic.

### Human approval for canon

Agents may add draft nodes and edges under an approved work order. They may not promote draft facts to canon, retire canon, or resolve disputed canon without explicit human or AtlasStudio sign-off (`studio/atlas-graph/storage-model.md`, Edit Rules).

**Why it matters:** canon is the shared ground truth every other agent builds on. If it can drift silently, every downstream document and every other agent's context becomes unreliable at once.

**How to apply:** if implementation reveals that canon needs to change, stop and request a canon revision - do not patch around it quietly. This is the Canon Change Rule from `studio/workflow.md`, restated here because it is foundational, not incidental.

### Capabilities outlive providers

Work should be described by what it requires (`architecture-review`, `python-development`, `canon-design`, and so on - see `atlas-core/capabilities/README.md`), not by which named agent should do it. This principle itself has a history: WO-0012 originally shipped as a named-agent "Agent Scheduler," then was retired in place and replaced by capability-based orchestration once it became clear that hardcoding "Claude Code" or "Codex" into a work order ties the studio's workflow to whichever vendor happens to be available today. See ADR-0006 and ADR-0007 in the decision log.

**Why it matters:** providers change - quotas run out, better models ship, a local model becomes good enough for a task. A studio built around capabilities adapts; a studio built around named agents has to be re-planned every time the provider landscape shifts.

**How to apply:** new work orders should be interpretable in terms of required/preferred capabilities even before `required_capabilities` frontmatter is universally adopted. Suggested providers are a recommendation output, never a hardcoded requirement.

### Every asset has an owner

The engine bridge's ownership model (generated / agent-drafted / human-edited / hand-authored / locked) exists because not all content is equally safe to regenerate. A generated map can be rebuilt; a hand-authored one cannot be silently overwritten without losing real work.

**Why it matters:** the fastest way to destroy trust in multi-agent production is for an agent to overwrite something a human spent hours hand-crafting, because the tooling had no concept of "this is locked."

**How to apply:** unknown ownership defaults to protected, never to overwritable (`tools/rpg_maker_bridge/README.md`: "Unknown ownership is treated as protected until an implementation work order performs a read-only audit"). When in doubt, treat content as more protected than you think it is, and let a human downgrade that if it's wrong.

### Every change has provenance

Every canon and production node and edge carries a `source` list pointing back to the document or file that justifies it (`studio/atlas-graph/storage-model.md`). The Validator and `missing-sources` query enforce this is never silently dropped.

**Why it matters:** provenance is what lets an agent - or a human, months later - answer "why does this fact exist?" without archaeology. A graph fact with no source is a claim nobody can check.

**How to apply:** never add a node or edge without a real source path that exists on disk. If the justification is "I decided this while writing the work order," the work order file itself is the source.

### Preserve meaningful diffs

The Immutable Formatting Rule (`studio/immutable-formatting-rule.md`) exists because reformatting and semantic change look identical in a raw diff view unless they are deliberately kept apart. A reviewer who cannot tell what actually changed cannot review anything.

**Why it matters:** in a multi-agent project, accidental reformatting hides the real change, makes reviews harder, and creates unnecessary merge conflicts between agents working concurrently on adjacent content.

**How to apply:** add new entries in the house style of the surrounding file; never run a broad formatter over a file as a side effect of a semantic change; run `python3 tools/atlas_format/format_guard.py --check` before submitting any graph JSON change; if a formatting change is genuinely needed, it must be its own explicitly-authorized work order, not a side effect of another one.

### Atlas proposes. Humans approve.

This is the master rule the others compose into. The Planning Engine recommends. The orchestrator recommends. The Canon Linter warns. None of them execute, dispatch, or promote on their own authority. Only a human (or an agent explicitly acting under an approved work order's scope) takes the action.

**Why it matters:** automation that can act on its own recommendations without a checkpoint is automation that can compound a bad recommendation into a bad outcome before anyone notices.

**How to apply:** any new tool that produces a recommendation must stop at the recommendation. If a future work order proposes automatic dispatch, treat that as a significant governance change requiring its own ADR, not an incremental feature.

## Resolving Conflicts Between Principles

Principles occasionally pull against each other. In order of precedence when they conflict:

1. **Human approval for canon** and **every asset has an owner** always win - protecting canon integrity and hand-authored work outranks velocity.
2. **Preserve meaningful diffs** outranks convenience - never bundle a formatting change with a semantic one to save a second commit.
3. **Deterministic systems before opaque AI** outranks speed of implementation - a slower deterministic check beats a fast opaque one for anything QA-shaped.
4. **Capabilities outlive providers** yields to explicit human instruction - if a human names a specific provider for a specific task, that instruction stands; the principle governs the *default*, not every case.

## Atlas Core vs. Projects: Governance Boundary

Restating the design rule from `studio/atlas-core.md` as an actual governance test, since "would this be useful to multiple projects" is sometimes ambiguous in the moment:

A change belongs in **Atlas Core** if any of the following is true:

- It changes the shape of the graph, a work order's frontmatter contract, or a registry (capability, provider, node-types, relationship-types).
- It is a tool, script, or process that operates the same way regardless of which project's graph it points at (Doctor, Validator, Canon Linter, Graph Diff, Formatting Guard, Planning Engine, Orchestration).
- It defines a role, a lifecycle, or a QA gate that every project should inherit by default.

A change belongs under **Projects** (`projects/<project-id>/`) if any of the following is true:

- It is a canon fact, a story beat, a character, a region, or any world-specific truth.
- It is a milestone, roadmap, or production plan for that project's content.
- It is an engine mapping specific to that project's chosen engine and repository.

**When a project-specific pattern should graduate to Atlas Core:** if the same pattern is independently needed by a second project, or if a project-specific tool turns out to have zero project-specific logic in it (it only reads generic graph shape), that is the signal to extract it into Atlas Core and register the change as an ADR.

## When Atlas Core Changes Require an ADR

Per `ATLAS_CORE_1.0.md` Section 5: a change needs an ADR if it alters a schema, a governance boundary, a QA gate's behavior, or the assignment model. Concretely, these require an ADR:

- Adding, removing, or changing the meaning of a required field in the work order frontmatter contract.
- Adding a new graph node type or relationship type category (not just a new instance of an existing type).
- Changing what the Validator, Canon Linter, or Formatting Guard treat as a failure versus a warning.
- Changing how providers are matched to capabilities, or introducing automatic dispatch.
- Retiring or superseding a prior architectural decision (mark the old ADR superseded; do not delete it).

These do not require an ADR, only normal work order review:

- Adding new canon facts, work orders, or project content.
- Adding a new capability or provider entry to an existing registry shape.
- Adding a new tool that composes existing primitives without changing their contracts.
