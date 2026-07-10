# Composition Analysis Framework - Evidence Report

Status: submitted

Scope: `WO-2002`. Synthesizes the evidence behind `academy/composition-analysis.md`'s ten required topics (focal point, negative space, traffic flow, sight lines, furniture grouping, room zones, entry readability, visual hierarchy, decoration balance, environmental storytelling), and applies the framework, honestly and to the extent the available evidence supports, to the one real, current motivating case: Ashford Inn's rejected `Map026` build.

This report is analysis and evidence, not implementation guidance. It does not direct any build against `TheLastSwordProtocol-Game` or `TheLastSwordProtocol-Atlas`, and it does not modify either repository or any existing Design Pattern document.

## Why This Report Exists

`work-orders/WO-2002-composition-analysis-framework.md`'s own Purpose states: "Recent rejected maps showed that functional correctness is not enough. AtlasStudio needs a way to evaluate composition before implementation is accepted." That is not a hypothetical framing. `TheLastSwordProtocol-Game/map_ownership.json` records, as of this report's writing, a real rejection:

```json
"26": {
  "state": "hand_authored",
  "atlas_screen": "SCR-HOM-ASH-004",
  "name": "INT_Ashford_Inn",
  "notes": "Rejected Map026 Ashford Inn build pass. Preserve as hand_authored/protected until revisited; do not ship or treat as accepted.",
  "implementation_status": "rejected",
  "rejected_on": "2026-07-08",
  "rejection_reason": "Human review rejected this Map026 pass: interior tiles are incorrect; rocks appear in the room; sofa/furniture rendering is poor."
}
```

This is the Ashford Inn build authorized by `reports/implementation-contracts/ashford-inn-pattern-aware-contract.md` and `IMP-HOM-020` (`TheLastSwordProtocol-Atlas`, `WO-0044`; renumbered from a duplicate `WO-0038` slot). Its first pass was rejected the same day this Academy series began. This report treats that rejection as real evidence, not as a convenient hypothetical - and is equally careful not to overclaim what a one-line rejection reason actually proves.

## Evidence Sources

| Source | What it contributes |
|---|---|
| `studio/design-patterns/interiors/*.pattern.md` (`shop`, `house`, `inn`, `bar`, `chief-house`) | Each pattern's own `Composition Rules` section - primary, extraction-derived evidence, per `studio/design-patterns/PATTERN_EXTRACTION_GUIDE.md`. |
| `reports/design-patterns/interior-pattern-corpus-review.md` (`WO-0025`) | Cross-pattern findings - most importantly, that wall-anchoring is a display/storage-specific convention (`shop`, `house`) that `bar.pattern.md` correctly overrides, not a universal interior rule. |
| `reports/map-analysis/item-shop-analysis.md` (`TheLastSwordProtocol-Game`, read-only) | A full worked composition analysis of one official sample map - the concrete case every abstract topic in `academy/composition-analysis.md` is checked against. |
| `references/atlas_academy_jrpg_map_research.md` | A research synthesis spanning official RPG Maker guidance, Dragon Quest design commentary, and wayfinding/environmental-storytelling literature, explicitly self-tiered by confidence (observed fact / expert opinion / community opinion / research hypothesis). Cited at its own stated tier throughout, never upgraded. |
| `atlas/docs/02_World/Locations/Home_Island/Ashford.md` (`LOC-ASH-001`, `TheLastSwordProtocol-Atlas`, read-only) | The project's own canon tone requirement ("warm, lived-in, ordinary, and quietly strange") that environmental storytelling (Topic 10) must serve, not a generic aesthetic standard. |
| `TheLastSwordProtocol-Game/map_ownership.json` | The real, dated Map026 rejection this report treats as its motivating case. |

## Coverage Check: Every Required Topic Has Grounding

`academy/composition-analysis.md` cites specific, existing evidence for each of the ten topics `work-orders/WO-2002`'s brief requires (focal point, negative space, traffic flow, sight lines, furniture grouping, room zones, entry readability, visual hierarchy, decoration balance, environmental storytelling). No topic in that document rests on an invented claim with no citation - each references at minimum one of the pattern documents, the corpus review, the Item Shop analysis, or the JRPG research doc, at that source's own stated confidence.

One asymmetry worth stating plainly: some topics (furniture grouping, room zones, decoration balance) have deep, multi-source, extraction-derived evidence already in this project's own pattern corpus. Others (sight lines, entry readability) lean more heavily on the newer research doc's synthesis, since the existing pattern corpus does not independently corroborate them as extensively. This asymmetry is inherited honestly into `academy/composition-analysis.md`'s per-topic grounding rather than smoothed over - a future extraction pass specifically targeting sight-line and entry-readability evidence (per `academy/curriculum.md` Level 1) would strengthen the weaker half of this coverage.

