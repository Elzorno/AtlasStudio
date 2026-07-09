"""World specification loading and validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from models import WorldSpec


REQUIRED_LOCATIONS = {
    "ashford",
    "rustshore",
    "fogfen",
    "glassfield",
    "skyreach",
    "hidden_cave",
    "sealed_node",
}


class SpecError(ValueError):
    """Raised when a world specification is incomplete."""


def load_world_spec(path: Path) -> WorldSpec:
    payload = json.loads(path.read_text(encoding="utf-8"))
    validate_world_spec_payload(payload)
    return WorldSpec.from_dict(payload)


def validate_world_spec_payload(payload: dict[str, Any]) -> None:
    for key in ("region_id", "map_name", "size", "shape", "canonical_locations"):
        if key not in payload:
            raise SpecError(f"missing required field: {key}")

    size = payload["size"]
    width = int(size.get("width", 0))
    height = int(size.get("height", 0))
    if width < 24 or height < 18:
        raise SpecError("world size must be at least 24x18 for terrain planning")

    locations = payload["canonical_locations"]
    missing = sorted(REQUIRED_LOCATIONS.difference(locations))
    if missing:
        raise SpecError("missing canonical locations: " + ", ".join(missing))

    for key, location in locations.items():
        if "placement" not in location:
            raise SpecError(f"location {key} missing placement")
