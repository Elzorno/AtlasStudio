#!/usr/bin/env python3
from __future__ import annotations

import argparse
import difflib
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any


sys.dont_write_bytecode = True
TOOL_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOL_DIR.parents[1]
ATLAS_GRAPH_DIR = REPO_ROOT / "tools" / "atlas_graph"
if str(ATLAS_GRAPH_DIR) not in sys.path:
    sys.path.insert(0, str(ATLAS_GRAPH_DIR))

from atlas_graph import DEFAULT_GRAPH_DIR, repo_root_from  # noqa: E402


WORKING_TREE = "working tree"
BROAD_CHURN_LINE_THRESHOLD = 40
BROAD_CHURN_RATIO_THRESHOLD = 0.5


@dataclass(frozen=True)
class FileSnapshot:
    path: str
    text: str | None
    label: str


@dataclass
class FormatFinding:
    path: str
    classification: str
    semantic_changed: bool
    formatting_changed: bool
    suspicious: bool
    changed_lines: int
    total_lines: int
    summary: str
    details: list[str]

    def to_json(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "classification": self.classification,
            "semantic_changed": self.semantic_changed,
            "formatting_changed": self.formatting_changed,
            "suspicious": self.suspicious,
            "changed_lines": self.changed_lines,
            "total_lines": self.total_lines,
            "summary": self.summary,
            "details": self.details,
        }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check AtlasStudio graph JSON diffs for suspicious formatting churn."
    )
    parser.add_argument("--check", action="store_true", help="Run in check-only mode.")
    parser.add_argument(
        "--graph-dir",
        default=str(DEFAULT_GRAPH_DIR),
        help="Graph directory to inspect. Defaults to the Last Sword Protocol graph.",
    )
    parser.add_argument("--base", default="HEAD", help="Base Git ref. Defaults to HEAD.")
    parser.add_argument("--head", help="Head Git ref. Defaults to the working tree.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable results.")
    parser.add_argument("--output", help="Optional report output path.")
    parser.add_argument(
        "--fail-on-warning",
        action="store_true",
        help="Exit 1 when suspicious formatting churn is found.",
    )
    args = parser.parse_args()

    root = repo_root_from()
    try:
        result = build_result(root, args.graph_dir, args.base, args.head)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Format Guard failed: {error}", file=sys.stderr)
        return 1

    rendered = json.dumps(result, indent=2, sort_keys=True) if args.json else render_report(result)
    print(rendered)

    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = root / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered + "\n", encoding="utf-8")

    if result["invalid_json_count"]:
        return 1
    if args.fail_on_warning and result["suspicious_count"]:
        return 1
    return 0


def build_result(root: Path, graph_dir: str | Path, base: str, head: str | None) -> dict[str, Any]:
    graph_path = normalize_graph_path(root, graph_dir)
    base_files = load_git_graph_files(root, graph_path, base)
    if head:
        head_files = load_git_graph_files(root, graph_path, head)
        head_label = head
    else:
        head_files = load_working_graph_files(root, graph_path)
        head_label = WORKING_TREE

    findings = [
        analyze_file(
            FileSnapshot(path, base_files.get(path), base),
            FileSnapshot(path, head_files.get(path), head_label),
        )
        for path in sorted(set(base_files) | set(head_files))
        if base_files.get(path) != head_files.get(path)
    ]

    counts = {
        "semantic": sum(1 for finding in findings if finding.classification == "semantic"),
        "formatting_only": sum(
            1 for finding in findings if finding.classification == "formatting-only"
        ),
        "mixed": sum(1 for finding in findings if finding.classification == "mixed"),
        "added": sum(1 for finding in findings if finding.classification == "added"),
        "removed": sum(1 for finding in findings if finding.classification == "removed"),
        "invalid_json": sum(1 for finding in findings if finding.classification == "invalid-json"),
    }

    return {
        "mode": "check-only",
        "graph_dir": graph_path.as_posix(),
        "base": base,
        "head": head_label,
        "changed_file_count": len(findings),
        "suspicious_count": sum(1 for finding in findings if finding.suspicious),
        "invalid_json_count": counts["invalid_json"],
        "counts": counts,
        "findings": [finding.to_json() for finding in findings],
    }


