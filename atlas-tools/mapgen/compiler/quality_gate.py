"""WO-0072: dual structural + visual quality gate for MapVision-integrated
generated candidates.

Two audits are computed completely independently and neither can offset the
other's failure: `audit_structural` retains the existing route/collision/
event/transfer/ownership/manifest hard-gate family (WO-0056/0062's own
vocabulary, re-verified here rather than assumed from "the assembler didn't
raise"), and `audit_visual_proxy` adds the MapVision-derived checks that are
mechanically verifiable from a MapPlan's own `tile_assembly_*` provenance
(WO-0071) without an actual rendered image.

Deliberately out of scope, and listed rather than silently skipped: every
`AVCP-HOM-ASH-001` constraint whose own `measurement_policy` requires a
rendered image and a blind human panel (first-camera salience, color/material
dominant-share, path-rhythm bend counting, density-zone pixel occupancy) --
see `NOT_YET_AUTOMATABLE`. This gate recommends, it never accepts: only
`apply_human_decision` can record final visual acceptance, and only when
called with `decided_by="Chris"`.
"""

from __future__ import annotations

import json
import sys
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from quality_auditor import AuditResult, Finding
from visual_critic import VisualCritique  # WO-0075: render-based aesthetic critic

COMPILER_DIR = Path(__file__).resolve().parent
WORKSPACE = COMPILER_DIR.parents[3]
sys.path.insert(0, str(WORKSPACE / "rpgmakerLSP" / "tools" / "atlas-import"))
from map_ownership_guard import load_ledger, map_write_allowed  # noqa: E402


# TileAssembly review_state values that must never be treated as a complete,
# placement-safe object -- mirrors WO-0070/0071's own enablement vocabulary.
BLOCKED_REVIEW_STATES = {
    "study_only",
    "blocked_for_ashford",
    "human_rejected",
    "human_corrected_bridge_reference",
    "unreviewed",
}

# ASH-BUILD-001's provisional operational threshold (AVCP-HOM-ASH-001).
MAX_APPROVED_BUILDING_HEIGHT_ROWS = 5

CANONICAL_BUILDING_TAGS = ("elara_house", "ashford_shop", "ashford_inn", "ashford_elder_house")

REQUIRED_MANIFEST_FIELDS = {
    "schema_version", "manifest_id", "map_intent_ref", "generator_ref",
    "archetype_ref", "layout_family_ref", "style_pack_ref", "seed",
    "contract_version", "generated_at", "status",
}

# AVCP-HOM-ASH-001 constraints whose measurement_policy requires an actual
# rendered image plus a blind human panel; this gate reports them as
# explicitly not-yet-automatable rather than silently omitting them.
NOT_YET_AUTOMATABLE = (
    "ASH-FIRST-001", "ASH-FIRST-002", "ASH-BUILD-002", "ASH-PATH-002",
    "ASH-PATH-003", "ASH-RHYTHM-001", "ASH-DENSITY-001", "ASH-MATERIAL-001",
    "ASH-MATERIAL-002", "ASH-VOCAB-001",
)


