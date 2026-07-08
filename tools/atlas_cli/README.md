# Atlas Unified CLI

`tools.atlas_cli` is the first implementation of the unified `atlas` command
specified by `studio/interface/ATLAS_CLI_SPEC.md`.

It is intentionally thin:

- Existing tools stay authoritative for their domains.
- Passthrough commands preserve the wrapped tool's arguments and exit code.
- Summary commands read existing reports, graph data, work orders, and routing
  logs without modifying sibling repositories or canon.
- The implementation uses only Python's standard library.

## Usage

```bash
python3 -m tools.atlas_cli.cli --help
python3 -m tools.atlas_cli.cli status
python3 -m tools.atlas_cli.cli today
python3 -m tools.atlas_cli.cli doctor
python3 -m tools.atlas_cli.cli route preview "Build Ashford Inn"
python3 -m tools.atlas_cli.cli validate
python3 -m tools.atlas_cli.cli planner
python3 -m tools.atlas_cli.cli graph validate
python3 -m tools.atlas_cli.cli work list
python3 -m tools.atlas_cli.cli history
```

Running without arguments launches the interactive shell:

```bash
python3 -m tools.atlas_cli.cli
```

Inside the shell, omit the `atlas` prefix:

```text
atlas> status
atlas> route preview "Build Ashford Inn"
atlas> exit
```

## Implemented Commands

- `today`: repository state, Studio Health summary, router attention items, and
  the top planner recommendation.
- `status`: one-screen Studio Health snapshot for the shell banner.
- `doctor`: passthrough to `tools/atlas_doctor/doctor.py`.
- `route`: read-only classification/preview over `tools/atlas_router`.
- `validate`: `tools/atlas_graph/validate_graph.py`, then
  `tools/atlas_format/format_guard.py --check`.
- `planner` / `plan`: passthrough to `tools/atlas_planner/planner.py`.
- `graph`: passthrough to `tools/atlas_graph/query_graph.py`; `graph validate`
  routes to `tools/atlas_graph/validate_graph.py`.
- `work`: `create` passthrough plus read-only `list`, `show`, and `review`.
- `review`: day-level work-order review, or `--work-order` alias for
  `work review`.
- `history`: router log, work-order commit, and decision-record history.
- `dispatch`: passthrough to `tools/atlas_router/cli.py wo dispatch`.
- `academy`: passthrough to `tools/atlas_academy/cli.py` - read-only access
  to Atlas Academy's case studies, knowledge, reports, grades, and
  reference-governance documents. See `tools/atlas_academy/README.md`.

## Verification

```bash
python3 -m unittest discover -s tools/atlas_cli/tests -v
```

