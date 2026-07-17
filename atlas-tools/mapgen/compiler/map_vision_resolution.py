"""WO-0071: resolve an approved MapVision + visual constraint profile into
version-pinned TileAssembly candidates the SemanticAssembler can bind to
module semantic tags, failing closed on every unresolved-canon, incomplete-
constraint, or missing-assembly condition the work order enumerates.

This module owns the compiler-integration mapping from a MapVision building
role / landmark id to the plausible TileAssembly/asset ids that could satisfy
it. That mapping is not part of the TileAssembly contract itself (kits do not
declare a "target role"); it is deliberately kept here, in one place, so it
can be audited and revised whenever a kit's enabled set changes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from tile_assembly_catalog import AssemblyRecord, enabled_candidates


class MapVisionResolutionError(ValueError):
    def __init__(self, code: str, message: str, context: dict | None = None):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.context = context or {}


# semantic_tag (module.semantic_tag / landmark_tag) -> plausible TileAssembly
# or custom-extension asset ids, in preference order. Listing a currently
# blocked/study-only id here is deliberate: it documents that a role has a
# real-world candidate on file, while `enabled_candidates` still fails closed
# on it until a kit review actually enables it.
SEMANTIC_TAG_CANDIDATES: dict[str, list[str]] = {
    "elara_house": ["TASM-ASHFORD-ELARA-HOUSE-AUTHORED"],
    "ashford_shop": ["TASM-ASHFORD-SHOP-AUTHORED"],
    "ashford_inn": ["TASM-ASHFORD-INN-AUTHORED"],
    "ashford_elder_house": ["TASM-ASHFORD-ELDER-HOUSE-AUTHORED"],
    "village_cottage": ["TASM-ASHFORD-COTTAGE-LOW-A", "TASM-ASHFORD-COTTAGE-LOW-B"],
    "central_well": ["ASH-CUSTOM-WELL-ROOFED-01", "TASM-ASHFORD-WELL-ROOFED-AUTHORED"],
    "warm_vent": ["TASM-ASHFORD-WARM-VENT-AUTHORED"],
    "humming_panel": ["ASH-CUSTOM-PANEL-01", "TASM-ASHFORD-HUMMING-PANEL-AUTHORED"],
    "patched_metal_fence": ["ASH-CUSTOM-FENCE-01", "TASM-ASHFORD-PATCHED-METAL-FENCE-AUTHORED"],
    "maintenance_drainage": ["ASH-CUSTOM-DRAINAGE-01", "TASM-ASHFORD-BRIDGE-AUTHORED"],
    "broadleaf_tree": ["TASM-ASHFORD-TREE-BROADLEAF-01"],
}

REQUIRED_BUILDING_ROLE_TAGS: dict[str, str] = {
    "Elara House": "elara_house",
    "Ashford Shop": "ashford_shop",
    "Ashford Inn": "ashford_inn",
    "Ashford Elder House": "ashford_elder_house",
}


@dataclass(frozen=True)
class ResolvedMapVision:
    map_vision_id: str
    version: str
    role_candidates: dict[str, list[AssemblyRecord]]


def _require_approved_map_vision(map_vision: Mapping[str, object]) -> None:
    if map_vision.get("status") != "approved":
        raise MapVisionResolutionError(
            "unresolved_canon",
            "MapVision is not approved",
            {"map_vision_id": map_vision.get("map_vision_id"), "status": map_vision.get("status")},
        )
    approval = map_vision.get("approval") or {}
    if not approval.get("canon_reconciled"):
        raise MapVisionResolutionError(
            "unresolved_canon", "MapVision canon is not reconciled", {"approval": approval}
        )
    if approval.get("unresolved_conflicts"):
        raise MapVisionResolutionError(
            "unresolved_canon",
            "MapVision has unresolved conflicts",
            {"unresolved_conflicts": approval["unresolved_conflicts"]},
        )
    if not approval.get("approved_by") or not approval.get("approved_at"):
        raise MapVisionResolutionError(
            "unresolved_canon", "MapVision is missing approved_by/approved_at", {"approval": approval}
        )


def _require_complete_constraint_profile(
    constraint_profile: Mapping[str, object], map_vision: Mapping[str, object]
) -> None:
    expected_ref = f"{map_vision['map_vision_id']}@{map_vision['version']}"
    target = str(constraint_profile.get("target_map_vision", ""))
    if not target.startswith(expected_ref):
        raise MapVisionResolutionError(
            "incomplete_visual_constraints",
            "constraint profile does not target the supplied MapVision version",
            {"expected": expected_ref, "found": target},
        )
    if constraint_profile.get("status") != "approved":
        raise MapVisionResolutionError(
            "incomplete_visual_constraints",
            "constraint profile is not approved",
            {"status": constraint_profile.get("status")},
        )
    approval = constraint_profile.get("approval") or {}
    if not approval.get("approved_by") or not approval.get("approved_at"):
        raise MapVisionResolutionError(
            "incomplete_visual_constraints",
            "constraint profile is missing approved_by/approved_at",
            {"approval": approval},
        )
    if not constraint_profile.get("constraints"):
        raise MapVisionResolutionError(
            "incomplete_visual_constraints", "constraint profile declares no constraints", {}
        )


def resolve_map_vision(
    map_vision: Mapping[str, object],
    constraint_profile: Mapping[str, object],
    catalog: Mapping[str, AssemblyRecord],
    *,
    required_semantic_tags: list[str] = (),
) -> ResolvedMapVision:
    """Validate approval and resolve every requested semantic tag to its
    catalog-enabled TileAssembly candidates. Does not require every tag in
    ``SEMANTIC_TAG_CANDIDATES`` to resolve -- only the ones a caller actually
    intends to place (``required_semantic_tags``) must end up non-empty;
    every other tag is still resolved (possibly to an empty list) so a
    caller can inspect what is and is not currently available.
    """

    _require_approved_map_vision(map_vision)
    _require_complete_constraint_profile(constraint_profile, map_vision)

    building_roles = {entry["building_role"] for entry in map_vision.get("building_silhouettes", [])}
    for role, tag in REQUIRED_BUILDING_ROLE_TAGS.items():
        if role in building_roles and tag not in SEMANTIC_TAG_CANDIDATES:
            raise MapVisionResolutionError(
                "incomplete_visual_constraints",
                "MapVision building role has no registered semantic-tag binding",
                {"building_role": role},
            )

    role_candidates: dict[str, list[AssemblyRecord]] = {
        tag: enabled_candidates(catalog, ids) for tag, ids in SEMANTIC_TAG_CANDIDATES.items()
    }

    for tag in required_semantic_tags:
        if not role_candidates.get(tag):
            raise MapVisionResolutionError(
                "missing_assembly",
                "no catalog-enabled TileAssembly satisfies this required semantic tag",
                {
                    "semantic_tag": tag,
                    "considered_ids": SEMANTIC_TAG_CANDIDATES.get(tag, []),
                },
            )

    return ResolvedMapVision(
        map_vision_id=str(map_vision["map_vision_id"]),
        version=str(map_vision["version"]),
        role_candidates=role_candidates,
    )
