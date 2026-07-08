#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True
TOOL_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOL_DIR.parents[1]
ACADEMY_DIR = REPO_ROOT / "academy"

# Directories a given `list`/`study`/`report`/`references` kind reads from, and
# the file extension that kind's records use. Every entry here is read-only -
# this CLI never writes into any of these directories, per
# work-orders/WO-2009-atlas-academy-cli.md's "Do not create analysis content
# automatically unless explicitly requested by the command" constraint (no
# command in this tool creates content at all).
KIND_DIRS: dict[str, list[Path]] = {
    "case-studies": [ACADEMY_DIR / "case-studies"],
    "knowledge": [ACADEMY_DIR / "knowledge"],
    "compositions": [ACADEMY_DIR / "compositions"],
    "observations": [ACADEMY_DIR / "observations"],
    "reports": [ACADEMY_DIR / "reports", REPO_ROOT / "reports" / "academy"],
    "references": [ACADEMY_DIR / "references"],
    "templates": [ACADEMY_DIR / "templates"],
}
KIND_GLOB: dict[str, str] = {
    "observations": "*.json",
}
DEFAULT_GLOB = "*.md"
GRADES_DIR = ACADEMY_DIR / "grades"


def main(argv: list[str] | None = None) -> int:
    args_list = list(sys.argv[1:] if argv is None else argv)
    parser = build_parser()
    args = parser.parse_args(args_list)

    if args.command in (None, "help"):
        print_help_text()
        return 0
    if args.command == "list":
        return handle_list(args)
    if args.command == "study":
        return handle_study(args)
    if args.command == "report":
        return handle_report(args)
    if args.command == "grade":
        return handle_grade(args)
    if args.command == "references":
        return handle_references(args)

    parser.print_help(sys.stderr)
    return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="atlas academy",
        description="Read-only interface to Atlas Academy's studies, knowledge, reports, and grades.",
    )
    subparsers = parser.add_subparsers(dest="command")

    list_parser = subparsers.add_parser("list", help="List Academy artifacts by kind.")
    list_parser.add_argument(
        "--kind",
        choices=sorted(KIND_DIRS) + ["all"],
        default="all",
    )
    list_parser.add_argument("--json", action="store_true")

    study_parser = subparsers.add_parser("study", help="Show one case study under academy/case-studies/.")
    study_parser.add_argument("study_id")
    study_parser.add_argument("--full", action="store_true", help="Print the full file instead of a section summary.")
    study_parser.add_argument("--json", action="store_true")

    report_parser = subparsers.add_parser("report", help="Show one evidence report under academy/reports/ or reports/academy/.")
    report_parser.add_argument("name")
    report_parser.add_argument("--full", action="store_true")
    report_parser.add_argument("--json", action="store_true")

    grade_parser = subparsers.add_parser("grade", help="Look up a filed map-grade record under academy/grades/.")
    grade_parser.add_argument("target", nargs="?", help="grade_id or a substring of the target file_path.")
    grade_parser.add_argument("--json", action="store_true")

    references_parser = subparsers.add_parser("references", help="List academy/references/ governance and source documents.")
    references_parser.add_argument("--json", action="store_true")

    subparsers.add_parser("help", help="Show this command summary.")
    return parser


def handle_list(args: argparse.Namespace) -> int:
    kinds = sorted(KIND_DIRS) if args.kind == "all" else [args.kind]
    payload: dict[str, list[dict[str, Any]]] = {}
    for kind in kinds:
        payload[kind] = [describe_file(path) for path in kind_files(kind)]

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        total = 0
        for kind in kinds:
            items = payload[kind]
            print(f"{kind} ({len(items)}):")
            for item in items:
                title = item["title"] or "(untitled)"
                status = f" [{item['status']}]" if item["status"] else ""
                print(f"  {item['path']:<55} {title}{status}")
            total += len(items)
            print()
        if total == 0:
            print("No Academy artifacts found for the requested kind(s).")
    total_items = sum(len(v) for v in payload.values())
    return 0 if total_items else 9


def kind_files(kind: str) -> list[Path]:
    glob = KIND_GLOB.get(kind, DEFAULT_GLOB)
    files: list[Path] = []
    for directory in KIND_DIRS[kind]:
        if not directory.exists():
            continue
        for path in sorted(directory.glob(glob)):
            if path.name == "README.md":
                continue
            files.append(path)
    return files


def describe_file(path: Path) -> dict[str, Any]:
    if path.suffix == ".json":
        try:
            data = json.loads(path.read_text("utf-8"))
        except (OSError, json.JSONDecodeError):
            data = {}
        title = data.get("observation_id") or data.get("grade_id") or data.get("review_id")
        status = None
    else:
        text = path.read_text("utf-8")
        title = parse_title(text)
        status = parse_status(text)
    return {"path": repo_relative(path), "title": title, "status": status}


def parse_title(text: str) -> str | None:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return None


