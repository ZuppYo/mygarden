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

## 3. Best Practices
- Always check that target image files exist before calling the script.
- Output files should be written back to appropriate directories (such as `resources/` or task specific subfolders).
- Keep backup copies of original raw house photos.
