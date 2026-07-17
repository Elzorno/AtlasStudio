"""WO-0072: dual structural + visual quality gate tests.

Runs the gate against the real WO-0071 Ashford fixtures (both audits must
pass independently), and proves neither audit can offset the other's
failure in both directions. Also runs a negative-control regression derived
from the documented 2026-07-14 Ashford v2 rejection reasons (half-trees,
excessive building height -- see
`rpgmakerLSP/reports/atlas-import/ashford-exterior-rebuild-v2/rebuild-report.md`)
-- not a full MapPlan translation of that candidate's raw RPG Maker JSON,
which predates the TileAssembly/MapVision contracts entirely and carries no
`tile_assembly_*` provenance to translate.
"""

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

COMPILER_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(COMPILER_DIR))

from quality_gate import (  # noqa: E402
    HumanDecisionError,
    apply_human_decision,
    audit_structural,
    audit_visual_proxy,
    record_gate_evidence,
    run_dual_gate,
)

FIXTURES = COMPILER_DIR / "prototypes" / "wo0071"


def load_fixture(stem: str) -> tuple[dict, dict]:
    plan = json.loads((FIXTURES / f"{stem}.map_plan.json").read_text(encoding="utf-8"))
    manifest = json.loads((FIXTURES / f"{stem}.generation_manifest.json").read_text(encoding="utf-8"))
    return plan, manifest


class RealFixtureTests(unittest.TestCase):
    def test_all_wo0071_fixtures_pass_both_audits_independently(self) -> None:
        for stem in ("core-seed-1", "core-seed-2", "dressed-seed-1", "dressed-seed-2"):
            with self.subTest(stem=stem):
                plan, manifest = load_fixture(stem)
                result = run_dual_gate(plan, manifest)
                self.assertTrue(result.structural.passed, result.structural.findings)
                self.assertTrue(result.visual_proxy.passed, result.visual_proxy.findings)
                self.assertEqual("candidate_for_human_review", result.recommendation)

    def test_missing_manifest_fails_structural_only(self) -> None:
        plan, _ = load_fixture("core-seed-1")
        result = run_dual_gate(plan, generation_manifest=None)
        self.assertFalse(result.structural.passed)
        self.assertTrue(result.visual_proxy.passed)
        self.assertEqual("rejected", result.recommendation)


class GateIndependenceTests(unittest.TestCase):
    """Neither audit may offset the other's failure, in either direction."""

    def test_structurally_broken_candidate_is_rejected_even_with_clean_visuals(self) -> None:
        plan, manifest = load_fixture("core-seed-1")
        broken = copy.deepcopy(plan)
        broken["validation"]["must_reach"].append("nonexistent_zone")
        result = run_dual_gate(broken, manifest)
        self.assertFalse(result.structural.passed)
        self.assertTrue(result.visual_proxy.passed)
        self.assertEqual("rejected", result.recommendation)
        self.assertEqual("required_zones_missing", result.structural.findings[0].code)

    def test_visually_broken_candidate_is_rejected_even_with_clean_structure(self) -> None:
        plan, manifest = load_fixture("core-seed-1")
        broken = copy.deepcopy(plan)
        for obstacle in broken["obstacles"]:
            if obstacle["name"] == "ashford_inn":
                obstacle["tile_assembly_review_state"] = "human_rejected"
        result = run_dual_gate(broken, manifest)
        self.assertTrue(result.structural.passed)
        self.assertFalse(result.visual_proxy.passed)
        self.assertEqual("rejected", result.recommendation)
        self.assertEqual(
            "ASH-ASSEMBLY-001_002_incomplete_or_unverified_assembly",
            result.visual_proxy.findings[0].code,
        )

    def test_dimension_attractive_but_structurally_invalid_candidate_fails(self) -> None:
        # A candidate with an obstacle whose parent zone was deleted --
        # visually indistinguishable, structurally broken.
        plan, manifest = load_fixture("dressed-seed-1")
        broken = copy.deepcopy(plan)
        broken["terrain"] = [z for z in broken["terrain"] if z["terrain_type"] != "shop_frontage"]
        result = run_dual_gate(broken, manifest)
        self.assertFalse(result.structural.passed)
        codes = {f.code for f in result.structural.findings}
        self.assertTrue({"required_zones_missing", "obstacle_parent_zone_missing"} & codes)
        self.assertEqual("rejected", result.recommendation)


