# Atlas Implementation Handoff

## Purpose

This document describes how an imported Atlas work package (a work order, an implementation packet, or a Build Gate) becomes an implementation contract AtlasStudio can hand to Codex, GitHub Copilot, GPT, Claude Code, or Ollama - without rewriting, restating, or forking the original Atlas document. The handoff is a routing and framing layer, not a new authorship layer.

## The Core Rule: Point, Don't Paraphrase

An AtlasStudio handoff never reproduces an Atlas implementation packet's content as new AtlasStudio prose. It points to the imported entity (by `source_identifier` and `source_path`, per `imported-entity-model.md`), states what capability the work requires, and lets the assigned provider read the original packet directly. If AtlasStudio's handoff text and the original Atlas packet ever say different things about the same work, the handoff is wrong by definition - there is exactly one authoritative description of the work, and it lives in Atlas.

## Handoff Shape

A handoff record references, at minimum:

```json
{
  "handoff_id": "(AtlasStudio-local identifier, not an Atlas ID)",
  "source_work_package": "IMP-HOM-017",
  "source_kind": "implementation_packet",
  "source_path": "atlas/docs/09_Technical/Implementation_Packets/Home_Island/IMP_HOM_017_Manual_Map_Build_Ashford_Exterior.md",
  "required_capabilities": ["rpg-maker-json", "architecture-review"],
  "recommended_provider": "codex",
  "fallback_provider": "claude-code",
  "atlasstudio_role": "bridge_documentation_only",
  "status": "not_started | in_progress | submitted | verified"
}
```

`required_capabilities` and provider recommendations are produced the same way AtlasStudio's existing capability-based orchestration model (`studio/orchestration/capability-based-orchestration.md`) already recommends providers for AtlasStudio's own work - reused here, not reinvented, because routing work to the right provider is a project-agnostic Atlas Core capability regardless of which repository the work's content lives in.

## Per-Provider Framing

The same imported packet is framed differently depending on who receives it - framing changes what context is surfaced first, never what the work actually is.

### Codex

Receives: the imported `implementation_packet` entity, its `implements` and `requires` relationships resolved to their own imported entities (so Codex sees the full dependency chain without needing to traverse Atlas manually), and the relevant `map` entity's current `ownership_state` from `TheLastSwordProtocol-Game/map_ownership.json` (imported, per `imported-entity-model.md`'s `map` entity). Codex should never receive a paraphrased summary of the packet in place of the packet itself - RPG Maker implementation detail is exactly where paraphrasing risks losing a load-bearing detail.

### GitHub Copilot

Receives: a narrower slice - the specific, already-scoped sub-task within a packet (e.g., "wire this one already-defined transfer event"), since Copilot's strength per `studio/agent-roles.md` is small, well-bounded edits, not open-ended packet interpretation. AtlasStudio's role here is decomposition-by-reference: pointing at a specific paragraph or checklist line within the original packet, not rewriting it into a new task description.

### GPT

Receives: the imported `dialogue_reference` and `character`/`npc` entities relevant to a packet, plus the packet's narrative framing verbatim, when the handoff involves dialogue authoring or creative review. GPT should be pointed at Atlas's own Story/Character/Creative Bibles directly for tone and canon, never at an AtlasStudio restatement of them - `WO-0018` already established that AtlasStudio's own gameplay-philosophy and character documents are historical for this project, and a GPT handoff must not accidentally resurface them as if they were still live.

### Claude Code

Receives: architecture-review-shaped handoffs - packets whose `object_type` implies structural or cross-cutting work (bridge design, validator/tooling proposals per `repository-authority.md`'s change-flow model, or a review of whether a completed implementation matches its source packet). Claude Code's role in this bridge is disproportionately about verifying traceability (does the built map actually match what the imported packet said) rather than authoring new design.

### Ollama

Receives: read-only consistency-check handoffs - for example, confirming that an imported entity's `title` or `relationships` are internally consistent with other imported entities, or producing a low-cost summary of a synchronization report (`synchronization-strategy.md`) for human review. Ollama is never handed a packet requiring canon judgment, per its existing "avoid assigning" guidance in `studio/agent-roles.md`.

## What The Handoff Explicitly Does Not Do

- It does not rewrite the original Atlas work order, implementation packet, or Build Gate. Any provider executing a handoff should be reading the original Atlas document, routed to by AtlasStudio, not a copy of it.
- It does not mark Atlas's own work order as complete or accepted - only Atlas's own process (its work order queue, its Production Director) can do that. AtlasStudio's `status` field on a handoff record tracks AtlasStudio's *awareness* of the work's progress, not an authoritative completion state.
- It does not grant AtlasStudio or any provider write access to `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` as a side effect of framing a handoff. Whatever access model those repositories already use (their own `AGENTS.md`, `map_ownership.json`) governs actual writes, independent of anything AtlasStudio's bridge does.
- It does not invent new implementation packets. If AtlasStudio's planning surfaces work that has no corresponding Atlas packet yet, the correct action is to propose that gap back to Atlas's own process (per `repository-authority.md`), not to draft a competing packet inside AtlasStudio.

## Verification Loop

Once a provider completes work against a handoff, AtlasStudio's role is to confirm - not certify - that the result matches the imported packet's stated requirements (a traceability check, reusing the Graph Diff Engine pattern against the `map`/`implementation_packet` entities' current state versus their imported baseline), and to report that confirmation back into the handoff's `status` field. Final acceptance of the actual game content remains Atlas's and the human Production Director's call, per `repository-authority.md`.

## Relationship To Existing AtlasStudio Tooling

This handoff model deliberately reuses, rather than replaces, AtlasStudio's existing capability-based orchestration design and its provider role definitions in `studio/agent-roles.md`. The only new concept this document introduces is the handoff record's `source_work_package` pointer and the discipline of never paraphrasing Atlas's own content - everything else (capability matching, provider recommendation, fallback logic) is the same machinery AtlasStudio already designed for its own (now-historical, per `WO-0018`) production work, now pointed at Atlas's live production instead.
