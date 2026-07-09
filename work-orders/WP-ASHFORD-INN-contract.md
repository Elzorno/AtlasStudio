---
work_order_id: WP-ASHFORD-INN
title: Ashford Inn Pattern-Aware Implementation Contract
status: submitted
project: the-last-sword-protocol
recommended_agent: codex
agent_role: implementation-engineer
risk_level: medium
player_facing: true
engine_specific: true
required_capabilities:
  - documentation
  - rpg-maker-json
  - pattern-application
created: 2026-07-08
---

# WP-ASHFORD-INN - Ashford Inn Pattern-Aware Implementation Contract

## Purpose

Create the authoritative AtlasStudio implementation contract for Ashford Inn from `IMP-HOM-020` (`TheLastSwordProtocol-Atlas`), using the pattern-aware contract format established by `WO-0027`, the Interior and Inn pattern layers, RPG Maker bridge rules, and the current `TheLastSwordProtocol-Game` state as read-only evidence.

## Player-Facing Goal

Indirect but concrete. The contract prepares the Ashford Inn to become a playable free-rest interior with a placeholder Innkeeper (`NPC-ASH-INN-001`), an Inn transfer loop, and pattern-informed layout guidance, while protecting the hand-authored Ashford Exterior and making no canon change.

## Background

An earlier draft of this contract (same deliverable paths) was written when `IMP-HOM-020` did not yet exist in `TheLastSwordProtocol-Atlas`, and correctly gated execution on that missing packet rather than inventing its requirements. `IMP-HOM-020`, its companion screen object `SCR-HOM-ASH-004`, and the Decision Record authorizing the Inn's existence (`DDR-0005`) now exist (`WO-0043`, `TheLastSwordProtocol-Atlas`; renumbered from a duplicate `WO-0038` slot). This work order supersedes that draft with the real, approved packet's actual requirements.

While drafting, a genuine pattern-fit gap was found and is recorded directly rather than smoothed over: `IMP-HOM-020`'s approved single-room design does not satisfy `studio/design-patterns/interiors/inn.pattern.md`'s (`PAT-INTERIOR-INN`) own Required Conditions, which call for a two-zone (common room plus guest wing) structure. `house.pattern.md` does not fit either (its Required Conditions exclude lodging-for-hire). No Specialization-tier pattern in the current library matches a single-room lodging interior. This is resolved per `studio/design-patterns/PATTERN_RESOLUTION_RULES.md`'s "Exceptions" rule (an unmet Required Conditions layer is skipped entirely, not partially applied) and recorded as a project-specific exception in the contract's `Project Pattern` section, rather than either forcing a bad-fit citation or silently dropping the Inn pattern from consideration.

A second, independent finding: AtlasStudio's own pre-existing `WP-03` production package (`projects/the-last-sword-protocol/production/ashford-village-event-plan.md` and siblings) had already envisioned a fuller, two-zone Inn with a production-only (explicitly non-canon) Innkeeper name, "Tomas," predating `IMP-HOM-020`. Per repository authority, `IMP-HOM-020`'s approved design controls wherever the two differ; "Tomas" is retained only as a non-canon AtlasStudio production label, not surfaced as a canon decision.

## Scope

### In Scope

- Rewrite `reports/implementation-contracts/ashford-inn-pattern-aware-contract.md` as the live, authoritative contract executing `IMP-HOM-020`.
- Cite `IMP-HOM-020`, `SCR-HOM-ASH-004`, and `DDR-0005` as Creative Authority / Implementation Packet.
- Evaluate the `Interior` virtual layer and `studio/design-patterns/interiors/inn.pattern.md` as the pattern chain, including the Required Conditions check and its documented exception.
- Define the proposed (unassigned-number) Inn map target and the protected exterior-side `Map001` transfer constraint.
- Define ownership restrictions, passability rules, required transfers/events/NPCs, validation checks, acceptance criteria, and recommended implementation agent.
- Verify no sibling repository or canon file was modified.

### Out of Scope

- Modifying `TheLastSwordProtocol-Game`.
- Modifying `TheLastSwordProtocol-Atlas` or Atlas canon.
- Modifying `IMP-HOM-020`, `SCR-HOM-ASH-004`, or `DDR-0005`.
- Modifying Design Pattern documents or confidence values.
- Modifying any implementation contract other than the Ashford Inn contract.
- Reserving a map number in the Game repo, or adding any Game-repo transfer/event/NPC.
- Reconciling `WP-03`'s production package against `IMP-HOM-020` (flagged as future work, not performed here).

## Inputs

- `../TheLastSwordProtocol-Atlas/atlas/docs/09_Technical/Implementation_Packets/Home_Island/IMP_HOM_020_Manual_Map_Build_Ashford_Inn.md`
- `../TheLastSwordProtocol-Atlas/atlas/docs/02_World/Screens/Home_Island/SCR_HOM_ASH_004_Ashford_Inn.md`
- `../TheLastSwordProtocol-Atlas/atlas/docs/99_Reference/Decision_Records/DDR-0005_Ashford_Inn.md`
- `studio/contracts/PATTERN_CONTRACT_SPEC.md`, `PATTERN_APPLICATION_CHECKLIST.md`
- `studio/design-patterns/PATTERN_INHERITANCE_MODEL.md`, `PATTERN_RESOLUTION_RULES.md`, `PATTERN_APPLICATION_GUIDE.md`, `PATTERN_CONFIDENCE_MODEL.md`
- `studio/design-patterns/interiors/inn.pattern.md`, `house.pattern.md`
- `reports/design-patterns/interior-pattern-corpus-review.md`
- `bridges/rpg-maker-mz/ownership-model.md`, `passability-rule.md`, `map-quality-standard.md`
- `projects/the-last-sword-protocol/design/ashford-village-experience-specification.md`, `production/ashford-village-map-brief.md`, `ashford-village-event-plan.md`, `ashford-village-implementation-checklist.md`
- `../TheLastSwordProtocol-Game/map_ownership.json`, `data/MapInfos.json` (read-only)
- `../TheLastSwordProtocol-Game/data/Map020.json` (read-only pattern evidence)

