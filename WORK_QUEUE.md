# CAR MASTER — SHARED WORK QUEUE

This file is the single handoff board between ordinary ChatGPT and ChatGPT Work.

## Current status

- Progress: **2%** (10/500)
- Completed: 0001–0010
- Current batch: 0011–0020
- Repository: `sywee-42880999/car-master`
- Branch: `main`

## Fixed objective

Produce a 500-entry **Automotive Visual Vocabulary / Wordbook** using Hyundai official Owner's Manual PDFs as the primary source. This is not a game.

## Permanent rules

1. Every term has a permanent four-digit ID. Never renumber an ID.
2. Search the full manuals and compare candidates instead of using the first image found.
3. Prefer the original embedded PDF image/drawing. Do not render pages when extraction is possible.
4. Use a clean 4:3 JPG. Do not enlarge weak sources.
5. Prefer a clear close-up. If the part fills the crop, no marker is required.
6. If context is necessary, use HTML overlays only:
   - precise small part: red dot;
   - multiple clearly visible parts: multiple red dots;
   - broad surface: isolated soft red oval blur.
7. Never bake markers into the JPG.
8. Verify manual numbering/description before locating a part.
9. Ambiguous items must be `REVIEW`, never guessed.
10. Automatic reverse QA: English term → actual part → image → marker.
11. Directly update CAR MASTER. Do not post contact sheets or request routine approval.
12. In chat, report only the overall progress, e.g. `30%`.

## Low-cost workflow

- Ordinary ChatGPT: terminology, candidate-page research, duplicate review, ID-safe work instructions.
- ChatGPT Work: embedded-image extraction, 4:3 crops, HTML/data updates, GitHub writes.
- Batch GitHub writes in groups of 50–100 where practical.
- Use `data/master.json` as the ID authority and `data/progress.json` as the status authority.

## Ordinary ChatGPT research — IDs 0011–0020

Status: terminology checked, duplicate relationships reviewed, Hyundai official manual candidates identified, extraction/crop instructions prepared. Permanent IDs unchanged.

### Best primary candidate set

Use **2026 Hyundai Palisade (LX3) US Owner's Manual / official Hyundai web manual** rear exterior overview as the first consolidated source for 0011, 0012, 0014–0020. It explicitly labels:
- Door
- Fuel filler door
- Rear combination light
- Reverse light
- Liftgate
- Wide-rear view camera
- Antenna
- Rear window wiper blade
- High mounted stop light

Official page: `https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/idc96f2f531d7.html`
Image key: `1C_OutsideVehicleRearOverview`

For individual close-ups / stronger source drawings, prefer the following official Hyundai pages before falling back to the consolidated overview.

### 0011 — DOORS / 도어
- Terminology: PASS. Broad plural category; Hyundai overview labels singular `Door`, but master plural `DOORS` is acceptable as vocabulary category.
- Duplicate check: no duplicate in 0001–0020.
- Candidate: LX3 rear exterior overview, image `1C_OutsideVehicleRearOverview`.
- Work spec: crop a clearly identifiable side/rear passenger door area. Because `DOORS` is a broad surface category, use a soft red oval HTML overlay only if the crop still contains competing body panels. No baked marker.

### 0012 — FUEL FILLER DOOR / 연료 주입구 도어
- Terminology: PASS; exact Hyundai term.
- Duplicate check: distinct from 0011 DOORS.
- Best close-up candidate: `https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/topic_wwh_zrb_5cc.html`
- Image key: `2C_FuelInletDoor` (closed exterior door), with opening sequence available on same topic.
- Alternate: 2025 Tucson official manual, `2C_FuelInletDoor` / `2C_FuelInletDoorOpen`.
- Work spec: use closed-door exterior image if possible; tight crop, no marker if panel fills crop. If overview is used, soft red oval HTML overlay.

### 0013 — ELECTRIC CHARGING DOOR / 충전구 도어
- Terminology: PASS; exact official Hyundai heading `Electric Charging Door`.
- Duplicate check: related to 0012 but NOT duplicate; ICE fuel door vs EV charging door must remain separate IDs.
- Primary PDF candidate: Hyundai India IONIQ 5 official Owner's Manual: `https://www.hyundai.com/content/dam/hyundai/in/en/data/connect-to-service/owners-manual/new/ioniq5oct2022-present.pdf`
- Official web candidate: `https://ownersmanual.hyundai.com/full_webhelp/NE1a/2025/en_US/topic_myd_hwf_hcc.html`
- Image key shown by official web manual: `2C_HowToUseChargingDoor`.
- Work spec: prefer exterior/door panel view over connector-only view. Tight crop, no marker when charging door fills crop; otherwise soft red oval HTML overlay.

### 0014 — REAR COMBINATION LIGHTS / 리어 콤비네이션 램프
- Terminology: PASS. Hyundai pages commonly use singular heading `Rear combination light`; master plural is acceptable for paired exterior lamps.
- Duplicate check: 0015 REVERSE LIGHTS is a subcomponent/function of rear lamp assembly on many models, but is NOT a duplicate.
- Candidate: `https://ownersmanual.hyundai.com/full_webhelp/NX4a/2026/en_US/idd90d669cdbf.html`
- Best overview image key: `2C_RearLampOverview` / `2C_RearLampOverview_2` depending type.
- Work spec: select an image where the complete lamp assembly is visually obvious, not a bulb-removal detail. Tight crop; no marker if assembly fills crop.

