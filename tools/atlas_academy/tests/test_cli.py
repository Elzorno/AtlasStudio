from __future__ import annotations

import contextlib
import io
import json
import unittest

from tools.atlas_academy import cli


class AtlasAcademyCliTests(unittest.TestCase):
    def test_help_with_no_arguments(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = cli.main([])
        self.assertEqual(code, 0)
        self.assertIn("atlas academy - read-only interface", stdout.getvalue())

    def test_list_case_studies_finds_the_wo_2007_worked_example(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = cli.main(["list", "--kind", "case-studies", "--json"])
        self.assertEqual(code, 0)
        payload = json.loads(stdout.getvalue())
        paths = [item["path"] for item in payload["case-studies"]]
        self.assertIn("academy/case-studies/official-map-001.md", paths)

    def test_list_excludes_readme_files(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            cli.main(["list", "--kind", "references", "--json"])
        payload = json.loads(stdout.getvalue())
        names = [item["path"].rsplit("/", 1)[-1] for item in payload["references"]]
        self.assertNotIn("README.md", names)

    def test_list_kind_all_covers_every_declared_kind(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            cli.main(["list", "--json"])
        payload = json.loads(stdout.getvalue())
        self.assertEqual(set(payload.keys()), set(cli.KIND_DIRS.keys()))

    def test_study_matches_by_id_substring(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = cli.main(["study", "001", "--json"])
        self.assertEqual(code, 0)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(payload["path"], "academy/case-studies/official-map-001.md")
        self.assertIn("Observation", " ".join(payload["sections"]))
        self.assertIsNone(payload["text"])

    def test_study_full_includes_text(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = cli.main(["study", "001", "--full", "--json"])
        self.assertEqual(code, 0)
        payload = json.loads(stdout.getvalue())
        self.assertIsNotNone(payload["text"])
        self.assertIn("Item Shop", payload["text"])

    def test_study_unknown_id_reports_available_studies(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = cli.main(["study", "does-not-exist"])
        self.assertEqual(code, 1)
        self.assertIn("No case study matches", stderr.getvalue())
        self.assertIn("official-map-001.md", stderr.getvalue())

    def test_report_ambiguous_query_lists_all_matches(self) -> None:
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            code = cli.main(["report", "composition"])
        self.assertEqual(code, 1)
        self.assertIn("is ambiguous", stderr.getvalue())
        self.assertIn("composition-analysis-framework.md", stderr.getvalue())
        self.assertIn("composition-validator-design.md", stderr.getvalue())

    def test_report_finds_documents_from_both_report_locations(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = cli.main(["report", "knowledge-extraction", "--json"])
        self.assertEqual(code, 0)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(payload["path"], "academy/reports/knowledge-extraction-report.md")

    def test_grade_without_filed_records_reports_where_the_worked_example_lives(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = cli.main(["grade", "--json"])
        self.assertEqual(code, 9)
        payload = json.loads(stdout.getvalue())
        self.assertFalse(payload["grades_dir_exists"])
        self.assertIn("GRD-ASHFORDINN-001", payload["message"])

    def test_references_lists_source_classes(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = cli.main(["references", "--json"])
        self.assertEqual(code, 0)
        payload = json.loads(stdout.getvalue())
        paths = [item["path"] for item in payload]
        self.assertIn("academy/references/source-classes.md", paths)

    def test_cli_never_writes_to_academy_directory(self) -> None:
        before = sorted(p.relative_to(cli.REPO_ROOT) for p in cli.ACADEMY_DIR.rglob("*"))
        with contextlib.redirect_stdout(io.StringIO()):
            cli.main(["list"])
            cli.main(["study", "001", "--full"])
            cli.main(["report", "knowledge-extraction"])
            cli.main(["grade"])
            cli.main(["references"])
        after = sorted(p.relative_to(cli.REPO_ROOT) for p in cli.ACADEMY_DIR.rglob("*"))
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
