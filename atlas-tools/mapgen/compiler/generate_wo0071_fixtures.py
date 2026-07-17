#!/usr/bin/env python3
"""Regenerate WO-0071's disposable fixtures: the Ashford exterior-settlement
compiler-example (map_intent/gameplay_graph/building_archetype/layout_family)
run through SemanticAssembler with the real, human-approved MV-HOM-ASH-001
MapVision, AVCP-HOM-ASH-001 constraint profile, and the real Ashford
TileAssembly catalog (reference kit + authored kit + custom tileset
extension) from TheLastSwordProtocol-Atlas / AtlasStudio.

Two required_beats combinations x two seeds = 4 candidates, each with a
GenerationManifest carrying map_vision_ref + tile_assembly_bindings
provenance, and a WO-0072 dual-gate evidence file with a pending human
decision. Nothing here writes to TheLastSwordProtocol-Game; every output
lands under prototypes/wo0071/, matching the WO-0058/WO-0059 convention."""

from __future__ import annotations

import json
from pathlib import Path

from assembler import AssemblyBudget, SemanticAssembler
from generation_manifest import GenerationManifest
from quality_gate import record_gate_evidence, run_dual_gate
from seed_streams import SeedStreams, derive_root_seed
from structural_preview import render_ascii, render_svg
from tile_assembly_catalog import (
    load_custom_extension_manifest,
    load_tile_assembly_kit_index,
    merge_catalogs,
)


COMPILER_DIR = Path(__file__).resolve().parent
EXAMPLES = COMPILER_DIR / "contract" / "examples" / "ashford"
SHARED = COMPILER_DIR / "contract" / "examples" / "shared"
OUTPUT = COMPILER_DIR / "prototypes" / "wo0071"

KIT_DIR = COMPILER_DIR.parent / "tile_assembly" / "kits" / "ashford"
ATLAS_MAP_GENERATION_DIR = (
    COMPILER_DIR.parents[3] / "TheLastSwordProtocol-Atlas" / "atlas" / "docs"
    / "09_Technical" / "Map_Generation"
)

REQUIRED_BEAT_COMBINATIONS = [
    ("core", ("exit_transfer",)),
    ("dressed", ("exit_transfer", "cultivation_dressing", "forest_dressing")),
]
SEEDS_PER_COMBINATION = 2


def load_example(name: str) -> dict:
    return json.loads((EXAMPLES / name).read_text(encoding="utf-8"))


