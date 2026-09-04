#!/usr/bin/env python3
"""Paint Scribblins — friendly doodle critters, layered like Foxins.

Every trait is a 12-frame APNG on a shared 512 canvas and 90ms clock.
Body, mug, hat, and wrap share one hover so accessories never warp the skeleton.
Field stays still. Charm floats on its own tiny bob.

Look: marker-on-paper cartoon — thick charcoal outline, warm muted fills, light grain.
Front-facing. Big round head. Egg body. Species told by ears, snout, and tail.
Hats sit on one crown point. Not a rainbow palette.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_shookums import (  # noqa: E402
    DURATION_MS,
    FRAMES,
    SIZE,
    place_portrait,
    save_apng,
    save_image,
)
from gif_bake import save_loop_gif  # noqa: E402

TRAIT_DIR = ROOT / "public" / "scribblins-traits"
PREVIEW_DIR = ROOT / "public" / "scribblins-preview"
BRAND_DIR = ROOT / "public" / "brand"
META_DIR = ROOT / "public" / "metadata"
SRC_DATA = ROOT / "src" / "data"

# Locked doodle skeleton. Never edit per trait.
CX = 256.0
HEAD_Y = 216.0
HEAD_R = 118.0
BODY_Y = 368.0
BODY_RX, BODY_RY = 104.0, 90.0
HAT_X, HAT_Y = 256.0, 86.0
WRAP_X, WRAP_Y = 256.0, 312.0
CHARM_X, CHARM_Y = 410.0, 392.0
INK = (36, 28, 24, 255)
CREAM = (248, 236, 214, 255)
BLUSH = (244, 176, 176, 255)
TEAL = (88, 140, 136, 255)
CLAY = (212, 120, 128, 255)
BUTTER = (236, 196, 96, 255)
LINE = 11

FIELDS = {
    "cream": ((244, 232, 210), (248, 220, 186)),
    "sky": ((198, 216, 214), (168, 196, 198)),
    "clay": ((232, 196, 186), (220, 160, 152)),
    "butter": ((246, 228, 168), (236, 200, 120)),
}

BODIES = {
    "bunny": {"fur": (232, 176, 96, 255), "cream": CREAM, "accent": (244, 176, 176, 255)},
    "bear": {"fur": (140, 96, 68, 255), "cream": CREAM, "accent": (92, 62, 44, 255)},
    "pup": {"fur": (220, 196, 160, 255), "cream": (252, 242, 224, 255), "accent": (196, 148, 120, 255)},
    "frog": {"fur": (122, 156, 112, 255), "cream": (232, 228, 186, 255), "accent": (88, 116, 80, 255)},
}

MUGS = ("blink", "grin", "sleepy", "spark", "wink", "pout", "heart", "blep")
HATS = ("none", "beanie", "bow", "flower", "cap", "headphones", "leaf")
WRAPS = ("none", "scarf", "bandana", "bowtie")
CHARMS = ("none", "star", "pencil", "heart", "balloon")


def hover_y(frame: int) -> float:
    return math.sin(frame / FRAMES * math.pi * 2.0) * 4.0


def blank() -> Image.Image:
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))


def grain(img: Image.Image, amp: int = 10, seed: int = 41) -> Image.Image:
    arr = np.asarray(img).astype(np.int16)
    rng = np.random.default_rng(seed)
    noise = rng.integers(-amp, amp + 1, arr.shape[:2], dtype=np.int16)
    rgb = np.clip(arr[..., :3] + noise[..., None], 0, 255)
    out = np.dstack([rgb, arr[..., 3]]).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def oval(draw: ImageDraw.ImageDraw, cx: float, cy: float, rx: float, ry: float, fill: tuple, width: int = LINE) -> None:
    draw.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=fill, outline=INK, width=width)


def poly(draw: ImageDraw.ImageDraw, pts: list[tuple[float, float]], fill: tuple, width: int = LINE) -> None:
    draw.polygon(pts, fill=fill, outline=INK)
    closed = list(pts) + [pts[0]]
    draw.line(closed, fill=INK, width=width, joint="curve")


def paint_field(kind: str, _frame: int) -> Image.Image:
    paper, halo = FIELDS[kind]
    img = Image.new("RGBA", (SIZE, SIZE), (*paper, 255))
    draw = ImageDraw.Draw(img)
    draw.ellipse((CX - 188, HEAD_Y - 168, CX + 188, HEAD_Y + 208), fill=(*halo, 255))
    return grain(img, amp=9, seed=17 + sum(ord(c) for c in kind))


def paint_body(kind: str, frame: int) -> Image.Image:
    pal = BODIES[kind]
    fur, cream, accent = pal["fur"], pal["cream"], pal["accent"]
    img = blank()
    draw = ImageDraw.Draw(img)
    dy = hover_y(frame)
    hx, hy = CX, HEAD_Y + dy
    bx, by = CX, BODY_Y + dy

    if kind == "bunny":
        oval(draw, hx - 50, hy - 118, 24, 74, fur)
        oval(draw, hx + 50, hy - 118, 24, 74, fur)
        oval(draw, hx - 50, hy - 118, 12, 50, accent, width=6)
        oval(draw, hx + 50, hy - 118, 12, 50, accent, width=6)
        oval(draw, bx + 96, by + 8, 22, 20, cream, width=8)
    elif kind == "bear":
        oval(draw, hx - 78, hy - 86, 30, 28, fur)
        oval(draw, hx + 78, hy - 86, 30, 28, fur)
        oval(draw, hx - 78, hy - 86, 14, 13, accent, width=6)
        oval(draw, hx + 78, hy - 86, 14, 13, accent, width=6)
        oval(draw, bx + 98, by - 6, 18, 16, fur, width=8)
    elif kind == "pup":
        oval(draw, hx - 100, hy + 10, 30, 54, fur)
        oval(draw, hx + 100, hy + 10, 30, 54, fur)
        oval(draw, hx - 100, hy + 14, 14, 32, accent, width=6)
        oval(draw, hx + 100, hy + 14, 14, 32, accent, width=6)
        poly(
            draw,
            [(bx + 78, by - 8), (bx + 128, by - 36), (bx + 118, by + 10), (bx + 86, by + 16)],
            fur,
            width=8,
        )
    else:
        oval(draw, hx - 96, hy + 18, 30, 26, fur)
        oval(draw, hx + 96, hy + 18, 30, 26, fur)
        oval(draw, bx - 56, by + 68, 22, 14, fur, width=8)
        oval(draw, bx + 56, by + 68, 22, 14, fur, width=8)

    oval(draw, bx, by, BODY_RX, BODY_RY, fur)
    oval(draw, bx - 94, by - 8, 30, 20, fur, width=8)
    oval(draw, bx + 94, by - 8, 30, 20, fur, width=8)
    oval(draw, hx, hy, HEAD_R, HEAD_R * 0.96, fur)

    if kind == "frog":
        oval(draw, hx, hy + 30, 72, 38, cream, width=8)
        oval(draw, bx, by + 10, 50, 40, cream, width=8)
    elif kind == "bear":
        oval(draw, hx, hy + 22, 58, 42, cream, width=8)
        oval(draw, bx, by + 10, 46, 38, cream, width=8)
    elif kind == "pup":
        oval(draw, hx, hy + 24, 56, 40, cream, width=8)
        oval(draw, bx, by + 12, 44, 36, cream, width=8)
    else:
        oval(draw, bx, by + 10, 44, 36, cream, width=8)

    for px, py, rx, ry in (
        (bx - 48, by + 62, 16, 12),
        (bx - 18, by + 74, 16, 11),
        (bx + 18, by + 74, 16, 11),
        (bx + 48, by + 62, 16, 12),
    ):
        if kind != "frog":
            oval(draw, px, py, rx, ry, fur, width=8)

    return grain(img, amp=6, seed=77 + sum(ord(c) for c in kind))


def paint_mug(kind: str, frame: int) -> Image.Image:
    img = blank()
    draw = ImageDraw.Draw(img)
    dy = hover_y(frame)
    blink = frame in (5, 6)
    lx, rx = CX - 40.0, CX + 40.0
    ey = HEAD_Y - 4.0 + dy
    mx, my = CX, HEAD_Y + 48.0 + dy

    draw.ellipse((CX - 74, HEAD_Y + 18 + dy, CX - 42, HEAD_Y + 38 + dy), fill=BLUSH)
    draw.ellipse((CX + 42, HEAD_Y + 18 + dy, CX + 74, HEAD_Y + 38 + dy), fill=BLUSH)
    draw.ellipse((CX - 7, HEAD_Y + 20 + dy, CX + 7, HEAD_Y + 32 + dy), fill=INK)

    def open_eye(x: float, y: float, r: float = 22.0) -> None:
        oval(draw, x, y, r, r * 0.92, (28, 22, 18, 255), width=8)
        draw.ellipse((x - 9, y - 11, x - 1, y - 3), fill=(255, 255, 255, 255))
        draw.ellipse((x + 3, y + 2, x + 8, y + 7), fill=(255, 255, 255, 220))

    def shut_eye(x: float, y: float) -> None:
        draw.arc((x - 22, y - 10, x + 22, y + 14), 200, 340, fill=INK, width=7)

    left_shut = kind == "sleepy" or kind == "wink" or (kind == "blink" and blink)
    right_shut = kind == "sleepy" or (kind == "blink" and blink)
    if left_shut:
        shut_eye(lx, ey)
    else:
        open_eye(lx, ey, 24.0 if kind == "spark" else 21.0)
    if right_shut:
        shut_eye(rx, ey)
    else:
        open_eye(rx, ey, 24.0 if kind == "spark" else 21.0)

    if kind == "grin":
        draw.arc((mx - 24, my - 8, mx + 24, my + 20), 10, 170, fill=INK, width=6)
    elif kind == "pout":
        draw.arc((mx - 12, my + 2, mx + 12, my + 16), 200, 340, fill=INK, width=5)
    elif kind == "blep":
        draw.arc((mx - 10, my - 4, mx + 10, my + 10), 20, 160, fill=INK, width=5)
        oval(draw, mx + 6, my + 12, 7, 9, (244, 130, 140, 255), width=5)
    elif kind == "heart":
        poly(
            draw,
            [
                (mx, my + 14),
                (mx - 12, my + 2),
                (mx - 4, my - 6),
                (mx, my),
                (mx + 4, my - 6),
                (mx + 12, my + 2),
            ],
            CLAY,
            width=5,
        )
    elif kind == "spark":
        draw.line((mx - 6, my + 4, mx + 6, my + 4), fill=INK, width=5)
        for sx, sy in ((lx - 28, ey - 22), (rx + 26, ey - 18)):
            draw.line((sx, sy - 7, sx, sy + 7), fill=INK, width=3)
            draw.line((sx - 7, sy, sx + 7, sy), fill=INK, width=3)
    else:
        draw.arc((mx - 10, my - 2, mx + 10, my + 12), 20, 160, fill=INK, width=5)
    return img


def paint_hat(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    img = blank()
    draw = ImageDraw.Draw(img)
    x, y = HAT_X, HAT_Y + hover_y(frame)
    dy = hover_y(frame)
    if kind == "beanie":
        oval(draw, x, y + 22, 60, 26, TEAL)
        oval(draw, x + 4, y - 2, 11, 11, CREAM, width=6)
    elif kind == "bow":
        poly(draw, [(x - 8, y + 16), (x - 46, y + 2), (x - 46, y + 32)], CLAY, width=7)
        poly(draw, [(x + 8, y + 16), (x + 46, y + 2), (x + 46, y + 32)], CLAY, width=7)
        oval(draw, x, y + 16, 11, 11, (184, 88, 100, 255), width=6)
    elif kind == "flower":
        for i in range(5):
            ang = i * (2.0 * math.pi / 5.0) - 0.4
            oval(draw, x + 8 + math.cos(ang) * 20, y + 18 + math.sin(ang) * 14, 12, 12, (244, 176, 176, 255), width=6)
        oval(draw, x + 8, y + 18, 10, 10, BUTTER, width=6)
    elif kind == "cap":
        oval(draw, x, y + 20, 56, 20, (140, 96, 68, 255))
        poly(
            draw,
            [(x + 20, y + 22), (x + 78, y + 28), (x + 78, y + 40), (x + 16, y + 34)],
            (164, 116, 82, 255),
            width=7,
        )
    elif kind == "headphones":
        hy = HEAD_Y + dy
        draw.arc((CX - 92, hy - 108, CX + 92, hy + 8), 200, 340, fill=INK, width=14)
        oval(draw, CX - 98, hy + 6, 20, 26, (52, 44, 40, 255))
        oval(draw, CX + 98, hy + 6, 20, 26, (52, 44, 40, 255))
        oval(draw, CX - 98, hy + 6, 10, 14, TEAL, width=6)
        oval(draw, CX + 98, hy + 6, 10, 14, TEAL, width=6)
    elif kind == "leaf":
        poly(draw, [(x - 8, y + 28), (x + 42, y - 8), (x + 10, y + 34)], (122, 156, 112, 255))
    return img


def paint_wrap(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    img = blank()
    draw = ImageDraw.Draw(img)
    x, y = WRAP_X, WRAP_Y + hover_y(frame)
    if kind == "scarf":
        oval(draw, x, y, 78, 18, TEAL, width=8)
        poly(draw, [(x + 36, y), (x + 78, y + 54), (x + 54, y + 62), (x + 22, y + 10)], TEAL, width=8)
    elif kind == "bandana":
        oval(draw, x, y, 70, 14, CLAY, width=8)
        poly(draw, [(x + 48, y), (x + 82, y + 28), (x + 52, y + 12)], CLAY, width=7)
    elif kind == "bowtie":
        poly(draw, [(x - 8, y), (x - 40, y - 16), (x - 40, y + 16)], BUTTER, width=7)
        poly(draw, [(x + 8, y), (x + 40, y - 16), (x + 40, y + 16)], BUTTER, width=7)
        oval(draw, x, y, 9, 9, (196, 148, 64, 255), width=6)
    return img


def paint_charm(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    img = blank()
    draw = ImageDraw.Draw(img)
    bob = hover_y(frame) + math.sin((frame + 3) / FRAMES * math.pi * 2.0) * 2.2
    x, y = CHARM_X, CHARM_Y + bob
    if kind == "star":
        pts = []
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            r = 20 if i % 2 == 0 else 9
            pts.append((x + math.cos(ang) * r, y + math.sin(ang) * r))
        poly(draw, pts, BUTTER, width=6)
    elif kind == "pencil":
        poly(draw, [(x - 6, y + 22), (x + 6, y + 22), (x + 6, y - 10), (x - 6, y - 10)], CREAM, width=6)
        poly(draw, [(x - 6, y - 10), (x + 6, y - 10), (x, y - 24)], CLAY, width=6)
        oval(draw, x, y + 22, 7, 5, TEAL, width=5)
    elif kind == "heart":
        poly(
            draw,
            [
                (x, y + 16),
                (x - 16, y),
                (x - 6, y - 12),
                (x, y - 4),
                (x + 6, y - 12),
                (x + 16, y),
            ],
            CLAY,
            width=6,
        )
    elif kind == "balloon":
        oval(draw, x, y - 8, 18, 22, TEAL, width=7)
        draw.line((x, y + 14, x + 2, y + 36), fill=INK, width=4)
        poly(draw, [(x - 5, y + 12), (x + 5, y + 12), (x, y + 20)], TEAL, width=5)
    return img


TRAIT_SPEC = {
    "field": [
        ("cream", "Cream", 32),
        ("sky", "Sky", 26),
        ("clay", "Clay", 24),
        ("butter", "Butter", 18),
    ],
    "body": [
        ("bunny", "Bunny", 36),
        ("bear", "Bear", 28),
        ("pup", "Pup", 22),
        ("frog", "Frog", 14),
    ],
    "mug": [
        ("blink", "Normal", 20),
        ("grin", "Grin", 16),
        ("sleepy", "Sleepy", 14),
        ("blep", "Blep", 12),
        ("wink", "Wink", 12),
        ("spark", "Sparkly", 10),
        ("pout", "Pout", 9),
        ("heart", "Heart", 7),
    ],
    "hat": [
        ("none", "None", 24),
        ("beanie", "Beanie", 16),
        ("bow", "Bow", 14),
        ("flower", "Flower", 12),
        ("cap", "Cap", 12),
        ("headphones", "Headphones", 12),
        ("leaf", "Leaf", 10),
    ],
    "wrap": [
        ("none", "None", 40),
        ("scarf", "Scarf", 24),
        ("bandana", "Bandana", 20),
        ("bowtie", "Bowtie", 16),
    ],
    "charm": [
        ("none", "None", 36),
        ("star", "Star", 20),
        ("pencil", "Pencil", 18),
        ("heart", "Heart", 14),
        ("balloon", "Balloon", 12),
    ],
}

PAINTERS = {
    "field": {k: (lambda kind: (lambda frame, k=kind: paint_field(k, frame)))(k) for k in FIELDS},
    "body": {k: (lambda kind: (lambda frame, k=kind: paint_body(k, frame)))(k) for k in BODIES},
    "mug": {k: (lambda kind: (lambda frame, k=kind: paint_mug(k, frame)))(k) for k in MUGS},
    "hat": {k: (lambda kind: (lambda frame, k=kind: paint_hat(k, frame)))(k) for k in HATS},
    "wrap": {k: (lambda kind: (lambda frame, k=kind: paint_wrap(k, frame)))(k) for k in WRAPS},
    "charm": {k: (lambda kind: (lambda frame, k=kind: paint_charm(k, frame)))(k) for k in CHARMS},
}

STACK = ("field", "body", "mug", "hat", "wrap", "charm")

SIGNATURES = [
    {"field": "cream", "body": "bunny", "mug": "grin", "hat": "headphones", "wrap": "none", "charm": "star"},
    {"field": "sky", "body": "bear", "mug": "sleepy", "hat": "beanie", "wrap": "scarf", "charm": "none"},
    {"field": "clay", "body": "pup", "mug": "wink", "hat": "cap", "wrap": "bandana", "charm": "pencil"},
    {"field": "butter", "body": "frog", "mug": "blep", "hat": "leaf", "wrap": "none", "charm": "balloon"},
    {"field": "cream", "body": "bear", "mug": "spark", "hat": "bow", "wrap": "bowtie", "charm": "heart"},
    {"field": "sky", "body": "bunny", "mug": "pout", "hat": "flower", "wrap": "scarf", "charm": "none"},
    {"field": "clay", "body": "frog", "mug": "grin", "hat": "headphones", "wrap": "none", "charm": "star"},
    {"field": "butter", "body": "pup", "mug": "heart", "hat": "beanie", "wrap": "bowtie", "charm": "pencil"},
    {"field": "cream", "body": "frog", "mug": "sleepy", "hat": "none", "wrap": "bandana", "charm": "balloon"},
    {"field": "sky", "body": "pup", "mug": "blink", "hat": "flower", "wrap": "none", "charm": "heart"},
    {"field": "clay", "body": "bunny", "mug": "spark", "hat": "cap", "wrap": "scarf", "charm": "star"},
    {"field": "butter", "body": "bear", "mug": "wink", "hat": "headphones", "wrap": "none", "charm": "none"},
    {"field": "cream", "body": "pup", "mug": "grin", "hat": "bow", "wrap": "bandana", "charm": "balloon"},
    {"field": "sky", "body": "frog", "mug": "pout", "hat": "beanie", "wrap": "bowtie", "charm": "pencil"},
    {"field": "clay", "body": "bear", "mug": "blep", "hat": "leaf", "wrap": "scarf", "charm": "heart"},
    {"field": "butter", "body": "bunny", "mug": "sleepy", "hat": "none", "wrap": "none", "charm": "star"},
]

TRAIT_LABELS = (
    ("field", "Field"),
    ("body", "Body"),
    ("mug", "Mug"),
    ("hat", "Hat"),
    ("wrap", "Wrap"),
    ("charm", "Charm"),
)

COLLECTION_DESCRIPTION = (
    "Scribblins is a 5,555-piece collection of looping doodle-critter PFP GIFs. "
    "Each Scribblin is stacked from six layers — field, body, mug, hat, wrap, and charm — then flattened onto one 12-frame GIF. "
    "Four bodies. One locked friendly cartoon. Thick ink, warm paper, no rainbow."
)

COLLECTION_STORY = (
    "Scribblins never try that hard.\n\n"
    "A 5,555-piece collection of looping doodle-critter PFP GIFs on Base. "
    "Each Scribblin is stacked from six layers — field, body, mug, hat, wrap, and charm — then flattened onto one 12-frame GIF. "
    "Four bodies only: bunny, bear, pup, and frog. The drawing stays friendly — thick charcoal outline, "
    "big oval eyes, a little blush, warm paper instead of rainbow ink.\n\n"
    "Hats sit on one crown. Scarves sit on the neck. Charms float beside the paws. One shared clock.\n\n"
    "Minting on Base (chain ID 8453). Gas is ETH."
)


def trait_path(category: str, trait_id: str) -> Path:
    return TRAIT_DIR / category / f"{trait_id}.png"


def render_trait_frames(category: str, trait_id: str) -> list[Image.Image]:
    paint = PAINTERS[category][trait_id]
    return [paint(frame) for frame in range(FRAMES)]


def compose_selection(selection: dict[str, str]) -> list[Image.Image]:
    layers: list[list[Image.Image]] = []
    for category in STACK:
        trait_id = selection[category]
        if trait_id == "none":
            continue
        path = trait_path(category, trait_id)
        if path.exists():
            with Image.open(path) as im:
                im.load()
                n = getattr(im, "n_frames", 1)
                frames = []
                for i in range(n):
                    im.seek(i)
                    frames.append(im.convert("RGBA").copy())
                layers.append(frames)
        else:
            layers.append(render_trait_frames(category, trait_id))
    out = []
    for i in range(FRAMES):
        canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        for frames in layers:
            canvas = Image.alpha_composite(canvas, frames[i % len(frames)])
        out.append(canvas)
    return out


def name_of(category: str, trait_id: str) -> str:
    for item_id, name, _rarity in TRAIT_SPEC[category]:
        if item_id == trait_id:
            return name
    return trait_id


def build_traits(only: str | None = None, ids: list[str] | None = None) -> None:
    TRAIT_DIR.mkdir(parents=True, exist_ok=True)
    wanted = set(ids) if ids else None
    for category, traits in TRAIT_SPEC.items():
        if only and category != only:
            continue
        for trait_id, _name, _rarity in traits:
            if trait_id == "none":
                continue
            if wanted and trait_id not in wanted:
                continue
            print(f"  {category}/{trait_id}")
            save_apng(render_trait_frames(category, trait_id), trait_path(category, trait_id))
    manifest = {
        "name": "Scribblins",
        "size": SIZE,
        "frames": FRAMES,
        "durationMs": DURATION_MS,
        "format": "apng",
        "loop": 0,
        "order": list(STACK),
        "note": "Each trait is a looping APNG. Studio stacks them live. Minted tokens flatten to GIF. Four doodle bodies share one locked skeleton; hats, wraps, and charms never edit the body.",
    }
    (TRAIT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def build_samples() -> None:
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    samples = []
    for index, selection in enumerate(SIGNATURES, start=1):
        print(f"  sample #{index}")
        frames = compose_selection(selection)
        save_loop_gif(frames, PREVIEW_DIR / f"{index}.gif", DURATION_MS, colors=64)
        samples.append(
            {
                "id": index,
                "name": f"Scribblin #{index}",
                "image": f"/scribblins-preview/{index}.gif",
                "attributes": [
                    {"trait_type": label, "value": name_of(key, selection[key])} for key, label in TRAIT_LABELS
                ],
            }
        )
    (PREVIEW_DIR / "samples.json").write_text(json.dumps(samples, indent=2) + "\n", encoding="utf-8")
    write_ts_gallery(samples)


def write_ts_gallery(samples: list[dict]) -> None:
    SRC_DATA.mkdir(parents=True, exist_ok=True)
    rows = []
    for sample in samples:
        attrs = ",\n      ".join(
            f'{{ trait_type: "{a["trait_type"]}", value: "{a["value"]}" }}' for a in sample["attributes"]
        )
        rows.append(
            "  {\n"
            f"    id: {sample['id']},\n"
            f'    name: "{sample["name"]}",\n'
            f'    image: "{sample["image"]}?v=1",\n'
            f"    attributes: [\n      {attrs},\n    ],\n"
            "  }"
        )
    (SRC_DATA / "scribblin-gallery.ts").write_text(
        "export type ScribblinSample = {\n"
        "  id: number;\n"
        "  name: string;\n"
        "  image: string;\n"
        "  attributes: { trait_type: string; value: string }[];\n"
        "};\n\n"
        "export const scribblinSamples: ScribblinSample[] = [\n"
        + ",\n".join(rows)
        + "\n];\n",
        encoding="utf-8",
    )


def panoramic_wash(width: int, height: int) -> Image.Image:
    colors = np.array(
        [
            np.array(FIELDS["sky"][0], dtype=np.float32) / 255.0,
            np.array(FIELDS["cream"][0], dtype=np.float32) / 255.0,
            np.array((232, 176, 96), dtype=np.float32) / 255.0,
            np.array(FIELDS["clay"][0], dtype=np.float32) / 255.0,
        ],
        dtype=np.float32,
    )
    x = np.linspace(0.0, 1.0, width, dtype=np.float32)
    y = np.linspace(0.0, 1.0, height, dtype=np.float32)
    xx, yy = np.meshgrid(x, y)
    t = np.clip(xx * 0.72 + yy * 0.28, 0.0, 0.999) * (len(colors) - 1)
    i0 = np.floor(t).astype(np.int32)
    f = (t - i0)[..., None]
    c0 = colors[i0]
    c1 = colors[np.clip(i0 + 1, 0, len(colors) - 1)]
    rgb_out = c0 * (1.0 - f) + c1 * f
    arr = np.dstack([np.clip(rgb_out * 255.0, 0, 255).astype(np.uint8), np.full((height, width), 255, dtype=np.uint8)])
    return Image.fromarray(arr, "RGBA")


def write_collection_meta() -> None:
    META_DIR.mkdir(parents=True, exist_ok=True)
    (META_DIR / "scribblins-description.txt").write_text(COLLECTION_STORY + "\n", encoding="utf-8")
    (META_DIR / "scribblins.json").write_text(
        json.dumps(
            {
                "name": "Scribblins",
                "symbol": "SCRIB",
                "description": COLLECTION_DESCRIPTION,
                "image": "/brand/collection-scribblins.gif",
                "featured_image": "/brand/featured-scribblins.jpg",
                "banner_image": "/brand/banner-scribblins.png",
                "opensea_banner_image": "/brand/banner-scribblins-opensea.jpg",
                "external_link": "/scribblins",
                "seller_fee_basis_points": 500,
                "fee_recipient": "0x0000000000000000000000000000000000000000",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def build_brand() -> None:
    BRAND_DIR.mkdir(parents=True, exist_ok=True)
    portraits = [compose_selection(selection)[0] for selection in SIGNATURES[:7]]
    logo_frames = compose_selection(SIGNATURES[0])

    logo = logo_frames[0].copy()
    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).ellipse((18, 18, SIZE - 18, SIZE - 18), fill=255)
    logo.putalpha(Image.composite(logo.split()[-1], Image.new("L", (SIZE, SIZE), 0), mask))
    ring = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse((10, 10, SIZE - 10, SIZE - 10), outline=INK, width=10)
    logo = Image.alpha_composite(logo, ring)
    save_image(logo.resize((512, 512), Image.Resampling.LANCZOS), BRAND_DIR / "logo-scribblins.png")
    save_apng(
        [frame.resize((512, 512), Image.Resampling.LANCZOS) for frame in logo_frames],
        BRAND_DIR / "logo-scribblins-loop.png",
    )

    def doodle_lineup(width: int, height: int, faces: list[Image.Image]) -> Image.Image:
        canvas = panoramic_wash(width, height)
        count = len(faces)
        size = int(height * 0.82)
        overlap = size // 5
        total = size * count - overlap * (count - 1)
        start_x = (width - total) // 2
        y = (height - size) // 2 + int(height * 0.04)
        for index, portrait in enumerate(faces):
            px = start_x + index * (size - overlap)
            place_portrait(canvas, portrait, px, y, size, radius=max(36, size // 10))
        return canvas

    save_image(doodle_lineup(1500, 560, portraits[:5]).convert("RGB"), BRAND_DIR / "banner-scribblins.png", quality=94)
    save_image(doodle_lineup(2800, 700, portraits).convert("RGB"), BRAND_DIR / "banner-scribblins-opensea.jpg", quality=90)

    featured = panoramic_wash(1200, 800)
    place_portrait(featured, portraits[0], 90, 110, 560, radius=64)
    place_portrait(featured, portraits[3], 540, 130, 560, radius=64)
    save_image(featured.convert("RGB"), BRAND_DIR / "featured-scribblins.jpg", quality=90)

    gif_frames = [frame.resize((1000, 1000), Image.Resampling.LANCZOS) for frame in logo_frames]
    save_loop_gif(gif_frames, BRAND_DIR / "collection-scribblins.gif", DURATION_MS, colors=64)
    write_collection_meta()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--brand-only", action="store_true")
    parser.add_argument("--hats-only", action="store_true")
    parser.add_argument("--hat", action="append", dest="hats")
    args = parser.parse_args()
    if args.brand_only:
        print("Writing Scribblins brand kit…")
        build_brand()
        print("Done.")
        return
    if args.hats_only:
        print("Rebuilding Scribblins hat layers…")
        build_traits(only="hat", ids=args.hats)
        print("Compositing sample GIF tokens…")
        build_samples()
        print("Writing brand…")
        build_brand()
        print("Done.")
        return
    print("Building Scribblins doodle-critter trait loops…")
    build_traits()
    print("Compositing sample GIF tokens…")
    build_samples()
    print("Writing brand…")
    build_brand()
    print("Done.")


if __name__ == "__main__":
    main()