def analyze_file(base: FileSnapshot, head: FileSnapshot) -> FormatFinding:
    if base.text is None:
        return FormatFinding(
            path=head.path,
            classification="added",
            semantic_changed=True,
            formatting_changed=False,
            suspicious=False,
            changed_lines=count_lines(head.text),
            total_lines=count_lines(head.text),
            summary="New graph JSON file.",
            details=[],
        )
    if head.text is None:
        return FormatFinding(
            path=base.path,
            classification="removed",
            semantic_changed=True,
            formatting_changed=False,
            suspicious=False,
            changed_lines=count_lines(base.text),
            total_lines=count_lines(base.text),
            summary="Graph JSON file was removed.",
            details=[],
        )

    changed_lines = changed_line_count(base.text, head.text)
    total_lines = max(count_lines(base.text), count_lines(head.text), 1)

    try:
        base_data = json.loads(base.text)
        head_data = json.loads(head.text)
    except json.JSONDecodeError as error:
        return FormatFinding(
            path=base.path,
            classification="invalid-json",
            semantic_changed=True,
            formatting_changed=True,
            suspicious=True,
            changed_lines=changed_lines,
            total_lines=total_lines,
            summary="Changed graph file contains invalid JSON.",
            details=[str(error)],
        )

    semantic_changed = base_data != head_data
    canonical_changed = canonical_json(base_data) != canonical_json(head_data)
    formatting_changed = base.text != head.text and not canonical_changed
    broad_churn = is_broad_churn(changed_lines, total_lines)

    if not semantic_changed:
        classification = "formatting-only"
        summary = "Graph JSON meaning is unchanged; text formatting changed."
        suspicious = broad_churn or changed_lines > 0
    elif broad_churn:
        classification = "mixed"
        summary = "Graph JSON facts changed alongside broad text churn."
        suspicious = True
    else:
        classification = "semantic"
        summary = "Graph JSON facts changed without broad formatting churn."
        suspicious = False

    details = [
        f"changed lines: {changed_lines}/{total_lines}",
        f"semantic changed: {yes_no(semantic_changed)}",
        f"formatting-only changed: {yes_no(formatting_changed)}",
    ]
    if broad_churn:
        details.append("broad churn heuristic triggered")

    return FormatFinding(
        path=base.path,
        classification=classification,
        semantic_changed=semantic_changed,
        formatting_changed=formatting_changed,
        suspicious=suspicious,
        changed_lines=changed_lines,
        total_lines=total_lines,
        summary=summary,
        details=details,
    )


def load_working_graph_files(root: Path, graph_path: PurePosixPath) -> dict[str, str]:
    directory = root / graph_path
    files: dict[str, str] = {}
    for path in sorted(directory.glob("*/*.json")):
        if is_graph_json(path):
            rel = path.relative_to(root).as_posix()
            files[rel] = path.read_text("utf-8")
    return files


def load_git_graph_files(root: Path, graph_path: PurePosixPath, ref: str) -> dict[str, str]:
    listing = run_git(
        ["ls-tree", "-r", "--name-only", ref, "--", graph_path.as_posix()],
        root,
        f"Cannot list graph files at {ref!r}",
    )
    files: dict[str, str] = {}
    for line in sorted(listing.splitlines()):
        path = PurePosixPath(line)
        if not is_graph_json(path):
            continue
        files[line] = run_git(["show", f"{ref}:{line}"], root, f"Cannot read {line} at {ref!r}")
    return files


def normalize_graph_path(root: Path, graph_dir: str | Path) -> PurePosixPath:
    graph_path = Path(graph_dir)
    if graph_path.is_absolute():
        graph_path = graph_path.relative_to(root)
    return PurePosixPath(graph_path.as_posix())


