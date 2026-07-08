#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
from collections import Counter
from dataclasses import replace
from datetime import date
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True
TOOL_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOL_DIR.parents[1]
ROUTER_LOG = REPO_ROOT / "reports" / "atlas-router" / "routing-log.jsonl"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.atlas_router.authority import route as route_request  # noqa: E402
from tools.atlas_router.classifier import classify  # noqa: E402
from tools.atlas_router.dispatcher import dispatch  # noqa: E402
from tools.atlas_router.models import (  # noqa: E402
    RouterConfigurationError,
    RoutingDecision,
    WorkOrderRequest,
)
from tools.atlas_router.parser import (  # noqa: E402
    parse_frontmatter,
    parse_text_request,
    parse_work_order_file,
    section_list_items,
    section_text,
)
from tools.atlas_router.scheduler import recommend  # noqa: E402


PROJECT_NAMES = {
    "the-last-sword-protocol": "The Last Sword Protocol",
    "atlasstudio": "AtlasStudio",
}
ATTENTION_ROUTER_STATUSES = {"blocked_ambiguous", "pending_approval"}


def main(argv: list[str] | None = None) -> int:
    args_list = list(sys.argv[1:] if argv is None else argv)
    if not args_list:
        return run_shell()

    parser = build_parser()
    args = parser.parse_args(args_list)
    try:
        if args.command == "today":
            return handle_today(args)
        if args.command == "status":
            return handle_status(args)
        if args.command == "doctor":
            return passthrough("tools/atlas_doctor/doctor.py", args.forwarded_args)
        if args.command == "route":
            return handle_route(args.forwarded_args)
        if args.command == "validate":
            return handle_validate()
        if args.command in {"planner", "plan"}:
            return passthrough("tools/atlas_planner/planner.py", args.forwarded_args)
        if args.command == "graph":
            return handle_graph(args.forwarded_args)
        if args.command == "work":
            return handle_work(args.forwarded_args)
        if args.command == "review":
            return handle_review(args)
        if args.command == "history":
            return handle_history(args)
        if args.command == "dispatch":
            return passthrough("tools/atlas_router/cli.py", ["wo", "dispatch", *args.forwarded_args])
    except (OSError, json.JSONDecodeError, ValueError, RouterConfigurationError) as error:
        print(f"atlas failed: {error}", file=sys.stderr)
        return 1
    parser.print_help(sys.stderr)
    return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="atlas",
        description="Unified AtlasStudio command line interface.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    today = subparsers.add_parser("today", help="Start-of-day production snapshot.")
    add_project_json(today)

    status = subparsers.add_parser("status", help="One-screen Studio Health snapshot.")
    add_project_json(status)

    for name in ("doctor", "planner", "plan", "graph", "route", "work", "dispatch"):
        sub = subparsers.add_parser(name)
        sub.add_argument("forwarded_args", nargs=argparse.REMAINDER)

    subparsers.add_parser("validate", help="Run graph validation and format guard.")

    review = subparsers.add_parser("review", help="Review today's progress or one work order.")
    review.add_argument("--work-order")
    review.add_argument("--since", default=date.today().isoformat())
    review.add_argument("--json", action="store_true")

    history = subparsers.add_parser("history", help="Show router, work-order, and decision history.")
    history.add_argument("--work-order")
    history.add_argument("--repository")
    history.add_argument("--since")
    history.add_argument("--router", action="store_true")
    history.add_argument("--json", action="store_true")
    return parser


