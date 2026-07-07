# Immutable Formatting Rule

## Purpose

AtlasStudio must preserve meaningful diffs.

In a multi-agent project, accidental reformatting can hide the real change, make reviews harder, and create unnecessary merge conflicts. This rule prevents agents and tools from rewriting files unless formatting changes are explicitly authorized.

## Rule

Semantic work orders must not reformat unrelated existing content.

A semantic change is a change that alters project meaning, behavior, graph facts, work order status, canon, implementation, or tool behavior.

A formatting change is a change that alters whitespace, indentation, ordering, wrapping, or serialization style without changing meaning.

## Default Behavior

Agents and tools must preserve existing file style by default.

This applies to:

- Graph JSON
- Markdown
- YAML
- TOML
- package/config files
- RPG Maker JSON
- generated reports when updating existing reports
- any other file already committed to the repository

## Prohibited By Default

Unless the work order explicitly permits formatting normalization, agents must not:

- Reorder existing arrays or object keys.
- Re-indent entire files.
- Rewrite JSON using a generic serializer if it changes unrelated formatting.
- Normalize line wrapping across a document.
- Convert quote style globally.
- Run broad formatters over unrelated files.
- Mix functional changes and formatting-only changes in one diff.

## Allowed By Default

Agents may:

- Add new entries in the house style of the surrounding file.
- Modify only the lines required by the work order.
- Add generated reports when the report file is new.
- Update an existing generated report if the report itself is the deliverable.
- Use formatters in check-only mode.

## Explicit Formatting Work Orders

Formatting changes are allowed when the work order explicitly says so.

Examples:

- Normalize graph JSON formatting.
- Apply Markdown wrapping standard.
- Reformat tool source code with Black.
- Convert legacy YAML to JSON.

Such work orders should be formatting-only and should avoid semantic changes.

## Tooling Requirement

AtlasStudio should eventually provide a formatting guard that detects formatting-only churn and warns reviewers.

The first implementation should prefer check-only behavior:

```bash
python3 tools/atlas_format/format_guard.py --check
```

A future formatter may support explicit write mode:

```bash
python3 tools/atlas_format/format_guard.py --write
```

Write mode must not be used unless the work order explicitly authorizes formatting normalization.

## Agent Reporting Requirement

When submitting work, agents should report whether formatting was preserved.

Recommended submission note:

```text
Formatting: preserved existing house style; no broad reformatting performed.
```

If formatting changes were unavoidable, the agent must explain:

- Which files were reformatted.
- Why the reformat was necessary.
- Whether the reformat was authorized by the work order.
- How reviewers can distinguish semantic changes from formatting changes.

## Review Standard

A good AtlasStudio diff should make the meaningful change obvious.

If a reviewer cannot easily tell what changed because the file was reformatted, the work should be revised or split into separate semantic and formatting commits.
