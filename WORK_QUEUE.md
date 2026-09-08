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