## Applying the Framework to the Map026 Rejection

The rejection reason - "interior tiles are incorrect; rocks appear in the room; sofa/furniture rendering is poor" - is short, and this report resists the temptation to read more diagnostic detail into it than it actually states. Mapped against `academy/composition-rubric.md`'s ten-topic checklist and `schemas/academy-observation.schema.json`'s observation categories:

| Stated reason fragment | Best-fit category | In composition-rubric.md's scope? |
|---|---|---|
| "interior tiles are incorrect" | `tile_usage` (Observation Engine category, `WO-2001`) | No - this is an asset/tileset-selection fact, not a composition topic. |
| "rocks appear in the room" | `tile_usage` / possibly `structural_object` if "rocks" were placed as intentional (but wrong) objects | No, for the same reason - unless a future observation record shows the rocks were a deliberate but mis-themed furniture choice, in which case Topic 5 (Furniture Grouping) and Topic 10 (Environmental Storytelling - a rock in the room does not serve `LOC-ASH-001`'s "warm, ordinary" tone) would both apply. |
| "sofa/furniture rendering is poor" | Ambiguous between an asset-quality complaint (out of scope here) and Topics 5/9 (Furniture Grouping, Decoration Balance) if the complaint is about placement or density rather than rendering quality itself | Partially - cannot be resolved from the one-line reason alone. |

**Finding, stated as a finding, not smoothed over:** the Map026 rejection reason, as recorded, is predominantly an asset/tile-correctness failure that `academy/composition-analysis.md`'s ten topics do not primarily cover - `work-orders/WO-2001`'s Observation Engine (specifically its `tile_usage` category) is the more directly applicable Academy tool for most of what was actually stated. Composition analysis may be *partially* relevant (furniture placement, thematic fit) but cannot be confirmed as the primary failure mode without a fuller observation record or build report, neither of which currently exists for this build.

This is not a weakness in the composition framework - it is exactly the kind of scope boundary `academy/README.md`'s Rejected-Map Rules already anticipates by requiring a rejection's stated reason to be read for what it actually says, not for what a framework wishes it said. It does mean this report does not claim to have fully diagnosed Map026's rejection. It recommends the following as a natural next step, not performed here: a Level 1 observation pass against the rejected `Map026.json` (once policy permits reading it - it remains `hand_authored`/protected per the ledger, read-only inspection does not require write access) would let a future composition analysis, filed under `academy/compositions/`, actually confirm or rule out Topics 5, 9, and 10 with cited evidence rather than inference from one sentence.

## Recommendations for Future Academy Work

- **Immediate candidate for `academy/observations/`:** a Level 1 observation record for `Map026.json` as it currently stands (rejected, `hand_authored`, protected - read-only inspection only), so the tile_usage-versus-composition question above can be resolved with evidence instead of left open.
- **Immediate candidate for `academy/compositions/`:** once that observation record exists, a full ten-topic composition pass against it, explicitly testing whether Topics 5, 9, and 10 held or were genuinely part of the rejection.
- **Immediate candidate for `academy/reports/`:** the resulting case study, once both of the above exist, as the first real entry in that directory - fulfilling exactly the role `academy/README.md` already anticipated when it named the Ashford Inn contract's Required Conditions gap as "Why This Exists Now."
- **A gap in existing pattern evidence, not urgent:** sight lines and entry readability (Topics 4 and 7) would benefit from a dedicated extraction pass, since current evidence for them leans on the research doc's synthesis more than on this project's own extracted pattern corpus.

None of these recommendations is performed by this report or this work order - naming them is the report's job; performing them is future curriculum work, per `academy/curriculum.md`'s own Level 1-4 sequencing.

## Constraints Observed

- No file under `TheLastSwordProtocol-Atlas` or `TheLastSwordProtocol-Game` was modified. `map_ownership.json` and the cited pattern/canon files were read only.
- No existing Design Pattern document was modified.
- No map was created or edited.
- Documentation only.

## References

- `academy/composition-analysis.md`, `composition-rubric.md`, `compositions/README.md`, `README.md`
- `studio/design-patterns/interiors/shop.pattern.md`, `house.pattern.md`, `inn.pattern.md`, `bar.pattern.md`, `chief-house.pattern.md`
- `reports/design-patterns/interior-pattern-corpus-review.md`
- `reports/map-analysis/item-shop-analysis.md` (`TheLastSwordProtocol-Game`, read-only)
- `references/atlas_academy_jrpg_map_research.md`
- `atlas/docs/02_World/Locations/Home_Island/Ashford.md` (`TheLastSwordProtocol-Atlas`, read-only)
- `TheLastSwordProtocol-Game/map_ownership.json` (read-only)
- `reports/implementation-contracts/ashford-inn-pattern-aware-contract.md`
- Created by `work-orders/WO-2002-composition-analysis-framework.md`
