#!/usr/bin/env python3
"""Stdlib-only JSON Schema validator for the WO-0056 reusable map compiler contract.

No `jsonschema` package is used, matching this project's established stdlib-only
convention for the compiler (see atlas-tools/mapgen/compiler/spec_parser.py in the
Atlas repo and specs/world_spec.schema.json's own "stdlib only" note in AtlasStudio).
This validator supports the subset of JSON Schema (2020-12 vocabulary) actually
used by contract/schemas/*.json: type, properties, required, additionalProperties,
items, enum, pattern, minimum, maximum, minItems, minLength.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    from .map_vision_validation import validate_map_vision_semantics
    from .tile_assembly_validation import validate_tile_assembly_semantics
except ImportError:  # Direct `python3 validate_contract.py` execution.
    from map_vision_validation import validate_map_vision_semantics
    from tile_assembly_validation import validate_tile_assembly_semantics

TYPE_MAP = {
    "object": dict,
    "array": list,
    "string": str,
    "boolean": bool,
    "null": type(None),
}


def _check_type(value: Any, type_name: str) -> bool:
    if type_name == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if type_name == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    expected = TYPE_MAP.get(type_name)
    if expected is None:
        return True
    if type_name == "boolean":
        return isinstance(value, bool)
    return isinstance(value, expected)


def validate(instance: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    errors: list[str] = []

    types = schema.get("type")
    if types is not None:
        type_list = types if isinstance(types, list) else [types]
        if not any(_check_type(instance, t) for t in type_list):
            errors.append(f"{path}: expected type {type_list}, got {type(instance).__name__}")
            return errors  # further checks are not meaningful on a type mismatch

    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: value {instance!r} not in enum {schema['enum']}")

    if isinstance(instance, str):
        if "pattern" in schema and not re.match(schema["pattern"], instance):
            errors.append(f"{path}: {instance!r} does not match pattern {schema['pattern']!r}")
        if "minLength" in schema and len(instance) < schema["minLength"]:
            errors.append(f"{path}: string shorter than minLength {schema['minLength']}")

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            errors.append(f"{path}: {instance} < minimum {schema['minimum']}")
        if "maximum" in schema and instance > schema["maximum"]:
            errors.append(f"{path}: {instance} > maximum {schema['maximum']}")

    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errors.append(f"{path}: array shorter than minItems {schema['minItems']}")
        item_schema = schema.get("items")
        if item_schema is not None:
            for i, item in enumerate(instance):
                errors.extend(validate(item, item_schema, f"{path}[{i}]"))

    if isinstance(instance, dict):
        for key in schema.get("required", []):
            if key not in instance:
                errors.append(f"{path}: missing required property '{key}'")
        properties = schema.get("properties", {})
        for key, value in instance.items():
            if key in properties:
                errors.extend(validate(value, properties[key], f"{path}.{key}"))
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}: unexpected property '{key}' (additionalProperties: false)")

    return errors


def validate_file(instance_path: Path, schema_path: Path) -> list[str]:
    instance = json.loads(instance_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    return validate(instance, schema)


# instance file -> schema file it must validate against
EXAMPLE_MANIFEST: dict[str, str] = {
    "examples/tile_assembly/valid_tile_assembly.json": "schemas/tile_assembly.schema.json",
    "examples/tile_assembly/valid_atomic_prop.json": "schemas/tile_assembly.schema.json",
    "examples/map_vision/valid_map_vision.json": "schemas/map_vision.schema.json",
    "examples/shop/map_intent.json": "schemas/map_intent.schema.json",
    "examples/shop/gameplay_graph.json": "schemas/gameplay_graph.schema.json",
    "examples/shop/building_archetype.json": "schemas/building_archetype.schema.json",
    "examples/shop/layout_family.json": "schemas/layout_family.schema.json",
    "examples/shop/generation_manifest.json": "schemas/generation_manifest.schema.json",
    "examples/inn/map_intent.json": "schemas/map_intent.schema.json",
    "examples/inn/gameplay_graph.json": "schemas/gameplay_graph.schema.json",
    "examples/inn/building_archetype.json": "schemas/building_archetype.schema.json",
    "examples/inn/layout_family.json": "schemas/layout_family.schema.json",
    "examples/inn/generation_manifest.json": "schemas/generation_manifest.schema.json",
    "examples/shared/module_counter_service_point.json": "schemas/module.schema.json",
    "examples/shared/module_bed_desk_nook.json": "schemas/module.schema.json",
    "examples/shared/module_shelf_wall_run.json": "schemas/module.schema.json",
    "examples/shared/module_display_table.json": "schemas/module.schema.json",
    "examples/shared/module_back_wall_shelf_run.json": "schemas/module.schema.json",
    "examples/shared/module_hearth_accent.json": "schemas/module.schema.json",
    "examples/shared/connector_open_floor.json": "schemas/connector.schema.json",
    "examples/shared/connector_chokepoint_corridor.json": "schemas/connector.schema.json",
    "examples/shared/style_pack_ashford_cozy_interior.json": "schemas/style_pack.schema.json",
    "examples/shared/tile_palette_ashford_cozy_interior_illustrative.json": "schemas/tile_palette.schema.json",
    "examples/shop/layout_family_offset.json": "schemas/layout_family.schema.json",
    "examples/inn/layout_family_compact.json": "schemas/layout_family.schema.json",
    "examples/inn/layout_family_zoned_expanded.json": "schemas/layout_family.schema.json",
    "examples/house/map_intent.json": "schemas/map_intent.schema.json",
    "examples/house/gameplay_graph.json": "schemas/gameplay_graph.schema.json",
    "examples/house/building_archetype.json": "schemas/building_archetype.schema.json",
    "examples/house/layout_family_compact.json": "schemas/layout_family.schema.json",
    "examples/house/layout_family_offset.json": "schemas/layout_family.schema.json",
    "examples/house/generation_manifest.json": "schemas/generation_manifest.schema.json",
    "examples/shared/style_pack_coastal_settlement_interior.json": "schemas/style_pack.schema.json",
    "examples/ashford/map_intent.json": "schemas/map_intent.schema.json",
    "examples/ashford/gameplay_graph.json": "schemas/gameplay_graph.schema.json",
    "examples/ashford/building_archetype.json": "schemas/building_archetype.schema.json",
    "examples/ashford/layout_family.json": "schemas/layout_family.schema.json",
    "examples/shared/module_elara_house.json": "schemas/module.schema.json",
    "examples/shared/module_ashford_shop.json": "schemas/module.schema.json",
    "examples/shared/module_ashford_inn.json": "schemas/module.schema.json",
    "examples/shared/module_ashford_elder_house.json": "schemas/module.schema.json",
    "examples/shared/module_patched_fence.json": "schemas/module.schema.json",
    "examples/shared/module_broadleaf_tree.json": "schemas/module.schema.json",
    "examples/ashford_production/map_intent.json": "schemas/map_intent.schema.json",
    "examples/ashford_production/gameplay_graph.json": "schemas/gameplay_graph.schema.json",
    "examples/ashford_production/building_archetype.json": "schemas/building_archetype.schema.json",
    "examples/ashford_production/layout_family.json": "schemas/layout_family.schema.json",
}


def main() -> int:
    root = Path(__file__).parent
    failures = 0
    for instance_rel, schema_rel in EXAMPLE_MANIFEST.items():
        instance_path = root / instance_rel
        schema_path = root / schema_rel
        errors = validate_file(instance_path, schema_path)
        if schema_rel == "schemas/map_vision.schema.json" and not errors:
            instance = json.loads(instance_path.read_text(encoding="utf-8"))
            errors.extend(validate_map_vision_semantics(instance))
        if schema_rel == "schemas/tile_assembly.schema.json" and not errors:
            instance = json.loads(instance_path.read_text(encoding="utf-8"))
            errors.extend(validate_tile_assembly_semantics(instance))
        if errors:
            failures += 1
            print(f"FAIL {instance_rel} against {schema_rel}:")
            for err in errors:
                print(f"  - {err}")
        else:
            print(f"PASS {instance_rel} against {schema_rel}")
    print(f"\n{len(EXAMPLE_MANIFEST) - failures}/{len(EXAMPLE_MANIFEST)} examples valid")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
