"""RPG Maker tile-painter boundary for the Atlas Map Compiler.

WO-0025 intentionally stops at terrain intent. The painter exists as a named
pipeline stage so future work can add RPG Maker MZ tile emission without hiding
that missing step inside the planner.
"""

from __future__ import annotations

from dataclasses import dataclass

from models import TerrainModel


class TilePainterUnavailable(RuntimeError):
    """Raised when a caller asks WO-0025 to produce finished RPG Maker tiles."""


@dataclass(frozen=True)
class TilePainterPlan:
    terrain_region_id: str
    target_engine: str
    status: str
    reason: str

    def to_dict(self) -> dict[str, str]:
        return {
            "terrain_region_id": self.terrain_region_id,
            "target_engine": self.target_engine,
            "status": self.status,
            "reason": self.reason,
        }


def describe_painter_plan(model: TerrainModel, target_engine: str = "RPG Maker MZ") -> TilePainterPlan:
    return TilePainterPlan(
        terrain_region_id=model.region_id,
        target_engine=target_engine,
        status="deferred",
        reason="WO-0025 produces intermediate terrain plans only; tile painting is a later work order.",
    )


def paint_tiles(model: TerrainModel, target_engine: str = "RPG Maker MZ") -> None:
    plan = describe_painter_plan(model, target_engine)
    raise TilePainterUnavailable(plan.reason)
