# Agent Scheduler Design (v1)

## Purpose

The Agent Scheduler recommends the best AI provider or agent for each work order based on task type, capability, risk, and available session/quota status.

The Planning Engine (WO-0011) answers **what** to work on next. The Agent Scheduler answers **who** should do it. Both recommend; neither dispatches. The human creator remains the final authority on every assignment.

## Design Principles

1. **Manual-first.** Session and quota status comes from a human-maintained status file. No provider API is called, ever, in v1.
2. **Deterministic and explainable.** Given the same work order, capability profiles, and status file, the scheduler always produces the same recommendation with the same stated reasons.
3. **Provider-neutral.** No logic depends on any single AI provider existing. Agents can be added or removed by editing profiles and status entries.
4. **Quota-conserving.** Scarce, strong agents are reserved for work that needs them. Cheap or local agents absorb low-risk work.
5. **Recommend, never dispatch.** Output is a ranked recommendation with fallbacks, not an action.

## Agent Capability Profiles

Profiles restate `studio/agent-roles.md` as scoreable data. Capability is rated per task class on a 0-3 scale:

- `3` - primary strength, prefer this agent
- `2` - competent, acceptable assignment
- `1` - possible but wasteful or needs review
- `0` - avoid, listed under the role's avoid rules

| Task class | gpt | claude_code | codex | github_copilot | ollama |
| --- | --- | --- | --- | --- | --- |
| creative_design (story, quests, dialogue, regions, pacing) | 3 | 1 | 0 | 0 | 1 |
| architecture (tool design, repo structure, exporters, refactors) | 0 | 3 | 1 | 0 | 0 |
| implementation (scripts, plugins, JSON transforms, build automation) | 0 | 2 | 3 | 1 | 1 |
| repetitive_edit (boilerplate, small edits, copy tweaks) | 0 | 0 | 2 | 3 | 2 |
| review_qa (consistency checks, draft critique, audits, summaries) | 1 | 2 | 2 | 0 | 3 |
| canon_decision (final creative or canon judgment) | 0 | 0 | 0 | 0 | 0 |

`canon_decision` is always routed to `agent.human`. No AI agent may score above 0 for it.

Each profile also carries:

- `risk_ceiling` - the highest `risk_level` the agent may take unreviewed: `high` for claude_code, `medium` for gpt and codex, `low` for github_copilot and ollama.
- `context_depth` - `deep` (gpt, claude_code), `medium` (codex, ollama), `shallow` (github_copilot). Work orders that span many documents or graph scopes need `deep` or `medium`.
- `scarcity` - `high` (claude_code, gpt), `medium` (codex, github_copilot), `none` (ollama). Used for quota conservation, not capability.

## Task Classification

The scheduler classifies a work order from its existing metadata. No new frontmatter is required for v1, though `task_class` may be set explicitly to override classification.

Signals, in priority order:

1. `task_class` frontmatter field, if present (explicit override).
2. `agent_role` frontmatter: `senior-software-architect` → architecture, `implementation-engineer` → implementation, `creative-systems-designer` → creative_design, `qa-reviewer` → review_qa.
3. `engine_specific: true` → implementation.
4. Title and Purpose keywords: story/quest/dialogue/region/NPC → creative_design; design/architecture/model → architecture; implement/script/tool/export → implementation; lint/audit/review/consistency → review_qa; rename/copy/format → repetitive_edit.
5. Default: implementation.

A work order that promotes graph facts to canon, or that resolves disputed canon, is additionally tagged `canon_decision` regardless of other signals, which forces human routing for that portion.

## Manual Session/Quota Status

Availability lives in a human-maintained file:

```text
studio/scheduling/agent-status.json
```

Schema: `schemas/agent-status.schema.json`. Example: `studio/scheduling/agent-status.example.json`.

Per-agent fields:

- `availability` - one of:
  - `available` - normal use
  - `limited` - usable, but conserve; only assign work scoring 3 for this agent
  - `exhausted` - quota spent; do not assign until reset
  - `offline` - not reachable or not installed
  - `unknown` - no recent human update; treat as `limited`
- `quota` - optional manual counters: `used`, `limit`, `unit` (sessions, messages, tokens, hours), `resets_at` (ISO 8601).
- `notes` - free-text human context ("weekly cap nearly spent, save for WO-0016").
- `last_verified` - date the human last confirmed the entry. Entries older than 7 days degrade to `unknown`.

The status file is data, not secrets. It must never contain API keys, tokens, or account identifiers beyond the agent id.

## Scheduling Algorithm

Deterministic steps:

1. **Classify** the work order into a task class (above).
2. **Capability filter.** Drop agents scoring 0 for the class.
3. **Risk gate.** Drop agents whose `risk_ceiling` is below the work order's `risk_level`, unless paired with a mandatory `REVIEWED_BY agent.human` condition (see Risk-Based Routing).
4. **Availability filter.** Drop `exhausted` and `offline` agents. Keep `limited`/`unknown` agents only if their capability score is 3.
5. **Rank** remaining agents by transparent component scores:
   - `capability_fit` - the 0-3 class score (weight 3)
   - `risk_alignment` - 1 if risk_ceiling ≥ risk_level, else 0 (weight 2)
   - `availability` - available 2, limited/unknown 1 (weight 2)
   - `context_fit` - deep 2, medium 1, shallow 0, compared to the work order's breadth (weight 1)
   - `quota_conservation` - none 2, medium 1, high 0; rewards saving scarce agents (weight 1)
