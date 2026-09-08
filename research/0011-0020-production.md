# CAR MASTER — Production Correction Handoff (IDs 0011–0020)

Purpose: replace visually ambiguous deployed crops with images where the physical part itself is unmistakable. Do **not** increment Production progress for this handoff. Current PASS flags in data are not proof of visual correctness; re-check each live card against the criteria below.

General rule: prefer a dedicated Hyundai Owner’s Manual page/image over a broad exterior overview. If a tight crop can make the part self-evident, use no marker. If context is required, use HTML overlay only; never bake a marker into JPG.

## 0011 — DOORS
- Official page: https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/idc96f2f531d7.html
- Image key: `1C_OutsideVehicleRearOverview`
- Must visibly show: one complete passenger door panel as a physical body panel, including enough of the window/handle/body seams to read clearly as a door.
- Preferred crop: 4:3 side/rear-side crop centered on a single complete door; avoid a whole-car crop where the door is too small.
- PASS: a reviewer can identify “door” without relying on the label or marker.
- REVIEW: crop shows mostly whole vehicle, window, handle, or body side with the door boundaries unclear.

## 0012 — FUEL FILLER DOOR
- Official page: https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/topic_wwh_zrb_5cc.html
- Image key: `2C_FuelInletDoor`
- Must visibly show: the exterior fuel filler door itself, not only the cap/filler neck.
- Preferred crop: tight 4:3 crop around the closed or clearly hinged filler door with surrounding quarter panel for location context.
- PASS: filler-door outline/hinge/opening is unmistakable.
- REVIEW: image mainly shows fuel cap, nozzle, fuel text, or a broad vehicle overview.

## 0013 — ELECTRIC CHARGING DOOR
- Official page: https://ownersmanual.hyundai.com/full_webhelp/NE1a/2025/en_US/topic_myd_hwf_hcc.html
- Image key: `2C_HowToUseChargingDoor`
- Official PDF alternate: https://www.hyundai.com/content/dam/hyundai/in/en/data/connect-to-service/owners-manual/new/ioniq5oct2022-present.pdf
- Must visibly show: the vehicle’s exterior charging door/flap as a physical panel.
- Preferred crop: tight exterior 4:3 crop showing the charging door open/closed with body-panel context; do not crop down to connector/socket only.
- PASS: the charging door panel is the obvious subject.
- REVIEW: only charge port/socket/plug is visible, or the flap is too small to identify.

## 0014 — REAR COMBINATION LIGHTS
- Official page: https://ownersmanual.hyundai.com/full_webhelp/NX4a/2026/en_US/idd90d669cdbf.html
- Preferred image keys: `2C_RearLampOverview`, then `2C_RearLampOverview_2`
- Must visibly show: the complete rear combination lamp assembly as one lamp unit, not a single bulb/function.
- Preferred crop: tight 4:3 crop containing the full lamp housing and a small amount of adjacent body panel.
- PASS: full rear lamp assembly/housing is unmistakable.
- REVIEW: crop isolates only reverse lamp, reflector, bulb access, or too much of the whole rear vehicle.

## 0015 — REVERSE LIGHTS
- Official page: https://ownersmanual.hyundai.com/full_webhelp/MX5a/2024/en_US/idd90d669cdbf.html
- Preferred image keys: `2C_BackupLampChange1`, `2C_BackupLampChange2`; use `2C_RearLampOverview` only if the reverse-light location remains unambiguous.
- Must visibly show: the actual reverse/backup light unit or clearly identified reverse-light section, not the whole combination lamp.
- Preferred crop: tight 4:3 detail of the backup/reverse lamp area with just enough bumper/lamp context to locate it.
- PASS: reverse lamp is visually distinct from tail/stop/turn lamp elements.
- REVIEW: only the complete combination lamp is visible with no clear reverse-light distinction.

## 0016 — LIFTGATE
- Official page: https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/idc96f2f531d7.html
- Image key: `1C_OutsideVehicleRearOverview`
- Must visibly show: the complete rear liftgate panel/opening as the movable rear body closure.
- Preferred crop: 4:3 rear crop including liftgate perimeter, rear glass, and lower gate edge; exclude excessive surrounding vehicle.
- PASS: liftgate boundaries and full closure panel are readable immediately.
- REVIEW: crop mainly shows rear window, camera, lamp, spoiler, or an undifferentiated whole rear view.

## 0017 — WIDE-REAR VIEW CAMERA
- Official page: https://ownersmanual.hyundai.com/full_webhelp/AXEV/2025/en_GN/id2c732e6188a.html
- Preferred image key: `2C_WideRearViewCamera`; alternate `2C_WideRearCamera`
- Must visibly show: the physical rear camera lens/module.
- Preferred crop: tight 4:3 close-up of the camera module with nearby garnish/handle/plate-area context so the lens is identifiable.
- PASS: camera lens/module is unmistakable as the subject.
- REVIEW: crop shows only rear view on a screen, liftgate handle, plate lamp, or a distant rear overview.

## 0018 — ANTENNA
- Official page: https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/id4d018a844fc.html
- Image key: `2C_Antenna`
- Must visibly show: the exterior roof antenna/shark-fin unit itself.
- Preferred crop: tight 4:3 roof crop with the complete antenna centered and enough roof surface for context.
- PASS: antenna housing is large and unmistakable.
- REVIEW: antenna is tiny in a whole-car/rear-overview image or confused with roof rail/spoiler.

## 0019 — REAR WINDOW WIPER BLADE
- Official page: https://ownersmanual.hyundai.com/full_webhelp/LX2/2025/en_US/id018ad5fe2f4.html
- Preferred image keys: `B0452KO05`, `B0452KO06`
- Source image filenames: `B0452KO05.eps.png`, `B0452KO06.eps.png`
- Must visibly show: the rear wiper **blade**, ideally attached to the rear wiper arm on rear glass.
- Preferred crop: tight 4:3 crop of the blade and arm against the rear window; blade should occupy meaningful frame area.
- PASS: blade shape/rubber wiping element is visually identifiable.
- REVIEW: only rear glass, whole rear vehicle, wiper motor/arm base, or a very small wiper silhouette is visible.

## 0020 — HIGH MOUNTED STOP LIGHT
- Official page: https://ownersmanual.hyundai.com/full_webhelp/NX4/2025/en_US/idce7496c4cd1.html
- Image key: `2C_HighMountedStopLamp`
- Must visibly show: the high-mounted stop lamp unit at the upper rear/spoiler area.
- Preferred crop: tight 4:3 crop around the upper rear lamp with a small amount of spoiler/rear-glass context.
- PASS: the high-mounted lamp itself is the obvious subject and separated from rear combination lamps.
- REVIEW: crop is a broad rear view where the lamp is tiny, or shows spoiler without the lamp clearly.

## Re-production order
1. Rebuild 0012, 0013, 0014, 0015, 0017, 0018, 0019, 0020 first from their dedicated official pages/images.
2. Rebuild 0011 and 0016 from the LX3 overview only with sufficiently tight, self-evident crops; if either still reads ambiguously, keep REVIEW and search a stronger dedicated Hyundai source before rebinding.
3. Reverse QA each candidate: English term → physical part → crop. If the part cannot be identified without reading the card title, it is not PASS.
4. Replace `images/parts/<ID>.jpg` only after the new crop meets PASS; then verify the live BLACK card on mobile.
5. Do not change `data/progress.json` or Production percentage as part of this correction handoff.
