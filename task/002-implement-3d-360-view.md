---
title: "Implement 3D 360 view menu"
type: planning
detail: "Research and implement a 3D pseudo-360 viewpoint switcher on the layout page using resources/"
tags: [3d-view, layout, web-research]
created: 2026-06-10
updated: 2026-06-10
---

# Implement 3D 360 view menu

Related: [task/001-create-home-outline.md](001-create-home-outline.md) · [outline/home.html](../outline/home.html)

## Task Requirement

- Goal: Add an interactive menu or feature in `outline/home.html` that simulates a 3D/360-degree virtual tour or turntable rotation of the house using the available photos.
- Research Findings (Web Research):
  - **Turntable Option**: Using libraries like `Cloudimage 360 View` or custom JS to cycle through sequential frames. Since our 13 photos are taken from varying heights and distances (not a perfect turntable sequence), a direct mouse-drag slider might look slightly jumpy.
  - **3D Compass / Floorplan Orbital Switcher (Recommended)**: Create an interactive 3D-style visual compass or SVG floorplan widget. Clicking or dragging the compass pointer to a specific angle immediately shows the corresponding photo (e.g. Front, Left-Front, Right-Back). This provides a very clean, structured "Virtual Tour" experience.
  - **Three.js projection**: Projecting images onto a simple 3D bounding box model.
- Additional Angles Needed (Optional):
  - High-angle corner views (e.g., front-left corner, back-right corner) to smooth out transitions.
- In scope:
  - Modify `outline/home.html` to add a new "3D 360 View" workspace tab.
  - Implement a custom interactive CSS/JS component (like a 3D Orbit Dial or Floorplan Compass).
  - Map all 13 photos to their respective spatial angles on the dial.
  - Build smooth transition fade animations between viewpoints.
- Out of scope: building actual 3D meshes (OBJ/GLTF) of the house.

## Checklist

- [x] T001 [N] Add "3D 360 Orbit View" UI tab and container in `outline/home.html`
  - ✅ Tab navigation integrated dynamically.
- [x] T002 [N] Implement the interactive Orbit Dial (SVG/CSS-based circular selector representing camera angles)
  - ✅ Implemented interactive SVG Dial with pointer needle and circular markers.
- [x] T003 [N] Map the 13 viewpoint photos to their respective positions on the Dial (0° to 360° plus high/low angles)
  - ✅ Mapped 13 photos onto exact spatial angles from 0° (North/Back) to 315° (North-West/Left-Back).
- [x] T004 [N] Add drag/scroll listener to the Dial for smooth orbital photo switching
  - ✅ Implemented mouse/touch drag triggers to calculate drag angle using atan2 and snap to closest viewpoint.
- [x] T005 [N] Document any gaps where additional photos from specific angles are needed for a smoother transition
  - ✅ Analyzed gaps: The horizontal coverage is excellent (20° to 45° intervals). The primary gaps are vertical elevation views (high/low angles) for the back/sides, and the need for diagonal corner viewpoints to smooth out transitions.
