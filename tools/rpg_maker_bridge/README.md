# RPG Maker Bridge Handoff Generator

This tool turns AtlasStudio First Playable Hour work packages into read-only RPG Maker MZ implementation handoff checklists.

It reads:

- `projects/the-last-sword-protocol/production/work-breakdown.md`
- `projects/the-last-sword-protocol/graph/`
- `bridges/rpg-maker-mz/bridge-design.md`
- `bridges/rpg-maker-mz/ownership-model.md`
- `bridges/rpg-maker-mz/handoff-format.md`

It does not read or write the RPG Maker game repository.

The bridge documents are loaded as inputs, including the handoff template sections and ownership states used by implementation checklists.

Run:

```bash
python3 tools/rpg_maker_bridge/handoff_generator.py
python3 tools/rpg_maker_bridge/handoff_generator.py --package WP-03
python3 tools/rpg_maker_bridge/handoff_generator.py --output reports/rpg-maker-bridge/wp-01-handoff-foundation.md
```

Unknown ownership is treated as protected until an implementation work order performs a read-only audit of the target RPG Maker project.
