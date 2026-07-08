---
work_order_id: WO-0029
title: AtlasStudio Daily Operations Manual
status: submitted
project: atlasstudio
recommended_agent: claude-code
agent_role: director
risk_level: low
player_facing: false
engine_specific: false
required_capabilities:
  - documentation
  - architecture-review
created: 2026-07-08
---

# WO-0029 - AtlasStudio Daily Operations Manual

## Purpose

AtlasStudio Core is complete (`studio/STATUS.md`). This work order defines the operational workflow for using AtlasStudio as the production operating environment for `The Last Sword Protocol` - the human operator's manual. It explains how a Production Director interacts with AtlasStudio throughout a normal development day, so there is no remaining uncertainty about which repository, which agent, which work order, and which validation steps should be used. This document set becomes the canonical operating guide for AtlasStudio.

## Player-Facing Goal

Indirect. This work order produces documentation only and changes no game file. Its purpose is to make every future player-facing production cycle run through a known, repeatable process, reducing the chance that a future screen ships in the same not-yet-accepted, not-yet-traceable state `reports/production-review/ashford-shop-production-review.md` found in Ashford Shop.

## Background

Review: `work-orders/WO-0018-repository-authority.md`, `WO-0020-ashford-village-implementation-contract-from-atlas-handoff.md`, `WO-0021-cross-repository-work-order-router.md`, `WO-0022-executable-router-specification.md`, `WO-0023-executable-work-order-router.md`, `WO-0024-design-pattern-library.md`, `WO-0025-interior-pattern-corpus.md`, `WO-0026-design-pattern-inheritance-model.md`, `WO-0027-pattern-aware-implementation-contracts.md`, `WO-0028-production-pipeline-validation.md`.

Review: `studio/governance/repository-authority.md`, `studio/orchestration/work-order-router.md`, `studio/scheduling/agent-scheduler-design.md`, `studio/design-patterns/` (Pattern Library and `PATTERN_RESOLUTION_RULES.md`), `reports/implementation-contracts/`, `studio/governance/production-readiness.md`.

`production-readiness.md` (`WO-0028`) found AtlasStudio's foundational mechanisms (Repository Authority, the ownership ledger) genuinely production-proven, its newer architecture well-designed but not yet exercised on a real build, and its weakest point the seam between decision and artifact - contracts, patterns, and packets not reliably traceable into what actually lands in the Game repository, and the loop from build to validation to human acceptance not yet closing. `lessons-learned.md`'s "AtlasStudio Before Journey I" section named seven standing operational practices recommended for all future implementation work. This work order is where those recommendations become the actual manual a human follows, ahead of Journey I's larger production push.

## Scope

### In Scope

- Documenting a complete production day's workflow, from Studio Health check through commit and status update, covering both an accepted and a rejected outcome.
- Producing a concise per-work-item production checklist.
- Documenting when each agent (Claude Code, Codex, GPT, Copilot, Ollama) is preferred, its strengths, limitations, recommended work types, and when it should not be used.
- Formalizing the four playtest/acceptance outcomes (Accepted, Accepted with Notes, Rejected, Deferred), including required evidence, documentation, and follow-up for each, with the Ashford Shop rejection (`BUILD-0043`) as a worked case study.
- Producing a repository-ownership decision tree with common worked examples.
- Producing a narrative day-in-the-life walkthrough starting from "I want to improve Journey I," showing routing, agent assignment, validation, and one accepted and one rejected outcome.
- Closing with a "How AtlasStudio Evolves" section stating that future AtlasStudio features should originate from real production experience rather than speculative architecture.

### Out of Scope

- Modifying `TheLastSwordProtocol-Atlas` in any way.
- Modifying `TheLastSwordProtocol-Game` in any way.
- Modifying any existing implementation contract.
- Modifying any Design Pattern document.
- Modifying any governance document (`studio/governance/`).
- Writing or modifying any code or tooling.
- Creating any new work order beyond this one.
- Redesigning any part of the architecture this manual documents.

## Inputs

