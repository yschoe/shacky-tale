#!/usr/bin/env python3

import sys
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# -----------------------------
# Tile appearance definitions
# -----------------------------
TILES = {
    '0': {"name": "blank",    "fill": (194, 226, 160), "label": ""},   # grass/plain
    '1': {"name": "tree",     "fill": ( 34, 139,  34), "label": "T"},
    '2': {"name": "mountain", "fill": ( 60,  60,  60), "label": "M"},
    '3': {"name": "water",    "fill": (135, 206, 235), "label": "W"},
    'f': {"name": "fox",      "fill": (230, 140,  40), "label": "F"},
    's': {"name": "skeleton", "fill": (230, 230, 230), "label": "Sk"},
    'b': {"name": "bat",      "fill": (100,  70, 120), "label": "B"},
    'c': {"name": "cave",     "fill": (110,  85,  60), "label": "Cv"},
    'h': {"name": "house",    "fill": (210, 180, 140), "label": "H"},
    'v': {"name": "vendor",   "fill": (255, 215,   0), "label": "V"},
    'w': {"name": "wall",     "fill": (128, 128, 128), "label": "#"},
    'A': {"name": "anhome",   "fill": (255, 182, 193), "label": "A"},
    'S': {"name": "slime",    "fill": (124, 252,   0), "label": "S"},
    'C': {"name": "caveend",  "fill": (160,  82,  45), "label": "Ce"},
}

UNKNOWN_TILE = {"name": "unknown", "fill": (255,  80,  80), "label": "?"}


def load_map(filepath):
    """
    Read ASCII map from a text file.
    Keeps spaces if they are present in the middle of lines.
    Trims only trailing newline characters.
    Pads shorter rows with '0'.
    """
    lines = Path(filepath).read_text(encoding="utf-8").splitlines()

    # Drop completely empty leading/trailing lines if present
    while lines and lines[0] == "":
        lines.pop(0)
    while lines and lines[-1] == "":
        lines.pop()

    if not lines:
        raise ValueError("Map file is empty.")

    width = max(len(line) for line in lines)
    grid = [list(line.ljust(width, '0')) for line in lines]
    return grid


