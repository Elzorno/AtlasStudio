---
work_order_id: WO-2004
title: Reference Library Governance
status: proposed
priority: future
phase: Atlas Academy
recommended_agent: claude_code
risk_level: low
player_facing: false
---

# WO-2004 - Reference Library Governance

## Objective

Define how Atlas Academy stores and classifies reference sources.

## Purpose

Not every reference map should have equal weight. AtlasStudio needs a governed reference library with provenance, scope, confidence, and allowed-use rules.

## Source Classes

- official RPG Maker sample maps
- approved project maps
- rejected project maps
- design references
- comparative JRPG references

## Deliverables

Create:

- `academy/references/reference-governance.md`
- `academy/references/source-classes.md`
- `academy/references/gold-standard-maps.md`
- `schemas/academy-reference-source.schema.json`
- `work-orders/WO-2004-reference-library-governance.md`

## Required Content

Define:

- source provenance
- approval status
- confidence contribution
- licensing notes
- citation rules
- accepted versus rejected project maps
- gold-standard map criteria
- when a reference can influence implementation contracts

## Constraints

Documentation and schema only.

Do not modify Atlas.

Do not modify TheLastSwordProtocol-Game.

Do not copy external maps.

Do not create maps.

Preserve Immutable Formatting Rule.

## Success Criteria

AtlasStudio can distinguish high-quality references, accepted project maps, rejected case studies, and experimental examples without mixing their authority levels.
