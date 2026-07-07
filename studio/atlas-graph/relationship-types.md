# Atlas Graph Relationship Types

## Edge Convention

Edges describe relationships between nodes.

Recommended edge shape:

```json
{
  "id": "edge.000001",
  "from": "region.ashford_vale",
  "type": "CONTAINS",
  "to": "location.ashford_village",
  "status": "draft",
  "source": ["projects/the-last-sword-protocol/home-region.md"]
}
```

Relationship types should be uppercase verbs or verb phrases.

## Canon Relationships

### CONTAINS

A parent place contains a child entity.

Examples:

```text
world.elyndor CONTAINS region.ashford_vale
region.ashford_vale CONTAINS location.hidden_cave
```

### LOCATED_IN

Inverse of CONTAINS when useful.

```text
location.hidden_cave LOCATED_IN region.ashford_vale
```

### CONNECTED_TO

Two places are geographically connected.

```text
location.ashford_village CONNECTED_TO location.old_north_road
```

### BORDERS

Two regions share a border.

```text
region.ashford_vale BORDERS region.iron_marches
```

### APPEARS_IN

A character, faction, quest, or story beat appears in a journey, region, or location.

```text
character.rowan APPEARS_IN region.ashford_vale
```

### KNOWS_ABOUT

A character or faction has knowledge of something.

```text
character.rowan KNOWS_ABOUT location.hidden_cave
```

### MISUNDERSTANDS

A character or faction knows a concept incorrectly.

```text
character.rowan MISUNDERSTANDS infrastructure.first_relay
```

### OWNS

A faction, character, or system owns or controls something.

```text
faction.keepers OWNS location.archive_library
```

### SEEKS

A character or faction actively seeks an item, location, or concept.

```text
faction.covenant_of_ash SEEKS item.last_sword
```

### UNLOCKS

One entity unlocks access to another.

```text
infrastructure.first_relay UNLOCKS location.rustshore_lighthouse
```

### REQUIRES

A quest, location, or story beat requires another entity.

```text
quest.j1_restore_first_relay REQUIRES item.last_sword
```

### STARTS_AT

A quest starts at a character or location.

```text
quest.j1_find_hidden_cave STARTS_AT character.rowan
```

### REWARDS

A quest or story beat rewards an item, access, or state change.

```text
quest.j1_hidden_cave REWARDS item.last_sword
```

### TEACHES

A region, quest, dungeon, or event teaches a concept.

```text
location.sword_shrine TEACHES concept.authentication
```

### REPRESENTS

A fantasy element represents an underlying design or cybersecurity concept.

```text
item.last_sword REPRESENTS concept.authentication_token
```

### CORRUPTS

A force corrupts another entity.

```text
faction.covenant_of_ash CORRUPTS infrastructure.relay_node
```

## Production Relationships

### DEPENDS_ON

A work order, build, or implementation target depends on another.

```text
work_order.wo_0005 DEPENDS_ON work_order.wo_0007
```

### CREATES

A work order creates a node, document, build, or implementation target.

```text
work_order.wo_0007 CREATES graph.atlas_graph
```

### MODIFIES

A work order modifies an existing entity.

```text
work_order.wo_0003 MODIFIES region.ashford_vale
```

### ASSIGNED_TO

A work order is assigned to an agent.

```text
work_order.wo_0007 ASSIGNED_TO agent.claude_code
```

### REVIEWED_BY

A work order or build was reviewed by an agent or human.

```text
work_order.wo_0003 REVIEWED_BY agent.human
```

### VERIFIED_BY

A QA finding, test, or review verifies a work product.

```text
build.lsp_home_region_0001 VERIFIED_BY qa_finding.route_complete
```

### IMPLEMENTED_BY

A design entity is implemented by a bridge or implementation target.

```text
region.ashford_vale IMPLEMENTED_BY implementation_target.rpgmaker.ashford_vale_overworld
```

## Bridge Relationships

### TRANSLATES_TO

A canon node translates to an implementation target.

```text
location.ashford_village TRANSLATES_TO implementation_target.rpgmaker.map_ashford_village
```

### PROTECTED_BY

An implementation target is protected by an ownership rule.

```text
implementation_target.rpgmaker.map_ashford_village PROTECTED_BY ownership_state.hand_authored
```

### GENERATED_FROM

An implementation target or build artifact was generated from a design node, work order, or export.

```text
implementation_target.rpgmaker.home_region_overworld GENERATED_FROM region.ashford_vale
```

## Relationship Design Rule

If two agents might disagree about how two things relate, make the relationship explicit in the graph.