6. **Fallback chain.** The ranked runners-up become fallbacks, with degradation conditions attached.
7. **Emit** the recommendation with every component score and every filter decision stated as evidence.

Ties break by quota_conservation, then by agent id alphabetically, so output is stable.

## Risk-Based Routing

- `risk_level: high` work is only recommended to agents with `risk_ceiling: high`; anything else requires `conditions: ["REVIEWED_BY agent.human before merge"]`.
- Work touching hand-authored or `ownership_state` protected content always adds a human review condition regardless of agent.
- Irreversible work (deletes, canon retirement, external publication) is never recommended to `limited`, `unknown`, or `shallow`-context agents.
- `canon_decision` work routes to `agent.human` with AI agents only as drafting support.

## Fallback Logic

Each recommendation lists fallbacks in rank order. A fallback entry states what changes if it is used:

- A weaker capability score adds a review condition ("codex may implement, claude_code reviews the design first").
- A `limited` agent adds a scope condition ("only if the work order stays single-session").
- If no agent passes the filters, the recommendation is `blocked` with the reason per agent ("claude_code exhausted until 2026-07-10, codex risk ceiling below high"), so the human can either wait, lower risk by splitting the work order, or override manually.

## Recommendation Output Format

```json
{
  "work_order": "work_order.wo_0013",
  "task_class": "implementation",
  "risk_level": "medium",
  "recommendation": {
    "agent": "agent.codex",
    "provider": "provider.openai",
    "score": 17,
    "components": {
      "capability_fit": 9,
      "risk_alignment": 2,
      "availability": 4,
      "context_fit": 1,
      "quota_conservation": 1
    },
    "conditions": [],
    "evidence": [
      "agent_role implementation-engineer classified as implementation",
      "codex capability 3 for implementation",
      "codex availability: available (verified 2026-07-07)",
      "risk medium within codex risk ceiling medium"
    ]
  },
  "fallbacks": [
    {
      "agent": "agent.claude_code",
      "score": 15,
      "conditions": ["conserve quota: availability is limited"]
    },
    {
      "agent": "agent.ollama",
      "score": 10,
      "conditions": ["REVIEWED_BY agent.human before merge"]
    }
  ],
  "excluded": [
    {"agent": "agent.gpt", "reason": "capability 0 for implementation"},
    {"agent": "agent.github_copilot", "reason": "context_depth shallow for multi-file work"}
  ]
}
```

## Worked Examples (Manual Verification)

Applying the model by hand to existing work orders:

- **WO-0003 Home Region Overworld Design** - creative_design, risk medium. gpt scores 3 capability, risk within ceiling → recommend `agent.gpt`; fallback `agent.ollama` for draft critique with human review; claude_code and codex excluded at capability 0-1.
- **WO-0010 Graph Diff Engine** - architecture (agent_role senior-software-architect), risk medium. claude_code scores 3 → recommend `agent.claude_code`; fallback `agent.codex` with the condition that claude_code reviews the design; matches the actual assignment.
- **WO-0013 Canon Linter** - implementation, risk medium. codex scores 3 and conserves claude_code quota → recommend `agent.codex`; matches the actual `ASSIGNED_TO agent.codex` edge.
- **Hypothetical exhausted case** - if `agent.codex` were `exhausted` with `resets_at 2026-07-10`, WO-0013 would fall back to `agent.claude_code` (capability 2) with evidence naming the quota reset date.

## Graph Representation

Providers and agents are production graph facts, using the existing `agent` and `provider` node types from `studio/atlas-graph/node-types.md`:

```text
agent.gpt            PROVIDED_BY provider.openai
agent.codex          PROVIDED_BY provider.openai
agent.claude_code    PROVIDED_BY provider.anthropic
agent.github_copilot PROVIDED_BY provider.github_copilot
agent.ollama         PROVIDED_BY provider.ollama
```

`PROVIDED_BY` is a new production relationship introduced by this design: an agent role is provided by a platform or model provider. It should be added to `studio/atlas-graph/relationship-types.md` under Production Relationships in a follow-up documentation change (that file is outside this work order's allowed changes).

Accepted assignments continue to use the existing `ASSIGNED_TO` edge. Scheduler recommendations themselves are ephemeral output, not graph facts; only human-accepted assignments enter the graph.

Volatile session status stays in `agent-status.json`, not in the graph, because it changes too often to be worth graph history.

## Out of Scope (Deferred)

- Live provider quota APIs, automatic dispatch, credential storage, and cost billing remain out of scope per WO-0012.
- A `tools/atlas_scheduler/` implementation of this model is a natural follow-up work order once the design is accepted.
