---
work_order_id: WO-2003
title: Map Metrics Framework
status: proposed
priority: future
phase: Atlas Academy
recommended_agent: codex
risk_level: medium
player_facing: false
---

# WO-2003 - Map Metrics Framework

## Objective

Design the measurable map metrics that Atlas Academy should eventually compute from RPG Maker map data and screenshots.

## Purpose

AtlasStudio should support map review with repeatable measurements where possible.

## Example Metrics

- walkable percentage
- blocked percentage
- event density
- decoration density
- empty floor ratio
- average aisle width
- door-to-focal-point distance
- furniture cluster count
- transfer count
- room-zone count
- map edge usage

## Deliverables

Create:

- `academy/metrics/README.md`
- `academy/map-metrics.md`
- `schemas/academy-map-metrics.schema.json`
- `reports/academy/map-metrics-framework.md`
- `work-orders/WO-2003-map-metrics-framework.md`

## Constraints

Documentation and schema only.

Do not implement code unless explicitly approved in a later work order.

Do not modify Atlas.

Do not modify TheLastSwordProtocol-Game.

Do not create maps.

Preserve Immutable Formatting Rule.

## Success Criteria

A future analyzer can compute consistent metrics for accepted maps, rejected maps, and official reference maps.
