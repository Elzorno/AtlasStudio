# Atlas Academy CLI

`tools.atlas_academy` implements the `atlas academy` command group named in
`work-orders/WO-2009-atlas-academy-cli.md`, wired into the unified
`atlas` CLI (`tools/atlas_cli/cli.py`) as a passthrough, exactly like
`doctor`, `planner`, and `graph` already are.

It is intentionally read-only, following this work order's own constraint
("Do not create analysis content automatically unless explicitly requested
by the command"): every command here reads files that already exist under
`academy/`, `reports/academy/`, or `academy/grades/`. Nothing in this tool
writes a new observation, composition analysis, grade, review, or map. It
uses only Python's standard library, matching `tools/atlas_cli`'s own
implementation constraint.

## Usage

```bash
python3 -m tools.atlas_academy.cli --help
python3 -m tools.atlas_academy.cli list
python3 -m tools.atlas_academy.cli list --kind case-studies --json
python3 -m tools.atlas_academy.cli study 001
python3 -m tools.atlas_academy.cli study official-map-001 --full
python3 -m tools.atlas_academy.cli report map-grading-system
python3 -m tools.atlas_academy.cli grade
python3 -m tools.atlas_academy.cli references
python3 -m tools.atlas_academy.cli help
```

Or through the unified CLI:

```bash
python3 -m tools.atlas_cli.cli academy list
python3 -m tools.atlas_cli.cli academy study 001
```

## Implemented Commands

- `list [--kind KIND] [--json]`: lists Academy artifacts by kind
  (`case-studies`, `knowledge`, `compositions`, `observations`, `reports`,
  `references`, `templates`, or `all`), reading the corresponding
  `academy/` subdirectory (and `reports/academy/` for the `reports` kind,
  per that directory's own documented split from `academy/reports/`). Each
  entry shows its path, parsed title (first `# ` heading), and status line
  where one exists.
- `study STUDY_ID [--full] [--json]`: looks up a case study under
  `academy/case-studies/` by a substring match against the filename, and
  prints its title, status, and section headings (or the full file with
  `--full`). Reports available studies on a miss.
- `report NAME [--full] [--json]`: same lookup, across both
  `academy/reports/` and `reports/academy/` (see `academy/reports/README.md`
  for why both exist).
- `grade [TARGET] [--json]`: looks up a filed map-grade record under
  `academy/grades/`. As of this work order, no grade has been filed as a
  standalone record - `academy/grading-system.md`'s worked example
  (`GRD-ASHFORDINN-001`) lives embedded in `reports/academy/map-grading-system.md`,
  not as a file under `academy/grades/`. This command reports that plainly
  rather than fabricating a result; it does not create `academy/grades/` or
  any record in it.
- `references [--json]`: lists `academy/references/` governance documents
  (`reference-governance.md`, `source-classes.md`, `gold-standard-maps.md`).
- `help`: prints this command summary. Also the default when no
  subcommand is given.

## Design Notes

- Ambiguous `study`/`report` queries (a substring matching more than one
  file) report every match rather than guessing one - consistent with this
  project's standing discipline against silently picking an interpretation.
- `list`, `study`, `report`, and `references` all exclude `README.md` files
  from their results; those are directory-level documentation, not Academy
  content entries.
- Exit codes follow `tools/atlas_cli`'s existing convention: `0` for a
  successful result with matches, `9` for a successful lookup that found
  nothing (matching `tools/atlas_cli/cli.py`'s `work list` behavior), `1`
  for an unresolved or ambiguous query, `2` for a CLI usage error.

## References

- `studio/interface/ATLAS_CLI_SPEC.md`, `COMMAND_REFERENCE.md`
- `tools/atlas_cli/README.md`, `cli.py`
- `academy/README.md`, `curriculum.md`, `grading-system.md`
- Created by `work-orders/WO-2009-atlas-academy-cli.md`
