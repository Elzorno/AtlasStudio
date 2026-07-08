# Work Order Router - Routing Test Plan

## Status

Specification only. Each case below becomes one fixture file under `tools/atlas_router/tests/fixtures/case_NN_<slug>.md` (a minimal work order Markdown file carrying just enough frontmatter and body text to exercise the case) plus one assertion in `tools/atlas_router/tests/test_classifier.py` / `test_authority.py` / `test_scheduler.py`. Codex should not invent additional judgment when writing these fixtures - the Input column below is the fixture's `## Purpose` text (and `--capability` flags, where named), and every Expected column is a literal assertion.

## How "Expected Agent" Was Derived

Every "Expected Agent" value below is computed by running `studio/scheduling/agent-scheduler-design.md`'s existing Agent Capability Profiles table and Task Classification signals against the case's `task_class` (mapped from the router classification per `IMPLEMENTATION_SPEC.md`'s `scheduler.py` table), not asserted by intuition. Where a case's target repository is not `AtlasStudio`, the agent is marked `(advisory)` - AtlasStudio's scheduler may compute a recommendation to attach to a proposal, but final assignment authority for `TheLastSwordProtocol-Atlas` and `TheLastSwordProtocol-Game` belongs to those repositories' own processes, per `studio/governance/repository-authority.md`.

## Canon Cases (route to `TheLastSwordProtocol-Atlas`)

| # | Input (Purpose / capabilities) | Signals Matched | Expected Classification | Expected Repository | Expected Task Class | Expected Agent | Expected Routing Status |
|---|---|---|---|---|---|---|---|
| 1 | "Write shopkeeper dialogue for the Ashford general store." | canon noun: dialogue | canon | TheLastSwordProtocol-Atlas | creative_design | agent.gpt (advisory) | routed |
| 2 | "Add a new sidequest where the blacksmith asks the player to recover a stolen tool." | canon nouns: quest, character (blacksmith) | canon | TheLastSwordProtocol-Atlas | creative_design | agent.gpt (advisory) | routed |
| 3 | "Update the protagonist's backstory to explain the new sidequest." | canon noun: protagonist, backstory | canon | TheLastSwordProtocol-Atlas | creative_design | agent.gpt (advisory) | routed - **and must not be accepted into AtlasStudio's own canon graph even provisionally**, per `WO-0018` |
| 4 | "Decide whether Rowan survives the Iron Marches arc." | canon noun: character; finality verb "decide" | canon | TheLastSwordProtocol-Atlas | canon_decision | agent.human (advisory - Atlas's own Production Director makes the actual call) | routed |
| 5 | "Rename the Whisperwood region to Whisperfen." | canon noun: region | canon | TheLastSwordProtocol-Atlas | creative_design | agent.gpt (advisory) | routed |
| 6 | "Add lore explaining why the Covenant of Ash corrupts relay nodes." | canon nouns: lore, faction, infrastructure | canon | TheLastSwordProtocol-Atlas | creative_design | agent.gpt (advisory) | routed |

## Game Implementation Cases (route to `TheLastSwordProtocol-Game`, gated)

| # | Input | Signals Matched | Expected Classification | Expected Repository | Expected Task Class | Expected Agent | Expected Routing Status |
|---|---|---|---|---|---|---|---|
| 7 | "Wire the Ashford Shop's transfer event in Map003 per IMP-HOM-019." `required_capabilities: [rpg-maker-json]` | rpg-maker-json capability + named Map003 file | game_implementation | AtlasStudio (implementation contract) | implementation | agent.codex (advisory) | pending_approval |
| 8 | "Fix a passability bug in Map001 where the player clips through a fence." `required_capabilities: [rpg-maker-json]` | rpg-maker-json capability + named Map001 file | game_implementation | AtlasStudio (implementation contract) | implementation | agent.codex (advisory) | pending_approval |
| 9 | "Add a new NPC sprite event reference to Map002's event list." `required_capabilities: [rpg-maker-json]` | rpg-maker-json capability + named Map002 file | game_implementation | AtlasStudio (implementation contract) | implementation | agent.codex (advisory) | pending_approval |
| 10 | "Update System.json to add a new shop item entry for the Ashford Shop." `required_capabilities: [rpg-maker-json]` | rpg-maker-json capability + named System.json file | game_implementation | AtlasStudio (implementation contract) | implementation | agent.codex (advisory) | pending_approval |
| 11 | Same as #7, invoked via `atlas wo dispatch --approved-by "Christopher Zornes" --approved-at 2026-07-07` | same, plus approval evidence present | game_implementation | TheLastSwordProtocol-Game | implementation | agent.codex (advisory) | routed (moved past pending_approval only because approval evidence was supplied) |
| 12 | "Regenerate Map001 from scratch using the pipeline generator." `required_capabilities: [rpg-maker-json]` | rpg-maker-json capability + named Map001 file, but Map001 is `PROTECTED_BY ownership_state.hand_authored` per `map_ownership.json` | game_implementation | AtlasStudio (implementation contract) | implementation | agent.codex (advisory) | pending_approval, **with an additional `safety_flags` note that approval alone is insufficient - the human approver must also confirm awareness of `map_ownership.json`'s protected status before dispatch, since this targets hand-authored content** |

## Production/Orchestration Cases (route to AtlasStudio)

| # | Input | Signals Matched | Expected Classification | Expected Repository | Expected Task Class | Expected Agent | Expected Routing Status |
|---|---|---|---|---|---|---|---|
| 13 | "Extend the Planning Engine to weight technical-debt work orders differently." `required_capabilities: [architecture-review]` | architecture-review capability + names tools/atlas_planner/ | production_orchestration | AtlasStudio | architecture | agent.claude_code | routed |
| 14 | "Add a new lint rule to the Canon Linter for duplicate quest IDs." `required_capabilities: [implementation]`, `agent_role: implementation-engineer` | agent_role implementation-engineer -> implementation | production_orchestration | AtlasStudio | implementation | agent.codex | routed |
| 15 | "Rename a variable in the Graph Diff Engine for clarity." title keyword "rename" | title keyword rename -> repetitive_edit | production_orchestration | AtlasStudio | repetitive_edit | agent.github_copilot | routed |
| 16 | "Write a summary report of this week's Studio Doctor findings." title keyword "summary/report" | title keyword summary -> review_qa | production_orchestration | AtlasStudio | review_qa | agent.ollama | routed |
| 17 | "Design a new capability scoring dimension for the Agent Scheduler." `agent_role: senior-software-architect` | agent_role senior-software-architect -> architecture | production_orchestration | AtlasStudio | architecture | agent.claude_code | routed |
| 18 | "Document the Work Order Router's classification rules." `agent_role: senior-software-architect` | agent_role senior-software-architect -> architecture; names studio/orchestration/ | production_orchestration | AtlasStudio | architecture | agent.claude_code | routed |

## Cross-Repository Bridge Cases (route to AtlasStudio, `bridges/`)

| # | Input | Signals Matched | Expected Classification | Expected Repository | Expected Task Class | Expected Agent | Expected Routing Status |
|---|---|---|---|---|---|---|---|
| 19 | "Build a synchronization report comparing AtlasStudio's imported Atlas entities against Atlas's current export." | describes comparing already-imported content, no new content proposed | cross_repository_bridge | AtlasStudio | architecture | agent.claude_code | routed |
| 20 | "Generate a traceability check confirming Map002's built content matches IMP-HOM-018." | traceability/verification of existing imported content | cross_repository_bridge | AtlasStudio | architecture | agent.claude_code | routed |
| 21 | "Propose the Graph Diff Engine to TheLastSwordProtocol-Atlas as an adoptable tool." | proposal of AtlasStudio's own retained tooling per `repository-authority.md`'s change flow, not a canon or content ask | cross_repository_bridge | AtlasStudio (dispatch opens a GitHub issue in Atlas per the change-flow rule, but authorship/target classification stays AtlasStudio) | architecture | agent.claude_code | routed |
| 22 | "Summarize the current Atlas synchronization status for human review." | describes summarizing already-imported/synced content for a human | cross_repository_bridge | AtlasStudio | review_qa | agent.ollama | routed |

## Ambiguous and Edge Cases

| # | Input | Why It's Hard | Expected Classification | Expected Repository | Expected Routing Status | Notes |
|---|---|---|---|---|---|---|
| 23 | "Fix the village." | No signal matches any row: no named location, no named defect, no stated content area | ambiguous | none | blocked_ambiguous | `ambiguous_reason: "no_signal_matched"` |
| 24 | "Add a new quest and wire its map trigger event." | Matches both a canon signal (quest) and a game_implementation signal (map trigger event) in one request | ambiguous | none | blocked_ambiguous | `ambiguous_reason: "conflicting_repository_signals"`, `conflicting_classifications: ["canon", "game_implementation"]`; rationale instructs splitting into two separate requests |
| 25 | "Improve the game." | No owned-content noun matched; too vague to classify | ambiguous | none | blocked_ambiguous | `ambiguous_reason: "no_signal_matched"` |
| 26 | "Make things better." with empty `required_capabilities` and empty scope bullets | No signals of any kind present | ambiguous | none | blocked_ambiguous | `ambiguous_reason: "no_signal_matched"`; this is the minimum-input degenerate case |
| 27 | "Extend the Planning Engine's scoring." with `project: unknown-project-not-in-graph` | Classification signals still resolve normally; the unrecognized `project` value is not itself a classification signal | production_orchestration | AtlasStudio | routed | Non-fatal: output includes `"warnings": ["unknown_project: 'unknown-project-not-in-graph' not found in Atlas Graph project list"]`; does not block routing (see `ERROR_HANDLING.md`) |
| 28 | "Wire the Ashford Shop transfer event." `required_capabilities: [rpg-maker-json]`, but no `IMP-HOM-*` packet id anywhere in Purpose/Scope | rpg-maker-json + map-shaped noun ("transfer event") still matches game_implementation, but no implementation packet is cited | game_implementation | AtlasStudio (implementation contract) | pending_approval, and additionally **cannot progress to approved even with `--approved-by`** until an implementation packet id is cited | See `ERROR_HANDLING.md`, "missing implementation packet" - this is a harder block than ordinary `pending_approval` |
| 29 | "Update the game's dialogue and also fix a bug in AtlasStudio's Canon Linter." | Bundles a canon-repository ask and an AtlasStudio-repository ask that are unrelated to each other (not the same feature split across repos like #24, but two independent asks) | ambiguous | none | blocked_ambiguous | `ambiguous_reason: "conflicting_repository_signals"`; rationale explicitly says these are unrelated asks and must be filed as two separate work orders, not one |
| 30 | "Add a new sidequest for Ashford Village" submitted with a self-declared frontmatter override `target_repository: AtlasStudio` | Canon content signal fires (quest, location), but the requester (human or agent) explicitly tried to force the target to AtlasStudio | canon (classifier ignores the override entirely) | TheLastSwordProtocol-Atlas (never AtlasStudio, regardless of the override) | **rejected_authority_violation** | `safety_flags.canon_leak_risk = true`. This is the literal test of the constraint "the router must never silently move canon into AtlasStudio" - it must be present and must pass before this package is considered complete |

## Coverage Checklist

- [ ] All five classifications (`canon`, `game_implementation`, `production_orchestration`, `cross_repository_bridge`, `ambiguous`) appear at least four times each.
- [ ] All six scheduler task classes (`creative_design`, `architecture`, `implementation`, `repetitive_edit`, `review_qa`, `canon_decision`) appear at least once.
- [ ] All four `routing_status` values (`routed`, `pending_approval`, `blocked_ambiguous`, `rejected_authority_violation`) appear at least twice.
- [ ] Case 30 (forced canon-to-AtlasStudio override) passes - this is the release-blocking case; the implementation is not acceptable if this case fails.
- [ ] Case 12 (protected/hand-authored content) passes - approval evidence alone is not sufficient when the target is `PROTECTED_BY ownership_state.hand_authored`.
- [ ] Case 24 and case 29 are both `blocked_ambiguous` but for different reasons (a single request spanning two repositories' owned content vs. two unrelated bundled asks); both must be distinguishable in the stored rationale text, not collapsed into identical output.

## Running the Suite (once implemented)

```bash
python3 -m pytest tools/atlas_router/tests/ -v
```

Every fixture file's expected values in this document are the assertions in that suite - there should be no assertion in `tools/atlas_router/tests/` that cannot be traced back to a row in this table or to a rule already stated in `studio/orchestration/work-order-router.md`.
