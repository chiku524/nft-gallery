#!/usr/bin/env python3
"""Paint Purrkins — looping chibi-cat PFP layers for an OpenSea Drop on HyperEVM.

Every trait is a 12-frame APNG on a shared 512 canvas and 80ms clock, same as Loopkins.
Pelt, fit, mug, and gear share one bob so a stacked preview stays locked together.
Pad and glow move on their own loops.

Look: kawaii bust-crop cats — thick outlines, flat cel fills, streetwear, pastel pads.
Head and fit carry the portrait. No floating paws or tail. Ears twitch. Eyes blink.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from io import BytesIO
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from gif_bake import save_loop_gif  # noqa: E402

TRAIT_DIR = ROOT / "public" / "purrkins-traits"
PREVIEW_DIR = ROOT / "public" / "purrkins-preview"
BRAND_DIR = ROOT / "public" / "brand"
META_DIR = ROOT / "public" / "metadata"

SIZE = 512
FRAMES = 12
DURATION_MS = 80
H, W = SIZE, SIZE

HEAD = (256.0, 246.0)
HEAD_RX = 174.0
HEAD_RY = 162.0
# Tiny cropped bust — narrower than the head, so the cat reads chibi, not shoulders-first.
BUST_Y = 542.0
BUST_RX = 128.0
BUST_RY = 112.0

SOFT = 1.35


def clamp01(x: np.ndarray | float) -> np.ndarray | float:
    return np.clip(x, 0.0, 1.0)


def smoothstep(edge0: float, edge1: float, x: np.ndarray) -> np.ndarray:
    t = clamp01((x - edge0) / (edge1 - edge0))
    return t * t * (3.0 - 2.0 * t)


def rgb(hex_color: str) -> np.ndarray:
    value = hex_color.lstrip("#")
    return np.array([int(value[i : i + 2], 16) / 255.0 for i in (0, 2, 4)], dtype=np.float32)


LINE = rgb("1a1612")


def mix(a: np.ndarray | float, b: np.ndarray | float, t: float | np.ndarray) -> np.ndarray:
    a = np.asarray(a, dtype=np.float32)
    b = np.asarray(b, dtype=np.float32)
    t = np.asarray(t, dtype=np.float32)
    if t.ndim == 2 and a.ndim == 1:
        t = t[..., None]
    return a * (1.0 - t) + b * t


def blank() -> np.ndarray:
    return np.zeros((H, W, 4), dtype=np.float32)


def grid() -> tuple[np.ndarray, np.ndarray]:
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    return xx, yy


def over(dst: np.ndarray, src: np.ndarray) -> None:
    sa = src[..., 3:4]
    da = dst[..., 3:4]
    out_a = sa + da * (1.0 - sa)
    rgb_out = src[..., :3] * sa + dst[..., :3] * da * (1.0 - sa)
    dst[..., :3] = np.divide(rgb_out, out_a, out=np.zeros_like(rgb_out), where=out_a > 1e-6)
    dst[..., 3:4] = out_a


def shade(color: np.ndarray, t: float = 0.22) -> np.ndarray:
    return mix(color, rgb("0c0a10"), t)


def lite(color: np.ndarray, t: float = 0.32) -> np.ndarray:
    return mix(color, rgb("ffffff"), t)


def disc(
    dst: np.ndarray,
    cx: float,
    cy: float,
    r: float,
    color: np.ndarray,
    opacity: float = 1.0,
    soft: float = SOFT,
) -> None:
    xx, yy = grid()
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    a = smoothstep(r + soft, r - soft, d) * opacity
    layer = blank()
    layer[..., :3] = color
    layer[..., 3] = a
    over(dst, layer)


def ellipse(
    dst: np.ndarray,
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    color: np.ndarray,
    opacity: float = 1.0,
    soft: float = SOFT,
) -> None:
    xx, yy = grid()
    d = np.sqrt(((xx - cx) / max(rx, 1.0)) ** 2 + ((yy - cy) / max(ry, 1.0)) ** 2)
    edge = soft / max(rx, ry, 1.0)
    a = smoothstep(1.0 + edge, 1.0 - edge, d) * opacity
    layer = blank()
    layer[..., :3] = color
    layer[..., 3] = a
    over(dst, layer)


def rounded_rect(
    dst: np.ndarray,
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    color: np.ndarray,
    opacity: float = 1.0,
    radius: float = 10.0,
    soft: float = SOFT,
) -> None:
    xx, yy = grid()
    ax = np.abs(xx - cx) - (rx - radius)
    ay = np.abs(yy - cy) - (ry - radius)
    d = np.sqrt(np.maximum(ax, 0.0) ** 2 + np.maximum(ay, 0.0) ** 2) + np.minimum(np.maximum(ax, ay), 0.0) - radius
    a = smoothstep(soft, -soft, d) * opacity
    layer = blank()
    layer[..., :3] = color
    layer[..., 3] = a
    over(dst, layer)


def outlined_disc(
    dst: np.ndarray,
    cx: float,
    cy: float,
    r: float,
    color: np.ndarray,
    outline: np.ndarray | None = None,
    width: float = 4.0,
    opacity: float = 1.0,
    cel: bool = True,
) -> None:
    ring = LINE if outline is None else outline
    disc(dst, cx, cy, r + width, ring, opacity)
    disc(dst, cx, cy, r, color, opacity)
    if cel:
        disc(dst, cx - r * 0.26, cy - r * 0.28, r * 0.32, lite(color, 0.5), 0.34, soft=min(3.4, r * 0.16))
        disc(dst, cx + r * 0.12, cy + r * 0.24, r * 0.42, shade(color, 0.14), 0.16, soft=min(4.2, r * 0.2))


def outlined_ellipse(
    dst: np.ndarray,
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    color: np.ndarray,
    outline: np.ndarray | None = None,
    width: float = 4.0,
    opacity: float = 1.0,
    cel: bool = True,
) -> None:
    ring = LINE if outline is None else outline
    ellipse(dst, cx, cy, rx + width, ry + width, ring, opacity)
    ellipse(dst, cx, cy, rx, ry, color, opacity)
    if cel:
        ellipse(dst, cx - rx * 0.2, cy - ry * 0.28, rx * 0.36, ry * 0.28, lite(color, 0.42), 0.28, soft=3.2)
        ellipse(dst, cx + rx * 0.1, cy + ry * 0.22, rx * 0.44, ry * 0.36, shade(color, 0.14), 0.16, soft=4.0)


def outlined_roundrect(
    dst: np.ndarray,
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    color: np.ndarray,
    radius: float = 12.0,
    width: float = 3.6,
    opacity: float = 1.0,
) -> None:
    rounded_rect(dst, cx, cy, rx + width, ry + width, LINE, opacity, radius=radius + width * 0.4)
    rounded_rect(dst, cx, cy, rx, ry, color, opacity, radius=radius)


def fill_poly(dst: np.ndarray, points: list[tuple[float, float]], color: np.ndarray, opacity: float = 1.0) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    fill = tuple(int(round(c * 255)) for c in color) + (int(round(opacity * 255)),)
    draw.polygon([(float(x), float(y)) for x, y in points], fill=fill)
    over(dst, np.asarray(im, dtype=np.float32) / 255.0)


def outlined_ear(
    dst: np.ndarray,
    tip_x: float,
    tip_y: float,
    base_l: tuple[float, float],
    base_r: tuple[float, float],
    fur: np.ndarray,
    inner: np.ndarray,
) -> None:
    ox, oy = 6.5, 4.5
    fill_poly(
        dst,
        [(tip_x, tip_y - oy), (base_l[0] - ox, base_l[1] + oy), (base_r[0] + ox, base_r[1] + oy)],
        LINE,
    )
    fill_poly(dst, [(tip_x, tip_y), base_l, base_r], fur)
    mx = (base_l[0] + base_r[0] + tip_x) / 3
    my = (base_l[1] + base_r[1] + tip_y) / 3 + 10
    fill_poly(
        dst,
        [
            (mix_scalar(tip_x, mx, 0.22), mix_scalar(tip_y, my, 0.26)),
            (mix_scalar(base_l[0], mx, 0.18), mix_scalar(base_l[1], my, 0.16)),
            (mix_scalar(base_r[0], mx, 0.18), mix_scalar(base_r[1], my, 0.16)),
        ],
        inner,
        0.96,
    )


def mix_scalar(a: float, b: float, t: float) -> float:
    return a * (1.0 - t) + b * t


def glow(dst: np.ndarray, cx: float, cy: float, r: float, color: np.ndarray, opacity: float) -> None:
    xx, yy = grid()
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    a = np.exp(-0.5 * (d / max(r, 1.0)) ** 2) * opacity
    layer = blank()
    layer[..., :3] = color
    layer[..., 3] = a
    over(dst, layer)


def halo_ring(dst: np.ndarray, cx: float, cy: float, rx: float, ry: float, color: np.ndarray, opacity: float, stamp: float = 36.0, count: int = 18, spin: float = 0.0) -> None:
    """Soft aura stamped around an ellipse so it sits outside the cat, not under it."""
    for i in range(count):
        ang = spin + i * (2.0 * math.pi / count)
        glow(dst, cx + math.cos(ang) * rx, cy + math.sin(ang) * ry, stamp, color, opacity)


def grain(seed: int, amp: float = 0.03) -> np.ndarray:
    rng = np.random.default_rng(seed)
    small = (rng.random((SIZE // 16, SIZE // 16)) * 2 - 1).astype(np.float32)
    im = Image.fromarray(((small + 1) * 127.5).astype(np.uint8), "L")
    big = np.asarray(im.resize((W, H), Image.Resampling.BICUBIC), dtype=np.float32) / 127.5 - 1.0
    return big * amp


def write_bytes_retry(path: Path, data: bytes, attempts: int = 10) -> None:
    import time

    last_error: OSError | None = None
    for attempt in range(attempts):
        try:
            path.write_bytes(data)
            return
        except OSError as error:
            last_error = error
            time.sleep(0.15 * (attempt + 1))
    if last_error is not None:
        raise last_error


def save_image(image: Image.Image, path: Path, **kwargs) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fmt = kwargs.pop("format", None) or path.suffix.lstrip(".").upper()
    if fmt == "JPG":
        fmt = "JPEG"
    buffer = BytesIO()
    image.save(buffer, format=fmt, **kwargs)
    write_bytes_retry(path, buffer.getvalue())


def to_image(arr: np.ndarray) -> Image.Image:
    return Image.fromarray(np.clip(arr * 255.0, 0, 255).astype(np.uint8), "RGBA")


def save_apng(frames: list[Image.Image], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    stamped = []
    for index, frame in enumerate(frames):
        copy = frame.convert("RGBA")
        pixels = copy.load()
        r, g, b, a = pixels[0, 0]
        pixels[0, 0] = (r, g, b, max(a, 1) if a == 0 else a)
        pixels[1, 0] = (index, 0, FRAMES, 1)
        stamped.append(copy)
    stamped[0].save(
        buffer := BytesIO(),
        save_all=True,
        append_images=stamped[1:],
        duration=[DURATION_MS] * len(stamped),
        loop=0,
        format="PNG",
        disposal=1,
        blend=0,
        compress_level=6,
    )
    write_bytes_retry(path, buffer.getvalue())


def bob(frame: int, amp: float = 3.0) -> float:
    return math.sin(2 * math.pi * frame / FRAMES) * amp


def phase(frame: int) -> float:
    return 2.0 * math.pi * frame / FRAMES


def blink_amount(frame: int, closed_at: int = 8) -> float:
    dist = min(abs(frame - closed_at), abs(frame - closed_at + FRAMES), abs(frame - closed_at - FRAMES))
    if dist == 0:
        return 1.0
    if dist == 1:
        return 0.55
    return 0.0


# --- pad --------------------------------------------------------------------

PADS = {
    "blush": ("f3c9d6", "e8b0c4", 7),
    "lilac": ("cfc6ea", "b8add8", 11),
    "mint": ("c5e6d2", "9ecfb4", 13),
    "slate": ("9aa4ae", "7d8792", 17),
    "cream": ("f3ead8", "e4d4b8", 19),
    "teal": ("163e3c", "0f2c2c", 23),
    "peach": ("f3cbb4", "e4b094", 29),
    "night": ("0d221e", "081614", 31),
}


def paint_pad(kind: str, frame: int) -> np.ndarray:
    top_h, bot_h, seed = PADS[kind]
    xx, yy = grid()
    t = phase(frame)
    top, bot = rgb(top_h), rgb(bot_h)
    v = yy / (H - 1)
    wash = mix(top, bot, (v * 0.85 + 0.08 * math.sin(t))[..., None])
    arr = blank()
    arr[..., :3] = wash
    arr[..., 3] = 1.0
    arr[..., :3] = np.clip(arr[..., :3] + grain(seed, 0.018)[..., None], 0.0, 1.0)

    if kind in ("teal", "night"):
        for i in range(5):
            gy = 70 + i * 86 + math.sin(t + i) * 4
            ellipse(arr, 256, gy, 280, 3.2, lite(top, 0.18), 0.12 + 0.04 * math.sin(t + i))
        for i in range(10):
            px = float((47 * i + 22) % W)
            py = float((23 * i + 18) % 220)
            disc(arr, px, py, 2.2, rgb("e8fff4"), 0.35 + 0.15 * math.sin(t + i), soft=1.2)
    elif kind == "mint":
        for i, (px, py) in enumerate(((70, 80), (440, 120), (90, 400), (430, 380))):
            disc(arr, px, py + math.sin(t + i) * 4, 18, lite(top, 0.25), 0.28)
    elif kind == "blush":
        glow(arr, 256, 200, 180, rgb("ffd0e0"), 0.16 + 0.04 * math.sin(t))
    elif kind == "lilac":
        for i in range(6):
            ang = t * 0.4 + i * 1.047
            disc(arr, 256 + math.cos(ang) * 180, 256 + math.sin(ang) * 140, 14, lite(top, 0.2), 0.18)
    elif kind == "peach":
        outlined_disc(arr, 420, 72, 22, rgb("fff0d8"), rgb("e8c090"), width=2.2, cel=False)
        glow(arr, 420, 72, 40, rgb("ffe8c0"), 0.2)
    elif kind == "cream":
        rounded_rect(arr, 256, 470, 260, 50, shade(bot, 0.08), 0.55, radius=8)
    else:
        rounded_rect(arr, 40, 80, 18, 70, shade(bot, 0.12), 0.25, radius=6)
        rounded_rect(arr, 472, 340, 16, 90, shade(bot, 0.1), 0.22, radius=6)
    return arr


# --- glow -------------------------------------------------------------------

GLOWS = {
    "sparkle": "ffe8a0",
    "mint": "7dffb8",
    "gold": "ffd36a",
    "blush": "ff90c8",
}


def paint_glow(kind: str, frame: int) -> np.ndarray:
    arr = blank()
    t = phase(frame)
    color = rgb(GLOWS[kind])
    cx, cy = HEAD
    # Sit outside the skull, ears, and headphone cups so the loop stays readable.
    ring_rx = HEAD_RX + 62
    ring_ry = HEAD_RY + 52
    pulse = 0.38 + 0.08 * math.sin(t)
    halo_ring(arr, cx, cy, ring_rx, ring_ry, color, pulse * 0.8, stamp=46.0, count=22, spin=t * 0.12)
    glow(arr, cx, cy - HEAD_RY - 48, 92, color, pulse * 0.62)
    glow(arr, cx, cy + HEAD_RY + 28, 70, color, pulse * 0.4)

    if kind == "sparkle":
        for i in range(11):
            ang = t + i * 0.57
            orbit = 1.02 + 0.1 * math.sin(t * 1.4 + i)
            disc(
                arr,
                cx + math.cos(ang) * ring_rx * orbit,
                cy + math.sin(ang) * ring_ry * orbit,
                3.8,
                color,
                0.78,
                soft=1.3,
            )
    elif kind == "mint":
        halo_ring(arr, cx, cy, ring_rx + 18, ring_ry + 14, color, pulse * 0.4, stamp=28.0, count=14, spin=-t * 0.08)
    elif kind == "gold":
        for i in range(7):
            ang = t * 0.7 + i * 0.9
            drift = 16 * math.sin(t + i * 0.8)
            disc(
                arr,
                cx + math.cos(ang) * (ring_rx + 10) + drift * 0.3,
                cy + math.sin(ang) * (ring_ry + 6) - abs(drift) * 0.2,
                5.5,
                color,
                0.62,
                soft=1.6,
            )
    else:
        glow(arr, cx - ring_rx, cy + 18, 56, color, pulse * 0.7)
        glow(arr, cx + ring_rx, cy + 18, 56, color, pulse * 0.7)
    return arr


# --- pelt -------------------------------------------------------------------

PELTS = {
    "cream": {
        "fur": "f4eee4",
        "mark": "c8b8a8",
        "inner": "f2b4ac",
        "belly": "fffaf4",
        "nose": "2a221c",
        "stripes": False,
        "seed": 11,
    },
    "ginger": {
        "fur": "e89a48",
        "mark": "c07028",
        "inner": "f0a898",
        "belly": "f8d8b0",
        "nose": "3a2214",
        "stripes": True,
        "seed": 17,
    },
    "soot": {
        "fur": "2c2c34",
        "mark": "1a1a22",
        "inner": "c08090",
        "belly": "4a4a54",
        "nose": "121218",
        "stripes": False,
        "seed": 23,
    },
    "mist": {
        "fur": "c4c0bc",
        "mark": "8e8a86",
        "inner": "e8b4ac",
        "belly": "ece8e4",
        "nose": "2a2624",
        "stripes": True,
        "seed": 29,
    },
    "calico": {
        "fur": "f2ebe0",
        "mark": "e09040",
        "inner": "f0b0a8",
        "belly": "fff8f0",
        "nose": "2c2018",
        "stripes": False,
        "seed": 31,
        "patch": True,
    },
    "matcha": {
        "fur": "8ec478",
        "mark": "5a8a48",
        "inner": "f0b8a8",
        "belly": "d8f0c8",
        "nose": "243018",
        "stripes": False,
        "seed": 37,
    },
}


def paint_pelt(kind: str, frame: int) -> np.ndarray:
    palette = PELTS[kind]
    fur, mark, inner, belly, nose = (rgb(palette[k]) for k in ("fur", "mark", "inner", "belly", "nose"))
    arr = blank()
    dy = bob(frame)
    cx, cy = HEAD[0], HEAD[1] + dy
    t = phase(frame)
    twitch = math.sin(t * 2) * 2.4
    rx, ry = HEAD_RX, HEAD_RY
    soot = rgb("2c2c34")
    ginger = rgb("e09040")

    # Tiny cropped chest. Clothing covers this; bare cats keep a hint of fur.
    outlined_ellipse(arr, cx, BUST_Y, BUST_RX - 8, BUST_RY - 4, fur, width=3.8)
    ellipse(arr, cx, 486, 42, 32, belly, 0.9, soft=2.4)

    left_tip = (cx - rx * 0.70, cy - ry - 44 + twitch)
    left_out = (cx - rx * 0.98, cy - ry + 56)
    left_in = (cx - rx * 0.24, cy - ry + 18)
    right_tip = (cx + rx * 0.70, cy - ry - 44 - twitch * 0.55)
    right_in = (cx + rx * 0.24, cy - ry + 18)
    right_out = (cx + rx * 0.98, cy - ry + 56)

    outlined_ear(arr, left_tip[0], left_tip[1], left_out, left_in, fur, inner)
    outlined_ear(arr, right_tip[0], right_tip[1], right_in, right_out, fur, inner)

    def ear_point(tip: tuple[float, float], outer: tuple[float, float], inner_pt: tuple[float, float], color: np.ndarray, opacity: float) -> None:
        fill_poly(
            arr,
            [
                tip,
                (mix_scalar(tip[0], outer[0], 0.55), mix_scalar(tip[1], outer[1], 0.55)),
                (mix_scalar(tip[0], inner_pt[0], 0.55), mix_scalar(tip[1], inner_pt[1], 0.55)),
            ],
            color,
            opacity,
        )

    if kind in ("cream", "matcha"):
        ear_point(left_tip, left_out, left_in, mark, 0.82 if kind == "matcha" else 0.7)
        ear_point(right_tip, right_out, right_in, mark, 0.82 if kind == "matcha" else 0.7)
    elif kind == "calico":
        ear_point(left_tip, left_out, left_in, soot, 0.94)

    outlined_ellipse(arr, cx, cy, rx, ry, fur, width=4.6)

    if kind == "soot":
        ellipse(arr, cx, cy + ry * 0.08, rx * 0.36, ry * 0.40, belly, 0.88, soft=2.8)
        ellipse(arr, cx, cy - ry * 0.22, rx * 0.22, ry * 0.14, lite(fur, 0.18), 0.45, soft=2.6)
    elif kind == "calico":
        ellipse(arr, cx + rx * 0.38, cy - ry * 0.32, rx * 0.30, ry * 0.26, ginger, 0.94, soft=2.2)
        ellipse(arr, cx + rx * 0.46, cy - ry * 0.04, rx * 0.18, ry * 0.16, ginger, 0.88, soft=2.0)
        ellipse(arr, cx - rx * 0.42, cy + ry * 0.30, rx * 0.18, ry * 0.14, soot, 0.9, soft=2.0)
        ellipse(arr, cx + 28, 488, 26, 20, ginger, 0.85, soft=2.0)
    elif kind == "cream":
        ellipse(arr, cx - rx * 0.48, cy - ry * 0.04, 24, 18, mark, 0.22, soft=2.4)
        ellipse(arr, cx + rx * 0.48, cy - ry * 0.04, 24, 18, mark, 0.22, soft=2.4)
    elif kind == "matcha":
        ellipse(arr, cx, cy - ry * 0.38, 28, 18, mark, 0.55, soft=2.0)
        fill_poly(
            arr,
            [(cx - 12, cy - ry * 0.46), (cx, cy - ry * 0.28), (cx + 12, cy - ry * 0.46), (cx, cy - ry * 0.52)],
            mark,
            0.45,
        )

    if palette.get("stripes") or kind == "ginger":
        top = cy - ry * 0.46
        fill_poly(
            arr,
            [
                (cx - 32, top),
                (cx - 20, top + 36),
                (cx - 9, top + 16),
                (cx, top + 38),
                (cx + 9, top + 16),
                (cx + 20, top + 36),
                (cx + 32, top),
                (cx + 18, top),
                (cx + 11, top + 16),
                (cx, top + 24),
                (cx - 11, top + 16),
                (cx - 18, top),
            ],
            mark,
            0.82,
        )
        for side in (-1.0, 1.0):
            rounded_rect(arr, cx + side * rx * 0.54, cy + ry * 0.22, 17, 5.4, mark, 0.68, radius=3, soft=1.3)
            rounded_rect(arr, cx + side * rx * 0.50, cy + ry * 0.32, 14, 4.6, mark, 0.5, radius=3, soft=1.3)

    if kind == "mist":
        ellipse(arr, cx - rx * 0.42, cy + ry * 0.04, 18, 13, mark, 0.28, soft=2.2)
        ellipse(arr, cx + rx * 0.42, cy + ry * 0.04, 18, 13, mark, 0.28, soft=2.2)

    ellipse(arr, cx, cy + ry * 0.14, 40, 30, belly, 0.55, soft=2.8)
    disc(arr, cx - rx * 0.44, cy + ry * 0.20, 17, inner, 0.4, soft=3.0)
    disc(arr, cx + rx * 0.44, cy + ry * 0.20, 17, inner, 0.4, soft=3.0)

    outlined_ellipse(arr, cx, cy + ry * 0.18, 8.4, 6.0, nose, width=1.6, cel=False)
    disc(arr, cx - 2.4, cy + ry * 0.16, 2.0, rgb("ffffff"), 0.55, soft=1.0)
    return arr


# --- fit --------------------------------------------------------------------

FITS = {
    "hoodie": ("2f6a4a", "1e4632"),
    "tee": ("3a6ea8", "2a4e78"),
    "jacket": ("2a2e38", "ff5a6a"),
    "polo": ("f4f0ea", "2a6a48"),
    "cardigan": ("c07050", "f0d8c0"),
}


def paint_fit(kind: str, frame: int) -> np.ndarray:
    arr = blank()
    cx, cy = HEAD[0], HEAD[1] + bob(frame)
    main, trim = (rgb(c) for c in FITS[kind])
    body_y = BUST_Y + bob(frame)
    neck = cy + HEAD_RY + 4
    if kind == "hoodie":
        outlined_ellipse(arr, cx, body_y, BUST_RX, BUST_RY, main, width=3.8, cel=False)
        ellipse(arr, cx, neck - 4, 62, 14, shade(main, 0.12), 0.95, soft=2.0)
        rounded_rect(arr, cx, neck + 8, 48, 10, shade(main, 0.16), 0.95, radius=6)
        rounded_rect(arr, cx, 470, 32, 16, shade(main, 0.12), 0.95, radius=8)
    elif kind == "tee":
        outlined_ellipse(arr, cx, body_y, BUST_RX - 4, BUST_RY - 2, main, width=3.6, cel=False)
        fill_poly(
            arr,
            [
                (cx - 28, neck - 6),
                (cx + 28, neck - 6),
                (cx + 16, neck + 16),
                (cx - 16, neck + 16),
            ],
            shade(main, 0.18),
        )
        rounded_rect(arr, cx, 468, 7, 18, trim, 0.9, radius=3)
    elif kind == "jacket":
        outlined_ellipse(arr, cx, body_y, BUST_RX + 2, BUST_RY, main, width=3.8, cel=False)
        ellipse(arr, cx, 468, 26, 32, rgb("f4eee4"), 0.55)
        rounded_rect(arr, cx - 42, 458, 11, 20, trim, 0.95, radius=4)
        rounded_rect(arr, cx + 42, 458, 11, 20, trim, 0.95, radius=4)
        fill_poly(arr, [(cx - 20, neck - 2), (cx - 4, neck - 2), (cx - 10, neck + 28)], main)
        fill_poly(arr, [(cx + 4, neck - 2), (cx + 20, neck - 2), (cx + 10, neck + 28)], main)
    elif kind == "polo":
        outlined_ellipse(arr, cx, body_y, BUST_RX - 4, BUST_RY - 2, main, width=3.6, cel=False)
        fill_poly(
            arr,
            [
                (cx - 22, neck - 2),
                (cx, neck + 18),
                (cx + 22, neck - 2),
                (cx + 10, neck - 2),
                (cx, neck + 10),
                (cx - 10, neck - 2),
            ],
            trim,
        )
        disc(arr, cx, neck + 20, 3.6, trim, 0.95)
    else:
        outlined_ellipse(arr, cx, body_y, BUST_RX - 2, BUST_RY - 2, main, width=3.6, cel=False)
        for y in (456.0, 472.0, 488.0):
            disc(arr, cx, y, 3.6, rgb("f0d8c0"), 0.95)
        ellipse(arr, cx, 468, 26, 30, trim, 0.5)
    return arr


# --- mug --------------------------------------------------------------------

def paint_mug(kind: str, frame: int) -> np.ndarray:
    arr = blank()
    cx, cy = HEAD[0], HEAD[1] + bob(frame)
    t = phase(frame)
    closed = blink_amount(frame)
    ink = LINE
    shine = rgb("fff8e8")
    pink = rgb("ff5a88")
    gold = rgb("ffe060")

    def eye(ex: float, ey: float, shut: float, heart: bool = False, spark: bool = False, wide: bool = False) -> None:
        r = 10.0 if wide else 8.6
        if shut >= 0.9:
            ellipse(arr, ex, ey + 2, r + 3, 2.6, ink, 0.96, soft=1.2)
            return
        if heart:
            disc(arr, ex, ey + 1.2, 7.0, pink, 0.98, soft=1.3)
            disc(arr, ex - 3.6, ey - 1.4, 4.0, pink, 0.95, soft=1.2)
            disc(arr, ex + 3.6, ey - 1.4, 4.0, pink, 0.95, soft=1.2)
            disc(arr, ex - 2.2, ey - 2.6, 1.6, shine, 0.85, soft=0.8)
        elif spark:
            disc(arr, ex, ey + 0.8, 7.0, gold, 0.98, soft=1.3)
            disc(arr, ex, ey + 0.8, 3.0, ink, 0.95, soft=1.0)
            disc(arr, ex - 2.2, ey - 2.0, 1.8, shine, 0.9, soft=0.8)
        else:
            disc(arr, ex, ey + 1.0, r, ink, 0.98, soft=1.2)
            disc(arr, ex - 2.0, ey - 1.6, 2.0, shine, 0.9, soft=0.8)
        if shut > 0.35:
            ellipse(arr, ex, ey - 5, r + 2, 5.5 * shut, ink, 0.88, soft=1.3)

    lx, rx, ey = cx - HEAD_RX * 0.30, cx + HEAD_RX * 0.30, cy + HEAD_RY * 0.04

    if kind == "wink":
        eye(lx, ey, 0.0)
        eye(rx, ey, 1.0)
    elif kind == "sleepy":
        eye(lx, ey + 2, 0.62)
        eye(rx, ey + 2, 0.62)
    elif kind == "spark":
        eye(lx, ey, closed, spark=True)
        eye(rx, ey, closed, spark=True)
    elif kind == "heart":
        eye(lx, ey, closed, heart=True)
        eye(rx, ey, closed, heart=True)
    elif kind == "wide":
        eye(lx, ey - 1, closed, wide=True)
        eye(rx, ey - 1, closed, wide=True)
    else:
        eye(lx, ey, closed)
        eye(rx, ey, closed)

    my = cy + HEAD_RY * 0.34
    if kind == "sleepy":
        ellipse(arr, cx, my, 9, 1.8, ink, 0.8, soft=1.2)
    elif kind == "grin":
        ellipse(arr, cx, my + 3, 14, 2.6, ink, 0.9, soft=1.3)
    elif kind == "wide":
        ellipse(arr, cx, my + 2, 6.5, 4.2, ink, 0.88, soft=1.2)
    else:
        ellipse(arr, cx - 5.2, my, 5.0, 2.0, ink, 0.9, soft=1.1)
        ellipse(arr, cx + 5.2, my, 5.0, 2.0, ink, 0.9, soft=1.1)

    for side in (-1, 1):
        ellipse(arr, cx + side * HEAD_RX * 0.50, cy + HEAD_RY * 0.20, 15, 1.3, ink, 0.42, soft=1.1)
        ellipse(arr, cx + side * HEAD_RX * 0.48, cy + HEAD_RY * 0.26, 13, 1.15, ink, 0.32, soft=1.1)

    if kind == "spark":
        disc(arr, cx + HEAD_RX * 0.46, cy - HEAD_RY * 0.30, 3, gold, 0.7 + 0.2 * math.sin(t), soft=1.2)
    return arr


# --- gear -------------------------------------------------------------------

def paint_gear(kind: str, frame: int) -> np.ndarray:
    arr = blank()
    cx, cy = HEAD[0], HEAD[1] + bob(frame)
    t = phase(frame)
    sway = math.sin(t) * 2.0
    rx, ry = HEAD_RX, HEAD_RY

    if kind == "beanie":
        hat = rgb("2a6a9a")
        trim = rgb("f0e8d8")
        outlined_ellipse(arr, cx, cy - ry + 22, rx * 0.70, 44, hat, width=3.4, cel=False)
        rounded_rect(arr, cx, cy - ry + 48, rx * 0.74, 16, trim, 0.98, radius=8)
        outlined_disc(arr, cx + 4, cy - ry - 16, 16, rgb("f0e8d8"), width=2.6, cel=False)
    elif kind == "cap":
        hat = rgb("1e3a28")
        outlined_ellipse(arr, cx + 8, cy - ry + 28, rx * 0.66, 36, hat, width=3.2, cel=False)
        fill_poly(
            arr,
            [
                (cx - 20, cy - ry + 46),
                (cx + rx * 0.82, cy - ry + 60),
                (cx + rx * 0.76, cy - ry + 80),
                (cx - 6, cy - ry + 62),
            ],
            hat,
        )
        fill_poly(
            arr,
            [
                (cx - 22, cy - ry + 44),
                (cx + rx * 0.84, cy - ry + 58),
                (cx + rx * 0.82, cy - ry + 62),
                (cx - 16, cy - ry + 48),
            ],
            LINE,
            0.7,
        )
        disc(arr, cx + 10, cy - ry + 28, 6, rgb("e8e0d0"), 0.9)
    elif kind == "bucket":
        hat = rgb("f2a0b8")
        outlined_ellipse(arr, cx, cy - ry + 38, rx * 0.78, 18, hat, width=3.2, cel=False)
        outlined_ellipse(arr, cx, cy - ry + 16, rx * 0.58, 32, hat, width=3.2, cel=False)
        for i in range(5):
            rounded_rect(arr, cx - rx * 0.36 + i * (rx * 0.18), cy - ry + 16, 5, 10, rgb("2a8a48"), 0.85, radius=2)
    elif kind == "shades":
        glass = rgb("141820")
        ex = HEAD_RX * 0.30
        ey = cy + HEAD_RY * 0.04
        outlined_roundrect(arr, cx - ex, ey, 30, 15, glass, radius=8, width=3.0)
        outlined_roundrect(arr, cx + ex, ey, 30, 15, glass, radius=8, width=3.0)
        rounded_rect(arr, cx, ey - 2, 18, 3.2, rgb("2a2e38"), 0.95, radius=2)
        ellipse(arr, cx - ex - 8, ey - 4, 9, 3, rgb("7dffb8"), 0.55 + 0.15 * math.sin(t), soft=1.4)
    elif kind == "phones":
        cup = rgb("2a2e38")
        outlined_ellipse(arr, cx, cy - ry + 10, rx * 0.62, 16, cup, width=3.0, cel=False)
        outlined_disc(arr, cx - rx + 6, cy + 8, 26, cup, width=3.2, cel=False)
        outlined_disc(arr, cx + rx - 6, cy + 8, 26, cup, width=3.2, cel=False)
        disc(arr, cx - rx + 6, cy + 8, 14, rgb("1a1e24"), 0.95)
        disc(arr, cx + rx - 6, cy + 8, 14, rgb("1a1e24"), 0.95)
        ellipse(arr, cx - rx + 6, cy, 8, 3, rgb("7dffb8"), 0.4, soft=1.3)
    elif kind == "phone":
        outlined_roundrect(arr, cx + 88 + sway, 482, 16, 26, rgb("1a1e24"), radius=6, width=3.0)
        rounded_rect(arr, cx + 88 + sway, 480, 12, 20, rgb("7dffd0"), 0.9, radius=4)
        disc(arr, cx + 88 + sway, 462, 2.2, rgb("e8e0d0"), 0.9)
    else:
        cup = rgb("f4eee4")
        outlined_roundrect(arr, cx - 88 + sway, 480, 16, 22, cup, radius=6, width=3.0)
        rounded_rect(arr, cx - 88 + sway, 462, 18, 6, rgb("2a6a4a"), 0.95, radius=3)
        ellipse(arr, cx - 88 + sway, 474, 11, 4.5, rgb("5a3a24"), 0.9, soft=1.4)
        rounded_rect(arr, cx - 70 + sway, 480, 3, 9, LINE, 0.85, radius=2)
        steam = 0.45 + 0.2 * math.sin(t)
        ellipse(arr, cx - 94 + sway, 444, 4, 10, rgb("e8f0ff"), steam, soft=2.2)
        ellipse(arr, cx - 82 + sway, 438, 3.5, 9, rgb("e8f0ff"), steam * 0.8, soft=2.0)
    return arr


# --- catalog ----------------------------------------------------------------

TRAIT_SPEC = {
    "pad": [
        ("blush", "Blush", 14),
        ("lilac", "Lilac", 14),
        ("mint", "Mint", 14),
        ("slate", "Slate", 12),
        ("cream", "Cream", 12),
        ("teal", "Teal Desk", 12),
        ("peach", "Peach", 12),
        ("night", "Night Desk", 10),
    ],
    "glow": [
        ("none", "No glow", 28),
        ("sparkle", "Sparkle", 18),
        ("mint", "Mint Halo", 18),
        ("gold", "Gold Dust", 18),
        ("blush", "Blush Bloom", 18),
    ],
    "pelt": [
        ("cream", "Cream", 22),
        ("ginger", "Ginger", 18),
        ("soot", "Soot", 16),
        ("mist", "Mist", 16),
        ("calico", "Calico", 14),
        ("matcha", "Matcha", 14),
    ],
    "fit": [
        ("none", "No fit", 20),
        ("hoodie", "Forest Hoodie", 18),
        ("tee", "Blue Tee", 16),
        ("jacket", "Ink Jacket", 16),
        ("polo", "Cream Polo", 16),
        ("cardigan", "Clay Cardigan", 14),
    ],
    "mug": [
        ("blink", "Blink", 22),
        ("wink", "Wink", 16),
        ("sleepy", "Sleepy", 16),
        ("grin", "Grin", 16),
        ("spark", "Spark", 16),
        ("heart", "Heart", 14),
        ("wide", "Wide", 14),
    ],
    "gear": [
        ("none", "None", 22),
        ("beanie", "Beanie", 14),
        ("cap", "Back Cap", 14),
        ("bucket", "Bucket Hat", 12),
        ("shades", "Shades", 12),
        ("phones", "Headphones", 12),
        ("phone", "Phone", 10),
        ("coffee", "Coffee", 10),
    ],
}

PAINTERS = {
    "pad": {k: (lambda kind: (lambda frame, k=kind: paint_pad(k, frame)))(k) for k in PADS},
    "glow": {k: (lambda kind: (lambda frame, k=kind: paint_glow(k, frame)))(k) for k in GLOWS},
    "pelt": {k: (lambda kind: (lambda frame, k=kind: paint_pelt(k, frame)))(k) for k in PELTS},
    "fit": {k: (lambda kind: (lambda frame, k=kind: paint_fit(k, frame)))(k) for k in FITS},
    "mug": {
        k: (lambda kind: (lambda frame, k=kind: paint_mug(k, frame)))(k)
        for k in ("blink", "wink", "sleepy", "grin", "spark", "heart", "wide")
    },
    "gear": {
        k: (lambda kind: (lambda frame, k=kind: paint_gear(k, frame)))(k)
        for k in ("beanie", "cap", "bucket", "shades", "phones", "phone", "coffee")
    },
}

STACK = ("pad", "glow", "pelt", "fit", "mug", "gear")

SIGNATURES = [
    {"pad": "teal", "glow": "mint", "pelt": "cream", "fit": "hoodie", "mug": "blink", "gear": "phones"},
    {"pad": "blush", "glow": "sparkle", "pelt": "ginger", "fit": "tee", "mug": "wink", "gear": "cap"},
    {"pad": "lilac", "glow": "blush", "pelt": "calico", "fit": "cardigan", "mug": "heart", "gear": "bucket"},
    {"pad": "mint", "glow": "gold", "pelt": "matcha", "fit": "polo", "mug": "spark", "gear": "coffee"},
    {"pad": "night", "glow": "mint", "pelt": "soot", "fit": "jacket", "mug": "grin", "gear": "shades"},
    {"pad": "cream", "glow": "none", "pelt": "mist", "fit": "none", "mug": "sleepy", "gear": "beanie"},
    {"pad": "peach", "glow": "sparkle", "pelt": "cream", "fit": "hoodie", "mug": "wide", "gear": "phone"},
    {"pad": "slate", "glow": "gold", "pelt": "ginger", "fit": "jacket", "mug": "blink", "gear": "none"},
    {"pad": "teal", "glow": "none", "pelt": "matcha", "fit": "tee", "mug": "wink", "gear": "phones"},
    {"pad": "blush", "glow": "blush", "pelt": "soot", "fit": "cardigan", "mug": "sleepy", "gear": "coffee"},
    {"pad": "lilac", "glow": "mint", "pelt": "mist", "fit": "polo", "mug": "grin", "gear": "cap"},
    {"pad": "mint", "glow": "sparkle", "pelt": "calico", "fit": "hoodie", "mug": "spark", "gear": "none"},
    {"pad": "night", "glow": "gold", "pelt": "cream", "fit": "none", "mug": "heart", "gear": "bucket"},
    {"pad": "cream", "glow": "mint", "pelt": "ginger", "fit": "jacket", "mug": "wide", "gear": "shades"},
    {"pad": "peach", "glow": "none", "pelt": "matcha", "fit": "cardigan", "mug": "blink", "gear": "beanie"},
    {"pad": "slate", "glow": "blush", "pelt": "calico", "fit": "tee", "mug": "wink", "gear": "phone"},
]

TRAIT_LABELS = (
    ("pad", "Pad"),
    ("glow", "Glow"),
    ("pelt", "Pelt"),
    ("fit", "Fit"),
    ("mug", "Mug"),
    ("gear", "Gear"),
)


def trait_path(category: str, trait_id: str) -> Path:
    return TRAIT_DIR / category / f"{trait_id}.png"


def render_trait_frames(category: str, trait_id: str) -> list[Image.Image]:
    paint = PAINTERS[category][trait_id]
    return [to_image(paint(frame)) for frame in range(FRAMES)]


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


def build_traits() -> None:
    TRAIT_DIR.mkdir(parents=True, exist_ok=True)
    for category, traits in TRAIT_SPEC.items():
        for trait_id, _name, _rarity in traits:
            if trait_id == "none":
                continue
            print(f"  {category}/{trait_id}")
            save_apng(render_trait_frames(category, trait_id), trait_path(category, trait_id))
    manifest = {
        "name": "Purrkins",
        "size": SIZE,
        "frames": FRAMES,
        "durationMs": DURATION_MS,
        "format": "apng",
        "loop": 0,
        "order": list(STACK),
        "note": "Each trait is a looping APNG. Studio stacks them live. Minted tokens flatten to GIF.",
    }
    (TRAIT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def build_samples() -> None:
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    META_DIR.mkdir(parents=True, exist_ok=True)
    samples = []
    for index, selection in enumerate(SIGNATURES, start=1):
        print(f"  sample #{index}")
        frames = compose_selection(selection)
        save_loop_gif(frames, PREVIEW_DIR / f"{index}.gif", DURATION_MS)
        samples.append(
            {
                "id": index,
                "name": f"Purrkin #{index}",
                "image": f"/purrkins-preview/{index}.gif",
                "attributes": [
                    {"trait_type": label, "value": name_of(key, selection[key])} for key, label in TRAIT_LABELS
                ],
            }
        )
    (META_DIR / "purrkins-samples.json").write_text(json.dumps(samples, indent=2) + "\n", encoding="utf-8")


COLLECTION_DESCRIPTION = (
    "Purrkins is a 10,000-piece collection of looping chibi-cat PFP GIFs on HyperEVM. "
    "Each cat is stacked from six layers — pad, glow, pelt, fit, mug, and gear — "
    "then flattened onto one 12-frame GIF. Thick outlines. Flat fills. Streetwear. "
    "Ears twitch. Eyes blink. Soft bob."
)

COLLECTION_STORY = (
    "Purrkins never sit still.\n\n"
    "A 10,000-piece collection of looping chibi-cat PFP GIFs on HyperEVM. "
    "Each Purrkin is stacked from six layers — pad, glow, pelt, fit, mug, and gear — "
    "then flattened onto one 12-frame GIF. Pastel desks behind them. Hoodies and beanies "
    "on top. Ears twitch. Eyes blink. Soft bob.\n\n"
    "Kawaii bust-crop cats with thick outlines, flat cel fills, and streetwear. One shared clock.\n\n"
    "Minting on HyperEVM (chain ID 999). Gas is HYPE."
)


def panoramic_wash(width: int, height: int, frame: int = 0) -> Image.Image:
    left = np.asarray(to_image(paint_pad("night", frame)).resize((width, height), Image.Resampling.LANCZOS), dtype=np.float32)
    mid = np.asarray(to_image(paint_pad("teal", frame)).resize((width, height), Image.Resampling.LANCZOS), dtype=np.float32)
    right = np.asarray(to_image(paint_pad("mint", frame)).resize((width, height), Image.Resampling.LANCZOS), dtype=np.float32)
    x = np.linspace(0.0, 1.0, width, dtype=np.float32)[None, :, None]
    w_left = np.clip(1.0 - x / 0.42, 0.0, 1.0)
    w_right = np.clip((x - 0.58) / 0.42, 0.0, 1.0)
    w_mid = np.clip(1.0 - w_left - w_right, 0.0, 1.0)
    out = left * w_left + mid * w_mid + right * w_right
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).convert("RGBA")


def rounded_portrait(portrait: Image.Image, size: int, radius: int = 56) -> Image.Image:
    face = portrait.resize((size, size), Image.Resampling.LANCZOS).convert("RGBA")
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=255)
    face.putalpha(Image.composite(face.split()[-1], Image.new("L", (size, size), 0), mask))
    return face


def place_portrait(canvas: Image.Image, portrait: Image.Image, x: int, y: int, size: int, radius: int = 56) -> None:
    face = rounded_portrait(portrait, size, radius)
    shadow = Image.new("RGBA", (size + 24, size + 24), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((8, 14, size + 8, size + 18), radius=radius, fill=(8, 20, 18, 90))
    canvas.alpha_composite(shadow, (x - 8, y - 6))
    canvas.alpha_composite(face, (x, y))


def lineup_banner(width: int, height: int, portraits: list[Image.Image]) -> Image.Image:
    canvas = panoramic_wash(width, height, frame=4)
    count = len(portraits)
    size = int(height * 0.82)
    overlap = size // 5
    total = size * count - overlap * (count - 1)
    start_x = (width - total) // 2
    y = (height - size) // 2 + int(height * 0.04)
    for index, portrait in enumerate(portraits):
        x = start_x + index * (size - overlap)
        place_portrait(canvas, portrait, x, y, size, radius=max(36, size // 10))
    return canvas


def write_collection_meta() -> None:
    META_DIR.mkdir(parents=True, exist_ok=True)
    (META_DIR / "purrkins-description.txt").write_text(COLLECTION_STORY + "\n", encoding="utf-8")
    (META_DIR / "purrkins.json").write_text(
        json.dumps(
            {
                "name": "Purrkins",
                "symbol": "PURR",
                "description": COLLECTION_DESCRIPTION,
                "image": "/brand/collection-purrkins.gif",
                "featured_image": "/brand/featured-purrkins.jpg",
                "banner_image": "/brand/banner-purrkins.png",
                "opensea_banner_image": "/brand/banner-purrkins-opensea.jpg",
                "external_link": "/purrkins",
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
    ImageDraw.Draw(ring).ellipse((10, 10, SIZE - 10, SIZE - 10), outline=(125, 255, 184, 220), width=10)
    logo = Image.alpha_composite(logo, ring)
    save_image(logo.resize((512, 512), Image.Resampling.LANCZOS), BRAND_DIR / "logo-purrkins.png")
    save_apng(
        [frame.resize((512, 512), Image.Resampling.LANCZOS) for frame in logo_frames],
        BRAND_DIR / "logo-purrkins-loop.png",
    )

    site_banner = lineup_banner(1500, 560, portraits[:5])
    save_image(site_banner.convert("RGB"), BRAND_DIR / "banner-purrkins.png", quality=94)

    opensea_banner = lineup_banner(2800, 700, portraits)
    save_image(opensea_banner.convert("RGB"), BRAND_DIR / "banner-purrkins-opensea.jpg", quality=90)

    featured = panoramic_wash(1200, 800, frame=8)
    place_portrait(featured, portraits[0], 90, 110, 560, radius=64)
    place_portrait(featured, portraits[2], 540, 130, 560, radius=64)
    save_image(featured.convert("RGB"), BRAND_DIR / "featured-purrkins.jpg", quality=90)

    gif_frames = [frame.resize((1000, 1000), Image.Resampling.LANCZOS) for frame in logo_frames]
    save_loop_gif(gif_frames, BRAND_DIR / "collection-purrkins.gif", DURATION_MS)
    write_collection_meta()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--brand-only", action="store_true", help="Rebuild logo, banners, and listing copy")
    args = parser.parse_args()
    if args.brand_only:
        print("Writing Purrkins brand kit…")
        build_brand()
        print("Done.")
        return
    print("Building Purrkins trait loops…")
    build_traits()
    print("Compositing sample GIF tokens…")
    build_samples()
    print("Writing brand…")
    build_brand()
    print("Done.")


if __name__ == "__main__":
    main()
