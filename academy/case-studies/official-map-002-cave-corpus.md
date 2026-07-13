# Official Map Study 002 — Cave and Ruin Reference Set

## Evidence Basis

Direct read-only inspection on 2026-07-10 of the official sample project files `Map051.json` (Stone Cave), `Map053.json` (Cursed Cave), `Map074.json` (Ancient Ruins), their `MapInfos.json`, and `Tilesets.json`. This is a three-map focused reference-set study requested to remediate rejected Sealed Node maps; it does not copy sample geometry, events, dialogue, or story.

## 1. Observation

- [Observed Fact] Stone Cave is 41x30, uses the Dungeon tileset, has 134 distinct base-layer tile IDs, 55 distinct non-empty upper-layer tile IDs, and four events.
- [Observed Fact] Cursed Cave is 50x50, uses the Dungeon tileset, and decorates 655 of 2500 cells (26.2%) on layers 1-3.
- [Observed Fact] Ancient Ruins is 41x50 and decorates 590 of 2050 cells (28.8%) on layers 1-3, including 68 distinct layer-3 IDs.
- [Inference] The reference quality comes from coordinated variation across silhouette, autotile edges, upper-layer dressing, and focal clusters—not from a single connected floor mask.

## 2. Composition

- [Observed Fact] All three maps use irregular room boundaries and local width changes rather than one repeated corridor width.
- [Observed Fact] Stone Cave uses the lowest decoration density but the highest base-layer vocabulary, making floor and wall variation carry more of its visual work.
- [Observed Fact] Cursed Cave and Ancient Ruins use upper-layer coverage above one quarter of the map area.
- [Inference] A compact production cave can remain readable while varying chambers, bends, pockets, edge treatments, and clustered dressing. Decoration should reinforce room identity and route hierarchy rather than form an even noise field.

## 3. Traffic Flow

- [Observed Fact] The maps provide chambers, connector passages, and side pockets rather than a single straight spine.
- [Inference] Main routes should alternate compression and release: narrow connector, readable chamber, landmark, then another connector. Optional pockets should remain visually subordinate and reconnect cleanly.

## 4. Negative Space

- [Observed Fact] Open areas are shaped around routes and chamber centers; upper-layer decoration concentrates near walls, corners, and focal areas.
- [Inference] Open floor is functional movement space, not unfinished canvas. Dense edge dressing can coexist with clear central circulation.

## 5. Landmarks

- [Observed Fact] Each reference uses multiple tile-layer treatments within one map rather than relying only on events as landmarks.
- [Inference] Every Sealed Node screen needs a distinct tile-built focal cluster: embedded ruin threshold, sealed-door machine room, Guardian arena, or Relay dais.

## 6. Passability

- [Observed Fact] This pass studied map structure and layer use directly. It did not infer The Last Sword Protocol collision from sample flags.
- [Inference] Remediation builds must validate collision against their own Dungeon tileset and preserve a clear reachability ring around every event.

## 7. Environmental Storytelling

- [Inference] Stone Cave demonstrates a natural-space baseline; Ancient Ruins demonstrates constructed remnants layered into traversable space. The Sealed Node should visibly progress between those two readings across Maps009-012.

## 8. Metrics

| Map | Size | Distinct base IDs | Distinct upper IDs | Decorated cells | Upper-layer coverage |
|---|---:|---:|---:|---:|---:|
| Map051 Stone Cave | 41x30 | 134 | 55 | 157 | 12.8% |
| Map053 Cursed Cave | 50x50 | 64 | 57 | 655 | 26.2% |
| Map074 Ancient Ruins | 41x50 | 115 | 101 | 590 | 28.8% |

## 9. Lessons Learned

1. Do not equate connectivity with composition quality.
2. Use irregular silhouettes, varied passage widths, chambers, pockets, and loops.
3. Target meaningful upper-layer dressing, generally between Stone Cave's restrained 13% and the denser references' 26-29%, adjusted for map size and readability.
4. Keep circulation centers open while clustering detail at edges and focal points.
5. Give each screen a unique tile-built landmark and make the cave-to-machine transition visible across the sequence.
6. Render and visually review every candidate before presenting it for approval.

## Boundary

This Academy study is evidence only. It does not approve a map, alter Atlas canon, or authorize copying official sample geometry or content.
