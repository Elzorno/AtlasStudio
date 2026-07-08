# Design Pattern Library

## Purpose

The Design Pattern Library captures reusable environment-design knowledge extracted from official RPG Maker sample maps and, over time, from AtlasStudio's own accepted builds.

It exists because reverse-engineering an official sample map once (see `reports/map-analysis/item-shop-analysis.md` in `TheLastSwordProtocol-Game`) is only useful if the lessons survive past that one report. Without a permanent library, every future shop, house, or dungeon interior would either re-derive the same lessons from scratch or, worse, invent layout conventions with no grounding in what official RPG Maker content actually does. The library turns one-off analysis into standing, citable design principles.

This work order (`WO-0024`) creates the framework only. It defines the schema, the extraction method, the confidence model, and the review process, and seeds the library with exactly one pattern (`interiors/shop.pattern.md`). Populating the rest of the library - houses, inns, dungeons, overworld towns, and so on - is future work under future work orders.

## Relationship to Atlas

`TheLastSwordProtocol-Atlas` remains the sole source of narrative and world-design canon: what a location is, why it exists, what happens there, and what an implementation packet must accomplish. The Design Pattern Library does not compete with Atlas and does not decide *what* to build.

The library answers a different question: *given* that Atlas has already specified a shop, a house, or a dungeon room, what does a well-built RPG Maker version of that space look like? Patterns describe reusable spatial and compositional technique - door placement, aisle width, shelf-to-wall discipline, object clustering - never story content, dialogue, item lists, or quest logic. If a pattern and Atlas ever appear to disagree, Atlas wins; the pattern is describing craft, not truth.

## Relationship to AtlasStudio

The library lives under `studio/` alongside AtlasStudio's other standing references (`studio/agent-roles.md`, `studio/governance/`, `bridges/rpg-maker-mz/`). It is AtlasStudio-owned production knowledge, not Atlas canon and not Game-repo content. Like `bridges/rpg-maker-mz/map-quality-standard.md` and `bridges/rpg-maker-mz/passability-rule.md`, it is a standing rule set that AtlasStudio maintains and that implementation contracts are expected to cite.

The library is versioned and reviewed the same way other AtlasStudio standing documents are: through work orders, with the Immutable Formatting Rule preserved, and without silently rewriting accepted patterns (see `PATTERN_REVIEW_PROCESS.md`).

## Relationship to Implementation Contracts

Implementation contracts (`reports/implementation-contracts/*.md`, e.g. `ashford-shop-build-contract.md`) already cite authoritative Atlas sources, exact Game-repo targets, ownership restrictions, and passability requirements. The Design Pattern Library adds one more citable input: a named, versioned, confidence-rated pattern that tells the implementing agent *how* to lay the space out well, in addition to *what* Atlas requires it to contain.

A future contract should reference a pattern the same way it references a packet or a screen object - by name and version, not by paraphrase:

```text
Apply: Interior Pattern - Shop v1.0
Confidence: High
```

See "Future Integration" below and `PATTERN_REVIEW_PROCESS.md` for exactly what that reference commits an implementing agent to.

Patterns never replace implementation packets. A packet still defines what a specific screen must contain (which NPC, which transfers, which inventory); a pattern defines how to build the general shape of that kind of space well. A contract that cites a pattern but no packet is incomplete; a packet without a citable pattern is still valid, just less informed.

## Relationship to RPG Maker

Every pattern in this library is derived from **official RPG Maker sample/demo map data** - the same reference material already used in `reports/rpg-maker-bridge/sample-project-analysis.md` and `reports/map-analysis/item-shop-analysis.md`. Patterns capture layout principles, spatial relationships, and composition technique observed in that official data. They do not, and must not, reproduce the sample maps themselves.

The library stores *design principles*, not tile grids, not JSON exports, and not screenshots-as-blueprints. This is both a legal boundary (official RPG Maker sample content is not AtlasStudio's or Atlas's to redistribute as game data) and a design boundary (a principle generalizes across many maps; a copied layout does not). See the Rules section below and `PATTERN_EXTRACTION_GUIDE.md` for how to observe a sample map without copying it.

## Directory Layout

```text
studio/design-patterns/
  README.md                      - this file
  PATTERN_SCHEMA.md               - the standard pattern format
  PATTERN_EXTRACTION_GUIDE.md     - how to analyze an official sample map
  PATTERN_CONFIDENCE_MODEL.md     - how confidence levels work and evolve
  PATTERN_REVIEW_PROCESS.md       - propose / review / accept / deprecate / version
  interiors/
    shop.pattern.md               - first pattern: Interior Pattern - Shop v1.0
  (future categories: exteriors/, dungeons/, towns/, transitions/, ...)
```

## Rules

- The pattern library stores principles. It never copies maps.
- It never stores copyrighted layouts, tile-for-tile grids, or verbatim exports from official RPG Maker sample data.
- It never replaces implementation packets or screen objects - it supplements them with reusable craft knowledge.
- Every pattern always references its authoritative source (the sample map(s) it was observed in, and the AtlasStudio report that performed the extraction).

## Future Integration

Implementation contracts should reference a pattern by name and version, and state the confidence level at reference time (confidence can change between when a pattern was written and when it is applied - see `PATTERN_CONFIDENCE_MODEL.md`):

```text
Apply: Interior Pattern - Shop v1.0
Confidence: Medium
```

An implementing agent reading that line should understand, without further explanation: which document to open (`interiors/shop.pattern.md`), which version of its rules applies (`v1.0`), how much authority those rules currently carry (`Medium` - observed once, in one official sample map; apply by default but flag it as single-source in the build report, per `PATTERN_CONFIDENCE_MODEL.md`), and that any required condition or common mistake listed in that pattern document applies to the current build unless the contract explicitly overrides it.

The confidence level cited in a contract must match the pattern document's current `confidence` field at the time the contract is written - it is not the contract author's judgment call to assign. Once a second official sample map corroborates `Shop v1.0`'s rules, its confidence is promoted to `High` (see `PATTERN_CONFIDENCE_MODEL.md`) and future contracts cite that instead.

## Success Criterion

A future implementation contract should be able to write `Apply Interior Pattern: Shop v1.0` and have an implementation agent understand exactly what that means - which document governs, what confidence it carries, and what rules it is now accountable to - without needing any further explanation from the contract author.