def audit_structural(
    map_plan: dict[str, Any],
    generation_manifest: dict[str, Any] | None = None,
    *,
    project_root: Path | None = None,
    target_map_id: int | None = None,
) -> AuditResult:
    """Route/collision/connector/ownership/manifest hard gates, re-verified
    independently of whatever the generator itself already enforced."""

    findings: list[Finding] = []
    zone_ids = {item["terrain_id"].removeprefix("ZONE-") for item in map_plan.get("terrain", [])}
    must_reach = set(map_plan.get("validation", {}).get("must_reach", []))
    missing = sorted(must_reach - zone_ids)
    if missing:
        findings.append(Finding("required_zones_missing", "error", "Required must-reach zones are absent from terrain.", {"missing": missing}))

    entry_zone = map_plan.get("validation", {}).get("entry_zone")
    adjacency: dict[str, set[str]] = {zid: set() for zid in zone_ids}
    for edge in map_plan.get("traversable_areas", []):
        a, b = edge.get("from_zone"), edge.get("to_zone")
        if a not in zone_ids or b not in zone_ids:
            findings.append(Finding("connector_alignment_failed", "error", "A traversable area references a zone missing from terrain.", {"edge": edge}))
            continue
        adjacency[a].add(b)
        adjacency[b].add(a)

    if entry_zone in zone_ids:
        reached = {entry_zone}
        queue = deque([entry_zone])
        while queue:
            current = queue.popleft()
            for neighbor in adjacency[current] - reached:
                reached.add(neighbor)
                queue.append(neighbor)
        unreachable = sorted(zone_ids - reached)
        if unreachable:
            findings.append(Finding("zones_unreachable_from_entry", "error", "Some zones cannot be reached from the entry zone.", {"unreachable": unreachable}))
    else:
        findings.append(Finding("entry_zone_missing", "error", "The declared entry zone is not present among terrain zones.", {"entry_zone": entry_zone}))

    for obstacle in map_plan.get("obstacles", []):
        parent = obstacle.get("parent_zone")
        if parent not in zone_ids:
            findings.append(Finding("obstacle_parent_zone_missing", "error", "An obstacle references a parent zone missing from terrain.", {"obstacle_id": obstacle.get("obstacle_id"), "parent_zone": parent}))

    atlas_screen_id = map_plan.get("atlas_screen_id")
    if target_map_id is not None:
        ledger = load_ledger(Path(project_root)) if project_root is not None else None
        if not map_write_allowed(ledger, target_map_id):
            findings.append(Finding("ownership_not_writable", "error", "The target production map is not writable per the ownership ledger.", {"target_map_id": target_map_id}))
    elif atlas_screen_id is not None:
        findings.append(Finding("ownership_unverified_production_target", "error", "Candidate declares a production atlas_screen_id with no ownership-ledger check supplied.", {"atlas_screen_id": atlas_screen_id}))

    if generation_manifest is None:
        findings.append(Finding("manifest_missing", "error", "No GenerationManifest was supplied for this candidate.", {}))
    else:
        missing_manifest = sorted(REQUIRED_MANIFEST_FIELDS - set(generation_manifest))
        if missing_manifest:
            findings.append(Finding("manifest_incomplete", "error", "GenerationManifest is missing required fields.", {"missing": missing_manifest}))
        if generation_manifest.get("status") not in {"generated_pending_review", "accepted", "accepted_with_notes", "rejected"}:
            findings.append(Finding("manifest_status_invalid", "error", "GenerationManifest status is not a recognized value.", {"status": generation_manifest.get("status")}))
        if generation_manifest.get("status", "").startswith("accepted"):
            findings.append(Finding("manifest_self_certified", "error", "GenerationManifest already claims an accepted status before any human decision was recorded.", {"status": generation_manifest.get("status")}))

    passed = not any(f.severity == "error" for f in findings)
    return AuditResult(target=map_plan.get("blueprint_id", "unknown"), passed=passed, findings=findings)


