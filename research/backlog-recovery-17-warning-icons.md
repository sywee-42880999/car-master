# CAR MASTER — Backlog Recovery 17 / Hyundai Warning Icons

Method: parse Hyundai official warning-light page, map each official label to its HyundaiOwns glyph/color class, convert Hyundai official WOFF to TTF, and render one 4:3 learning card per icon.

## PASS
- **0390 Airbag warning light** — official item (2), glyph `=`, class `red`, 23486 bytes
- **0391 Seat belt warning light** — official item (1), glyph `!`, class `red`, 23449 bytes
- **0392 Parking brake & Brake fluid warning light** — official item (3), glyph `?`, class `red`, 45390 bytes
- **0393 Anti-lock Brake System (ABS) warning light** — official item (4), glyph `ǹ`, class `orange`, 30662 bytes
- **0394 Electronic Stability Control (ESC) indicator light** — official item (26), glyph `a`, class `orange`, 20243 bytes
- **0395 Master warning light** — official item (23), glyph `X`, class `orange`, 24518 bytes
- **0421 Motor Driven Power Steering (MDPS) warning light** — official item (6), glyph `E`, class `red`, 27519 bytes
- **0422 Low fuel level warning light** — official item (7), glyph `G`, class `orange`, 21167 bytes
- **0423 Engine oil pressure warning light** — official item (8), glyph `H`, class `red`, 27209 bytes
- **0424 Malfunction Indicator Lamp (MIL)** — official item (9), glyph `I`, class `orange`, 22445 bytes
- **0425 12 V Battery Charging system warning light** — official item (10), glyph `K`, class `orange`, 20849 bytes
- **0426 Low tire pressure warning light** — official item (11), glyph `L`, class `orange`, 21754 bytes
- **0427 Electronic Parking Brake (EPB) warning light** — official item (12), glyph `M`, class `orange`, 22515 bytes
- **0428 AUTO HOLD indicator light** — official item (13), glyph `N`, class `default`, 24548 bytes
- **0430 Forward Safety warning light** — official item (15), glyph `O`, class `default`, 19619 bytes
- **0431 Emergency steering warning light** — official item (16), glyph `P`, class `default`, 22136 bytes
- **0432 Lane Safety indicator light** — official item (17), glyph `S`, class `default`, 18767 bytes
- **0433 Lane Following Assist (LFA) indicator light** — official item (18), glyph `ġ`, class `default`, 18026 bytes
- **0434 Speed limiter indicator light** — official item (19), glyph `Ý`, class `green`, 35882 bytes
- **0435 Intelligent Speed Limit Assist (ISLA) indicator light** — official item (20), glyph `y`, class `orange`, 17412 bytes
- **0436 Inattentive driving warning light** — official item (21), glyph `W`, class `orange`, 21105 bytes
- **0437 Forward Attention Warning light** — official item (22), glyph `ƻ`, class `red`, 29758 bytes
- **0438 LED headlight warning light** — official item (24), glyph `Y`, class `orange`, 26551 bytes
- **0439 Downhill Brake Control (DBC) indicator light** — official item (25), glyph `U`, class `green`, 28430 bytes
- **0440 Electronic Stability Control (ESC) indicator light** — official item (26), glyph `a`, class `orange`, 20243 bytes
- **0441 Electronic Stability Control (ESC) OFF indicator light** — official item (27), glyph `b`, class `orange`, 25802 bytes
- **0442 Immobilizer indicator light** — official item (28), glyph `j`, class `orange`, 22074 bytes
- **0443 Low beam indicator light** — official item (30), glyph `^`, class `green`, 28733 bytes
- **0444 High beam indicator light** — official item (31), glyph `]`, class `blue`, 20677 bytes
- **0445 High Beam Assist (HBA) indicator light** — official item (32), glyph `Z`, class `default`, 21283 bytes

## Failures
- **0429 AWD warning light** — label not found

## Reverse-QA
- Each image is generated from Hyundai's official warning-page glyph rendered with Hyundai's official HyundaiOwns font.
- The card contains only the target icon on a dark field; no generic cluster screenshot is reused.
- 0394 and 0440 intentionally map to the same official ESC symbol because the master contains both warning/indicator terminology variants.
- Count live Production only after Codex bind + mobile + reverse-QA.