## Deliverables

- `reports/implementation-contracts/ashford-inn-pattern-aware-contract.md`
- `work-orders/WP-ASHFORD-INN-contract.md`

## Acceptance Criteria

- The contract names authoritative source paths (`IMP-HOM-020`, `SCR-HOM-ASH-004`, `DDR-0005`, `ATLAS-STY-010`, the affected registries) as real, existing files - no missing-packet gate remains.
- The contract defines the target Game map/file, `MapInfos.json`, `map_ownership.json`, the protected `Map001` exterior target, and the read-only sample `Map020`.
- The contract states ownership restrictions and fail-safe behavior for a missing ledger entry and for the `hand_authored` `Map001`.
- The contract cites applicable patterns (`Interior`, `PAT-INTERIOR-INN`), evaluates `PAT-INTERIOR-INN`'s Required Conditions against `IMP-HOM-020`'s actual design, and records the resulting exception explicitly rather than silently forcing or dropping the citation.
- The contract states pattern confidence values without changing any pattern file.
- The contract defines passability rules, route validation, required transfers/events/NPCs, validation checks, acceptance criteria, and a recommended implementation agent with rationale.
- The contract does not modify `TheLastSwordProtocol-Game`.
- The contract does not modify `TheLastSwordProtocol-Atlas` or Atlas canon.
- The Immutable Formatting Rule is preserved.
- This work package is marked `submitted`.

## Verification Steps

```bash
test -f reports/implementation-contracts/ashford-inn-pattern-aware-contract.md
test -f work-orders/WP-ASHFORD-INN-contract.md
rg -n "IMP-HOM-020|PAT-INTERIOR-INN|Required Conditions|Tomas|Codex" reports/implementation-contracts/ashford-inn-pattern-aware-contract.md
git diff --stat -- studio/design-patterns
git diff --stat -- ../TheLastSwordProtocol-Atlas
git diff --stat -- ../TheLastSwordProtocol-Game
python3 tools/atlas_format/format_guard.py --check
git -C ../TheLastSwordProtocol-Atlas status --porcelain
git -C ../TheLastSwordProtocol-Game status --porcelain
```

## Allowed Changes

- `reports/implementation-contracts/ashford-inn-pattern-aware-contract.md`
- `work-orders/WP-ASHFORD-INN-contract.md`

## Protected Areas

- Do not modify `TheLastSwordProtocol-Game`.
- Do not modify `TheLastSwordProtocol-Atlas` or Atlas canon.
- Do not modify Design Pattern Library files.
- Do not modify any implementation contract other than the Ashford Inn contract.
- Preserve the Immutable Formatting Rule.

## Notes for Assigned Agent

This is a contract-drafting package, not the Inn implementation itself. Two execution gates remain before implementation can begin, both stated in the contract: a map number must be reserved in `map_ownership.json`/`MapInfos.json`, and the additive `TRN-HOM-031` edit to `Map001` must be explicitly approved as work against a `hand_authored` map. Do not treat this submitted contract as permission to touch the Game repo.

## Submission Record

Submitted 2026-07-08 by Claude Code.

Delivered:

- `reports/implementation-contracts/ashford-inn-pattern-aware-contract.md` - rewritten as the live, authoritative pattern-aware contract, now that `IMP-HOM-020` exists. Cites `IMP-HOM-020`/`SCR-HOM-ASH-004`/`DDR-0005` as Creative Authority and Implementation Packet; cites `Interior` (virtual, High) as the resolving Environment layer; evaluates `Inn` (`PAT-INTERIOR-INN` v1.0, Medium) against its own Required Conditions, finds them unmet by `IMP-HOM-020`'s single-room design, and records that as a project-specific exception per `PATTERN_RESOLUTION_RULES.md` rather than forcing or silently dropping the citation; defines the proposed map target, ownership restrictions (including the `Map001` additive-approval gate), passability rules and route validation, required transfers/events/NPCs (`TRN-HOM-031`/`032`, `EVT-HOM-032`), validation requirements, acceptance criteria (`IMP-HOM-020`'s nine plus two contract-level execution gates), and Codex as the recommended implementation agent with stated rationale. Also reconciles AtlasStudio's own pre-existing, non-canon "Tomas" production label against Atlas's unnamed canon roster entry, and flags `WP-03`'s production package as stale relative to `IMP-HOM-020` for a future reconciliation pass.
- This work package, marked `submitted`.

No file in `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` was modified - both were read-only throughout. No Design Pattern document or its confidence value was modified. No other implementation contract was modified.

Formatting: preserved existing house style; no broad reformatting performed.

Verification performed:

```bash
test -f reports/implementation-contracts/ashford-inn-pattern-aware-contract.md
test -f work-orders/WP-ASHFORD-INN-contract.md
git diff --stat -- studio/design-patterns
git -C ../TheLastSwordProtocol-Atlas status --porcelain
git -C ../TheLastSwordProtocol-Game status --porcelain
python3 tools/atlas_format/format_guard.py --check
```
