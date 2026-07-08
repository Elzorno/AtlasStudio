# Work Order Router - Implementation Specification

## Status

This is a specification, not code. No file under `tools/atlas_router/` other than this document and its three companions (`CLI_SPEC.md`, `ROUTING_TEST_PLAN.md`, `ERROR_HANDLING.md`) exists yet. This document is written so that Codex can implement the package described below without making a single architectural decision - every module, function signature, data shape, and rule referenced here already exists in an approved design document, listed under Source Documents.

## Source Documents (authoritative - do not re-derive, only translate to code)

- `studio/orchestration/work-order-router.md` (WO-0021) - classification model, routing rules, safety rules, target repository mapping. This is the specification of *what* the router decides.
- `schemas/work-order-routing.schema.json` (WO-0021) - the exact shape of a routing decision record.
- `studio/governance/repository-authority.md` (WO-0018) - the ownership boundary table. Hardcode this as static data; do not parse it from Markdown at runtime.
- `studio/scheduling/agent-scheduler-design.md` (WO-0012) - the deterministic agent-recommendation algorithm this package's `scheduler.py` implements verbatim.
- `schemas/agent-status.schema.json` and `studio/scheduling/agent-status.example.json` - the manual availability data `scheduler.py` reads.
- `studio/agent-roles.md` - the per-agent "best for / avoid" lists used as the scheduler's underlying rationale text.
- `bridges/atlas/implementation-handoff.md` (WO-0019) - the "point, don't paraphrase" rule this package's dispatch behavior for `canon` and `game_implementation` must follow.
- `work-orders/WO-0020-ashford-village-implementation-contract-from-atlas-handoff.md` - the precedent shape for an implementation contract, which `dispatcher.py` produces for unapproved `game_implementation` requests.
- `studio/work-order-format.md` - the frontmatter and body template `dispatcher.py` writes into new AtlasStudio work orders.
- `tools/atlas_planner/planner.py`, `tools/atlas_doctor/doctor.py`, `tools/atlas_graph/atlas_graph.py` - existing code whose conventions (stdlib-only, `sys.dont_write_bytecode`, `REPO_ROOT` resolution, manual frontmatter parsing, `argparse`, dataclasses, `--json` flag) this package must match rather than reinvent.

If implementation reveals a gap none of the above documents cover, the correct action is to stop and request a documentation update - not to invent a rule inline. This mirrors the "ambiguous work orders stop" rule the router itself enforces on its own input.

## Overall Architecture

The router is a five-stage pipeline. Every stage is a pure function of its inputs plus the static authority/scheduler data files - no stage calls a network service except the final dispatch stage's optional GitHub call, and even that call is isolated to one module (`github.py`).

```text
Work Order Request (Markdown file or CLI flags)
        |
        v
   [1] parser.py     -> WorkOrderRequest
        |
        v
   [2] classifier.py -> ClassificationResult
        |
        v
   [3] authority.py  -> RoutingDecision   (enforces WO-0021 Safety Rules)
        |
        v
   [4] scheduler.py  -> RoutingDecision + SchedulerRecommendation (advisory)
        |
        v
   [5] dispatcher.py -> DispatchOutcome   (local file write, or github.py issue, or nothing)
        |
        v
   audit.py appends RoutingDecision (+ DispatchOutcome, if any) to the audit log
```

`atlas wo classify` runs stages 1-3. `atlas wo preview` runs stages 1-4 without stage 5. `atlas wo dispatch` runs all five stages. `atlas wo create` runs stages 1-3 and, only for classifications that resolve to an AtlasStudio-owned target, proceeds to write a `proposed` work order (a restricted form of stage 5; see `dispatcher.py` below). Every stage's output is appended to the audit log by `audit.py` regardless of which CLI command triggered it, so partial runs (e.g., `classify` alone) still produce a permanent record.

## Directory Layout

```text
tools/atlas_router/
    __init__.py
    cli.py
    models.py
    parser.py
    classifier.py
    authority.py
    scheduler.py
    dispatcher.py
    github.py
    audit.py
    tests/
        __init__.py
        fixtures/
            *.md            # one file per ROUTING_TEST_PLAN.md case, named case_01_... .md etc.
        test_parser.py
        test_classifier.py
        test_authority.py
        test_scheduler.py
        test_dispatcher.py
        test_audit.py
        test_cli.py
```

