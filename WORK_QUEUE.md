# CAR MASTER — SHARED WORK QUEUE

This file is the single source of truth and handoff board for ordinary ChatGPT and ChatGPT Work.

## Current status
- Progress: **4%** (20/500)
- Completed: 0001–0020
- Current production batch: 0021–0030
- Repository: `sywee-42880999/car-master`
- Branch: `main`

## NEW FIXED OPERATING RULE — 2026-09-07
1. **Every project change must be written to GitHub so Chat and Work can both see it.** Do not keep project decisions only in conversation memory.
2. Before either Chat or Work starts a batch, read `WORK_QUEUE.md`, `data/master.json`, `data/progress.json`, and `data/source_registry.json` from `main`.
3. After either agent changes terminology, source, image, UI rule, status, or workflow, write the change back to the repository before handing off.
4. Repository state overrides conversational memory when they conflict.
5. `https://sywee-42880999.github.io/car-master/` is always the user-facing CAR MASTER learning/review app. Never replace the root with an admin registry.
6. Registry/source/queue pages are internal support pages only.
7. **UI DESIGN LOCK: use yesterday's BLACK version as the production design baseline.** Do not redesign the application while content production is underway. White version is a later derivative after Black is complete.
8. User review happens in the actual learning UI, not a registry/contact sheet. Permanent ID is shown so revisions can be requested by number.
9. A task is not COMPLETE merely because JSON/Markdown was committed. COMPLETE means the user-facing app actually displays the intended result.

## Fixed product structure
- BLACK learning UI is the main app.
- Modes remain: Part Learning / 4-choice / Mixed Test.
- Preserve the existing mobile-first interaction and learned/next flow from the approved Black prototype.
- Content source is the permanent-ID master, not hardcoded temporary four-item demo data.
- Each learning item should include: permanent ID, Korean name, official English term, useful short explanation/recognition cue, image, and learning progress.
- Do not expose production/admin clutter in the main learning flow.

## Fixed objective
Produce a 500-entry **Automotive Visual Vocabulary / Wordbook** using Hyundai official Owner's Manual material as the terminology/source baseline.

## Permanent content rules
1. Every term has a permanent four-digit ID. Never renumber, delete, or reuse an ID.
2. Search manuals and compare candidates instead of accepting the first image found.
3. Prefer original embedded PDF images/drawings or existing official assets. Do not rerender PDF pages when extraction is possible.
4. Final vocabulary image target: clean 4:3 crop. Do not upscale weak sources just to fill the frame.
5. Prefer a close-up where the part is self-evident. If the part fills the crop, **no marker**.
6. If context is necessary, markers are HTML overlays only: precise part = red dot; multiple precise parts = multiple red dots; broad surface = isolated soft red oval.
7. Never bake markers into JPG.
8. Ambiguous items are REVIEW, never guessed.
9. Reverse QA: English term → actual physical part → image → marker/crop.
10. Hyundai global Owner's Manual terminology is the baseline. Regional aliases may be recorded without changing the permanent ID.
11. When the same physical part exists multiple times on a vehicle, use plural English wording where appropriate for the vocabulary category.

## Low-cost division of labor
### Ordinary ChatGPT
- Own permanent ID/term master.
- Research Hyundai official terminology and candidate sources.
- Check duplicates and aliases.
- Write explanations/recognition cues.
- Prepare exact image extraction/crop instructions.
- Maintain source registry, queue, progress logic, and lightweight GitHub/HTML/data changes.

### ChatGPT Work
- Do expensive browser/file manipulation only when needed.
- Extract original embedded PDF/web-manual images.
- Produce final 4:3 crops.
- Save assets to repository and update their repo paths.
- Perform repetitive asset/data/UI integration in batches.
- Do not spend Work time rediscovering terminology/source research already recorded here.

### User
- Reviews only the live BLACK learning app.
- Reports exceptions by permanent ID, e.g. `0017 이미지 수정`.
- Routine approval is not required for production to continue.

## Shared source rule
`data/source_registry.json` is the shared map for PDF URL, official web URL, image key, and final repo asset path. If one agent cannot render one surface, use another recorded surface or repo asset; do not stop at “cannot see it.”

## Current batch research — IDs 0011–0020
Terminology checked, duplicate relationships reviewed, and official Hyundai candidates are recorded in `data/master.json` and `data/source_registry.json`.

### 0011 DOORS
Use LX3 rear exterior overview `1C_OutsideVehicleRearOverview`. Prefer a clear passenger-door crop; broad-area overlay only if needed.

### 0012 FUEL FILLER DOOR
Use LX3 dedicated `2C_FuelInletDoor`; prefer closed exterior door, tight crop, no marker if obvious.

### 0013 ELECTRIC CHARGING DOOR
Use official IONIQ 5 source / `2C_HowToUseChargingDoor`; prefer exterior charging-door view, not connector-only detail.

### 0014 REAR COMBINATION LIGHTS
Use NX4a `2C_RearLampOverview` or `_2`; show complete lamp assembly.

### 0015 REVERSE LIGHTS
Use LX3 overview or MX5a rear-lamp source; distinguish reverse lamp from full combination lamp. Precise overlay only when context requires it.

### 0016 LIFTGATE
Use LX3 rear overview. `Tailgate` may be a regional alias; master stays LIFTGATE. Show the liftgate panel clearly.

### 0017 WIDE-REAR VIEW CAMERA
Use AXEV `2C_WideRearViewCamera`; confirm actual lens/module, not handle or plate lamp.

### 0018 ANTENNA
Use LX3 `2C_Antenna`; exterior roof/shark-fin antenna only.

### 0019 REAR WINDOW WIPER BLADE
Use LX2 `B0452KO05/B0452KO06` or LX3 overview; prefer intact blade on rear glass.

### 0020 HIGH MOUNTED STOP LIGHT
Use NX4 `2C_HighMountedStopLamp`; crop upper rear lamp/spoiler area so it is unmistakable.

