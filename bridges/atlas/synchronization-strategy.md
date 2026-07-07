# Atlas Synchronization Strategy

## Purpose

This document describes how AtlasStudio should keep its imported entity cache (`imported-entity-model.md`) aligned with `TheLastSwordProtocol-Atlas` over time, without ever silently merging a change or treating a report as a decision. Per `import-architecture.md`'s governing constraint, synchronization only ever flows downhill: Atlas changes, AtlasStudio's cache is updated to reflect it, and AtlasStudio reports what changed. AtlasStudio never pushes a synchronization change back upstream automatically.

## First Import

The first import establishes the baseline:

1. Discover the newest `atlas-exports/*.json` (or, for entities the export does not cover, read the secondary sources listed in `import-architecture.md`).
2. Parse and normalize every discoverable entity into the shapes defined in `imported-entity-model.md`.
3. Stamp every entity with `imported_version: 1` and the current `imported_at` timestamp.
4. Record the source commit (`source_commit`) the baseline was taken from.
5. Produce a first-import report: total entities imported, grouped by `kind`, plus any parse failures encountered (reported, never silently dropped).

No conflict detection runs against a first import, since there is no prior state to compare against - conflict detection begins at the first *re*-import.

## Incremental Updates

Every subsequent import compares the newly discovered/parsed state against the existing cache, entity by entity, keyed by `source_identifier`:

- **Unchanged entity:** no action. `imported_version` does not increment for a no-op re-import (an unchanged entity re-imported is not "new information," and inflating its version would make the version number meaningless as a change signal).
- **Changed entity:** the cache entry is replaced with the new state, `imported_version` increments, and the change is reported field-by-field (old value -> new value), reusing the same before/after reporting shape AtlasStudio's existing Graph Diff Engine already produces for its own graph (`tools/atlas_graph/diff_graph.py`) - a deliberate consistency choice, not a coincidence, since a future `atlas_diff.py` (see "Future Tooling") should be able to reuse that engine's comparison logic directly against the imported cache's JSON shape.
- **New entity:** added to the cache at `imported_version: 1`, reported as newly discovered.

## Conflict Reporting

Per `import-architecture.md`'s Conflict Detection section, any of the following produces a report entry, never an automatic resolution:

- A cross-source disagreement (export says one thing, a directly-read frontmatter file says another).
- A schema version the importer does not recognize - this halts import for the affected source entirely, rather than guessing at a mapping.
- An ownership contradiction between an Atlas screen's `rpg_maker_map_name` and the actual game repository's map data.

A conflict report always names: the entity's `source_identifier`, what disagreed, which sources disagreed, and the exact fields involved. It never includes an automatic recommendation to prefer one source over another - that judgment belongs to a human, exactly as `WO-0018`'s own conflict analysis had to be judged by a human rather than resolved by AtlasStudio unilaterally.

## Deleted Source Items

If a previously-imported `source_identifier` is no longer discoverable in Atlas (removed, retired, or superseded by an ID change Atlas's own Canonical ID Registry does not track as a rename):

- The cache entry is **not deleted automatically**. It is marked `source_status: not_found_at_last_sync` with the timestamp of the sync that first failed to find it.
- This is reported prominently, since a disappearing entity in the authoritative repository is exactly the kind of signal a human should see before any dependent AtlasStudio work (a bridge handoff, a scheduling recommendation) continues to reference it.
- A human or an explicitly-scoped follow-up import may confirm the deletion and purge the stale cache entry - the importer itself never does this silently.

## Renamed Items

Per the Canonical ID Registry's own rule ("IDs are stable, names can change"), a renamed entity is detected as: same `source_identifier`, different `title` (or other non-ID field). This is treated as a normal incremental update (see above), reported as a title change, and is explicitly **not** treated as a deletion-plus-new-entity pair - the stable ID is what continuity is judged against, matching Atlas's own stated rule rather than inventing a different one.

If an actual ID change occurs (rare, and against Atlas's own stated practice), it cannot be distinguished from a deletion-plus-new-entity by AtlasStudio's importer alone - this should be reported as an ambiguous case requiring human confirmation, not guessed at via fuzzy title matching.

## Reporting, Never Merging

Every synchronization run produces a single, human-readable synchronization report (not an automatic action) covering: entities added, entities changed (with field-level detail), entities flagged `not_found_at_last_sync`, and any conflicts detected. This report is the deliverable of a sync run. AtlasStudio's cache reflects Atlas's current state after a sync completes, but no downstream AtlasStudio process (planning, scheduling, bridge handoff) should silently trust a changed entity without that report being visible to whoever is relying on it - consistent with `studio/governance/atlas-principles.md`'s "planning should be explainable" principle, extended here to synchronization.

## Synchronization Cadence

This document does not mandate a cadence (hourly, daily, per-work-order) - that is an operational decision for whoever builds the future tooling in "Future Tooling" below, informed by how often Atlas actually changes in practice. What it does mandate: synchronization is always an explicit, invokable action with a visible report, never a silent background process a human cannot see the result of.
