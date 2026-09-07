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

## Next queue

Process permanent IDs 0011–0020 from `data/master.json`. Apply results directly to CAR MASTER. Preserve 0001–0010. Update `data/progress.json` after completion.

## Instruction for any new chat

Read this file plus `data/master.json` and `data/progress.json` before continuing. Do not rely on conversational memory when repository state is available.
