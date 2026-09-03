#!/usr/bin/env python3
"""Paint BirbNation — looping round-borb robin PFP layers for an OpenSea Drop on Robinhood Chain.

Every trait is a 12-frame APNG on a shared 512 canvas and 90ms clock.
Plumage, mug, and accent share one blink clock. Field stays still except a faint ground wash.

Look: painted 3D illustration — BAYC form-light with Doodles clay volume.
One fat sphere. Warm key, cool fill, soft rim. Canvas grain. Thick drawn outline.
Chocolate cap, burnt-orange chest, cream belly, jagged feather seams.
Solid glossy black eyes. Cream brow tufts. Tiny yellow beak. A pink blep.
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

TRAIT_DIR = ROOT / "public" / "birbs-traits"
PREVIEW_DIR = ROOT / "public" / "birbs-preview"
BRAND_DIR = ROOT / "public" / "brand"
META_DIR = ROOT / "public" / "metadata"

SIZE = 512
FRAMES = 12
DURATION_MS = 90
H, W = SIZE, SIZE
YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)

# Sitting borb — one sphere, planted, lots of margin for accents.
CX, CY = 256.0, 286.0
R = 166.0
LINE_W = 9.2
SOFT = 1.35

KEY = np.array([-0.44, -0.56, 0.70], dtype=np.float32)
KEY /= float(np.linalg.norm(KEY))
FILL = np.array([0.60, 0.16, 0.42], dtype=np.float32)
FILL /= float(np.linalg.norm(FILL))
RIM = np.array([0.86, 0.14, 0.20], dtype=np.float32)
RIM /= float(np.linalg.norm(RIM))
VIEW = np.array([0.02, 0.06, 0.998], dtype=np.float32)
VIEW /= float(np.linalg.norm(VIEW))
HALF = KEY + VIEW
HALF /= float(np.linalg.norm(HALF))


def clamp01(x: np.ndarray | float) -> np.ndarray | float:
    return np.clip(x, 0.0, 1.0)


def smoothstep(edge0: float, edge1: float, x: np.ndarray) -> np.ndarray:
    t = clamp01((x - edge0) / (edge1 - edge0))
    return t * t * (3.0 - 2.0 * t)


def rgb(hex_color: str) -> np.ndarray:
    value = hex_color.lstrip("#")
    return np.array([int(value[i : i + 2], 16) / 255.0 for i in (0, 2, 4)], dtype=np.float32)


LINE = rgb("2a1c12")


def mix(a: np.ndarray | float, b: np.ndarray | float, t: float | np.ndarray) -> np.ndarray:
    a = np.asarray(a, dtype=np.float32)
    b = np.asarray(b, dtype=np.float32)
    t = np.asarray(t, dtype=np.float32)
    if t.ndim == 2 and a.ndim in (1, 3):
        t = t[..., None]
    return a * (1.0 - t) + b * t


def blank() -> np.ndarray:
    return np.zeros((H, W, 4), dtype=np.float32)


def grid() -> tuple[np.ndarray, np.ndarray]:
    return XX, YY


_GRAIN: dict[tuple[int, int], np.ndarray] = {}


def grain(seed: int, amp: float = 0.04) -> np.ndarray:
    key = (seed, int(amp * 1000))
    cached = _GRAIN.get(key)
    if cached is not None:
        return cached
    rng = np.random.default_rng(seed)
    small = (rng.random((SIZE // 11, SIZE // 16)) * 2 - 1).astype(np.float32)
    im = Image.fromarray(((small + 1) * 127.5).astype(np.uint8), "L")
    big = np.asarray(im.resize((W, H), Image.Resampling.BICUBIC), dtype=np.float32) / 127.5 - 1.0
    out = big * amp
    _GRAIN[key] = out
    return out


def ellipsoid(cx: float, cy: float, rx: float, ry: float, soft: float = 2.2) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    nx = (XX - cx) / max(rx, 1.0)
    ny = (YY - cy) / max(ry, 1.0)
    r2 = nx * nx + ny * ny
    nz = np.sqrt(np.maximum(0.0, 1.0 - r2))
    length = np.maximum(np.sqrt(nx * nx + ny * ny + nz * nz), 1e-6)
    rad = np.sqrt(r2)
    edge = soft / max(min(rx, ry), 1.0)
    alpha = smoothstep(1.0 + edge, 1.0 - edge * 0.32, rad)
    return nx / length, ny / length, nz / length, alpha


def bump_normals(
    nx: np.ndarray, ny: np.ndarray, nz: np.ndarray, seed: int, amount: float = 0.08
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    nx = nx + grain(seed, amount)
    ny = ny + grain(seed + 19, amount)
    length = np.maximum(np.sqrt(nx * nx + ny * ny + nz * nz), 1e-6)
    return nx / length, ny / length, nz / length


def shade_paint(
    albedo: np.ndarray,
    nx: np.ndarray,
    ny: np.ndarray,
    nz: np.ndarray,
    *,
    ambient: float = 0.20,
    wrap: float = 0.16,
    spec: float = 0.22,
    shininess: float = 18.0,
    sss: float = 0.26,
) -> np.ndarray:
    albedo = np.asarray(albedo, dtype=np.float32)
    if albedo.ndim == 1:
        albedo = np.broadcast_to(albedo, (H, W, 3)).copy()
    ndotk = nx * KEY[0] + ny * KEY[1] + nz * KEY[2]
    wrap_l = clamp01((ndotk + wrap) / (1.0 + wrap))
    ndotf = clamp01(nx * FILL[0] + ny * FILL[1] + nz * FILL[2])
    ndotr = clamp01(nx * RIM[0] + ny * RIM[1] + nz * RIM[2])
    ndotv = clamp01(nx * VIEW[0] + ny * VIEW[1] + nz * VIEW[2])
    ndoth = clamp01(nx * HALF[0] + ny * HALF[1] + nz * HALF[2])
    highlight = np.power(ndoth, shininess)
    soft_hl = np.power(ndoth, max(shininess * 0.35, 6.0))
    fresnel = np.power(np.clip(1.0 - ndotv, 0.0, 1.0), 2.0)
    ao = clamp01(0.40 + 0.60 * nz - 0.16 * ny)
    sss_term = clamp01(-ndotk) * fresnel * sss
    lit = albedo * (ambient * ao)[..., None]
    lit = lit + albedo * wrap_l[..., None] * rgb("fff4dc") * 1.18
    lit = lit + albedo * ndotf[..., None] * (rgb("6a78a8") * 0.48)
    lit = lit + highlight[..., None] * rgb("fffaf2") * spec
    lit = lit + soft_hl[..., None] * mix(albedo, rgb("ffffff"), 0.55) * 0.18
    lit = lit + (fresnel * ndotr)[..., None] * (rgb("ffe6c4") * 0.55)
    lit = lit + sss_term[..., None] * mix(albedo, rgb("ffb090"), 0.35)
    canvas = 1.0 + grain(41, 0.055) + grain(73, 0.022)
    return np.clip(lit * canvas[..., None], 0.0, 1.0)


def blit_volume(dst: np.ndarray, albedo: np.ndarray, nx: np.ndarray, ny: np.ndarray, nz: np.ndarray, alpha: np.ndarray, **kwargs) -> None:
    layer = blank()
    layer[..., :3] = shade_paint(albedo, nx, ny, nz, **kwargs)
    layer[..., 3] = np.clip(alpha, 0.0, 1.0)
    over(dst, layer)


def blit_soft(dst: np.ndarray, color: np.ndarray, alpha: np.ndarray) -> None:
    layer = blank()
    layer[..., :3] = color
    layer[..., 3] = np.clip(alpha, 0.0, 1.0)
    over(dst, layer)


def outline_disk(dst: np.ndarray, cx: float, cy: float, rx: float, ry: float, width: float = 7.4, alpha: float = 0.94) -> None:
    _nx, _ny, _nz, outer = ellipsoid(cx, cy, rx + width, ry + width, soft=1.8)
    blit_soft(dst, LINE, outer * alpha)


def volume_ball(
    dst: np.ndarray,
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    albedo: np.ndarray,
    *,
    outline: bool = True,
    width: float = 5.4,
    spec: float = 0.16,
    shininess: float = 16.0,
    sss: float = 0.18,
    bump: int | None = 11,
) -> None:
    if outline:
        outline_disk(dst, cx, cy, rx, ry, width=width)
    nx, ny, nz, a = ellipsoid(cx, cy, rx, ry, soft=1.4)
    if bump is not None:
        nx, ny, nz = bump_normals(nx, ny, nz, bump, 0.07)
    blit_volume(dst, albedo, nx, ny, nz, a, spec=spec, shininess=shininess, sss=sss)


def over(dst: np.ndarray, src: np.ndarray) -> None:
    sa = src[..., 3:4]
    da = dst[..., 3:4]
    out_a = sa + da * (1.0 - sa)
    rgb_out = src[..., :3] * sa + dst[..., :3] * da * (1.0 - sa)
    dst[..., :3] = np.divide(rgb_out, out_a, out=np.zeros_like(rgb_out), where=out_a > 1e-6)
    dst[..., 3:4] = out_a


def shade(color: np.ndarray, t: float = 0.22) -> np.ndarray:
    return mix(color, rgb("2a1c14"), t)


def lite(color: np.ndarray, t: float = 0.32) -> np.ndarray:
    return mix(color, rgb("ffffff"), t)


def disc(dst: np.ndarray, cx: float, cy: float, r: float, color: np.ndarray, opacity: float = 1.0, soft: float = SOFT) -> None:
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


def outlined_disc(
    dst: np.ndarray,
    cx: float,
    cy: float,
    r: float,
    color: np.ndarray,
    width: float = LINE_W,
    opacity: float = 1.0,
    cel: bool = True,
) -> None:
    disc(dst, cx, cy, r + width, LINE, opacity)
    disc(dst, cx, cy, r, color, opacity)
    if cel:
        disc(dst, cx - r * 0.18, cy - r * 0.26, r * 0.58, lite(color, 0.26), 0.22, soft=max(8.0, r * 0.42))
        disc(dst, cx + r * 0.04, cy + r * 0.30, r * 0.64, shade(color, 0.12), 0.20, soft=max(9.0, r * 0.46))


def outlined_ellipse(
    dst: np.ndarray,
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    color: np.ndarray,
    width: float = 5.6,
    opacity: float = 1.0,
    cel: bool = True,
) -> None:
    ellipse(dst, cx, cy, rx + width, ry + width, LINE, opacity)
    ellipse(dst, cx, cy, rx, ry, color, opacity)
    if cel:
        ellipse(dst, cx - rx * 0.16, cy - ry * 0.24, rx * 0.5, ry * 0.42, lite(color, 0.24), 0.2, soft=6.0)
        ellipse(dst, cx + rx * 0.06, cy + ry * 0.26, rx * 0.56, ry * 0.46, shade(color, 0.12), 0.18, soft=7.0)


def fill_poly(dst: np.ndarray, points: list[tuple[float, float]], color: np.ndarray, opacity: float = 1.0) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    fill = tuple(int(round(c * 255)) for c in color) + (int(round(opacity * 255)),)
    draw.polygon([(float(x), float(y)) for x, y in points], fill=fill)
    over(dst, np.asarray(im, dtype=np.float32) / 255.0)


def outlined_poly(dst: np.ndarray, points: list[tuple[float, float]], color: np.ndarray, width: float = 5.0) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    outline = tuple(int(round(c * 255)) for c in LINE) + (255,)
    fill = tuple(int(round(c * 255)) for c in color) + (255,)
    draw.polygon([(float(x), float(y)) for x, y in points], fill=fill, outline=outline)
    # PIL outline is thin — stamp a thicker ring by drawing the same poly scaled out.
    over(dst, np.asarray(im, dtype=np.float32) / 255.0)
    # Thicker outline pass
    ring = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ring)
    rd.line(points + [points[0]], fill=outline, width=int(round(width)), joint="curve")
    over(dst, np.asarray(ring, dtype=np.float32) / 255.0)
    fill_poly(dst, points, color)


def clip_disc(src: np.ndarray, cx: float, cy: float, r: float, soft: float = 1.4) -> None:
    xx, yy = grid()
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    src[..., 3] *= smoothstep(r + soft, r - soft, d)


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


# --- catalogs ----------------------------------------------------------------

FIELDS = {
    "white": rgb("fffdf8"),
    "cream": rgb("f3e4c8"),
    "blush": rgb("f3d2c8"),
    "mint": rgb("d7ead8"),
    "sky": rgb("cfe4f6"),
    "peach": rgb("f4d7b0"),
    "dusk": rgb("d8c6de"),
    "clover": rgb("cfe3b8"),
    "space": rgb("1a1e32"),
}

PLUMAGES = {
    "classic": {"back": rgb("4a2c18"), "breast": rgb("e86a22"), "belly": rgb("f4e6c4"), "beak": rgb("f0b43c"), "feet": rgb("2e1c14")},
    "blue": {"back": rgb("2a4a6e"), "breast": rgb("4a8ad4"), "belly": rgb("e8f0f8"), "beak": rgb("f0c46a"), "feet": rgb("1c2c40")},
    "snow": {"back": rgb("b7aea2"), "breast": rgb("f09a6a"), "belly": rgb("fff8ef"), "beak": rgb("f2cf6e"), "feet": rgb("8a6e58")},
    "dusk": {"back": rgb("4a2e40"), "breast": rgb("e07062"), "belly": rgb("f0d8d4"), "beak": rgb("e8b86a"), "feet": rgb("3a222c")},
    "moss": {"back": rgb("4a4824"), "breast": rgb("e08628"), "belly": rgb("efe6c8"), "beak": rgb("e6c04a"), "feet": rgb("343018")},
    "berry": {"back": rgb("5a2834"), "breast": rgb("e05a6c"), "belly": rgb("f4d8dc"), "beak": rgb("f0b85a"), "feet": rgb("3a1c24")},
    "ink": {"back": rgb("221e22"), "breast": rgb("c43c3c"), "belly": rgb("e8ddd4"), "beak": rgb("e8b44a"), "feet": rgb("1a1618")},
    "gold": {"back": rgb("6e4a22"), "breast": rgb("f0a828"), "belly": rgb("fff0d0"), "beak": rgb("f2c44a"), "feet": rgb("4a3214")},
    "frost": {"back": rgb("465460"), "breast": rgb("e89262"), "belly": rgb("eef2f6"), "beak": rgb("e8c46a"), "feet": rgb("2c343c")},
    "rainbow": {"back": rgb("4a2c18"), "breast": rgb("e86a22"), "belly": rgb("fff4d8"), "beak": rgb("f0b43c"), "feet": rgb("2e1c14")},
}

MUGS = ("blink", "sleepy", "sad", "blep", "wink", "heart", "wide", "spark", "angry", "starry")
ACCENTS = ("none", "bandana", "berry", "leaf", "bow", "worm", "flower", "hat", "crown")


def blink_amount(frame: int) -> float:
    # Closed on frames 5–6, easing in/out. No body bob.
    if frame in (5, 6):
        return 1.0
    if frame == 4:
        return 0.55
    if frame == 7:
        return 0.35
    return 0.0


def stroke_ellipse(dst: np.ndarray, bbox: tuple[float, float, float, float], width: float, color: np.ndarray = LINE) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    col = tuple(int(round(c * 255)) for c in color) + (255,)
    draw.ellipse(bbox, outline=col, width=max(2, int(round(width))))
    over(dst, np.asarray(im, dtype=np.float32) / 255.0)


def fluffy_arc(dst: np.ndarray, cx: float, cy: float, rx: float, ry: float, color: np.ndarray, n: int = 9, blob: float = 15.0) -> None:
    """Scalloped seam across the top of an ellipse — Style C fluffy breast edge."""
    for i in range(n):
        t = (i / max(n - 1, 1)) * math.pi
        x = cx + math.cos(math.pi - t) * rx
        y = cy - math.sin(t) * ry
        disc(dst, x, y, blob * (0.82 + 0.18 * math.sin(t)), color, 1.0, soft=2.4)


def feather_scallops(dst: np.ndarray, cx: float, cy: float, rx: float, ry: float, color: np.ndarray, rows: int = 3) -> None:
    for row in range(rows):
        y = cy - ry * 0.18 + row * (ry * 0.28)
        span = rx * (0.78 - row * 0.1)
        stroke_ellipse(dst, (cx - span, y, cx + span, y + ry * 0.34), 3.2, color)


def paint_foot(dst: np.ndarray, fx: float, fy: float, feet: np.ndarray) -> None:
    volume_ball(dst, fx, fy, 13, 7.4, feet, width=3.6, spec=0.10, shininess=12.0, sss=0.10, bump=21)
    for dx, dy in ((-10.0, 7.2), (0.0, 10.0), (10.0, 7.2)):
        volume_ball(dst, fx + dx, fy + dy, 4.8, 6.8, shade(feet, 0.04), width=2.6, spec=0.08, shininess=10.0, sss=0.08, bump=None)


def sphere_mask(soft: float = 1.8) -> np.ndarray:
    xx, yy = grid()
    return smoothstep(R + soft, R - soft, np.sqrt((xx - CX) ** 2 + (yy - CY) ** 2))


def jagged_below(seam_y: float, xx: np.ndarray, yy: np.ndarray, soft: float = 12.0) -> np.ndarray:
    wave = (
        seam_y
        + 8.0 * np.sin((xx - CX) / 18.0)
        + 4.2 * np.sin((xx - CX) / 7.4 + 1.15)
        + 2.4 * np.abs(np.sin((xx - CX) / 5.0 + 0.4))
    )
    return smoothstep(wave - soft * 0.15, wave + soft * 0.55, yy)


def rainbow_fill(xx: np.ndarray, yy: np.ndarray) -> np.ndarray:
    ang = (np.arctan2(yy - CY, xx - CX) + math.pi) / (2.0 * math.pi)
    stops = np.stack(
        [rgb("e85a4a"), rgb("f0a03a"), rgb("f2d24a"), rgb("5aaa5a"), rgb("4a8ad4"), rgb("8a5ad0")],
        axis=0,
    )
    t = np.clip(ang * (len(stops) - 1), 0.0, len(stops) - 1 - 1e-4)
    i0 = np.floor(t).astype(np.int32)
    frac = (t - i0)[..., None]
    return stops[i0] * (1.0 - frac) + stops[np.clip(i0 + 1, 0, len(stops) - 1)] * frac


def paint_field(kind: str, _frame: int) -> np.ndarray:
    dst = blank()
    color = FIELDS[kind]
    dst[..., :3] = color
    dst[..., 3] = 1.0
    xx, yy = grid()
    vig = ((xx - CX) / 380.0) ** 2 + ((yy - CY) / 380.0) ** 2
    wash = mix(color, shade(color, 0.16 if kind == "space" else 0.08), clamp01(vig * 0.55)[..., None])
    wash = mix(wash, lite(color, 0.10), clamp01(1.0 - vig * 1.4)[..., None] * 0.35)
    dst[..., :3] = np.clip(wash * (1.0 + grain(17 + sum(ord(c) for c in kind), 0.03)[..., None]), 0.0, 1.0)
    ellipse(dst, CX, CY + R + 20, 118, 22, shade(color, 0.28), 0.28 if kind != "space" else 0.40, soft=16.0)
    if kind == "space":
        rng = np.random.RandomState(7)
        for _ in range(46):
            disc(
                dst,
                float(rng.uniform(18, 494)),
                float(rng.uniform(18, 494)),
                float(rng.uniform(0.7, 2.1)),
                rgb("ffffff"),
                float(rng.uniform(0.35, 0.92)),
                soft=0.55,
            )
    return dst


def paint_plumage(kind: str, frame: int) -> np.ndarray:
    dst = blank()
    pal = PLUMAGES[kind]
    back, breast, belly, beak, feet = pal["back"], pal["breast"], pal["belly"], pal["beak"], pal["feet"]
    wing = 3.2 if frame in (3, 4) else 0.0
    xx, yy = grid()

    volume_ball(dst, CX - 150, CY + 92, 34, 20, shade(back, 0.04), width=5.4, spec=0.10, shininess=12.0, bump=31)
    paint_foot(dst, CX - 50, CY + R + 4, feet)
    paint_foot(dst, CX + 50, CY + R + 4, feet)

    outline_disk(dst, CX, CY, R, R, width=LINE_W)
    nx, ny, nz, sphere = ellipsoid(CX, CY, R, R, soft=1.6)
    nx, ny, nz = bump_normals(nx, ny, nz, 101 + sum(ord(c) for c in kind), 0.075)

    albedo = np.broadcast_to(back, (H, W, 3)).copy()
    if kind == "rainbow":
        albedo = rainbow_fill(xx, yy)
    chest_t = jagged_below(CY + 8.0, xx, yy, soft=7.0)
    belly_t = jagged_below(CY + 88.0, xx, yy, soft=6.5)
    albedo = mix(albedo, breast, chest_t)
    albedo = mix(albedo, belly, chest_t * belly_t)
    blit_volume(dst, albedo, nx, ny, nz, sphere, spec=0.20, shininess=18.0, sss=0.26)
    catch = blank()
    disc(catch, CX - R * 0.28, CY - R * 0.34, R * 0.22, rgb("ffffff"), 0.16, soft=R * 0.28)
    catch[..., 3] *= sphere
    over(dst, catch)

    for side in (-1.0, 1.0):
        wx, wy = CX + side * 130, CY + 42 - wing
        volume_ball(dst, wx, wy, 28, 58, shade(back, 0.02), width=5.8, spec=0.12, shininess=14.0, sss=0.14, bump=44)
        nxw, nyw, nzw, aw = ellipsoid(wx - side * 5, wy + 8, 15, 24, soft=2.4)
        blit_volume(dst, shade(back, 0.10), nxw, nyw, nzw, aw * 0.55, spec=0.08, shininess=10.0, sss=0.10)

    bx, by = CX, CY - 2
    volume_ball(dst, bx, by + 4, 15, 11, beak, width=4.2, spec=0.28, shininess=22.0, sss=0.12, bump=None)
    return dst


def paint_star(dst: np.ndarray, x: float, y: float, size: float, color: np.ndarray) -> None:
    fill_poly(
        dst,
        [
            (x, y - size),
            (x + size * 0.22, y - size * 0.22),
            (x + size, y),
            (x + size * 0.22, y + size * 0.22),
            (x, y + size),
            (x - size * 0.22, y + size * 0.22),
            (x - size, y),
            (x - size * 0.22, y - size * 0.22),
        ],
        color,
    )


def draw_eye(dst: np.ndarray, ex: float, ey: float, radius: float, closed: float, kind: str) -> None:
    if closed >= 0.85:
        outlined_ellipse(dst, ex, ey + 2, radius * 0.94, 7.2, LINE, width=3.6, cel=False)
        return

    if kind == "wide":
        radius *= 1.08
    if kind == "angry":
        radius *= 0.94

    ink = rgb("121010")
    if kind == "heart":
        ink = rgb("3a1418")

    outline_disk(dst, ex, ey, radius, radius, width=5.8)
    nx, ny, nz, a = ellipsoid(ex, ey, radius, radius, soft=1.2)
    blit_volume(dst, ink, nx, ny, nz, a, spec=0.62, shininess=36.0, sss=0.04, ambient=0.16, wrap=0.12)

    if kind == "heart":
        pr = radius * 0.42
        fill_poly(
            dst,
            [
                (ex, ey + pr * 0.72),
                (ex - pr * 0.72, ey - 2),
                (ex - pr * 0.22, ey - pr * 0.55),
                (ex, ey - pr * 0.18),
                (ex + pr * 0.22, ey - pr * 0.55),
                (ex + pr * 0.72, ey - 2),
            ],
            rgb("f08aa0"),
        )
    else:
        disc(dst, ex - radius * 0.30, ey - radius * 0.32, radius * 0.28, rgb("ffffff"), 0.98, soft=1.0)
        disc(dst, ex + radius * 0.22, ey + radius * 0.18, radius * 0.12, rgb("ffffff"), 0.84, soft=0.8)
        if kind in ("spark", "starry"):
            disc(dst, ex + radius * 0.02, ey - radius * 0.04, radius * 0.08, rgb("fff6c8"), 0.92, soft=0.7)

    if closed > 0.2:
        lid = blank()
        ellipse(lid, ex, ey - radius * (1.2 - closed * 0.95), radius * 1.12, radius * 0.92, rgb("4a2c18"), 1.0)
        clip_disc(lid, ex, ey, radius + 1.2)
        over(dst, lid)


def paint_brow(dst: np.ndarray, ex: float, ey: float, radius: float, kind: str) -> None:
    by = ey - radius - 10
    if kind == "angry":
        inward = 1.0 if ex < CX else -1.0
        fill_poly(
            dst,
            [
                (ex - 20 * inward, by - 10),
                (ex + 18 * inward, by + 6),
                (ex + 16 * inward, by + 12),
                (ex - 20 * inward, by - 2),
            ],
            LINE,
        )
        return
    tilt = -10.0 if kind == "sad" else 0.0
    outlined_ellipse(dst, ex + tilt * 0.15, by + (4 if kind == "sad" else 0), 15, 5.8, rgb("efd6b4"), width=3.2, cel=False)
    if kind == "sad":
        fill_poly(
            dst,
            [(ex - 18, by - 6), (ex + 16, by + 6), (ex + 14, by + 11), (ex - 18, by)],
            LINE,
        )


def paint_mug(kind: str, frame: int) -> np.ndarray:
    dst = blank()
    closed = blink_amount(frame)
    if kind == "sleepy":
        closed = 1.0
    if kind == "wink":
        left_closed, right_closed = 1.0, closed
    else:
        left_closed = right_closed = closed

    lx, rx, ey = CX - 52.0, CX + 52.0, CY - 50.0
    er = 36.0 if kind != "wide" else 39.0
    draw_eye(dst, lx, ey, er, left_closed, kind)
    draw_eye(dst, rx, ey, er, right_closed, kind)
    paint_brow(dst, lx, ey, er, kind)
    paint_brow(dst, rx, ey, er, kind)

    if kind == "sad":
        outlined_ellipse(dst, rx + 10, ey + 48, 6.5, 11, rgb("b8d8f0"), width=3.2, cel=False)
    if kind in ("spark", "starry") and closed < 0.4:
        fill_poly(dst, [(lx - 5, ey - 58), (lx, ey - 42), (lx + 5, ey - 58), (lx, ey - 64)], rgb("fff6c8"))
    if kind == "starry" and closed < 0.45:
        paint_star(dst, lx - 38, ey - 18, 7.0, rgb("fff6c8"))
        paint_star(dst, rx + 40, ey + 10, 6.0, rgb("ffe08a"))

    mx, my = CX + 6, CY + 14
    if kind in ("blep", "blink", "wide", "spark", "starry"):
        outlined_ellipse(dst, mx + 3, my + 5, 8.5, 11, rgb("f09098"), width=3.2, cel=False)
    elif kind == "sad":
        ellipse(dst, CX, my + 6, 10, 4, LINE, 0.85, soft=1.1)
    elif kind == "sleepy":
        ellipse(dst, CX, my + 2, 7, 3, LINE, 0.8, soft=1.0)
    elif kind == "angry":
        ellipse(dst, CX, my + 4, 8, 3.2, LINE, 0.88, soft=1.0)
    return dst


def paint_accent(kind: str, frame: int) -> np.ndarray:
    dst = blank()
    if kind == "none":
        return dst
    bob = math.sin(frame / FRAMES * math.pi * 2.0) * 2.2

    if kind == "bandana":
        # Neck kerchief on the lower sphere — knot + two tails, not a chest sash.
        y = CY + 86
        xx, yy = grid()
        d = np.sqrt((xx - CX) ** 2 + (yy - CY) ** 2)
        band = blank()
        ellipse(band, CX, y, 88, 16, LINE, 1.0)
        ellipse(band, CX, y, 82, 11, rgb("5a9a4a"), 1.0)
        band[..., 3] *= (yy > CY + 70).astype(np.float32) * smoothstep(R + 1.0, R - 10.0, d)
        over(dst, band)
        outlined_disc(dst, CX - 82, y + 6, 11, rgb("6aaa52"), width=3.6, cel=False)
        outlined_poly(
            dst,
            [(CX - 88, y + 4), (CX - 126, y + 26 + bob), (CX - 110, y + 34 + bob), (CX - 80, y + 12)],
            rgb("5a9a4a"),
            width=3.8,
        )
        outlined_poly(
            dst,
            [(CX - 82, y + 8), (CX - 116, y + 42 + bob), (CX - 98, y + 48 + bob), (CX - 74, y + 14)],
            rgb("6aaa52"),
            width=3.8,
        )
    elif kind == "berry":
        bx, by = CX + 34, CY - 8 + bob
        volume_ball(dst, bx, by, 13, 13, rgb("c43c4a"), width=3.8, spec=0.28, shininess=20.0)
        volume_ball(dst, bx + 14, by + 6, 11, 11, rgb("d44a56"), width=3.4, spec=0.28, shininess=20.0)
        volume_ball(dst, bx + 4, by - 16, 10, 6, rgb("5a9a4a"), width=3.0, spec=0.16, shininess=12.0)
    elif kind == "leaf":
        lx, ly = CX + 18, CY - R - 8 + bob
        volume_ball(dst, lx, ly, 28, 16, rgb("6aaa52"), width=4.2, spec=0.18, shininess=14.0)
        fill_poly(dst, [(lx - 4, ly + 14), (lx, ly - 4), (lx + 4, ly + 14)], shade(rgb("4a3428"), 0.1))
    elif kind == "bow":
        y = CY - R + 8 + bob
        volume_ball(dst, CX - 22, y, 20, 14, rgb("e06a7a"), width=3.8, spec=0.22, shininess=16.0)
        volume_ball(dst, CX + 22, y, 20, 14, rgb("e06a7a"), width=3.8, spec=0.22, shininess=16.0)
        volume_ball(dst, CX, y, 9, 9, rgb("c43c4a"), width=3.2, spec=0.24, shininess=18.0)
    elif kind == "worm":
        wx, wy = CX + 26, CY + 4 + bob
        volume_ball(dst, wx, wy, 22, 8, rgb("f09aa8"), width=3.6, spec=0.20, shininess=14.0, sss=0.24)
        disc(dst, wx + 16, wy - 2, 3.2, LINE, 0.9, soft=0.8)
        disc(dst, wx + 10, wy - 2, 3.2, LINE, 0.9, soft=0.8)
    elif kind == "flower":
        fx, fy = CX - 118, CY - 36 + bob
        for ang in range(5):
            a = ang * (2.0 * math.pi / 5.0) - 0.4
            volume_ball(dst, fx + math.cos(a) * 14, fy + math.sin(a) * 14, 9, 9, rgb("f0b0c0"), width=3.0, spec=0.22, shininess=16.0, sss=0.20)
        volume_ball(dst, fx, fy, 8, 8, rgb("f0c14a"), width=3.0, spec=0.30, shininess=20.0)
    elif kind == "hat":
        y = CY - R + 10 + bob
        volume_ball(dst, CX, y + 22, 86, 26, rgb("c44a32"), width=4.8, spec=0.18, shininess=14.0)
        volume_ball(dst, CX, y + 6, 72, 24, rgb("d45a3e"), width=4.6, spec=0.20, shininess=16.0)
        volume_ball(dst, CX + 68, y + 2, 11, 11, rgb("f0c14a"), width=3.2, spec=0.32, shininess=22.0)
    elif kind == "crown":
        y = CY - R - 2 + bob
        outlined_poly(
            dst,
            [
                (CX - 48, y + 28),
                (CX - 50, y + 4),
                (CX - 28, y + 18),
                (CX, y - 8),
                (CX + 28, y + 18),
                (CX + 50, y + 4),
                (CX + 48, y + 28),
            ],
            rgb("f0c14a"),
            width=4.6,
        )
        for jx, jy, jc in ((CX, y + 2, rgb("e05a6c")), (CX - 30, y + 16, rgb("4a8ad4")), (CX + 30, y + 16, rgb("6aaa52"))):
            volume_ball(dst, jx, jy, 5.5, 5.5, jc, width=2.4, spec=0.40, shininess=28.0, bump=None)
    return dst


TRAIT_SPEC = {
    "field": [
        ("white", "White", 16),
        ("cream", "Cream", 14),
        ("blush", "Blush", 13),
        ("mint", "Mint", 13),
        ("sky", "Sky", 14),
        ("peach", "Peach", 12),
        ("dusk", "Dusk", 10),
        ("clover", "Forest", 10),
        ("space", "Space", 5),
    ],
    "plumage": [
        ("classic", "Brown", 25),
        ("blue", "Blue", 18),
        ("berry", "Pink", 14),
        ("moss", "Green", 14),
        ("gold", "Gold", 10),
        ("snow", "Snow", 8),
        ("dusk", "Dusk", 6),
        ("frost", "Frost", 5),
        ("rainbow", "Rainbow", 4),
        ("ink", "Void", 3),
    ],
    "mug": [
        ("blep", "Blep", 22),
        ("blink", "Normal", 16),
        ("spark", "Sparkly", 14),
        ("sleepy", "Sleepy", 12),
        ("wink", "Wink", 10),
        ("wide", "Wide", 8),
        ("angry", "Angry", 7),
        ("sad", "Sad", 5),
        ("starry", "Starry", 4),
        ("heart", "Heart", 3),
    ],
    "accent": [
        ("none", "None", 36),
        ("bandana", "Bandana", 12),
        ("flower", "Flower", 10),
        ("leaf", "Leaf", 9),
        ("berry", "Berry", 8),
        ("hat", "Hat", 7),
        ("worm", "Worm", 6),
        ("bow", "Bow", 5),
        ("crown", "Crown", 4),
    ],
}

PAINTERS = {
    "field": {k: (lambda kind: (lambda frame, k=kind: paint_field(k, frame)))(k) for k in FIELDS},
    "plumage": {k: (lambda kind: (lambda frame, k=kind: paint_plumage(k, frame)))(k) for k in PLUMAGES},
    "mug": {k: (lambda kind: (lambda frame, k=kind: paint_mug(k, frame)))(k) for k in MUGS},
    "accent": {k: (lambda kind: (lambda frame, k=kind: paint_accent(k, frame)))(k) for k in ACCENTS},
}

STACK = ("field", "plumage", "mug", "accent")

SIGNATURES = [
    {"field": "white", "plumage": "classic", "mug": "blep", "accent": "none"},
    {"field": "blush", "plumage": "berry", "mug": "heart", "accent": "bow"},
    {"field": "mint", "plumage": "moss", "mug": "blink", "accent": "leaf"},
    {"field": "sky", "plumage": "blue", "mug": "wide", "accent": "flower"},
    {"field": "cream", "plumage": "snow", "mug": "sleepy", "accent": "none"},
    {"field": "peach", "plumage": "gold", "mug": "spark", "accent": "berry"},
    {"field": "dusk", "plumage": "dusk", "mug": "wink", "accent": "worm"},
    {"field": "clover", "plumage": "classic", "mug": "sad", "accent": "leaf"},
    {"field": "space", "plumage": "ink", "mug": "starry", "accent": "crown"},
    {"field": "cream", "plumage": "rainbow", "mug": "spark", "accent": "none"},
    {"field": "blush", "plumage": "snow", "mug": "blink", "accent": "hat"},
    {"field": "mint", "plumage": "gold", "mug": "sleepy", "accent": "flower"},
    {"field": "sky", "plumage": "berry", "mug": "spark", "accent": "bandana"},
    {"field": "peach", "plumage": "frost", "mug": "heart", "accent": "none"},
    {"field": "dusk", "plumage": "blue", "mug": "angry", "accent": "worm"},
    {"field": "clover", "plumage": "ink", "mug": "blink", "accent": "leaf"},
]

TRAIT_LABELS = (
    ("field", "Field"),
    ("plumage", "Plumage"),
    ("mug", "Mug"),
    ("accent", "Accent"),
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
        "name": "BirbNation",
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
    samples = []
    for index, selection in enumerate(SIGNATURES, start=1):
        print(f"  sample #{index}")
        frames = compose_selection(selection)
        save_loop_gif(frames, PREVIEW_DIR / f"{index}.gif", DURATION_MS, colors=180)
        samples.append(
            {
                "id": index,
                "name": f"Birb #{index}",
                "image": f"/birbs-preview/{index}.gif",
                "attributes": [
                    {"trait_type": label, "value": name_of(key, selection[key])} for key, label in TRAIT_LABELS
                ],
            }
        )
    (PREVIEW_DIR / "samples.json").write_text(json.dumps(samples, indent=2) + "\n", encoding="utf-8")


COLLECTION_DESCRIPTION = (
    "BirbNation is a 2,222-piece collection of looping round-borb robin PFP GIFs on Robinhood Chain. "
    "Each birb is stacked from four layers — field, plumage, mug, and accent — then flattened onto one 12-frame GIF. "
    "Painted 3D illustration. Warm key. Soft clay volume. Chocolate cap. Burnt-orange chest. Cream belly. A pink blep."
)

COLLECTION_STORY = (
    "Welcome to BirbNation.\n\n"
    "A 2,222-piece collection of looping round-borb robin PFP GIFs on Robinhood Chain. "
    "Each birb is stacked from four layers — field, plumage, mug, and accent — then flattened onto one 12-frame GIF. "
    "Sticker fields behind them. Chocolate caps. Burnt-orange chests. Cream bellies. Hats, crowns, and the occasional worm. "
    "Eyes blink. Wings twitch. The body stays a sphere.\n\n"
    "Painted like a Doodle with BAYC form-light — canvas grain, wrap shade, a warm key from the left.\n\n"
    "Each birb is a vibe — explorers, dreamers, jokers, guardians — on one shared clock.\n\n"
    "Minting on Robinhood Chain (chain ID 4663). Gas is ETH."
)


def panoramic_wash(width: int, height: int) -> Image.Image:
    colors = [FIELDS["cream"], FIELDS["blush"], FIELDS["mint"], FIELDS["sky"]]
    x = np.linspace(0.0, 1.0, width, dtype=np.float32)
    y = np.linspace(0.0, 1.0, height, dtype=np.float32)
    xx, yy = np.meshgrid(x, y)
    stops = np.stack(colors, axis=0)
    t = np.clip(xx * 0.72 + yy * 0.28, 0.0, 0.999) * (len(colors) - 1)
    i0 = np.floor(t).astype(np.int32)
    f = (t - i0)[..., None]
    c0 = stops[i0]
    c1 = stops[np.clip(i0 + 1, 0, len(colors) - 1)]
    rgb_out = c0 * (1.0 - f) + c1 * f
    arr = np.dstack([np.clip(rgb_out * 255.0, 0, 255).astype(np.uint8), np.full((height, width), 255, dtype=np.uint8)])
    return Image.fromarray(arr, "RGBA")


def rounded_portrait(portrait: Image.Image, size: int, radius: int = 56) -> Image.Image:
    face = portrait.resize((size, size), Image.Resampling.LANCZOS).convert("RGBA")
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=255)
    face.putalpha(Image.composite(face.split()[-1], Image.new("L", (size, size), 0), mask))
    return face


def place_portrait(canvas: Image.Image, portrait: Image.Image, x: int, y: int, size: int, radius: int = 56) -> None:
    face = rounded_portrait(portrait, size, radius)
    shadow = Image.new("RGBA", (size + 24, size + 24), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((8, 14, size + 8, size + 18), radius=radius, fill=(74, 52, 40, 70))
    canvas.alpha_composite(shadow, (x - 8, y - 6))
    canvas.alpha_composite(face, (x, y))


def lineup_banner(width: int, height: int, portraits: list[Image.Image]) -> Image.Image:
    canvas = panoramic_wash(width, height)
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
    (META_DIR / "birbs-description.txt").write_text(COLLECTION_STORY + "\n", encoding="utf-8")
    (META_DIR / "birbs.json").write_text(
        json.dumps(
            {
                "name": "BirbNation",
                "symbol": "BIRB",
                "description": COLLECTION_DESCRIPTION,
                "image": "/brand/collection-birbs.gif",
                "featured_image": "/brand/featured-birbs.jpg",
                "banner_image": "/brand/banner-birbs.png",
                "opensea_banner_image": "/brand/banner-birbs-opensea.jpg",
                "external_link": "/birbs",
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
    ImageDraw.Draw(ring).ellipse((10, 10, SIZE - 10, SIZE - 10), outline=(224, 122, 58, 230), width=10)
    logo = Image.alpha_composite(logo, ring)
    save_image(logo.resize((512, 512), Image.Resampling.LANCZOS), BRAND_DIR / "logo-birbs.png")
    save_apng(
        [frame.resize((512, 512), Image.Resampling.LANCZOS) for frame in logo_frames],
        BRAND_DIR / "logo-birbs-loop.png",
    )

    save_image(lineup_banner(1500, 560, portraits[:5]).convert("RGB"), BRAND_DIR / "banner-birbs.png", quality=94)
    save_image(lineup_banner(2800, 700, portraits).convert("RGB"), BRAND_DIR / "banner-birbs-opensea.jpg", quality=90)

    featured = panoramic_wash(1200, 800)
    place_portrait(featured, portraits[0], 90, 110, 560, radius=64)
    place_portrait(featured, portraits[2], 540, 130, 560, radius=64)
    save_image(featured.convert("RGB"), BRAND_DIR / "featured-birbs.jpg", quality=90)

    gif_frames = [frame.resize((1000, 1000), Image.Resampling.LANCZOS) for frame in logo_frames]
    save_loop_gif(gif_frames, BRAND_DIR / "collection-birbs.gif", DURATION_MS, colors=180)
    write_collection_meta()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--brand-only", action="store_true", help="Rebuild logo, banners, and listing copy")
    args = parser.parse_args()
    if args.brand_only:
        print("Writing BirbNation brand kit…")
        build_brand()
        print("Done.")
        return
    print("Building BirbNation trait loops…")
    build_traits()
    print("Compositing sample GIF tokens…")
    build_samples()
    print("Writing brand…")
    build_brand()
    print("Done.")


if __name__ == "__main__":
    main()
