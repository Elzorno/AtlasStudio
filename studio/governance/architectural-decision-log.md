# Architectural Decision Log

## Purpose

This is the running record of architectural decisions behind AtlasStudio / Atlas Core. Entries are numbered sequentially and never renumbered or deleted. A decision that is later reversed is marked `Superseded by ADR-NNNN`, not removed - the history of why something changed is as valuable as the current state.

New entries use `studio/governance/decision-record-template.md`. See `studio/governance/atlas-principles.md`, "When Atlas Core Changes Require an ADR," for what qualifies.

## Index

| ADR | Title | Status |
| --- | --- | --- |
| [ADR-0001](#adr-0001---split-atlas-core-from-projects) | Split Atlas Core from Projects | Accepted |
| [ADR-0002](#adr-0002---git-native-json-graph-over-a-database-for-v0) | Git-native JSON graph over a database for v0 | Accepted |
| [ADR-0003](#adr-0003---stdlib-only-deterministic-graph-tooling) | Stdlib-only deterministic graph tooling | Accepted |
| [ADR-0004](#adr-0004---immutable-formatting-rule) | Immutable Formatting Rule | Accepted |
| [ADR-0005](#adr-0005---graph-diff-engine-as-the-standard-review-artifact) | Graph Diff Engine as the standard review artifact | Accepted |
| [ADR-0006](#adr-0006---manual-first-named-agent-scheduler) | Manual-first named-agent scheduler | Superseded by ADR-0007 |
| [ADR-0007](#adr-0007---replace-named-agent-scheduling-with-capability-based-orchestration) | Replace named-agent scheduling with capability-based orchestration | Accepted |
| [ADR-0008](#adr-0008---rule-driven-deterministic-canon-linter) | Rule-driven deterministic canon linter | Accepted |
| [ADR-0009](#adr-0009---deterministic-evidence-scored-planning-engine) | Deterministic, evidence-scored planning engine | Accepted |
| [ADR-0010](#adr-0010---engine-bridge-ownership-model) | Engine bridge ownership model | Accepted |
| [ADR-0011](#adr-0011---human-modeled-as-a-provider) | Human modeled as a provider | Accepted |

---

## ADR-0001 - Split Atlas Core from Projects

**Status:** Accepted
**Date:** 2026-07-07

**Context:** AtlasStudio needed a foundation that would not tie its tooling and process to The Last Sword Protocol specifically. Atlas v1 had no such separation and its patterns were hard to reuse.

**Decision:** Treat AtlasStudio as two layers - Atlas Core (reusable platform: graph tooling, work order lifecycle, agent/capability model, diagnostics, QA intelligence, engine bridge framework) and Projects (individual games and their canon, graphs, and engine mappings). The rule of thumb: if a feature would help more than one project, it belongs in Atlas Core.

**Consequences:** Every subsequent tool (Doctor, Validator, Canon Linter, Graph Diff, Planning Engine, Orchestration) was built to operate on any project's graph shape, not hardcoded to The Last Sword Protocol. This costs a little extra abstraction discipline up front in exchange for reuse later.

**Alternatives Considered:** Build tooling directly against The Last Sword Protocol and generalize later - rejected because Atlas v1 already showed that retrofitting reusability after the fact is expensive.

**Related:** Work order: `WO-0001`. Documents: `studio/atlas-core.md`, `studio/vision.md`.

**Governance Note:** Governance boundary decision - defines the Atlas Core vs. Projects test used by every later ADR.

---

## ADR-0002 - Git-native JSON graph over a database for v0

**Status:** Accepted
**Date:** 2026-07-07

**Context:** AtlasStudio needed a shared memory layer connecting canon, production, and engine bridge facts for agents, without agents re-deriving relationships from prose every session.

**Decision:** Store the Atlas Graph as versioned JSON files in Git (`projects/<project>/graph/nodes/*.json`, `graph/edges/*.json`), not in SQLite, DuckDB, or Neo4j.

**Consequences:** The graph is reviewable in pull requests, editable by any agent with a text editor, and requires no runtime infrastructure. The cost is weaker query performance at scale and no native graph traversal engine - acceptable for v0's size, explicitly flagged as revisitable in `studio/atlas-graph/storage-model.md`'s Future Migration Path.

**Alternatives Considered:** SQLite/DuckDB (better query performance, worse Git reviewability), Neo4j or RDF/Turtle (native graph semantics, infrastructure overhead disproportionate to v0's needs).

**Related:** Work order: `WO-0007`. Documents: `studio/atlas-graph/storage-model.md`, `studio/atlas-graph/overview.md`.

**Governance Note:** Schema change - establishes the graph's on-disk contract that the Validator and every graph tool depend on.

---

## ADR-0003 - Stdlib-only deterministic graph tooling

**Status:** Accepted
**Date:** 2026-07-07

**Context:** The graph needed validation and query tools that any agent or CI environment could run without dependency installation friction.

**Decision:** Build the Validator and Query tools (`tools/atlas_graph/`) using only the Python standard library, with deterministic, explainable output.

**Consequences:** Zero dependency-install friction and fully reproducible output. The trade-off is writing more by hand (no framework conveniences) - accepted because these tools are the trust floor every other tool builds on.

**Alternatives Considered:** A schema-validation framework (jsonschema, pydantic) - rejected for v0 to avoid a dependency surface for a tool meant to run everywhere with zero setup.

**Related:** Work order: `WO-0008`. Documents: `tools/atlas_graph/validate_graph.py`, `tools/atlas_graph/query_graph.py`.

**Governance Note:** Sets the precedent - carried forward by Doctor, Canon Linter, Graph Diff, and Formatting Guard - that Atlas Core tooling defaults to stdlib-only unless a dependency is unavoidable.

---

## ADR-0004 - Immutable Formatting Rule

**Status:** Accepted
**Date:** 2026-07-07

**Context:** In a multi-agent project, accidental reformatting (re-indenting, reordering keys, wrapping changes) can hide the real semantic change in a diff, making review harder and creating avoidable merge conflicts between concurrently-working agents.

**Decision:** Semantic work orders must not reformat unrelated existing content. Agents preserve house style by default; explicit formatting-only work orders are the only sanctioned path to broad reformatting, and they must not mix with semantic changes. A check-only tool (`tools/atlas_format/format_guard.py`) detects and warns about formatting-only churn and suspicious mixed diffs without ever rewriting files itself.

**Consequences:** Every diff stays reviewable at the cost of agents needing to hand-match surrounding style rather than reach for an auto-formatter. The guard is advisory (warnings), not a hard CI gate, in v1.

**Alternatives Considered:** Auto-formatting all graph JSON on every write (rejected - destroys diff readability by design); no formatting discipline at all (rejected after observing how easily a full-file rewrite obscures a one-line semantic change).

**Related:** Work order: `WO-0014`. Documents: `studio/immutable-formatting-rule.md`.

**Governance Note:** QA gate behavior decision - defines what the Formatting Guard treats as a warning versus clean.

---

## ADR-0005 - Graph Diff Engine as the standard review artifact

**Status:** Accepted
**Date:** 2026-07-07

**Context:** As graph changes became as consequential as code changes, reviewers and handoff agents needed a way to see exactly what changed between two graph states without manually diffing raw JSON.

**Decision:** Build a diff engine (`tools/atlas_graph/diff_graph.py`) that compares two graph states (Git refs, commits, or directories) and reports added/removed/changed nodes and edges, grouped by canon/production/bridge scope, with status changes, scope moves, and source reference changes highlighted separately.

**Consequences:** Every work order touching the graph can produce a single human-readable change summary for QA and agent handoff, instead of a raw JSON diff. This became the standard verification step for graph-touching work orders going forward.

**Alternatives Considered:** Relying on raw `git diff` on the JSON files - rejected because scope (canon vs. production vs. bridge) and semantic highlights (a status promotion vs. an unrelated field edit) are invisible in a raw text diff.

**Related:** Work order: `WO-0010`. Documents: `studio/atlas-graph/diff-model.md`.

**Governance Note:** Established the graph-diff-before-review pattern referenced by the Implementation Plan and Doctor's verification chain.

---

## ADR-0006 - Manual-first named-agent scheduler

**Status:** Superseded by ADR-0007
**Date:** 2026-07-07

**Context:** The human creator coordinates several distinct AI providers (GPT, Claude Code, Codex, GitHub Copilot, Ollama) and wanted AtlasStudio to recommend which one should take a given work order, conserving limited sessions.

**Decision:** Build an Agent Scheduler that scored named agents (`agent.gpt`, `agent.claude_code`, `agent.codex`, ...) directly against task classes, with a manual, human-maintained session/quota status file driving availability.

**Consequences:** Delivered a working, explainable recommendation model quickly. The cost, discovered shortly after, was that the model tied every work order's routing logic to specific vendor names - a provider swap or a new provider meant revisiting the scoring table itself rather than just updating a registry entry.

**Alternatives Considered:** None seriously considered at the time; capability-first design was recognized as the better foundation only after this version was built and reviewed.

**Related:** Work order: `WO-0012` (original scope). Documents: `studio/scheduling/agent-scheduler-design.md` (retained for historical reference).

**Governance Note:** Assignment model decision, later reversed - see ADR-0007.

---

## ADR-0007 - Replace named-agent scheduling with capability-based orchestration

**Status:** Accepted
**Date:** 2026-07-07

**Context:** ADR-0006's named-agent scheduler worked, but coupled AtlasStudio's routing logic to specific vendors. The studio needed to adapt when a provider runs out of quota, a stronger model becomes available, or a local model becomes sufficient, without redesigning the assignment model each time.

**Decision:** Retire the Agent Scheduler in place and replace it with a capability-based orchestration model: work is described by required/preferred capabilities (`atlas-core/capabilities/`), capabilities are supplied by providers (`atlas-core/providers/`), and manual provider status drives availability. The orchestrator recommends a primary and fallback provider per capability, with an explanation; it does not dispatch.

**Consequences:** Provider changes (a new model, a quota exhaustion, a vendor swap) now only require a registry update, not a redesign of the scoring model. The cost is one more layer of indirection (capability -> provider) versus scoring agents directly.

**Alternatives Considered:** Patching the named-agent scheduler to add an aliasing layer - rejected as a half-measure that would keep vendor names as the primary key internally.

**Related:** Work order: `WO-0012` (revised scope, `supersedes: Agent Scheduler`). Documents: `studio/orchestration/capability-based-orchestration.md`, `atlas-core/capabilities/README.md`, `atlas-core/providers/README.md`.

**Governance Note:** Assignment model decision; supersedes ADR-0006. This is also the concrete case study behind the "Capabilities outlive providers" principle in `studio/governance/atlas-principles.md`.

---

## ADR-0008 - Rule-driven deterministic canon linter

**Status:** Accepted
**Date:** 2026-07-07

**Context:** As canon grew, AtlasStudio needed a way to check whether canon was coherent enough for agents to build on - missing containment relationships, incomplete design hooks, duplicate or conflicting facts - without relying on an LLM's subjective read of the world documents.

**Decision:** Build a deterministic canon linter (`tools/atlas_lint/`) whose rules live in a reviewable JSON file (`tools/atlas_lint/rules/canon_lint_rules.json`), checking structure, completeness, consistency, coverage, production linkage, and bridge readiness. The linter never modifies canon; warnings are QA prompts, not hard failures, unless `--fail-on-warning` is explicitly passed.

**Consequences:** Canon QA results are reproducible and arguable - a human can read the rule file and agree or disagree with a specific check, rather than accepting or rejecting an opaque model judgment. The cost is that genuinely subjective canon quality (tone, voice, creative coherence) is out of scope for this tool by design.

**Alternatives Considered:** An LLM-based "canon reviewer" agent - rejected per the "deterministic before opaque AI" principle; subjective creative review still happens, but through human and GPT creative collaboration, not through a QA gate.

**Related:** Work order: `WO-0013`. Documents: `tools/atlas_lint/README.md`.

**Governance Note:** QA gate behavior decision - defines what counts as a deterministically-checkable canon defect.

---

## ADR-0009 - Deterministic, evidence-scored planning engine

**Status:** Accepted
**Date:** 2026-07-07

**Context:** As the number of open work orders and tools grew, AtlasStudio needed a way to recommend what to work on next without a human manually re-deriving priority from scratch each time, and without that recommendation becoming an unaccountable black box.

**Decision:** Build a Planning Engine (`tools/atlas_planner/`) that reads graph state, work order frontmatter, Studio Doctor signals, and Canon Linter findings, and produces recommendations with named component scores (milestone impact, dependency value, technical debt, player value, core platform value) plus evidence and suggested agents. The planner never creates work orders automatically.

**Consequences:** Prioritization becomes reproducible and auditable rather than ad hoc. The planner is only as good as the signals it reads - Doctor and Canon Linter findings - so its recommendations degrade gracefully (not silently) if those signals are stale.

**Alternatives Considered:** A single opaque "priority score" - rejected per the "planning should be explainable" principle; an LLM-driven planner - rejected per "deterministic before opaque AI" for the same reason the Canon Linter is deterministic.

**Related:** Work order: `WO-0011`. Documents: `tools/atlas_planner/README.md`.

**Governance Note:** Assignment/prioritization model decision - establishes the "recommend, never auto-create" boundary the Capability-Based Orchestration model (ADR-0007) also follows.

---

## ADR-0010 - Engine bridge ownership model

**Status:** Accepted
**Date:** 2026-07-07

**Context:** RPG Maker MZ implementation work needed a defined home separate from engine-independent design canon, and a way to protect hand-authored maps and events from being silently regenerated or overwritten by an implementation agent.

**Decision:** Build an engine bridge (`bridges/rpg-maker-mz/`) that owns the design-to-implementation translation, defines ownership states (generated, agent-drafted, human-edited, hand-authored, locked), and produces read-only handoff checklists (`tools/rpg_maker_bridge/handoff_generator.py`) rather than writing directly into the game repository. Unknown ownership defaults to protected.

**Consequences:** Core design documents stay engine-independent, and implementation agents get a clear, auditable handoff format instead of ad hoc instructions. The cost is an extra translation layer between design intent and RPG Maker JSON - accepted because the alternative (engine IDs leaking into canon) was explicitly identified as an Atlas v1 failure mode.

**Alternatives Considered:** Letting implementation agents read/write the game repository directly from work order text - rejected because it offers no ownership protection and re-creates Atlas v1's implementation-leaking design.

**Related:** Work order: `WO-0005`. Documents: `bridges/rpg-maker-mz/bridge-design.md`, `bridges/rpg-maker-mz/ownership-model.md`, `bridges/rpg-maker-mz/handoff-format.md`.

**Governance Note:** Governance boundary decision - defines where engine-specific detail is allowed to live, and the ownership contract every implementation-facing tool must respect.

---

## ADR-0011 - Human modeled as a provider

**Status:** Accepted
**Date:** 2026-07-07

**Context:** Some capabilities genuinely cannot be delegated to any AI provider - final canon approval, creative direction, risk acceptance, scope approval, and merge approval. The orchestration model needed a way to represent this without a special-cased exception path.

**Decision:** Model the human creator as a provider in the Provider Registry (`atlas-core/providers/`), with a defined set of human-only or human-primary capabilities, rather than treating human involvement as an implicit step outside the capability model.

**Consequences:** "Human approval required" becomes a normal, queryable output of the orchestrator (a capability with exactly one eligible provider) instead of a special case bolted onto every recommendation. This keeps `atlas proposes, humans approve` (the master governance rule) expressed in the same data model as everything else, rather than as an unenforced convention.

**Alternatives Considered:** Keeping human approval as an implicit, undocumented step after every AI recommendation - rejected because it is exactly the kind of unenforced convention that erodes over time without being modeled explicitly.

**Related:** Documents: `studio/orchestration/capability-based-orchestration.md` ("Human As Provider"), `atlas-core/providers/README.md`.

**Governance Note:** Assignment model decision - the concrete implementation of the "Atlas proposes, humans approve" principle for capabilities that cannot be delegated.
