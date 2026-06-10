# Multi-View Plant Placement Workflow

Coordinate-based + generative + occlusion-aware landscaping pipeline.

## Files

| File | Role |
|------|------|
| `design/placements.json` | Canonical element position |
| `design/view-anchors.json` | Per-view pixel anchors (all 13 views) |
| `design/visibility-matrix.json` | Per-view `full` / `partial` / `hidden` |
| `design/occluders.json` | Occluder polygons per view |
| `design/guides/` | Phase 1 placement guides |

## Mandatory 3-step pipeline

```
1. Placement Picker (outline/home.html) — pick anchor per view
2. Phase 1: place --guide-dir design/guides — position guides
3. Phase 2: generate_image — blend into CGI (occlusion-aware prompts)
4. reset-hidden — copy raw to *_designed.png for hidden views
```

### Phase 1 — Placement guide

```bash
python process_image.py place --placement <id> --guide-dir design/guides
```

Skips views marked `hidden` in visibility matrix.

### Phase 2 — Generative blend

Per view with `full` or `partial` visibility:

- Image 1: raw house PNG
- Image 2: tree species reference
- Image 3: guide PNG
- Prompt: include `normX`/`normY`; for `partial` add occlusion hint (wall/pillar blocks)

### 3D foreground occlusion (roof/beams in front of tree)

For `partial` views where structure blocks the tree (e.g. `garage-right` carport roof):

```bash
python process_image.py composite-foreground --view garage-right
```

Pastes roof/beam pixels from **raw** image over `_designed.png` using `foregroundLayers` polygons in `design/occluders.json`. Run after Phase 2 generative blend; resize designed to raw dimensions first if sizes differ.

### Occlusion — hidden views

```bash
python process_image.py reset-hidden --placement <id>
```

Copies raw `resources/<view>.png` → `<view>_designed.png` (no tree).

```bash
python process_image.py visibility --placement <id>
```

Prints per-view visibility report.

## Visibility levels

| Level | Guide | Generate | Output |
|-------|-------|----------|--------|
| `full` | yes | yes, standard prompt | blended `_designed.png` |
| `partial` | yes | yes, occlusion prompt | blended with depth cues |
| `hidden` | skip | skip | `reset-hidden` → raw copy |

## Placement Picker (UI)

- Toggle in **header** (next to Design/Raw mode)
- Dropdown: all 13 views — **every view can set planting anchor** (click on image)
- Badge: full / partial / hidden = **final render behavior only**, not picker restriction
- Export JSON keyed by `viewId` → update `design/view-anchors.json`

## References

- [004](../task/004-improve-multi-view-plant-placement.md) placement registry
- [005](../task/005-hybrid-generative-blend.md) generative blend
- [006](../task/006-placement-picker-occlusion-3d.md) picker UX + occlusion