No other files. No `requirements.txt`, `pyproject.toml`, or third-party dependency of any kind - this package is stdlib-only, matching every existing `tools/atlas_*` package. The one external process this package may invoke is the `gh` CLI (already relied on elsewhere in this environment for GitHub operations), invoked exclusively from `github.py` via `subprocess.run`.

## Module Specifications

### `models.py`

Pure data definitions. No I/O, no logic beyond `__post_init__` field validation and `to_dict()` / `from_dict()` methods. All dataclasses use `from __future__ import annotations` and `@dataclass` (or `@dataclass(frozen=True)` for immutable records), matching `tools/atlas_planner/planner.py`'s style.

```python
CLASSIFICATIONS = ("canon", "game_implementation", "production_orchestration", "cross_repository_bridge", "ambiguous")
TARGET_REPOSITORIES = ("TheLastSwordProtocol-Atlas", "TheLastSwordProtocol-Game", "AtlasStudio", "none")
ROUTING_STATUSES = ("routed", "pending_approval", "blocked_ambiguous", "rejected_authority_violation")
TASK_CLASSES = ("creative_design", "architecture", "implementation", "repetitive_edit", "review_qa", "canon_decision")

@dataclass
class WorkOrderRequest:
    source_path: str | None          # None when built from CLI flags via `atlas wo create`
    work_order_id: str | None        # None for a not-yet-filed request
    title: str
    project: str
    purpose: str
    scope_in: list[str]
    scope_out: list[str]
    required_capabilities: list[str]
    preferred_capabilities: list[str]
    risk_level: str
    player_facing: bool
    engine_specific: bool
    claimed_target_repository: str | None   # a self-declared target_repository field, if present; NEVER trusted over classifier signals

@dataclass
class ClassificationResult:
    classification: str              # one of CLASSIFICATIONS
    signals_matched: list[str]       # human-readable signal descriptions, per work-order-router.md's Signals table
    conflicting_classifications: list[str]  # non-empty only when classification == "ambiguous" due to a split verdict
    ambiguous_reason: str | None     # None unless classification == "ambiguous"

@dataclass
class SchedulerRecommendation:
    task_class: str                  # one of TASK_CLASSES
    primary_agent: str | None        # "agent.<id>" or None if task_class == "canon_decision" and no draft support applies
    primary_provider: str | None
    score: int | None
    components: dict[str, int]
    fallbacks: list[dict[str, Any]]  # same shape as agent-scheduler-design.md's "fallbacks" list
    excluded: list[dict[str, str]]
    advisory: bool                   # True whenever target_repository != "AtlasStudio"; Atlas/Game keep final assignment authority
    evidence: list[str]

@dataclass
class RoutingDecision:
    # Mirrors schemas/work-order-routing.schema.json field-for-field.
    schema_version: str
    work_order_id: str
    title: str
    classification: str
    target_repository: str
    target_path_hint: str | None
    routing_status: str
    requires_explicit_approval: bool
    approved_by: str | None
    approved_at: str | None          # ISO date
    signals_matched: list[str]
    rationale: str
    safety_flags: dict[str, bool]    # {"canon_leak_risk": bool, "cross_repo_write_attempted": bool}
    created: str                     # ISO date
    decided_by: str                  # "tools/atlas_router/router.py" or a human identity string
    scheduler_recommendation: SchedulerRecommendation | None  # not part of the JSON Schema's required fields; stored as an extra key the schema permits only if additionalProperties is relaxed for this field - see Note below.
    warnings: list[str]

@dataclass
class DispatchOutcome:
    action: str                      # "wrote_local_work_order" | "opened_github_issue" | "no_action_pending_approval" | "no_action_blocked"
    target_repository: str
    path_or_url: str | None
    dispatched_at: str | None
    idempotency_key: str             # stable hash of work_order_id + classification, used to avoid duplicate GitHub issues on retry
```