def draw_tree(draw, x0, y0, cell):
    trunk_w = max(2, cell // 8)
    trunk_h = max(4, cell // 5)
    cx = x0 + cell // 2
    # trunk
    draw.rectangle(
        [cx - trunk_w // 2, y0 + cell - trunk_h - 4, cx + trunk_w // 2, y0 + cell - 4],
        fill=(101, 67, 33)
    )
    # canopy
    draw.polygon(
        [
            (cx, y0 + 6),
            (x0 + 6, y0 + cell // 2 + 2),
            (x0 + cell - 6, y0 + cell // 2 + 2),
        ],
        fill=(20, 110, 20)
    )


def draw_mountain(draw, x0, y0, cell):
    draw.polygon(
        [
            (x0 + cell // 2, y0 + 5),
            (x0 + 5, y0 + cell - 5),
            (x0 + cell - 5, y0 + cell - 5),
        ],
        fill=(50, 50, 50)
    )
    draw.polygon(
        [
            (x0 + cell // 2, y0 + 8),
            (x0 + cell // 2 - 8, y0 + cell // 3),
            (x0 + cell // 2 + 8, y0 + cell // 3),
        ],
        fill=(240, 240, 240)
    )


def draw_water(draw, x0, y0, cell):
    # simple wave lines
    for k in range(3):
        yy = y0 + 10 + k * (cell // 4)
        step = max(8, cell // 4)
        for xx in range(x0 + 4, x0 + cell - 8, step):
            draw.arc([xx, yy - 4, xx + step, yy + 4], start=0, end=180, fill=(70, 140, 220), width=2)


def draw_house(draw, x0, y0, cell):
    draw.rectangle([x0 + 10, y0 + 18, x0 + cell - 10, y0 + cell - 8], fill=(220, 190, 140), outline=(80, 50, 20))
    draw.polygon(
        [(x0 + cell // 2, y0 + 6), (x0 + 6, y0 + 20), (x0 + cell - 6, y0 + 20)],
        fill=(150, 60, 50),
        outline=(80, 30, 20)
    )
    draw.rectangle([x0 + cell // 2 - 5, y0 + cell - 18, x0 + cell // 2 + 5, y0 + cell - 8], fill=(90, 60, 40))


def draw_cave(draw, x0, y0, cell):
    draw.ellipse([x0 + 7, y0 + 12, x0 + cell - 7, y0 + cell - 6], fill=(60, 45, 30), outline=(20, 15, 10))
    draw.ellipse([x0 + 16, y0 + 20, x0 + cell - 16, y0 + cell - 8], fill=(15, 15, 15))


def draw_wall(draw, x0, y0, cell):
    brick_h = max(8, cell // 4)
    brick_w = max(12, cell // 3)
    for row, yy in enumerate(range(y0, y0 + cell, brick_h)):
        offset = brick_w // 2 if row % 2 else 0
        for xx in range(x0 - offset, x0 + cell, brick_w):
            draw.rectangle(
                [xx, yy, min(xx + brick_w, x0 + cell), min(yy + brick_h, y0 + cell)],
                fill=(140, 140, 140),
                outline=(90, 90, 90)
            )


def draw_character(draw, x0, y0, cell, label, color, font):
    r = max(8, cell // 4)
    cx = x0 + cell // 2
    cy = y0 + cell // 2
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color, outline=(0, 0, 0))
    if label:
        bbox = draw.textbbox((0, 0), label, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((cx - tw / 2, cy - th / 2), label, fill=(0, 0, 0), font=font)


def draw_tile(draw, x0, y0, cell, ch, font):
    tile = TILES.get(ch, UNKNOWN_TILE)

    # background
    draw.rectangle([x0, y0, x0 + cell, y0 + cell], fill=tile["fill"], outline=(80, 80, 80))

    # custom icons
    if ch == '1':
        draw_tree(draw, x0, y0, cell)
    elif ch == '2':
        draw_mountain(draw, x0, y0, cell)
    elif ch == '3':
        draw_water(draw, x0, y0, cell)
    elif ch in ('h', 'A'):
        draw_house(draw, x0, y0, cell)
        if ch == 'A':
            draw.rectangle([x0 + 4, y0 + 4, x0 + 14, y0 + 14], fill=(255, 182, 193), outline=(0, 0, 0))
    elif ch in ('c', 'C'):
        draw_cave(draw, x0, y0, cell)
        if ch == 'C':
            draw.arc([x0 + 6, y0 + 6, x0 + cell - 6, y0 + cell - 6], start=300, end=60, fill=(255, 215, 0), width=3)
    elif ch == 'w':
        draw_wall(draw, x0, y0, cell)
    elif ch == '0':
        # subtle grass speckles
        for dx, dy in [(10, 12), (22, 30), (35, 15), (42, 36)]:
            if dx < cell - 3 and dy < cell - 3:
                draw.line([x0 + dx, y0 + dy, x0 + dx, y0 + dy + 5], fill=(80, 150, 70), width=1)
    else:
        # creatures / special entities
        char_colors = {
            'f': (230, 120, 30),
            's': (245, 245, 245),
            'b': (90, 60, 120),
            'v': (255, 220, 0),
            'S': (100, 240, 60),
        }
        draw_character(draw, x0, y0, cell, tile["label"], char_colors.get(ch, (255, 255, 255)), font)


def render_map(grid, cell_size=50, margin=20, legend=True):
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    legend_cols = 3
    legend_items = list(TILES.items())
    legend_rows = (len(legend_items) + legend_cols - 1) // legend_cols
    legend_h = (legend_rows * 26 + 20) if legend else 0

    width = margin * 2 + cols * cell_size
    height = margin * 2 + rows * cell_size + legend_h

    img = Image.new("RGB", (width, height), (245, 245, 245))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", max(12, cell_size // 4))
        small_font = ImageFont.truetype("DejaVuSans.ttf", 16)
    except OSError:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # draw tiles
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            px = margin + x * cell_size
            py = margin + y * cell_size
            draw_tile(draw, px, py, cell_size, ch, font)

    # legend
    if legend:
        ly = margin + rows * cell_size + 12
        lx = margin
        draw.text((lx, ly), "Legend", fill=(0, 0, 0), font=small_font)
        ly += 24

        col_w = max(180, (width - 2 * margin) // legend_cols)
        for idx, (ch, info) in enumerate(legend_items):
            cx = idx % legend_cols
            cy = idx // legend_cols
            xx = lx + cx * col_w
            yy = ly + cy * 26

            draw.rectangle([xx, yy + 3, xx + 18, yy + 18], fill=info["fill"], outline=(0, 0, 0))
            draw.text((xx + 26, yy), f"{ch} = {info['name']}", fill=(0, 0, 0), font=small_font)

    return img


def main():
    parser = argparse.ArgumentParser(description="Render an ASCII map as a colored image.")
    parser.add_argument("input_map", help="Input text file containing the ASCII map")
    parser.add_argument("-o", "--output", help="Output PNG filename")
    parser.add_argument("--cell-size", type=int, default=50, help="Tile size in pixels (default: 50)")
    parser.add_argument("--no-legend", action="store_true", help="Do not draw a legend")
    parser.add_argument("--show", action="store_true", help="Open the generated image after saving")
    args = parser.parse_args()

    grid = load_map(args.input_map)

    out_file = args.output
    if not out_file:
        out_file = str(Path(args.input_map).with_suffix(".png"))

    img = render_map(grid, cell_size=args.cell_size, legend=not args.no_legend)
    img.save(out_file)

    print(f"Saved map image to: {out_file}")

    if args.show:
        img.show()


if __name__ == "__main__":
    main()
