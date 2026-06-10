#!/usr/bin/env python
import json
import os
import sys
import argparse
from pathlib import Path

# Check if Pillow is installed
try:
    from PIL import Image
except ImportError:
    print("Error: The 'Pillow' library is not installed.", file=sys.stderr)
    print("Please install it using: pip install Pillow", file=sys.stderr)
    sys.exit(1)

def do_crop(args):
    print(f"Cropping {args.input} -> {args.output} with box {args.box}")
    img = Image.open(args.input)
    cropped = img.crop(args.box)
    cropped.save(args.output)
    print("Crop complete successfully.")

def do_resize(args):
    print(f"Resizing {args.input} -> {args.output} to size {args.size}")
    img = Image.open(args.input)
    resized = img.resize(args.size, Image.Resampling.LANCZOS)
    resized.save(args.output)
    print("Resize complete successfully.")

def do_overlay(args):
    print(f"Overlaying {args.overlay} onto {args.base} -> {args.output} at ({args.x}, {args.y})")
    base = Image.open(args.base).convert("RGBA")
    overlay = Image.open(args.overlay).convert("RGBA")

    # Handle scaling if provided
    if args.scale and args.scale != 1.0:
        w, h = overlay.size
        new_w = int(w * args.scale)
        new_h = int(h * args.scale)
        overlay = overlay.resize((new_w, new_h), Image.Resampling.LANCZOS)

    # Handle alpha channel opacity adjust if provided
    if args.alpha and args.alpha != 1.0:
        # Split into bands and modify alpha band
        r, g, b, a = overlay.split()
        a = a.point(lambda p: int(p * args.alpha))
        overlay = Image.merge("RGBA", (r, g, b, a))

    # Composite overlay onto base
    # Paste using overlay as its own mask to preserve transparency
    base.paste(overlay, (args.x, args.y), overlay)
    
    # Save output (if file extension is png, save as RGBA; otherwise convert to RGB)
    _, ext = os.path.splitext(args.output.lower())
    if ext in ['.jpg', '.jpeg']:
        base.convert("RGB").save(args.output)
    else:
        base.save(args.output)
    print("Overlay composite complete successfully.")

def do_collage(args):
    print(f"Creating collage from {len(args.inputs)} images -> {args.output} with {args.columns} columns")
    if not args.inputs:
        print("Error: No input images provided for collage.", file=sys.stderr)
        sys.exit(1)

    images = [Image.open(p) for p in args.inputs]

    # Calculate individual tile sizes
    if args.tile_width and args.tile_height:
        tw, th = args.tile_width, args.tile_height
    else:
        # Auto size based on max dimensions
        tw = max(img.width for img in images)
        th = max(img.height for img in images)

    # Resize all to tile size
    resized_images = [img.resize((tw, th), Image.Resampling.LANCZOS) for img in images]

    # Calculate collage grid dimensions
    num_imgs = len(resized_images)
    cols = min(args.columns, num_imgs)
    rows = (num_imgs + cols - 1) // cols

    collage_img = Image.new("RGBA", (cols * tw, rows * th), (255, 255, 255, 0))

    for idx, img in enumerate(resized_images):
        c = idx % cols
        r = idx // cols
        collage_img.paste(img, (c * tw, r * th))

    # Save
    _, ext = os.path.splitext(args.output.lower())
    if ext in ['.jpg', '.jpeg']:
        collage_img.convert("RGB").save(args.output)
    else:
        collage_img.save(args.output)
    print("Collage creation complete successfully.")


def _load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _find_placement(placements_data, placement_id):
    for element in placements_data.get("elements", []):
        if element["id"] == placement_id:
            return element
    return None


def _find_view(views_data, view_id):
    for view in views_data.get("views", []):
        if view["viewId"] == view_id:
            return view
    return None


def _point_in_polygon(x, y, polygon):
    inside = False
    n = len(polygon)
    j = n - 1
    for i in range(n):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        denom = (yj - yi) or 1e-12
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / denom + xi):
            inside = not inside
        j = i
    return inside