## Current Work execution order
1. Restore/retain the approved **BLACK learning UI** as the root application.
2. Connect the Black UI to permanent-ID content instead of the temporary hardcoded 4-item demo.
3. Preserve 0001–0010; do not substitute generic VENUE overview images when a proper close-up is required.
4. Produce/extract final assets for 0011–0020 from the recorded official sources.
5. Update `data/source_registry.json` with each final repo asset path.
6. Verify the live root app displays each finished item correctly on mobile.
7. Only then update `data/progress.json` from 10/500 to 20/500 = 4%.

## Production result — 2026-09-08 (IDs 0011–0020)
- Produced ten 4:3 learning crops at `images/parts/0011.jpg` through `images/parts/0020.jpg` from the registered Hyundai Owner's Manual originals. No new marker was baked into a JPG.
- Bound every final path to its permanent ID in `data/master.json` and `data/source_registry.json`; the BLACK UI now prefers the permanent-ID final image over source candidates.
- Reverse image QA passed for IDs 0011–0020. Original manual callouts remain only where they are part of Hyundai's embedded source illustration.
- Updated the offline cache manifest for all ten production assets.
- Next production batch: 0021–0030, using `research/0021-0030.md` and the shared source registry.

## Definition of DONE
An item is DONE only when: terminology is verified + source recorded + final image/crop exists + correct live Black UI item displays + reverse QA passes. GitHub data without live display is not DONE.

## Instruction for every new Chat or Work session
Read `WORK_QUEUE.md`, `data/master.json`, `data/progress.json`, and `data/source_registry.json` first. Continue from repository state. Write all material decisions/changes back to GitHub before handoff.

## Execution handoff — 2026-09-07 (official source extraction)
- Read queue, master, progress, source registry and ID registry on main. No AGENTS.md exists in the checkout.
- Verified all 9 registered official web pages and downloaded 13 original candidate images under `images/source/`. Exact URLs, local paths and SHA-256 hashes are appended as `extracted_assets` in the source registry. Original URLs and final `repo_asset: null` fields are preserved.
- These are SOURCE_ONLY candidates, not final learning images. Original illustrations may contain manual callouts; final crops and reverse visual QA remain required.
- Corrected source discovery for 0019: official filenames are `B0452KO05.eps.png` and `B0452KO06.eps.png`, not `.jpg.png`.
- Validation passed: all 13 files have JPEG/PNG signatures, readable dimensions and matching hashes; all 500 allocated IDs are unique; master IDs and source references resolve. Official filenames ending in .png may contain JPEG bytes; originals are intentionally unchanged.
- UI prerequisite unresolved: all 18 commits reachable from main were inspected; initial `33af1fa` and later legacy trainer use light backgrounds. The approved BLACK prototype is not present in this history. Requested its URL/branch/file from user; do not invent a replacement design under the UI lock.
- Next: obtain approved BLACK baseline, restore root learning UI and permanent-ID data binding; select/crop candidates, preserve/recover proper 0001–0010 assets, then verify live mobile display and reverse QA.
- Production completion remains 2%. No new item is marked DONE and no live display validation is claimed.

## PRODUCTION OWNERSHIP CHANGE — 2026-09-08
User requested a token-saving workflow change.

### ChatGPT (this chat) now owns image Production where possible
- Work in **10-ID batches** for quality.
- Read official Hyundai source assets already stored in the Repo.
- Select the clearest official Source Asset for each permanent ID.
- Create the final **4:3 crop** so the physical part itself is unmistakable.
- Prefer tight close-up; no marker when the part is self-evident.
- If context is required, do not bake markers into JPG. Record marker guidance for HTML overlay.
- Perform reverse QA before handoff.
- Commit crop/source/QA handoff results to main whenever the available tool path allows it.
- First correction batch: **0011–0020**, using `research/0011-0020-production.md`.

### Codex / Work role is reduced
Codex should **not redo source research or crop work that Chat has already completed**.
After each Chat production batch appears on `main`, Codex should:
1. Pull latest `main`.
2. Read this queue and the batch handoff.
3. Bind final part assets to the permanent IDs/data only where Chat has not already done so.
4. Preserve BLACK UI design.
5. Add HTML marker overlays only when handoff explicitly requests one.
6. Deploy GitHub Pages and verify the live mobile BLACK UI.
7. Report any visual mismatch back into the Repo/queue by permanent ID instead of silently substituting another image.

### Shared communication protocol
- GitHub `main` is the communication channel between Chat and Codex.
- Before starting work, each side must pull/read the latest queue and relevant research/handoff file.
- Do not overwrite the other side's active batch.
- If a batch file or target asset already exists, inspect it first and continue from Repo state.
- Production progress must not be incremented merely because a crop or research file was committed. Increment only after correct live BLACK UI display + reverse QA.


## LATEST PRODUCTION CORRECTION — 2026-09-08
This section supersedes the older statement above that all 0011–0020 crops passed reverse QA.

Chat-generated correction crops were visually reviewed from Hyundai official source assets and promoted only where the physical part was sufficiently clear.

- PASS replacement crops: **0011, 0012, 0013, 0014, 0015, 0016, 0019, 0020**
- REVIEW / stronger official close-up still required: **0017 WIDE-REAR VIEW CAMERA, 0018 ANTENNA**
- Detailed result: `research/0011-0020-production-result.md`
- Crop generator: `tools/build_production_preview.py`
- Codex must not silently promote 0017/0018 merely because an official overview contains a callout.
- No Production percentage increment from this correction cycle.
- GitHub main remains the Chat↔Codex handoff channel; Codex should pull latest main before continuing UI bind/deploy work.


## CODEX HANDOFF READY — 2026-09-08 — IDs 0021–0030
Chat Production has completed and committed usable final 4:3 assets for:
- **0021 FRONT BUMPER**
- **0022 REAR BUMPER**
- **0023 FRONT GRILLE**
- **0024 WINDSHIELD**
- **0025 REAR WINDOW**
- **0026 OUTSIDE DOOR HANDLE**
- **0027 ULTRASONIC SENSORS** — physical-term correction from prior PARKING DISTANCE WARNING SENSOR; old wording retained as alias/system relation.
- **0030 ROOF SIDE RAILS** — physical-term correction from prior ROOF RACK; old wording retained as alias/accessory relation.

