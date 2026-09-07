# CAR MASTER — SHARED WORK QUEUE

This file is the single source of truth and handoff board for ordinary ChatGPT and ChatGPT Work.

## Current status
- Progress: **2%** (10/500)
- Completed: 0001–0010
- Current production batch: 0011–0020
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

## Definition of DONE
An item is DONE only when: terminology is verified + source recorded + final image/crop exists + correct live Black UI item displays + reverse QA passes. GitHub data without live display is not DONE.

## Instruction for every new Chat or Work session
Read `WORK_QUEUE.md`, `data/master.json`, `data/progress.json`, and `data/source_registry.json` first. Continue from repository state. Write all material decisions/changes back to GitHub before handoff.