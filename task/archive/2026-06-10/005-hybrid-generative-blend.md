---
title: "Hybrid generative blend pipeline"
type: execution
detail: "Two-phase place-then-generate workflow so designed views integrate Lamsam tree naturally into 3D renders while keeping placement coords"
tags: [design, generative, blend, placement, multi-view]
created: 2026-06-10
updated: 2026-06-10
---

# Hybrid generative blend pipeline

Related: [task/index.md](index.md) · [004-improve-multi-view-plant-placement](./004-improve-multi-view-plant-placement.md)

## Task Requirement

- Goal: Fix "pasted photo" look from Task 004 `place` output by adding a generative blend phase that re-renders the tree into each 3D view style, while keeping coordinate precision from the placement registry.
- Problem: Pillow overlay pastes a real-photo tree cutout onto CGI renders — mismatched lighting, perspective, and background.
- In scope:
  - Update workflow docs: Phase 1 `place` → placement guide; Phase 2 `generate_image` → final `_designed.png`.
  - Extend `process_image.py` with `--guide-dir` for non-destructive guide output.
  - Regenerate all 5 visibility-matrix views for `lamsam-front-right` using hybrid pipeline.
  - Update SKILL.md and AGENTS.md to clarify roles: `place` = position guide, `generate_image` = visual blend.
- Out of scope: Training custom models; changing placement coordinates (use existing anchors).

## Checklist

- [x] T001 [U] Update `design/WORKFLOW.md` with mandatory 2-phase hybrid pipeline
  - ✅ Documented Phase 1 guide + Phase 2 generative blend as mandatory; guides in `design/guides/`.
- [x] T002 [N] Add `--guide-dir` option to `place` command (guides without overwriting finals)
  - ✅ `place --guide-dir design/guides` writes `{viewId}_guide.png` without touching `_designed.png`.
- [x] T003 [N] Run placement guides for all 5 views → `design/guides/`
  - ✅ Generated front-low, front-high, front-center, garage-front, garage-right guides.
- [x] T004 [N] Generative blend all 5 views with `generate_image` (raw + tree ref + guide + anchored prompt)
  - ✅ Blended all 5 views with normX/normY anchored prompts and 3 reference images each.
- [x] T005 [U] Copy blended outputs to `resources/*_designed.png`
  - ✅ Copied 5 blended PNGs to `resources/`.
- [x] T006 [U] Update `image-processor` SKILL.md and AGENTS.md rules for hybrid workflow
  - ✅ SKILL section 3 hybrid rules; AGENTS.md mandates 2-phase pipeline.
