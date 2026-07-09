# Agent Assignment System (v1)

## Purpose

Defines how AtlasStudio matches a work order to the AI provider (or human) best suited to do it, conserving scarce sessions and keeping every recommendation explainable. This is the WO-0004 deliverable.

## Relationship to Prior and Current Design

Two earlier decisions already cover most of this ground; this document does not re-derive or paraphrase them, only assembles the parts WO-0004 asked for and fills the gaps between them.

- **ADR-0006 (superseded)** built a scheduler that scored named agents (`agent.gpt`, `agent.claude_code`, ...) directly against task classes. Its deterministic algorithm - classify, filter, rank, fall back - is sound and is reused below. Its documented form, `studio/scheduling/agent-scheduler-design.md`, is retained for historical reference only; do not cite it as current.
- **ADR-0007 (current)** replaced named-agent scoring with capability-based orchestration: work needs *capabilities*, capabilities are supplied by *providers*, and the orchestrator recommends primary/fallback providers per capability rather than hardcoding vendor names. See `studio/orchestration/capability-based-orchestration.md`, `atlas-core/capabilities/README.md`, `atlas-core/providers/README.md`.

ADR-0007 established the philosophy and named the registries but left both registries as prose ("Registry Direction") with no schema and no ranking algorithm - the capability model was never actually made operable. This document closes that gap: it defines the schema those registries need (`schemas/capability.schema.json`, `schemas/provider.schema.json`) and restates ADR-0006's algorithm in capability terms so it can run against them.

