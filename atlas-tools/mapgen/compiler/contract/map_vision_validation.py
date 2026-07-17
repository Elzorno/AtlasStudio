"""Cross-field semantic validation for the MapVision 0.1 contract."""

from __future__ import annotations

from typing import Any

FORBIDDEN_ENGINE_KEYS = {
    "tile_id", "tileId", "tileset_id", "tilesetId", "asset_filename",
    "database_id", "rpgmaker_tile_id",
}


def _records(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _records(child)
    elif isinstance(value, list):
        for child in value:
            yield from _records(child)


def validate_map_vision_semantics(instance: dict[str, Any]) -> list[str]:
    """Return deterministic cross-field errors not expressible by the schema subset."""
    errors: list[str] = []
    provenance = {
        entry.get("source_ref"): entry
        for entry in instance.get("source_provenance", [])
        if isinstance(entry, dict) and entry.get("source_ref")
    }

    for record in _records(instance):
        forbidden = sorted(FORBIDDEN_ENGINE_KEYS.intersection(record))
        if forbidden:
            errors.append(f"raw engine binding keys are forbidden in MapVision: {', '.join(forbidden)}")

        source_refs = record.get("source_refs")
        if isinstance(source_refs, list):
            missing = sorted(ref for ref in source_refs if ref not in provenance)
            if missing:
                errors.append(f"statement cites source absent from source_provenance: {', '.join(missing)}")
            if record.get("authority") == "required_canon":
                source_types = {
                    provenance[ref].get("source_type")
                    for ref in source_refs
                    if ref in provenance
                }
                if "atlas_canon" not in source_types:
                    errors.append("required_canon statement has no atlas_canon source")

    for entry in provenance.values():
        if entry.get("source_type") == "concept_art" and entry.get("authority") == "required_canon":
            errors.append("concept_art provenance cannot have required_canon authority")

    approval = instance.get("approval", {})
    conflicts = approval.get("unresolved_conflicts", [])
    status = instance.get("status")
    if conflicts and status != "pending_human_approval":
        errors.append("unresolved conflicts require pending_human_approval status")
    if conflicts and approval.get("canon_reconciled") is not False:
        errors.append("unresolved conflicts require canon_reconciled=false")
    if status == "approved":
        if approval.get("canon_reconciled") is not True:
            errors.append("approved MapVision requires canon_reconciled=true")
        if conflicts:
            errors.append("approved MapVision cannot have unresolved conflicts")
        if not approval.get("approved_by") or not approval.get("approved_at"):
            errors.append("approved MapVision requires approved_by and approved_at")

    return sorted(set(errors))

