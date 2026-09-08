# CAR MASTER — Backlog Recovery 13

## PASS
- **0233 ROOF SPOILER GARNISH** — 480x360, 20039 bytes, HY_LX3_2026_REAR_OVERVIEW
- **0234 LIFTGATE GARNISH** — 524x393, 49476 bytes, HY_LX3_2026_REAR_OVERVIEW
- **0236 LICENSE PLATE GARNISH** — 480x360, 49671 bytes, HY_LX3_2026_REAR_OVERVIEW
- **0240 BUMPER MOLDING** — 509x382, 67777 bytes, HY_LX3_2026_REAR_OVERVIEW
- **0307 CARGO FLOOR BOARD** — 480x360, 53561 bytes, HY_AXEV_2026_CARGO_FLOOR
- **0359 SUNGLASSES HOLDER** — 673x504, 60724 bytes, KIA_ON_2024_SUNGLASS_HOLDER

## Failures
- None

## Reverse-QA
- 0233/0234/0236/0240 are distinct rear-body crops; do not substitute the uncropped rear overview.
- 0307 must show the physical cargo floor board/cover being lifted, not only the storage tray beneath.
- 0359 uses Kia official Owner’s Manual under the approved manufacturer-manual fallback policy and must visibly show the sunglass holder.
- Count live Production only after Codex bind + mobile + reverse-QA.
