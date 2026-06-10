---
title: "Create home layout template"
type: execution
detail: "Create outline/home.html displaying all house images from resources folder categorized by angle"
tags: [layout, template, resources]
created: 2026-06-10
updated: 2026-06-10
---

# Create home layout template

Related: [task/index.md](index.md)

## Task Requirement

- Goal: Create a layout template web page displaying all house images categorized by their respective angles.
- In scope:
  - Create the folder `outline/` if it does not exist.
  - Create `outline/home.html` containing an organized UI layout of the photos.
  - Group photos logically into Front, Back, Left Side, Right Side, and Garage sections.
  - Style the HTML page nicely with premium dark/light modern UI aesthetics.
- Out of scope: actual garden design elements or photo modification.

## Checklist

- [x] T001 [N] Create `outline/` directory
  - ✅ Directory created successfully.
- [x] T002 [N] Create `outline/home.html` with grid layout structure and modern styles
  - ✅ Template page created with responsive grid and dark obsidian glassmorphism.
- [x] T003 [N] Map and embed all 13 PNG images from `resources/` into the HTML page with labels in Thai/English
  - ✅ All 13 images embedded with relative paths and correct zone labels.
- [x] T004 [N] Add basic interactive filtering/navigation by section (Front, Back, Sides, Garage) for easier viewing
  - ✅ Interactive filtering (Tabs + Search input) and zoom preview modal implemented.
