# Atlas Academy Composition Rubric

## Status

Composition-only. This rubric operationalizes `academy/composition-analysis.md`'s ten topics into a checkable form; it does not combine composition with passability, metrics, or project fit into one overall recommendation - that multi-category combination is `work-orders/WO-2005-map-grading-system.md`'s scope. `WO-2005`'s own brief already lists "composition" as one of several categories its fuller grading model will assemble; this document is what that category's own check consists of.

## Purpose

`academy/grading-rubric.md` (`WO-2000`) states foundation-level Accepted/Rejected eligibility for an Academy case study, reusing `PLAYTEST_AND_ACCEPTANCE.md`'s outcome vocabulary. It does not check composition specifically. This rubric fills that gap: a repeatable checklist for whether a map's composition works, so a reviewer can point at a specific topic and a specific reason rather than reaching for "it doesn't feel right" - directly answering `WO-2002`'s own Success Criteria.

## How to Use This Rubric

For each of the ten topics below, record one of three verdicts against the room or screen under review:

- **Holds** - the topic's "What to check" question is answered affirmatively, with a cited reason.
- **Gap** - the topic's check fails, with a specific, falsifiable reason (per `academy/curriculum.md` Level 3's diagnostic standard - "the counter placement felt cramped" is not acceptable; "the counter's interaction side has zero adjacent walkable tiles" is).
- **N/A** - the topic does not apply to this room (for example, Room Zones does not apply to a single-room building whose governing pattern's `Required Conditions` do not call for zoning - see `academy/composition-analysis.md`, Topic 6).

A verdict of Gap should always name which cited pattern, research-doc claim, or project canon fact (`LOC-ASH-001`, an implementation packet, etc.) the finding traces back to, matching `academy/composition-rubric.md`'s parent framework's own evidence-citation discipline - an ungrounded Gap is not usable downstream.

## The Checklist

```text
□ 1. Focal Point
    Exactly one primary focal point, reachable within a short read
    time from the entrance. Two+ competing focal points, or zero, is
    a Gap.

□ 2. Negative Space
    Every open-floor region has a stated purpose (path, browsing
    zone, atmosphere). Unstated open floor is a Gap; stated open
    floor, however large, is not.

□ 3. Traffic Flow
    The visible composition (aisle width, furniture edges, door
    alignment) predicts the actual reachable set from spawn. A
    mismatch between what composition implies and what an
    observation record's walkable_tiles entry shows is a Gap.

□ 4. Sight Lines
    From the entry tile, the unobstructed view communicates the
    room's purpose. A view that hides the room's purpose behind
    obstruction on entry is a Gap.

□ 5. Furniture Grouping
    Every furniture cluster's grouping logic is statable in one
    sentence. A cluster mixing unrelated object types without
    narrative reason is a Gap. Confirm the correct pattern's
    anchoring convention was applied (wall-anchored for
    display/storage per shop.pattern.md/house.pattern.md; scattered
    islands for social/seating per bar.pattern.md) - applying the
    wrong convention to a room's actual function is itself a Gap,
    not a style choice.

□ 6. Room Zones
    N/A for a single-zone room. For a multi-zone room: zones connect
    via a deliberate chokepoint, not an open boundary. An open
    boundary between zones that should read as distinct is a Gap.

□ 7. Entry Readability
    Synthesis check, not independent of 1/3/4: within the room's
    short read time, a first-time viewer could state the room's
    purpose and primary route. If Topics 1, 3, and 4 all Hold but
    entry readability still fails, record why explicitly - that
    combination is itself informative.

□ 8. Visual Hierarchy
    A viewer can name, in order, what they notice first, second,
    third. Elements competing equally for attention (the research
    doc's "over-decoration" anti-pattern) is a Gap.

□ 9. Decoration Balance
    Decoration density reads as intentional for this room's function,
    checked against the closest-fitting pattern's own stated density
    (a shop denser than a house; a bar denser still). Copying one
    pattern's density onto a functionally different room is a Gap.

□ 10. Environmental Storytelling
    The room's use, ownership, and recent history are readable from
    composition alone, without dialogue. For an Ashford interior
    specifically: does it carry LOC-ASH-001's required "warm,
    ordinary, quietly strange" tone, or does it read as generic? A
    generic read is a Gap even if every other topic Holds.
```

## Worked Example: Why This Rubric Would Not Fully Diagnose the Map026 Rejection

The real, current rejection of Ashford Inn's first build pass (`map_ownership.json`, `Map026`, rejected 2026-07-08: "interior tiles are incorrect; rocks appear in the room; sofa/furniture rendering is poor") is a useful test of this rubric's actual boundaries, run here honestly rather than force-fit into a clean composition verdict:

- **"Rocks appear in the room"** and **"interior tiles are incorrect"** describe wrong tile/asset selection - a `tile_usage`-category finding per `schemas/academy-observation.schema.json` (`WO-2001`), not a composition topic this rubric checks. This rubric would not have caught this on its own; an Observation Engine pass checking tile usage against the intended tileset family would.
- **"Sofa/furniture rendering is poor"** partially engages Topic 5 (Furniture Grouping) and Topic 9 (Decoration Balance) - but "rendering is poor" as stated is closer to an asset-quality complaint than a grouping-logic or density complaint this rubric is built to check. Whether the sofa's *placement* was also a compositional Gap (wrong cluster, wrong room, wrong density for a free-rest inn per `IMP-HOM-020`) cannot be determined from the one-line rejection reason alone - no observation record or fuller build report exists yet for this build.

**Conclusion, stated plainly:** this rubric alone would not have fully explained the Map026 rejection, and this document does not claim it would. See `reports/academy/composition-analysis-framework.md` for the fuller treatment of why a rejection can span multiple Academy categories at once, and why that is a finding about Academy's own scope boundaries, not a weakness to paper over.

## References

- `academy/composition-analysis.md` - the ten topics this rubric checks.
- `academy/grading-rubric.md` - the foundation-level Accepted/Rejected eligibility this rubric operates alongside, not in place of.
- `academy/curriculum.md` - Level 3's diagnostic standard, applied to every Gap verdict here.
- `schemas/academy-observation.schema.json` - the `tile_usage` category this rubric explicitly does not cover.
- `reports/academy/composition-analysis-framework.md`
- `work-orders/WO-2005-map-grading-system.md` - the future work order this rubric's composition category feeds into.
- Created by `work-orders/WO-2002-composition-analysis-framework.md`