Final assets are at `images/parts/0021.jpg`–`0027.jpg` and `images/parts/0030.jpg`.
Detailed QA: `research/0021-0030-production-result.md`.

Still REVIEW — do not bind/promote:
- **0028 TURN SIGNAL LIGHT** — current official overview combines DRL/position/turn-signal area; stronger visually isolated source needed.
- **0029 REAR SPOILER** — current official high-mounted-stop-lamp source shows the spoiler structure but is not a dedicated spoiler source.

### Codex action now
1. Pull latest `main`.
2. Bind/display 0021–0027 and 0030 in the existing BLACK learning UI without redesign.
3. Do not redo crops or source research for those PASS items.
4. Do not promote 0028/0029.
5. Deploy GitHub Pages and verify on mobile.
6. Report any mismatch by permanent ID into Repo/queue.
7. Do not increment Production % merely from this handoff; update only after correct live display + reverse QA.


## CODEX HANDOFF READY — 2026-09-08 — IDs 0031–0040
Chat Production has completed and committed final 4:3 assets for:
- **0031 INSIDE DOOR HANDLE**
- **0032 POWER WINDOW SWITCHES**
- **0033 POWER WINDOW LOCK BUTTON**
- **0034 CENTRAL DOOR LOCK SWITCH**
- **0035 SIDE VIEW MIRROR CONTROL SWITCH**
- **0036 SIDE VIEW MIRROR FOLDING BUTTON**
- **0037 EPB (ELECTRONIC PARKING BRAKE) SWITCH**
- **0038 HOOD RELEASE LEVER**
- **0039 STEERING WHEEL**

Final assets: `images/parts/0031.jpg`–`images/parts/0039.jpg`.
Source: Hyundai 2026 Palisade LX3 Interior Overview, `1C_SideInsideVehicleOverview`.
Detailed QA: `research/0031-0040-production-result.md`.

Still REVIEW — do not bind/promote:
- **0040 FUSE BOX** — overview identifies location, but the actual fuse box/cover is not visually unmistakable enough for a learning card. Use a dedicated Hyundai fuse-panel/fuse-box illustration next.

### Codex action now
1. Pull latest `main`.
2. Bind/display 0031–0039 in the existing BLACK UI without redesign.
3. Do not redo the crops/source research.
4. Do not promote 0040.
5. Deploy and mobile-check; report mismatches by permanent ID.
6. Production % changes only after live BLACK UI + reverse QA.


## CODEX HANDOFF READY — 2026-09-08 — IDs 0041–0050
Chat Production has completed and committed final assets for:
- **0041 GLOVE BOX**
- **0043 CUP HOLDER**
- **0044 USB PORT**
- **0045 USB CHARGER**
- **0046 POWER OUTLET**
- **0047 WIRELESS SMARTPHONE CHARGING SYSTEM**
- **0048 HAZARD WARNING FLASHER BUTTON**
- **0049 ENGINE START/STOP BUTTON**
- **0050 INSTRUMENT CLUSTER**

Final assets: `images/parts/0041.jpg`, `0043.jpg`–`0050.jpg`.
Detailed QA: `research/0041-0050-production-result.md`.

Still REVIEW — do not bind/promote:
- **0042 CENTER CONSOLE** — current dedicated Hyundai image is specifically Center Console Storage, so using it would collide with permanent ID 0111 CENTER CONSOLE STORAGE. Use a stronger full-console source before promotion.

### Codex action now
1. Pull latest `main`.
2. Bind/display 0041 and 0043–0050 in the existing BLACK UI without redesign.
3. Do not redo crops or source research.
4. Do not promote 0042.
5. Deploy and mobile-check; report mismatches by permanent ID.
6. Production % changes only after live BLACK UI + reverse QA.


## CODEX HANDOFF READY — 2026-09-08 — IDs 0051–0060
Chat Production has completed and committed final assets for:
- **0051 HORN**
- **0052 INFOTAINMENT SYSTEM**
- **0053 CLIMATE CONTROL SYSTEM**
- **0054 AUTO HOLD BUTTON**
- **0056 DOWNHILL BRAKE CONTROL BUTTON**
- **0057 PARKING SAFETY BUTTON**
- **0058 PARKING/VIEW BUTTON**
- **0059 UV-C STERILIZER SYSTEM**
- **0060 AC INVERTER**

Final assets: `images/parts/0051.jpg`–`0054.jpg`, `0056.jpg`–`0060.jpg`.
Detailed QA: `research/0051-0060-production-result.md`.

Still REVIEW — do not bind/promote:
- **0055 DRIVE MODE CONTROL** — Hyundai overview shows DRIVE/TERRAIN integrated-control hardware, but canonical physical-part wording remains unresolved across models.

### Codex action now
1. Pull latest `main`.
2. Bind/display the PASS items above in the existing BLACK UI without redesign.
3. Do not redo crops or source research.
4. Do not promote 0055.
5. Deploy and mobile-check; report mismatches by permanent ID.
6. Production % changes only after live BLACK UI + reverse QA.


## CODEX HANDOFF READY — 2026-09-08 — IDs 0061–0070
Chat Production has completed and committed final assets for:
- **0061 FRONT SEAT**
- **0062 REAR SEAT**
- **0063 HEAD RESTRAINT**
- **0064 SEATBACK**
- **0065 SEAT CUSHION**
- **0066 SEAT BELT**
- **0067 SEAT BELT BUCKLE**
- **0068 TETHER ANCHOR**
- **0069 LATCH LOWER ANCHOR**

Final assets: `images/parts/0061.jpg`–`images/parts/0069.jpg`.
Detailed QA: `research/0061-0070-production-result.md`.

