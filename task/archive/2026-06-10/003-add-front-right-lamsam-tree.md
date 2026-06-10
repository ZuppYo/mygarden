---
title: "Add front-right Lamsam tree"
type: execution
detail: "Add a 2-2.5m Lamsam tree on the front-right side of the yard with Japanese grass ground cover, modifying low and high angle views"
tags: [design, resources, front-yard, tree]
created: 2026-06-10
updated: 2026-06-10
---

# Add front-right Lamsam tree

Related: [task/index.md](index.md)

## Task Requirement

- Goal: Add a Lamsam tree as a main focus tree (2-2.5m height, 1.5-2m canopy width) on the front-right side of the house, and cover the ground around it with Japanese grass.
- Input photos:
  - `resources/หน้าบ้านมุมต่ำ.png`
  - `resources/หน้าบ้านมุมสูง.png`
  - Reference tree: `resources/tree/ต้นล่ำซำ-1.png` or `ต้นล่ำซำ-3.png`
- In scope:
  - Generate design concepts using `generate_image` tool by combining front house views with the Lamsam tree style.
  - Save the designed images as new assets (preserving the original backups).
  - Update `outline/home.html` to display the designed landscape for the front low-angle and high-angle views.
- Out of scope:
  - Modifying non-front viewpoints.

## Checklist

- [x] T001 [N] Backup original `resources/หน้าบ้านมุมต่ำ.png` and `resources/หน้าบ้านมุมสูง.png` to `resources/backup/`
  - ✅ Backups verified in `resources/backup/` (MD5 match with originals); originals preserved at `resources/`.
- [x] T002 [N] Generate design concept image for front low angle with Lamsam tree and Japanese grass using `generate_image`
  - ✅ Generated `resources/หน้าบ้านมุมต่ำ_designed.png` — Lamsam tree on front-right, Japanese grass ground cover.
- [x] T003 [N] Generate design concept image for front high angle with Lamsam tree and Japanese grass using `generate_image`
  - ✅ Generated `resources/หน้าบ้านมุมสูง_designed.png` — Lamsam tree on front-right, Japanese grass lawn.
- [x] T004 [U] Update `outline/home.html` to show the designed views and ensure the switcher maps them correctly
  - ✅ Gallery cards, Design/Raw toggle, and Orbit `designedSrc` mapping verified for both front viewpoints.
