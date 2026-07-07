# Provider Registry

Providers describe who or what can supply capabilities.

Examples:

- GPT
- Claude Code
- Codex
- GitHub Copilot
- Ollama
- Human

## Registry Direction

Each provider should eventually have a JSON definition with:

- id
- name
- provider_type
- cloud or local status
- capabilities supplied
- confidence by capability
- cost class
- strengths
- avoid_when notes

## Human Provider

The human creator should be represented as a provider for capabilities that require final approval, creative direction, scope control, risk acceptance, or final canon authority.