class NegativeControlTests(unittest.TestCase):
    """Regression derived from the documented 2026-07-14 Ashford v2 rejection.

    See rebuild-report.md: "trees show only the bottom half of a two-tile
    set, the buildings are too tall and do not match the references". This
    is a minimal, clearly-labeled stand-in encoding those two documented
    facts (a tree with no verified assembly binding; the Inn's real
    pre-authored-pack height of 7 rows, cited in
    REFERENCE-FIDELITY-REVIEW.md), not a full translation of the preserved
    Map001.reconciled-candidate.json.
    """

    def test_rejected_v2_fails_complete_tree_and_building_proportion_checks(self) -> None:
        # This fixture has no broadleaf_tree obstacle in the "core" beats
        # combination -- use "dressed", which does.
        plan, _ = load_fixture("dressed-seed-1")
        broken = copy.deepcopy(plan)
        for obstacle in broken["obstacles"]:
            if obstacle["name"] == "broadleaf_tree" and obstacle["obstacle_id"].endswith("-1"):
                obstacle.pop("tile_assembly_ref", None)
                obstacle.pop("tile_assembly_review_state", None)
            if obstacle["name"] == "ashford_inn":
                obstacle["tile_assembly_height"] = 7
                obstacle["tile_assembly_building_height_rows"] = 7

        result = audit_visual_proxy(broken)
        self.assertFalse(result.passed)
        codes = {f.code for f in result.findings}
        self.assertIn("ASH-ASSEMBLY-001_002_incomplete_or_unverified_assembly", codes)
        self.assertIn("ASH-BUILD-001_excessive_building_height", codes)


class EvidencePersistenceTests(unittest.TestCase):
    def test_evidence_is_persisted_with_pending_human_decision(self) -> None:
        plan, manifest = load_fixture("core-seed-1")
        result = run_dual_gate(plan, manifest)
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            output_path = Path(tmp) / "evidence.json"
            evidence = record_gate_evidence(
                result,
                concept_refs=["Concepts/Ashford/ashford-overhead-composition-v2.png"],
                render_refs=["prototypes/wo0071/core-seed-1.svg"],
                output_path=output_path,
            )
            self.assertEqual("pending", evidence["human_decision"]["status"])
            self.assertIsNone(evidence["human_decision"]["decision"])
            reloaded = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(evidence, reloaded)

    def test_only_chris_may_record_acceptance(self) -> None:
        plan, manifest = load_fixture("core-seed-1")
        result = run_dual_gate(plan, manifest)
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            output_path = Path(tmp) / "evidence.json"
            record_gate_evidence(result, concept_refs=[], render_refs=[], output_path=output_path)
            with self.assertRaises(HumanDecisionError):
                apply_human_decision(output_path, decision="accepted", decided_by="Codex", decided_at="2026-07-15")
            applied = apply_human_decision(
                output_path, decision="accepted_with_notes", decided_by="Chris", decided_at="2026-07-15", notes="looks right"
            )
            self.assertEqual("Chris", applied["human_decision"]["decided_by"])
            self.assertEqual("recorded", applied["human_decision"]["status"])

    def test_cannot_accept_a_rejected_candidate(self) -> None:
        plan, manifest = load_fixture("core-seed-1")
        broken = copy.deepcopy(plan)
        broken["validation"]["must_reach"].append("nonexistent_zone")
        result = run_dual_gate(broken, manifest)
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            output_path = Path(tmp) / "evidence.json"
            record_gate_evidence(result, concept_refs=[], render_refs=[], output_path=output_path)
            with self.assertRaises(HumanDecisionError):
                apply_human_decision(output_path, decision="accepted", decided_by="Chris", decided_at="2026-07-15")
            # Chris may still explicitly record the rejection.
            applied = apply_human_decision(output_path, decision="rejected", decided_by="Chris", decided_at="2026-07-15")
            self.assertEqual("rejected", applied["human_decision"]["decision"])


if __name__ == "__main__":
    unittest.main()
