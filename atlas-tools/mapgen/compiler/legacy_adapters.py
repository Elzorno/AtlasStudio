"""Adapters from existing Atlas artifacts into the versioned MapPlan contract."""

from __future__ import annotations

from typing import Any

from map_plan import MapPlan


def blueprint_to_map_plan(payload: dict[str, Any], manifest_id: str | None = None) -> MapPlan:
    plan = MapPlan.from_dict(payload)
    return plan.with_manifest_ref(manifest_id) if manifest_id is not None else plan


def landmass_to_map_plan(payload: dict[str, Any], manifest_id: str | None = None) -> MapPlan:
    size = payload.get("size", {})
    region_id = str(payload.get("region_id", "unknown-region"))
    map_name = str(payload.get("map_name", region_id))
    cells = list(payload.get("cells", []))
    plan_payload: dict[str, Any] = {
        "schema_version": "0.1",
        "blueprint_id": f"BP-ADAPTED-{region_id}",
        "atlas_screen_id": None,
        "title": f"{map_name} (adapted landmass plan)",
        "source_documents": list(payload.get("source_documents", [])) or ["legacy-landmass-plan"],
        "map_intent": {
            "purpose": f"Preserve the existing {map_name} landmass plan in the reusable MapPlan contract.",
            "layout_mode": "procedural",
            "generation_seed": payload.get("seed"),
            "critical_path_role": "legacy_overworld_adapter",
        },
        "dimensions": {
            "width": int(size["width"]),
            "height": int(size["height"]),
            "unit": "tile",
            "coordinate_system": "atlas_tile",
            "origin": "top_left",
        },
        "terrain": cells,
        "landmark_icons": [
            {"landmark_id": key, **value}
            for key, value in sorted(payload.get("anchor_zones", {}).items())
        ],
        "generation_manifest_ref": manifest_id,
    }
    return MapPlan.from_dict(plan_payload)


def apply_adventure_flow(plan: MapPlan, payload: dict[str, Any]) -> MapPlan:
    updated = plan.to_dict()
    existing = list(updated.get("traversable_areas", []))
    for corridor in payload.get("travel_corridors", []):
        existing.append({
            "area_id": corridor.get("route_id"),
            "purpose": corridor.get("label", "adventure flow corridor"),
            "area": {"shape": "polyline", "points": [
                [point["x"], point["y"]] for point in corridor.get("travel_corridor", [])
            ]},
            "beats": list(corridor.get("beats", [])),
            "soft_gate": corridor.get("soft_gate"),
            "source_generator": payload.get("generator", "legacy-adventure-flow"),
        })
    updated["traversable_areas"] = existing
    return MapPlan.from_dict(updated)
