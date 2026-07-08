---
work_order_id: WO-2001
title: Atlas Academy Observation Engine
status: proposed
priority: future
phase: Atlas Academy
recommended_agent: claude_code
risk_level: low
player_facing: false
---

# WO-2001 - Atlas Academy Observation Engine

## Objective

Design the observation model for map study.

The Observation Engine records factual map observations before any interpretation or grading occurs.

## Purpose

AtlasStudio should separate facts from conclusions.

Examples of observations:

- map dimensions
- door coordinates
- room zones
- event count
- walkable percentage
- furniture groups
- counter placement
- window count
- transfer locations

## Deliverables

Create:

- `academy/observation-model.md`
- `academy/observations/README.md`
- `schemas/academy-observation.schema.json`
- `work-orders/WO-2001-academy-observation-engine.md`

## Required Content

Define:

- observation fields
- evidence requirements
- source map provenance
- screenshot references
- JSON references
- distinction between objective and subjective notes
- how observations feed pattern extraction

## Constraints

Documentation and schema only.

Do not write analysis code.

Do not modify Atlas.

Do not modify TheLastSwordProtocol-Game.

Do not create or edit maps.

Preserve Immutable Formatting Rule.

## Success Criteria

A future tool or agent can record a map observation without mixing factual measurements with design judgment.