def parse_status(text: str) -> str | None:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        match = re.match(r"^Status:\s*(.+)$", line.strip())
        if match:
            return truncate(match.group(1).strip())
        if line.strip() == "## Status":
            for candidate in lines[index + 1 :]:
                if candidate.strip():
                    return truncate(candidate.strip())
    return None


def truncate(text: str, limit: int = 90) -> str:
    first_sentence = re.split(r"(?<=[.:])\s", text, maxsplit=1)[0]
    value = first_sentence if len(first_sentence) <= limit else text
    return value if len(value) <= limit else value[: limit - 1].rstrip() + "…"


def handle_study(args: argparse.Namespace) -> int:
    return show_named_document(
        candidates=kind_files("case-studies"),
        query=args.study_id,
        full=args.full,
        as_json=args.json,
        not_found_message="No case study matches",
    )


def handle_report(args: argparse.Namespace) -> int:
    return show_named_document(
        candidates=kind_files("reports"),
        query=args.name,
        full=args.full,
        as_json=args.json,
        not_found_message="No report matches",
    )


def show_named_document(
    *,
    candidates: list[Path],
    query: str,
    full: bool,
    as_json: bool,
    not_found_message: str,
) -> int:
    matches = [path for path in candidates if query.lower() in path.stem.lower()]
    if not matches:
        print(f"{not_found_message} '{query}'.", file=sys.stderr)
        print("Available:", file=sys.stderr)
        for path in candidates:
            print(f"  {repo_relative(path)}", file=sys.stderr)
        return 1
    if len(matches) > 1:
        print(f"'{query}' is ambiguous; matches:", file=sys.stderr)
        for path in matches:
            print(f"  {repo_relative(path)}", file=sys.stderr)
        return 1

    path = matches[0]
    text = path.read_text("utf-8")
    if as_json:
        payload = {
            "path": repo_relative(path),
            "title": parse_title(text),
            "status": parse_status(text),
            "sections": section_headings(text),
            "text": text if full else None,
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    print(f"{repo_relative(path)}")
    title = parse_title(text)
    if title:
        print(title)
    status = parse_status(text)
    if status:
        print(f"Status: {status}")
    if full:
        print()
        print(text)
    else:
        print()
        print("Sections:")
        for heading in section_headings(text):
            print(f"  {heading}")
        print()
        print("(use --full to print the entire file)")
    return 0


def section_headings(text: str) -> list[str]:
    return [line.strip("# ").strip() for line in text.splitlines() if line.startswith("## ")]


def handle_grade(args: argparse.Namespace) -> int:
    if not GRADES_DIR.exists():
        message = (
            "No filed grade records yet (academy/grades/ does not exist). "
            "See academy/grading-system.md and the worked example "
            "(GRD-ASHFORDINN-001) embedded in reports/academy/map-grading-system.md - "
            "no grade has been filed as a standalone schemas/academy-map-grade.schema.json "
            "record yet."
        )
        if args.json:
            print(json.dumps({"grades_dir_exists": False, "message": message, "matches": []}, indent=2))
        else:
            print(message)
        return 9

    records = sorted(GRADES_DIR.glob("*.json"))
    matches = []
    for path in records:
        try:
            data = json.loads(path.read_text("utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if args.target is None:
            matches.append((path, data))
            continue
        needle = args.target.lower()
        haystack = " ".join(
            str(data.get(field, "")) for field in ("grade_id", "target")
        ).lower()
        if needle in haystack:
            matches.append((path, data))

    if args.json:
        print(json.dumps(
            [{"path": repo_relative(path), "record": data} for path, data in matches],
            indent=2,
            sort_keys=True,
        ))
    else:
        if not matches:
            print(f"No filed grade record matches '{args.target}'." if args.target else "No filed grade records.")
        for path, data in matches:
            print(f"{repo_relative(path)}  {data.get('grade_id', '')}  outcome={data.get('outcome', '')}")
    return 0 if matches else 9


def handle_references(args: argparse.Namespace) -> int:
    items = [describe_file(path) for path in kind_files("references")]
    if args.json:
        print(json.dumps(items, indent=2, sort_keys=True))
    else:
        for item in items:
            status = f" [{item['status']}]" if item["status"] else ""
            print(f"{item['path']:<45} {item['title'] or '(untitled)'}{status}")
        if not items:
            print("No reference documents found under academy/references/.")
    return 0 if items else 9


def repo_relative(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def print_help_text() -> None:
    print("atlas academy - read-only interface to Atlas Academy")
    print()
    print("  list        [--kind KIND] [--json]   List Academy artifacts.")
    print("  study       STUDY_ID [--full] [--json]  Show one case study.")
    print("  report      NAME [--full] [--json]       Show one evidence report.")
    print("  grade       [TARGET] [--json]            Look up a filed grade record.")
    print("  references  [--json]                     List reference-governance docs.")
    print("  help                                      Show this summary.")
    print()
    print("This command group is read-only: it never creates or edits an Academy")
    print("document, observation, grade, or map. It reads what already exists on disk.")


if __name__ == "__main__":
    raise SystemExit(main())