def get_view_visibility(view_id, norm_x, norm_y, visibility_entry, occluders_data):
    """Return full | partial | hidden for a placement anchor in normalized view coords."""
    explicit = visibility_entry.get("viewVisibility", {}).get(view_id)
    if explicit:
        return explicit

    hidden_ids = set(visibility_entry.get("hiddenViewIds", []))
    if view_id in hidden_ids:
        return "hidden"

    view_occluders = occluders_data.get("views", {}).get(view_id, {}).get("occluders", [])
    for occ in view_occluders:
        if _point_in_polygon(norm_x, norm_y, occ["polygon"]):
            return occ.get("effect", "hidden")
    return "full"


def _draw_grass_patch(base, anchor_x, anchor_y, radius, color, alpha):
    from PIL import ImageDraw

    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    bbox = [
        anchor_x - radius,
        anchor_y - radius * 0.55,
        anchor_x + radius,
        anchor_y + radius * 0.15,
    ]
    draw.ellipse(bbox, fill=(*color, alpha))
    return Image.alpha_composite(base, layer)


def _paste_tree(base, asset_path, anchor_x, anchor_y, scale):
    overlay = Image.open(asset_path).convert("RGBA")
    if scale != 1.0:
        w, h = overlay.size
        overlay = overlay.resize(
            (max(1, int(w * scale)), max(1, int(h * scale))),
            Image.Resampling.LANCZOS,
        )
    paste_x = int(anchor_x - overlay.width / 2)
    paste_y = int(anchor_y - overlay.height)
    base.paste(overlay, (paste_x, paste_y), overlay)
    return base


def do_place(args):
    workspace = Path(args.workspace).resolve()
    design_dir = workspace / args.design_dir
    resources_dir = workspace / args.resources_dir

    placements_data = _load_json(design_dir / "placements.json")
    view_anchors_data = _load_json(design_dir / "view-anchors.json")
    visibility_data = _load_json(design_dir / "visibility-matrix.json")
    occluders_path = design_dir / "occluders.json"
    occluders_data = _load_json(occluders_path) if occluders_path.exists() else {"views": {}}

    placement = _find_placement(placements_data, args.placement)
    if not placement:
        print(f"Error: placement '{args.placement}' not found.", file=sys.stderr)
        sys.exit(1)

    visibility_entry = visibility_data.get("placements", {}).get(args.placement)
    if not visibility_entry:
        print(f"Error: no visibility entry for '{args.placement}'.", file=sys.stderr)
        sys.exit(1)

    asset_path = workspace / placement["asset"]
    if not asset_path.exists():
        print(f"Error: asset not found: {asset_path}", file=sys.stderr)
        sys.exit(1)

    grass_cfg = placement.get("grass", {})
    grass_enabled = grass_cfg.get("enabled", False)
    grass_color = tuple(grass_cfg.get("color", [46, 125, 50]))
    grass_alpha = grass_cfg.get("alpha", 160)

    processed = []
    skipped = []
    for view_id in visibility_entry["viewIds"]:
        view = _find_view(view_anchors_data, view_id)
        if not view:
            print(f"Warning: view '{view_id}' not in view-anchors.json, skipping.", file=sys.stderr)
            continue

        params = view.get("placements", {}).get(args.placement)
        if not params:
            print(f"Warning: no placement params for '{args.placement}' in '{view_id}', skipping.", file=sys.stderr)
            continue

        norm_x = params["anchorX"] / view["width"]
        norm_y = params["anchorY"] / view["height"]
        visibility = get_view_visibility(view_id, norm_x, norm_y, visibility_entry, occluders_data)
        if visibility == "hidden":
            print(f"Skipping '{view_id}' — occlusion: hidden")
            skipped.append(view_id)
            continue
        if visibility == "partial":
            print(f"Placing '{view_id}' — occlusion: partial (guide only)")

        base_path = resources_dir / view["file"]
        if not base_path.exists():
            print(f"Warning: base image missing: {base_path}, skipping.", file=sys.stderr)
            continue

        stem = Path(view["file"]).stem
        if args.guide_dir:
            guide_dir = workspace / args.guide_dir
            guide_dir.mkdir(parents=True, exist_ok=True)
            output_path = guide_dir / f"{view_id}_guide.png"
        else:
            output_path = resources_dir / f"{stem}_designed.png"

        print(f"Placing '{args.placement}' on {view['file']} -> {output_path}")
        base = Image.open(base_path).convert("RGBA")

        anchor_x = int(params["anchorX"])
        anchor_y = int(params["anchorY"])
        scale = float(params.get("scale", 1.0))
        grass_radius = int(params.get("grassRadius", 100))

        if grass_enabled:
            base = _draw_grass_patch(base, anchor_x, anchor_y, grass_radius, grass_color, grass_alpha)

        base = _paste_tree(base, asset_path, anchor_x, anchor_y, scale)
        base.convert("RGB").save(output_path)
        processed.append(str(output_path.relative_to(workspace)))

    if not processed:
        print("Error: no views were processed.", file=sys.stderr)
        sys.exit(1)

    print(f"Place complete: {len(processed)} view(s), skipped {len(skipped)} hidden.")
    for p in processed:
        print(f"  - {p}")