def audit_visual_proxy(
    map_plan: dict[str, Any],
    generation_manifest: dict[str, Any] | None = None,
) -> AuditResult:
    """MapVision-derived checks computable from a MapPlan's own
    `tile_assembly_*` provenance fields, without a rendered image."""

    findings: list[Finding] = []

    unverified: list[dict[str, Any]] = []
    for obstacle in map_plan.get("obstacles", []):
        tag = obstacle.get("name")
        ref = obstacle.get("tile_assembly_ref")
        state = obstacle.get("tile_assembly_review_state")
        if ref is None:
            unverified.append({"tag": tag, "obstacle_id": obstacle.get("obstacle_id"), "reason": "no tile_assembly_ref bound"})
        elif state in BLOCKED_REVIEW_STATES:
            unverified.append({"tag": tag, "tile_assembly_ref": ref, "reason": f"review_state {state!r} is not downstream-generation-approved"})
    for slot in map_plan.get("landmark_slots", []):
        tag = slot.get("landmark_tag")
        ref = slot.get("tile_assembly_ref")
        state = slot.get("tile_assembly_review_state")
        if ref is None:
            unverified.append({"tag": tag, "reason": "no tile_assembly_ref bound"})
        elif state in BLOCKED_REVIEW_STATES:
            unverified.append({"tag": tag, "tile_assembly_ref": ref, "reason": f"review_state {state!r} is not downstream-generation-approved"})
    if unverified:
        findings.append(Finding(
            "ASH-ASSEMBLY-001_002_incomplete_or_unverified_assembly",
            "error",
            "One or more placed objects are not backed by a catalog-enabled, non-blocked TileAssembly -- the isolated/partial-object failure mode MapVision explicitly forbids (e.g. a half-tree).",
            {"objects": unverified},
        ))

    buildings: dict[str, dict[str, Any]] = {
        obstacle["name"]: obstacle
        for obstacle in map_plan.get("obstacles", [])
        if obstacle.get("name") in CANONICAL_BUILDING_TAGS
    }
    def _building_height(obstacle: dict[str, Any]) -> int | None:
        # Prefer the door-anchor-derived building height (excludes the
        # ground/approach row the full extraction rectangle typically
        # includes below the door); fall back to the raw extraction height
        # only if no entry anchor was available to derive it from.
        rows = obstacle.get("tile_assembly_building_height_rows")
        return rows if rows is not None else obstacle.get("tile_assembly_height")

    tall_buildings = [
        {"tag": tag, "height": _building_height(obstacle), "limit": MAX_APPROVED_BUILDING_HEIGHT_ROWS}
        for tag, obstacle in buildings.items()
        if _building_height(obstacle) is not None
        and _building_height(obstacle) > MAX_APPROVED_BUILDING_HEIGHT_ROWS
    ]
    if tall_buildings:
        findings.append(Finding(
            "ASH-BUILD-001_excessive_building_height",
            "error",
            "A canonical building's bound assembly exceeds the approved height cap.",
            {"buildings": tall_buildings},
        ))

    if len(buildings) >= 2:
        silhouettes = {tag: (b.get("tile_assembly_width"), _building_height(b)) for tag, b in buildings.items()}
        seen: dict[tuple, str] = {}
        duplicates = []
        for tag, dims in silhouettes.items():
            if dims in seen:
                duplicates.append([seen[dims], tag])
            else:
                seen[dims] = tag
        if duplicates:
            findings.append(Finding(
                "ASH-BUILD-003_repeated_building_silhouette",
                "error",
                "Two or more canonical buildings share an identical bound-assembly footprint -- one repeated shell rather than distinct silhouettes.",
                {"silhouettes": {k: list(v) for k, v in silhouettes.items()}, "duplicate_pairs": duplicates},
            ))

    dominant = [slot for slot in map_plan.get("landmark_slots", []) if slot.get("dominant")]
    if not dominant:
        findings.append(Finding("ASH-LANDMARK-001_no_dominant_landmark", "error", "No landmark slot is marked dominant.", {}))
    else:
        bad = [
            {"landmark_tag": slot.get("landmark_tag"), "tile_assembly_ref": slot.get("tile_assembly_ref"), "review_state": slot.get("tile_assembly_review_state")}
            for slot in dominant
            if slot.get("tile_assembly_ref") is None or slot.get("tile_assembly_review_state") in BLOCKED_REVIEW_STATES
        ]
        if bad:
            findings.append(Finding("ASH-LANDMARK-001_dominant_landmark_unverified", "error", "The dominant landmark is not backed by a catalog-enabled TileAssembly.", {"landmarks": bad}))

    passed = not any(f.severity == "error" for f in findings)
    return AuditResult(target=map_plan.get("blueprint_id", "unknown"), passed=passed, findings=findings)


def audit_visual_render(critique: VisualCritique) -> AuditResult:
    """WO-0075: adapt a render-based :class:`VisualCritique` into the gate's
    ``AuditResult`` vocabulary, automating the AVCP constraints previously
    parked in :data:`NOT_YET_AUTOMATABLE`.

    A core-criterion ``fail`` is an error (blocks); a non-core ``fail`` or any
    ``partial`` is a warning (surfaces but does not block). ``passed`` follows
    the same "no error findings" rule as the other audits, so it agrees with
    ``critique.overall == "reject"`` by construction. This audit can only ever
    reject or flag -- it never contributes acceptance."""

    findings: list[Finding] = []
    for result in critique.results:
        crit = result.criterion
        avcp = list(crit.avcp_refs) if crit else []
        if result.verdict == "fail":
            findings.append(Finding(
                f"{result.criterion_id}_fail",
                "error" if result.core else "warning",
                result.reason,
                {"criterion": result.criterion_id, "verdict": "fail", "core": result.core, "avcp_refs": avcp},
            ))
        elif result.verdict == "partial":
            findings.append(Finding(
                f"{result.criterion_id}_partial",
                "warning",
                result.reason,
                {"criterion": result.criterion_id, "verdict": "partial", "avcp_refs": avcp},
            ))
    passed = not any(f.severity == "error" for f in findings)
    return AuditResult(target=critique.image_ref, passed=passed, findings=findings)


