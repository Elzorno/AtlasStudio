# Atlas Graph Overview

## Purpose

The Atlas Graph is the shared memory layer for AtlasStudio.

Markdown documents explain the project to humans. The Atlas Graph connects the project for agents.

It records structured relationships between world canon, production work, agents, engine bridges, and build readiness.

## What The Graph Solves

AI agents are good at reading documents, but they repeatedly spend context and time rediscovering relationships.

The graph makes those relationships explicit.

Instead of asking an agent to infer that Rowan knows about the Hidden Cave because a paragraph says so, the graph records:

```text
character.rowan KNOWS_ABOUT location.hidden_cave
```

Instead of asking an agent to infer that the First Relay unlocks Rustshore Lighthouse, the graph records:

```text
infrastructure.first_relay UNLOCKS location.rustshore_lighthouse
```

## Design Goals

The Atlas Graph should be:

- Human-readable
- Git-friendly
- Easy for agents to edit
- Validatable
- Queryable
- Engine-independent at the canon layer
- Extendable to production tracking and engine bridges

## Not A Replacement For Markdown

The graph does not replace design documents.

Markdown remains the best place for:

- Narrative explanation
- Design rationale
- Tone and intent
- Human review
- Long-form creative work

The graph is best for:

- Entities
- Relationships
- Dependencies
- Ownership
- Queryable facts
- Agent handoff
- Consistency checks

## Initial Layers

```text
Atlas Graph
  Canon Graph
    World
    Regions
    Locations
    Characters
    Factions
    Quests
    Story Beats
    Ancient Infrastructure
    Monsters

  Production Graph
    Work Orders
    Agents
    Providers
    Builds
    Reviews
    QA Findings

  Bridge Graph
    Engine Bridges
    Implementation Targets
    Generated Assets
    Ownership States
```

## v0 Storage Decision

Atlas Graph v0 should be stored as versioned files in Git.

Preferred starting format:

```text
projects/<project-id>/graph/nodes/*.json
projects/<project-id>/graph/edges/*.json
```

This keeps the graph simple, reviewable, and compatible with any AI agent or local tool.

A future version may migrate to SQLite, DuckDB, Neo4j, or another graph-aware store, but v0 should avoid infrastructure complexity.

## Core Principle

If a relationship matters to story, gameplay, implementation, QA, or agent coordination, it should eventually exist in the graph.
