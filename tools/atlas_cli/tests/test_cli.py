from __future__ import annotations

import contextlib
import io
import unittest
from unittest.mock import patch

from tools.atlas_cli import cli


class AtlasCliTests(unittest.TestCase):
    def test_route_preview_reuses_router_without_audit_passthrough(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = cli.main(["route", "preview", "Build Ashford Shop from IMP-HOM-019"])
        self.assertEqual(code, 0)
        output = stdout.getvalue()
        self.assertIn("Classification: game_implementation", output)
        self.assertIn("Routing status: pending_approval", output)
        self.assertIn("Action: would_write_local_work_order", output)

    def test_graph_validate_routes_to_graph_validator(self) -> None:
        with patch("tools.atlas_cli.cli.passthrough", return_value=0) as passthrough:
            code = cli.main(["graph", "validate", "--json"])
        self.assertEqual(code, 0)
        passthrough.assert_called_once_with("tools/atlas_graph/validate_graph.py", ["--json"])

    def test_validate_runs_format_guard_only_after_clean_graph(self) -> None:
        with patch("tools.atlas_cli.cli.passthrough", side_effect=[0, 0]) as passthrough:
            code = cli.main(["validate"])
        self.assertEqual(code, 0)
        self.assertEqual(
            passthrough.call_args_list[0].args,
            ("tools/atlas_graph/validate_graph.py", []),
        )
        self.assertEqual(
            passthrough.call_args_list[1].args,
            ("tools/atlas_format/format_guard.py", ["--check"]),
        )

    def test_work_show_reads_existing_work_order(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = cli.main(["work", "show", "WO-0030"])
        self.assertEqual(code, 0)
        self.assertIn("WO-0030 - AtlasStudio Interactive CLI", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()

