#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import replace
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    __package__ = "tools.atlas_router"

from . import audit
from .authority import route
from .classifier import classify
from .dispatcher import dispatch
from .models import (
    GithubUnavailableError,
    NetworkError,
    RouterConfigurationError,
    RoutingDecision,
    WorkOrderRequest,
)
from .parser import parse_request_from_args, parse_text_request, parse_work_order_file
from .scheduler import recommend


sys.dont_write_bytecode = True
TOOL_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOL_DIR.parents[1]


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "wo":
            return handle_wo(args)
        if args.command in {"classify", "preview", "explain"}:
            args.wo_command = args.command
            return handle_wo(args)
        if args.command == "doctor":
            return passthrough("tools/atlas_doctor/doctor.py", args.forwarded_args)
        if args.command == "plan":
            return passthrough("tools/atlas_planner/planner.py", args.forwarded_args)
        if args.command == "graph":
            return passthrough("tools/atlas_graph/query_graph.py", args.forwarded_args)
        if args.command == "validate":
            return validate()
        if args.command == "scheduler":
            return handle_scheduler(args)
        if args.command in {"status", "import", "sync"}:
            print(
                f"atlas {args.command} is not yet implemented. See bridges/atlas/import-architecture.md for its design.",
                file=sys.stderr,
            )
            return 3
    except (OSError, json.JSONDecodeError, ValueError, RouterConfigurationError) as error:
        print(f"Work Order Router failed: {error}", file=sys.stderr)
        return 1
    except NetworkError:
        print(
            "Dispatch failed: network error contacting GitHub. The routing decision was recorded; no issue was created. Retry 'atlas wo dispatch' once connectivity is restored.",
            file=sys.stderr,
        )
        return 6
    except GithubUnavailableError as error:
        print(f"Dispatch failed: GitHub unavailable. {error}", file=sys.stderr)
        return 6
    parser.print_help(sys.stderr)
    return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AtlasStudio CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    wo = subparsers.add_parser("wo", help="Work order router commands")
    wo_subparsers = wo.add_subparsers(dest="wo_command", required=True)
    for name in ("classify", "preview", "dispatch", "explain"):
        sub = wo_subparsers.add_parser(name)
        sub.add_argument("request", help="Work order path, work order id, or inline request text")
        sub.add_argument("--json", action="store_true")
        if name in {"preview", "dispatch"}:
            sub.add_argument("--status-file")
        if name in {"classify", "preview", "dispatch"}:
            sub.add_argument("--approved-by")
            sub.add_argument("--approved-at")
        if name == "dispatch":
            sub.add_argument("--force-reissue", action="store_true")
            sub.add_argument("--reason")

    create = wo_subparsers.add_parser("create")
    create.add_argument("--title", required=True)
    create.add_argument("--project", required=True)
    create.add_argument("--purpose", required=True)
    create.add_argument("--scope-in", action="append", default=[])
    create.add_argument("--scope-out", action="append", default=[])
    create.add_argument("--capability", action="append", default=[])
    create.add_argument("--preferred-capability", action="append", default=[])
    create.add_argument("--risk-level", choices=["low", "medium", "high"], default="medium")
    player_group = create.add_mutually_exclusive_group()
    player_group.add_argument("--player-facing", dest="player_facing", action="store_true")
    player_group.add_argument("--no-player-facing", dest="player_facing", action="store_false")
    engine_group = create.add_mutually_exclusive_group()
    engine_group.add_argument("--engine-specific", dest="engine_specific", action="store_true")
    engine_group.add_argument("--no-engine-specific", dest="engine_specific", action="store_false")
    create.set_defaults(player_facing=False, engine_specific=False)
    create.add_argument("--approved-by")
    create.add_argument("--approved-at")
    create.add_argument("--json", action="store_true")
    create.add_argument("--dry-run", action="store_true")

    for name in ("classify", "preview", "explain"):
        sub = subparsers.add_parser(name, help=f"Alias for wo {name}")
        sub.add_argument("request", help="Work order path, work order id, or inline request text")
        sub.add_argument("--json", action="store_true")
        if name == "preview":
            sub.add_argument("--status-file")

    for name in ("doctor", "plan", "graph", "status", "import", "sync"):
        sub = subparsers.add_parser(name)
        sub.add_argument("forwarded_args", nargs=argparse.REMAINDER)
    subparsers.add_parser("validate")

    scheduler = subparsers.add_parser("scheduler")
    scheduler_subparsers = scheduler.add_subparsers(dest="scheduler_command", required=True)
    rec = scheduler_subparsers.add_parser("recommend")
    rec.add_argument("request")
    rec.add_argument("--status-file")
    rec.add_argument("--json", action="store_true")
    return parser


