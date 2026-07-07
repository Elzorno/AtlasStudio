# Atlas Planning Engine

Planning Engine v1 recommends next work without creating it.

Run:

```bash
python3 tools/atlas_planner/planner.py
python3 tools/atlas_planner/planner.py --project the-last-sword-protocol
python3 tools/atlas_planner/planner.py --output reports/atlas-planner/latest.md
```

The planner reads:

- Atlas Graph production/canon/bridge data.
- Work order Markdown frontmatter.
- Studio Doctor health signals.
- Canon Linter findings.

Recommendations are deterministic. Each recommendation includes component scores for milestone impact, dependency value, technical debt, player value, and core platform value, plus evidence and suggested agents. The planner never creates work orders automatically.