def do_reset_hidden(args):
    """Copy raw base images to *_designed.png for occluded views (no tree)."""
    import shutil

    workspace = Path(args.workspace).resolve()
    design_dir = workspace / args.design_dir
    resources_dir = workspace / args.resources_dir

    view_anchors_data = _load_json(design_dir / "view-anchors.json")
    visibility_data = _load_json(design_dir / "visibility-matrix.json")
    visibility_entry = visibility_data.get("placements", {}).get(args.placement)
    if not visibility_entry:
        print(f"Error: no visibility entry for '{args.placement}'.", file=sys.stderr)
        sys.exit(1)

    hidden_ids = visibility_entry.get("hiddenViewIds", [])
    reset = []
    for view_id in hidden_ids:
        view = _find_view(view_anchors_data, view_id)
        if not view:
            continue
        src = resources_dir / view["file"]
        dst = resources_dir / f"{Path(view['file']).stem}_designed.png"
        if not src.exists():
            print(f"Warning: missing {src}", file=sys.stderr)
            continue
        shutil.copy2(src, dst)
        reset.append(str(dst.relative_to(workspace)))
        print(f"Reset hidden view {view_id}: {dst.name} (= raw)")

    print(f"Reset complete: {len(reset)} view(s).")


def do_visibility_report(args):
    workspace = Path(args.workspace).resolve()
    design_dir = workspace / args.design_dir
    view_anchors_data = _load_json(design_dir / "view-anchors.json")
    visibility_data = _load_json(design_dir / "visibility-matrix.json")
    occluders_data = _load_json(design_dir / "occluders.json")

    visibility_entry = visibility_data.get("placements", {}).get(args.placement)
    if not visibility_entry:
        print(f"Error: no visibility entry for '{args.placement}'.", file=sys.stderr)
        sys.exit(1)

    print(f"Visibility report for '{args.placement}':")
    for view in view_anchors_data.get("views", []):
        view_id = view["viewId"]
        params = view.get("placements", {}).get(args.placement)
        if params:
            norm_x = params["anchorX"] / view["width"]
            norm_y = params["anchorY"] / view["height"]
            vis = get_view_visibility(view_id, norm_x, norm_y, visibility_entry, occluders_data)
        else:
            vis = visibility_entry.get("viewVisibility", {}).get(view_id, "n/a")
        print(f"  {view_id}: {vis}")


