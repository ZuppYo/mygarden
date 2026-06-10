# Multi-View Plant Placement Workflow

Coordinate-based + generative landscaping pipeline for this repo.

## Problems solved

| Gap | Fix |
|-----|-----|
| Imprecise position | Placement registry + Placement Picker |
| Missing views | Visibility matrix + multi-view processing |
| 3D 360 gap | `designedSrc` on all visible orbit viewpoints |
| "Pasted photo" look | **Phase 2 generative blend** re-renders tree into CGI style |

## Files

| File | Role |
|------|------|
| `design/placements.json` | Canonical element position (world coords, asset, size) |
| `design/view-anchors.json` | Per-view pixel anchors + overlay params |
| `design/visibility-matrix.json` | Which views show each placement |
| `design/guides/` | Phase 1 placement guides (not final output) |

## Mandatory 2-phase hybrid pipeline

```
Phase 1 — Placement guide (precise position)
  python process_image.py place --placement <id> --guide-dir design/guides
  → Rough tree position + grass marker for AI reference

Phase 2 — Generative blend (visual quality)
  generate_image per view with:
    - raw house PNG (Image 1)
    - tree species reference PNG (Image 2)
    - placement guide PNG (Image 3)
  Prompt: integrate tree at guide coords in matching 3D CGI style
  → Save as resources/<view>_designed.png
```

**Never use Phase 1 output as final** — guides are position hints only.  
**Never use text-only generate_image for position** — always include guide + anchor coords.

## Coordinate system

- **Site plan:** `worldX`, `worldY` in `[0, 1]`
- **View pixels:** `anchorX`, `anchorY` = bottom-center of tree on ground
- **Normalized:** `normX = anchorX / width`, `normY = anchorY / height`

## Visibility rules (front-yard)

Element with `worldX > 0.5` visible from: `front-low`, `front-high`, `front-center`, `garage-front`, `garage-right`.

## Asset requirements

- Tree reference: `resources/tree/ต้นล่ำซำ-*.png` for species/style in Phase 2
- Cutout assets (`*-cutout.png`) only for Phase 1 guides, not final renders

## References

- [004-improve-multi-view-plant-placement](../task/004-improve-multi-view-plant-placement.md)
- [005-hybrid-generative-blend](../task/005-hybrid-generative-blend.md)
