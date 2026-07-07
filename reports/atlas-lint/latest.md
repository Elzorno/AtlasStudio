# Atlas Canon Lint Report

Project: `the-last-sword-protocol`
Generated: 2026-07-07

## Summary

- Graph: `projects/the-last-sword-protocol/graph`
- Nodes: 36
- Edges: 43
- Canon nodes: 14
- Rules loaded: 12
- Structural errors: 0
- Findings: 18

## Severity Counts

- info: 18

## Category Counts

- Bridge: 7
- Production: 11

## Structural Graph Errors

- None.

## Structure

- No findings.

## Completeness

- No findings.

## Consistency

- No findings.

## Coverage

- No findings.

## Production

- INFO `character.elara` (character): character.elara is not connected to a creating or modifying work order.
  - Rule: `production.canon_has_work_order_edge`
- INFO `character.rowan` (character): character.rowan is not connected to a creating or modifying work order.
  - Rule: `production.canon_has_work_order_edge`
- INFO `concept.access_control` (concept): concept.access_control is not connected to a creating or modifying work order.
  - Rule: `production.canon_has_work_order_edge`
- INFO `concept.authentication` (concept): concept.authentication is not connected to a creating or modifying work order.
  - Rule: `production.canon_has_work_order_edge`
- INFO `infrastructure.first_relay` (infrastructure): infrastructure.first_relay is not connected to a creating or modifying work order.
  - Rule: `production.canon_has_work_order_edge`
- INFO `item.last_sword` (item): item.last_sword is not connected to a creating or modifying work order.
  - Rule: `production.canon_has_work_order_edge`
- INFO `location.ashford_village` (location): location.ashford_village is not connected to a creating or modifying work order.
  - Rule: `production.canon_has_work_order_edge`
- INFO `location.glassfield_ruins` (location): location.glassfield_ruins is not connected to a creating or modifying work order.
  - Rule: `production.canon_has_work_order_edge`
- INFO `location.hidden_cave` (location): location.hidden_cave is not connected to a creating or modifying work order.
  - Rule: `production.canon_has_work_order_edge`
- INFO `location.rustshore_dock` (location): location.rustshore_dock is not connected to a creating or modifying work order.
  - Rule: `production.canon_has_work_order_edge`
- INFO `location.sword_shrine` (location): location.sword_shrine is not connected to a creating or modifying work order.
  - Rule: `production.canon_has_work_order_edge`

## Bridge

- INFO `infrastructure.first_relay` (infrastructure): infrastructure.first_relay has no bridge or implementation mapping edge yet.
  - Rule: `bridge.canon_has_implementation_signal`
- INFO `location.ashford_village` (location): location.ashford_village has no bridge or implementation mapping edge yet.
  - Rule: `bridge.canon_has_implementation_signal`
- INFO `location.glassfield_ruins` (location): location.glassfield_ruins has no bridge or implementation mapping edge yet.
  - Rule: `bridge.canon_has_implementation_signal`
- INFO `location.hidden_cave` (location): location.hidden_cave has no bridge or implementation mapping edge yet.
  - Rule: `bridge.canon_has_implementation_signal`
- INFO `location.rustshore_dock` (location): location.rustshore_dock has no bridge or implementation mapping edge yet.
  - Rule: `bridge.canon_has_implementation_signal`
- INFO `location.sword_shrine` (location): location.sword_shrine has no bridge or implementation mapping edge yet.
  - Rule: `bridge.canon_has_implementation_signal`
- INFO `region.ashford_vale` (region): region.ashford_vale has no bridge or implementation mapping edge yet.
  - Rule: `bridge.canon_has_implementation_signal`

## Recommendation

- Treat warnings as design QA prompts; revise canon through approved work orders only.