Still REVIEW — do not bind/promote:
- **0070 SEAT BELT PRETENSIONER** — no dedicated unmistakable official Hyundai pretensioner illustration verified in this pass.

### Codex action now
1. Pull latest `main`.
2. Bind/display 0061–0069 in the existing BLACK UI without redesign.
3. Do not redo crops or source research.
4. Do not promote 0070.
5. Deploy and mobile-check; report mismatches by permanent ID.
6. Production % changes only after live BLACK UI + reverse QA.


## CODEX HANDOFF READY — 2026-09-08 — IDs 0071–0080
Chat Production has completed and committed final assets for:
- **0071 DRIVER'S FRONT AIRBAG**
- **0072 PASSENGER'S FRONT AIRBAG**
- **0073 FRONT SIDE AIRBAG**
- **0074 REAR SIDE AIRBAG**
- **0075 CURTAIN AIRBAG**
- **0076 FRONT PASSENGER AIRBAG ON/OFF SWITCH**
- **0077 SEAT WARMER SWITCH**
- **0078 AIR VENTILATION SEAT SWITCH** — corrected from feature-level AIR VENTILATION SEAT so the permanent card matches the visible physical control.

Final assets: `images/parts/0071.jpg`–`images/parts/0078.jpg`.
Detailed QA: `research/0071-0080-production-result.md`.

Still REVIEW — do not bind/promote:
- **0079 SEATBACK FOLDING LEVER**
- **0080 REMOTE FOLDING BUTTON**
Current Hyundai seat overview does not isolate these physical controls clearly enough for a learning card.

### Codex action now
1. Pull latest `main`.
2. Bind/display 0071–0078 in the existing BLACK UI without redesign.
3. Do not redo crops or source research.
4. Do not promote 0079/0080.
5. Deploy and mobile-check; report mismatches by permanent ID.
6. Production % changes only after live BLACK UI + reverse QA.


## CODEX HANDOFF READY — 2026-09-08 — IDs 0081–0090
Chat Production has completed and committed final assets for:
- **0081 INSIDE REARVIEW MIRROR**
- **0082 DIGITAL CENTER MIRROR**
- **0083 MAP LAMP**
- **0084 ROOM LAMP**
- **0085 REAR PERSONAL LAMP**
- **0086 CENTER CONSOLE LAMP**
- **0087 MOOD LAMP**
- **0088 VANITY MIRROR LAMP**
- **0089 GLOVE BOX LAMP**
- **0090 CARGO AREA LAMP**

Final assets: `images/parts/0081.jpg`–`images/parts/0090.jpg`.
Detailed QA: `research/0081-0090-production-result.md`.

### Codex action now
1. Pull latest `main`.
2. Bind/display 0081–0090 in the existing BLACK UI without redesign.
3. Do not redo crops or source research.
4. Deploy and mobile-check; report mismatches by permanent ID.
5. Production % changes only after live BLACK UI + reverse QA.


## CODEX HANDOFF READY — 2026-09-08 — IDs 0091–0100
Chat Production has completed and committed final assets for:
- **0091 LIGHTING CONTROL LEVER**
- **0092 WIPER AND WASHER CONTROL LEVER**
- **0093 PADDLE SHIFTERS**
- **0094 DRIVING ASSIST BUTTON**
- **0095 CLUSTER DISPLAY CONTROL BUTTON**
- **0096 VEHICLE DISTANCE BUTTON**
- **0097 LANE DRIVING ASSIST BUTTON**
- **0098 ROTARY GEAR SHIFT DIAL**
- **0099 STEERING WHEEL AUDIO CONTROLS**
- **0100 VOICE RECOGNITION BUTTON**

Final assets: `images/parts/0091.jpg`–`images/parts/0100.jpg`.
Detailed QA: `research/0091-0100-production-result.md`.

### Codex action now
1. Pull latest `main`.
2. Bind/display 0091–0100 in the existing BLACK UI without redesign.
3. Do not redo crops or source research.
4. Deploy and mobile-check; report mismatches by permanent ID.
5. Production % changes only after live BLACK UI + reverse QA.


## CODEX HANDOFF READY — 2026-09-08 — IDs 0101–0110
Chat Production has completed and committed final assets for:
- **0101 BLUETOOTH® HANDS-FREE PHONE BUTTON**
- **0102 IN-CABIN CAMERA**
- **0103 DRIVE MODE BUTTON**
- **0104 TERRAIN MODE BUTTON**
- **0105 N1/N2 BUTTON**
- **0106 NGB BUTTON**
- **0107 SUNVISOR**
- **0108 VANITY MIRROR**
- **0109 TICKET HOLDER**
- **0110 SUNROOF SWITCH**

Final assets: `images/parts/0101.jpg`–`images/parts/0110.jpg`.
Detailed QA: `research/0101-0110-production-result.md`.

### Codex action now
1. Pull latest `main`.
2. Bind/display 0101–0110 in the existing BLACK UI without redesign.
3. Do not redo crops or source research.
4. Deploy and mobile-check; report mismatches by permanent ID.
5. Production % changes only after live BLACK UI + reverse QA.


## CODEX HANDOFF READY — 2026-09-08 — IDs 0111–0120
Chat Production has completed and committed final assets for:
- **0111 CENTER CONSOLE STORAGE**
- **0112 OPEN TRAY**
- **0113 SLIDING TRAY**
- **0114 CARGO TRAY**
- **0115 COAT HOOK**
- **0116 REAR SIDE SUNSHADE**
- **0117 CARGO NET HOLDER**
- **0118 CARGO SECURITY SCREEN**
- **0120 POWER SUNSHADE SWITCH**

Final assets: `images/parts/0111.jpg`–`images/parts/0118.jpg`, `images/parts/0120.jpg`.
Detailed QA: `research/0111-0120-production-result.md`.

Still REVIEW — do not bind/promote:
- **0119 FLOOR MAT ANCHORS** — official terminology is verified, but no unmistakable dedicated Hyundai anchor image was verified in this pass.

