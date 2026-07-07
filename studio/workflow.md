# AtlasStudio Workflow

AtlasStudio uses a director-led, work-order-driven workflow.

## Production Loop

```text
Human intent
  ↓
AtlasStudio interprets direction
  ↓
AtlasStudio updates canon or project model
  ↓
AtlasStudio identifies affected areas
  ↓
AtlasStudio creates work orders
  ↓
Work orders are assigned to agents
  ↓
Agents produce deliverables
  ↓
AtlasStudio validates against acceptance tests
  ↓
Human reviews playable results
  ↓
AtlasStudio records decisions and next work
```

## Work Order Lifecycle

1. Proposed
2. Approved
3. Assigned
4. In Progress
5. Submitted
6. QA Review
7. Needs Revision
8. Accepted
9. Closed

## Work Order Rules

Every work order must include:

- A player-facing goal
- Scope boundaries
- Assigned agent or recommended agent
- Required inputs
- Deliverables
- Acceptance criteria
- Files allowed to change
- Files or systems that must not be changed
- Verification steps

## Canon Change Rule

A work order may not silently change canon.

If implementation reveals that canon needs to change, the agent must request a canon revision. AtlasStudio then records the decision before implementation proceeds.

## Engine Bridge Rule

AtlasStudio project documents should stay engine-independent unless they are inside an engine bridge folder.

For The Last Sword Protocol, RPG Maker MZ implementation details belong in an RPG Maker bridge, not in the core story or world model.

## Ownership Rule

Generated content may be regenerated. Hand-authored content must be protected.

Any implementation bridge must track whether maps, events, assets, or files are:

- generated
- agent-drafted
- human-edited
- hand-authored
- locked

## Quality Rule

A build is not complete because the file exists.

A build is complete when:

1. It can be verified.
2. It improves the player experience.
3. It does not break canon.
4. It does not overwrite protected work.
5. The next agent can understand what happened.
