# Atlas Academy Knowledge: Validation Rules

## Status

Documentation only, per `work-orders/WO-2006-atlas-academy-knowledge-extraction.md`. This file converts `references/atlas_academy_jrpg_map_research.md` (Part 8 "Metrics," Part 9 "Design anti-patterns," Part 10 "Validation rules" and "Grading rubrics," Module 7, Module 9, Module 10) into reusable Atlas Academy knowledge. It does not modify `academy/map-metrics.md` (`WO-2003`), `academy/grading-system.md` or `grading-rubric.md` (`WO-2005`), which remain the governing metrics and grading authority. It does not grade or validate any specific map.

## Observed Fact

- Official guidance privileges purpose, consistency, and compactness over raw scale, so any metric system that rewards larger maps or more decoration by default would contradict the source material.[cite:16][cite:20][cite:46]
- Official RPG Maker guidance explicitly criticizes unused floor area and rooms that do not make practical use of the available footprint (the report's first named anti-pattern: empty space without meaning).[cite:46]
- Random furniture or prop placement (a bed beside a shop counter, implausibly placed windows, storage scattered away from work zones) is named directly as weakening both realism and navigational intuition.[cite:46]

## Expert Opinion

- High-confidence findings named by the report itself are compactness, purposeful furnishing, readability, landmark utility, and simplified-over-realistic map logic - because these draw on official RPG Maker guidance, Dragon Quest creator remarks, and wayfinding research converging together.[cite:16][cite:20][cite:30][cite:33][cite:37][cite:46]

## Community Practice

- The report's community-vs-official section (see `academy/knowledge/composition-rules.md`) is the only community-practice material relevant here, and it functions as a caution rather than a validation rule: community advice toward visual richness and denser decoration can drift toward clutter or prioritize screenshot aesthetics over play readability, and should not be adopted as a validation target without qualification.[cite:21][cite:26]

## Atlas Interpretation

- The report's Part 10 "Grading rubrics" proposes a five-axis 1-5 scale (readability, purposeful composition, traffic flow, environmental storytelling, exploration payoff).[cite:16][cite:33][cite:46][cite:49] **This reconciliation already happened, in `WO-2005`.** `academy/grading-system.md` states directly that its nine scored categories are "adapted from `references/atlas_academy_jrpg_map_research.md`'s Part 10 proposed five-axis 1-5 rubric," cited at that document's own stated confidence tier (research hypothesis for the numeric scale itself, higher for the underlying design principles). This knowledge file does not re-derive or re-propose that reconciliation; it records the correspondence for traceability:

| Report's five axes (Part 10) | `academy/grading-system.md` category |
|---|---|
| Readability | `readability` |
| Purposeful composition | `composition` |
| Traffic flow | `traffic_flow` |
| Environmental storytelling | `environmental_storytelling` |
| Exploration payoff | Closest existing match is `dragon_quest_exploration_feel` (applicable-when-relevant), though "exploration payoff" in the report is broader (reward pacing generally) than `dragon_quest_exploration_feel`'s narrower DDR-gated scope. This is a noted partial match, not a claimed exact one. |

- The report's Part 8 metrics table (walkable percentage, decoration density, room utilization, average sight line, average aisle width, door spacing, NPC density, empty floor ratio, landmark spacing, visibility distance to goal) corresponds to `academy/map-metrics.md`'s existing metric groups (`WO-2003`): Geometry, Traversal, Events And Interaction, Composition Inputs, RPG Maker Production Health. Both documents already carry the same evidentiary posture - the report labels its metric target bands "research hypothesis... provisional," and `academy/map-metrics.md` independently applies its own confidence discipline per metric. This file records the correspondence; it does not add a new metric group or override either document's existing confidence labels.
- The report's Part 9 anti-patterns (empty space without meaning; over-decoration; random furniture/prop placement; poor traffic flow; maze-like civic space) are recorded here as a checklist an Academy reviewer can hold alongside `academy/composition-rubric.md` and `academy/grading-rubric.md` - each anti-pattern maps to a low score on an existing category (`composition`, `traffic_flow`, `rpg_maker_quality`) rather than requiring a new "anti-pattern" field in either schema.
- The report's Module 10 ("Require agents to analyze and grade maps before proposing original ones")[cite:16][cite:20][cite:30][cite:46] matches `academy/curriculum.md`'s existing sequencing, where Level 1-3 (observe, compare, diagnose) precede Level 4 (propose). No new sequencing rule is introduced; the correspondence is recorded in `academy/knowledge/teaching-lessons.md`.

## Research Hypothesis

- The report's own metrics table (walkable percentage, decoration density, room utilization, average sight line, average aisle width, door spacing, NPC density, empty floor ratio, landmark spacing, visibility distance to goal) is explicitly presented as "design-analysis aids, not rigid laws," with thresholds varying by map type, art style, and intended mood.[cite:5][cite:37][cite:49]
- A map stops feeling like a world and starts feeling like an editor canvas when its objects do not imply systems of use, ownership, and movement - offered as an explanation for why "pretty but unreadable" often fails harder than "simple but clear."[cite:37][cite:46][cite:49]
- Atlas Academy should train agents in three validation passes: structural critique without aesthetic judgment; experiential critique focused on guidance, curiosity, and reward pacing; implementation critique focused on passability, tile logic, density, and consistency.[cite:17][cite:20][cite:37][cite:46] This three-pass structure is recorded as a hypothesis about validation *sequencing*; it is not adopted as a required process by this documentation-only work order, and any future adoption would need its own work order against `academy/grading-system.md`'s existing "How a Grade Is Produced" steps.

## Non-Goals

- Does not modify `academy/map-metrics.md`, `academy/grading-system.md`, or `grading-rubric.md`.
- Does not grade, score, or validate any specific map.
- Does not add a new metric group, category, or schema field.

## References

- `references/atlas_academy_jrpg_map_research.md` (Part 8, Part 9, Part 10 "Validation rules"/"Grading rubrics"/"Implementation guidance," Module 7, Module 9, Module 10)
- `academy/map-metrics.md`, `grading-system.md`, `grading-rubric.md`, `composition-rubric.md`
- `academy/curriculum.md`
- `reports/academy/knowledge-extraction-report.md`
- Created by `work-orders/WO-2006-atlas-academy-knowledge-extraction.md`
