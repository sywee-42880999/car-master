# CAR MASTER — Backlog Recovery 10

Hyundai official front/rear exterior overviews, converted into card-specific crops.

## PASS
- **0028 TURN SIGNAL LIGHT** — 585x439, 81487 bytes, HY_LX3_2026_EXTERIOR_OVERVIEWS
- **0029 REAR SPOILER** — 479x359, 31563 bytes, HY_LX3_2026_REAR_OVERVIEW
- **0211 FRONT DOOR GLASS** — 480x360, 38789 bytes, HY_LX3_2026_EXTERIOR_OVERVIEWS
- **0212 REAR DOOR GLASS** — 478x359, 39542 bytes, HY_LX3_2026_EXTERIOR_OVERVIEWS
- **0213 QUARTER GLASS** — 478x359, 23292 bytes, HY_LX3_2026_EXTERIOR_OVERVIEWS
- **0235 TAILGATE GLASS** — 648x486, 77860 bytes, HY_LX3_2026_REAR_OVERVIEW
- **0237 FRONT SKID PLATE** — 479x359, 47454 bytes, HY_LX3_2026_EXTERIOR_OVERVIEWS
- **0238 REAR SKID PLATE** — 480x360, 47927 bytes, HY_LX3_2026_REAR_OVERVIEW

## Failures
- None

## Reverse-QA
- Each card must read as the requested exterior part, not the whole vehicle.
- 0211/0212/0213 must remain visually distinct as front door glass / rear door glass / quarter glass.
- 0237/0238 must clearly read as lower skid-plate areas.
- Count live Production only after Codex bind + mobile + reverse-QA.
