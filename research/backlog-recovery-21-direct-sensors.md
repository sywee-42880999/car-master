# CAR MASTER — Backlog Recovery 21 — Direct Sensors & Fuse Puller

## PASS
- **0009 FRONT RADAR** — 584x438, 46675 bytes — HY_NX4_2025_RADARS
- **0010 FRONT VIEW CAMERA** — 480x360, 11409 bytes — HY_NE1N_2026_FCA_SENSORS
- **0218 FRONT CAMERA** — 480x360, 11409 bytes — HY_NE1N_2026_FCA_SENSORS
- **0378 FRONT CORNER RADAR** — 478x359, 30448 bytes — HY_NE1N_2026_FCA_SENSORS
- **0379 REAR CORNER RADAR** — 582x437, 45628 bytes — HY_NE1N_2026_FCA_SENSORS
- **0219 SIDE CAMERA** — 478x359, 32333 bytes — HY_NE1N_2025_WIDE_CAMERAS
- **0220 REAR CAMERA** — 582x437, 38844 bytes — HY_NE1N_2025_WIDE_CAMERAS
- **0380 WIDE-FRONT VIEW CAMERA** — 478x359, 22689 bytes — HY_NE1N_2025_WIDE_CAMERAS
- **0381 WIDE-SIDE VIEW CAMERA** — 478x359, 32333 bytes — HY_NE1N_2025_WIDE_CAMERAS
- **0475 FUSE PULLER** — 478x359, 51629 bytes — HY_NX4_2025_FUSE_PULLER

## Failures

## Reverse-QA
- 0009 must show the physical front radar unit/location, not a generic bumper.
- 0010/0218 must show front view camera area.
- 0378/0379 must distinguish front/rear corner radar.
- 0219/0381 must show side/wide-side camera; 0220 rear camera; 0380 wide-front camera.
- 0475 must visibly show the fuse puller tool in use.
- Count live Production only after Codex bind + mobile + reverse-QA.
