"""WO-0075: tests for the automated render-based visual critic.

Covers the rubric/overall logic, the backends, the calibration go/no-go
(including that it genuinely discriminates -- a rubber-stamp backend must
fail it), the model-JSON parsing used by the live backends, and the advisory
integration into the WO-0072 quality gate (a render reject blocks; a render
pass never manufactures acceptance; and callers that pass no critique keep
byte-identical behaviour).

Runs under plain unittest (this project has no pytest installed):
    python3 tests/test_visual_critic.py
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

COMPILER_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(COMPILER_DIR))

from visual_critic import (  # noqa: E402
    COVERED_AVCP_REFS,
    RUBRIC,
    RUBRIC_BY_ID,
    AnthropicVisionBackend,
    CriterionResult,
    CritiqueRequest,
    OllamaVisionBackend,
    RecordedCritiqueBackend,
    VisualCritique,
    _critique_from_model_json,
    _extract_json,
    recorded_calibration_backend,
    run_calibration,
    session_frontier_critiques,
    write_critique_evidence,
)
import quality_gate  # noqa: E402
from quality_gate import audit_visual_render, run_dual_gate  # noqa: E402

FIXTURES = COMPILER_DIR / "prototypes" / "wo0071"


def load_fixture(stem: str) -> tuple[dict, dict]:
    plan = json.loads((FIXTURES / f"{stem}.map_plan.json").read_text(encoding="utf-8"))
    manifest = json.loads((FIXTURES / f"{stem}.generation_manifest.json").read_text(encoding="utf-8"))
    return plan, manifest


def all_pass() -> dict[str, tuple[str, str]]:
    return {c.id: ("pass", "ok") for c in RUBRIC}


def critique(label: str, **overrides: tuple[str, str]) -> VisualCritique:
    verdicts = all_pass()
    verdicts.update(overrides)
    return VisualCritique.from_verdicts(
        label=label, image_ref=f"{label}.png", backend="test", model="test", verdicts=verdicts
    )


class RubricTests(unittest.TestCase):
    def test_rubric_has_stable_ids_and_seven_core(self) -> None:
        self.assertEqual(len(RUBRIC), len(RUBRIC_BY_ID))
        core = [c for c in RUBRIC if c.core]
        self.assertEqual(len(core), 7)

    def test_critic_covers_exactly_the_gate_deferred_constraints(self) -> None:
        # The whole point: the critic automates precisely the AVCP ids the
        # WO-0072 gate parked in NOT_YET_AUTOMATABLE -- no more, no fewer.
        self.assertEqual(set(COVERED_AVCP_REFS), set(quality_gate.NOT_YET_AUTOMATABLE))


class OverallLogicTests(unittest.TestCase):
    def test_all_pass_is_pass(self) -> None:
        self.assertEqual(critique("m").overall, "pass")

    def test_core_fail_rejects(self) -> None:
        self.assertEqual(critique("m", **{"ENCLOSURE-001": ("fail", "open field")}).overall, "reject")

    def test_noncore_fail_flags(self) -> None:
        self.assertEqual(critique("m", **{"WATER-LANDMARK-001": ("fail", "no water")}).overall, "flag")

    def test_three_partials_flag_but_two_pass(self) -> None:
        two = critique("m", **{"FIRST-VIEW-001": ("partial", "a"), "REWARD-CLUSTER-001": ("partial", "b")})
        self.assertEqual(two.overall, "pass")
        three = critique(
            "m",
            **{
                "FIRST-VIEW-001": ("partial", "a"),
                "REWARD-CLUSTER-001": ("partial", "b"),
                "WATER-LANDMARK-001": ("partial", "c"),
            },
        )
        self.assertEqual(three.overall, "flag")

    def test_invalid_verdict_rejected(self) -> None:
        with self.assertRaises(ValueError):
            CriterionResult("ENCLOSURE-001", "maybe", "x")


class FromVerdictsTests(unittest.TestCase):
    def test_missing_criteria_filled_partial(self) -> None:
        c = VisualCritique.from_verdicts(
            label="m", image_ref="m.png", backend="b", model="x",
            verdicts={"ENCLOSURE-001": ("pass", "walled")},
        )
        self.assertEqual(len(c.results), len(RUBRIC))
        filled = {r.criterion_id: r.verdict for r in c.results}
        self.assertEqual(filled["ENCLOSURE-001"], "pass")
        self.assertEqual(filled["PATH-ORGANIC-001"], "partial")


class RecordedBackendTests(unittest.TestCase):
    def test_replays_and_refuses_unknown(self) -> None:
        backend = RecordedCritiqueBackend({"known": critique("known")})
        got = backend.critique(CritiqueRequest(label="known", candidate_image="k.png"))
        self.assertEqual(got.overall, "pass")
        with self.assertRaises(KeyError):
            backend.critique(CritiqueRequest(label="unseen", candidate_image="u.png"))


class CalibrationTests(unittest.TestCase):
    def test_recorded_frontier_backend_passes_calibration(self) -> None:
        result = run_calibration(recorded_calibration_backend())
        self.assertTrue(result.passed, result.to_dict())
        by_label = {r.label: r for r in result.rows}
        self.assertEqual(by_label["map017"].actual, "pass")
        self.assertEqual(by_label["map001"].actual, "pass")
        self.assertEqual(by_label["wo0073_candidate"].actual, "reject")

    def test_rubber_stamp_backend_fails_calibration(self) -> None:
        # A backend that "passes everything" must NOT pass calibration, or the
        # harness would be a rubber stamp.
        rubber = RecordedCritiqueBackend(
            {"map017": critique("map017"), "map001": critique("map001"), "wo0073_candidate": critique("wo0073_candidate")}
        )
        self.assertFalse(run_calibration(rubber).passed)

    def test_reject_without_required_reasons_fails_calibration(self) -> None:
        # Rejecting the WO-0073 candidate is not enough; it must reject for the
        # right (enclosure/path/material) reasons.
        wrong_reasons = critique(
            "wo0073_candidate",
            **{"DECOR-DENSITY-001": ("fail", "empty"), "DOMINANT-LANDMARK-001": ("fail", "none")},
        )
        self.assertEqual(wrong_reasons.overall, "reject")
        backend = RecordedCritiqueBackend(
            {"map017": critique("map017"), "map001": critique("map001"), "wo0073_candidate": wrong_reasons}
        )
        result = run_calibration(backend)
        self.assertFalse(result.passed)

    def test_evidence_roundtrips(self) -> None:
        import tempfile

        crit = session_frontier_critiques()["wo0073_candidate"]
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "c.json"
            write_critique_evidence(crit, out)
            reloaded = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(reloaded["overall"], "reject")
        self.assertEqual(reloaded["label"], "wo0073_candidate")


class ModelParsingTests(unittest.TestCase):
    def test_extract_json_from_fence_and_prose(self) -> None:
        self.assertEqual(_extract_json('```json\n{"a": 1}\n```')["a"], 1)
        self.assertEqual(_extract_json('Sure!\n{"a": 2}\nDone.')["a"], 2)

    def test_critique_from_model_json_ignores_junk(self) -> None:
        payload = {
            "results": [
                {"criterion_id": "ENCLOSURE-001", "verdict": "fail", "reason": "open field"},
                {"criterion_id": "NOT-A-REAL-ID", "verdict": "fail", "reason": "ignored"},
                {"criterion_id": "PATH-ORGANIC-001", "verdict": "banana", "reason": "bad verdict ignored"},
            ]
        }
        c = _critique_from_model_json(
            payload, request=CritiqueRequest(label="m", candidate_image="m.png"), backend="ollama", model="llava"
        )
        by_id = {r.criterion_id: r.verdict for r in c.results}
        self.assertEqual(by_id["ENCLOSURE-001"], "fail")
        self.assertEqual(by_id["PATH-ORGANIC-001"], "partial")  # bad verdict -> filled
        self.assertNotIn("NOT-A-REAL-ID", by_id)

    def test_live_backends_construct_without_calling(self) -> None:
        # Constructing must not require a running server or an API key.
        self.assertEqual(OllamaVisionBackend().name, "ollama")
        self.assertEqual(AnthropicVisionBackend(api_key="").name, "anthropic")


class GateIntegrationTests(unittest.TestCase):
    def test_audit_visual_render_core_fail_is_error(self) -> None:
        result = audit_visual_render(critique("m", **{"ENCLOSURE-001": ("fail", "open field")}))
        self.assertFalse(result.passed)
        self.assertTrue(any(f.severity == "error" for f in result.findings))

    def test_audit_visual_render_all_pass_is_clean(self) -> None:
        result = audit_visual_render(critique("m"))
        self.assertTrue(result.passed)
        self.assertEqual(result.findings, [])

    def test_render_reject_blocks_an_otherwise_passing_candidate(self) -> None:
        plan, manifest = load_fixture("core-seed-1")
        baseline = run_dual_gate(plan, manifest)
        self.assertEqual(baseline.recommendation, "candidate_for_human_review")
        rejected = run_dual_gate(
            plan, manifest, visual_critique=critique("core-seed-1", **{"PATH-ORGANIC-001": ("fail", "rigid cross")})
        )
        self.assertEqual(rejected.recommendation, "rejected")
        self.assertIn("visual_render", rejected.to_dict())

    def test_render_pass_does_not_manufacture_acceptance(self) -> None:
        plan, manifest = load_fixture("core-seed-1")
        result = run_dual_gate(plan, manifest, visual_critique=critique("core-seed-1"))
        # Still only a candidate for human review -- never "accepted".
        self.assertEqual(result.recommendation, "candidate_for_human_review")
        self.assertTrue(result.to_dict()["visual_render"]["passed"])

    def test_no_critique_keeps_wo0072_behaviour(self) -> None:
        plan, manifest = load_fixture("core-seed-1")
        result = run_dual_gate(plan, manifest)
        self.assertIsNone(result.visual_render)
        self.assertNotIn("visual_render", result.to_dict())


if __name__ == "__main__":
    unittest.main()
