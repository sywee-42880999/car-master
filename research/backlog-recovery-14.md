# CAR MASTER — Backlog Recovery 14

Dedicated Hyundai official control images only.

## PASS
- **0261 STEERING WHEEL TILT/TELESCOPIC LEVER** — 584x438, 81513 bytes, HY_NX4A_2026_STEERING_LEVER
- **0264 ESC OFF BUTTON** — 582x437, 73960 bytes, HY_LX3_2026_ESC_OFF
- **0267 POWER LIFTGATE BUTTON** — 582x437, 75294 bytes, HY_LX3_2026_POWER_LIFTGATE_BUTTON
- **0268 FUEL FILLER DOOR RELEASE BUTTON** — 582x437, 75213 bytes, HY_LX3HEV_2026_FUEL_DOOR_BUTTON
- **0269 CHARGING DOOR OPEN/CLOSE BUTTON** — 582x437, 52730 bytes, HY_NE1N_2026_CHARGING_DOOR_BUTTON

## Failures
- None

## Reverse-QA
- Each card uses a dedicated button/lever image rather than a shared cabin overview.
- 0261 must visibly show the lock-release lever and steering adjustment context.
- 0264/0267/0268/0269 must each show the correct button icon/physical switch.
- Count live Production only after Codex bind + mobile + reverse-QA.
