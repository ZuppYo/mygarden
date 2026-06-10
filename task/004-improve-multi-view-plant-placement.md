---
title: "Improve multi-view plant placement workflow"
type: planning
detail: "Research and redesign workflow so Lamsam tree placement is coordinate-precise, propagates to all visible viewpoints, and appears in 3D 360 orbit"
tags: [workflow, multi-view, placement, 3d-view, research]
created: 2026-06-10
updated: 2026-06-10
---

# Improve multi-view plant placement workflow

Related: [task/index.md](index.md) · [003-add-front-right-lamsam-tree](./003-add-front-right-lamsam-tree.md) · [image-processor skill](../.agents/skills/image-processor/SKILL.md)

## Task Requirement

- Goal: Fix three gaps exposed by Task 003 — imprecise tree position, missing tree in other viewpoints that should show it, and no tree in 3D 360 orbit — by introducing a repeatable, coordinate-based multi-view design workflow.
- Problems from Task 003:
  1. **Position imprecise** — `generate_image` with text-only prompts ("front-right") cannot guarantee pixel-accurate placement; user cannot specify exact spot.
  2. **Single-view edits only** — only `หน้าบ้านมุมต่ำ` and `หน้าบ้านมุมสูง` were designed; other views at the same zone (e.g. `หน้าบ้านตรงกลาง`, `โรงจอดรถด้านหน้า/ขวา`) still show raw images without the tree even though the tree would be visible from those angles.
  3. **3D 360 orbit gap** — Orbit viewer only swaps to `designedSrc` when defined; currently only `front-low` and `front-high` have it, so rotating to 180° normal (front-center) or nearby garage angles shows no Lamsam.
- In scope:
  - Web research synthesis and documented best-practice workflow for this repo's toolchain (Pillow + optional AI blend).
  - Placement registry schema (world/site coordinates → per-view pixel overlay).
  - View-coverage matrix: which `resources/*.png` must be updated when a front-yard element is placed.
  - Placement picker or coordinate-spec UI in `outline/home.html` (or lightweight JSON editor).
  - Extend `image-processor` skill/script for placement-driven overlay pipeline.
  - Re-apply Lamsam tree using the new workflow on all affected viewpoints; wire `designedSrc` for every orbit viewpoint that should show it.
- Out of scope:
  - Training custom diffusion models (EditP23, Tinker, DragMV).
  - Full 3D Gaussian Splatting or NeRF reconstruction.
  - Modifying non-front-yard zones in this iteration.

## Analysis & Research Findings

### Root cause (Task 003)

| Problem | Root cause in current workflow |
|---------|-------------------------------|
| Position off | `generate_image` is generative — no spatial contract; "front-right" is interpreted freely each run. |
| Other views missing tree | Task 003 explicitly scoped to 2 PNGs only; no cross-view propagation or visibility rules. |
| 3D 360 shows no tree | `viewpoints[]` in `home.html` only sets `designedSrc` on `front-low` / `front-high`; `front-center` at 180° normal falls back to raw `src`. |

### Industry / research best practices (2025)

1. **Canonical site placement first** (CAD/GIS standard)  
   Define each plant once on a site plan with real-world or normalized coordinates (meters or 0–1 grid). AutoCAD landscape workflows use attributed blocks on a `NEW-PLANTING` layer; ArcGIS Site Scan georeferences overlays via 2+ control points.  
   → *Adaptation:* `design/placements.json` — one record per element with `{ id, species, worldX, worldY, heightM, canopyM }`.

2. **Per-view projection, not per-view guessing** (georeferencing pattern)  
   Map the canonical position to pixel `(x, y, scale)` per viewpoint using 2–4 anchor landmarks shared across views (gate center, driveway corner, house corner).  
   → *Adaptation:* `design/view-anchors.json` + helper that computes overlay position per `resources/*.png`.

3. **Hybrid compositing pipeline** (practical for this repo)  
   - **Precise:** Pillow `overlay` for tree asset at computed coordinates (deterministic, repeatable).  
   - **Blend:** optional `generate_image` inpainting only for grass/ground around the overlay mask (artistic fill, not placement).  
   This matches professional "plan overlay on photo" workflows (Realtime Landscaping CAD import, Photoshop warp) without ML training.

4. **Multi-view consistency** (research: EditP23, Tinker, Correspondence Guidance)  
   State-of-the-art uses edit propagation across views via diffusion guidance. For our lightweight stack:  
   - **Anchor view:** user confirms placement on one reference view (e.g. front-low).  
   - **Propagate:** derive other views from placement registry + visibility matrix, not independent AI prompts.  
   - **Validate:** side-by-side gallery check in `home.html` Design mode.

5. **Visibility matrix** (scene-graph reasoning, cf. LayerCraft ChainArchitect)  
   Before editing, enumerate which viewpoints can see a given world position. Front-right yard tree is visible from: `หน้าบ้านมุมต่ำ`, `หน้าบ้านมุมสูง`, `หน้าบ้านตรงกลาง`, `โรงจอดรถด้านหน้า`, `โรงจอดรถด้านขวา` (approx. angles 155°–195°).  
   Each gets a `designedSrc` once composited.

### Proposed workflow (target state)

```
1. User picks spot on reference view (front-low) → saves normalized coords
2. placements.json updated (canonical position)
3. Script computes per-view overlay (x, y, scale) from anchors
4. Pillow overlays tree PNG + optional grass mask
5. Optional AI blend pass on masked ground only
6. Save *_designed.png for every view in visibility matrix
7. home.html viewpoints[] + orbit designedSrc wired for all affected IDs
```

## Checklist

- [x] T001 [N] Document research synthesis and proposed workflow in `design/WORKFLOW.md` (placement schema, visibility matrix, hybrid overlay pipeline)
  - ✅ Created `design/WORKFLOW.md` with coordinate system, pipeline, visibility rules, and hybrid compositing guidance.
- [x] T002 [N] Create `design/placements.json` and `design/view-anchors.json` schemas with Lamsam front-right seed entry
  - ✅ Seed placement `lamsam-front-right` with world coords, cutout asset, grass config; 5 views with anchor params.
- [x] T003 [N] Build front-yard visibility matrix mapping `placements.json` elements → list of `resources/*.png` + orbit viewpoint IDs
  - ✅ Created `design/visibility-matrix.json` mapping to 5 files and orbit IDs.
- [x] T004 [N] Extend `image-processor` script with `place` command: read placement + anchors, overlay tree asset per view, output `*_designed.png`
  - ✅ Added `place` command with grass ellipse + bottom-center tree anchor compositing.
- [x] T005 [N] Add placement picker UI in `outline/home.html` (click on reference image → export normalized x/y to placements JSON or copy-paste block)
  - ✅ Placement Picker panel on front-low with click marker, JSON output, and copy button.
- [x] T006 [U] Re-apply Lamsam + Japanese grass on all visibility-matrix views using new `place` pipeline (not text-only `generate_image`)
  - ✅ Ran `place --placement lamsam-front-right`; generated 5 `*_designed.png` files; created `ต้นล่ำซำ-3-cutout.png`.
- [x] T007 [U] Update `outline/home.html` orbit `viewpoints[]` — add `designedSrc` for every viewpoint in visibility matrix (front-center, garage-front, garage-right, etc.)
  - ✅ `designedSrc` on 5 viewpoints; gallery cards + `DESIGNED_GALLERY_VIEWS` mode switcher updated.
- [x] T008 [N] Update `image-processor` SKILL.md and AGENTS.md rules to mandate placement-registry workflow for future design tasks
  - ✅ SKILL.md section 3 (placement workflow); AGENTS.md rule against text-only plant placement.
