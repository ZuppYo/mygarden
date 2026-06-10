---
title: "Placement picker UX and 3D occlusion"
type: planning
detail: "Fix Placement Picker button layout, enable all-view picking, and add per-view 3D occlusion so hidden angles do not show the tree"
tags: [placement, occlusion, 3d, ui, multi-view]
created: 2026-06-10
updated: 2026-06-10
---

# Placement picker UX and 3D occlusion

Related: [task/index.md](index.md) · [004-improve-multi-view-plant-placement](./004-improve-multi-view-plant-placement.md) · [005-hybrid-generative-blend](./005-hybrid-generative-blend.md) · [design/WORKFLOW.md](../design/WORKFLOW.md)

## Task Requirement

- Goal: Fix three remaining gaps after Task 005 — Placement Picker UX, single-view limitation, and incorrect 3D layering where occluded viewpoints still show the tree.
- Problems:
  1. **Button layout** — `📍 Placement Picker` sits inside `.search-box` beside the search input; on wrap/narrow layout it drops below the text field and feels detached from controls.
  2. **Single-view picker** — hardcoded to `หน้าบ้านมุมต่ำ` with fixed `2153×1228`; cannot pick anchors on garage, side, or other views.
  3. **No 3D occlusion** — `visibility-matrix.json` uses zone rules only (worldX > 0.5 → 5 views). No per-view depth/occluder logic; tree appears even when house wall, gate, or carport should block it from that camera.
- In scope:
  - Relocate Placement Picker toggle to header toolbar (alongside Design/Raw mode).
  - Multi-view picker: dropdown of all `view-anchors.json` views (or all 13 resources), dynamic image size, per-view JSON export.
  - Occlusion system: `design/occluders.json` + per-placement per-view `visible` flag derived from world position vs occluder regions.
  - Update hybrid blend pipeline (guide + `generate_image`) to skip or prompt-hide tree on occluded views.
  - Update `design/WORKFLOW.md` and `image-processor` SKILL.md.
- Out of scope:
  - Full NeRF / Gaussian Splatting reconstruction.
  - Automatic ML occlusion (MVTracker-style); use lightweight manual occluder regions first.

## Checklist

- [x] T001 [U] Move `📍 Placement Picker` toggle from `.search-box` to header toolbar (no wrap under search input)
  - ✅ Toggle moved to header next to Design/Raw mode badge.
- [x] T002 [N] Add view selector dropdown to Placement Picker — all entries from `design/view-anchors.json` (extend to full 13 views as needed)
  - ✅ Dropdown with all 13 views; `view-anchors.json` v2 expanded.
- [x] T003 [U] Dynamic picker: load selected view image + width/height; export per-`viewId` JSON for `view-anchors.json`
  - ✅ Dynamic image/dimensions, visibility badge, per-view JSON export with saved anchor markers.
- [x] T004 [N] Create `design/occluders.json` schema with house/wall/gate polygon regions per view
  - ✅ Occluder polygons per view + world sector rules documented.
- [x] T005 [N] Implement visibility evaluator: world position + viewId → `full` | `hidden` | `partial`; update `visibility-matrix.json` for `lamsam-front-right`
  - ✅ `get_view_visibility()` in process_image.py; matrix v2 with `viewVisibility` + `hiddenViewIds`.
- [x] T006 [U] Update hybrid pipeline: skip blend on `hidden` views; occlusion-aware prompts on `partial`; extend `process_image.py place` or blend script
  - ✅ `place` skips hidden; `visibility` + `reset-hidden` commands added.
- [x] T007 [N] Regenerate only views where visibility classification changed; verify garage-left and side views show no tree
  - ✅ Regenerated partial garage-front/garage-right; `reset-hidden` for 8 hidden views (= raw, no tree).
- [x] T008 [U] Update `design/WORKFLOW.md` and `image-processor` SKILL.md with occlusion rules
  - ✅ 3-step pipeline with occlusion table documented.
