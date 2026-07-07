# Atlas Graph Node Types

## Node ID Convention

Node IDs should be stable, lowercase, and namespaced.

Examples:

```text
world.elyndor
region.ashford_vale
location.ashford_village
character.rowan
quest.j1_hidden_cave
work_order.wo_0003
agent.claude_code
bridge.rpg_maker_mz
```

## Common Node Fields

Every node should include:

```json
{
  "id": "region.ashford_vale",
  "type": "region",
  "name": "Ashford Vale",
  "status": "draft",
  "project": "the-last-sword-protocol",
  "summary": "Starting region for Journey I.",
  "source": ["projects/the-last-sword-protocol/home-region.md"]
}
```

## Canon Node Types

### world

Represents the game world or major world-scale setting.

Examples:

- `world.elyndor`

### region

A major explorable area of the world.

Examples:

- `region.ashford_vale`
- `region.iron_marches`
- `region.whisperwood`

### location

A specific place within a region.

Examples:

- `location.ashford_village`
- `location.hidden_cave`
- `location.rustshore_dock`

### settlement

A location subtype for towns, villages, castles, camps, and ports.

Can be represented as `type: location` with `subtype: settlement` unless implementation needs a separate type.

### dungeon

A location subtype for caves, towers, ruins, mines, shrines, and other adventure sites.

Can be represented as `type: location` with `subtype: dungeon` unless implementation needs a separate type.

### character

A named person or recurring individual.

Examples:

- `character.hero`
- `character.elara`
- `character.rowan`

### faction

A group, institution, political force, or ideology.

Examples:

- `faction.keepers`
- `faction.wardens`
- `faction.covenant_of_ash`

### quest

A player-facing objective chain.

Examples:

- `quest.j1_find_hidden_cave`
- `quest.j1_restore_first_relay`

### story_beat

A narrative moment or progression beat.

Examples:

- `story_beat.sword_authenticates_hero`
- `story_beat.rustshore_lighthouse_awakens`

### infrastructure

Ancient system components interpreted as fantasy ruins or magic.

Examples:

- `infrastructure.first_relay`
- `infrastructure.heart_archive`
- `infrastructure.signal_gate_ashford`

### monster_family

A reusable enemy family.

Examples:

- `monster_family.gel`
- `monster_family.construct`
- `monster_family.wraith`

### item

Important world or gameplay objects.

Examples:

- `item.last_sword`
- `item.protocol_medallion`

### concept

A design or metaphor concept.

Examples:

- `concept.authentication`
- `concept.access_control`
- `concept.archive_recovery`

## Production Node Types

### work_order

A unit of production work.

Examples:

- `work_order.wo_0002`
- `work_order.wo_0007`

### agent

An AI or human production role.

Examples:

- `agent.gpt`
- `agent.claude_code`
- `agent.codex`
- `agent.github_copilot`
- `agent.human`

### provider

A specific model or platform provider.

Examples:

- `provider.openai`
- `provider.anthropic`
- `provider.github_copilot`
- `provider.ollama`

### build

A playable or verifiable project state.

Examples:

- `build.atlasstudio_0001`
- `build.lsp_home_region_prototype_0001`

### tool

A production support script or utility that helps agents validate, query, export, or inspect project data.

Examples:

- `tool.atlas_graph_validator`
- `tool.atlas_graph_query`

### qa_finding

A review or validation result.

Examples:

- `qa_finding.missing_home_region_secret`

## Bridge Node Types

### bridge

An engine or platform translation layer.

Examples:

- `bridge.rpg_maker_mz`

### implementation_target

A concrete implementation artifact in an engine-specific repository.

Examples:

- `implementation_target.rpgmaker.home_region_overworld_map`

### ownership_state

Represents whether something is generated, agent-drafted, human-edited, hand-authored, or locked.
