---
name: image-processor
description: >-
  Handles image generation via native generate_image tool, and programmatic image editing/compositing
  via Pillow python script (crop, resize, overlay, collages).
disable-model-invocation: false
---

# Image Processor Skill

Use this skill when designing or editing landscape images. It combines AI generation and precise programmatic manipulation.

## 1. AI Image Generation / Editing
For generating initial landscaping concepts or performing artistic/generative edits on house photos:
- Use the native `generate_image` tool.
- Provide the source images from `resources/` in the `ImagePaths` array (up to 3 images).
- Use descriptive prompts focusing on gardening details, plants, layout style (e.g. Zen, Modern, Tropical), paths, water features, and lighting.

## 2. Programmatic Image Editing
For exact, pixel-perfect composition (e.g., cropping a specific zone of a photo, overlays, collages, drawing layout grids, or joining photos), run the Python helper script:

`python .agents/skills/image-processor/scripts/process_image.py <command> [arguments]`

### Script Commands

- **crop**: Crop a rectangular region from an image.
  ```bash
  python .agents/skills/image-processor/scripts/process_image.py crop --input <path> --output <path> --box <left> <top> <right> <bottom>
  ```

- **resize**: Resize an image to new dimensions.
  ```bash
  python .agents/skills/image-processor/scripts/process_image.py resize --input <path> --output <path> --size <width> <height>
  ```

- **overlay**: Composite (overlay) one image onto another at a specific position with optional scale and alpha opacity.
  ```bash
  python .agents/skills/image-processor/scripts/process_image.py overlay --base <path> --overlay <path> --output <path> --x <x> --y <y> [--scale <float>] [--alpha <float>]
  ```

- **collage**: Combine multiple images into a grid collage.
  ```bash
  python .agents/skills/image-processor/scripts/process_image.py collage --inputs <path1> <path2> ... --output <path> --columns <num> [--tile-width <num>] [--tile-height <num>]
  ```

- **place**: Multi-view placement pipeline — reads placement registry, composites tree guide on every visible view.
  ```bash
  # Phase 1: placement guides (not final output)
  python .agents/skills/image-processor/scripts/process_image.py place --placement <id> --guide-dir design/guides [--workspace <repo-root>]

  # Legacy: direct overlay to *_designed.png (avoid — looks pasted on CGI)
  python .agents/skills/image-processor/scripts/process_image.py place --placement <id>
  ```

## 3. Hybrid workflow (required for new plants)

**Phase 1 — Placement guide** (`place --guide-dir design/guides`): precise position marker.  
**Phase 2 — Generative blend** (`generate_image`): re-render tree into 3D scene style.

1. Register element in `design/placements.json`.
2. Set per-view anchors in `design/view-anchors.json` (Placement Picker in `outline/home.html`).
3. Confirm visibility in `design/visibility-matrix.json`.
4. Run `place --guide-dir design/guides` → guides for AI reference.
5. Run `generate_image` per view with: **raw house** + **tree species ref** + **guide** + anchored prompt (`normX`/`normY`).
6. Save Phase 2 output to `resources/*_designed.png`.
7. Wire `designedSrc` in `outline/home.html` for all visibility-matrix views.

**Rules:** `place` alone = position only (not final). `generate_image` alone without guide = imprecise position. Always use both phases.

See [design/WORKFLOW.md](../../../design/WORKFLOW.md).

## 4. Best Practices
- Phase 1 guides use cutout assets; Phase 2 uses species reference photos for style.
- Final outputs always from Phase 2 generative blend on 3D renders.
- Keep backup copies of original raw house photos in `resources/backup/`.
