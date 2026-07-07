# Atlas Graph Diff Model

## Purpose

The diff model defines how AtlasStudio explains changes between two Atlas Graph states.

Graph changes matter as much as code changes. Before acting on a project, agents should be able to see which nodes and relationships were added, removed, changed, promoted, or retired since a known-good state.

The diff engine is an Atlas Core feature. It works on any project graph that follows the storage model, not only The Last Sword Protocol.

## Tool

```text
tools/atlas_graph/diff_graph.py
```

The tool is dependency-free Python. Git refs are read with `git ls-tree` and `git show`, so no checkout or temporary worktree is needed.

## Comparing Graph States

A graph state can come from a Git ref, a commit, or a plain directory.

```bash
# Compare two commits or refs
python3 tools/atlas_graph/diff_graph.py --base HEAD~1 --head HEAD

# Compare a ref against the working tree (head defaults to the working tree)
python3 tools/atlas_graph/diff_graph.py --base HEAD

# Compare two directories
python3 tools/atlas_graph/diff_graph.py --base-dir old_graph --head-dir projects/the-last-sword-protocol/graph

# Mix a ref base with a directory head
python3 tools/atlas_graph/diff_graph.py --base v0.1.0 --head-dir projects/the-last-sword-protocol/graph
```

Options:

- `--graph-dir` selects the graph directory used for ref-based loading and the working tree (defaults to the Last Sword Protocol graph).
- `--json` prints machine-readable results.
- `--output <path>` also writes the report to a file.
- `--exit-code` exits with status 1 when the states differ, for scripting and CI-style gates.

## What The Diff Reports

Nodes and edges are matched by `id`. For each item the engine reports one of:

- `added` - present in head only
- `removed` - present in base only
- `changed` - present in both with different fields

Changed items list every changed field with its base and head values.

## Scopes

Every change is attributed to the scope of the graph file it lives in: `canon`, `production`, or `bridge` (unrecognized file prefixes fall into `other`). The report groups changes by scope so reviewers can immediately tell canon changes from production-only or bridge-only changes.

If an item id moves between files, the report records a scope move (for example `production -> canon` when a fact is promoted).

## Highlighted Changes

Three kinds of changes get their own sections at the top of the report because they carry review weight:

- **Status Changes** - any `status` or `work_order_status` transition, such as `draft -> canon` or `proposed -> accepted`.
- **Scope Moves** - items relocated between canon, production, and bridge files.
- **Source Reference Changes** - changes to an item's `source` document list.

## Report Format

Human output is Markdown, suitable for QA review, agent handoff notes, and pull request descriptions:

```text
# Atlas Graph Diff

Base: HEAD~1 (projects/the-last-sword-protocol/graph) (28 nodes, 31 edges)
Head: working tree (30 nodes, 34 edges)

Summary: nodes +2 -0 ~0, edges +3 -0 ~0

## Status Changes
...

## Canon Changes
### Nodes Changed (1)
...

## Production Changes
### Edges Added (3)
...
```

JSON output mirrors the same structure: `base`, `head`, `summary`, per-scope `scopes` buckets, `status_changes`, `source_changes`, and `scope_moves`.

## Agent Handoff Rule

When a work order changes graph files, the submitting agent should include or reference a graph diff (for example `reports/atlas-diff/latest.md`) so the next agent and human reviewers can see exactly which facts changed without reading raw JSON diffs.
