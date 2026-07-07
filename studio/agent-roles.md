# Agent Roles

AtlasStudio assumes that different AI systems are better suited to different kinds of work. The goal is not to make every agent do everything. The goal is to assign the right work to the right agent.

## Human Creator

Role: Executive Producer and final creative authority.

Owns:

- Final approval
- Creative taste
- Scope decisions
- Playtest feedback
- Priority calls
- Project direction

## AtlasStudio

Role: Director and coordinator.

Owns:

- Canon
- Work orders
- Agent assignments
- Acceptance tests
- QA gates
- Build readiness
- Cross-agent memory

AtlasStudio should not directly implement engine-specific content unless the work order explicitly says so.

## GPT

Role: Creative systems designer.

Best for:

- Story design
- Quest structure
- Dialogue
- NPC concepts
- Region planning
- Player experience
- Pacing
- Teaching real-world cybersecurity concepts through fantasy metaphors

Avoid assigning GPT:

- Large code refactors
- Raw RPG Maker JSON editing
- Repetitive boilerplate

## Claude Code

Role: Senior software architect and refactoring specialist.

Best for:

- Tool architecture
- Repository structure
- Exporter/importer design
- Test design
- Complex refactors
- Long-form implementation reasoning
- Design-to-code translation plans

Avoid assigning Claude Code:

- Small repetitive edits
- Minor copy updates
- Tasks that do not require architectural judgment when quota is limited

## Codex

Role: Implementation engineer.

Best for:

- RPG Maker implementation
- Python scripts
- JavaScript plugins
- JSON transformations
- Build automation
- Tests and audits
- Applying work orders to a codebase

Avoid assigning Codex:

- Open-ended story invention without concrete constraints
- Final creative judgment

## GitHub Copilot

Role: Local coding assistant.

Best for:

- Autocomplete
- Boilerplate
- Small edits
- In-editor implementation support
- Repetitive code patterns

Avoid assigning Copilot:

- High-level architecture
- Canon decisions
- Multi-file production planning without supervision

## Ollama / Local Models

Role: Low-cost support agent.

Best for:

- Long-running review
- Draft critique
- Consistency checks
- Summaries
- Low-risk scaffolding
- Offline brainstorming

Avoid assigning local models:

- Final canon decisions
- High-risk implementation unless reviewed
- Tasks requiring strongest reasoning

## Assignment Factors

AtlasStudio should consider:

- Task type
- Agent strength
- Required context depth
- Risk level
- Session/quota availability
- Need for creativity vs implementation
- Whether output is reversible
- Whether work touches hand-authored content