def load_modules() -> dict[str, dict]:
    result = {}
    for path in sorted(SHARED.glob("module_*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        result[payload["module_id"]] = payload
    return result


def load_catalog() -> dict:
    return merge_catalogs(
        load_tile_assembly_kit_index(KIT_DIR / "index.json"),
        load_tile_assembly_kit_index(KIT_DIR / "authored" / "index.json"),
        load_custom_extension_manifest(KIT_DIR / "custom_extension" / "manifest.json"),
    )


def load_map_vision() -> dict:
    return json.loads(
        (ATLAS_MAP_GENERATION_DIR / "Instances" / "MV-HOM-ASH-001.json").read_text(encoding="utf-8")
    )


def load_constraint_profile() -> dict:
    return json.loads(
        (ATLAS_MAP_GENERATION_DIR / "Academy" / "ASHFORD-VISUAL-CONSTRAINT-PROFILE-001.json").read_text(
            encoding="utf-8"
        )
    )


def main() -> None:
    map_intent = load_example("map_intent.json")
    gameplay_graph = load_example("gameplay_graph.json")
    archetype = load_example("building_archetype.json")
    layout_family = load_example("layout_family.json")
    modules = load_modules()
    catalog = load_catalog()
    map_vision = load_map_vision()
    constraint_profile = load_constraint_profile()

    OUTPUT.mkdir(parents=True, exist_ok=True)
    candidate_index: list[dict[str, object]] = []

    for slug, required_beats in REQUIRED_BEAT_COMBINATIONS:
        for index in range(1, SEEDS_PER_COMBINATION + 1):
            seed = derive_root_seed((slug, f"seed-{index}", "WO-0071"))
            manifest_id = f"GEN-WO0071-FIXTURE-{slug.upper()}-{index:03d}"
            result = SemanticAssembler(budget=AssemblyBudget(5000, 20)).assemble(
                map_intent=map_intent,
                gameplay_graph=gameplay_graph,
                archetype=archetype,
                layout_family=layout_family,
                modules=modules,
                streams=SeedStreams(seed),
                manifest_id=manifest_id,
                required_beats=required_beats,
                assembly_catalog=catalog,
                map_vision=map_vision,
                visual_constraint_profile=constraint_profile,
            )
            manifest = GenerationManifest.create(
                manifest_id=manifest_id,
                map_intent_id=map_intent["map_intent_id"],
                generator_id="atlas-reusable-map-compiler",
                generator_version="0.1.0",
                archetype_id=archetype["archetype_id"],
                archetype_version=archetype["version"],
                layout_family_id=layout_family["layout_family_id"],
                layout_family_version=layout_family["version"],
                variant_id=result.variant_id,
                style_pack_id="STY-NONE-EXTERIOR-VISUAL-PIPELINE",
                style_pack_version="0.1",
                salt=f"wo-0071-{slug}-{index}",
                generated_at="2026-07-15",
                map_vision_id=map_vision["map_vision_id"],
                map_vision_version=map_vision["version"],
                tile_assembly_bindings=list(result.tile_assembly_bindings),
                output_map_plan_ref=result.map_plan.blueprint_id,
            )
            stem = OUTPUT / f"{slug}-seed-{index}"
            stem.with_suffix(".map_plan.json").write_text(result.map_plan.to_json(), encoding="utf-8")
            stem.with_suffix(".generation_manifest.json").write_text(manifest.to_json(), encoding="utf-8")
            stem.with_suffix(".txt").write_text(render_ascii(result.map_plan), encoding="utf-8")
            stem.with_suffix(".svg").write_text(render_svg(result.map_plan), encoding="utf-8")

            gate_result = run_dual_gate(result.map_plan.to_dict(), manifest.to_dict())
            evidence = record_gate_evidence(
                gate_result,
                concept_refs=[
                    "TheLastSwordProtocol-Atlas/atlas/docs/09_Technical/Map_Generation/Concepts/Ashford/ashford-overhead-composition-v2.png",
                    "TheLastSwordProtocol-Atlas/atlas/docs/09_Technical/Map_Generation/Concepts/Ashford/ashford-building-silhouettes-v2.png",
                ],
                render_refs=[
                    f"atlas-tools/mapgen/compiler/prototypes/wo0071/{stem.name}.svg",
                    f"atlas-tools/mapgen/compiler/prototypes/wo0071/{stem.name}.txt",
                ],
                output_path=stem.with_suffix(".gate_evidence.json"),
            )
            candidate_index.append({
                "slug": slug,
                "seed_index": index,
                "manifest_id": manifest_id,
                "root_seed": seed,
                "required_beats": list(required_beats),
                "variant_id": result.variant_id,
                "attempts": result.attempts,
                "dimensions": result.map_plan.to_dict()["dimensions"],
                "tile_assembly_bindings": list(result.tile_assembly_bindings),
                "gate_recommendation": evidence["recommendation"],
            })

    (OUTPUT / "index.json").write_text(
        json.dumps(
            {
                "schema_version": "0.1",
                "map_vision_ref": f"{map_vision['map_vision_id']}@{map_vision['version']}",
                "candidate_count": len(candidate_index),
                "candidates": candidate_index,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Generated {len(candidate_index)} Ashford exterior candidates across {len(REQUIRED_BEAT_COMBINATIONS)} beat combinations.")


if __name__ == "__main__":
    main()
