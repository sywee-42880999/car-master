# CAR MASTER — Backlog Recovery 25 — Cluster

## PASS
- **0388 DISTANCE TO EMPTY** — 582x437, 21950 bytes — HY_LX3_2026_DISTANCE_TO_EMPTY
- **0389 OUTSIDE TEMPERATURE GAUGE** — 582x437, 12909 bytes — HY_NE1A_2025_OUTSIDE_TEMP
- **0386 ENGINE COOLANT TEMPERATURE GAUGE** — 697x522, 103767 bytes — HY_LX3_2026_CLUSTER_GAUGES_WARNINGS
- **0387 CLUSTER DISPLAY** — 709x532, 131795 bytes — HY_LX3_2026_CLUSTER_GAUGES_WARNINGS

## Failures

## Reverse-QA
- 0388 must show Distance to Empty directly.
- 0389 must show Outside Temperature directly.
- 0386 must read as engine coolant temperature gauge; 0387 as central cluster display.
- Count live Production only after Codex reverse-QA.