def add_project_json(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--project", default="the-last-sword-protocol")
    parser.add_argument("--json", action="store_true")


def handle_today(args: argparse.Namespace) -> int:
    health, doctor_code, doctor_error = read_doctor_health(args.project)
    router_summary = summarize_router_log()
    repos = repo_statuses()
    recommendation = top_recommendation(args.project)

    payload = {
        "date": date.today().isoformat(),
        "repositories": repos,
        "studio_health": health_summary(health, doctor_code, doctor_error),
        "work_orders": (health or {}).get("work_orders", {}),
        "router": router_summary,
        "top_recommendation": recommendation,
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print_today(payload, args.project)

    attention = any(repo["state"] != "clean" for repo in repos)
    attention = attention or payload["studio_health"]["structural_errors"] > 0
    attention = attention or router_summary["pending_approval"] > 0
    attention = attention or router_summary["blocked_ambiguous"] > 0
    if doctor_error and health is None:
        return 1
    return 8 if attention else 0


def handle_status(args: argparse.Namespace) -> int:
    health, doctor_code, doctor_error = read_doctor_health(args.project)
    router_summary = summarize_router_log()
    payload = {
        "project": PROJECT_NAMES.get(args.project, args.project),
        "studio_health": health_summary(health, doctor_code, doctor_error),
        "work_orders": (health or {}).get("work_orders", {}),
        "router": {
            "pending_approval": router_summary["pending_approval"],
            "blocked_ambiguous": router_summary["blocked_ambiguous"],
        },
        "journey": current_journey(),
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print_status(payload)
    if doctor_error and health is None:
        return 1
    return 8 if payload["studio_health"]["structural_errors"] or router_summary["blocked_ambiguous"] else 0


def read_doctor_health(project: str) -> tuple[dict[str, Any] | None, int, str | None]:
    result = run_python("tools/atlas_doctor/doctor.py", ["--project", project, "--json"], capture=True)
    if result.stdout:
        try:
            return json.loads(result.stdout), result.returncode, result.stderr.strip() or None
        except json.JSONDecodeError:
            pass
    return None, result.returncode, result.stderr.strip() or result.stdout.strip() or "Doctor did not return JSON."


def health_summary(
    health: dict[str, Any] | None,
    doctor_code: int,
    doctor_error: str | None,
) -> dict[str, Any]:
    if health is None:
        return {
            "label": "Unavailable",
            "doctor_exit_code": doctor_code,
            "structural_errors": 1,
            "message": doctor_error or "Doctor failed.",
        }
    graph_integrity = health.get("graph_integrity", {})
    structural_errors = int(graph_integrity.get("structural_error_count", 0))
    return {
        "label": "Healthy" if structural_errors == 0 else "Needs Attention",
        "doctor_exit_code": doctor_code,
        "structural_errors": structural_errors,
        "validation_errors": int(graph_integrity.get("validation_error_count", 0)),
        "missing_sources": int(graph_integrity.get("missing_source_count", 0)),
    }


def print_today(payload: dict[str, Any], project: str) -> None:
    print(f"AtlasStudio - Today ({payload['date']})")
    print()
    print("Repositories:")
    for repo in payload["repositories"]:
        print(f"  {repo['name']:<28} {repo['state']}")
    print()

    health = payload["studio_health"]
    work_orders = health_work_orders(payload)
    status_text = ", ".join(f"{status}: {count}" for status, count in work_orders["status_counts"].items())
    print(
        f"Studio Health: {health['label']} "
        f"({health['structural_errors']} structural errors, "
        f"{work_orders['count']} work orders"
        f"{': ' + status_text if status_text else ''})"
    )
    if "message" in health:
        print(f"  {health['message']}")
    print()

    router = payload["router"]
    print(f"Router: {router['pending_approval']} pending_approval, {router['blocked_ambiguous']} blocked_ambiguous")
    for item in router["attention_items"][:5]:
        print(f"  - {item['work_order_id']} ({item['classification']}, {item['routing_status']})")
    print()

    rec = payload["top_recommendation"]
    if rec:
        print(
            f"Top recommendation: \"{rec['title']}\" "
            f"({rec['priority']}, {rec['total_score']}/100)"
        )
    else:
        print("Top recommendation: none")
    print("Run `atlas planner` for full detail, or `atlas work review` on items already in flight.")


def print_status(payload: dict[str, Any]) -> None:
    health = payload["studio_health"]
    work_orders = payload.get("work_orders") or {}
    counts = work_orders.get("status_counts", {})
    status_text = ", ".join(f"{status}: {count}" for status, count in counts.items()) or "none"
    print(f"Project: {payload['project']}")
    print(f"Studio Health: {health['label']}")
    if "message" in health:
        print(f"Doctor: {health['message']}")
    print(f"Work Orders: {work_orders.get('count', 0)} ({status_text})")
    router = payload["router"]
    print(f"Router: {router['pending_approval']} pending_approval, {router['blocked_ambiguous']} blocked_ambiguous")
    print(f"Journey: {payload['journey']}")


def health_work_orders(payload: dict[str, Any]) -> dict[str, Any]:
    work_orders = payload.get("work_orders") or {}
    if work_orders:
        return work_orders
    status_counts = work_order_status_counts()
    return {"count": sum(status_counts.values()), "status_counts": dict(status_counts)}


def summarize_router_log() -> dict[str, Any]:
    latest: dict[str, dict[str, Any]] = {}
    for record in read_router_records():
        work_order_id = str(record.get("work_order_id", ""))
        if work_order_id:
            latest[work_order_id] = record
    statuses = Counter(str(record.get("routing_status", "unknown")) for record in latest.values())
    attention = [
        {
            "work_order_id": record.get("work_order_id"),
            "classification": record.get("classification"),
            "routing_status": record.get("routing_status"),
        }
        for record in latest.values()
        if record.get("routing_status") in ATTENTION_ROUTER_STATUSES
    ]
    return {
        "records": len(latest),
        "status_counts": dict(sorted(statuses.items())),
        "pending_approval": statuses.get("pending_approval", 0),
        "blocked_ambiguous": statuses.get("blocked_ambiguous", 0),
        "attention_items": attention,
    }


def read_router_records() -> list[dict[str, Any]]:
    if not ROUTER_LOG.exists():
        return []
    records: list[dict[str, Any]] = []
    for line in ROUTER_LOG.read_text("utf-8").splitlines():
        if not line.strip():
            continue
        records.append(json.loads(line))
    return records


def repo_statuses() -> list[dict[str, str]]:
    repos = [
        ("TheLastSwordProtocol-Atlas", REPO_ROOT.parent / "TheLastSwordProtocol-Atlas"),
        ("AtlasStudio", REPO_ROOT),
        ("TheLastSwordProtocol-Game", REPO_ROOT.parent / "TheLastSwordProtocol-Game"),
    ]
    statuses: list[dict[str, str]] = []
    for name, path in repos:
        if not path.exists():
            statuses.append({"name": name, "state": "missing"})
            continue
        result = subprocess.run(
            ["git", "-C", str(path), "status", "--porcelain"],
            text=True,
            capture_output=True,
            check=False,
            env=child_env(),
        )
        if result.returncode:
            state = "unavailable"
        elif result.stdout.strip():
            state = "dirty"
        else:
            state = "clean"
        statuses.append({"name": name, "state": state})
    return statuses


def top_recommendation(project: str) -> dict[str, Any] | None:
    result = run_python("tools/atlas_planner/planner.py", ["--project", project, "--json"], capture=True)
    if result.returncode not in {0, 1} or not result.stdout:
        return None
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None
    recommendations = data.get("recommendations") or []
    if not recommendations:
        return None
    rec = recommendations[0]
    return {
        "title": rec.get("title"),
        "priority": rec.get("priority"),
        "total_score": rec.get("total_score"),
        "recommended_agents": rec.get("recommended_agents", []),
    }


def current_journey() -> str:
    status_path = REPO_ROOT / "studio" / "STATUS.md"
    if not status_path.exists():
        return "unknown"
    text = status_path.read_text("utf-8")
    for line in text.splitlines():
        if "Journey:" in line:
            return line.split("Journey:", 1)[1].strip(" *`")
    return "I"


def handle_route(forwarded_args: list[str]) -> int:
    route_parser = argparse.ArgumentParser(prog="atlas route")
    route_parser.add_argument("forwarded_args", nargs=argparse.REMAINDER)
    parsed = route_parser.parse_args(forwarded_args)
    args = list(parsed.forwarded_args)
    if not args:
        route_parser.print_help(sys.stderr)
        return 2
    mode = "preview"
    if args[0] in {"classify", "preview", "explain", "dispatch"}:
        mode = args.pop(0)
    if mode == "dispatch":
        return passthrough("tools/atlas_router/cli.py", ["wo", "dispatch", *args])

    json_output = False
    if "--json" in args:
        json_output = True
        args.remove("--json")
    if not args:
        print("atlas route requires a request.", file=sys.stderr)
        return 2
    request = load_request(" ".join(args))
    if mode == "explain":
        return passthrough("tools/atlas_router/cli.py", ["wo", "explain", *args, *(["--json"] if json_output else [])])

    classification = classify(request)
    decision = route_request(request, classification)
    recommendation = None
    outcome = None
    if mode == "preview" and decision.routing_status not in {
        "blocked_ambiguous",
        "rejected_authority_violation",
    }:
        recommendation = recommend(request, classification, decision)
        decision = replace(decision, scheduler_recommendation=recommendation)
        outcome = dispatch(request, decision, recommendation, dry_run=True)

    if json_output:
        payload: dict[str, Any] = {
            "classification_result": classification.to_dict(),
            "routing_decision": decision.to_full_dict(),
        }
        if recommendation is not None:
            payload["scheduler_recommendation"] = recommendation.to_dict()
        if outcome is not None:
            payload["dispatch"] = outcome.to_dict()
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print_route_result(decision, outcome)
    return route_exit_code(decision, dispatch_attempted=False)


def load_request(value: str) -> WorkOrderRequest:
    path = Path(value)
    if path.exists():
        return parse_work_order_file(path)
    return parse_text_request(value)


def print_route_result(decision: RoutingDecision, outcome: Any) -> None:
    print(f"Classification: {decision.classification}")
    print(f"Target repository: {decision.target_repository}")
    print(f"Routing status: {decision.routing_status}")
    print("Signals matched:")
    for signal in decision.signals_matched:
        print(f"  - {signal}")
    if decision.scheduler_recommendation is not None:
        rec = decision.scheduler_recommendation
        print(f"Scheduler recommendation (advisory={rec.advisory}): {rec.primary_agent} (score {rec.score})")
    if outcome is not None:
        print(f"Action: {outcome.action}")
        if outcome.path_or_url:
            print(f"Target: {outcome.path_or_url}")
    if decision.warnings:
        print("Warnings:")
        for warning in decision.warnings:
            print(f"  - {warning}")
    print(f"Rationale: {decision.rationale}")


def route_exit_code(decision: RoutingDecision, *, dispatch_attempted: bool) -> int:
    if decision.routing_status == "blocked_ambiguous":
        return 4
    if decision.routing_status == "rejected_authority_violation":
        return 5
    if dispatch_attempted and decision.routing_status == "pending_approval":
        return 7
    return 0


def handle_validate() -> int:
    graph = passthrough("tools/atlas_graph/validate_graph.py", [])
    if graph:
        return graph
    return passthrough("tools/atlas_format/format_guard.py", ["--check"])


def handle_graph(forwarded_args: list[str]) -> int:
    if forwarded_args and forwarded_args[0] == "validate":
        return passthrough("tools/atlas_graph/validate_graph.py", forwarded_args[1:])
    return passthrough("tools/atlas_graph/query_graph.py", forwarded_args)


def handle_work(forwarded_args: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="atlas work")
    subparsers = parser.add_subparsers(dest="work_command", required=True)

    create = subparsers.add_parser("create")
    create.add_argument("forwarded_args", nargs=argparse.REMAINDER)

    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--status", action="append", default=[])
    list_parser.add_argument("--project")
    list_parser.add_argument("--json", action="store_true")

    show = subparsers.add_parser("show")
    show.add_argument("work_order_id")
    show.add_argument("--json", action="store_true")

    review = subparsers.add_parser("review")
    review.add_argument("work_order_id")
    review.add_argument("--json", action="store_true")

    args = parser.parse_args(forwarded_args)
    if args.work_command == "create":
        return passthrough("tools/atlas_router/cli.py", ["wo", "create", *args.forwarded_args])
    if args.work_command == "list":
        return work_list(args)
    if args.work_command == "show":
        return work_show(args)
    if args.work_command == "review":
        return work_review(args)
    return 2


def work_list(args: argparse.Namespace) -> int:
    items = []
    for path in work_order_paths():
        work_order = read_work_order(path)
        if args.status and work_order["frontmatter"].get("status") not in set(args.status):
            continue
        if args.project and work_order["frontmatter"].get("project") != args.project:
            continue
        items.append(work_order)
    if args.json:
        print(json.dumps(items, indent=2, sort_keys=True))
    else:
        for item in items:
            fm = item["frontmatter"]
            print(
                f"{fm.get('work_order_id', item['id']):<8} "
                f"{fm.get('status', 'unknown'):<14} "
                f"{fm.get('recommended_agent', ''):<14} "
                f"{fm.get('title', item['title'])}"
            )
    return 0 if items else 9


def work_show(args: argparse.Namespace) -> int:
    path = find_work_order(args.work_order_id)
    if path is None:
        print(f"Work order not found: {args.work_order_id}", file=sys.stderr)
        return 1
    item = read_work_order(path)
    latest = latest_router_record(args.work_order_id)
    graph = graph_node(args.work_order_id)
    payload = {"work_order": item, "latest_router_record": latest, "graph_node": graph}
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        fm = item["frontmatter"]
        print(f"{fm.get('work_order_id', item['id'])} - {fm.get('title', item['title'])}")
        print(f"Path: {item['path']}")
        print(f"Status: {fm.get('status', 'unknown')}")
        print(f"Project: {fm.get('project', 'unknown')}")
        print(f"Recommended agent: {fm.get('recommended_agent', '')}")
        if item["purpose"]:
            print()
            print("Purpose:")
            print(item["purpose"])
        if latest:
            print()
            print(f"Latest router: {latest.get('classification')} -> {latest.get('target_repository')} ({latest.get('routing_status')})")
        if graph:
            print(f"Graph: {graph.get('id')} ({graph.get('status')})")
    return 0


def work_review(args: argparse.Namespace) -> int:
    path = find_work_order(args.work_order_id)
    if path is None:
        print(f"Work order not found: {args.work_order_id}", file=sys.stderr)
        return 1
    item = read_work_order(path)
    checks = build_work_review_checks(path, item)
    if args.json:
        print(json.dumps({"work_order": item["id"], "checks": checks}, indent=2, sort_keys=True))
    else:
        for check in checks:
            print(f"{check['name']:<42} {check['state']:<20} {check['detail']}")
        automated = [check for check in checks if check["automated"]]
        passing = [check for check in automated if check["state"] in {"yes", "clean", "n/a"}]
        human = [check for check in checks if not check["automated"]]
        print()
        print(f"{len(passing)} of {len(automated)} automated checks passing. {len(human)} requires human judgment.")
    return 0 if all(check["state"] in {"yes", "clean", "n/a", "needs human judgment"} for check in checks) else 8


def build_work_review_checks(path: Path, item: dict[str, Any]) -> list[dict[str, Any]]:
    text = path.read_text("utf-8")
    allowed_changes = section_list_items(text, "Allowed Changes")
    format_result = run_python("tools/atlas_format/format_guard.py", ["--check"], capture=True)
    sibling_states = [
        repo for repo in repo_statuses()
        if repo["name"] in {"TheLastSwordProtocol-Atlas", "TheLastSwordProtocol-Game"}
    ]
    siblings_clean = all(repo["state"] == "clean" for repo in sibling_states)
    sibling_detail = ", ".join(f"{repo['name']}={repo['state']}" for repo in sibling_states)
    if not (item["frontmatter"].get("engine_specific") or item["frontmatter"].get("player_facing")):
        sibling_state = "n/a"
        sibling_detail = "work order metadata does not require sibling-repository inspection"
    else:
        sibling_state = "yes" if siblings_clean else "attention"
    return [
        check(
            "Deliverables match Allowed Changes",
            "yes" if allowed_changes else "attention",
            f"{len(allowed_changes)} allowed path entries declared" if allowed_changes else "no Allowed Changes entries found",
        ),
        check(
            "Formatting preserved note present",
            "yes" if "Formatting:" in text else "attention",
            "submission note found" if "Formatting:" in text else "no submission note found",
        ),
        check(
            "Sources cited by path, not paraphrased",
            "needs human judgment",
            "review against source files required",
            automated=False,
        ),
        check(
            "format_guard.py --check",
            "clean" if format_result.returncode == 0 else "attention",
            first_output_line(format_result) or f"exit {format_result.returncode}",
        ),
        check("Sibling repositories untouched", sibling_state, sibling_detail),
    ]


def check(name: str, state: str, detail: str, *, automated: bool = True) -> dict[str, Any]:
    return {"name": name, "state": state, "detail": detail, "automated": automated}


def handle_review(args: argparse.Namespace) -> int:
    if args.work_order:
        review_args = argparse.Namespace(work_order_id=args.work_order, json=args.json)
        return work_review(review_args)

    changed = changed_work_orders_since(args.since)
    payload = {
        "since": args.since,
        "changed_work_orders": [read_work_order(path) for path in changed],
        "status": status_payload_for_review(),
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"Work orders updated since {args.since}:")
        if not changed:
            print("  none")
        for item in payload["changed_work_orders"]:
            fm = item["frontmatter"]
            print(f"  {fm.get('work_order_id', item['id']):<8} {fm.get('status', 'unknown'):<14} \"{fm.get('title', item['title'])}\"")
        print()
        print(f"Studio Health: {payload['status']['studio_health']['label']}")
        router = payload["status"]["router"]
        print(f"Router: {router['pending_approval']} pending_approval, {router['blocked_ambiguous']} blocked_ambiguous")
    return 0 if changed else 9


def changed_work_orders_since(since: str) -> list[Path]:
    result = subprocess.run(
        ["git", "log", "--name-only", "--pretty=format:", "--since", since, "--", "work-orders/"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
        env=child_env(),
    )
    changed: list[Path] = []
    for line in result.stdout.splitlines():
        if line.startswith("work-orders/") and line.endswith(".md"):
            path = REPO_ROOT / line
            if path.exists() and path not in changed:
                changed.append(path)
    return sorted(changed)


def status_payload_for_review() -> dict[str, Any]:
    health, doctor_code, doctor_error = read_doctor_health("the-last-sword-protocol")
    return {
        "studio_health": health_summary(health, doctor_code, doctor_error),
        "router": summarize_router_log(),
    }


def handle_history(args: argparse.Namespace) -> int:
    router_records = filter_router_records(args)
    work_logs = [] if args.router else git_work_order_history(args.work_order, args.since)
    decisions = [] if args.router else decision_records(args.work_order)
    payload = {
        "router_records": router_records,
        "work_order_commits": work_logs,
        "decision_records": decisions,
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        for record in router_records:
            print(
                f"{record.get('created', '')}  {record.get('routing_status', ''):<18} "
                f"{record.get('classification', '')} -> {record.get('target_repository', '')} "
                f"{record.get('work_order_id', '')}"
            )
        for commit in work_logs:
            print(f"{commit['date']}  commit {commit['hash']}  {commit['subject']}")
        for decision in decisions:
            print(f"{decision['path']}  decision record")
        if not router_records and not work_logs and not decisions:
            print("No history matched.")
    return 0 if router_records or work_logs or decisions else 9


def filter_router_records(args: argparse.Namespace) -> list[dict[str, Any]]:
    records = read_router_records()
    filtered: list[dict[str, Any]] = []
    for record in records:
        if args.work_order and record.get("work_order_id") != args.work_order:
            continue
        if args.repository and record.get("target_repository") != args.repository:
            continue
        if args.since and str(record.get("created", "")) < args.since:
            continue
        filtered.append(record)
    return filtered


def git_work_order_history(work_order_id: str | None, since: str | None) -> list[dict[str, str]]:
    command = ["git", "log", "--date=short", "--pretty=format:%h%x09%ad%x09%s"]
    if since:
        command.extend(["--since", since])
    command.append("--")
    if work_order_id:
        path = find_work_order(work_order_id)
        if path is None:
            return []
        command.append(str(path.relative_to(REPO_ROOT)))
    else:
        command.append("work-orders/")
    result = subprocess.run(command, cwd=REPO_ROOT, text=True, capture_output=True, check=False, env=child_env())
    commits = []
    for line in result.stdout.splitlines():
        parts = line.split("\t", 2)
        if len(parts) == 3:
            commits.append({"hash": parts[0], "date": parts[1], "subject": parts[2]})
    return commits


def decision_records(work_order_id: str | None) -> list[dict[str, str]]:
    decisions_dir = REPO_ROOT / "studio" / "governance" / "decisions"
    if not decisions_dir.exists():
        return []
    records: list[dict[str, str]] = []
    for path in sorted(decisions_dir.glob("*.md")):
        rel = str(path.relative_to(REPO_ROOT))
        if work_order_id is None or work_order_id in path.read_text("utf-8"):
            records.append({"path": rel})
    return records


def work_order_paths() -> list[Path]:
    return sorted((REPO_ROOT / "work-orders").glob("WO-*.md"))


def find_work_order(work_order_id: str) -> Path | None:
    candidates = sorted((REPO_ROOT / "work-orders").glob(f"{work_order_id}-*.md"))
    if candidates:
        return candidates[0]
    direct = REPO_ROOT / "work-orders" / f"{work_order_id}.md"
    return direct if direct.exists() else None


def read_work_order(path: Path) -> dict[str, Any]:
    text = path.read_text("utf-8")
    frontmatter = parse_frontmatter(text)
    return {
        "id": str(frontmatter.get("work_order_id", path.stem.split("-", 2)[0])),
        "title": str(frontmatter.get("title", path.stem)),
        "path": str(path.relative_to(REPO_ROOT)),
        "frontmatter": frontmatter,
        "purpose": section_text(text, "Purpose"),
        "allowed_changes": section_list_items(text, "Allowed Changes"),
    }


def work_order_status_counts() -> Counter[str]:
    counts: Counter[str] = Counter()
    for path in work_order_paths():
        status = read_work_order(path)["frontmatter"].get("status", "unknown")
        counts[str(status)] += 1
    return counts


def latest_router_record(work_order_id: str) -> dict[str, Any] | None:
    latest = None
    for record in read_router_records():
        if record.get("work_order_id") == work_order_id:
            latest = record
    return latest


def graph_node(work_order_id: str) -> dict[str, Any] | None:
    node_id = "work_order." + work_order_id.lower().replace("-", "_")
    result = run_python("tools/atlas_graph/query_graph.py", ["get", node_id, "--json"], capture=True)
    if result.returncode != 0 or not result.stdout:
        return None
    try:
        return json.loads(result.stdout).get("node")
    except json.JSONDecodeError:
        return None


def first_output_line(result: subprocess.CompletedProcess[str]) -> str:
    text = (result.stdout or result.stderr or "").strip()
    return text.splitlines()[0] if text else ""


def passthrough(script: str, args: list[str]) -> int:
    return run_python(script, args, capture=False).returncode


def run_python(script: str, args: list[str], *, capture: bool) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(REPO_ROOT / script), *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=capture,
        check=False,
        env=child_env(),
    )


def child_env() -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def run_shell() -> int:
    print("AtlasStudio v1.0")
    print()
    handle_status(argparse.Namespace(project="the-last-sword-protocol", json=False))
    print()
    while True:
        try:
            line = input("atlas> ")
        except EOFError:
            print()
            return 0
        except KeyboardInterrupt:
            print()
            continue
        line = line.strip()
        if not line:
            continue
        if line in {"exit", "quit"}:
            return 0
        if line in {"help", "?"}:
            print_shell_help()
            continue
        if line == "atlas":
            handle_status(argparse.Namespace(project="the-last-sword-protocol", json=False))
            continue
        if line.startswith("atlas "):
            line = line[6:]
        try:
            command_args = shlex.split(line)
        except ValueError as error:
            print(f"Could not parse command: {error}")
            continue
        code = main(command_args)
        if code:
            print(f"(exit {code})")


def print_shell_help() -> None:
    print("Situational awareness   today, status, doctor, history")
    print("Routing and work        route, work, dispatch")
    print("Quality gates           review, validate")
    print("Knowledge and graph     graph, planner")
    print()
    print("Type `exit` to leave the shell.")


if __name__ == "__main__":
    raise SystemExit(main())