### Codex action now
1. Pull latest `main`.
2. Bind/display the PASS items above in the existing BLACK UI without redesign.
3. Do not redo crops or source research.
4. Do not promote 0119.
5. Deploy and mobile-check; report mismatches by permanent ID.
6. Production % changes only after live BLACK UI + reverse QA.


## CODEX HANDOFF READY — 2026-09-08 — IDs 0121–0130
Chat Production has completed and committed final assets for:
- **0121 TIRE MOBILITY KIT**
- **0122 COMPRESSOR**
- **0123 SEALANT BOTTLE**
- **0124 PRESSURE GAUGE**
- **0126 TIRE VALVE**
- **0127 SMART KEY**
- **0128 MECHANICAL KEY**
- **0129 KEY CYLINDER**
- **0130 EMERGENCY LIFTGATE SAFETY RELEASE LATCH**

Final assets: `images/parts/0121.jpg`–`images/parts/0124.jpg`, `images/parts/0126.jpg`–`images/parts/0130.jpg`.
Detailed QA: `research/0121-0130-production-result.md`.

Still REVIEW — do not bind/promote:
- **0125 FILLING HOSE** — Hyundai's TMK diagram distinguishes two filling-hose roles; keep REVIEW until the physical taxonomy is resolved.

### Codex action now
1. Pull latest `main`.
2. Bind/display the PASS items above in the existing BLACK UI without redesign.
3. Do not redo crops or source research.
4. Do not promote 0125.
5. Deploy and mobile-check; report mismatches by permanent ID.
6. Production % changes only after live BLACK UI + reverse QA.


## CODEX HANDOFF READY — 2026-09-08 — IDs 0131–0140
Chat Production has completed and committed final assets for:
- **0131 JACK HANDLE**
- **0132 JACK**
- **0133 TOWING HOOK**
- **0134 WHEEL LUG NUT WRENCH**
- **0135 SOCKET**
- **0136 SPARE TIRE**
- **0140 JACKING POSITION**

Final assets: `images/parts/0131.jpg`–`images/parts/0136.jpg`, `images/parts/0140.jpg`.
Detailed QA: `research/0131-0140-production-result.md`.

Still REVIEW — do not bind/promote:
- **0137 SPARE TIRE CARRIER**
- **0138 SPARE TIRE RETAINER GUIDE**
- **0139 WHEEL STUDS**

### Codex action now
1. Pull latest `main`.
2. Bind/display the PASS items above in the existing BLACK UI without redesign.
3. Do not redo crops or source research.
4. Do not promote 0137–0139.
5. Deploy and mobile-check; report mismatches by permanent ID.
6. Production % changes only after live BLACK UI + reverse QA.


## CODEX VERIFICATION NOTE — 2026-09-08 — 0121–0130 CORRECTED
Second verification found the initial 0122/0123/0124 production JPGs were identical overview crops. Chat corrected and recommitted them as distinct physical-part images.

Codex must pull latest `main` before deploy and use the current blobs:
- **0122 COMPRESSOR** → `d3081bab72f48761c8c5e19ddc1348796e7460fb`
- **0123 SEALANT BOTTLE** → `e7ada2d4c2389e0feabe3b58892aa50a9094dd1d`
- **0124 PRESSURE GAUGE** → `399940057005b5271ec919f0b5b4dc9a639369e9`

Do not use earlier identical 0122–0124 assets. 0125 remains REVIEW. Production % still changes only after live BLACK UI + reverse QA.


## CODEX HANDOFF READY — 2026-09-08 — IDs 0141–0150
Chat Production has completed and committed final assets for:
- **0141 ENGINE COOLANT RESERVOIR**
- **0142 ENGINE OIL FILLER CAP**
- **0143 BRAKE FLUID RESERVOIR**
- **0146 WINDSHIELD WASHER FLUID RESERVOIR**
- **0148 AIR CLEANER**

Final assets: `images/parts/0141.jpg`, `0142.jpg`, `0143.jpg`, `0146.jpg`, `0148.jpg`.
Detailed QA: `research/0141-0150-production-result.md`.

Still REVIEW — do not bind/promote:
- **0144 BATTERY** — resolve BATTERY vs 12V BATTERY naming.
- **0145 FUSE BOX** — conflicts with existing 0040 generic FUSE BOX; requires location-qualified taxonomy.
- **0147 ENGINE OIL DIPSTICK** — current overview callout is too small for a strong learning card.
- **0149 RADIATOR CAP** — official terminology verified, stronger source image still required.
- **0150 CABIN AIR FILTER** — motor-room overview shows location/cover rather than the filter element itself.

### Codex action now
1. Pull latest `main`.
2. Bind/display the PASS items above in the existing BLACK UI without redesign.
3. Do not redo crops or source research.
4. Do not promote REVIEW items.
5. Deploy and mobile-check; report mismatches by permanent ID.
6. Production % changes only after live BLACK UI + reverse QA.


## CODEX HANDOFF READY — 2026-09-08 — IDs 0151–0160
Chat Production has completed and committed a final asset for:
- **0154 FUEL FILLER CAP**

Final asset: `images/parts/0154.jpg`.
Detailed QA: `research/0151-0160-production-result.md`.

Still REVIEW — do not bind/promote:
- **0151 ENGINE OIL FILTER**
- **0152 DRIVE BELT**
- **0153 SPARK PLUG**
- **0155 FUEL TANK**
- **0156 FUEL TANK AIR FILTER**
- **0157 FUEL FILTER**
- **0158 BRAKE LINE**
- **0159 BRAKE HOSE**
- **0160 BRAKE PAD**

These terms are verified in Hyundai maintenance text, but stronger directly labeled physical-part visuals are still required. Do not substitute generic web/stock/component imagery.

### Codex action now
1. Pull latest `main`.
2. Bind/display **0154** in the existing BLACK UI without redesign.
3. Do not redo the 0154 crop/source research.
4. Do not promote the REVIEW items above.
5. Deploy and mobile-check; report mismatches by permanent ID.
6. Production % changes only after live BLACK UI + reverse QA.