Note on `scheduler_recommendation`: `schemas/work-order-routing.schema.json` is `additionalProperties: false` and does not define this field, because the schema models the router's classification/authority decision, not the scheduler's advisory output. `models.py` must therefore serialize `RoutingDecision` to two different JSON shapes: `to_schema_dict()` (only the fields the schema defines, for `audit.py`'s schema-validated log) and `to_full_dict()` (every field, including `scheduler_recommendation` and `warnings`, for CLI display). This split is intentional and required - never relax `additionalProperties` on the schema to fit the scheduler data in; the schema is a WO-0021 deliverable and is not part of this work order's Allowed Changes.

### `parser.py`

Reads either a work order Markdown file or CLI-flag input into a `WorkOrderRequest`.

```python
def parse_work_order_file(path: Path) -> WorkOrderRequest: ...
def parse_request_from_args(args: argparse.Namespace) -> WorkOrderRequest: ...
def parse_frontmatter(text: str) -> dict[str, Any]: ...
def parse_scalar(value: str) -> Any: ...
def parse_bool(value: Any) -> bool: ...
def section_text(text: str, heading: str) -> str: ...
def section_list_items(text: str, heading: str) -> list[str]: ...
```

`parse_frontmatter` extends `tools/atlas_planner/planner.py`'s function of the same name to support single-level YAML list values, because `required_capabilities`, `preferred_capabilities`, and `produces` are lists and the existing implementation silently drops them (any line without a `:` is skipped). The extension: when a `key:` line is followed by one or more lines matching `^\s*-\s+(.+)$` before the next `key:` line or the closing `---`, collect those as a `list[str]` value for that key instead of a scalar. Scalar parsing (`parse_scalar`, `parse_bool`) is otherwise reused unchanged. `section_text` and `section_list_items` reuse `planner.py`'s heading-scan approach; `section_list_items` additionally recognizes Markdown bullet lines (`- item`) under a heading and returns them as a list, used to read `## Scope` -> `### In Scope` / `### Out Of Scope` bullets into `scope_in` / `scope_out`.

`parse_request_from_args` builds a `WorkOrderRequest` with `source_path=None` and `work_order_id=None` directly from `atlas wo create`'s flags (see `CLI_SPEC.md`), with no Markdown parsing involved.

### `classifier.py`

```python
def classify(request: WorkOrderRequest) -> ClassificationResult: ...
```

Implements the Signals table in `studio/orchestration/work-order-router.md` as an ordered list of signal-check functions, each returning `None` or a `(classification, signal_description)` tuple:

```python
SIGNAL_CHECKS: list[Callable[[WorkOrderRequest], tuple[str, str] | None]] = [
    _check_canon_capability,          # required_capabilities has canon-design / creative-writing / final-canon
    _check_canon_noun,                # title/purpose/scope contains a canon noun (see CANON_NOUNS below)
    _check_game_implementation_capability,   # required_capabilities has rpg-maker-json AND a named Game-repo file/map
    _check_orchestration_capability,  # required_capabilities has architecture-review/schema-design/graph-analysis AND names tools/, studio/, schemas/, or "Atlas Graph"
    _check_bridge_signal,             # scope describes importing/diffing/handing off already-existing sibling-repo content without proposing new content
]
```

`classify` runs every check (not short-circuiting on the first match), collects every `(classification, signal)` pair returned, and applies exactly this decision rule, matching work-order-router.md's "Classification Model" section verbatim:

1. If zero checks matched: `classification = "ambiguous"`, `ambiguous_reason = "no_signal_matched"`.
2. If every matched check agrees on one classification: use it; `signals_matched` lists every matched signal description.
3. If matched checks disagree (more than one distinct classification value present): `classification = "ambiguous"`, `ambiguous_reason = "conflicting_repository_signals"`, `conflicting_classifications` lists the distinct values found. Per work-order-router.md: "The router does not average or pick a majority."

`CANON_NOUNS` and `GAME_IMPLEMENTATION_FILE_PATTERNS` are static word/regex lists derived directly from `studio/governance/repository-authority.md`'s ownership table (story, character, protagonist, quest, dialogue, lore, world, region, location, faction nouns for canon; `Map\d+\.json`, `System.json`, `Tilesets.json`, `map_ownership.json`, "tileset", "transfer event" for game_implementation) and from `studio/atlas-graph/node-types.md`'s Canon Node Types list, so the word list has one traceable source rather than being invented ad hoc.

### `authority.py`

The enforcement point for every Safety Rule in `studio/orchestration/work-order-router.md`. Converts a `ClassificationResult` into a `RoutingDecision`.

```python
REPOSITORY_BOUNDARIES: dict[str, dict[str, Any]] = { ... }  # hardcoded transcription of repository-authority.md's ownership table; see below

def route(request: WorkOrderRequest, classification: ClassificationResult) -> RoutingDecision: ...
def _target_for(classification: str) -> tuple[str, str]: ...   # (target_repository, target_path_hint), per the Target Repository / Path Mapping table
def _check_forced_override(request: WorkOrderRequest, decision: RoutingDecision) -> RoutingDecision: ...
```

`REPOSITORY_BOUNDARIES` is a literal Python dict transcription of `repository-authority.md`'s ownership table - not a Markdown parser. Example shape:

```python
REPOSITORY_BOUNDARIES = {
    "canon": {"owner": "TheLastSwordProtocol-Atlas", "may_be_authored_by_atlasstudio": False},
    "game_implementation": {"owner": "TheLastSwordProtocol-Game", "requires_explicit_approval": True},
    "production_orchestration": {"owner": "AtlasStudio", "may_be_authored_by_atlasstudio": True},
    "cross_repository_bridge": {"owner": "AtlasStudio", "may_be_authored_by_atlasstudio": True, "write_restricted_to": "bridges/"},
}
```

`route` logic, in order:

1. If `classification.classification == "ambiguous"`: return a `RoutingDecision` with `target_repository="none"`, `routing_status="blocked_ambiguous"`, `rationale` built from `classification.ambiguous_reason` (using the exact wording template in `ERROR_HANDLING.md`), and stop. No further step runs.
2. Otherwise look up `_target_for(classification.classification)` for the default `(target_repository, target_path_hint)`.
3. **Forced-override check (must run before anything else touches `target_repository`):** if `request.claimed_target_repository` is set and differs from the computed target, the computed target from the classifier always wins - `request.claimed_target_repository` is never used to set `RoutingDecision.target_repository`. If the classifier's computed target is `TheLastSwordProtocol-Atlas` (i.e., `classification == "canon"`) and the request's claimed target was `"AtlasStudio"`, additionally set `routing_status = "rejected_authority_violation"` and `safety_flags.canon_leak_risk = True` - this is the literal implementation of "the router must never silently move canon into AtlasStudio," tested explicitly by `ROUTING_TEST_PLAN.md` case 30.
4. If `classification.classification == "game_implementation"`: set `requires_explicit_approval = True`. If `request` carries no approval evidence (see `CLI_SPEC.md`'s `--approved-by`/`--approved-at` flags), `target_repository = "AtlasStudio"` (the implementation-contract path) and `routing_status = "pending_approval"`. If approval evidence is present, `target_repository = "TheLastSwordProtocol-Game"` and `routing_status = "routed"`.
5. Otherwise (`canon`, `production_orchestration`, `cross_repository_bridge` with no override conflict): `routing_status = "routed"`.
6. Populate `rationale` from `signals_matched`, `safety_flags` defaulting to `{"canon_leak_risk": False, "cross_repo_write_attempted": False}` unless step 3 set them, `created` to today's date, `decided_by` to `"tools/atlas_router/router.py"`.

`authority.py` must fail closed: if `REPOSITORY_BOUNDARIES` fails to import or is empty (this should be structurally impossible since it is a literal in the module, but the rule is stated for the test suite to assert), `route` must raise rather than default any request to any repository. There is no code path in which a classification failure results in `target_repository = "AtlasStudio"` by default.

### `scheduler.py`

Implements `studio/scheduling/agent-scheduler-design.md`'s algorithm exactly, reusing its worked-example numbers as unit test oracles.

```python
CAPABILITY_TABLE: dict[str, dict[str, int]] = { ... }   # transcription of the Agent Capability Profiles table
AGENT_PROFILES: dict[str, dict[str, Any]] = { ... }      # risk_ceiling, context_depth, scarcity per agent, from the same doc

def task_class_for(request: WorkOrderRequest, classification: ClassificationResult) -> str: ...
def load_agent_status(path: Path | None = None) -> dict[str, dict[str, Any]]: ...
def recommend(request: WorkOrderRequest, classification: ClassificationResult, routing: RoutingDecision, status_path: Path | None = None) -> SchedulerRecommendation: ...
```

`task_class_for` maps a router `classification` (not a scheduler concept on its own) to a scheduler `task_class` using this fixed table, which resolves the mapping gap between the two documents' vocabularies:

| Router classification | Task class | Rationale |
|---|---|---|
| `canon` | `creative_design`, unless the request's Purpose/title contains a finality verb (`decide`, `resolve`, `finalize`, `canonize`) matching `canon_decision` per agent-scheduler-design.md's own rule | Drafting quest/dialogue/lore content is creative_design; only the act of finalizing disputed canon is canon_decision |
| `game_implementation` | `implementation` | Matches agent-roles.md's Codex "RPG Maker implementation" best-for entry |
| `production_orchestration` | Existing `studio/scheduling/agent-scheduler-design.md` Task Classification signals 1-5, applied unchanged | No new mapping needed; this is AtlasStudio's own work |
| `cross_repository_bridge` | `architecture` | Matches the WO-0019 precedent assignment (claude_code, senior-software-architect) |
| `ambiguous` | N/A | `scheduler.py` is never called for an ambiguous `RoutingDecision`; `dispatcher.py` and `cli.py` must skip this stage entirely rather than call it with a placeholder task_class |

`recommend` then runs `agent-scheduler-design.md`'s six-step Scheduling Algorithm (classify already done via `task_class_for`; capability filter; risk gate; availability filter; rank; fallback chain; emit) verbatim, using `CAPABILITY_TABLE` and `AGENT_PROFILES` for steps 2-5 and `load_agent_status` for step 4's data. `load_agent_status` reads `studio/scheduling/agent-status.json` if it exists (validated shape per `schemas/agent-status.schema.json`), else falls back to `studio/scheduling/agent-status.example.json` and the returned `SchedulerRecommendation.advisory` is forced `True` with a warning appended (see `ERROR_HANDLING.md`, "missing scheduler information").

`SchedulerRecommendation.advisory` is additionally forced `True` whenever `routing.target_repository != "AtlasStudio"` (i.e., for `canon` and for `game_implementation` before approval), regardless of the status file used, because AtlasStudio never has final assignment authority over another repository's own production - see `studio/governance/repository-authority.md`. An advisory recommendation is still computed and shown (it is useful context to attach to a GitHub proposal issue), but `dispatcher.py` must never treat it as binding.

### `dispatcher.py`

```python
def dispatch(request: WorkOrderRequest, routing: RoutingDecision, recommendation: SchedulerRecommendation | None, *, dry_run: bool) -> DispatchOutcome: ...
def _next_work_order_id(work_orders_dir: Path) -> str: ...
def _render_work_order_markdown(request, routing, recommendation, work_order_id: str) -> str: ...
def _render_github_issue_body(request, routing, recommendation) -> str: ...
```

Behavior by `routing.routing_status` / `routing.target_repository`, matching `work-order-router.md`'s Routing Rules and Target Repository / Path Mapping table exactly:

| Case | Action | Writes a local file? | Calls `github.py`? |
|---|---|---|---|
| `target_repository == "AtlasStudio"`, `routing_status == "routed"` (`production_orchestration`, `cross_repository_bridge`) | Render and write a new `work-orders/WO-NNNN-*.md` using `studio/work-order-format.md`'s template, `status: proposed` | Yes, under `work-orders/` | No |
| `target_repository == "AtlasStudio"`, `routing_status == "pending_approval"` (`game_implementation`, unapproved) | Render and write an implementation-contract-shaped work order (`WO-0020` pattern: points at the cited Atlas implementation packet, does not restate its content), `status: proposed` | Yes, under `work-orders/` | No |
| `target_repository == "TheLastSwordProtocol-Game"`, `routing_status == "routed"` (`game_implementation`, approved) | Open a GitHub issue in `TheLastSwordProtocol-Game` containing the approved contract, tagged for that repository's own `AGENTS.md`/`map_ownership.json` workflow | No | Yes |
| `target_repository == "TheLastSwordProtocol-Atlas"` (`canon`, always, and `cross_repository_bridge` tooling proposals per `repository-authority.md`'s change-flow) | Open a GitHub issue in `TheLastSwordProtocol-Atlas` containing the *original request's title/purpose/scope verbatim* - never AtlasStudio's paraphrase, per WO-0019's "point, don't paraphrase" rule - tagged for that repository's own work-order intake | No | Yes |
| `routing_status == "blocked_ambiguous"` or `"rejected_authority_violation"` | No action of any kind. `DispatchOutcome.action = "no_action_blocked"` | No | No |

`dry_run=True` (used by `atlas wo preview`) computes and returns the `DispatchOutcome` that *would* result, including the exact rendered Markdown or issue body in `DispatchOutcome.path_or_url` as a local preview path under a temp-like `reports/atlas-router/previews/` location, but performs no write to `work-orders/` and no GitHub call. `atlas wo create` always calls `dispatch` with `dry_run=False` but only for classifications whose target is `AtlasStudio` (the first two table rows); for any other classification, `atlas wo create` stops after `authority.py` and reports the routing decision without calling `dispatcher.py` at all - creating a *new* AtlasStudio work order is never the right action for canon or unapproved game_implementation content, so the dispatcher's local-write path is structurally unreachable for those classifications, not merely policy-blocked.

`_next_work_order_id` scans `work-orders/WO-*.md` for the highest existing `WO-NNNN` number and returns the next one, zero-padded to four digits, matching the existing numbering convention (WO-0001 through WO-0022 as of this specification).

### `github.py`

The only module permitted to perform network I/O. Two functions only:

```python
def check_reachable(repo: str) -> bool: ...          # `gh repo view <owner>/<repo>` with a short timeout; True/False, never raises
def open_issue(repo: str, title: str, body: str, labels: list[str]) -> str: ...  # returns the created issue URL; raises GithubUnavailableError or NetworkError (see ERROR_HANDLING.md)
```

Implemented via `subprocess.run(["gh", "issue", "create", "--repo", repo, "--title", title, "--body", body, "--label", ",".join(labels)], capture_output=True, timeout=30)`, matching this environment's existing convention of using the `gh` CLI for all GitHub operations rather than a raw HTTP client or an API-key-bearing library. `repo` is always one of the two literal strings `"Elzorno/TheLastSwordProtocol-Atlas"` or `"Elzorno/TheLastSwordProtocol-Game"` (the actual `origin` remotes of the two sibling repositories) - never a value derived from user input, to prevent a malformed request from directing an issue to an arbitrary repository. `open_issue` is idempotent per `DispatchOutcome.idempotency_key`: before creating an issue, `dispatcher.py` checks the audit log (via `audit.py`) for a prior `DispatchOutcome` with the same `idempotency_key` and `action == "opened_github_issue"`; if found, `dispatch` returns that prior outcome instead of creating a duplicate.

`github.py` must never accept a write/push/merge operation of any kind - only `issue create` and `repo view` (read-only reachability check) are implemented, matching `bridges/atlas/implementation-handoff.md`'s "It does not grant AtlasStudio... write access... as a side effect" rule literally at the code level, not just as a documented policy.

### `audit.py`

```python
def append_routing_record(decision: RoutingDecision, outcome: DispatchOutcome | None = None) -> None: ...
def read_routing_record(work_order_id: str) -> dict[str, Any] | None: ...   # most recent record for this id, or None
def append_correction(work_order_id: str, original: str, corrected: str, reason: str, corrected_by: str) -> None: ...
```

- `append_routing_record` appends one line of `json.dumps(decision.to_schema_dict() | ({"dispatch": outcome.to_dict()} if outcome else {}))` to `reports/atlas-router/routing-log.jsonl`, creating the file and its parent directory if absent. Append-only: this function never opens the file in a mode other than `"a"`, and never rewrites a previous line - preserving history is the same principle behind the Immutable Formatting Rule, applied to this new log rather than to the canon graph.
- `read_routing_record` scans the log for the last line whose `work_order_id` matches, used by `atlas wo explain`.
- `append_correction` appends to `reports/atlas-router/corrections.jsonl`, per `work-order-router.md`'s "Human Correction Logging" implementation-plan step. This function only ever logs; it never modifies `classifier.py`'s signal tables. Any signal-table change stays a manual, documented edit to `work-order-router.md` and `classifier.py`, reviewed like an ADR.

### `cli.py`

`argparse` entrypoint, matching `tools/atlas_graph/query_graph.py`'s subparser style. Full command specification is in `CLI_SPEC.md`; `cli.py`'s responsibility is limited to argument parsing, wiring parsed args to the module functions above in the pipeline order, and exit-code selection per the shared table in `CLI_SPEC.md`. `cli.py` contains no classification, authority, or scheduling logic of its own - if a rule isn't already specified in another module above, it does not belong in `cli.py`.

`main()` returns an `int` exit code, following every existing `tools/atlas_*` script's convention (`doctor.py`, `format_guard.py`, `planner.py` all do this), and the module ends with:

```python
if __name__ == "__main__":
    sys.exit(main())
```

## Dependency Graph

```text
models.py       <- (no internal deps)
parser.py       <- models.py
classifier.py   <- models.py, parser.py (types only, no function calls)
scheduler.py     <- models.py
authority.py    <- models.py, classifier.py (types only)
github.py       <- models.py (types only)
audit.py        <- models.py
dispatcher.py   <- models.py, authority.py (types only), scheduler.py (types only), github.py, audit.py
cli.py          <- parser.py, classifier.py, authority.py, scheduler.py, dispatcher.py, audit.py
                <- subprocess passthrough only (no import) to tools/atlas_doctor/doctor.py,
                   tools/atlas_planner/planner.py, tools/atlas_graph/query_graph.py,
                   tools/atlas_graph/validate_graph.py, tools/atlas_format/format_guard.py
```

No module in this package imports from `tools/atlas_graph`, `tools/atlas_doctor`, or `tools/atlas_planner` directly - `cli.py`'s passthrough commands invoke those tools as separate subprocesses (see `CLI_SPEC.md`), not as in-process imports, because those tools' own `argparse` surfaces are already stable public interfaces and re-parsing their output in-process would duplicate logic that already exists and works. This is a deliberate deviation from `tools/atlas_planner/planner.py`'s existing in-process-import pattern (it imports `doctor.build_health` directly): that pattern is acceptable for `planner.py` because it consumes `doctor.py`'s data as an input to its own scoring, whereas `cli.py`'s passthrough commands do not consume or transform the other tools' output at all - they only forward the exit code and stream output, so a subprocess call is the simpler, lower-judgment choice here.

## Logging and Audit Records

Two append-only JSON Lines files, both under `reports/atlas-router/` (created if absent, never truncated or rewritten):

- `reports/atlas-router/routing-log.jsonl` - one line per `RoutingDecision` (plus `DispatchOutcome` when dispatch ran), written by every `atlas wo classify|preview|create|dispatch` invocation regardless of outcome, including blocked and rejected ones. This is the router's full audit trail.
- `reports/atlas-router/corrections.jsonl` - one line per human override of a router classification, written only when a human explicitly runs a future correction command (out of scope for this specification's CLI surface; `audit.append_correction` exists now so `dispatcher.py`/`cli.py` have a stable function to call once that command is specified in a follow-up work order).

Diagnostic logging (not audit data) follows the existing convention: human-readable progress and error text goes to `stderr`; the final structured result goes to `stdout`, as plain text by default or as JSON when `--json` is passed, matching `doctor.py`, `planner.py`, and `format_guard.py`.

## What This Specification Does Not Do

It does not implement any code. It does not modify `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game`. It does not modify AtlasStudio's canon or `schemas/work-order-routing.schema.json` (that schema is a WO-0021 deliverable, referenced here read-only). It does not redesign any routing rule, classification category, or safety rule from WO-0021 - every behavior above is a direct translation of an existing rule into a function signature, not a new decision.
