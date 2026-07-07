# Capability Registry

Capabilities describe what a work order needs.

Providers supply capabilities.

AtlasStudio should reason about capabilities before selecting providers.

## Initial Capability Examples

- architecture-review
- python-development
- creative-writing
- graph-analysis
- schema-design
- documentation
- qa-review
- rpg-maker-json
- canon-design
- human-approval

## Registry Direction

Each capability should eventually have a JSON definition with:

- id
- name
- description
- category
- typical deliverables
- risk notes
- useful verification signals
