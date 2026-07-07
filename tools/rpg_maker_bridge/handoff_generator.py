#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True
TOOL_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOL_DIR.parents[1]
ATLAS_GRAPH_DIR = REPO_ROOT / "tools" / "atlas_graph"
if str(ATLAS_GRAPH_DIR) not in sys.path:
    sys.path.insert(0, str(ATLAS_GRAPH_DIR))

from atlas_graph import DEFAULT_GRAPH_DIR, AtlasGraph, repo_root_from  # noqa: E402


DEFAULT_WORK_BREAKDOWN = Path("projects/the-last-sword-protocol/production/work-breakdown.md")
DEFAULT_BRIDGE_DIR = Path("bridges/rpg-maker-mz")
DEFAULT_TARGET_REPO = "TheLastSwordProtocol-Game"

ENGINE_PACKAGES = {
    "WP-03",
    "WP-04",
    "WP-05",
    "WP-06",
    "WP-07",
    "WP-09",
    "WP-10",
    "WP-11",
}

PACKAGE_PROFILES: dict[str, dict[str, Any]] = {
    "WP-03": {
        "source_nodes": ["location.ashford_village", "character.rowan"],
        "targets": [
            ("data/MapXXX.json", "unknown", "Audit village exterior/interior map IDs before edit."),
            ("data/CommonEvents.json", "unknown", "Add only approved shared dialogue/event helpers."),
        ],
        "protected": ["Existing human-authored village maps and NPC events."],
    },
    "WP-04": {
        "source_nodes": [
            "region.ashford_vale",
            "location.ashford_village",
            "location.hidden_cave",
            "location.glassfield_ruins",
            "location.rustshore_dock",
        ],
        "targets": [
            ("data/MapXXX.json", "unknown", "Audit overworld map ID before edit."),
            ("data/Troops.json", "unknown", "Use only approved encounter rows after audit."),
        ],
        "protected": ["Existing overworld map layout if human-edited or hand-authored."],
    },
    "WP-05": {
        "source_nodes": ["location.hidden_cave", "location.sword_shrine", "item.last_sword"],
        "targets": [
            ("data/MapXXX.json", "unknown", "Audit cave and shrine map IDs before edit."),
            ("data/Weapons.json", "unknown", "Reserve Last Sword database row before edit."),
            ("data/CommonEvents.json", "unknown", "Add sword-grant event only in approved range."),
        ],
        "protected": ["Existing item/database rows outside approved ranges."],
    },
    "WP-06": {
        "source_nodes": ["location.glassfield_ruins", "infrastructure.first_relay", "item.last_sword"],
        "targets": [
            ("data/MapXXX.json", "unknown", "Audit ruins and relay map IDs before edit."),
            ("data/CommonEvents.json", "unknown", "Add relay activation helper only if approved."),
            ("data/System.json", "human-edited", "Do not rewrite global system data."),
        ],
        "protected": ["Existing relay/ruins events; global system settings."],
    },
    "WP-07": {
        "source_nodes": ["location.rustshore_dock", "infrastructure.first_relay"],
        "targets": [
            ("data/MapXXX.json", "unknown", "Audit dock map ID before edit."),
            ("data/CommonEvents.json", "unknown", "Add departure transition only in approved range."),
        ],
        "protected": ["Existing dock events and transfer routes."],
    },
    "WP-09": {
        "source_nodes": ["region.ashford_vale", "location.hidden_cave", "location.glassfield_ruins"],
        "targets": [
            ("data/Enemies.json", "unknown", "Reserve enemy rows for six early monster families."),
            ("data/Troops.json", "unknown", "Reserve troop rows after enemy rows are known."),
            ("img/enemies/", "unknown", "Add or reference assets only after ownership audit."),
        ],
        "protected": ["Existing enemy/troop rows and existing image assets."],
    },
    "WP-10": {
        "source_nodes": ["region.ashford_vale"],
        "targets": [
            ("audio/bgm/", "unknown", "Add approved music tracks only."),
            ("audio/se/", "unknown", "Add approved sound effects only."),
            ("data/MapXXX.json", "unknown", "Wire cues only after map ownership is known."),
        ],
        "protected": ["Existing audio assets and map event pages."],
    },
    "WP-11": {
        "source_nodes": ["location.ashford_village", "location.rustshore_dock"],
        "targets": [
            ("data/MapXXX.json", "unknown", "Audit opening and credits map/event targets before edit."),
            ("data/CommonEvents.json", "unknown", "Add shared cutscene pattern only in approved range."),
        ],
        "protected": ["Existing cutscene events and transfer events."],
    },
}


