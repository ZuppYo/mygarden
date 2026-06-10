#!/usr/bin/env python
import os
import sys
import argparse

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

    args = parser.parse_args()

    if args.command == "crop":
        do_crop(args)
    elif args.command == "resize":
        do_resize(args)
    elif args.command == "overlay":
        do_overlay(args)
    elif args.command == "collage":
        do_collage(args)

if __name__ == "__main__":
    main()