@dataclass(frozen=True)
class DualGateResult:
    candidate_ref: str
    structural: AuditResult
    visual_proxy: AuditResult
    not_yet_automatable: tuple[str, ...] = NOT_YET_AUTOMATABLE
    # WO-0075: optional render-based critic pass. When absent the gate behaves
    # exactly as WO-0072 did (structural + provenance-derived visual proxy);
    # when present, a render reject blocks, but it can never turn a rejection
    # into a recommendation -- the critic flags/rejects, never accepts.
    visual_render: AuditResult | None = None

    @property
    def recommendation(self) -> str:
        # No audit can offset another: all present audits must pass independently.
        render_ok = self.visual_render is None or self.visual_render.passed
        if self.structural.passed and self.visual_proxy.passed and render_ok:
            return "candidate_for_human_review"
        return "rejected"

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "candidate_ref": self.candidate_ref,
            "structural": self.structural.to_dict(),
            "visual_proxy": self.visual_proxy.to_dict(),
            "not_yet_automatable": list(self.not_yet_automatable),
            "recommendation": self.recommendation,
        }
        # Added only when a render critique was supplied, so evidence for
        # callers that pass none stays byte-identical to WO-0072.
        if self.visual_render is not None:
            payload["visual_render"] = self.visual_render.to_dict()
        return payload


def run_dual_gate(
    map_plan: dict[str, Any],
    generation_manifest: dict[str, Any] | None = None,
    *,
    project_root: Path | None = None,
    target_map_id: int | None = None,
    visual_critique: VisualCritique | None = None,
) -> DualGateResult:
    structural = audit_structural(map_plan, generation_manifest, project_root=project_root, target_map_id=target_map_id)
    visual_proxy = audit_visual_proxy(map_plan, generation_manifest)
    # WO-0075: fold in the render-based critic only when a critique is supplied
    # (a trusted, calibrated backend produced it). Callers that pass none get
    # WO-0072's exact behaviour.
    visual_render = audit_visual_render(visual_critique) if visual_critique is not None else None
    return DualGateResult(
        candidate_ref=map_plan.get("blueprint_id", "unknown"),
        structural=structural,
        visual_proxy=visual_proxy,
        visual_render=visual_render,
    )


class HumanDecisionError(ValueError):
    pass


def record_gate_evidence(
    result: DualGateResult,
    *,
    concept_refs: list[str],
    render_refs: list[str],
    output_path: Path,
) -> dict[str, Any]:
    """Persist side-by-side concept/candidate evidence with a pending human
    decision -- the human_decision block is the only part `apply_human_decision`
    may later touch."""

    evidence = {
        "schema_version": "0.1",
        **result.to_dict(),
        "concept_refs": list(concept_refs),
        "render_refs": list(render_refs),
        "human_decision": {"status": "pending", "decision": None, "decided_by": None, "decided_at": None, "notes": None},
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return evidence


def apply_human_decision(
    evidence_path: Path,
    *,
    decision: str,
    decided_by: str,
    decided_at: str,
    notes: str | None = None,
) -> dict[str, Any]:
    """Record Chris's final visual decision onto a persisted evidence file.

    Fails closed (no write) unless `decided_by == "Chris"` -- WO-0072's own
    "no self-certification" constraint applies to this function, not just to
    the automated audits above.
    """

    if decided_by != "Chris":
        raise HumanDecisionError("Only Chris may record final visual acceptance (WO-0072: no self-certification).")
    if decision not in {"accepted", "accepted_with_notes", "rejected"}:
        raise HumanDecisionError(f"unrecognized decision: {decision!r}")
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    if decision.startswith("accepted") and evidence["recommendation"] != "candidate_for_human_review":
        raise HumanDecisionError("Cannot accept a candidate the dual gate did not recommend for human review.")
    evidence["human_decision"] = {
        "status": "recorded",
        "decision": decision,
        "decided_by": decided_by,
        "decided_at": decided_at,
        "notes": notes,
    }
    evidence_path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return evidence