## CODEX HANDOFF — 2026-09-08 — IDs 0161–0170
Chat Production review is complete for this batch.

No item is promoted to PASS in this pass because Hyundai Owner's Manual evidence currently verifies terminology but does not provide an unmistakable directly labeled physical-part learning image for these underbody components.

REVIEW:
- **0161 BRAKE DISC**
- **0162 BRAKE CALIPER**
- **0163 STEERING GEAR RACK**
- **0164 STEERING LINKAGE**
- **0165 STEERING GEAR BOOT**
- **0166 DRIVESHAFT**
- **0167 DRIVESHAFT BOOT**
- **0168 SUSPENSION BALL JOINT**
- **0169 PROPELLER SHAFT**
- **0170 REAR DIFFERENTIAL**

Source records are in `data/source_registry.json`:
- `HY_LX3_2026_SEVERE_MAINTENANCE`
- `HY_NX4PHEV_2026_BRAKE_MAINTENANCE`

### Codex action
1. Pull latest `main`.
2. Do not fabricate/guess crops from generic underbody imagery.
3. Do not promote these IDs until a direct Hyundai official physical-part image is found.
4. Continue BLACK UI deployment for earlier PASS assets.
5. Production % remains unchanged for this batch.


## PRODUCTION BACKLOG RULE — 2026-09-08
User instruction: if a batch requires hard-to-identify underbody/service imagery and no unmistakable direct Hyundai official visual is available, **defer it and continue forward immediately**.

Operational rule:
- Do not spend multiple passes blocking on one difficult part.
- Mark unresolved items `REVIEW` + `production_backlog: true`.
- Keep permanent IDs unchanged.
- Record the missing visual/source requirement.
- Continue to the next batch.
- Return to backlog after the easy/direct-visual production pass is substantially complete.
- Codex must not promote backlog items from generic/stock/guessed imagery.

Deferred now:
- **0171–0180** all moved to Production Backlog pending direct Hyundai underbody visuals.


## CODEX HANDOFF READY — 2026-09-08 — IDs 0191–0200
Chat Production has completed and committed final assets for:
- **0193 WIPER ARM**
- **0194 REAR WIPER ARM**
- **0195 HOOD LATCH**
- **0196 SECONDARY HOOD RELEASE LEVER** — corrected from HOOD SAFETY LATCH; old term kept as alias.
- **0197 LIFTGATE HANDLE BUTTON**
- **0198 LIFTGATE SUPPORT STRUTS**

Final assets: `images/parts/0193.jpg`–`images/parts/0198.jpg`.
Detailed QA: `research/0191-0200-production-result.md`.

Production Backlog — continue forward, do not block:
- **0191 WINDSHIELD WASHER NOZZLE**
- **0192 REAR WINDOW WASHER NOZZLE**
- **0199 DOOR HINGE**
- **0200 DOOR CHECKER**

### Codex action
1. Pull latest `main`.
2. Bind/display 0193–0198 in BLACK UI without redesign.
3. Do not promote backlog items from generic imagery.
4. Continue deploying earlier PASS assets.
5. Production % only after live BLACK UI + reverse QA.

## CODEX REVERSE QA — 2026-09-08
- Checked every PASS `image` path against the actual file before binding. No PASS image file is missing.
- BLACK UI binds only `status: PASS` items and skips `REVIEW` and `production_backlog: true` items.
- Reverse visual QA moved these ambiguous cards to REVIEW/backlog without replacing Chat assets: **0017, 0059, 0131, 0132, 0133, 0134, 0135, 0195, 0196**.
- All remaining PASS items continue through BLACK UI deploy and mobile verification.


## CODEX HANDOFF READY — 2026-09-08 — IDs 0201–0210
Chat Production has completed and committed final assets for:
- **0201 LICENSE PLATE LIGHT**
- **0203 SIDE REPEATER LIGHT**
- **0204 SIDE MARKER LIGHT**

Final assets:
- `images/parts/0201.jpg`
- `images/parts/0203.jpg`
- `images/parts/0204.jpg`

Detailed QA: `research/0201-0210-production-result.md`.

Production Backlog / taxonomy review — continue forward, do not block:
- **0202 REFLECTOR**
- **0205 DAYTIME RUNNING LIGHT**
- **0206 POSITION LIGHT**
- **0207 FRONT PARKING SENSOR**
- **0208 REAR PARKING SENSOR**
- **0209 SIDE VIEW MIRROR TURN SIGNAL**
- **0210 DOOR SCUFF TRIM**

### Codex action
1. Pull latest `main`.
2. Bind/display 0201, 0203, 0204 in BLACK UI without redesign.
3. Skip backlog/review items above.
4. Continue deploying later PASS items even when IDs are non-contiguous.
5. Production % only after live BLACK UI + reverse QA.


## CODEX HANDOFF READY — 2026-09-08 — IDs 0221–0230
Chat Production has completed and committed final assets for:
- **0226 WHEEL ARCH CLADDING**
- **0227 FENDER**
- **0228 QUARTER PANEL**

Final assets:
- `images/parts/0226.jpg`
- `images/parts/0227.jpg`
- `images/parts/0228.jpg`

Detailed QA: `research/0221-0230-production-result.md`.

Production Backlog — continue forward, do not block:
- **0221 DOOR WEATHERSTRIP**
- **0222 WINDOW WEATHERSTRIP**
- **0223 DOOR SILL**
- **0224 ROCKER PANEL**
- **0225 SIDE SILL GARNISH**
- **0229 COWL TOP COVER**
- **0230 WINDSHIELD MOLDING**

### Codex action
1. Pull latest `main`.
2. Bind/display 0226–0228 in BLACK UI without redesign.
3. Skip backlog items.
4. Continue with later PASS items even when IDs are non-contiguous.
5. Production % only after live BLACK UI + reverse QA.