- `work-orders/WO-0018`, `WO-0020` through `WO-0028`.
- `studio/governance/repository-authority.md`, `production-readiness.md`, `decision-record-template.md`.
- `studio/orchestration/work-order-router.md`, `capability-based-orchestration.md`.
- `studio/scheduling/agent-scheduler-design.md`, `studio/agent-roles.md`.
- `studio/design-patterns/PATTERN_RESOLUTION_RULES.md`, `PATTERN_REVIEW_PROCESS.md`.
- `reports/implementation-contracts/ashford-shop-build-contract.md` and siblings.
- `reports/production-review/ashford-shop-production-review.md`, `pipeline-gap-analysis.md`, `lessons-learned.md`.
- `bridges/rpg-maker-mz/ownership-model.md`, `passability-rule.md`, `handoff-format.md`.
- `rpgmakerLSP/reports/atlas-import/build-0043-guided-map-runtime-review.md` (read-only).
- `studio/immutable-formatting-rule.md`, `studio/work-order-format.md`, `studio/workflow.md`, `studio/STATUS.md`.

## Deliverables

- `studio/operations/DAILY_WORKFLOW.md`
- `studio/operations/PRODUCTION_CHECKLIST.md`
- `studio/operations/AGENT_USAGE_GUIDE.md`
- `studio/operations/PLAYTEST_AND_ACCEPTANCE.md`
- `studio/operations/REPOSITORY_DECISION_TREE.md`
- `reports/operations/atlasstudio-day-in-the-life.md`
- `work-orders/WO-0029-atlasstudio-daily-operations.md`

## Acceptance Criteria

- `DAILY_WORKFLOW.md` describes the complete production day (Start of day → Check Studio Health → Review Router recommendations → Select work → Assign agent → Review output → Validate → Playtest → Accept or Reject → Commit → Update production status), including both a successful and a rejected implementation path.
- `PRODUCTION_CHECKLIST.md` provides a concise checklist covering repository confirmed, authority confirmed, work order exists, agent assigned, validation completed, playtest completed, acceptance decision recorded, and commit completed.
- `AGENT_USAGE_GUIDE.md` documents when Claude Code, Codex, GPT, Copilot, and Ollama are each preferred, their strengths and limitations, recommended work types, and when each should not be used.
- `PLAYTEST_AND_ACCEPTANCE.md` defines Accepted, Accepted with Notes, Rejected, and Deferred, each with required evidence, required documentation, and required follow-up, and includes the Ashford Shop rejection as a worked case study grounded in `BUILD-0043`.
- `REPOSITORY_DECISION_TREE.md` answers which repository (Atlas, AtlasStudio, or Game) owns a given request, with common worked examples.
- `atlasstudio-day-in-the-life.md` walks a realistic day starting from "I want to improve Journey I," showing how AtlasStudio routes work, recommends an agent, validates the result, and records the outcome, including one successful and one rejected implementation, and closes with a section titled exactly "How AtlasStudio Evolves" stating that future AtlasStudio features should originate from real production experience rather than speculative architecture.
- No file under `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` is modified.
- No existing implementation contract, Design Pattern document, or governance document is modified.
- Documentation only: no code is added or modified.
- The Immutable Formatting Rule is preserved: no existing file is reformatted.
- This work order is marked `submitted`.

## Verification Steps

```bash
find studio/operations -name "DAILY_WORKFLOW.md" -o -name "PRODUCTION_CHECKLIST.md" -o -name "AGENT_USAGE_GUIDE.md" -o -name "PLAYTEST_AND_ACCEPTANCE.md" -o -name "REPOSITORY_DECISION_TREE.md"
find reports/operations -name "atlasstudio-day-in-the-life.md"
find work-orders -name "WO-0029-atlasstudio-daily-operations.md"
git diff --stat -- reports/implementation-contracts studio/design-patterns studio/governance
# expect no output: no implementation contract, pattern, or governance document is modified
python3 tools/atlas_format/format_guard.py --check
git -C ../TheLastSwordProtocol-Atlas status --porcelain
git -C ../TheLastSwordProtocol-Game status --porcelain
```

## Allowed Changes

