#!/usr/bin/env python3
"""Regenerate WO-0059's structural fixtures: three seeds per authored layout
family, across all three archetypes (Shop, Inn, House), using WO-0058's
SemanticAssembler unchanged. 7 layout families x 3 seeds = 21 candidates
(not 27 -- WO-0059 deliberately did not author a zoned/expanded tier for
Shop or House; see contract/README.md and each archetype's provenance)."""

from __future__ import annotations

import json
from pathlib import Path

from assembler import AssemblyBudget, SemanticAssembler
from seed_streams import SeedStreams, derive_root_seed
from structural_preview import render_ascii, render_svg


ROOT = Path(__file__).resolve().parent
EXAMPLES = ROOT / "contract" / "examples"
OUTPUT = ROOT / "prototypes" / "wo0059"

# (output slug, archetype dir, layout_family filename, tier, required_beats)
LAYOUT_FAMILIES = [
    ("shop-compact", "shop", "layout_family.json", "compact", ("exit_transfer", "npc_service_point")),
    ("shop-offset", "shop", "layout_family_offset.json", "offset_l", ("exit_transfer", "npc_service_point")),
    ("inn-compact", "inn", "layout_family_compact.json", "compact", ("exit_transfer", "npc_service_point")),
    ("inn-offset", "inn", "layout_family.json", "offset_l", ("exit_transfer", "npc_service_point")),
    ("inn-zoned-expanded", "inn", "layout_family_zoned_expanded.json", "zoned_expanded", ("exit_transfer", "npc_service_point")),
    ("house-compact", "house", "layout_family_compact.json", "compact", ("exit_transfer",)),
    ("house-offset", "house", "layout_family_offset.json", "offset_l", ("exit_transfer",)),
]

SEEDS_PER_FAMILY = 3


def load(relative: str) -> dict:
    return json.loads((EXAMPLES / relative).read_text(encoding="utf-8"))


def main() -> None:
    module_defs = {}
    for path in sorted((EXAMPLES / "shared").glob("module_*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        module_defs[payload["module_id"]] = payload

    OUTPUT.mkdir(parents=True, exist_ok=True)
    manifest_index: list[dict[str, object]] = []

    for slug, archetype_dir, layout_family_file, tier, required_beats in LAYOUT_FAMILIES:
        map_intent = load(f"{archetype_dir}/map_intent.json")
        gameplay_graph = load(f"{archetype_dir}/gameplay_graph.json")
        archetype = load(f"{archetype_dir}/building_archetype.json")
        layout_family = load(f"{archetype_dir}/{layout_family_file}")
        assert layout_family.get("tier") == tier, f"{slug}: expected tier {tier!r}, found {layout_family.get('tier')!r}"

        for index in range(1, SEEDS_PER_FAMILY + 1):
            seed = derive_root_seed((slug, f"seed-{index}", "WO-0059"))
            manifest_id = f"GEN-WO0059-FIXTURE-{slug.upper()}-{index:03d}"
            result = SemanticAssembler(budget=AssemblyBudget(5000, 20)).assemble(
                map_intent=map_intent,
                gameplay_graph=gameplay_graph,
                archetype=archetype,
                layout_family=layout_family,
                modules=module_defs,
                streams=SeedStreams(seed),
                manifest_id=manifest_id,
                required_beats=required_beats,
            )
            stem = OUTPUT / f"{slug}-seed-{index}"
            stem.with_suffix(".map_plan.json").write_text(result.map_plan.to_json(), encoding="utf-8")
            stem.with_suffix(".txt").write_text(render_ascii(result.map_plan), encoding="utf-8")
            stem.with_suffix(".svg").write_text(render_svg(result.map_plan), encoding="utf-8")
            manifest_index.append({
                "slug": slug,
                "archetype_id": archetype["archetype_id"],
                "layout_family_id": layout_family["layout_family_id"],
                "tier": tier,
                "seed_index": index,
                "manifest_id": manifest_id,
                "root_seed": seed,
                "variant_id": result.variant_id,
                "rotation": result.rotation,
                "reflected": result.reflected,
                "attempts": result.attempts,
                "dimensions": result.map_plan.to_dict()["dimensions"],
                "landmark_slots": result.map_plan.to_dict().get("landmark_slots", []),
            })

    (OUTPUT / "index.json").write_text(
        json.dumps({"schema_version": "0.1", "candidate_count": len(manifest_index), "candidates": manifest_index}, indent=2),
        encoding="utf-8",
    )
    print(f"Generated {len(manifest_index)} structural candidates across {len(LAYOUT_FAMILIES)} layout families.")


if __name__ == "__main__":
    main()