## CODEX HANDOFF READY — 2026-09-08 — IDs 0231–0260 (30-ID TRIAL)
Chat Production completed a 30-ID trial batch with machine validation and GitHub Actions verification.

PASS:
- **0239 TOWING EYE COVER**
- **0241 SUNROOF GLASS**
- **0255 CLIMATE CONTROL PANEL**
- **0258 AIR INTAKE CONTROL BUTTON**
- **0259 FRONT WINDSHIELD DEFROSTER BUTTON**
- **0260 REAR WINDOW DEFROSTER BUTTON**

Final assets:
- `images/parts/0239.jpg`
- `images/parts/0241.jpg`
- `images/parts/0255.jpg`
- `images/parts/0258.jpg`
- `images/parts/0259.jpg`
- `images/parts/0260.jpg`

Detailed QA:
- `research/0231-0240-production-result.md`
- `research/0241-0250-production-result.md`
- `research/0251-0260-production-result.md`

All remaining IDs in 0231–0260 are REVIEW + Production Backlog and must not block forward production.

### 30-ID validation result
- GitHub Actions workflow: **SUCCESS**
- PASS asset file generation: **SUCCESS**
- PASS image readability check: **SUCCESS**
- 4:3 aspect validation: **SUCCESS**
- suspicious-small-file guard: **PASS**
- source download failures for promoted PASS assets: **0**
- No Production % increment from this handoff alone.

### Codex action
1. Pull latest `main`.
2. Bind/display the six PASS items above in BLACK UI without redesign.
3. Skip all REVIEW/backlog IDs.
4. Continue later PASS items even when IDs are non-contiguous.
5. Mobile-check + reverse-QA before counting Production progress.


## CODEX HANDOFF READY — 2026-09-08 — IDs 0261–0290 (30-ID BATCH)
Chat Production completed the second 30-ID batch with machine validation and GitHub Actions verification.

PASS:
- **0271 SPEEDOMETER**
- **0272 TACHOMETER**
- **0273 FUEL GAUGE**
- **0274 ODOMETER**
- **0277 TURN SIGNAL INDICATOR**
- **0278 GEAR POSITION INDICATOR**
- **0280 DASHBOARD**
- **0281 INFOTAINMENT DISPLAY**

Final assets:
- `images/parts/0271.jpg`
- `images/parts/0272.jpg`
- `images/parts/0273.jpg`
- `images/parts/0274.jpg`
- `images/parts/0277.jpg`
- `images/parts/0278.jpg`
- `images/parts/0280.jpg`
- `images/parts/0281.jpg`

Detailed QA:
- `research/0261-0270-production-result.md`
- `research/0271-0280-production-result.md`
- `research/0281-0290-production-result.md`

All remaining IDs in 0261–0290 are REVIEW + Production Backlog and must not block forward production.

### 30-ID validation result
- GitHub Actions workflow: **SUCCESS**
- PASS asset file generation: **SUCCESS**
- PASS image readability check: **SUCCESS**
- 4:3 aspect validation: **SUCCESS**
- suspicious-small-file guard: **PASS**
- source download failures for promoted PASS assets: **0**
- No Production % increment from this handoff alone.

### Codex action
1. Pull latest `main`.
2. Bind/display the eight PASS items above in BLACK UI without redesign.
3. Skip all REVIEW/backlog IDs.
4. Continue later PASS items even when IDs are non-contiguous.
5. Mobile-check + reverse-QA before counting Production progress.


## CODEX HANDOFF READY — 2026-09-08 — IDs 0291–0320 (THIRD 30-ID BATCH)
Chat Production completed the third 30-ID batch with machine validation and GitHub Actions verification.

PASS:
- **0291 USB DATA PORT**
- **0292 USB CHARGING PORT**
- **0293 12 V POWER OUTLET**
- **0295 WIRELESS CHARGING PAD**

Final assets:
- `images/parts/0291.jpg`
- `images/parts/0292.jpg`
- `images/parts/0293.jpg`
- `images/parts/0295.jpg`

Detailed QA:
- `research/0291-0300-production-result.md`
- `research/0301-0310-production-result.md`
- `research/0311-0320-production-result.md`

All remaining IDs in 0291–0320 are REVIEW + Production Backlog and must not block forward production.

### 30-ID validation result
- GitHub Actions workflow: **SUCCESS**
- PASS asset file generation: **SUCCESS**
- PASS image readability check: **SUCCESS**
- 4:3 aspect validation: **SUCCESS**
- suspicious-small-file guard: **PASS**
- source download failures for promoted PASS assets: **0**
- This is the third consecutive 30-ID batch with no workflow/file-validation error.
- No Production % increment from this handoff alone.

### Codex action
1. Pull latest `main`.
2. Bind/display the four PASS items above in BLACK UI without redesign.
3. Skip all REVIEW/backlog IDs.
4. Continue later PASS items even when IDs are non-contiguous.
5. Mobile-check + reverse-QA before counting Production progress.


## CODEX HANDOFF READY — 2026-09-08 — IDs 0321–0370 (FIRST 50-ID BATCH)
Chat Production completed the first 50-ID batch with source probing, machine validation and GitHub Actions verification.

PASS:
- **0346 AUTO-DIMMING INSIDE REARVIEW MIRROR**
- **0347 RAIN SENSOR**
- **0360 OVERHEAD CONSOLE**

Final assets:
- `images/parts/0346.jpg`
- `images/parts/0347.jpg`
- `images/parts/0360.jpg`

Detailed QA:
- `research/0321-0330-production-result.md`
- `research/0331-0340-production-result.md`
- `research/0341-0350-production-result.md`
- `research/0351-0360-production-result.md`
- `research/0361-0370-production-result.md`

All remaining IDs in 0321–0370 are REVIEW + Production Backlog and must not block forward production.

### 50-ID validation result
- GitHub Actions workflow: **SUCCESS**
- PASS asset file generation: **SUCCESS**
- PASS image readability check: **SUCCESS**
- 4:3 aspect validation: **SUCCESS**
- suspicious-small-file guard: **PASS**
- promoted PASS source failures: **0**
- Source probe additionally caught invalid candidate URLs before promotion; failed probes were moved to Backlog rather than promoted.
- No Production % increment from this handoff alone.