@dataclass
class WorkPackage:
    package_id: str
    title: str
    covers: str = ""
    size: str = ""
    capability: str = ""
    providers: str = ""
    prerequisites: str = ""
    completion: str = ""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate safe RPG Maker MZ implementation handoff checklists from AtlasStudio work packages."
    )
    parser.add_argument("--project", default="the-last-sword-protocol", help="Project ID.")
    parser.add_argument(
        "--package",
        dest="package_id",
        help="Specific work package ID such as WP-03. Defaults to all engine-facing packages.",
    )
    parser.add_argument("--target-repo", default=DEFAULT_TARGET_REPO, help="Implementation repo label.")
    parser.add_argument("--output", help="Optional Markdown output path.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable handoff data.")
    args = parser.parse_args()

    root = repo_root_from()
    try:
        graph = AtlasGraph.load(DEFAULT_GRAPH_DIR, root=root)
        packages = parse_work_packages(root / DEFAULT_WORK_BREAKDOWN)
        bridge_docs = read_bridge_docs(root / DEFAULT_BRIDGE_DIR)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"RPG Maker Bridge handoff generation failed: {error}", file=sys.stderr)
        return 1

    selected = select_packages(packages, args.package_id)
    result = build_result(args.project, args.target_repo, selected, graph, bridge_docs)
    rendered = json.dumps(result, indent=2, sort_keys=True) if args.json else render_markdown(result)

    print(rendered)

    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = root / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered if rendered.endswith("\n") else rendered + "\n", encoding="utf-8")

    return 0


def parse_work_packages(path: Path) -> dict[str, WorkPackage]:
    text = path.read_text("utf-8")
    packages: dict[str, WorkPackage] = {}
    current: WorkPackage | None = None
    for line in text.splitlines():
        if line.startswith("### WP-"):
            heading = line.removeprefix("### ").strip()
            package_id, title = heading.split(" - ", 1)
            current = WorkPackage(package_id=package_id, title=title)
            packages[package_id] = current
            continue
        if current is None or not line.startswith("- **"):
            continue
        field = parse_field(line)
        if field is None:
            continue
        label, value = field
        if label == "Covers":
            current.covers = value
        elif label == "Size":
            current.size = value
        elif label == "Recommended capability":
            current.capability = value
        elif label == "Suggested providers":
            current.providers = value
        elif label == "Prerequisites":
            current.prerequisites = value
        elif label == "Completion definition":
            current.completion = value
    return packages


def parse_field(line: str) -> tuple[str, str] | None:
    text = line.removeprefix("- **")
    if ":**" not in text:
        return None
    label, value = text.split(":**", 1)
    return label.strip(), value.strip()


def read_bridge_docs(bridge_dir: Path) -> dict[str, dict[str, Any]]:
    required = {
        "bridge_design": bridge_dir / "bridge-design.md",
        "ownership_model": bridge_dir / "ownership-model.md",
        "handoff_format": bridge_dir / "handoff-format.md",
    }
    missing = [str(path) for path in required.values() if not path.exists()]
    if missing:
        raise ValueError("Missing bridge docs: " + ", ".join(missing))
    docs: dict[str, dict[str, Any]] = {}
    for key, path in required.items():
        text = path.read_text("utf-8")
        docs[key] = {
            "path": str(path),
            "headings": extract_headings(text),
        }
        if key == "handoff_format":
            docs[key]["template_sections"] = extract_template_sections(text)
        if key == "ownership_model":
            docs[key]["ownership_states"] = extract_ownership_states(text)
    return docs