### 0015 — REVERSE LIGHTS / 후진등
- Terminology: PASS with note. Official Hyundai wording is usually singular `Reverse light` or `Back up light`; keep permanent master wording unchanged unless a later editorial normalization pass explicitly changes text without changing ID.
- Duplicate check: not duplicate of 0014; treat as specific lamp within/near rear combination lighting.
- Strong candidate: LX3 2026 rear exterior overview explicitly labels `Reverse light` separately.
- Alternate detailed candidate: MX5a 2024 official page `https://ownersmanual.hyundai.com/full_webhelp/MX5a/2024/en_US/idd90d669cdbf.html`, image `2C_RearLampOverview`, with reverse-light replacement images `2C_BackupLampChange1` and `2C_BackupLampChange2`.
- Work spec: avoid replacement/socket-only crop for vocabulary if exterior lamp location is available. If overview retained, use precise red dot HTML overlay on the reverse lamp.

### 0016 — LIFTGATE / 리프트게이트
- Terminology: PASS for US Hyundai wording. Some global manuals use `Tailgate`; do not rename ID based on regional wording.
- Duplicate check: none.
- Candidate: LX3 2026 rear exterior overview, image `1C_OutsideVehicleRearOverview`, explicitly labels `Liftgate`.
- Work spec: broad panel. Prefer crop where the entire liftgate outline is obvious; soft red oval HTML overlay only if needed to distinguish from rear glass/lamps.

### 0017 — WIDE-REAR VIEW CAMERA / 광각 후방 카메라
- Terminology: PASS; exact official Hyundai wording includes hyphenated `Wide-rear view camera`.
- Duplicate check: distinct from 0010 FRONT VIEW CAMERA.
- Best dedicated candidate: `https://ownersmanual.hyundai.com/full_webhelp/AXEV/2025/en_GN/id2c732e6188a.html`
- Image key: `2C_WideRearViewCamera`.
- Alternate: Surround View Monitor pages with `2C_WideRearCamera`.
- Work spec: this is a precise small part. Use close-up with no marker if camera itself is unmistakable; otherwise single red dot HTML overlay exactly on lens/module.

### 0018 — ANTENNA / 안테나
- Terminology: PASS.
- Duplicate check: none.
- Best dedicated candidate: `https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/id4d018a844fc.html`
- Image key: `2C_Antenna`.
- Work spec: prefer exterior roof antenna/shark-fin portion, not hidden dashboard antenna. Tight 4:3 crop, no marker if isolated.

### 0019 — REAR WINDOW WIPER BLADE / 후면 와이퍼 블레이드
- Terminology: PASS. Official manuals use both plural in overview and singular in replacement heading; permanent master singular is clear.
- Duplicate check: distinct from 0003 FRONT WIPER BLADES.
- Dedicated close-up candidate: `https://ownersmanual.hyundai.com/full_webhelp/LX2/2025/en_US/id018ad5fe2f4.html`
- Image keys: `B0452KO05`, `B0452KO06`.
- Alternate overview: LX3 2026 `1C_OutsideVehicleRearOverview`.
- Work spec: prefer intact rear wiper blade on rear glass rather than detached replacement step if both are available. Tight crop, no marker if obvious.

### 0020 — HIGH MOUNTED STOP LIGHT / 보조 제동등
- Terminology: PASS; exact Hyundai term.
- Duplicate check: distinct from 0014 rear combination lamps.
- Dedicated candidate: `https://ownersmanual.hyundai.com/full_webhelp/NX4/2025/en_US/idce7496c4cd1.html`
- Image key: `2C_HighMountedStopLamp`.
- Alternate: NE1a 2025 same image key.
- Work spec: crop rear spoiler/upper rear-glass lamp so the stop light is unmistakable. No marker if isolated; otherwise one precise red dot/short-area overlay in HTML only.

### Batch QA / handoff rules for Work

1. Preserve IDs 0011–0020 exactly; never renumber.
2. Prefer official Hyundai PDF embedded assets when a downloadable PDF counterpart is available; use web-manual image keys above to locate the correct drawing before extraction.
3. For 0014 vs 0015, verify the full assembly vs reverse-light subcomponent visually; do not reuse the same crop unless the overlays make the distinction unambiguous.
4. For 0012 vs 0013, never substitute fuel filler door for EV charging door or vice versa.
5. For 0016, regional `Tailgate` wording is an alias only; master remains `LIFTGATE`.
6. For 0017, confirm camera lens/module rather than license-plate lamp or handle button.
7. For 0018, use the exterior antenna, not the hidden crash-pad antenna.
8. Run reverse QA English term → physical part → crop → HTML marker before PASS.
9. If source geometry or labeling is ambiguous, set `REVIEW`; do not guess.
10. After Work creates/extracts the final 0011–0020 assets and updates CAR MASTER, update `data/progress.json` to 20/500 = 4% only when all ten are actually complete.

## Next queue

Work should now execute permanent IDs 0011–0020 using the research/spec above. Preserve 0001–0010. Update `data/progress.json` only after asset/data completion.

## Instruction for any new chat

Read this file plus `data/master.json` and `data/progress.json` before continuing. Do not rely on conversational memory when repository state is available.