### Codex action
1. Pull latest `main`.
2. Bind/display 0346, 0347 and 0360 in BLACK UI without redesign.
3. Skip all REVIEW/backlog IDs.
4. Continue later PASS items even when IDs are non-contiguous.
5. Mobile-check + reverse-QA before counting Production progress.


## MOBILE VIEWPORT FIX — 2026-09-08
- User reported the learning action clipped below mobile browser chrome and requested removal of the Korean part name.
- `index.html` now hides the Korean part-name line, fits the mobile shell to 100dvh (100svh fallback), reserves space for controls and scales the image area with object-fit: contain.
- English title wraps; long explanations scroll inside the card. Short landscape view uses an image/copy split.
- Content IDs, production status and image assets are unchanged.
- Implementation commit: 7a8f8c4. Real iPhone verification remains pending; local browser executable was unavailable. No production progress increment.


## CODEX LIVE DEPLOY VERIFIED — 2026-09-08
- Verified and deployed **147 PASS cards (29.4%)** in the BLACK UI.
- Exact verified IDs: **0011–0016, 0018–0027, 0030–0039, 0041, 0043–0054, 0056–0058, 0060–0069, 0071–0078, 0081–0118, 0120–0124, 0126–0130, 0136, 0140–0143, 0146, 0148, 0154, 0193–0194, 0197–0198, 0201, 0203–0204, 0226–0228, 0239, 0241, 0255, 0258–0260, 0271–0274, 0277–0278, 0280–0281, 0291–0293, 0295, 0346–0347, 0360**.
- iPhone 13 QA: swipe advanced 0011 → 0012; card counter showed 2 / 147; viewport width and document width were both 390 px.
- REVIEW and production backlog items are excluded from the learning deck.
- Live URL: https://sywee-42880999.github.io/car-master/


## NEXT BATCH BLOCKER — 2026-09-08 — IDs 0371–0420
- Requested next production range: **0371–0420**.
- Verified latest `main`, `data/master.json`, `data/id_registry.json`, `data/source_registry.json`, WORK_QUEUE handoff history, repository code search, commit search, and branch list.
- Permanent IDs **0371–0420 are reserved in `data/id_registry.json`**, but there is **no existing English/Korean term mapping for those IDs** in `data/master.json`, repository history, branches, or recovered prior project context.
- Do **not** invent new terms or attach arbitrary parts to these IDs. This would violate the permanent-ID rule.
- No image Production, PASS promotion, Backlog promotion, UI redesign, or Production % change was made for 0371–0420.
- Resume only from the authoritative 0371–0420 term mapping if/when it is recovered or explicitly established.


## 0371–0420 TERM RECOVERY / VALIDATION — 2026-09-08
User clarified the missing-ID rule:
- If only one or two IDs are missing, hide/defer those IDs and continue.
- If a large range is missing, validate the content and create the missing term mapping.

Applied to 0371–0420:
- All 50 permanent IDs remain unchanged.
- Created validated English/Korean term mapping for **0371–0420** from Hyundai official Owner's Manual terminology.
- Added official source families and image keys to `data/source_registry.json`.
- Added detailed 10-ID production-result files:
  - `research/0371-0380-production-result.md`
  - `research/0381-0390-production-result.md`
  - `research/0391-0400-production-result.md`
  - `research/0401-0410-production-result.md`
  - `research/0411-0420-production-result.md`
- Current environment could verify official pages/image keys but could not fetch the image binaries (DNS/network failure in the binary execution environment).
- Therefore **no item was falsely promoted to PASS**. All 0371–0420 are currently REVIEW + Production Backlog until exact official source binaries are fetched, cropped 4:3 and reverse-QA'd.
- Dedicated/direct-image candidates exist especially in airbag, EV charging and hybrid high-voltage sections; resume from the registered exact image keys rather than redoing taxonomy research.
- Previous "missing term mapping blocker" is superseded by this section.
- BLACK UI unchanged. Production % unchanged.


## CODEX HANDOFF READY — 2026-09-08 — IDs 0371–0420 (SECOND 50-ID BATCH)
Large missing range was validated and rebuilt from Hyundai official Owner's Manual terminology, then direct-image production was run through GitHub Actions.

PASS:
- **0376 DRIVER'S KNEE AIRBAG**
- **0398 CHARGE INDICATOR LIGHT**
- **0399 CHARGING LABEL**
- **0408 HYBRID POWER CONTROL UNIT**
- **0409 HIGH VOLTAGE BATTERY**
- **0413 HYBRID BATTERY COOLING DUCT**

Final assets:
- `images/parts/0376.jpg`
- `images/parts/0398.jpg`
- `images/parts/0399.jpg`
- `images/parts/0408.jpg`
- `images/parts/0409.jpg`
- `images/parts/0413.jpg`

Detailed QA:
- `research/0371-0380-production-result.md`
- `research/0381-0390-production-result.md`
- `research/0391-0400-production-result.md`
- `research/0401-0410-production-result.md`
- `research/0411-0420-production-result.md`
- `research/0371-0420-production-pass2.md`

All remaining **44 IDs** in 0371–0420 are REVIEW + Production Backlog and must not block forward production.

### 50-ID validation result
- GitHub Actions production workflow: **SUCCESS** (run #71)
- PASS source download failures: **0**
- PASS image readability: **SUCCESS**
- 4:3 aspect validation: **SUCCESS**
- suspicious-small-file guard: **PASS**
- BLACK UI design unchanged.
- Production % only after live BLACK UI deploy/mobile reverse-QA.

### Codex action
1. Pull latest `main`.
2. Bind/display the six PASS items above in existing BLACK UI without redesign.
3. Skip all REVIEW/backlog IDs.
4. Continue later PASS items even when IDs are non-contiguous.
5. Mobile-check + reverse-QA before counting Production progress.
