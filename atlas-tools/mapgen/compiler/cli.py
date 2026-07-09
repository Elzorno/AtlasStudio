"""CLI for the Atlas Map Compiler foundation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from models import TerrainModel
from planner import TerrainPlanner
from quality_auditor import QualityAuditor
from spec_parser import load_world_spec


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Atlas Map Compiler foundation.")
    sub = parser.add_subparsers(dest="command", required=True)

    generate = sub.add_parser("generate-prototype", help="Generate an intermediate terrain model.")
    generate.add_argument("--spec", required=True, type=Path)
    generate.add_argument("--output", required=True, type=Path)
    generate.set_defaults(func=handle_generate)

    audit_terrain = sub.add_parser("audit-terrain", help="Audit an intermediate terrain model.")
    audit_terrain.add_argument("--spec", type=Path)
    audit_terrain.add_argument("--terrain", required=True, type=Path)
    audit_terrain.add_argument("--output", type=Path)
    audit_terrain.set_defaults(func=handle_audit_terrain)

    audit_map = sub.add_parser("audit-map", help="Audit an RPG Maker map as an overworld candidate.")
    audit_map.add_argument("--map", required=True, type=Path)
    audit_map.add_argument("--output", type=Path)
    audit_map.set_defaults(func=handle_audit_map)

    return parser


def handle_generate(args: argparse.Namespace) -> int:
    spec = load_world_spec(args.spec)
    model = TerrainPlanner().build(spec)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(model.to_dict(), indent=2) + "\n", encoding="utf-8")
    print(f"Wrote terrain prototype: {args.output}")
    return 0


def handle_audit_terrain(args: argparse.Namespace) -> int:
    model = TerrainModel.from_dict(json.loads(args.terrain.read_text(encoding="utf-8")))
    spec = load_world_spec(args.spec) if args.spec else None
    result = QualityAuditor().audit_terrain_model(model, spec)
    emit_result(result.to_dict(), args.output)
    return 0 if result.passed else 1


def handle_audit_map(args: argparse.Namespace) -> int:
    result = QualityAuditor().audit_rpgmaker_map(args.map)
    emit_result(result.to_dict(), args.output)
    return 0 if result.passed else 1


def emit_result(payload: dict, output: Path | None) -> None:
    rendered = json.dumps(payload, indent=2)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered + "\n", encoding="utf-8")
        print(f"Wrote audit: {output}")
    else:
        print(rendered)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
