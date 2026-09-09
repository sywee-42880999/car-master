# CAR MASTER — Backlog Recovery 18

## PASS
- **0460 TPMS MALFUNCTION INDICATOR** — 640x480, 21754 bytes, HY_LX3_2026_TPMS
- **0418 CHARGE/POWER GAUGE** — 584x438, 25800 bytes, HY_NE1A_2025_EV_GAUGES_2
- **0419 HIGH VOLTAGE BATTERY SOC GAUGE** — 582x437, 14182 bytes, HY_NE1A_2025_EV_GAUGES_2
- **0406 V2L CONNECTOR** — 582x437, 45219 bytes, HY_NE1A_2025_V2L
- **0407 V2L POWER OUTLET** — 582x437, 47774 bytes, HY_NE1A_2025_V2L

## Failures
- **0429 AWD WARNING LIGHT** — 14

## Notes
- 0429 uses Hyundai official warning-page item 14 (AWD) via HyundaiOwns font.
- 0460 uses Hyundai official low-tire/TPMS symbol; TPMS malfunction uses the same symbol with blinking behavior.
- 0418/0419 reuse exact already-validated physical gauge images from 0467/0468 because the master terminology is synonymous.
- 0406/0407 use dedicated Hyundai IONIQ 5 V2L official images.
- Count live Production only after Codex bind + mobile + reverse-QA.