- `studio/operations/DAILY_WORKFLOW.md`
- `studio/operations/PRODUCTION_CHECKLIST.md`
- `studio/operations/AGENT_USAGE_GUIDE.md`
- `studio/operations/PLAYTEST_AND_ACCEPTANCE.md`
- `studio/operations/REPOSITORY_DECISION_TREE.md`
- `reports/operations/atlasstudio-day-in-the-life.md`
- `work-orders/WO-0029-atlasstudio-daily-operations.md`

## Protected Areas

- Do not modify `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game`.
- Do not modify any existing implementation contract.
- Do not modify any Design Pattern document.
- Do not modify any governance document (`studio/governance/`).
- Do not write or modify code.
- Preserve the Immutable Formatting Rule.

## Notes for Assigned Agent

This is a documentation-and-process work order, not an architecture change. Every process step it documents (Studio Health, the Router, the Scheduler, the ownership ledger, the Pattern Library) already exists - this work order sequences and formalizes usage of what is already built, per `studio/STATUS.md`'s rule that AtlasStudio Core is frozen and new process should be production-driven.

The day-in-the-life walkthrough must not fabricate new history in a sibling repository. Where a rejected-implementation example is needed, ground it in the real, already-documented `BUILD-0043` Ashford Shop precedent rather than inventing an unrelated failure. Where an accepted-implementation example is needed, it may be illustrative, but must say so plainly rather than implying a commit was made that was not.

## Submission Record

Submitted 2026-07-08 by Claude Code.

Delivered:

- `studio/operations/DAILY_WORKFLOW.md` - the eleven-step daily production loop (Start of day through Update production status), with dedicated Successful Path and Rejected Path subsections under the Accept-or-Reject step.
- `studio/operations/PRODUCTION_CHECKLIST.md` - the eight-item per-work-item checklist requested, plus usage notes distinguishing "repository confirmed" from "authority confirmed."
- `studio/operations/AGENT_USAGE_GUIDE.md` - strengths, limitations, recommended work types, and explicit "when not to use" guidance for GPT, Claude Code, Codex, GitHub Copilot, and Ollama, plus the Human Creator's non-delegable role, restating (not altering) `studio/agent-roles.md` and `studio/scheduling/agent-scheduler-design.md`'s scoring model, with a quick-reference table.
- `studio/operations/PLAYTEST_AND_ACCEPTANCE.md` - Accepted, Accepted with Notes, Rejected, and Deferred, each with required evidence/documentation/follow-up, and a two-part Ashford Shop case study: the real `BUILD-0043` "NO GO for automatic final map construction" rejection, and the current, still-open Deferred status of the hand-authored rebuild that followed it.
- `studio/operations/REPOSITORY_DECISION_TREE.md` - a walkable decision tree over `repository-authority.md` and `work-order-router.md`'s classification rules, with eight worked examples including the router's own precedent cases and a fresh AtlasStudio-documentation example.
- `reports/operations/atlasstudio-day-in-the-life.md` - a full walkthrough starting from "I want to improve Journey I," narrowing an ambiguous request through the Repository Decision Tree, routing and assigning an agent, validating and playtesting, and recording one Accepted outcome (illustrative, clearly marked as such) and one Rejected outcome (the real `BUILD-0043` precedent). Closes with "How AtlasStudio Evolves," tying the day's outcome back to `studio/STATUS.md`'s frozen-Core principle and `lessons-learned.md`'s finding that unproven architecture should be tested by production use before it is extended.
- This work order, marked `submitted`.

No file in `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` was modified - both were read-only throughout. No existing implementation contract, Design Pattern document, or governance document was modified. No code was written or modified. All seven deliverables are new files.

Formatting: preserved existing house style; no existing file was reformatted.

Verification performed:

```bash
find studio/operations -maxdepth 1 -type f
find reports/operations -maxdepth 1 -type f
find work-orders -name "WO-0029-atlasstudio-daily-operations.md"
git diff --stat -- reports/implementation-contracts studio/design-patterns studio/governance
git -C ../TheLastSwordProtocol-Atlas status --porcelain
git -C ../TheLastSwordProtocol-Game status --porcelain
```
