#!/usr/bin/env python3
"""Paint Party Pandas — looping party-panda PFP layers for an OpenSea Drop on Base.

Every trait is a 12-frame APNG on a shared 512 canvas and 80ms clock, same as Loopkins.
Panda, mood, fit, and extra share one bob so a stacked preview stays locked together.
Venue and glow move on their own loops.

Look: cartoon illustration of a real giant panda — crisp outlines, cel shading,
classic black-and-white markings.
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

TRAIT_DIR = ROOT / "public" / "party-pandas-traits"
PREVIEW_DIR = ROOT / "public" / "party-pandas-preview"
BRAND_DIR = ROOT / "public" / "brand"
META_DIR = ROOT / "public" / "metadata"

SIZE = 512
FRAMES = 12
DURATION_MS = 80
H, W = SIZE, SIZE

HEAD = (256.0, 236.0)


def clamp01(x: np.ndarray | float) -> np.ndarray | float:
    return np.clip(x, 0.0, 1.0)


def smoothstep(edge0: float, edge1: float, x: np.ndarray) -> np.ndarray:
    t = clamp01((x - edge0) / (edge1 - edge0))
    return t * t * (3.0 - 2.0 * t)


def rgb(hex_color: str) -> np.ndarray:
    value = hex_color.lstrip("#")
    return np.array([int(value[i : i + 2], 16) / 255.0 for i in (0, 2, 4)], dtype=np.float32)


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


SOFT = 2.2
LINE = rgb("1a1420")


def shade(color: np.ndarray, t: float = 0.22) -> np.ndarray:
    return mix(color, rgb("0c0a12"), t)


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
    width: float = 3.2,
    opacity: float = 1.0,
    cel: bool = True,
) -> None:
    ring = LINE if outline is None else outline
    disc(dst, cx, cy, r + width, ring, opacity)
    disc(dst, cx, cy, r, color, opacity)
    if cel:
        disc(dst, cx - r * 0.22, cy - r * 0.26, r * 0.38, lite(color, 0.45), 0.28, soft=min(4.0, r * 0.18))
        disc(dst, cx + r * 0.1, cy + r * 0.22, r * 0.48, shade(color, 0.18), 0.22, soft=min(5.0, r * 0.22))


def outlined_ellipse(
    dst: np.ndarray,
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    color: np.ndarray,
    outline: np.ndarray | None = None,
    width: float = 3.2,
    opacity: float = 1.0,
    cel: bool = True,
) -> None:
    ring = LINE if outline is None else outline
    ellipse(dst, cx, cy, rx + width, ry + width, ring, opacity)
    ellipse(dst, cx, cy, rx, ry, color, opacity)
    if cel:
        ellipse(dst, cx - rx * 0.18, cy - ry * 0.28, rx * 0.42, ry * 0.32, lite(color, 0.4), 0.26, soft=4.0)
        ellipse(dst, cx + rx * 0.08, cy + ry * 0.22, rx * 0.5, ry * 0.42, shade(color, 0.16), 0.2, soft=5.0)


def fur_speckle(dst: np.ndarray, seed: int, amp: float = 0.05) -> None:
    rng = np.random.default_rng(seed)
    noise = rng.random((H, W), dtype=np.float32)
    mask = (dst[..., 3] > 0.35).astype(np.float32)
    dst[..., :3] = np.clip(dst[..., :3] + ((noise - 0.5) * amp)[..., None] * mask[..., None], 0.0, 1.0)


def fill_poly(dst: np.ndarray, points: list[tuple[float, float]], color: np.ndarray, opacity: float = 1.0) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    fill = tuple(int(round(c * 255)) for c in color) + (int(round(opacity * 255)),)
    draw.polygon([(float(x), float(y)) for x, y in points], fill=fill)
    over(dst, np.asarray(im, dtype=np.float32) / 255.0)


def glow(dst: np.ndarray, cx: float, cy: float, r: float, color: np.ndarray, opacity: float) -> None:
    xx, yy = grid()
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    a = np.exp(-0.5 * (d / max(r, 1.0)) ** 2) * opacity
    layer = blank()
    layer[..., :3] = color
    layer[..., 3] = a
    over(dst, layer)


def grain(seed: int, amp: float = 0.04) -> np.ndarray:
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


def bob(frame: int, amp: float = 5.0) -> float:
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


# --- venue ------------------------------------------------------------------

VENUES = {
    "disco": ("1a0c28", "3c1460", "2a1840", 7),
    "neon": ("06141c", "0a3040", "082028", 11),
    "bamboo": ("143024", "1e4834", "245038", 13),
    "rooftop": ("101830", "1c2848", "243050", 17),
    "candy": ("301028", "642050", "401830", 19),
    "moonlight": ("101428", "1c2848", "182038", 23),
    "confetti": ("2c1810", "583828", "3c2418", 29),
    "garden": ("183020", "2c4830", "204028", 31),
}


def paint_venue(kind: str, frame: int) -> np.ndarray:
    top_h, mid_h, bot_h, seed = VENUES[kind]
    xx, yy = grid()
    t = phase(frame)
    top, mid, bot = rgb(top_h), rgb(mid_h), rgb(bot_h)
    v = yy / (H - 1)
    sky = mix(top, mid, np.clip(v / 0.62, 0.0, 1.0)[..., None])
    floor = mix(mid, bot, np.clip((v - 0.62) / 0.38, 0.0, 1.0)[..., None])
    fill = np.where((v < 0.62)[..., None], sky, floor)
    arr = blank()
    arr[..., :3] = fill
    arr[..., 3] = 1.0
    arr[..., :3] = np.clip(arr[..., :3] + grain(seed, 0.012)[..., None], 0.0, 1.0)

    floor_y = 392.0
    rounded_rect(arr, 256, 452, 270, 62, shade(bot, 0.08), 0.95, radius=8)
    ellipse(arr, 256, floor_y, 240, 10, shade(bot, 0.25), 0.55)

    if kind == "disco":
        tile = 32
        check = (((xx // tile).astype(np.int32) + (yy // tile).astype(np.int32)) % 2 == 0) & (yy > floor_y)
        arr[check, :3] = mix(arr[check, :3], rgb("ff40c0")[None, :], 0.22)
        for i, color in enumerate((rgb("ff40c0"), rgb("40e0ff"), rgb("ffe040"))):
            ang = t + i * 2.094
            px, py = 256 + math.cos(ang) * 150, 150 + math.sin(ang * 1.2) * 40
            glow(arr, px, py, 55, color, 0.42)
            disc(arr, px, py, 10, color, 0.85)
        rounded_rect(arr, 256, 36, 80, 10, rgb("ffe060"), 0.7, radius=4)
    elif kind == "neon":
        for i in range(6):
            gy = 56 + i * 54
            ellipse(arr, 256, gy, 250, 3.5, rgb("20e0d0"), 0.45 + 0.12 * math.sin(t + i))
        rounded_rect(arr, 70, 160, 18, 70, rgb("ff40c0"), 0.8, radius=6)
        rounded_rect(arr, 442, 300, 18, 90, rgb("20e0d0"), 0.8, radius=6)
        glow(arr, 70, 160, 36, rgb("ff40c0"), 0.28)
        glow(arr, 442, 300, 40, rgb("20e0d0"), 0.28)
    elif kind == "bamboo":
        stem = rgb("3a7a48")
        joint = rgb("245830")
        leaf = rgb("7cc86a")
        for i, x in enumerate((58.0, 128.0, 392.0, 458.0)):
            sway = math.sin(t + i * 0.7) * 4
            outlined_ellipse(arr, x + sway, 250, 11, 210, stem, shade(stem, 0.35), width=2.4)
            for j in range(4):
                ellipse(arr, x + sway, 90.0 + j * 70, 14, 5, joint, 0.9)
            disc(arr, x + sway + 16, 78 + (i % 3) * 36, 16, leaf, 0.92)
            disc(arr, x + sway - 14, 110 + (i % 2) * 28, 13, shade(leaf, 0.12), 0.88)
    elif kind == "rooftop":
        outlined_disc(arr, 404, 78, 28, rgb("fff4c8"), rgb("e8d090"), width=2.4)
        glow(arr, 404, 78, 48, rgb("fff4c8"), 0.28 + 0.06 * math.sin(t))
        for bx, bw, bh in ((48, 36, 150), (96, 28, 210), (148, 40, 128), (356, 32, 170), (408, 44, 230), (468, 30, 140)):
            rounded_rect(arr, bx, 392 - bh / 2, bw / 2, bh / 2, rgb("1a2448"), 0.96, radius=4)
            rounded_rect(arr, bx, 392 - bh / 2 - 4, bw / 2 - 4, 8, rgb("ffe080"), 0.35 + 0.15 * math.sin(t + bx), radius=2)
    elif kind == "candy":
        for i, (px, py, r, c) in enumerate(
            ((90, 90, 34, "ff6ab8"), (430, 120, 28, "80e0ff"), (70, 300, 22, "ffe060"), (450, 280, 26, "c070ff"))
        ):
            outlined_disc(arr, px, py + math.sin(t + i) * 5, r, rgb(c), width=2.6)
        glow(arr, 256, 160, 90, rgb("ff90c8"), 0.16)
    elif kind == "moonlight":
        outlined_disc(arr, 400, 86, 34, rgb("e8f0ff"), rgb("c8d8f0"), width=2.4)
        disc(arr, 388, 78, 12, rgb("ffffff"), 0.35)
        glow(arr, 400, 86, 70, rgb("c8d8f0"), 0.22)
        for i in range(16):
            disc(arr, float((41 * i + 18) % W), float((19 * i + 30) % 210), 1.8, rgb("e8f0ff"), 0.8, soft=1.0)
    elif kind == "confetti":
        rounded_rect(arr, 256, 210, 248, 170, shade(mid, 0.12), 0.55, radius=6)
        rounded_rect(arr, 256, 392, 270, 18, shade(bot, 0.2), 0.9, radius=4)
        for i in range(8):
            rounded_rect(arr, 40.0 + i * 62, 392, 18, 3, rgb("d8b070") if i % 2 == 0 else rgb("c09050"), 0.55, radius=1)
        streamers = (rgb("ff5a8a"), rgb("ffe040"), rgb("40e0ff"), rgb("c070ff"))
        for i in range(8):
            sx = 40 + i * 62
            fill_poly(arr, [(sx - 8, 8), (sx + 8, 8), (sx + 3, 58), (sx - 3, 58)], streamers[i % 4])
            fill_poly(arr, [(sx - 10, 8), (sx + 10, 8), (sx + 10, 18), (sx - 10, 18)], LINE, 0.85)
        bits = streamers
        for i in range(28):
            px = (37 * i + int(math.sin(t + i) * 14)) % W
            py = (17 * i + frame * 10 + i * 5) % int(floor_y)
            rounded_rect(arr, float(px), float(py), 5, 3, bits[i % 4], 0.9, radius=1.5, soft=1.2)
    else:
        rounded_rect(arr, 256, 430, 260, 28, rgb("3a6840"), 0.9, radius=6)
        for i, (px, c) in enumerate(((70, "ff90b0"), (130, "ffe060"), (400, "ff90b0"), (460, "80e070"))):
            disc(arr, px, 400 + math.sin(t + i) * 3, 16, rgb(c), 0.95)
            disc(arr, px, 388 + math.sin(t + i) * 3, 8, lite(rgb(c), 0.2), 0.9)
            ellipse(arr, px, 418, 3, 14, rgb("2a5030"), 0.9)
    return arr


# --- glow -------------------------------------------------------------------

GLOWS = {
    "disco": "ff40c0",
    "laser": "40e0ff",
    "sparkle": "ffe060",
    "neon": "70ffb0",
    "champagne": "f0d090",
}


def paint_glow(kind: str, frame: int) -> np.ndarray:
    arr = blank()
    t = phase(frame)
    color = rgb(GLOWS[kind])
    cx, cy = HEAD
    pulse = 0.18 + 0.06 * math.sin(t)
    glow(arr, cx, cy + 24, 150 + 10 * math.sin(t), color, pulse)
    if kind == "disco":
        for i in range(3):
            ang = t + i * 2.094
            disc(arr, cx + math.cos(ang) * 90, cy + math.sin(ang) * 50, 8, color, 0.55)
    elif kind == "laser":
        ellipse(arr, cx + math.cos(t) * 70, cy - 10, 150, 6, color, 0.35)
        ellipse(arr, cx - math.sin(t) * 50, cy + 30, 6, 120, color, 0.28)
    elif kind == "sparkle":
        for i in range(10):
            ang = t + i * 0.63
            disc(arr, cx + math.cos(ang) * 100, cy + math.sin(ang) * 70, 3.5, color, 0.7, soft=1.4)
    elif kind == "neon":
        ellipse(arr, cx, cy + 8, 130, 150, color, 0.0)
        ellipse(arr, cx, cy + 8, 118, 138, color, 0.22)
    return arr


# --- panda ------------------------------------------------------------------

PANDAS = {
    "classic": {
        "fur": "f6f1e8",
        "ink": "1a1a22",
        "belly": "fffaf4",
        "blush": "f0a898",
        "nose": "141418",
        "scale": 1.0,
        "seed": 11,
    },
    "chubby": {
        "fur": "f8f0e4",
        "ink": "201c24",
        "belly": "ffe8d4",
        "blush": "ee9080",
        "nose": "1c1818",
        "scale": 1.1,
        "seed": 17,
    },
    "cub": {
        "fur": "fff8ee",
        "ink": "242028",
        "belly": "fffaf4",
        "blush": "f0b8a8",
        "nose": "201818",
        "scale": 0.88,
        "seed": 23,
    },
    "dancer": {
        "fur": "f4ecf4",
        "ink": "281828",
        "belly": "fce8f4",
        "blush": "e870a0",
        "nose": "1a1020",
        "scale": 0.97,
        "seed": 29,
    },
    "tuxedo": {
        "fur": "faf8f2",
        "ink": "0c0c12",
        "belly": "ffffff",
        "blush": "e8a090",
        "nose": "08080c",
        "scale": 1.02,
        "seed": 31,
    },
    "peach": {
        "fur": "f8e6d4",
        "ink": "4a2c22",
        "belly": "ffdcc8",
        "blush": "ee8070",
        "nose": "301818",
        "scale": 1.0,
        "seed": 37,
    },
}


def paint_panda(kind: str, frame: int) -> np.ndarray:
    palette = PANDAS[kind]
    fur, ink, belly, blush, nose = (rgb(palette[k]) for k in ("fur", "ink", "belly", "blush", "nose"))
    scale = float(palette["scale"])
    arr = blank()
    cx, cy = HEAD[0], HEAD[1] + bob(frame)
    sway = math.sin(phase(frame)) * 3.5
    s = scale

    # legs
    outlined_ellipse(arr, cx - 42 * s, cy + 198 * s, 28 * s, 36 * s, ink, width=2.6)
    outlined_ellipse(arr, cx + 42 * s, cy + 198 * s, 28 * s, 36 * s, ink, width=2.6)
    ellipse(arr, cx - 42 * s, cy + 220 * s, 22 * s, 10 * s, shade(ink, 0.1), 0.95)
    ellipse(arr, cx + 42 * s, cy + 220 * s, 22 * s, 10 * s, shade(ink, 0.1), 0.95)

    # torso: black sides, white belly
    outlined_ellipse(arr, cx, cy + 132 * s, 108 * s, 92 * s, ink, width=3.0)
    outlined_ellipse(arr, cx, cy + 138 * s, 64 * s, 72 * s, belly, width=2.2)
    if kind == "tuxedo":
        ellipse(arr, cx, cy + 132 * s, 22 * s, 64 * s, fur, 0.98)
        disc(arr, cx, cy + 96 * s, 6 * s, rgb("ffe060"), 0.9)

    # arms + paws
    arm_y = cy + 118 * s
    outlined_ellipse(arr, cx - 102 * s + sway * 0.35, arm_y, 32 * s, 58 * s, ink, width=2.6)
    outlined_ellipse(arr, cx + 102 * s + sway * 0.35, arm_y, 32 * s, 58 * s, ink, width=2.6)
    outlined_disc(arr, cx - 114 * s + sway * 0.35, arm_y + 52 * s, 20 * s, ink, width=2.4)
    outlined_disc(arr, cx + 114 * s + sway * 0.35, arm_y + 52 * s, 20 * s, ink, width=2.4)
    disc(arr, cx - 108 * s + sway * 0.35, arm_y + 48 * s, 5 * s, lite(ink, 0.18), 0.35)
    disc(arr, cx + 96 * s + sway * 0.35, arm_y + 48 * s, 5 * s, lite(ink, 0.18), 0.35)

    # ears (behind head rim)
    ear_r = 32 * (1.16 if kind == "cub" else 1.0) * s
    outlined_disc(arr, cx - 78 * s, cy - 92 * s, ear_r, ink, width=2.8)
    outlined_disc(arr, cx + 78 * s, cy - 92 * s, ear_r, ink, width=2.8)
    disc(arr, cx - 78 * s, cy - 88 * s, ear_r * 0.42, blush, 0.7)
    disc(arr, cx + 78 * s, cy - 88 * s, ear_r * 0.42, blush, 0.7)

    # head
    head_r = 108 * s
    outlined_disc(arr, cx, cy - 4 * s, head_r, fur, width=3.2)

    # classic panda patches
    outlined_ellipse(arr, cx - 40 * s, cy - 8 * s, 32 * s, 38 * s, ink, width=1.8)
    outlined_ellipse(arr, cx + 40 * s, cy - 8 * s, 32 * s, 38 * s, ink, width=1.8)

    # snout
    outlined_ellipse(arr, cx, cy + 36 * s, 44 * s, 30 * s, belly, width=2.2)
    disc(arr, cx - 46 * s, cy + 24 * s, 12 * s, blush, 0.42)
    disc(arr, cx + 46 * s, cy + 24 * s, 12 * s, blush, 0.42)
    outlined_ellipse(arr, cx, cy + 28 * s, 13 * s, 9 * s, nose, width=1.6)
    disc(arr, cx - 4, cy + 24 * s, 3.4, rgb("ffffff"), 0.7, soft=1.4)

    fur_speckle(arr, int(palette["seed"]), amp=0.045)
    return arr


# --- mood -------------------------------------------------------------------

def paint_mood(kind: str, frame: int) -> np.ndarray:
    arr = blank()
    cx, cy = HEAD[0], HEAD[1] + bob(frame)
    t = phase(frame)
    closed = blink_amount(frame)
    white = rgb("ffffff")
    pupil = rgb("141418")
    shine = rgb("fff8e8")
    ink = rgb("1a1a22")
    pink = rgb("ff5a88")
    gold = rgb("ffe060")
    lid = rgb("f6f1e8")

    def eye(ex: float, ey: float, shut: float, heart: bool = False, spark: bool = False) -> None:
        if shut >= 0.9:
            ellipse(arr, ex, ey + 2, 18, 4, ink, 0.95, soft=1.6)
            ellipse(arr, ex, ey - 1, 16, 3, shade(ink, 0.2), 0.55, soft=1.4)
            return
        outlined_disc(arr, ex, ey, 16, white, ink, width=2.2)
        if heart:
            disc(arr, ex, ey + 2, 9, pink, 0.98, soft=1.6)
            disc(arr, ex - 5, ey - 2, 5.5, pink, 0.95, soft=1.4)
            disc(arr, ex + 5, ey - 2, 5.5, pink, 0.95, soft=1.4)
            disc(arr, ex - 3, ey - 4, 2.2, shine, 0.8, soft=1.0)
        elif spark:
            disc(arr, ex, ey + 1, 8.5, gold, 0.98, soft=1.6)
            disc(arr, ex, ey + 1, 4, pupil, 0.95, soft=1.2)
            disc(arr, ex - 3.5, ey - 3, 2.6, shine, 0.9, soft=1.0)
        else:
            disc(arr, ex, ey + 1.5, 9, pupil, 0.98, soft=1.5)
            disc(arr, ex - 3.5, ey - 3.2, 3.4, shine, 0.95, soft=1.0)
            disc(arr, ex + 3, ey + 4, 1.6, shine, 0.55, soft=0.8)
        if shut > 0.35:
            ellipse(arr, ex, ey - 10, 17, 9 * shut, lid, 0.96, soft=1.8)

    if kind == "shades":
        glass = rgb("12161e")
        rim = rgb("2a2e38")
        rounded_rect(arr, cx - 40, cy - 2, 26, 14, glass, 0.96, radius=8)
        rounded_rect(arr, cx + 40, cy - 2, 26, 14, glass, 0.96, radius=8)
        rounded_rect(arr, cx, cy - 4, 16, 3.5, rim, 0.95, radius=2)
        ellipse(arr, cx - 48, cy - 6, 10, 4, rgb("40e0ff"), 0.55 + 0.15 * math.sin(t), soft=1.8)
        ellipse(arr, cx + 32, cy - 6, 8, 3, rgb("ff40c0"), 0.4, soft=1.6)
    elif kind == "wink":
        eye(cx - 40, cy - 8, 0.0)
        eye(cx + 40, cy - 8, 1.0)
    elif kind == "heart":
        eye(cx - 40, cy - 8, closed, heart=True)
        eye(cx + 40, cy - 8, closed, heart=True)
    elif kind == "spark":
        eye(cx - 40, cy - 8, closed, spark=True)
        eye(cx + 40, cy - 8, closed, spark=True)
    elif kind == "sleepy":
        eye(cx - 40, cy - 6, 0.55)
        eye(cx + 40, cy - 6, 0.55)
    else:
        eye(cx - 40, cy - 8, closed)
        eye(cx + 40, cy - 8, closed)

    if kind == "sleepy":
        ellipse(arr, cx, cy + 50, 11, 3.2, ink, 0.7, soft=1.5)
    else:
        ellipse(arr, cx, cy + 52, 18, 5.5 + math.sin(t), ink, 0.0, soft=1.6)
        ellipse(arr, cx, cy + 48, 16, 4.2, ink, 0.7, soft=1.6)
        ellipse(arr, cx, cy + 46, 14, 2.4, rgb("f6f1e8"), 0.85, soft=1.4)
    return arr


# --- fit --------------------------------------------------------------------

def paint_fit(kind: str, frame: int) -> np.ndarray:
    arr = blank()
    cx, cy = HEAD[0], HEAD[1] + bob(frame)
    t = phase(frame)
    sway = math.sin(t) * 3
    if kind == "cone":
        hat = rgb("ff4a7a")
        trim = rgb("ffe060")
        tip_x = cx + sway * 0.15
        tip_y = cy - 218
        left, right, base_y = cx - 52, cx + 52, cy - 106
        fill_poly(arr, [(tip_x, tip_y - 4), (left - 4, base_y + 2), (right + 4, base_y + 2)], LINE)
        fill_poly(arr, [(tip_x, tip_y), (left, base_y), (right, base_y)], hat)
        for frac, band in ((0.38, trim), (0.68, trim)):
            y0 = tip_y + (base_y - tip_y) * frac
            y1 = y0 + 10
            span0 = (y0 - tip_y) / (base_y - tip_y)
            span1 = (y1 - tip_y) / (base_y - tip_y)
            w0, w1 = 52 * span0, 52 * span1
            fill_poly(
                arr,
                [
                    (tip_x - w0, y0),
                    (tip_x + w0, y0),
                    (tip_x + w1, y1),
                    (tip_x - w1, y1),
                ],
                band,
            )
        outlined_ellipse(arr, cx, cy - 108, 54, 11, hat, width=2.2)
        outlined_disc(arr, tip_x, tip_y + 2, 10, trim, width=2.0)
    elif kind == "bow":
        silk = rgb("d42848")
        outlined_ellipse(arr, cx - 26, cy + 96, 20, 13, silk, width=2.0)
        outlined_ellipse(arr, cx + 26, cy + 96, 20, 13, silk, width=2.0)
        outlined_disc(arr, cx, cy + 96, 8, silk, width=2.0)
        disc(arr, cx, cy + 94, 3.2, rgb("ffe060"), 0.85, soft=1.2)
    elif kind == "phones":
        band = rgb("2a2e36")
        cup = rgb("ff40c0")
        outlined_ellipse(arr, cx, cy - 92, 96, 18, band, width=2.4)
        outlined_ellipse(arr, cx - 104, cy + 6, 20, 28, cup, width=2.4)
        outlined_ellipse(arr, cx + 104, cy + 6, 20, 28, cup, width=2.4)
        ellipse(arr, cx - 104, cy + 6, 10, 14, rgb("1a1a22"), 0.9)
        ellipse(arr, cx + 104, cy + 6, 10, 14, rgb("1a1a22"), 0.9)
        glow(arr, cx - 104, cy + 6, 12, rgb("40e0ff"), 0.28 + 0.1 * math.sin(t))
    elif kind == "lei":
        petals = (rgb("ff6a9a"), rgb("ffe060"), rgb("70e0c0"), rgb("ff9040"))
        for i, ang in enumerate(np.linspace(-2.5, 2.5, 13)):
            px = cx + math.sin(ang) * 88
            py = cy + 92 + math.cos(ang) * 16
            outlined_disc(arr, px, py, 11, petals[i % 4], width=1.8)
            disc(arr, px, py, 3.6, rgb("fff4d0"), 0.8, soft=1.2)
    elif kind == "crown":
        gold = rgb("ffe060")
        glow(arr, cx, cy - 124, 28, gold, 0.16 + 0.05 * math.sin(t))
        outlined_ellipse(arr, cx, cy - 108, 54, 11, gold, width=2.2)
        for ox, oy in ((-28, -128), (0, -140), (28, -128)):
            outlined_disc(arr, cx + ox, cy + oy, 8 if ox else 10, gold, width=1.8)
        disc(arr, cx, cy - 140, 3.5, rgb("fff8d0"), 0.85, soft=1.2)
    elif kind == "afro":
        hair = rgb("241018")
        puffs = (
            (-70, -70, 28),
            (70, -70, 28),
            (0, -122, 30),
            (-42, -108, 24),
            (42, -108, 24),
            (-88, -36, 22),
            (88, -36, 22),
            (-28, -86, 20),
            (28, -86, 20),
        )
        for ox, oy, r in puffs:
            outlined_disc(arr, cx + ox, cy + oy, r, hair, width=2.6, cel=False)
        disc(arr, cx - 18, cy - 112, 5, lite(hair, 0.22), 0.35, soft=2.0)
    return arr


# --- extra ------------------------------------------------------------------

def paint_extra(kind: str, frame: int) -> np.ndarray:
    arr = blank()
    cx, cy = HEAD[0], HEAD[1] + bob(frame, amp=3.0)
    t = phase(frame)
    if kind == "confetti":
        bits = (rgb("ff5a8a"), rgb("ffe040"), rgb("40e0ff"), rgb("c070ff"), rgb("70ffb0"))
        for i in range(18):
            px = (cx - 170 + (i * 24 + math.sin(t + i) * 16)) % (W - 24) + 12
            py = (36 + i * 17 + frame * 12) % (H - 36)
            rounded_rect(arr, float(px), float(py), 6, 3.2, bits[i % 5], 0.92, radius=1.4, soft=1.1)
    elif kind == "balloon":
        color = rgb("ff4a7a")
        bx = cx + 148 + math.sin(t) * 7
        by = cy - 96 + math.cos(t) * 5
        outlined_ellipse(arr, bx, by, 26, 34, color, width=2.4)
        disc(arr, bx - 8, by - 12, 7, rgb("ffffff"), 0.45, soft=2.5)
        ellipse(arr, bx, by + 38, 4, 7, color, 0.9, soft=1.4)
        ellipse(arr, bx - 3, by + 72, 2.2, 30, rgb("f4efe6"), 0.7, soft=1.3)
    elif kind == "cocktail":
        glass = rgb("e8f4f8")
        drink = rgb("ff6a9a")
        gx, gy = cx + 138, cy + 72 + math.sin(t) * 2.5
        outlined_ellipse(arr, gx, gy, 20, 14, drink, width=2.0)
        ellipse(arr, gx, gy - 4, 20, 6, glass, 0.45, soft=1.6)
        rounded_rect(arr, gx, gy + 28, 2.4, 22, glass, 0.8, radius=1.5, soft=1.2)
        outlined_ellipse(arr, gx, gy + 50, 12, 3.5, glass, width=1.6)
        outlined_disc(arr, gx + 10, gy - 18, 5, rgb("ffe060"), width=1.4)
    elif kind == "sparkler":
        gold = rgb("ffe060")
        sx, sy = cx - 146, cy + 42
        rounded_rect(arr, sx, sy + 28, 2.4, 30, rgb("c8a070"), 0.92, radius=1.4, soft=1.2)
        glow(arr, sx, sy - 8, 22, gold, 0.4 + 0.12 * math.sin(t * 2))
        for i in range(12):
            ang = t * 2 + i * 0.52
            disc(arr, sx + math.cos(ang) * 16, sy - 8 + math.sin(ang) * 16, 2.2, gold, 0.85, soft=1.1)
    elif kind == "boombox":
        box = rgb("2a2432")
        bx, by = cx + 148, cy + 88
        rounded_rect(arr, bx, by, 42, 22, box, 0.96, radius=8)
        rounded_rect(arr, bx, by, 44, 24, LINE, 0.0, radius=8)
        outlined_disc(arr, bx - 18, by, 10, rgb("1a1a22"), width=2.0)
        outlined_disc(arr, bx + 18, by, 10, rgb("1a1a22"), width=2.0)
        glow(arr, bx - 18, by, 7, rgb("ff40c0"), 0.32 + 0.12 * math.sin(t * 2))
        glow(arr, bx + 18, by, 7, rgb("40e0ff"), 0.28 + 0.12 * math.cos(t * 2))
        rounded_rect(arr, bx, by - 10, 10, 3, rgb("ffe060"), 0.7, radius=1.5, soft=1.1)
    return arr


# --- catalog ----------------------------------------------------------------

TRAIT_SPEC = {
    "venue": [
        ("disco", "Disco Night", 16),
        ("neon", "Neon Club", 14),
        ("bamboo", "Bamboo Lounge", 14),
        ("rooftop", "Rooftop Glow", 12),
        ("candy", "Candy Rave", 12),
        ("moonlight", "Moonlight", 12),
        ("confetti", "Confetti Hall", 10),
        ("garden", "Garden Party", 10),
    ],
    "glow": [
        ("none", "No glow", 22),
        ("disco", "Disco Pulse", 16),
        ("laser", "Laser Sweep", 14),
        ("sparkle", "Sparkle Burst", 14),
        ("neon", "Neon Ring", 12),
        ("champagne", "Champagne Haze", 12),
    ],
    "panda": [
        ("classic", "Classic", 20),
        ("chubby", "Chubby", 18),
        ("cub", "Cub", 16),
        ("dancer", "Dancer", 16),
        ("tuxedo", "Tuxedo", 16),
        ("peach", "Peach", 14),
    ],
    "mood": [
        ("blink", "Blink", 22),
        ("wink", "Wink", 18),
        ("shades", "Shades", 16),
        ("heart", "Heart", 16),
        ("sleepy", "Sleepy", 14),
        ("spark", "Spark", 14),
    ],
    "fit": [
        ("none", "Bare head", 22),
        ("cone", "Party Hat", 16),
        ("bow", "Bowtie", 14),
        ("phones", "Headphones", 14),
        ("lei", "Lei", 12),
        ("crown", "Tiny Crown", 12),
        ("afro", "Disco Afro", 10),
    ],
    "extra": [
        ("none", "None", 22),
        ("confetti", "Confetti", 16),
        ("balloon", "Balloon", 14),
        ("cocktail", "Cocktail", 14),
        ("sparkler", "Sparkler", 12),
        ("boombox", "Boombox", 10),
    ],
}

PAINTERS = {
    "venue": {k: (lambda kind: (lambda frame, k=kind: paint_venue(k, frame)))(k) for k in VENUES},
    "glow": {k: (lambda kind: (lambda frame, k=kind: paint_glow(k, frame)))(k) for k in GLOWS},
    "panda": {k: (lambda kind: (lambda frame, k=kind: paint_panda(k, frame)))(k) for k in PANDAS},
    "mood": {k: (lambda kind: (lambda frame, k=kind: paint_mood(k, frame)))(k) for k in ("blink", "wink", "shades", "heart", "sleepy", "spark")},
    "fit": {k: (lambda kind: (lambda frame, k=kind: paint_fit(k, frame)))(k) for k in ("cone", "bow", "phones", "lei", "crown", "afro")},
    "extra": {k: (lambda kind: (lambda frame, k=kind: paint_extra(k, frame)))(k) for k in ("confetti", "balloon", "cocktail", "sparkler", "boombox")},
}

STACK = ("venue", "glow", "panda", "mood", "fit", "extra")

SIGNATURES = [
    {"venue": "disco", "glow": "disco", "panda": "classic", "mood": "blink", "fit": "cone", "extra": "confetti"},
    {"venue": "neon", "glow": "laser", "panda": "dancer", "mood": "shades", "fit": "phones", "extra": "boombox"},
    {"venue": "bamboo", "glow": "neon", "panda": "chubby", "mood": "heart", "fit": "lei", "extra": "balloon"},
    {"venue": "rooftop", "glow": "none", "panda": "tuxedo", "mood": "wink", "fit": "bow", "extra": "cocktail"},
    {"venue": "candy", "glow": "sparkle", "panda": "cub", "mood": "spark", "fit": "crown", "extra": "none"},
    {"venue": "moonlight", "glow": "champagne", "panda": "peach", "mood": "sleepy", "fit": "none", "extra": "sparkler"},
    {"venue": "confetti", "glow": "disco", "panda": "classic", "mood": "shades", "fit": "afro", "extra": "confetti"},
    {"venue": "garden", "glow": "sparkle", "panda": "chubby", "mood": "blink", "fit": "cone", "extra": "balloon"},
    {"venue": "disco", "glow": "laser", "panda": "dancer", "mood": "heart", "fit": "crown", "extra": "sparkler"},
    {"venue": "neon", "glow": "neon", "panda": "cub", "mood": "wink", "fit": "phones", "extra": "none"},
    {"venue": "bamboo", "glow": "none", "panda": "peach", "mood": "sleepy", "fit": "lei", "extra": "cocktail"},
    {"venue": "rooftop", "glow": "champagne", "panda": "tuxedo", "mood": "blink", "fit": "bow", "extra": "boombox"},
    {"venue": "candy", "glow": "disco", "panda": "classic", "mood": "spark", "fit": "afro", "extra": "confetti"},
    {"venue": "moonlight", "glow": "laser", "panda": "dancer", "mood": "shades", "fit": "none", "extra": "balloon"},
    {"venue": "confetti", "glow": "sparkle", "panda": "chubby", "mood": "heart", "fit": "cone", "extra": "none"},
    {"venue": "garden", "glow": "champagne", "panda": "cub", "mood": "blink", "fit": "crown", "extra": "sparkler"},
]

TRAIT_LABELS = (
    ("venue", "Venue"),
    ("glow", "Glow"),
    ("panda", "Panda"),
    ("mood", "Mood"),
    ("fit", "Fit"),
    ("extra", "Extra"),
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
        "name": "Party Pandas",
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
                "name": f"Party Panda #{index}",
                "image": f"/party-pandas-preview/{index}.gif",
                "attributes": [
                    {"trait_type": label, "value": name_of(key, selection[key])}
                    for key, label in TRAIT_LABELS
                ],
            }
        )
    (META_DIR / "party-pandas-samples.json").write_text(json.dumps(samples, indent=2) + "\n", encoding="utf-8")


COLLECTION_DESCRIPTION = (
    "Party Pandas is a 4,444-piece collection of looping party-panda PFP GIFs on Base. "
    "Each panda is stacked from six layers — venue, glow, panda, mood, fit, and extra — "
    "then flattened onto one 12-frame GIF. Classic black-and-white markings, crisp outlines, fluffy fur. "
    "Clubs pulse. Hats bounce. Confetti never lands."
)

COLLECTION_STORY = (
    "Party Pandas never sit still.\n\n"
    "A 4,444-piece collection of looping party-panda PFP GIFs on Base. "
    "Each panda is stacked from six layers — venue, glow, panda, mood, fit, and extra — "
    "then flattened onto one 12-frame GIF. Clubs pulse. Eyes blink. Hats bounce. Confetti never lands.\n\n"
    "Cartoon pandas with classic black-and-white markings, crisp outlines, and fluffy fur. "
    "Soft edges. One shared clock.\n\n"
    "Minting on Base (chain ID 8453). Gas is ETH."
)


def panoramic_wash(width: int, height: int, frame: int = 0) -> Image.Image:
    left = np.asarray(to_image(paint_venue("disco", frame)).resize((width, height), Image.Resampling.LANCZOS), dtype=np.float32)
    mid = np.asarray(to_image(paint_venue("candy", frame)).resize((width, height), Image.Resampling.LANCZOS), dtype=np.float32)
    right = np.asarray(to_image(paint_venue("neon", frame)).resize((width, height), Image.Resampling.LANCZOS), dtype=np.float32)
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
    ImageDraw.Draw(shadow).rounded_rectangle((8, 14, size + 8, size + 18), radius=radius, fill=(16, 6, 18, 90))
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
    (META_DIR / "party-pandas-description.txt").write_text(COLLECTION_STORY + "\n", encoding="utf-8")
    (META_DIR / "party-pandas.json").write_text(
        json.dumps(
            {
                "name": "Party Pandas",
                "symbol": "PAND",
                "description": COLLECTION_DESCRIPTION,
                "image": "/brand/collection-party-pandas.gif",
                "featured_image": "/brand/featured-party-pandas.jpg",
                "banner_image": "/brand/banner-party-pandas.png",
                "opensea_banner_image": "/brand/banner-party-pandas-opensea.jpg",
                "external_link": "/party-pandas",
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
    ImageDraw.Draw(ring).ellipse((10, 10, SIZE - 10, SIZE - 10), outline=(255, 64, 192, 220), width=10)
    logo = Image.alpha_composite(logo, ring)
    save_image(logo.resize((512, 512), Image.Resampling.LANCZOS), BRAND_DIR / "logo-party-pandas.png")
    save_apng([frame.resize((512, 512), Image.Resampling.LANCZOS) for frame in logo_frames], BRAND_DIR / "logo-party-pandas-loop.png")

    site_banner = lineup_banner(1500, 560, portraits[:5])
    save_image(site_banner.convert("RGB"), BRAND_DIR / "banner-party-pandas.png", quality=94)

    opensea_banner = lineup_banner(2800, 700, portraits)
    save_image(opensea_banner.convert("RGB"), BRAND_DIR / "banner-party-pandas-opensea.jpg", quality=90)

    featured = panoramic_wash(1200, 800, frame=8)
    place_portrait(featured, portraits[0], 90, 110, 560, radius=64)
    place_portrait(featured, portraits[2], 540, 130, 560, radius=64)
    save_image(featured.convert("RGB"), BRAND_DIR / "featured-party-pandas.jpg", quality=90)

    gif_frames = [frame.resize((1000, 1000), Image.Resampling.LANCZOS) for frame in logo_frames]
    save_loop_gif(gif_frames, BRAND_DIR / "collection-party-pandas.gif", DURATION_MS)
    write_collection_meta()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--brand-only", action="store_true", help="Rebuild logo, banners, and listing copy")
    args = parser.parse_args()
    if args.brand_only:
        print("Writing Party Pandas brand kit…")
        build_brand()
        print("Done.")
        return
    print("Building Party Pandas trait loops…")
    build_traits()
    print("Compositing sample GIF tokens…")
    build_samples()
    print("Writing brand…")
    build_brand()
    print("Done.")


if __name__ == "__main__":
    main()
