from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

from .models import WorkOrderRequest, listify


def parse_work_order_file(path: Path) -> WorkOrderRequest:
    text = path.read_text("utf-8")
    frontmatter = parse_frontmatter(text)
    work_order_id = str(frontmatter.get("work_order_id", path.stem.split("-", 2)[0]))
    title = str(frontmatter.get("title", path.stem))
    return WorkOrderRequest(
        source_path=str(path),
        work_order_id=work_order_id,
        title=title,
        project=str(frontmatter.get("project", "atlasstudio")),
        purpose=section_text(text, "Purpose") or title,
        scope_in=section_list_items(text, "In Scope"),
        scope_out=section_list_items(text, "Out of Scope"),
        required_capabilities=listify(frontmatter.get("required_capabilities", [])),
        preferred_capabilities=listify(frontmatter.get("preferred_capabilities", [])),
        risk_level=str(frontmatter.get("risk_level", "medium")),
        player_facing=parse_bool(frontmatter.get("player_facing", False)),
        engine_specific=parse_bool(frontmatter.get("engine_specific", False)),
        claimed_target_repository=frontmatter.get("target_repository"),
        approved_by=frontmatter.get("approved_by"),
        approved_at=frontmatter.get("approved_at"),
        agent_role=frontmatter.get("agent_role"),
        recommended_agent=frontmatter.get("recommended_agent"),
        task_class=frontmatter.get("task_class"),
    )


def parse_request_from_args(args: argparse.Namespace) -> WorkOrderRequest:
    text = getattr(args, "request_text", None) or getattr(args, "title", "")
    return WorkOrderRequest(
        source_path=None,
        work_order_id=getattr(args, "work_order_id", None),
        title=getattr(args, "title", None) or text,
        project=getattr(args, "project", "atlasstudio"),
        purpose=getattr(args, "purpose", None) or text,
        scope_in=list(getattr(args, "scope_in", []) or []),
        scope_out=list(getattr(args, "scope_out", []) or []),
        required_capabilities=list(getattr(args, "capability", []) or []),
        preferred_capabilities=list(getattr(args, "preferred_capability", []) or []),
        risk_level=getattr(args, "risk_level", "medium"),
        player_facing=bool(getattr(args, "player_facing", False)),
        engine_specific=bool(getattr(args, "engine_specific", False)),
        claimed_target_repository=getattr(args, "target_repository", None),
        approved_by=getattr(args, "approved_by", None),
        approved_at=getattr(args, "approved_at", None),
        agent_role=getattr(args, "agent_role", None),
        task_class=getattr(args, "task_class", None),
    )


def parse_text_request(text: str) -> WorkOrderRequest:
    return WorkOrderRequest(
        source_path=None,
        work_order_id=synthetic_work_order_id(text),
        title=text,
        project="atlasstudio",
        purpose=text,
    )


def synthetic_work_order_id(text: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", text.strip()).strip("-").upper()
    return f"REQ-{slug[:32] or 'UNTITLED'}"


def parse_frontmatter(text: str) -> dict[str, Any]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    data: dict[str, Any] = {}
    index = 1
    while index < len(lines):
        line = lines[index]
        if line.strip() == "---":
            break
        if ":" not in line:
            index += 1
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value:
            data[key] = parse_scalar(value)
            index += 1
            continue
        items: list[str] = []
        lookahead = index + 1
        while lookahead < len(lines):
            candidate = lines[lookahead]
            if candidate.strip() == "---":
                break
            if re.match(r"^[A-Za-z0-9_-]+:\s*", candidate):
                break
            match = re.match(r"^\s*-\s+(.+)$", candidate)
            if match:
                items.append(str(parse_scalar(match.group(1).strip())))
            lookahead += 1
        data[key] = items if items else ""
        index = lookahead
    return data


def parse_scalar(value: str) -> Any:
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    return value.strip('"').strip("'")


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).lower() == "true"


def section_text(text: str, heading: str) -> str:
    marker = f"## {heading}"
    lines = text.splitlines()
    try:
        start = lines.index(marker) + 1
    except ValueError:
        return ""
    collected: list[str] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        if line.strip():
            collected.append(line.strip())
    return " ".join(collected)


def section_list_items(text: str, heading: str) -> list[str]:
    markers = [f"### {heading}", f"## {heading}"]
    lines = text.splitlines()
    start = None
    for marker in markers:
        try:
            start = lines.index(marker) + 1
            break
        except ValueError:
            continue
    if start is None:
        return []
    items: list[str] = []
    for line in lines[start:]:
        if line.startswith("## ") or line.startswith("### "):
            break
        match = re.match(r"^\s*-\s+(.+)$", line)
        if match:
            items.append(match.group(1).strip())
    return items
