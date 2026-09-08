# CAR MASTER — CODEX EXECUTION INSTRUCTIONS

Updated: 2026-09-08

Codex must treat GitHub `main` as the source of truth. Do not rely on chat memory.

## 1. Start every run like this
1. Pull latest `main`.
2. Read:
   - `WORK_QUEUE.md`
   - `data/master.json`
   - `data/source_registry.json`
   - latest `research/*-production-result.md`
3. Do not say “there is nothing” before checking the PASS items and `images/parts/`.

## 2. What already exists
Chat has already produced many final 4:3 Production assets and committed them under:
- `images/parts/<PERMANENT_ID>.jpg`

The authoritative PASS/REVIEW state is in:
- `data/master.json`

The Chat→Codex handoff list is appended in:
- `WORK_QUEUE.md`

The source registry is:
- `data/source_registry.json`

Do NOT redo source research or crop work for PASS items.

## 3. Codex job
For every PASS item that has `image: images/parts/XXXX.jpg` in `data/master.json`:
1. Bind that item to the existing BLACK learning UI.
2. Preserve the approved BLACK design. No redesign.
3. Preserve permanent ID exactly.
4. Use the existing image path. Do not substitute another image.
5. Keep Part Learning / 4-choice / Mixed Test behavior.
6. Deploy GitHub Pages.
7. Verify on mobile-sized viewport.
8. Reverse QA: English term → intended physical part → displayed image.
9. If mismatch exists, report the exact permanent ID in `WORK_QUEUE.md`; do not silently replace the asset.

## 4. REVIEW / Production Backlog
If an item is `REVIEW` or has `production_backlog: true`:
- Do not promote it.
- Do not guess from generic images.
- Skip it and continue with later PASS items.
- Backlog items are intentionally deferred.

## 5. Current forward-production rule
Difficult underbody/service items are not blockers.
Chat will continue forward and mark unresolved IDs as Production Backlog.
Codex should therefore deploy PASS items even when IDs in between are REVIEW.

## 6. Progress rule
Do not increase Production % just because files exist in GitHub.
Only count an item after:
- final asset exists
- data bind is correct
- BLACK UI displays it
- deploy succeeds
- mobile check passes
- reverse QA passes

## 7. Important correction
For 0122/0123/0124, use the latest current blobs only. Earlier identical overview crops are obsolete.
- 0122 COMPRESSOR
- 0123 SEALANT BOTTLE
- 0124 PRESSURE GAUGE

Always pull latest `main` before deploy.

## 8. If Codex thinks something is missing
Before stopping:
1. Check `data/master.json` for the ID and `image` field.
2. Check that exact path under `images/parts/`.
3. Check `WORK_QUEUE.md` for the latest handoff section.
4. Check `research/<batch>-production-result.md`.
5. Check `data/source_registry.json`.

If the PASS image truly does not exist after those checks, append:
`CODEX BLOCKER — ID XXXX — missing <exact file/path>`
to `WORK_QUEUE.md`, then continue other PASS items.

## 9. Never do these
- Never renumber IDs.
- Never replace the root app with an admin page.
- Never redesign BLACK UI during content production.
- Never promote REVIEW items.
- Never use stock/generic images to fill gaps.
- Never redo Chat crop/source work unless a specific ID is reported as wrong.
- Never stop the whole batch because one ID is missing.

## 10. Immediate execution target
Continue from latest `main` and process all currently un-deployed PASS items in `data/master.json`.
Skip REVIEW/backlog items.
Deploy, mobile-check, reverse-QA, then write exact verified IDs back to `WORK_QUEUE.md`.
