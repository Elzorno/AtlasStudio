# Atlas Canon Linter

The Canon Linter is deterministic Level 3 Atlas QA. It checks whether graph canon is coherent enough for agents to build on, without modifying graph data.

Run:

```bash
python3 tools/atlas_lint/canon_lint.py --project the-last-sword-protocol
python3 tools/atlas_lint/canon_lint.py --project the-last-sword-protocol --output reports/atlas-lint/latest.md
```

Rules live in `tools/atlas_lint/rules/canon_lint_rules.json`.

The first rule categories are:

- Structure: required place and containment relationships.
- Completeness: expected design hooks such as character appearances and quest progression.
- Consistency: duplicate names or conflicting facts that can be checked deterministically.
- Coverage: whether design concepts are represented in gameplay/world facts.
- Production: whether canon is connected to work orders.
- Bridge: whether implementation-ready canon has bridge mapping signals.

Warnings are design QA prompts. The linter does not alter canon and does not fail on warnings unless `--fail-on-warning` is passed.
