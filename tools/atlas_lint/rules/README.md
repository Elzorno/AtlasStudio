# Canon Lint Rules

Canon Linter rules are JSON metadata so agents can extend deterministic design QA without rewriting the linter.

Each rule includes:

- `id`: stable rule identifier.
- `category`: one of Structure, Completeness, Consistency, Coverage, Production, or Bridge.
- `severity`: `info`, `warning`, or `error`.
- `description`: human-readable purpose.
- `kind`: evaluator type used by `canon_lint.py`.
- `target_types`: node types the rule applies to.
- `applicable_statuses`: node statuses included by the rule.

Supported `kind` values:

- `required_relationship`: target nodes must have a matching incoming, outgoing, or either-direction edge.
- `duplicate_name_within_type`: names must be unique within a node type.
- `production_coverage`: canon nodes should have production work order coverage.
- `implementation_coverage`: canon nodes should have bridge or implementation mapping coverage.

Rules are check-only. They report design QA findings and do not modify graph data.