def extract_headings(text: str) -> list[str]:
    return [
        line.removeprefix("## ").strip()
        for line in text.splitlines()
        if line.startswith("## ")
    ]


def extract_template_sections(text: str) -> list[str]:
    sections: list[str] = []
    in_template = False
    for line in text.splitlines():
        if line == "```markdown":
            in_template = True
            continue
        if in_template and line == "```":
            break
        if in_template and line.startswith("## "):
            sections.append(line.removeprefix("## ").strip())
    return sections


def extract_ownership_states(text: str) -> list[str]:
    states: list[str] = []
    for line in text.splitlines():
        if not line.startswith("| `"):
            continue
        state = line.split("|", 2)[1].strip().strip("`")
        if state:
            states.append(state)
    return states


def select_packages(packages: dict[str, WorkPackage], package_id: str | None) -> list[WorkPackage]:
    if package_id:
        if package_id not in packages:
            raise ValueError(f"Unknown work package: {package_id}")
        return [packages[package_id]]
    return [packages[package_id] for package_id in sorted(ENGINE_PACKAGES) if package_id in packages]


def build_result(
    project: str,
    target_repo: str,
    packages: list[WorkPackage],
    graph: AtlasGraph,
    bridge_docs: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    return {
        "project": project,
        "target_repo": target_repo,
        "generated_on": date.today().isoformat(),
        "mode": "read-only handoff generation",
        "bridge_docs": bridge_docs,
        "guardrails": [
            "Do not modify RPG Maker repositories during handoff generation.",
            "Treat unknown ownership as human-edited until audited.",
            "Do not change AtlasStudio canon from an RPG Maker implementation task.",
            "Do not run broad formatters over RPG Maker JSON.",
        ],
        "handoffs": [build_handoff(package, graph, project, target_repo) for package in packages],
    }


def build_handoff(
    package: WorkPackage, graph: AtlasGraph, project: str, target_repo: str
) -> dict[str, Any]:
    profile = PACKAGE_PROFILES.get(package.package_id, {})
    source_nodes = profile.get("source_nodes", [])
    missing_nodes = [node_id for node_id in source_nodes if graph.get_node(node_id) is None]
    targets = [
        {
            "target": target,
            "current_ownership": ownership,
            "allowed_change": allowed_change,
            "ownership_rule": ownership_rule(ownership),
        }
        for target, ownership, allowed_change in profile.get("targets", [])
    ]
    return {
        "work_package_id": package.package_id,
        "title": package.title,
        "target_repo": target_repo,
        "source_work_order": "WO-1000",
        "project": project,
        "recommended_agent": recommended_agent(package),
        "recommended_capability": package.capability,
        "suggested_providers": package.providers,
        "prerequisites": package.prerequisites,
        "completion_definition": package.completion,
        "source_nodes": source_nodes,
        "missing_source_nodes": missing_nodes,
        "rpg_maker_targets": targets,
        "protected_areas": profile.get("protected", []),
        "checklist": checklist_for(package, missing_nodes),
        "verification_steps": verification_steps_for(package),
    }


def ownership_rule(ownership: str) -> str:
    if ownership in {"human-edited", "hand-authored", "locked", "unknown"}:
        return "Audit before edit; do not overwrite existing content."
    if ownership == "agent-drafted":
        return "Agent may edit with clear diff and protected-range review."
    if ownership == "generated":
        return "May regenerate only when the implementation work order authorizes it."
    return "Audit before edit."


def checklist_for(package: WorkPackage, missing_nodes: list[str]) -> list[str]:
    checklist = [
        "Confirm human approval for the implementation work order before touching the RPG Maker repo.",
        "Inspect target RPG Maker files read-only and record ownership before edits.",
        "Reserve or confirm map, event, switch, variable, database, plugin, and asset ranges.",
        "Prefer additive edits; do not rewrite existing RPG Maker JSON blobs.",
        "Run file-level validation and a player-facing manual test after implementation.",
        "Record changed targets and ownership states in the submission report.",
    ]
    if missing_nodes:
        checklist.insert(
            0,
            "Resolve missing source graph nodes before implementation: " + ", ".join(missing_nodes),
        )
    if package.package_id == "WP-06":
        checklist.append("Confirm sword-acquired and relay-restored flags are named and reserved before wiring gates.")
    if package.package_id == "WP-07":
        checklist.append("Confirm dock departure remains locked until the relay-restored flag is set.")
    return checklist


def verification_steps_for(package: WorkPackage) -> list[str]:
    steps = [
        "Open RPG Maker project without JSON parse errors.",
        "Confirm no protected map/event/database target was overwritten.",
        "Run the exact player-facing route for this package.",
    ]
    if package.package_id == "WP-09":
        steps.append("Verify encounter tables reference implemented enemy and troop rows.")
    if package.package_id == "WP-10":
        steps.append("Verify every new cue plays from the intended map or event hook.")
    return steps


def recommended_agent(package: WorkPackage) -> str:
    providers = package.providers.lower()
    if "codex" in providers:
        return "codex"
    if "claude" in providers:
        return "claude-code"
    if "gpt" in providers:
        return "gpt"
    return "codex"


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# RPG Maker MZ Implementation Handoff Checklist",
        "",
        f"Project: `{result['project']}`",
        f"Target repo: `{result['target_repo']}`",
        f"Generated: {result['generated_on']}",
        f"Mode: {result['mode']}",
        "",
        "## Bridge Inputs",
        "",
    ]
    for label, doc in result["bridge_docs"].items():
        lines.append(f"- {label}: `{doc['path']}`")
        if label == "handoff_format":
            lines.append(
                "- handoff template sections: "
                + ", ".join(doc.get("template_sections", []))
            )
        if label == "ownership_model":
            states = ", ".join(f"`{state}`" for state in doc.get("ownership_states", []))
            lines.append(f"- ownership states: {states}")

    lines.extend(["", "## Guardrails", ""])
    for guardrail in result["guardrails"]:
        lines.append(f"- {guardrail}")

    for handoff in result["handoffs"]:
        lines.extend(["", f"## {handoff['work_package_id']} - {handoff['title']}", ""])
        lines.append(f"- Source work order: `{handoff['source_work_order']}`")
        lines.append(f"- Recommended agent: `{handoff['recommended_agent']}`")
        lines.append(f"- Capability: {handoff['recommended_capability']}")
        lines.append(f"- Suggested providers: {handoff['suggested_providers']}")
        lines.append(f"- Prerequisites: {handoff['prerequisites']}")
        lines.append(f"- Completion definition: {handoff['completion_definition']}")

        lines.extend(["", "### Source Graph Nodes", ""])
        if handoff["source_nodes"]:
            for node_id in handoff["source_nodes"]:
                marker = "missing" if node_id in handoff["missing_source_nodes"] else "ok"
                lines.append(f"- `{node_id}` ({marker})")
        else:
            lines.append("- No source nodes mapped yet; audit before implementation.")

        lines.extend(["", "### RPG Maker Targets", ""])
        if handoff["rpg_maker_targets"]:
            lines.append("| Target | Ownership | Allowed Change | Rule |")
            lines.append("|---|---|---|---|")
            for target in handoff["rpg_maker_targets"]:
                lines.append(
                    f"| `{target['target']}` | {target['current_ownership']} | "
                    f"{target['allowed_change']} | {target['ownership_rule']} |"
                )
        else:
            lines.append("- No targets mapped yet; create a target profile before implementation.")

        lines.extend(["", "### Protected Areas", ""])
        for item in handoff["protected_areas"] or ["Unknown ownership targets; audit first."]:
            lines.append(f"- {item}")

        lines.extend(["", "### Implementation Checklist", ""])
        for item in handoff["checklist"]:
            lines.append(f"- [ ] {item}")

        lines.extend(["", "### Verification Steps", ""])
        for item in handoff["verification_steps"]:
            lines.append(f"- [ ] {item}")

    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
