"""WO-0071: merged, enablement-aware TileAssembly catalog for compiler integration.

A "kit" here is any of the Ashford TileAssembly artifacts produced under WO-0070:
the raw reference-extraction kit, the adapter-authored revision kit, and the
human-approved custom tileset extension. Each kit records its own per-record
review state; this module normalizes all three into one lookup keyed by
assembly id and applies a single, explicit enablement rule so the compiler
never has to special-case a kit's on-disk shape.

Enablement rule: a record is usable if and only if its own
``downstream_generation_allowed`` flag (falling back to ``enabled`` when that
key is absent) is true. A kit-level ``enabled``/``approval_state`` flag (the
authored kit currently ships ``"enabled": false`` at the kit level even though
five of its nine records are individually ``human_approved`` /
``downstream_generation_allowed: true``) is treated as advisory provenance,
not a gate -- the per-record field is the one WO-0070's own hardening pass
introduced specifically so downstream selection could fail closed record by
record. See REFERENCE-FIDELITY-REVIEW.md / AUTHORED-PACK-FIDELITY-REVIEW.md
"Post-review hardening" / "Subsequent human decision" sections for why.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping


DEFAULT_ADAPTER_REF = "rpg_maker_mz@0.1"


@dataclass(frozen=True)
class AssemblyRecord:
    assembly_id: str
    width: int
    height: int
    enabled: bool
    review_state: str
    adapter_ref: str
    source_kit: str
    # Vertical extent from roof ridge (row 0) through the door row, per its
    # own "entry" anchor -- distinct from `height`, which is the full
    # extraction rectangle and typically includes one ground/approach row
    # below the door. None when the record has no "entry" anchor (props,
    # atomic components): ASH-BUILD-001 only applies to buildings.
    building_height_rows: int | None = None


class CatalogError(ValueError):
    pass


def _entry_door_anchor_y(kit_dir: Path, entry: Mapping[str, object]) -> int | None:
    """Read the record's own file for an "entry"-role anchor's y coordinate.

    Returns None if the file is unreadable or has no entry anchor -- callers
    must treat that as "no building-height adjustment available", not as an
    error, since props/atomic components legitimately have none.
    """

    file_name = entry.get("file")
    if not file_name:
        return None
    try:
        payload = json.loads((kit_dir / str(file_name)).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    for anchor in payload.get("anchors", []):
        if anchor.get("role") == "entry" and "y" in anchor:
            return int(anchor["y"])
    return None


def _record_from_tile_assembly_entry(
    entry: Mapping[str, object], *, source_kit: str, kit_dir: Path | None = None
) -> AssemblyRecord:
    region = entry["source_region"]  # type: ignore[index]
    downstream_allowed = entry.get("downstream_generation_allowed")
    enabled = bool(downstream_allowed if downstream_allowed is not None else entry.get("enabled", False))
    door_anchor_y = _entry_door_anchor_y(kit_dir, entry) if kit_dir is not None else None
    return AssemblyRecord(
        assembly_id=str(entry["tile_assembly_id"]),
        width=int(region["width"]),  # type: ignore[index]
        height=int(region["height"]),  # type: ignore[index]
        enabled=enabled,
        review_state=str(entry.get("review_state", "unreviewed")),
        adapter_ref=DEFAULT_ADAPTER_REF,
        source_kit=source_kit,
        building_height_rows=None if door_anchor_y is None else door_anchor_y + 1,
    )


def _record_from_custom_extension_asset(entry: Mapping[str, object], *, source_kit: str) -> AssemblyRecord:
    size = entry["tile_size"]  # type: ignore[index]
    downstream_allowed = entry.get("downstream_generation_allowed")
    enabled = bool(downstream_allowed if downstream_allowed is not None else entry.get("enabled", False))
    return AssemblyRecord(
        assembly_id=str(entry["asset_id"]),
        width=int(size["width"]),  # type: ignore[index]
        height=int(size["height"]),  # type: ignore[index]
        enabled=enabled,
        review_state=str(entry.get("review_state", "unreviewed")),
        adapter_ref=DEFAULT_ADAPTER_REF,
        source_kit=source_kit,
    )


def load_tile_assembly_kit_index(path: Path) -> dict[str, AssemblyRecord]:
    """Load a WO-0070-shaped kit ``index.json`` (``assemblies: [...]``)."""

    payload = json.loads(path.read_text(encoding="utf-8"))
    kit_id = str(payload.get("kit_id", path.parent.name))
    records = {}
    for entry in payload["assemblies"]:
        record = _record_from_tile_assembly_entry(entry, source_kit=kit_id, kit_dir=path.parent)
        records[record.assembly_id] = record
    return records


def load_custom_extension_manifest(path: Path) -> dict[str, AssemblyRecord]:
    """Load the custom tileset extension's ``manifest.json`` (``assets: [...]``)."""

    payload = json.loads(path.read_text(encoding="utf-8"))
    extension_id = str(payload.get("extension_id", path.parent.name))
    if not payload.get("enabled", False):
        return {}
    records = {}
    for entry in payload["assets"]:
        record = _record_from_custom_extension_asset(entry, source_kit=extension_id)
        records[record.assembly_id] = record
    return records


def merge_catalogs(*catalogs: Mapping[str, AssemblyRecord]) -> dict[str, AssemblyRecord]:
    merged: dict[str, AssemblyRecord] = {}
    for catalog in catalogs:
        for assembly_id, record in catalog.items():
            if assembly_id in merged and merged[assembly_id] != record:
                raise CatalogError(
                    f"assembly id {assembly_id!r} is defined differently by "
                    f"{merged[assembly_id].source_kit!r} and {record.source_kit!r}"
                )
            merged[assembly_id] = record
    return merged


def enabled_candidates(
    catalog: Mapping[str, AssemblyRecord],
    candidate_ids: list[str],
) -> list[AssemblyRecord]:
    """Filter a role's plausible candidate ids down to catalog-enabled records.

    Candidate ids that are absent from the catalog entirely are silently
    excluded rather than raising: a role's binding table may list ids from a
    kit that has not been loaded in a given context (e.g. tests that load
    only one kit), and the caller (map_vision_resolution) is responsible for
    fail-closed behaviour on an empty result.
    """

    return [catalog[cid] for cid in candidate_ids if cid in catalog and catalog[cid].enabled]
