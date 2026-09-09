# CAR MASTER — FINAL CODEX HANDOFF

Date: 2026-09-09
Repository: `sywee-42880999/car-master`
Branch: `main`
Starting main observed before this handoff: `6586662a46dfdca8bc0b1d11ea50a8c5e471a3e5`

## Current candidate state
- Permanent IDs `0001–0500` are all allocated.
- `data/master.json` currently has image paths and PASS candidate state across the full 500-card set.
- A repository search found no current `status: REVIEW` entries.
- This means **500/500 image candidates are prepared**, not automatically 100% live Production.

## Do not undo newer UI/test work
The current main already includes newer Codex/UI work, including commit `6586662a46dfdca8bc0b1d11ea50a8c5e471a3e5` (`Use primary US term for exact-input test answers`). Preserve those newer changes. Do not reset main to an older production commit.

## Your job now
Do NOT redo the 500-card image-production pass from scratch.

Perform a full final verification pass:
1. Pull latest `main`.
2. Read `WORK_QUEUE.md`, this file, `data/master.json`, `data/source_registry.json`, and recent `research/backlog-recovery-*` files.
3. Bind/rebind current `images/parts/<ID>.jpg` blobs to the BLACK learning UI wherever needed. Do not use cached/older blobs.
4. Reverse-QA every card as:
   **English term -> exact physical component/location/icon -> displayed image.**
5. Mobile-check the BLACK UI, especially iPhone-width layout, image containment, title wrapping, and no horizontal clipping.
6. Preserve the approved BLACK UI. Do not redesign it.
7. Preserve the current exact-input test logic and current terminology normalization unless a real bug is found.
8. If a card fails, move ONLY that exact ID back to REVIEW/backlog, record the concrete reason, and leave unrelated PASS cards untouched.
9. Do not silently substitute a different generic image for a failed card.
10. After fixes, deploy GitHub Pages and report the actual live-verified count.

## Highest-priority reverse-QA groups
### A. Original mechanical / underbody schematics
Check visual separation carefully:
- brake pad / brake disc / brake caliper
- steering rack / steering gear boot / steering linkage
- driveshaft / driveshaft boot / propeller shaft
- front differential / rear differential / transfer case
- shock absorber / coil spring / strut / strut mount
- lower control arm / upper control arm / ball joint
- stabilizer bar / stabilizer link
- wheel hub / wheel bearing / steering knuckle
- subframe / crossmember / under cover / mud guard
- front suspension / rear suspension

### B. Door / seat-belt / trim schematics
Check:
- door hinge / checker / striker / latch / lock actuator
- seat-belt tongue / retractor / guide / pretensioner
- door weatherstrip / window weatherstrip / door glass run / door seal
- front vs rear door frame
- liftgate / hood / cowl weatherstrip
- windshield / roof / roof-drip molding
- sunroof wind deflector vs sunroof drain

### C. Conceptual display cards
Strictly check:
- `0275 TRIP COMPUTER`
- `0276 WARNING LIGHT`
- `0279 DRIVER INFORMATION DISPLAY`
- `0465 I-PEDAL INDICATOR`

If any of these are too generic to teach the exact term, hold the exact ID rather than forcing PASS.

### D. SRS sensor cards
Highest-risk group:
- `0369 FRONT IMPACT SENSOR`
- `0370 SIDE IMPACT SENSOR`
- `0371 SRS CONTROL MODULE`
- `0372 ROLLOVER SENSOR`
- `0373 SEAT BELT BUCKLE SENSOR`
- `0374 SIDE IMPACT PRESSURE SENSOR`
- `0375 SIDE IMPACT ACCELERATION SENSOR`

These require especially strict location/function QA.

### E. Charging cards
Check that these remain visibly distinct:
- `0397 CHARGING INLET`
- `0493 CHARGING PORT CAP`
- `0494 DC CHARGING INLET`
- `0495 AC CHARGING INLET`
- `0496 CHARGING CONNECTOR LOCK`
- `0400 CHARGING CONNECTOR`
- `0401 CHARGING CONNECTOR UNLOCK BUTTON`
- `0497 CHARGING CONNECTOR RELEASE BUTTON`

### F. Duplicate/synonymous physical-hardware cases
Check taxonomy and UI behavior rather than automatically rejecting duplicates:
- `0294 / 0353 AC POWER OUTLET`
- `0191 / 0192 washer nozzle terms`
- `0324 / 0363 SEAT BELT RETRACTOR`
- `0330 / 0364 SEAT BELT GUIDE`
- repeated gauge/charging/USB terms where the master intentionally contains location or terminology variants.

## Reporting format
When complete, append a new section to `WORK_QUEUE.md` with:
- live BLACK UI verified count / 500
- exact held IDs, if any
- one-line reason per held ID
- mobile QA result
- GitHub Pages deploy status
- commit SHA used for final verification

Do not call 500/500 Production complete until live BLACK UI + mobile + reverse-QA are all finished.
