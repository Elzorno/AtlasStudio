"""GenerationManifest construction, validation, and canonical serialization."""

from __future__ import annotations

import copy
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from contract.validate_contract import validate
from map_plan import canonical_json
from seed_streams import ALGORITHM, SeedStreams, derive_root_seed


COMPILER_DIR = Path(__file__).resolve().parent
SCHEMA_PATH = COMPILER_DIR / "contract" / "schemas" / "generation_manifest.schema.json"
SUPPORTED_SCHEMA_VERSIONS = {"0.1"}
SUPPORTED_CONTRACT_VERSIONS = {"0.1"}


class ManifestValidationError(ValueError):
    pass


def seed_inputs(
    map_intent_id: str,
    archetype_id: str,
    archetype_version: str,
    layout_family_id: str,
    layout_family_version: str,
    variant_id: str,
    style_pack_id: str,
    style_pack_version: str,
    salt: str,
) -> list[str]:
    return [
        map_intent_id,
        f"{archetype_id}@{archetype_version}",
        f"{layout_family_id}@{layout_family_version}",
        variant_id,
        f"{style_pack_id}@{style_pack_version}",
        salt,
    ]


def _schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


@dataclass(frozen=True)
class GenerationManifest:
    payload: dict[str, Any]

    @classmethod
    def create(
        cls,
        *,
        manifest_id: str,
        map_intent_id: str,
        generator_id: str,
        generator_version: str,
        archetype_id: str,
        archetype_version: str,
        layout_family_id: str,
        layout_family_version: str,
        variant_id: str,
        style_pack_id: str,
        style_pack_version: str,
        salt: str,
        generated_at: str,
        adapter_id: str | None = None,
        adapter_version: str | None = None,
        tile_palette_id: str | None = None,
        tile_palette_version: str | None = None,
        output_map_plan_ref: str | None = None,
        status: str = "generated_pending_review",
    ) -> "GenerationManifest":
        inputs = seed_inputs(
            map_intent_id,
            archetype_id,
            archetype_version,
            layout_family_id,
            layout_family_version,
            variant_id,
            style_pack_id,
            style_pack_version,
            salt,
        )
        if (adapter_id is None) != (adapter_version is None):
            raise ManifestValidationError("adapter_id and adapter_version must be supplied together")
        if (tile_palette_id is None) != (tile_palette_version is None):
            raise ManifestValidationError("tile_palette_id and tile_palette_version must be supplied together")
        payload = {
            "schema_version": "0.1",
            "manifest_id": manifest_id,
            "map_intent_ref": map_intent_id,
            "generator_ref": {"generator_id": generator_id, "version": generator_version},
            "adapter_ref": None if adapter_id is None else {"adapter_id": adapter_id, "version": adapter_version},
            "archetype_ref": {"archetype_id": archetype_id, "version": archetype_version},
            "layout_family_ref": {
                "layout_family_id": layout_family_id,
                "version": layout_family_version,
                "variant_id": variant_id,
            },
            "style_pack_ref": {"style_pack_id": style_pack_id, "version": style_pack_version},
            "tile_palette_ref": None if tile_palette_id is None else {
                "tile_palette_id": tile_palette_id,
                "version": tile_palette_version,
            },
            "seed": {"algorithm": ALGORITHM, "inputs": inputs, "salt": salt, "value": derive_root_seed(inputs)},
            "contract_version": "0.1",
            "generated_at": generated_at,
            "output_map_plan_ref": output_map_plan_ref,
            "status": status,
        }
        return cls.from_dict(payload)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "GenerationManifest":
        candidate = copy.deepcopy(payload)
        schema_version = str(candidate.get("schema_version", ""))
        contract_version = str(candidate.get("contract_version", ""))
        if schema_version not in SUPPORTED_SCHEMA_VERSIONS:
            raise ManifestValidationError(f"unsupported manifest schema_version: {schema_version!r}")
        if contract_version not in SUPPORTED_CONTRACT_VERSIONS:
            raise ManifestValidationError(f"unsupported contract_version: {contract_version!r}")
        errors = validate(candidate, _schema())
        if errors:
            raise ManifestValidationError("invalid GenerationManifest: " + "; ".join(errors))
        seed = candidate["seed"]
        expected = derive_root_seed(seed["inputs"])
        if seed["value"] != expected:
            raise ManifestValidationError(f"seed value mismatch: recorded {seed['value']}, expected {expected}")
        if seed["salt"] != seed["inputs"][-1]:
            raise ManifestValidationError("seed salt must equal the final ordered seed input")
        return cls(candidate)

    @classmethod
    def load(cls, path: Path) -> "GenerationManifest":
        return cls.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def to_dict(self) -> dict[str, Any]:
        return copy.deepcopy(self.payload)

    def to_json(self) -> str:
        return canonical_json(self.payload)

    def write(self, path: Path) -> None:
        path.write_text(self.to_json(), encoding="utf-8")

    @property
    def root_seed(self) -> int:
        return int(self.payload["seed"]["value"])

    @property
    def streams(self) -> SeedStreams:
        return SeedStreams(self.root_seed)
