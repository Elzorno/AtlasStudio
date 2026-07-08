from __future__ import annotations

import contextlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path

from tools.atlas_router import audit
from tools.atlas_router.authority import route
from tools.atlas_router.classifier import classify
from tools.atlas_router.cli import main
from tools.atlas_router.models import DispatchOutcome, WorkOrderRequest
from tools.atlas_router.parser import parse_frontmatter, parse_work_order_file


class ParserAuditCliTests(unittest.TestCase):
    def test_parse_frontmatter_supports_yaml_lists(self) -> None:
        text = """---
work_order_id: WO-9999
required_capabilities:
  - architecture-review
  - graph-analysis
player_facing: false
---
"""
        frontmatter = parse_frontmatter(text)
        self.assertEqual(frontmatter["required_capabilities"], ["architecture-review", "graph-analysis"])
        self.assertIs(frontmatter["player_facing"], False)

    def test_parse_work_order_file_reads_scope_lists(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "WO-9999-test.md"
            path.write_text(
                """---
work_order_id: WO-9999
title: Test Router
project: atlasstudio
required_capabilities:
  - architecture-review
---

# WO-9999 - Test Router

## Purpose

Extend the Planning Engine.

## Scope

### In Scope

- Add scoring.

### Out of Scope

- Change canon.
""",
                encoding="utf-8",
            )
            request = parse_work_order_file(path)
        self.assertEqual(request.required_capabilities, ["architecture-review"])
        self.assertEqual(request.scope_in, ["Add scoring."])
        self.assertEqual(request.scope_out, ["Change canon."])

    def test_audit_append_and_read(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            old = os.environ.get("ATLAS_ROUTER_AUDIT_DIR")
            os.environ["ATLAS_ROUTER_AUDIT_DIR"] = directory
            try:
                request = WorkOrderRequest(
                    source_path=None,
                    work_order_id="WO-9999",
                    title="Write shopkeeper dialogue",
                    project="atlasstudio",
                    purpose="Write shopkeeper dialogue",
                )
                decision = route(request, classify(request))
                outcome = DispatchOutcome(
                    action="no_action_blocked",
                    target_repository=decision.target_repository,
                    path_or_url=None,
                    dispatched_at=None,
                    idempotency_key="abc123",
                )
                audit.append_routing_record(decision, outcome)
                record = audit.read_routing_record("WO-9999")
            finally:
                if old is None:
                    os.environ.pop("ATLAS_ROUTER_AUDIT_DIR", None)
                else:
                    os.environ["ATLAS_ROUTER_AUDIT_DIR"] = old
        self.assertIsNotNone(record)
        assert record is not None
        self.assertEqual(record["classification"], "canon")
        self.assertEqual(record["dispatch"]["idempotency_key"], "abc123")

    def test_cli_classify_writes_audit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            old = os.environ.get("ATLAS_ROUTER_AUDIT_DIR")
            os.environ["ATLAS_ROUTER_AUDIT_DIR"] = directory
            try:
                stdout = io.StringIO()
                with contextlib.redirect_stdout(stdout):
                    code = main(["classify", "Write shopkeeper dialogue", "--json"])
                output = json.loads(stdout.getvalue())
                record = audit.read_routing_record("REQ-WRITE-SHOPKEEPER-DIALOGUE")
            finally:
                if old is None:
                    os.environ.pop("ATLAS_ROUTER_AUDIT_DIR", None)
                else:
                    os.environ["ATLAS_ROUTER_AUDIT_DIR"] = old
        self.assertEqual(code, 0)
        self.assertEqual(output["routing_decision"]["classification"], "canon")
        self.assertIsNotNone(record)

    def test_cli_explain_inline_request(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = main(["explain", "Create a graph diff tool"])
        self.assertEqual(code, 0)
        self.assertIn("Classification: production_orchestration", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
