#!/usr/bin/env python3
"""Paint Foxkins — Style 5 bold graphic fox, layered like Shook'ums.

Every trait is a 12-frame APNG on a shared 512 canvas and 90ms clock.
Pelt, mug, hat, and wrap share one hover so accessories never warp the skeleton.
Field stays still. Charm floats on its own tiny bob.

Look: flat sticker graphic — thick charcoal outline, limited palette, risograph grain.
Front-facing. Big circular head. Egg body. Tail on the right. Hats sit between the ears.
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

TRAIT_DIR = ROOT / "public" / "foxkins-traits"
PREVIEW_DIR = ROOT / "public" / "foxkins-preview"
BRAND_DIR = ROOT / "public" / "brand"
META_DIR = ROOT / "public" / "metadata"
SRC_DATA = ROOT / "src" / "data"

# Style 5 locked skeleton — front-facing graphic fox. Never edit per trait.
CX = 256.0
HEAD_Y = 216.0
HEAD_R = 118.0
BODY_Y = 368.0
BODY_RX, BODY_RY = 104.0, 90.0
HAT_X, HAT_Y = 256.0, 86.0
WRAP_X, WRAP_Y = 256.0, 312.0
CHARM_X, CHARM_Y = 410.0, 392.0
INK = (20, 16, 14, 255)
CREAM = (248, 236, 214, 255)
BLUSH = (244, 176, 176, 255)
LINE = 11

FIELDS = {
    "peach": ((243, 214, 196), (244, 184, 196)),
    "snow": ((226, 232, 236), (214, 222, 230)),
    "dusk": ((58, 42, 72), (168, 96, 120)),
    "hearth": ((92, 42, 32), (232, 132, 72)),
}

PELTS = {
    "maple": {"fur": (232, 122, 48, 255), "cream": CREAM, "ear": (36, 28, 24, 255)},
    "snow": {"fur": (236, 228, 218, 255), "cream": (255, 250, 244, 255), "ear": (232, 168, 160, 255)},
    "dusk": {"fur": (92, 72, 112, 255), "cream": (232, 208, 198, 255), "ear": (36, 26, 34, 255)},
}

MUGS = ("blink", "grin", "sleepy", "spark", "wink", "pout", "heart", "blep")
HATS = ("none", "beret", "cap", "flower", "leaf", "beanie", "bow")
WRAPS = ("none", "scarf", "bandana", "bell")
CHARMS = ("none", "acorn", "leaf", "lantern")


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
    return grain(img, amp=9, seed=11 + sum(ord(c) for c in kind))


def paint_pelt(kind: str, frame: int) -> Image.Image:
    pal = PELTS[kind]
    fur, cream, ear = pal["fur"], pal["cream"], pal["ear"]
    img = blank()
    draw = ImageDraw.Draw(img)
    dy = hover_y(frame)
    hx, hy = CX, HEAD_Y + dy
    bx, by = CX, BODY_Y + dy

    # Tail — comma on the right, cream tip.
    poly(
        draw,
        [
            (bx + 70, by - 10),
            (bx + 128, by - 70),
            (bx + 148, by - 30),
            (bx + 132, by + 36),
            (bx + 78, by + 28),
        ],
        fur,
    )
    poly(
        draw,
        [
            (bx + 126, by - 78),
            (bx + 158, by - 58),
            (bx + 146, by - 18),
            (bx + 118, by - 36),
        ],
        cream,
        width=8,
    )

    # Ears first so the head sits on top.
    poly(draw, [(hx - 86, hy - 18), (hx - 92, hy - 132), (hx - 28, hy - 58)], fur)
    poly(draw, [(hx + 86, hy - 18), (hx + 92, hy - 132), (hx + 28, hy - 58)], fur)
    poly(draw, [(hx - 72, hy - 28), (hx - 78, hy - 102), (hx - 40, hy - 52)], ear, width=6)
    poly(draw, [(hx + 72, hy - 28), (hx + 78, hy - 102), (hx + 40, hy - 52)], ear, width=6)

    # Egg body, then circular head.
    oval(draw, bx, by, BODY_RX, BODY_RY, fur)
    oval(draw, hx, hy, HEAD_R, HEAD_R * 0.96, fur)

    # Cream belly and teardrop muzzle.
    oval(draw, bx, by + 8, 44, 38, cream, width=8)
    poly(
        draw,
        [
            (hx, hy + 8),
            (hx - 62, hy + 38),
            (hx - 28, hy + 62),
            (hx, hy + 54),
            (hx + 28, hy + 62),
            (hx + 62, hy + 38),
        ],
        cream,
        width=8,
    )

    # Four paw nubs.
    for px, py, rx, ry in (
        (bx - 48, by + 62, 16, 12),
        (bx - 18, by + 74, 16, 11),
        (bx + 18, by + 74, 16, 11),
        (bx + 48, by + 62, 16, 12),
    ):
        oval(draw, px, py, rx, ry, fur, width=8)

    return grain(img, amp=6, seed=90 + sum(ord(c) for c in kind))


def paint_mug(kind: str, frame: int) -> Image.Image:
    img = blank()
    draw = ImageDraw.Draw(img)
    dy = hover_y(frame)
    blink = frame in (5, 6)
    lx, rx = CX - 40.0, CX + 40.0
    ey = HEAD_Y - 6.0 + dy
    mx, my = CX, HEAD_Y + 44.0 + dy

    def open_eye(x: float, y: float, r: float = 21.0) -> None:
        oval(draw, x, y, r, r, (16, 14, 12, 255), width=8)
        draw.ellipse((x - 8, y - 10, x - 1, y - 3), fill=(255, 255, 255, 255))
        draw.ellipse((x + 3, y + 2, x + 8, y + 7), fill=(255, 255, 255, 230))

    def shut_eye(x: float, y: float) -> None:
        draw.arc((x - 22, y - 10, x + 22, y + 14), 200, 340, fill=INK, width=7)

    left_shut = kind == "sleepy" or (kind == "wink") or (kind == "blink" and blink)
    right_shut = kind == "sleepy" or (kind == "blink" and blink)
    if left_shut:
        shut_eye(lx, ey)
    else:
        open_eye(lx, ey, 22.0 if kind == "spark" else 20.0)
    if right_shut:
        shut_eye(rx, ey)
    else:
        open_eye(rx, ey, 22.0 if kind == "spark" else 20.0)

    if kind == "grin":
        draw.arc((mx - 22, my - 6, mx + 22, my + 18), 10, 170, fill=INK, width=6)
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
            (232, 96, 118, 255),
            width=5,
        )
    elif kind == "spark":
        draw.line((mx - 6, my + 4, mx + 6, my + 4), fill=INK, width=5)
        for sx, sy in ((lx - 28, ey - 22), (rx + 26, ey - 18)):
            draw.line((sx, sy - 7, sx, sy + 7), fill=INK, width=3)
            draw.line((sx - 7, sy, sx + 7, sy), fill=INK, width=3)
    else:
        draw.arc((mx - 8, my - 2, mx + 8, my + 10), 20, 160, fill=INK, width=5)
    return img


def paint_hat(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    img = blank()
    draw = ImageDraw.Draw(img)
    x, y = HAT_X, HAT_Y + hover_y(frame)
    if kind == "beret":
        oval(draw, x + 8, y + 18, 62, 22, (48, 56, 92, 255))
        oval(draw, x + 36, y + 2, 12, 10, (36, 42, 72, 255), width=7)
    elif kind == "cap":
        oval(draw, x, y + 20, 56, 20, (72, 96, 68, 255))
        poly(draw, [(x + 20, y + 22), (x + 78, y + 28), (x + 78, y + 40), (x + 16, y + 34)], (88, 112, 82, 255), width=7)
    elif kind == "flower":
        for i in range(5):
            ang = i * (2.0 * math.pi / 5.0) - 0.4
            oval(draw, x + 8 + math.cos(ang) * 20, y + 18 + math.sin(ang) * 14, 12, 12, (244, 168, 180, 255), width=6)
        oval(draw, x + 8, y + 18, 10, 10, (244, 196, 72, 255), width=6)
    elif kind == "leaf":
        poly(
            draw,
            [(x - 8, y + 28), (x + 42, y - 8), (x + 10, y + 34)],
            (220, 92, 42, 255),
        )
    elif kind == "beanie":
        oval(draw, x, y + 22, 58, 24, (196, 72, 80, 255))
        oval(draw, x + 4, y - 2, 10, 10, CREAM, width=6)
    elif kind == "bow":
        poly(draw, [(x - 8, y + 16), (x - 44, y + 2), (x - 44, y + 30)], (232, 96, 128, 255), width=7)
        poly(draw, [(x + 8, y + 16), (x + 44, y + 2), (x + 44, y + 30)], (232, 96, 128, 255), width=7)
        oval(draw, x, y + 16, 10, 10, (196, 56, 88, 255), width=6)
    return img


def paint_wrap(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    img = blank()
    draw = ImageDraw.Draw(img)
    x, y = WRAP_X, WRAP_Y + hover_y(frame)
    if kind == "scarf":
        oval(draw, x, y, 78, 18, (48, 140, 132, 255), width=8)
        poly(draw, [(x + 36, y), (x + 78, y + 54), (x + 54, y + 62), (x + 22, y + 10)], (48, 140, 132, 255), width=8)
    elif kind == "bandana":
        oval(draw, x, y, 70, 14, (212, 64, 64, 255), width=8)
        poly(draw, [(x + 48, y), (x + 82, y + 28), (x + 52, y + 12)], (212, 64, 64, 255), width=7)
    elif kind == "bell":
        oval(draw, x, y, 64, 12, (36, 28, 24, 255), width=8)
        oval(draw, x, y + 20, 14, 16, (244, 196, 72, 255), width=7)
    return img


def paint_charm(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    img = blank()
    draw = ImageDraw.Draw(img)
    bob = hover_y(frame) + math.sin((frame + 3) / FRAMES * math.pi * 2.0) * 2.2
    x, y = CHARM_X, CHARM_Y + bob
    if kind == "acorn":
        oval(draw, x, y + 8, 14, 16, (148, 92, 48, 255), width=7)
        oval(draw, x, y - 6, 16, 10, (92, 62, 36, 255), width=7)
    elif kind == "leaf":
        poly(draw, [(x - 8, y + 14), (x + 22, y - 18), (x + 4, y + 18)], (220, 92, 42, 255))
    elif kind == "lantern":
        oval(draw, x, y, 16, 18, (244, 188, 72, 255), width=7)
        oval(draw, x, y - 18, 8, 6, (92, 62, 36, 255), width=6)
    return img


TRAIT_SPEC = {
    "field": [
        ("peach", "Peach", 32),
        ("snow", "Snow", 26),
        ("dusk", "Dusk", 24),
        ("hearth", "Hearth", 18),
    ],
    "pelt": [
        ("maple", "Maple", 55),
        ("snow", "Snow", 28),
        ("dusk", "Dusk", 17),
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
        ("none", "None", 28),
        ("leaf", "Leaf", 16),
        ("beret", "Beret", 14),
        ("flower", "Flower", 12),
        ("beanie", "Beanie", 12),
        ("cap", "Cap", 10),
        ("bow", "Bow", 8),
    ],
    "wrap": [
        ("none", "None", 40),
        ("scarf", "Scarf", 24),
        ("bandana", "Bandana", 20),
        ("bell", "Bell", 16),
    ],
    "charm": [
        ("none", "None", 40),
        ("acorn", "Acorn", 24),
        ("leaf", "Leaf", 20),
        ("lantern", "Lantern", 16),
    ],
}

PAINTERS = {
    "field": {k: (lambda kind: (lambda frame, k=kind: paint_field(k, frame)))(k) for k in FIELDS},
    "pelt": {k: (lambda kind: (lambda frame, k=kind: paint_pelt(k, frame)))(k) for k in PELTS},
    "mug": {k: (lambda kind: (lambda frame, k=kind: paint_mug(k, frame)))(k) for k in MUGS},
    "hat": {k: (lambda kind: (lambda frame, k=kind: paint_hat(k, frame)))(k) for k in HATS},
    "wrap": {k: (lambda kind: (lambda frame, k=kind: paint_wrap(k, frame)))(k) for k in WRAPS},
    "charm": {k: (lambda kind: (lambda frame, k=kind: paint_charm(k, frame)))(k) for k in CHARMS},
}

STACK = ("field", "pelt", "mug", "hat", "wrap", "charm")

SIGNATURES = [
    {"field": "peach", "pelt": "maple", "mug": "blink", "hat": "none", "wrap": "none", "charm": "none"},
    {"field": "peach", "pelt": "maple", "mug": "grin", "hat": "leaf", "wrap": "scarf", "charm": "acorn"},
    {"field": "dusk", "pelt": "dusk", "mug": "spark", "hat": "beret", "wrap": "bandana", "charm": "lantern"},
    {"field": "snow", "pelt": "snow", "mug": "sleepy", "hat": "beanie", "wrap": "none", "charm": "none"},
    {"field": "hearth", "pelt": "maple", "mug": "wink", "hat": "cap", "wrap": "bell", "charm": "leaf"},
    {"field": "peach", "pelt": "snow", "mug": "blep", "hat": "flower", "wrap": "scarf", "charm": "acorn"},
    {"field": "dusk", "pelt": "maple", "mug": "pout", "hat": "none", "wrap": "bandana", "charm": "lantern"},
    {"field": "snow", "pelt": "dusk", "mug": "grin", "hat": "leaf", "wrap": "none", "charm": "leaf"},
    {"field": "hearth", "pelt": "snow", "mug": "spark", "hat": "beret", "wrap": "scarf", "charm": "none"},
    {"field": "peach", "pelt": "dusk", "mug": "sleepy", "hat": "cap", "wrap": "bell", "charm": "acorn"},
    {"field": "dusk", "pelt": "snow", "mug": "wink", "hat": "flower", "wrap": "none", "charm": "lantern"},
    {"field": "hearth", "pelt": "dusk", "mug": "heart", "hat": "beanie", "wrap": "bandana", "charm": "leaf"},
    {"field": "snow", "pelt": "maple", "mug": "grin", "hat": "bow", "wrap": "bell", "charm": "acorn"},
    {"field": "peach", "pelt": "maple", "mug": "spark", "hat": "beret", "wrap": "none", "charm": "none"},
    {"field": "dusk", "pelt": "snow", "mug": "sleepy", "hat": "leaf", "wrap": "scarf", "charm": "lantern"},
    {"field": "hearth", "pelt": "maple", "mug": "blep", "hat": "flower", "wrap": "none", "charm": "leaf"},
]

TRAIT_LABELS = (
    ("field", "Field"),
    ("pelt", "Pelt"),
    ("mug", "Mug"),
    ("hat", "Hat"),
    ("wrap", "Wrap"),
    ("charm", "Charm"),
)

COLLECTION_DESCRIPTION = (
    "Foxkins is a 5,555-piece collection of looping bold-graphic fox PFP GIFs. "
    "Each Foxkin is stacked from six layers — field, pelt, mug, hat, wrap, and charm — then flattened onto one 12-frame GIF. "
    "Three pelts. One locked front-facing sticker. Hats sit between the ears. The silhouette never changes shape."
)

COLLECTION_STORY = (
    "Foxkins.\n\n"
    "A 5,555-piece collection of looping bold-graphic fox PFP GIFs. "
    "Each Foxkin is stacked from six layers — field, pelt, mug, hat, wrap, and charm — then flattened onto one 12-frame GIF. "
    "Three pelts only: maple, snow, and dusk. The sticker never gets a special cutout. "
    "Hats sit between the ears. Scarves sit on the neck. Charms float by the paws.\n\n"
    "Flat graphic — thick charcoal outline, limited palette, a little paper grain. "
    "Front-facing. Big circular head. Egg body. Tail on the right. One shared clock.\n\n"
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
    leftover = TRAIT_DIR / "field" / "grove.png"
    if leftover.exists():
        leftover.unlink()
    manifest = {
        "name": "Foxkins",
        "size": SIZE,
        "frames": FRAMES,
        "durationMs": DURATION_MS,
        "format": "apng",
        "loop": 0,
        "order": list(STACK),
        "note": "Each trait is a looping APNG. Studio stacks them live. Minted tokens flatten to GIF. Three pelt bodies share one Style 5 graphic skeleton; hats, wraps, and charms never edit the pelt.",
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
                "name": f"Foxkin #{index}",
                "image": f"/foxkins-preview/{index}.gif",
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
            f'    image: "{sample["image"]}?v=2",\n'
            f"    attributes: [\n      {attrs},\n    ],\n"
            "  }"
        )
    (SRC_DATA / "foxkin-gallery.ts").write_text(
        "export type FoxkinSample = {\n"
        "  id: number;\n"
        "  name: string;\n"
        "  image: string;\n"
        "  attributes: { trait_type: string; value: string }[];\n"
        "};\n\n"
        "export const foxkinSamples: FoxkinSample[] = [\n"
        + ",\n".join(rows)
        + "\n];\n",
        encoding="utf-8",
    )


def panoramic_wash(width: int, height: int) -> Image.Image:
    colors = np.array(
        [
            np.array(FIELDS["dusk"][0], dtype=np.float32) / 255.0,
            np.array(FIELDS["peach"][0], dtype=np.float32) / 255.0,
            np.array((232, 122, 48), dtype=np.float32) / 255.0,
            np.array(FIELDS["hearth"][0], dtype=np.float32) / 255.0,
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
    (META_DIR / "foxkins-description.txt").write_text(COLLECTION_STORY + "\n", encoding="utf-8")
    (META_DIR / "foxkins.json").write_text(
        json.dumps(
            {
                "name": "Foxkins",
                "symbol": "FOXK",
                "description": COLLECTION_DESCRIPTION,
                "image": "/brand/collection-foxkins.gif",
                "featured_image": "/brand/featured-foxkins.jpg",
                "banner_image": "/brand/banner-foxkins.png",
                "opensea_banner_image": "/brand/banner-foxkins-opensea.jpg",
                "external_link": "/foxkins",
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
    ImageDraw.Draw(ring).ellipse((10, 10, SIZE - 10, SIZE - 10), outline=(20, 16, 14, 255), width=10)
    logo = Image.alpha_composite(logo, ring)
    save_image(logo.resize((512, 512), Image.Resampling.LANCZOS), BRAND_DIR / "logo-foxkins.png")
    save_apng(
        [frame.resize((512, 512), Image.Resampling.LANCZOS) for frame in logo_frames],
        BRAND_DIR / "logo-foxkins-loop.png",
    )

    def fox_lineup(width: int, height: int, faces: list[Image.Image]) -> Image.Image:
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

    save_image(fox_lineup(1500, 560, portraits[:5]).convert("RGB"), BRAND_DIR / "banner-foxkins.png", quality=94)
    save_image(fox_lineup(2800, 700, portraits).convert("RGB"), BRAND_DIR / "banner-foxkins-opensea.jpg", quality=90)

    featured = panoramic_wash(1200, 800)
    place_portrait(featured, portraits[0], 90, 110, 560, radius=64)
    place_portrait(featured, portraits[3], 540, 130, 560, radius=64)
    save_image(featured.convert("RGB"), BRAND_DIR / "featured-foxkins.jpg", quality=90)

    gif_frames = [frame.resize((1000, 1000), Image.Resampling.LANCZOS) for frame in logo_frames]
    save_loop_gif(gif_frames, BRAND_DIR / "collection-foxkins.gif", DURATION_MS, colors=64)
    write_collection_meta()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--brand-only", action="store_true")
    parser.add_argument("--hats-only", action="store_true")
    parser.add_argument("--hat", action="append", dest="hats")
    args = parser.parse_args()
    if args.brand_only:
        print("Writing Foxkins brand kit…")
        build_brand()
        print("Done.")
        return
    if args.hats_only:
        print("Rebuilding Foxkins hat layers…")
        build_traits(only="hat", ids=args.hats)
        print("Compositing sample GIF tokens…")
        build_samples()
        print("Writing brand…")
        build_brand()
        print("Done.")
        return
    print("Building Foxkins Style 5 graphic trait loops…")
    build_traits()
    print("Compositing sample GIF tokens…")
    build_samples()
    print("Writing brand…")
    build_brand()
    print("Done.")


if __name__ == "__main__":
    main()