Populating `atlas-core/capabilities/` and `atlas-core/providers/` with real entries is out of scope here (outside this work order's allowed change paths) and is the natural next work order once this model is accepted.

## Known Terminology Gap

Three documents in this repository use "agent" and "provider" inconsistently, and this document does not resolve it, only names it so a future work order can:

- `studio/atlas-graph/node-types.md`: `agent.*` = an AI or human production role (e.g. `agent.claude_code`); `provider.*` = the underlying platform (e.g. `provider.anthropic`).
- `atlas-core/providers/README.md` and `studio/orchestration/capability-based-orchestration.md`: "provider" = the tool itself (GPT, Claude Code, Codex, ...), matching what the graph calls `agent.*`.
- `studio/work-order-format.md`: `recommended_agent` frontmatter = the tool itself, using the graph's "agent" sense, not the orchestration docs' "provider" sense.

This document follows `work-order-format.md`, the existing, load-bearing convention across every work order written so far: **"agent" means the tool** (claude-code, gpt, codex, github-copilot, ollama, or human). Where it discusses the capability registries, it uses their native term, "provider," for the same thing. Treat the two as synonyms until a dedicated work order reconciles the vocabulary.

## Assignment Metadata (Work Order Frontmatter)

Two frontmatter fields on every work order, per `studio/work-order-format.md`:

- `recommended_agent` (existing) - the primary recommendation.
- `fallback_agent` (new) - the next-best agent if `recommended_agent` is unavailable or over its risk ceiling. Optional; older work orders may omit it.

Both are advisory metadata produced or confirmed by the algorithm below, never a dispatch instruction - the human creator remains the final authority on assignment, per `studio/agent-roles.md`'s Human Creator role. Schema: `schemas/work-order.schema.json`.

## Task Classification

Signals, in priority order (unchanged from the superseded scheduler, since classification was never the part ADR-0007 objected to):

1. `task_class` frontmatter field, if present (explicit override).
2. `agent_role` frontmatter: `senior-software-architect` -> `architecture`, `implementation-engineer` -> `implementation`, `creative-systems-designer` -> `creative_design`, `qa-reviewer` / `implementation-auditor` -> `review_qa`.
3. `engine_specific: true` -> `implementation`.
4. Title and Purpose keywords: story/quest/dialogue/region/NPC -> `creative_design`; design/architecture/model -> `architecture`; implement/script/tool/export -> `implementation`; lint/audit/review/consistency -> `review_qa`; rename/copy/format -> `repetitive_edit`.
5. Default: `implementation`.

A work order that promotes graph facts to canon, or resolves disputed canon, is additionally tagged `canon_decision` regardless of other signals.

## Task Class to Capability Mapping

Where ADR-0006 scored named agents per task class directly, this model routes through the capability registry (`atlas-core/capabilities/README.md`) instead, per ADR-0007:

| Task class | Primary capability | Secondary capability |
| --- | --- | --- |
| `creative_design` | `creative-writing` | `canon-design` |
| `architecture` | `architecture-review` | `schema-design` |
| `implementation` | `python-development` or `rpg-maker-json` (per `engine_specific`) | `graph-analysis` |
| `repetitive_edit` | `rpg-maker-json` or `python-development` (per `engine_specific`) | - |
| `review_qa` | `qa-review` | `documentation` |
| `canon_decision` | `human-approval` | `canon-design` |

`canon_decision` always requires `human-approval`, which per `schemas/capability.schema.json`'s `human_only` flag excludes every provider but `human` regardless of confidence score.

## Assignment Algorithm

Deterministic steps, run per work order:

1. **Classify** into a task class (above), then map to a required capability.
2. **Capability filter.** Using `schemas/provider.schema.json` entries, drop providers with confidence `0` (or no entry at all) for the required capability.
3. **Risk gate.** Drop providers whose `risk_ceiling` is below the work order's `risk_level`, unless paired with a `REVIEWED_BY provider.human` condition.
4. **Availability filter.** Using the manual status file (schema: `schemas/agent-status.schema.json`), drop `exhausted` and `offline` providers. Keep `limited`/`unknown` providers only if their capability confidence is `3`.
5. **Rank** remaining providers by weighted component scores:
   - `capability_fit` - the 0-3 confidence score (weight 3)
   - `risk_alignment` - 1 if `risk_ceiling` >= `risk_level`, else 0 (weight 2)
   - `availability` - available 2, limited/unknown 1 (weight 2)
   - `context_fit` - deep 2, medium 1, shallow 0, compared to the work order's breadth (weight 1)
   - `quota_conservation` - none 2, medium 1, high 0 (weight 1)
6. **Fallback chain.** The next-ranked provider becomes `fallback_agent`, with any degradation condition stated (e.g. "conserve quota: availability is limited").
7. **Emit** the recommendation with every component score and filter decision stated as evidence, and write `recommended_agent` / `fallback_agent` into the work order's frontmatter.

If no provider passes the filters, the recommendation is `blocked`, naming the reason per provider, so the human can wait, split the work order, or override manually. Ties break by `quota_conservation`, then by provider id alphabetically, so output is stable.

This step order and scoring formula are unchanged from `studio/scheduling/agent-scheduler-design.md`; only the object being filtered and ranked changed, from named agents scored per task class to providers scored per capability, per ADR-0007.

## Risk-Based Routing

- `risk_level: high` work is only recommended to providers with `risk_ceiling: high`; anything else requires `REVIEWED_BY provider.human before merge`.
- Work touching hand-authored or protected content always adds a human review condition regardless of provider.
- Irreversible work (deletes, canon retirement, external publication) is never recommended to `limited`, `unknown`, or `shallow`-context providers.
- `canon_decision` work routes to `provider.human`, with AI providers only as drafting support.

## Manual Session/Quota Status

Unchanged from the superseded scheduler design: availability lives in a human-maintained file at `studio/scheduling/agent-status.json` (not yet created - `studio/scheduling/agent-status.example.json` is the worked example), validated against `schemas/agent-status.schema.json`. Manual-first by design: no provider API is called in v1. Entries older than 7 days (`last_verified`) degrade to `unknown`.

## Worked Example

**WO-0013 Canon Linter** - `agent_role: implementation-auditor`, `engine_specific: false`, `risk_level: medium` -> classified `review_qa` -> required capability `qa-review`. If `provider.codex` has `capabilities_supplied: [{qa-review, confidence: 2}]`, `risk_ceiling: medium`, and status `available`, and `provider.ollama` has `{qa-review, confidence: 3}` but `risk_ceiling: low`, the risk gate drops Ollama for this `medium`-risk work order unless paired with human review, and Codex is recommended with Ollama listed as a fallback carrying a `REVIEWED_BY provider.human` condition.

## Acceptance Criteria Status

- Work orders can specify recommended agent and fallback agent: done via `recommended_agent` / `fallback_agent` in `schemas/work-order.schema.json`.
- Assignment model accounts for strengths, quota, risk, and task type: done via the algorithm above, `schemas/provider.schema.json`, and `schemas/agent-status.schema.json`.
- Model supports manual entry of session status if APIs do not expose it: done, unchanged from the superseded scheduler's manual-first design.
- Model does not depend on any one AI provider: done, capability-first per ADR-0007.

## Out of Scope (Deferred)

- Live provider quota APIs, automated dispatch, credential storage, and cost billing.
- Populating `atlas-core/capabilities/` and `atlas-core/providers/` with real entries against the new schemas.
- Reconciling the agent/provider terminology gap named above.
- A `tools/atlas_scheduler/` implementation of this model - a natural follow-up work order once this design is accepted, per the same deferral `agent-scheduler-design.md` already noted.