def is_graph_json(path: Path | PurePosixPath) -> bool:
    name = path.name
    parent = path.parent.name
    return parent in {"nodes", "edges"} and (
        name.endswith(".nodes.json") or name.endswith(".edges.json")
    )


def changed_line_count(base_text: str, head_text: str) -> int:
    diff = difflib.SequenceMatcher(None, base_text.splitlines(), head_text.splitlines())
    count = 0
    for tag, base_start, base_end, head_start, head_end in diff.get_opcodes():
        if tag == "equal":
            continue
        count += max(base_end - base_start, head_end - head_start)
    return count


def count_lines(text: str | None) -> int:
    if text is None:
        return 0
    return len(text.splitlines())


def canonical_json(data: Any) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def is_broad_churn(changed_lines: int, total_lines: int) -> bool:
    if changed_lines >= BROAD_CHURN_LINE_THRESHOLD:
        return True
    return total_lines > 0 and changed_lines / total_lines >= BROAD_CHURN_RATIO_THRESHOLD


def render_report(result: dict[str, Any]) -> str:
    lines = [
        "# Immutable Formatting Guard",
        "",
        f"Mode: `{result['mode']}`",
        f"Graph directory: `{result['graph_dir']}`",
        f"Base: `{result['base']}`",
        f"Head: `{result['head']}`",
        "",
        "## Summary",
        "",
        f"- Changed graph JSON files: {result['changed_file_count']}",
        f"- Suspicious formatting warnings: {result['suspicious_count']}",
        f"- Invalid JSON files: {result['invalid_json_count']}",
        f"- Semantic-only files: {result['counts']['semantic']}",
        f"- Formatting-only files: {result['counts']['formatting_only']}",
        f"- Mixed semantic/formatting files: {result['counts']['mixed']}",
        f"- Added files: {result['counts']['added']}",
        f"- Removed files: {result['counts']['removed']}",
    ]

    append_findings(
        lines,
        "Formatting-Only Changes",
        result["findings"],
        {"formatting-only"},
        empty="None.",
    )
    append_findings(
        lines,
        "Semantic Changes",
        result["findings"],
        {"semantic", "added", "removed"},
        empty="None.",
    )
    append_findings(
        lines,
        "Mixed Or Suspicious Changes",
        result["findings"],
        {"mixed", "invalid-json"},
        only_suspicious=True,
        empty="None.",
    )

    if result["suspicious_count"]:
        lines.extend(
            [
                "",
                "## Recommendation",
                "",
                "- Review suspicious files and split formatting-only churn from semantic changes before commit.",
            ]
        )
    else:
        lines.extend(["", "## Recommendation", "", "- No suspicious graph JSON formatting churn detected."])

    return "\n".join(lines) + "\n"


def append_findings(
    lines: list[str],
    title: str,
    findings: list[dict[str, Any]],
    classifications: set[str],
    only_suspicious: bool = False,
    empty: str = "None.",
) -> None:
    lines.extend(["", f"## {title}", ""])
    selected = [
        finding
        for finding in findings
        if finding["classification"] in classifications
        and (not only_suspicious or finding["suspicious"])
    ]
    if not selected:
        lines.append(f"- {empty}")
        return
    for finding in selected:
        marker = "WARNING" if finding["suspicious"] else "OK"
        lines.append(
            f"- {marker} `{finding['path']}`: {finding['classification']} "
            f"({finding['changed_lines']}/{finding['total_lines']} changed lines)"
        )
        lines.append(f"  - {finding['summary']}")
        for detail in finding["details"]:
            lines.append(f"  - {detail}")


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def run_git(args: list[str], root: Path, error_context: str) -> str:
    process = subprocess.run(
        ["git", *args],
        cwd=root,
        capture_output=True,
        text=True,
    )
    if process.returncode != 0:
        detail = process.stderr.strip() or process.stdout.strip()
        raise ValueError(f"{error_context}: {detail}")
    return process.stdout


if __name__ == "__main__":
    raise SystemExit(main())
