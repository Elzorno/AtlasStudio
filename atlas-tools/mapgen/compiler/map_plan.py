"""Versioned, schema-validated MapPlan wrapper with canonical JSON output."""

from __future__ import annotations

import copy
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from contract.validate_contract import validate


COMPILER_DIR = Path(__file__).resolve().parent
SCHEMA_PATH = COMPILER_DIR / "contract" / "schemas" / "map_plan.schema.json"
SUPPORTED_SCHEMA_VERSIONS = {"0.1"}


class MapPlanValidationError(ValueError):
    pass


def canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def _load_schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


@dataclass(frozen=True)
class MapPlan:
    payload: dict[str, Any]

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "MapPlan":
        candidate = copy.deepcopy(payload)
        version = str(candidate.get("schema_version", ""))
        if version not in SUPPORTED_SCHEMA_VERSIONS:
            raise MapPlanValidationError(f"unsupported MapPlan schema_version: {version!r}")
        errors = validate(candidate, _load_schema())
        if errors:
            raise MapPlanValidationError("invalid MapPlan: " + "; ".join(errors))
        return cls(candidate)

    @classmethod
    def load(cls, path: Path) -> "MapPlan":
        return cls.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def to_dict(self) -> dict[str, Any]:
        return copy.deepcopy(self.payload)

    def to_json(self) -> str:
        return canonical_json(self.payload)

    def write(self, path: Path) -> None:
        path.write_text(self.to_json(), encoding="utf-8")

    @property
    def blueprint_id(self) -> str:
        return str(self.payload["blueprint_id"])

    @property
    def generation_manifest_ref(self) -> str | None:
        return self.payload.get("generation_manifest_ref")

    def with_manifest_ref(self, manifest_id: str | None) -> "MapPlan":
        payload = self.to_dict()
        payload["generation_manifest_ref"] = manifest_id
        return MapPlan.from_dict(payload)