def main():
    parser = argparse.ArgumentParser(description="Programmatic Image manipulation tool utilizing Pillow.")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Command to run")

    # Crop
    crop_parser = subparsers.add_parser("crop", help="Crop an image")
    crop_parser.add_argument("--input", required=True, help="Input image path")
    crop_parser.add_argument("--output", required=True, help="Output image path")
    crop_parser.add_argument("--box", required=True, type=int, nargs=4, metavar=('LEFT', 'TOP', 'RIGHT', 'BOTTOM'),
                            help="Bounding box dimensions: left top right bottom")

    # Resize
    resize_parser = subparsers.add_parser("resize", help="Resize an image")
    resize_parser.add_argument("--input", required=True, help="Input image path")
    resize_parser.add_argument("--output", required=True, help="Output image path")
    resize_parser.add_argument("--size", required=True, type=int, nargs=2, metavar=('WIDTH', 'HEIGHT'),
                               help="New dimensions: width height")

    # Overlay
    overlay_parser = subparsers.add_parser("overlay", help="Overlay one image onto another")
    overlay_parser.add_argument("--base", required=True, help="Base image path")
    overlay_parser.add_argument("--overlay", required=True, help="Overlay image path")
    overlay_parser.add_argument("--output", required=True, help="Output image path")
    overlay_parser.add_argument("--x", required=True, type=int, help="X position to paste")
    overlay_parser.add_argument("--y", required=True, type=int, help="Y position to paste")
    overlay_parser.add_argument("--scale", type=float, default=1.0, help="Scale factor for overlay image")
    overlay_parser.add_argument("--alpha", type=float, default=1.0, help="Opacity level for overlay image (0.0 to 1.0)")

    # Collage
    collage_parser = subparsers.add_parser("collage", help="Create a grid collage from multiple images")
    collage_parser.add_argument("--inputs", required=True, nargs="+", help="Input image paths")
    collage_parser.add_argument("--output", required=True, help="Output image path")
    collage_parser.add_argument("--columns", required=True, type=int, help="Number of columns in collage")
    collage_parser.add_argument("--tile-width", type=int, help="Optional width for each grid cell")
    collage_parser.add_argument("--tile-height", type=int, help="Optional height for each grid cell")

    # Place (multi-view placement pipeline)
    place_parser = subparsers.add_parser(
        "place",
        help="Apply placement registry to all visible views (outputs *_designed.png)",
    )
    place_parser.add_argument("--placement", required=True, help="Placement element id from placements.json")
    place_parser.add_argument(
        "--workspace",
        default=".",
        help="Workspace root (default: current directory)",
    )
    place_parser.add_argument(
        "--design-dir",
        default="design",
        help="Design config directory relative to workspace",
    )
    place_parser.add_argument(
        "--resources-dir",
        default="resources",
        help="Resources image directory relative to workspace",
    )
    place_parser.add_argument(
        "--guide-dir",
        default=None,
        help="If set, write placement guides here (e.g. design/guides) instead of *_designed.png",
    )

    reset_parser = subparsers.add_parser(
        "reset-hidden",
        help="Copy raw images to *_designed.png for hidden/occluded views",
    )
    reset_parser.add_argument("--placement", required=True)
    reset_parser.add_argument("--workspace", default=".")
    reset_parser.add_argument("--design-dir", default="design")
    reset_parser.add_argument("--resources-dir", default="resources")

    vis_parser = subparsers.add_parser("visibility", help="Print per-view visibility report")
    vis_parser.add_argument("--placement", required=True)
    vis_parser.add_argument("--workspace", default=".")
    vis_parser.add_argument("--design-dir", default="design")

    args = parser.parse_args()

    if args.command == "crop":
        do_crop(args)
    elif args.command == "resize":
        do_resize(args)
    elif args.command == "overlay":
        do_overlay(args)
    elif args.command == "collage":
        do_collage(args)
    elif args.command == "place":
        do_place(args)
    elif args.command == "reset-hidden":
        do_reset_hidden(args)
    elif args.command == "visibility":
        do_visibility_report(args)

if __name__ == "__main__":
    main()
