# CAR MASTER — Backlog Recovery 16

Smart-key button cards use distinct crops from Hyundai official Smart Key Overview.

## PASS
- **0447 DOOR LOCK BUTTON** — 480x360, 30098 bytes, HY_LX3_2026_SMART_KEY
- **0448 DOOR UNLOCK BUTTON** — 480x360, 29648 bytes, HY_LX3_2026_SMART_KEY
- **0450 PANIC BUTTON** — 480x360, 20365 bytes, HY_LX3_2026_SMART_KEY
- **0451 LIFTGATE OPEN/CLOSE BUTTON** — 480x360, 32207 bytes, HY_LX3_2026_SMART_KEY

## Failures
- None

## Reverse-QA
- 0447/0448/0450/0451 must each show the correct smart-key icon/button.
- Do not bind the uncropped full smart-key overview to these cards.
- If any crop does not clearly isolate the requested button, Codex must hold only that exact ID.
- Count live Production only after Codex bind + mobile + reverse-QA.
