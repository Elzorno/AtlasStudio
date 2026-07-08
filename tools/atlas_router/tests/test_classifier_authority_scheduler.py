from __future__ import annotations

import unittest

from tools.atlas_router.authority import route
from tools.atlas_router.classifier import classify
from tools.atlas_router.models import WorkOrderRequest
from tools.atlas_router.scheduler import recommend, task_class_for


def req(
    text: str,
    *,
    capabilities: list[str] | None = None,
    project: str = "atlasstudio",
    target_repository: str | None = None,
    approved_by: str | None = None,
    agent_role: str | None = None,
) -> WorkOrderRequest:
    return WorkOrderRequest(
        source_path=None,
        work_order_id="WO-TEST",
        title=text,
        project=project,
        purpose=text,
        required_capabilities=capabilities or [],
        claimed_target_repository=target_repository,
        approved_by=approved_by,
        agent_role=agent_role,
    )


class RouterPlanTests(unittest.TestCase):
    def test_routing_plan_cases(self) -> None:
        cases = [
            (req("Write shopkeeper dialogue for the Ashford general store."), "canon", "TheLastSwordProtocol-Atlas", "routed"),
            (req("Add a new sidequest where the blacksmith asks the player to recover a stolen tool."), "canon", "TheLastSwordProtocol-Atlas", "routed"),
            (req("Decide whether Rowan survives the Iron Marches arc."), "canon", "TheLastSwordProtocol-Atlas", "routed"),
            (req("Wire the Ashford Shop's transfer event in Map003 per IMP-HOM-019.", capabilities=["rpg-maker-json"]), "game_implementation", "AtlasStudio", "pending_approval"),
            (req("Fix a passability bug in Map001 where the player clips through a fence.", capabilities=["rpg-maker-json"]), "game_implementation", "AtlasStudio", "pending_approval"),
            (req("Update System.json to add a new shop item entry for the Ashford Shop.", capabilities=["rpg-maker-json"]), "game_implementation", "AtlasStudio", "pending_approval"),
            (req("Wire the Ashford Shop's transfer event in Map003 per IMP-HOM-019.", capabilities=["rpg-maker-json"], approved_by="Christopher Zornes"), "game_implementation", "TheLastSwordProtocol-Game", "routed"),
            (req("Extend the Planning Engine to weight technical-debt work orders differently.", capabilities=["architecture-review"]), "production_orchestration", "AtlasStudio", "routed"),
            (req("Add a new lint rule to the Canon Linter for duplicate quest IDs.", capabilities=["implementation"], agent_role="implementation-engineer"), "production_orchestration", "AtlasStudio", "routed"),
            (req("Rename a variable in the Graph Diff Engine for clarity."), "production_orchestration", "AtlasStudio", "routed"),
            (req("Build a synchronization report comparing AtlasStudio's imported Atlas entities against Atlas's current export."), "cross_repository_bridge", "AtlasStudio", "routed"),
            (req("Generate a traceability check confirming Map002's built content matches IMP-HOM-018."), "cross_repository_bridge", "AtlasStudio", "routed"),
            (req("Fix the village."), "ambiguous", "none", "blocked_ambiguous"),
            (req("Improve the game."), "ambiguous", "none", "blocked_ambiguous"),
            (req("Add a new sidequest for Ashford Village", target_repository="AtlasStudio"), "canon", "TheLastSwordProtocol-Atlas", "rejected_authority_violation"),
        ]
        for request, classification, repository, status in cases:
            with self.subTest(request=request.title):
                result = classify(request)
                decision = route(request, result)
                self.assertEqual(result.classification, classification)
                self.assertEqual(decision.target_repository, repository)
                self.assertEqual(decision.routing_status, status)

    def test_conflicting_repository_signals_fail_closed(self) -> None:
        for request in [
            req("Add a new quest and wire its map trigger event."),
            req("Update the game's dialogue and also fix a bug in AtlasStudio's Canon Linter."),
        ]:
            with self.subTest(request=request.title):
                result = classify(request)
                decision = route(request, result)
                self.assertEqual(result.classification, "ambiguous")
                self.assertEqual(result.ambiguous_reason, "conflicting_repository_signals")
                self.assertEqual(decision.target_repository, "none")
                self.assertEqual(decision.routing_status, "blocked_ambiguous")

    def test_unknown_project_is_warning_not_blocking(self) -> None:
        request = req(
            "Extend the Planning Engine's scoring.",
            capabilities=["architecture-review"],
            project="unknown-project-not-in-graph",
        )
        decision = route(request, classify(request))
        self.assertEqual(decision.routing_status, "routed")
        self.assertEqual(
            decision.warnings,
            ["unknown_project: 'unknown-project-not-in-graph' not found in Atlas Graph project list"],
        )

    def test_missing_implementation_packet_blocks_approval_progression(self) -> None:
        request = req(
            "Wire the Ashford Shop transfer event.",
            capabilities=["rpg-maker-json"],
            approved_by="Christopher Zornes",
        )
        decision = route(request, classify(request))
        self.assertEqual(decision.routing_status, "pending_approval")
        self.assertEqual(decision.target_repository, "AtlasStudio")
        self.assertTrue(any("Cannot approve" in warning for warning in decision.warnings))

    def test_implementation_packet_with_implementation_context_routes_to_game_implementation(self) -> None:
        cases = [
            "Build Ashford Shop from IMP-HOM-019",
            "Create Ashford Shop from IMP-HOM-019",
            "Add Shopkeeper event from IMP-HOM-019",
            "Wire transfers for IMP-HOM-019",
        ]
        for text in cases:
            with self.subTest(text=text):
                decision = route(req(text), classify(req(text)))
                self.assertEqual(decision.classification, "game_implementation")
                self.assertEqual(decision.target_repository, "AtlasStudio")
                self.assertEqual(decision.routing_status, "pending_approval")

    def test_guardrail_routes_remain_unchanged(self) -> None:
        canon_decision = route(req("Write shopkeeper dialogue"), classify(req("Write shopkeeper dialogue")))
        canon_with_packet = route(
            req("Write shopkeeper dialogue from IMP-HOM-019"),
            classify(req("Write shopkeeper dialogue from IMP-HOM-019")),
        )
        tooling_decision = route(
            req("Create a graph diff tool", capabilities=["implementation"]),
            classify(req("Create a graph diff tool", capabilities=["implementation"])),
        )
        tooling_with_packet = route(
            req("Create a graph diff tool from IMP-HOM-019", capabilities=["implementation"]),
            classify(req("Create a graph diff tool from IMP-HOM-019", capabilities=["implementation"])),
        )
        ambiguous_decision = route(req("Fix the village"), classify(req("Fix the village")))

        self.assertEqual(canon_decision.target_repository, "TheLastSwordProtocol-Atlas")
        self.assertEqual(canon_with_packet.target_repository, "TheLastSwordProtocol-Atlas")
        self.assertEqual(tooling_decision.target_repository, "AtlasStudio")
        self.assertEqual(tooling_with_packet.target_repository, "AtlasStudio")
        self.assertEqual(ambiguous_decision.routing_status, "blocked_ambiguous")
        self.assertEqual(ambiguous_decision.target_repository, "none")

    def test_scheduler_recommendations(self) -> None:
        cases = [
            (req("Write shopkeeper dialogue for the Ashford general store."), "creative_design", "agent.gpt"),
            (req("Decide whether Rowan survives the Iron Marches arc."), "canon_decision", "agent.human"),
            (req("Wire the Ashford Shop's transfer event in Map003 per IMP-HOM-019.", capabilities=["rpg-maker-json"]), "implementation", "agent.codex"),
            (req("Extend the Planning Engine to weight technical-debt work orders differently.", capabilities=["architecture-review"]), "architecture", "agent.claude_code"),
            (req("Rename a variable in the Graph Diff Engine for clarity."), "repetitive_edit", "agent.github_copilot"),
        ]
        for request, expected_task_class, expected_agent in cases:
            with self.subTest(request=request.title):
                classification = classify(request)
                decision = route(request, classification)
                self.assertEqual(task_class_for(request, classification), expected_task_class)
                recommendation = recommend(request, classification, decision)
                self.assertEqual(recommendation.primary_agent, expected_agent)


if __name__ == "__main__":
    unittest.main()
