#!/usr/bin/env python3
"""Regenerate the three deterministic WO-0058 structural fixtures."""

from __future__ import annotations

import json
from pathlib import Path

from assembler import AssemblyBudget, SemanticAssembler
from seed_streams import SeedStreams, derive_root_seed
from structural_preview import render_ascii, render_svg


ROOT = Path(__file__).resolve().parent
EXAMPLES = ROOT / "contract" / "examples"
OUTPUT = ROOT / "prototypes" / "wo0058"


def load(relative: str) -> dict:
    return json.loads((EXAMPLES / relative).read_text(encoding="utf-8"))


def main() -> None:
    module_defs = {}
    for path in sorted((EXAMPLES / "shared").glob("module_*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        module_defs[payload["module_id"]] = payload
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for index, label in enumerate(("ashford-shop-a", "ashford-shop-b", "ashford-shop-c"), start=1):
        seed = derive_root_seed((label, "WO-0058"))
        result = SemanticAssembler(budget=AssemblyBudget(5000, 20)).assemble(
            map_intent=load("shop/map_intent.json"), gameplay_graph=load("shop/gameplay_graph.json"),
            archetype=load("shop/building_archetype.json"), layout_family=load("shop/layout_family.json"),
            modules=module_defs, streams=SeedStreams(seed), manifest_id=f"GEN-WO0058-FIXTURE-{index:03d}",
            required_beats=("exit_transfer", "npc_service_point"),
        )
        stem = OUTPUT / f"shop-seed-{index}"
        stem.with_suffix(".map_plan.json").write_text(result.map_plan.to_json(), encoding="utf-8")
        stem.with_suffix(".txt").write_text(render_ascii(result.map_plan), encoding="utf-8")
        stem.with_suffix(".svg").write_text(render_svg(result.map_plan), encoding="utf-8")


if __name__ == "__main__":
    main()
