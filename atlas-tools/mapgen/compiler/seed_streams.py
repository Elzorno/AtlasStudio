"""Stable root and named seed derivation for the reusable map compiler."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Iterable


ALGORITHM = "sha256_truncated_64"
DEFAULT_STREAMS = (
    "terrain",
    "gameplay_graph",
    "building_selection",
    "structures",
    "decoration",
    "encounters",
)


def _sha256_truncated_64(parts: Iterable[str]) -> int:
    encoded = "|".join(str(part) for part in parts).encode("utf-8")
    return int(hashlib.sha256(encoded).hexdigest()[:16], 16)


def derive_root_seed(inputs: Iterable[str]) -> int:
    """Apply the exact WO-0056 contract algorithm to ordered inputs."""

    material = tuple(str(value) for value in inputs)
    if not material:
        raise ValueError("root seed derivation requires at least one input")
    return _sha256_truncated_64(material)


def derive_named_seed(root_seed: int, stream_name: str, scope: str = "global") -> int:
    """Derive an isolated deterministic stream from a root seed."""

    if root_seed < 0:
        raise ValueError("root_seed must be non-negative")
    if not stream_name:
        raise ValueError("stream_name must not be empty")
    if not scope:
        raise ValueError("scope must not be empty")
    return _sha256_truncated_64((str(root_seed), stream_name, scope))


@dataclass(frozen=True)
class SeedStreams:
    root_seed: int

    def seed(self, stream_name: str, scope: str = "global") -> int:
        return derive_named_seed(self.root_seed, stream_name, scope)

    def standard(self) -> dict[str, int]:
        return {name: self.seed(name) for name in DEFAULT_STREAMS}

    def structure(self, structure_id: str) -> int:
        return self.seed("structures", structure_id)