def handle_wo(args: argparse.Namespace) -> int:
    if args.wo_command == "explain":
        return explain(args)
    request = load_request(args.request) if args.wo_command != "create" else parse_request_from_args(args)
    if args.wo_command in {"classify", "preview", "dispatch"}:
        request.approved_by = getattr(args, "approved_by", None)
        request.approved_at = getattr(args, "approved_at", None)
    classification = classify(request)
    decision = route(request, classification)
    recommendation = None
    outcome = None
    if args.wo_command in {"preview", "dispatch"} and decision.routing_status not in {
        "blocked_ambiguous",
        "rejected_authority_violation",
    }:
        recommendation = recommend(
            request,
            classification,
            decision,
            Path(args.status_file) if getattr(args, "status_file", None) else None,
        )
        decision = replace(decision, scheduler_recommendation=recommendation)
    if args.wo_command == "preview":
        outcome = dispatch(request, decision, recommendation, dry_run=True)
    elif args.wo_command == "dispatch":
        if args.force_reissue and not args.reason:
            print("--reason is required with --force-reissue", file=sys.stderr)
            return 2
        outcome = dispatch(request, decision, recommendation, dry_run=False, force_reissue=args.force_reissue)
    elif args.wo_command == "create":
        if decision.target_repository == "AtlasStudio" and not args.dry_run:
            if decision.routing_status == "pending_approval":
                outcome = dispatch(request, decision, recommendation, dry_run=True)
            elif decision.routing_status == "routed":
                outcome = dispatch(request, decision, recommendation, dry_run=False)
    audit.append_routing_record(decision, outcome)
    print_result(args, classification.to_dict(), decision, outcome)
    return exit_code_for(decision, dispatch_attempted=args.wo_command == "dispatch")


def explain(args: argparse.Namespace) -> int:
    record = audit.read_routing_record(args.request)
    if record is not None:
        if args.json:
            print(json.dumps(record, indent=2, sort_keys=True))
        else:
            print(f"{record.get('work_order_id')} - {record.get('title', '')}")
            print(f"Classification: {record.get('classification')}")
            print(f"Routing status: {record.get('routing_status')}")
            print(f"Target repository: {record.get('target_repository')}")
            print(f"Rationale: {record.get('rationale')}")
        return 0

    if args.request.startswith(("WO-", "WP-", "REQ-")):
        print(f"No routing record found for {args.request}", file=sys.stderr)
        return 1

    request = parse_text_request(args.request)
    classification = classify(request)
    decision = route(request, classification)
    if args.json:
        print(json.dumps(decision.to_full_dict(), indent=2, sort_keys=True))
    else:
        print(f"Classification: {decision.classification}")
        print(f"Target repository: {decision.target_repository}")
        print(f"Routing status: {decision.routing_status}")
        print(f"Rationale: {decision.rationale}")
    return exit_code_for(decision, dispatch_attempted=False)


def handle_scheduler(args: argparse.Namespace) -> int:
    if args.scheduler_command != "recommend":
        return 2
    request = load_request(args.request)
    classification = classify(request)
    decision = route(request, classification)
    if decision.routing_status in {"blocked_ambiguous", "rejected_authority_violation"}:
        print(decision.rationale, file=sys.stderr)
        return exit_code_for(decision, dispatch_attempted=False)
    recommendation = recommend(
        request,
        classification,
        decision,
        Path(args.status_file) if args.status_file else None,
    )
    if args.json:
        print(json.dumps(recommendation.to_dict(), indent=2, sort_keys=True))
    else:
        print_recommendation(recommendation)
    return 0


def load_request(value: str) -> WorkOrderRequest:
    if value == "--stdin":
        return WorkOrderRequest.from_dict(json.loads(sys.stdin.read()))
    path = Path(value)
    if path.exists():
        return parse_work_order_file(path)
    return parse_text_request(value)


def print_result(
    args: argparse.Namespace,
    classification: dict[str, Any],
    decision: RoutingDecision,
    outcome: Any,
) -> None:
    if getattr(args, "json", False):
        payload: dict[str, Any] = {"classification_result": classification, "routing_decision": decision.to_full_dict()}
        if outcome is not None:
            payload["dispatch"] = outcome.to_dict()
        print(json.dumps(payload, indent=2, sort_keys=True))
        return
    print(f"Classification: {decision.classification}")
    print(f"Target repository: {decision.target_repository}")
    print(f"Routing status: {decision.routing_status}")
    print("Signals matched:")
    for signal in decision.signals_matched:
        print(f"  - {signal}")
    if decision.scheduler_recommendation is not None:
        rec = decision.scheduler_recommendation
        print(
            f"Scheduler recommendation (advisory={rec.advisory}): {rec.primary_agent} (score {rec.score})"
        )
    if outcome is not None:
        print(f"Action: {outcome.action}")
        if outcome.path_or_url:
            print(f"Target: {outcome.path_or_url}")
    if decision.warnings:
        print("Warnings:")
        for warning in decision.warnings:
            print(f"  - {warning}")
    print(f"Rationale: {decision.rationale}")


def print_recommendation(recommendation: Any) -> None:
    print(
        f"Scheduler recommendation (advisory={recommendation.advisory}): {recommendation.primary_agent} (score {recommendation.score})"
    )
    for name, score in recommendation.components.items():
        print(f"  {name}: {score}")
    for fallback in recommendation.fallbacks:
        print(f"Fallback: {fallback['agent']} (score {fallback['score']})")


def exit_code_for(decision: RoutingDecision, *, dispatch_attempted: bool) -> int:
    if decision.routing_status == "blocked_ambiguous":
        return 4
    if decision.routing_status == "rejected_authority_violation":
        return 5
    if dispatch_attempted and decision.routing_status == "pending_approval":
        return 7
    return 0


def passthrough(script: str, forwarded_args: list[str]) -> int:
    result = subprocess.run([sys.executable, str(REPO_ROOT / script), *forwarded_args], check=False)
    return result.returncode


def validate() -> int:
    first = passthrough("tools/atlas_graph/validate_graph.py", [])
    if first:
        return first
    return passthrough("tools/atlas_format/format_guard.py", ["--check"])


if __name__ == "__main__":
    raise SystemExit(main())
