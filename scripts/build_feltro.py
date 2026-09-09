#!/usr/bin/env python3
"""Paint Feltro — foam mascot suits on a gym floor.

Language: plush foam, mesh eyes, felt nap, stitched seams. A block head and
a cylindrical suit, not an egg, not a sticker cutout, not a charcoal doodle.
The suit stays in one envelope. The bounce is the dance.
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

from gif_bake import save_loop_gif  # noqa: E402
from paint_kit import DURATION_MS, FRAMES, SIZE, place_portrait, save_apng, save_image  # noqa: E402

GIF_COLORS = 96
GIF_DITHER = Image.Dither.NONE

TRAIT_DIR = ROOT / "public" / "feltro-traits"
PREVIEW_DIR = ROOT / "public" / "feltro-preview"
BRAND_DIR = ROOT / "public" / "brand"
META_DIR = ROOT / "public" / "metadata"
SRC_DATA = ROOT / "src" / "data"

SLUG = "feltro"
NAME = "Feltro"
SYMBOL = "FLTR"
TOKEN = "Suit"

GYMS = ("maple", "linoleum", "turf", "court", "night", "mat", "clay", "vinyl")
SUITS = ("bear", "lion", "frog", "bunny", "dino", "wolf", "octopus", "shark")
NAPS = ("down", "cross", "tight", "swirl")
MESHES = ("round", "visor", "button", "slit")
SEAMS = ("white", "black", "gold", "contrast")
CRESTS = ("none", "star", "patch", "letter", "badge")
FUZZES = ("none", "loose", "halo", "drift")

FOAM = {
    "bear": (176, 48, 52),
    "lion": (214, 154, 46),
    "frog": (42, 142, 78),
    "bunny": (236, 214, 198),
    "dino": (38, 148, 150),
    "wolf": (52, 64, 118),
    "octopus": (124, 58, 168),
    "shark": (72, 112, 132),
}
GYM = {
    "maple": ((92, 62, 40), (214, 176, 122), (168, 124, 74)),
    "linoleum": ((46, 78, 86), (196, 214, 210), (120, 168, 166)),
    "turf": ((28, 92, 48), (86, 156, 72), (214, 214, 208)),
    "court": ((214, 92, 48), (236, 214, 176), (232, 232, 228)),
    "night": ((18, 22, 36), (48, 56, 82), (210, 186, 92)),
    "mat": ((42, 48, 58), (92, 98, 108), (196, 78, 62)),
    "clay": ((122, 72, 48), (214, 154, 112), (168, 92, 62)),
    "vinyl": ((58, 42, 86), (176, 148, 214), (92, 214, 196)),
}
SEAM = {
    "white": (244, 236, 228),
    "black": (28, 24, 28),
    "gold": (214, 168, 64),
    "contrast": (236, 92, 48),
}


def blank() -> Image.Image:
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))


def shift(rgb: tuple[int, int, int], amount: int) -> tuple[int, int, int]:
    return tuple(max(0, min(255, channel + amount)) for channel in rgb)  # type: ignore[return-value]


def pose(frame: int) -> dict[str, int]:
    turn = frame / FRAMES * math.tau
    return {
        "bob": int(round(math.sin(turn) * 16)),
        "lean": int(round(math.sin(turn) * 10)),
        "larm": int(round(math.sin(turn) * 46)),
        "rarm": int(round(math.sin(turn + math.pi) * 46)),
        "step": int(round(math.sin(turn) * 18)),
        "squash": int(round(max(0.0, math.sin(turn)) * 8)),
    }


def capsule(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], radius: int, fill: tuple[int, int, int]) -> None:
    draw.line((start, end), fill=fill, width=radius * 2)
    draw.ellipse((start[0] - radius, start[1] - radius, start[0] + radius, start[1] + radius), fill=fill)
    draw.ellipse((end[0] - radius, end[1] - radius, end[0] + radius, end[1] + radius), fill=fill)


def paint_gym(kind: str, _frame: int) -> Image.Image:
    wall, floor, line = GYM[kind]
    image = Image.new("RGBA", (SIZE, SIZE), (*wall, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 286, SIZE, SIZE), fill=(*floor, 255))
    draw.line((0, 286, SIZE, 286), fill=shift(floor, -28), width=4)
    for offset in range(-1, 4):
        y = 318 + offset * 36
        draw.line((40, y, SIZE - 40, y), fill=(*line, 255), width=3)
    draw.rounded_rectangle((148, 330, 364, 470), radius=8, outline=(*line, 255), width=4)
    return image


def head_box(bob: int, lean: int) -> tuple[int, int, int, int]:
    return (168 + lean, 78 + bob, 344 + lean, 228 + bob)


def torso_box(bob: int, lean: int, squash: int) -> tuple[int, int, int, int]:
    return (172 + lean - squash, 214 + bob, 340 + lean + squash, 392 + bob)


def paint_suit(kind: str, frame: int) -> Image.Image:
    step = pose(frame)
    bob, lean, squash = step["bob"], step["lean"], step["squash"]
    foam = FOAM[kind]
    image = blank()
    draw = ImageDraw.Draw(image)
    dark = shift(foam, -42)
    light = shift(foam, 36)

    left_hip = (214 + lean, 372 + bob)
    right_hip = (298 + lean, 372 + bob)
    capsule(draw, left_hip, (198 + lean - step["step"], 448 + bob), 22, dark)
    capsule(draw, right_hip, (314 + lean + step["step"], 448 + bob), 22, dark)
    draw.rounded_rectangle(torso_box(bob, lean, squash), radius=42, fill=foam)
    draw.rounded_rectangle((196 + lean, 236 + bob, 246 + lean, 368 + bob), radius=10, fill=light)
    left_shoulder = (188 + lean, 246 + bob)
    right_shoulder = (324 + lean, 246 + bob)
    capsule(draw, left_shoulder, (148 + lean, 292 + bob - step["larm"]), 20, foam)
    capsule(draw, right_shoulder, (364 + lean, 292 + bob - step["rarm"]), 20, foam)
    draw.rounded_rectangle(head_box(bob, lean), radius=28, fill=foam)
    species(draw, kind, bob, lean, foam, light, dark)
    return image


def species(
    draw: ImageDraw.ImageDraw,
    kind: str,
    bob: int,
    lean: int,
    foam: tuple[int, int, int],
    light: tuple[int, int, int],
    dark: tuple[int, int, int],
) -> None:
    hx0, hy0, hx1, _hy1 = head_box(bob, lean)
    mid = (hx0 + hx1) // 2
    if kind == "bear":
        draw.ellipse((hx0 - 8, hy0 - 18, hx0 + 42, hy0 + 28), fill=foam)
        draw.ellipse((hx1 - 42, hy0 - 18, hx1 + 8, hy0 + 28), fill=foam)
        draw.rounded_rectangle((mid - 28, hy0 + 62, mid + 28, hy0 + 108), radius=12, fill=dark)
    elif kind == "lion":
        for index, angle in enumerate(range(0, 360, 24)):
            rad = math.radians(angle)
            cx = mid + int(math.cos(rad) * 78)
            cy = hy0 + 70 + int(math.sin(rad) * 62)
            draw.rounded_rectangle((cx - 14, cy - 16, cx + 14, cy + 16), radius=8, fill=shift(foam, -18 if index % 2 else 12))
        draw.rounded_rectangle((mid - 22, hy0 + 58, mid + 22, hy0 + 92), radius=8, fill=dark)
    elif kind == "frog":
        draw.rounded_rectangle((hx0 - 18, hy0 + 18, hx1 + 18, hy0 + 92), radius=18, fill=foam)
        draw.ellipse((hx0 + 8, hy0 + 8, hx0 + 52, hy0 + 42), fill=light)
        draw.ellipse((hx1 - 52, hy0 + 8, hx1 - 8, hy0 + 42), fill=light)
    elif kind == "bunny":
        draw.rounded_rectangle((hx0 + 18, hy0 - 78, hx0 + 48, hy0 + 16), radius=16, fill=foam)
        draw.rounded_rectangle((hx1 - 48, hy0 - 78, hx1 - 18, hy0 + 16), radius=16, fill=foam)
        draw.ellipse((mid - 16, hy0 + 72, mid + 16, hy0 + 96), fill=light)
    elif kind == "dino":
        draw.polygon([(hx1 - 8, hy0 + 48), (hx1 + 46, hy0 + 58), (hx1 - 4, hy0 + 78)], fill=foam)
        draw.rounded_rectangle((mid - 10, hy0 - 22, mid + 10, hy0 + 8), radius=4, fill=light)
        draw.polygon([(340 + lean, 360 + bob), (392 + lean, 392 + bob), (332 + lean, 400 + bob)], fill=dark)
    elif kind == "wolf":
        draw.polygon([(hx0 + 16, hy0 + 8), (hx0 + 28, hy0 - 36), (hx0 + 52, hy0 + 6)], fill=foam)
        draw.polygon([(hx1 - 16, hy0 + 8), (hx1 - 28, hy0 - 36), (hx1 - 52, hy0 + 6)], fill=foam)
        draw.polygon([(mid - 22, hy0 + 54), (mid + 22, hy0 + 58), (mid, hy0 + 108)], fill=dark)
    elif kind == "octopus":
        for index, x in enumerate((148, 176, 336, 364)):
            lift = 8 if index % 2 else -6
            draw.rounded_rectangle((x + lean, 300 + bob + lift, x + 22 + lean, 430 + bob), radius=10, fill=foam)
        draw.ellipse((mid - 18, hy0 + 70, mid + 18, hy0 + 98), fill=dark)
    else:
        draw.polygon([(hx1 - 20, hy0 + 36), (hx1 + 52, hy0 + 62), (hx1 - 12, hy0 + 86)], fill=foam)
        draw.polygon([(mid - 8, hy0 - 8), (mid + 18, hy0 - 48), (mid + 28, hy0 + 6)], fill=light)
        draw.polygon([(128 + lean, 268 + bob), (168 + lean, 286 + bob), (136 + lean, 318 + bob)], fill=dark)


def paint_nap(kind: str, frame: int) -> Image.Image:
    step = pose(frame)
    image = blank()
    draw = ImageDraw.Draw(image)
    box = torso_box(step["bob"], step["lean"], step["squash"])
    ink = (28, 22, 28, 70)
    if kind == "down":
        for x in range(box[0] + 12, box[2] - 8, 10):
            draw.line((x, box[1] + 16, x + 2, box[3] - 14), fill=ink, width=2)
    elif kind == "cross":
        for x in range(box[0] + 8, box[2], 14):
            draw.line((x, box[1] + 12, x + 18, box[3] - 10), fill=ink, width=2)
    elif kind == "tight":
        for y in range(box[1] + 16, box[3] - 8, 8):
            draw.line((box[0] + 14, y, box[2] - 14, y + 3), fill=ink, width=2)
    else:
        cx, cy = (box[0] + box[2]) // 2, (box[1] + box[3]) // 2
        for ring in range(16, 70, 12):
            draw.arc((cx - ring, cy - ring, cx + ring, cy + ring), 20, 250, fill=ink, width=2)
    return image


def paint_mesh(kind: str, frame: int) -> Image.Image:
    step = pose(frame)
    bob, lean = step["bob"], step["lean"]
    image = blank()
    draw = ImageDraw.Draw(image)
    screen = (18, 22, 28, 235)
    if kind == "round":
        for cx in (214, 292):
            draw.ellipse((cx + lean - 22, 128 + bob, cx + lean + 22, 172 + bob), fill=screen)
            mesh_grid(draw, cx + lean, 150 + bob, 18)
    elif kind == "visor":
        draw.rounded_rectangle((198 + lean, 126 + bob, 316 + lean, 168 + bob), radius=12, fill=screen)
        mesh_grid(draw, 256 + lean, 148 + bob, 28)
    elif kind == "button":
        for cx in (214, 292):
            draw.ellipse((cx + lean - 16, 132 + bob, cx + lean + 16, 168 + bob), fill=(236, 232, 224, 255))
            draw.ellipse((cx + lean - 8, 140 + bob, cx + lean + 8, 156 + bob), fill=screen)
    else:
        for cx in (214, 292):
            draw.rounded_rectangle((cx + lean - 20, 138 + bob, cx + lean + 20, 154 + bob), radius=4, fill=screen)
    return image


def mesh_grid(draw: ImageDraw.ImageDraw, cx: int, cy: int, span: int) -> None:
    line = (210, 214, 208, 120)
    for x in range(cx - span, cx + span, 6):
        draw.line((x, cy - span // 2, x, cy + span // 2), fill=line, width=1)
    for y in range(cy - span // 2, cy + span // 2, 5):
        draw.line((cx - span, y, cx + span, y), fill=line, width=1)


def paint_seam(kind: str, frame: int) -> Image.Image:
    step = pose(frame)
    bob, lean = step["bob"], step["lean"]
    image = blank()
    draw = ImageDraw.Draw(image)
    stitch = (*SEAM[kind], 255)
    draw.line((256 + lean, 92 + bob, 256 + lean, 372 + bob), fill=stitch, width=3)
    for y in range(110 + bob, 360 + bob, 12):
        draw.line((250 + lean, y, 262 + lean, y + 6), fill=stitch, width=2)
    box = torso_box(bob, lean, step["squash"])
    draw.rounded_rectangle(box, radius=42, outline=stitch, width=3)
    return image


def paint_crest(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    step = pose(frame)
    image = blank()
    draw = ImageDraw.Draw(image)
    cx, cy = 256 + step["lean"], 286 + step["bob"]
    if kind == "star":
        draw.regular_polygon((cx, cy, 28), 5, rotation=18, fill=(236, 196, 64, 255))
    elif kind == "patch":
        draw.rounded_rectangle((cx - 34, cy - 22, cx + 34, cy + 22), radius=8, fill=(244, 236, 220, 255))
        draw.rounded_rectangle((cx - 28, cy - 16, cx + 28, cy + 16), radius=6, outline=(176, 48, 52, 255), width=3)
    elif kind == "letter":
        draw.rounded_rectangle((cx - 26, cy - 26, cx + 26, cy + 26), radius=6, fill=(28, 24, 28, 255))
        draw.rectangle((cx - 10, cy - 14, cx + 10, cy + 14), fill=(244, 236, 220, 255))
    else:
        draw.ellipse((cx - 24, cy - 24, cx + 24, cy + 24), fill=(236, 92, 48, 255))
        draw.ellipse((cx - 12, cy - 12, cx + 12, cy + 12), fill=(244, 236, 220, 255))
    return image


def paint_fuzz(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    step = pose(frame)
    image = blank()
    draw = ImageDraw.Draw(image)
    turn = frame / FRAMES * math.tau
    fiber = (244, 228, 210, 180)
    if kind == "loose":
        for index in range(7):
            x = 150 + index * 32 + int(math.sin(turn + index) * 6)
            y = 70 + (index % 3) * 18 + step["bob"] // 2
            draw.line((x, y, x + 8, y - 14), fill=fiber, width=2)
    elif kind == "halo":
        hx0, hy0, hx1, hy1 = head_box(step["bob"], step["lean"])
        draw.arc((hx0 - 10, hy0 - 16, hx1 + 10, hy1 + 8), 200, 340, fill=fiber, width=3)
    else:
        for index in range(9):
            x = 80 + index * 42
            y = 40 + int(math.sin(turn + index * 0.7) * 10)
            draw.ellipse((x, y, x + 5, y + 5), fill=fiber)
    return image


PAINTERS = {
    "gym": {kind: (lambda frame, kind=kind: paint_gym(kind, frame)) for kind in GYMS},
    "suit": {kind: (lambda frame, kind=kind: paint_suit(kind, frame)) for kind in SUITS},
    "nap": {kind: (lambda frame, kind=kind: paint_nap(kind, frame)) for kind in NAPS},
    "mesh": {kind: (lambda frame, kind=kind: paint_mesh(kind, frame)) for kind in MESHES},
    "seam": {kind: (lambda frame, kind=kind: paint_seam(kind, frame)) for kind in SEAMS},
    "crest": {kind: (lambda frame, kind=kind: paint_crest(kind, frame)) for kind in CRESTS if kind != "none"},
    "fuzz": {kind: (lambda frame, kind=kind: paint_fuzz(kind, frame)) for kind in FUZZES if kind != "none"},
}

STACK = ("gym", "suit", "nap", "mesh", "seam", "crest", "fuzz")
TRAIT_LABELS = (
    ("gym", "Gym"),
    ("suit", "Suit"),
    ("nap", "Nap"),
    ("mesh", "Mesh"),
    ("seam", "Seam"),
    ("crest", "Crest"),
    ("fuzz", "Fuzz"),
)
TRAIT_SPEC = {
    "gym": [
        ("maple", "Maple Court", 18),
        ("linoleum", "Linoleum Court", 16),
        ("turf", "Turf Court", 14),
        ("court", "Wood Court", 14),
        ("night", "Night Court", 12),
        ("mat", "Mat Court", 10),
        ("clay", "Clay Court", 8),
        ("vinyl", "Vinyl Court", 8),
    ],
    "suit": [
        ("bear", "Bear Suit", 16),
        ("lion", "Lion Suit", 14),
        ("frog", "Frog Suit", 14),
        ("bunny", "Bunny Suit", 14),
        ("dino", "Dino Suit", 12),
        ("wolf", "Wolf Suit", 12),
        ("octopus", "Octopus Suit", 10),
        ("shark", "Shark Suit", 8),
    ],
    "nap": [
        ("down", "Down Nap", 30),
        ("cross", "Cross Nap", 26),
        ("tight", "Tight Nap", 24),
        ("swirl", "Swirl Nap", 20),
    ],
    "mesh": [
        ("round", "Round Mesh", 32),
        ("visor", "Visor Mesh", 28),
        ("button", "Button Eyes", 22),
        ("slit", "Slit Mesh", 18),
    ],
    "seam": [
        ("white", "White Seam", 32),
        ("black", "Black Seam", 28),
        ("gold", "Gold Seam", 22),
        ("contrast", "Contrast Seam", 18),
    ],
    "crest": [
        ("none", "No Crest", 28),
        ("star", "Star Crest", 22),
        ("patch", "Patch Crest", 20),
        ("letter", "Letter Crest", 16),
        ("badge", "Badge Crest", 14),
    ],
    "fuzz": [
        ("none", "Clean Air", 34),
        ("loose", "Loose Fuzz", 26),
        ("halo", "Halo Fuzz", 22),
        ("drift", "Drift Fuzz", 18),
    ],
}
SIGNATURES = [
    {"gym": "maple", "suit": "bear", "nap": "down", "mesh": "round", "seam": "white", "crest": "star", "fuzz": "loose"},
    {"gym": "night", "suit": "lion", "nap": "cross", "mesh": "visor", "seam": "gold", "crest": "badge", "fuzz": "halo"},
    {"gym": "turf", "suit": "frog", "nap": "tight", "mesh": "button", "seam": "black", "crest": "none", "fuzz": "none"},
    {"gym": "vinyl", "suit": "bunny", "nap": "swirl", "mesh": "round", "seam": "contrast", "crest": "patch", "fuzz": "drift"},
    {"gym": "court", "suit": "dino", "nap": "down", "mesh": "slit", "seam": "white", "crest": "letter", "fuzz": "loose"},
    {"gym": "mat", "suit": "wolf", "nap": "cross", "mesh": "visor", "seam": "black", "crest": "star", "fuzz": "none"},
    {"gym": "clay", "suit": "octopus", "nap": "swirl", "mesh": "round", "seam": "gold", "crest": "badge", "fuzz": "halo"},
    {"gym": "linoleum", "suit": "shark", "nap": "tight", "mesh": "button", "seam": "contrast", "crest": "letter", "fuzz": "drift"},
    {"gym": "night", "suit": "bear", "nap": "cross", "mesh": "slit", "seam": "gold", "crest": "patch", "fuzz": "loose"},
    {"gym": "turf", "suit": "lion", "nap": "down", "mesh": "round", "seam": "white", "crest": "none", "fuzz": "halo"},
    {"gym": "maple", "suit": "frog", "nap": "swirl", "mesh": "visor", "seam": "black", "crest": "star", "fuzz": "drift"},
    {"gym": "vinyl", "suit": "dino", "nap": "tight", "mesh": "round", "seam": "contrast", "crest": "badge", "fuzz": "loose"},
    {"gym": "court", "suit": "bunny", "nap": "down", "mesh": "button", "seam": "white", "crest": "patch", "fuzz": "none"},
    {"gym": "mat", "suit": "shark", "nap": "cross", "mesh": "slit", "seam": "gold", "crest": "star", "fuzz": "halo"},
    {"gym": "linoleum", "suit": "wolf", "nap": "swirl", "mesh": "visor", "seam": "contrast", "crest": "none", "fuzz": "drift"},
    {"gym": "clay", "suit": "octopus", "nap": "tight", "mesh": "button", "seam": "white", "crest": "letter", "fuzz": "loose"},
]

BLURBS = {
    "gym": "The floor under the suit — maple, linoleum, turf, court, night, mat, clay, vinyl.",
    "suit": "The dancing mascot. Eight foam suits: bear, lion, frog, bunny, dino, wolf, octopus, shark.",
    "nap": "Felt pile on the cylinder — down, cross, tight, swirl.",
    "mesh": "The eye screen — round, visor, button, slit.",
    "seam": "Stitch down the foam — white, black, gold, contrast.",
    "crest": "A badge on the chest — star, patch, letter, badge — or bare foam.",
    "fuzz": "Loose fibers in the air — loose, halo, drift — or clean air.",
}
NONE_LABELS = {"crest": "No Crest", "fuzz": "Clean Air"}
DEFAULTS = {key: SIGNATURES[0][key] for key in STACK}

COLLECTION_STORY = (
    "Feltro.\n\n"
    "A 10,000-piece collection of looping foam-mascot PFP GIFs on Robinhood Chain. "
    "Each suit is stacked from seven plates — gym, suit, nap, mesh, seam, crest, and fuzz — "
    "then flattened onto one 12-frame GIF. Eight dancing suits: bear, lion, frog, bunny, dino, wolf, octopus, and shark. "
    "Mesh covers the eyes. A seam runs the cylinder. The bounce is the loop.\n\n"
    "Plush foam on a court. Not a leather puppet. Not neon tubing. Not soy-ink blots. "
    "The suit stays seated in one envelope. The dance is the squash. One shared clock.\n\n"
    "Minting free on Robinhood Chain (chain ID 4663). Gas is ETH."
)
COLLECTION_DESCRIPTION = (
    "Feltro is a 10,000-piece collection of looping foam-mascot PFP GIFs. "
    "Each suit is stacked from seven plates — gym, suit, nap, mesh, seam, crest, and fuzz — "
    "then flattened onto one 12-frame GIF. Plush foam. Mesh eyes. A seam down the cylinder."
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
                frames = []
                for i in range(getattr(im, "n_frames", 1)):
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


def build_traits() -> None:
    TRAIT_DIR.mkdir(parents=True, exist_ok=True)
    for category, traits in TRAIT_SPEC.items():
        for trait_id, _name, _rarity in traits:
            if trait_id == "none":
                continue
            print(f"  {category}/{trait_id}")
            save_apng(render_trait_frames(category, trait_id), trait_path(category, trait_id))
    (TRAIT_DIR / "manifest.json").write_text(
        json.dumps(
            {
                "name": NAME,
                "size": SIZE,
                "frames": FRAMES,
                "durationMs": DURATION_MS,
                "format": "apng",
                "loop": 0,
                "order": list(STACK),
                "note": "Each trait is a looping APNG. Studio stacks them live. Minted tokens flatten to GIF.",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def build_samples() -> None:
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    samples = []
    for index, selection in enumerate(SIGNATURES, start=1):
        print(f"  sample #{index}")
        frames = compose_selection(selection)
        save_loop_gif(frames, PREVIEW_DIR / f"{index}.gif", DURATION_MS, colors=GIF_COLORS, dither=GIF_DITHER, palette_picks=FRAMES)
        samples.append(
            {
                "id": index,
                "name": f"{TOKEN} #{index}",
                "image": f"/{SLUG}-preview/{index}.gif",
                "attributes": [{"trait_type": label, "value": name_of(key, selection[key])} for key, label in TRAIT_LABELS],
            }
        )
    (PREVIEW_DIR / "samples.json").write_text(json.dumps(samples, indent=2) + "\n", encoding="utf-8")
    write_ts_gallery(samples)
    write_ts_traits()


def write_ts_gallery(samples: list[dict]) -> None:
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
    (SRC_DATA / f"{SLUG}-gallery.ts").write_text(
        f"export type {NAME}Sample = {{\n"
        "  id: number;\n"
        "  name: string;\n"
        "  image: string;\n"
        "  attributes: { trait_type: string; value: string }[];\n"
        "};\n\n"
        f"export const {SLUG}Samples: {NAME}Sample[] = [\n" + ",\n".join(rows) + "\n];\n",
        encoding="utf-8",
    )


def write_ts_traits() -> None:
    cats = []
    for key, label in TRAIT_LABELS:
        traits = []
        for trait_id, name, rarity in TRAIT_SPEC[key]:
            if trait_id == "none":
                continue
            traits.append(
                "      { "
                f'id: "{trait_id}", name: "{name}", image: "/{SLUG}-traits/{key}/{trait_id}.png", rarity: {rarity} '
                "}"
            )
        none = NONE_LABELS.get(key)
        none_line = f'\n    noneLabel: "{none}",' if none else ""
        cats.append(
            "  {\n"
            f'    id: "{key}",\n'
            f'    label: "{label}",\n'
            f'    blurb: "{BLURBS[key]}",'
            f"{none_line}\n"
            "    traits: [\n" + ",\n".join(traits) + ",\n    ],\n  }"
        )
    ids = " | ".join(f'"{key}"' for key, _label in TRAIT_LABELS)
    picks = ",\n".join(f'    {key}: pick({SLUG}CategoryById("{key}"))' for key, _label in TRAIT_LABELS)
    defaults = ",\n".join(f'  {key}: "{DEFAULTS[key]}"' for key in STACK)
    (SRC_DATA / f"{SLUG}-traits.ts").write_text(
        f"export type {NAME}Trait = {{\n"
        "  id: string;\n"
        "  name: string;\n"
        "  image?: string;\n"
        "  rarity: number;\n"
        "};\n\n"
        f"export type {NAME}TraitCategory = {{\n"
        f"  id: {ids};\n"
        "  label: string;\n"
        "  blurb: string;\n"
        "  noneLabel?: string;\n"
        f"  traits: {NAME}Trait[];\n"
        "};\n\n"
        f'export const {SYMBOL}_ART_VERSION = "{SLUG}-v1";\n\n'
        f"export const {SYMBOL}_FRAMES = 12;\n"
        f"export const {SYMBOL}_DURATION_MS = 90;\n\n"
        f"export function {SLUG}TraitSrc(path?: string) {{\n"
        '  if (!path) return "";\n'
        f"  return `${{path}}?v=${{{SYMBOL}_ART_VERSION}}`;\n"
        "}\n\n"
        f"export const {SLUG}TraitCategories: {NAME}TraitCategory[] = [\n" + ",\n".join(cats) + "\n];\n\n"
        f'export const none{NAME}Trait: {NAME}Trait = {{ id: "none", name: "None", rarity: 0 }};\n\n'
        f"export function {SLUG}CategoryById(id: {NAME}TraitCategory[\"id\"]) {{\n"
        f"  const category = {SLUG}TraitCategories.find((item) => item.id === id);\n"
        f"  if (!category) throw new Error(`Unknown {NAME} trait category: ${{id}}`);\n"
        "  return category;\n"
        "}\n\n"
        f"export function find{NAME}Trait(categoryId: {NAME}TraitCategory[\"id\"], traitId: string) {{\n"
        f'  if (traitId === "none") return none{NAME}Trait;\n'
        f"  return {SLUG}CategoryById(categoryId).traits.find((trait) => trait.id === traitId);\n"
        "}\n\n"
        f"export const default{NAME}Selection = {{\n{defaults},\n}} as const;\n\n"
        f"export type {NAME}Selection = Record<{NAME}TraitCategory[\"id\"], string>;\n\n"
        f"export function random{NAME}Selection(): {NAME}Selection {{\n"
        f"  const pick = (category: {NAME}TraitCategory) => {{\n"
        f"    const pool: {NAME}Trait[] = category.noneLabel\n"
        '      ? [{ id: "none", name: category.noneLabel, rarity: 22 }, ...category.traits]\n'
        "      : category.traits;\n"
        "    const total = pool.reduce((sum, trait) => sum + Math.max(trait.rarity, 1), 0);\n"
        "    let roll = Math.random() * total;\n"
        "    for (const trait of pool) {\n"
        "      roll -= Math.max(trait.rarity, 1);\n"
        "      if (roll <= 0) return trait.id;\n"
        "    }\n"
        "    return pool[0].id;\n"
        "  };\n\n"
        "  return {\n" + picks + ",\n  };\n"
        "}\n\n"
        f"export function {SLUG}CombinationCount() {{\n"
        f"  return {SLUG}TraitCategories.reduce((product, category) => {{\n"
        "    const extra = category.noneLabel ? 1 : 0;\n"
        "    return product * (category.traits.length + extra);\n"
        "  }, 1);\n"
        "}\n\n"
        f"export function {SLUG}SelectionToLayers(selection: {NAME}Selection) {{\n"
        f"  return ({json.dumps(list(STACK))} as const)\n"
        f"    .map((id) => find{NAME}Trait(id, selection[id]))\n"
        f"    .filter((trait): trait is {NAME}Trait => Boolean(trait?.image))\n"
        f"    .map((trait) => {SLUG}TraitSrc(trait.image));\n"
        "}\n",
        encoding="utf-8",
    )


def panoramic_wash(width: int, height: int) -> Image.Image:
    colors = np.array([[0.36, 0.22, 0.16], [0.86, 0.36, 0.28], [0.18, 0.16, 0.22], [0.78, 0.62, 0.42]], dtype=np.float32)
    x = np.linspace(0.0, 1.0, width, dtype=np.float32)
    yy = np.linspace(0.0, 1.0, height, dtype=np.float32)[:, None]
    xx = np.broadcast_to(x, (height, width))
    t = np.clip(xx * 0.62 + yy * 0.38, 0.0, 0.999) * (len(colors) - 1)
    i0 = np.floor(t).astype(np.int32)
    frac = (t - i0)[..., None]
    rgb_out = colors[i0] * (1.0 - frac) + colors[np.clip(i0 + 1, 0, len(colors) - 1)] * frac
    arr = np.dstack([np.clip(rgb_out * 255.0, 0, 255).astype(np.uint8), np.full((height, width), 255, dtype=np.uint8)])
    return Image.fromarray(arr, "RGBA")


def write_collection_meta() -> None:
    META_DIR.mkdir(parents=True, exist_ok=True)
    (META_DIR / f"{SLUG}-description.txt").write_text(COLLECTION_STORY + "\n", encoding="utf-8")
    (META_DIR / f"{SLUG}.json").write_text(
        json.dumps(
            {
                "name": NAME,
                "symbol": SYMBOL,
                "description": COLLECTION_DESCRIPTION,
                "image": f"/brand/collection-{SLUG}.gif",
                "featured_image": f"/brand/featured-{SLUG}.jpg",
                "banner_image": f"/brand/banner-{SLUG}.png",
                "opensea_banner_image": f"/brand/banner-{SLUG}-opensea.jpg",
                "external_link": f"/{SLUG}",
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
    ImageDraw.Draw(mask).rounded_rectangle((16, 16, SIZE - 17, SIZE - 17), radius=36, fill=255)
    logo.putalpha(Image.composite(logo.split()[-1], Image.new("L", (SIZE, SIZE), 0), mask))
    rim = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    ImageDraw.Draw(rim).rounded_rectangle((12, 12, SIZE - 13, SIZE - 13), radius=40, outline=(236, 92, 48, 255), width=4)
    logo = Image.alpha_composite(logo, rim)
    save_image(logo.resize((512, 512), Image.Resampling.LANCZOS), BRAND_DIR / f"logo-{SLUG}.png")
    save_apng([frame.resize((512, 512), Image.Resampling.LANCZOS) for frame in logo_frames], BRAND_DIR / f"logo-{SLUG}-loop.png")

    def lineup(width: int, height: int, faces: list[Image.Image]) -> Image.Image:
        canvas = panoramic_wash(width, height)
        count = len(faces)
        size = int(height * 0.82)
        overlap = size // 5
        total = size * count - overlap * (count - 1)
        start_x = (width - total) // 2
        y = (height - size) // 2 + int(height * 0.03)
        for index, portrait in enumerate(faces):
            place_portrait(canvas, portrait, start_x + index * (size - overlap), y, size, radius=max(20, size // 16))
        return canvas

    save_image(lineup(1500, 560, portraits[:5]).convert("RGB"), BRAND_DIR / f"banner-{SLUG}.png", quality=94)
    save_image(lineup(2800, 700, portraits).convert("RGB"), BRAND_DIR / f"banner-{SLUG}-opensea.jpg", quality=90)
    featured = panoramic_wash(1200, 800)
    place_portrait(featured, portraits[0], 90, 110, 560, radius=28)
    place_portrait(featured, portraits[2], 540, 130, 560, radius=28)
    save_image(featured.convert("RGB"), BRAND_DIR / f"featured-{SLUG}.jpg", quality=90)
    save_loop_gif(
        [frame.resize((1000, 1000), Image.Resampling.LANCZOS) for frame in logo_frames],
        BRAND_DIR / f"collection-{SLUG}.gif",
        DURATION_MS,
        colors=GIF_COLORS,
        dither=GIF_DITHER,
        palette_picks=FRAMES,
    )
    write_collection_meta()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--brand-only", action="store_true")
    args = parser.parse_args()
    if args.brand_only:
        print("Writing Feltro brand kit…")
        build_brand()
        print("Done.")
        return
    print("Building Feltro foam mascots…")
    build_traits()
    print("Compositing sample GIF tokens…")
    build_samples()
    print("Writing brand…")
    build_brand()
    print("Done.")


if __name__ == "__main__":
    main()
