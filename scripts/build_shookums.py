#!/usr/bin/env python3
"""Paint Halloween Shook'ums — looping sheet-ghost PFP layers.

Every trait is a 12-frame APNG on a shared 512 canvas and 90ms clock.
Sheet, mug, hat, and wrap share one hover so accessories never warp the skeleton.
Night stays still. Charm floats on its own tiny bob.

Look: painted 3D clay — BAYC form-light with Doodles volume.
One plump sheet. Two arm nubs. A scalloped hem. Thick drawn outline.
Three bodies only: classic white, blush, void. Hats sit on the crown.
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

TRAIT_DIR = ROOT / "public" / "shookums-traits"
PREVIEW_DIR = ROOT / "public" / "shookums-preview"
BRAND_DIR = ROOT / "public" / "brand"
META_DIR = ROOT / "public" / "metadata"

SIZE = 512
FRAMES = 12
DURATION_MS = 90
H, W = SIZE, SIZE
YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)

# Locked skeleton — accessories must sit on these points. Never edit per trait.
CX, CY = 256.0, 278.0
RX, RY = 154.0, 172.0
LINE_W = 9.0
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


LINE = rgb("2a1c14")


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


def over(dst: np.ndarray, src: np.ndarray) -> None:
    sa = src[..., 3:4]
    da = dst[..., 3:4]
    out_a = sa + da * (1.0 - sa)
    rgb_out = src[..., :3] * sa + dst[..., :3] * da * (1.0 - sa)
    dst[..., :3] = np.divide(rgb_out, out_a, out=np.zeros_like(rgb_out), where=out_a > 1e-6)
    dst[..., 3:4] = out_a


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


def shade(color: np.ndarray, t: float = 0.22) -> np.ndarray:
    return mix(color, rgb("2a1c14"), t)


def lite(color: np.ndarray, t: float = 0.32) -> np.ndarray:
    return mix(color, rgb("ffffff"), t)


def disc(dst: np.ndarray, cx: float, cy: float, r: float, color: np.ndarray, opacity: float = 1.0, soft: float = SOFT) -> None:
    d = np.sqrt((XX - cx) ** 2 + (YY - cy) ** 2)
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
    d = np.sqrt(((XX - cx) / max(rx, 1.0)) ** 2 + ((YY - cy) / max(ry, 1.0)) ** 2)
    edge = soft / max(rx, ry, 1.0)
    a = smoothstep(1.0 + edge, 1.0 - edge, d) * opacity
    layer = blank()
    layer[..., :3] = color
    layer[..., 3] = a
    over(dst, layer)


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
    over(dst, np.asarray(im, dtype=np.float32) / 255.0)
    ring = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ring)
    rd.line(points + [points[0]], fill=outline, width=int(round(width)), joint="curve")
    over(dst, np.asarray(ring, dtype=np.float32) / 255.0)
    fill_poly(dst, points, color)


def clip_disc(src: np.ndarray, cx: float, cy: float, r: float, soft: float = 1.4) -> None:
    d = np.sqrt((XX - cx) ** 2 + (YY - cy) ** 2)
    src[..., 3] *= smoothstep(r + soft, r - soft, d)


def stroke_ellipse(dst: np.ndarray, bbox: tuple[float, float, float, float], width: float, color: np.ndarray = LINE) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    col = tuple(int(round(c * 255)) for c in color) + (255,)
    draw.ellipse(bbox, outline=col, width=max(2, int(round(width))))
    over(dst, np.asarray(im, dtype=np.float32) / 255.0)


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


def hover_y(frame: int) -> float:
    """Shared bob. Sheet, mug, hat, and wrap all use this — the skeleton never desyncs."""
    return math.sin(frame / FRAMES * math.pi * 2.0) * 5.2


def hem_mask(cx: float, cy: float, rx: float, ry: float) -> np.ndarray:
    t = (XX - cx) / max(rx, 1.0)
    hem = cy + ry * 0.80 + 16.5 * np.sin(t * 3.2) + 7.0 * np.sin(t * 6.6 + 0.55)
    return smoothstep(hem + 7.0, hem - 9.0, YY)


def sheet_volume(cx: float, cy: float, rx: float = RX, ry: float = RY) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    nx, ny, nz, a = ellipsoid(cx, cy, rx, ry, soft=1.55)
    a = a * hem_mask(cx, cy, rx, ry)
    parts = [
        (nx, ny, nz, a),
        ellipsoid(cx - rx * 0.90, cy + 16.0, 40.0, 25.0, soft=1.7),
        ellipsoid(cx + rx * 0.90, cy + 16.0, 40.0, 25.0, soft=1.7),
        ellipsoid(cx, cy - ry * 0.92, 22.0, 16.0, soft=1.8),
    ]
    out_a = np.zeros((H, W), dtype=np.float32)
    out_nx = np.zeros((H, W), dtype=np.float32)
    out_ny = np.zeros((H, W), dtype=np.float32)
    out_nz = np.zeros((H, W), dtype=np.float32)
    for pnx, pny, pnz, pa in parts:
        choose = pa >= out_a
        out_nx = np.where(choose, pnx, out_nx)
        out_ny = np.where(choose, pny, out_ny)
        out_nz = np.where(choose, pnz, out_nz)
        out_a = np.maximum(out_a, pa)
    return out_nx, out_ny, out_nz, out_a


# --- catalogs ----------------------------------------------------------------

NIGHTS = {
    "parchment": rgb("f4ebe0"),
    "pumpkin": rgb("f0c090"),
    "blush": rgb("e8c4d0"),
    "midnight": rgb("1c1830"),
    "moss": rgb("2a3828"),
    "dusk": rgb("3a2a48"),
    "candy": rgb("f0d0dc"),
    "fog": rgb("c8c4d4"),
    "bloodmoon": rgb("4a2020"),
    "void": rgb("121018"),
}

SHEETS = {
    "classic": {"cloth": rgb("f2ece4"), "shade": rgb("d8cfc4")},
    "blush": {"cloth": rgb("f0c8d4"), "shade": rgb("e0a8b8")},
    "void": {"cloth": rgb("2e2a38"), "shade": rgb("1c1826")},
}

MUGS = ("blink", "spooked", "sleepy", "sad", "blep", "wink", "heart", "spark", "angry", "starry")
HATS = ("none", "witch", "pumpkin", "bow", "halo", "party", "crown", "cat", "wizard", "flower")
WRAPS = ("none", "chain", "scarf", "bowtie", "cape", "pearls", "collar")
CHARMS = ("none", "pumpkin", "candy", "bat", "broom", "corn", "potion", "moon")


def blink_amount(frame: int) -> float:
    if frame in (5, 6):
        return 1.0
    if frame == 4:
        return 0.55
    if frame == 7:
        return 0.35
    return 0.0


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


def paint_night(kind: str, _frame: int) -> np.ndarray:
    dst = blank()
    color = NIGHTS[kind]
    dst[..., :3] = color
    dst[..., 3] = 1.0
    vig = ((XX - CX) / 380.0) ** 2 + ((YY - CY) / 380.0) ** 2
    dark = kind in ("midnight", "moss", "dusk", "bloodmoon", "void")
    wash = mix(color, shade(color, 0.18 if dark else 0.08), clamp01(vig * 0.55)[..., None])
    wash = mix(wash, lite(color, 0.10), clamp01(1.0 - vig * 1.4)[..., None] * 0.35)
    dst[..., :3] = np.clip(wash * (1.0 + grain(17 + sum(ord(c) for c in kind), 0.03)[..., None]), 0.0, 1.0)
    ellipse(dst, CX, CY + RY + 28, 120, 22, shade(color, 0.30), 0.32 if not dark else 0.46, soft=16.0)
    if kind in ("midnight", "void", "dusk"):
        rng = np.random.RandomState(11)
        for _ in range(40):
            disc(
                dst,
                float(rng.uniform(18, 494)),
                float(rng.uniform(18, 494)),
                float(rng.uniform(0.7, 2.0)),
                rgb("fff6d8"),
                float(rng.uniform(0.28, 0.88)),
                soft=0.55,
            )
    if kind == "bloodmoon":
        disc(dst, 410, 86, 38, rgb("e07062"), 0.22, soft=28.0)
    return dst


def paint_sheet(kind: str, frame: int) -> np.ndarray:
    dst = blank()
    pal = SHEETS[kind]
    cloth, fold = pal["cloth"], pal["shade"]
    dy = hover_y(frame)
    cx, cy = CX, CY + dy
    nx, ny, nz, a = sheet_volume(cx, cy)
    nx, ny, nz = bump_normals(nx, ny, nz, 90 + sum(ord(c) for c in kind), 0.055)
    outline = blank()
    onx, ony, onz, oa = sheet_volume(cx, cy, RX + LINE_W, RY + LINE_W)
    blit_soft(outline, LINE, oa * 0.96)
    over(dst, outline)
    albedo = np.broadcast_to(cloth, (H, W, 3)).copy()
    fold_t = clamp01(((YY - cy) / RY) * 0.45 + 0.18)
    albedo = mix(albedo, fold, fold_t)
    blit_volume(dst, albedo, nx, ny, nz, a, spec=0.14, shininess=14.0, sss=0.32)
    catch = blank()
    disc(catch, cx - RX * 0.28, cy - RY * 0.36, RX * 0.22, rgb("ffffff"), 0.18 if kind != "void" else 0.10, soft=RX * 0.28)
    catch[..., 3] *= a
    over(dst, catch)
    return dst


def draw_eye(dst: np.ndarray, ex: float, ey: float, radius: float, closed: float, kind: str) -> None:
    if closed >= 0.85:
        outlined_ellipse(dst, ex, ey + 2, radius * 0.94, 6.6, LINE, width=3.4, cel=False)
        return
    if kind == "spooked":
        radius *= 1.10
    if kind == "angry":
        radius *= 0.94
    ink = rgb("121010")
    if kind == "heart":
        ink = rgb("3a1418")
    outline_disk(dst, ex, ey, radius, radius, width=5.4)
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
        ellipse(lid, ex, ey - radius * (1.2 - closed * 0.95), radius * 1.12, radius * 0.92, rgb("d8cfc4"), 1.0)
        clip_disc(lid, ex, ey, radius + 1.2)
        over(dst, lid)


def paint_brow(dst: np.ndarray, ex: float, ey: float, radius: float, kind: str) -> None:
    by = ey - radius - 8
    if kind == "angry":
        inward = 1.0 if ex < CX else -1.0
        fill_poly(
            dst,
            [
                (ex - 18 * inward, by - 8),
                (ex + 16 * inward, by + 6),
                (ex + 14 * inward, by + 11),
                (ex - 18 * inward, by - 1),
            ],
            LINE,
        )
        return
    if kind == "sad":
        fill_poly(
            dst,
            [(ex - 16, by - 4), (ex + 14, by + 7), (ex + 12, by + 12), (ex - 16, by + 2)],
            LINE,
        )


def paint_mug(kind: str, frame: int) -> np.ndarray:
    dst = blank()
    dy = hover_y(frame)
    closed = blink_amount(frame)
    if kind == "sleepy":
        closed = 1.0
    if kind == "wink":
        left_closed, right_closed = 1.0, closed
    else:
        left_closed = right_closed = closed
    lx, rx, ey = CX - 48.0, CX + 48.0, CY - 46.0 + dy
    er = 30.0 if kind != "spooked" else 33.0
    draw_eye(dst, lx, ey, er, left_closed, kind)
    draw_eye(dst, rx, ey, er, right_closed, kind)
    paint_brow(dst, lx, ey, er, kind)
    paint_brow(dst, rx, ey, er, kind)
    if kind == "sad":
        outlined_ellipse(dst, rx + 8, ey + 42, 6.0, 10, rgb("b8d8f0"), width=3.0, cel=False)
    if kind in ("spark", "starry") and closed < 0.4:
        fill_poly(dst, [(lx - 4, ey - 50), (lx, ey - 36), (lx + 4, ey - 50), (lx, ey - 56)], rgb("fff6c8"))
    if kind == "starry" and closed < 0.45:
        paint_star(dst, lx - 34, ey - 16, 6.4, rgb("fff6c8"))
        paint_star(dst, rx + 36, ey + 8, 5.6, rgb("ffe08a"))
    mx, my = CX + 4, CY + 8 + dy
    if kind in ("blep", "blink", "spooked", "spark", "starry"):
        outlined_ellipse(dst, mx + 3, my + 6, 7.8, 10, rgb("f09098"), width=3.0, cel=False)
    elif kind == "sad":
        ellipse(dst, CX, my + 6, 9, 3.6, LINE, 0.85, soft=1.1)
    elif kind == "sleepy":
        ellipse(dst, CX, my + 2, 6.5, 2.8, LINE, 0.8, soft=1.0)
    elif kind == "angry":
        ellipse(dst, CX, my + 4, 7.5, 3.0, LINE, 0.88, soft=1.0)
    elif kind == "heart":
        outlined_ellipse(dst, mx, my + 4, 6.5, 4.2, rgb("e06a7a"), width=2.8, cel=False)
    return dst


# Hat-layer only. `y` is the hat origin; each kind draws its brim/base below that.
# Brimmed hats need more lift so the brim perches on the crown instead of the
# forehead. Tall cones are drawn shorter so the tip stays on the 512 canvas.
HAT_LIFT = {
    "witch": 84.0,
    "wizard": 74.0,
    "pumpkin": 74.0,
    "halo": 32.0,
    "party": 38.0,
    "crown": 52.0,
    "bow": 46.0,
    "flower": 52.0,
    "cat": 42.0,
}


def paint_hat(kind: str, frame: int) -> np.ndarray:
    dst = blank()
    if kind == "none":
        return dst
    dy = hover_y(frame)
    y = CY - RY + 8 - HAT_LIFT.get(kind, 24.0) + dy
    if kind == "witch":
        volume_ball(dst, CX, y + 34, 108, 20, rgb("1e1a24"), width=5.2, spec=0.08, shininess=8.0, sss=0.04)
        outlined_poly(
            dst,
            [(CX - 38, y + 28), (CX + 38, y + 28), (CX + 14, y - 6), (CX - 14, y - 6)],
            rgb("2a2430"),
            width=5.0,
        )
        volume_ball(dst, CX, y - 8, 13, 11, rgb("1e1a24"), width=3.2, spec=0.08, shininess=8.0, sss=0.04)
        ellipse(dst, CX, y + 24, 36, 8, rgb("f0c14a"), 0.96, soft=1.4)
    elif kind == "pumpkin":
        volume_ball(dst, CX, y + 22, 86, 28, rgb("e07028"), width=4.8, spec=0.18, shininess=14.0)
        volume_ball(dst, CX, y + 4, 58, 22, rgb("f08632"), width=4.4, spec=0.20, shininess=16.0)
        volume_ball(dst, CX, y - 18, 10, 14, rgb("5a9a4a"), width=3.2, spec=0.16, shininess=12.0)
    elif kind == "bow":
        volume_ball(dst, CX - 24, y + 6, 22, 16, rgb("e06a8a"), width=3.8, spec=0.22, shininess=16.0)
        volume_ball(dst, CX + 24, y + 6, 22, 16, rgb("e06a8a"), width=3.8, spec=0.22, shininess=16.0)
        volume_ball(dst, CX, y + 6, 10, 10, rgb("c43c5a"), width=3.2, spec=0.24, shininess=18.0)
    elif kind == "halo":
        stroke_ellipse(dst, (CX - 58, y - 24, CX + 58, y + 8), 14.0, LINE)
        stroke_ellipse(dst, (CX - 54, y - 20, CX + 54, y + 4), 9.0, rgb("f0c14a"))
        disc(dst, CX + 40, y - 16, 5.5, rgb("fff6c8"), 0.78, soft=2.0)
    elif kind == "party":
        outlined_poly(
            dst,
            [(CX - 36, y + 20), (CX + 36, y + 20), (CX, y - 52)],
            rgb("e05a6c"),
            width=4.2,
        )
        volume_ball(dst, CX, y - 54, 8, 8, rgb("f0c14a"), width=2.8, spec=0.34, shininess=22.0)
        for i, col in enumerate((rgb("f0c14a"), rgb("4a8ad4"), rgb("f0c14a"))):
            disc(dst, CX - 14 + i * 14, y + 8, 5.5, col, 0.95, soft=1.0)
    elif kind == "crown":
        outlined_poly(
            dst,
            [
                (CX - 48, y + 30),
                (CX - 50, y + 6),
                (CX - 28, y + 20),
                (CX, y - 6),
                (CX + 28, y + 20),
                (CX + 50, y + 6),
                (CX + 48, y + 30),
            ],
            rgb("f0c14a"),
            width=4.6,
        )
        for jx, jy, jc in ((CX, y + 4, rgb("e05a6c")), (CX - 30, y + 18, rgb("4a8ad4")), (CX + 30, y + 18, rgb("6aaa52"))):
            volume_ball(dst, jx, jy, 5.5, 5.5, jc, width=2.4, spec=0.40, shininess=28.0, bump=None)
    elif kind == "cat":
        for side in (-1.0, 1.0):
            outlined_poly(
                dst,
                [
                    (CX + side * 28, y + 18),
                    (CX + side * 58, y + 22),
                    (CX + side * 40, y - 28),
                ],
                rgb("2a2430"),
                width=3.8,
            )
            fill_poly(
                dst,
                [
                    (CX + side * 34, y + 14),
                    (CX + side * 50, y + 16),
                    (CX + side * 40, y - 14),
                ],
                rgb("f09098"),
            )
    elif kind == "wizard":
        volume_ball(dst, CX, y + 26, 88, 16, rgb("4a2e68"), width=4.4, spec=0.14, shininess=12.0)
        outlined_poly(
            dst,
            [(CX - 16, y + 20), (CX + 16, y + 20), (CX + 5, y - 30), (CX - 5, y - 30)],
            rgb("5a3a7a"),
            width=4.2,
        )
        paint_star(dst, CX + 8, y - 12, 7.0, rgb("f0c14a"))
    elif kind == "flower":
        for i in range(5):
            ang = i * (2.0 * math.pi / 5.0) - 0.3
            volume_ball(
                dst,
                CX + math.cos(ang) * 28,
                y + 8 + math.sin(ang) * 16,
                12,
                12,
                rgb("f0b0c0"),
                width=3.0,
                spec=0.22,
                shininess=16.0,
                sss=0.20,
            )
        volume_ball(dst, CX, y + 8, 10, 10, rgb("f0c14a"), width=3.0, spec=0.30, shininess=20.0)
    return dst


def paint_wrap(kind: str, frame: int) -> np.ndarray:
    dst = blank()
    if kind == "none":
        return dst
    dy = hover_y(frame)
    y = CY + 78 + dy
    if kind == "chain":
        for i in range(7):
            volume_ball(dst, CX - 54 + i * 18, y + math.sin(i * 0.9) * 3, 8, 8, rgb("f0c14a"), width=2.8, spec=0.42, shininess=26.0, bump=None)
        volume_ball(dst, CX, y + 16, 11, 14, rgb("e8b44a"), width=3.2, spec=0.38, shininess=24.0, bump=None)
    elif kind == "scarf":
        volume_ball(dst, CX, y, 78, 16, rgb("e07028"), width=4.2, spec=0.16, shininess=12.0)
        volume_ball(dst, CX + 8, y + 6, 70, 10, rgb("2a2430"), width=3.4, spec=0.12, shininess=10.0)
        outlined_poly(
            dst,
            [(CX + 40, y + 4), (CX + 78, y + 36), (CX + 62, y + 44), (CX + 28, y + 12)],
            rgb("e07028"),
            width=3.6,
        )
    elif kind == "bowtie":
        volume_ball(dst, CX - 22, y - 4, 20, 14, rgb("6a3a8a"), width=3.6, spec=0.20, shininess=14.0)
        volume_ball(dst, CX + 22, y - 4, 20, 14, rgb("6a3a8a"), width=3.6, spec=0.20, shininess=14.0)
        volume_ball(dst, CX, y - 4, 9, 9, rgb("4a2e68"), width=3.0, spec=0.22, shininess=16.0)
    elif kind == "cape":
        volume_ball(dst, CX, y - 6, 72, 14, rgb("c43c3c"), width=4.2, spec=0.16, shininess=12.0)
        volume_ball(dst, CX, y + 2, 18, 10, rgb("f0c14a"), width=3.2, spec=0.34, shininess=22.0)
    elif kind == "pearls":
        for i in range(6):
            volume_ball(dst, CX - 48 + i * 19, y + math.sin(i * 0.8) * 2, 7.5, 7.5, rgb("f4efe6"), width=2.6, spec=0.46, shininess=28.0, bump=None)
    elif kind == "collar":
        volume_ball(dst, CX, y - 4, 70, 12, rgb("2a2430"), width=4.0, spec=0.12, shininess=10.0)
        volume_ball(dst, CX, y - 4, 8, 8, rgb("f0c14a"), width=2.8, spec=0.34, shininess=22.0)
    return dst


def paint_charm(kind: str, frame: int) -> np.ndarray:
    dst = blank()
    if kind == "none":
        return dst
    bob = hover_y(frame) + math.sin((frame + 3) / FRAMES * math.pi * 2.0) * 2.4
    if kind == "pumpkin":
        px, py = CX + 118, CY + 42 + bob
        volume_ball(dst, px, py, 22, 20, rgb("e07028"), width=3.8, spec=0.20, shininess=16.0)
        volume_ball(dst, px, py - 18, 6, 8, rgb("5a9a4a"), width=2.6, spec=0.14, shininess=12.0)
        disc(dst, px - 7, py - 2, 3.2, LINE, 0.9, soft=0.7)
        disc(dst, px + 7, py - 2, 3.2, LINE, 0.9, soft=0.7)
        ellipse(dst, px, py + 7, 6, 3, LINE, 0.85, soft=0.8)
    elif kind == "candy":
        px, py = CX - 118, CY + 36 + bob
        volume_ball(dst, px, py, 16, 16, rgb("f09098"), width=3.4, spec=0.24, shininess=18.0)
        outlined_poly(dst, [(px - 22, py - 8), (px - 14, py), (px - 22, py + 8), (px - 30, py)], rgb("fff6ef"), width=2.8)
        outlined_poly(dst, [(px + 22, py - 8), (px + 30, py), (px + 22, py + 8), (px + 14, py)], rgb("fff6ef"), width=2.8)
    elif kind == "bat":
        px, py = CX + 126, CY - 40 + bob
        volume_ball(dst, px, py, 13, 11, rgb("3a3448"), width=3.2, spec=0.12, shininess=10.0, sss=0.06)
        disc(dst, px - 4, py - 1, 2.4, rgb("fff6c8"), 0.9, soft=0.6)
        disc(dst, px + 4, py - 1, 2.4, rgb("fff6c8"), 0.9, soft=0.6)
        for side in (-1.0, 1.0):
            outlined_poly(
                dst,
                [
                    (px + side * 10, py),
                    (px + side * 38, py - 14),
                    (px + side * 28, py + 4),
                    (px + side * 40, py + 16),
                    (px + side * 10, py + 8),
                ],
                rgb("4a4458"),
                width=3.2,
            )
    elif kind == "broom":
        px, py = CX - 126, CY + 20 + bob
        fill_poly(dst, [(px - 4, py - 40), (px + 4, py - 40), (px + 3, py + 28), (px - 3, py + 28)], rgb("8a6a40"))
        volume_ball(dst, px, py + 36, 16, 12, rgb("c4a06a"), width=3.2, spec=0.14, shininess=10.0)
    elif kind == "corn":
        px, py = CX + 120, CY + 8 + bob
        volume_ball(dst, px, py - 10, 8, 8, rgb("f0c14a"), width=2.8, spec=0.24, shininess=16.0)
        volume_ball(dst, px, py, 9, 8, rgb("f09040"), width=2.8, spec=0.22, shininess=16.0)
        volume_ball(dst, px, py + 10, 8, 7, rgb("fff6ef"), width=2.8, spec=0.22, shininess=16.0)
    elif kind == "potion":
        px, py = CX - 120, CY + 8 + bob
        volume_ball(dst, px, py + 8, 14, 16, rgb("6aaa7a"), width=3.4, spec=0.28, shininess=22.0, sss=0.20)
        volume_ball(dst, px, py - 10, 8, 8, rgb("d8cfc4"), width=3.0, spec=0.20, shininess=14.0)
        disc(dst, px - 4, py + 2, 4, rgb("ffffff"), 0.35, soft=2.0)
    elif kind == "moon":
        px, py = CX + 118, CY - 48 + bob
        volume_ball(dst, px, py, 16, 16, rgb("f4e6b0"), width=3.4, spec=0.24, shininess=16.0)
        bite = np.sqrt((XX - (px + 7.0)) ** 2 + (YY - (py - 3.0)) ** 2)
        dst[..., 3] *= 1.0 - smoothstep(11.5, 8.5, bite)
    return dst


TRAIT_SPEC = {
    "night": [
        ("parchment", "Parchment", 14),
        ("pumpkin", "Pumpkin", 13),
        ("blush", "Blush", 12),
        ("midnight", "Midnight", 12),
        ("candy", "Candy", 11),
        ("fog", "Fog", 10),
        ("moss", "Graveyard", 9),
        ("dusk", "Dusk", 8),
        ("bloodmoon", "Blood Moon", 7),
        ("void", "Void", 4),
    ],
    "sheet": [
        ("classic", "Classic", 55),
        ("blush", "Blush", 28),
        ("void", "Void", 17),
    ],
    "mug": [
        ("blink", "Normal", 18),
        ("spooked", "Spooked", 16),
        ("blep", "Blep", 14),
        ("sleepy", "Sleepy", 12),
        ("wink", "Wink", 10),
        ("spark", "Sparkly", 9),
        ("angry", "Angry", 7),
        ("sad", "Sad", 6),
        ("starry", "Starry", 5),
        ("heart", "Heart", 3),
    ],
    "hat": [
        ("none", "None", 28),
        ("witch", "Witch", 12),
        ("bow", "Bow", 11),
        ("pumpkin", "Pumpkin", 10),
        ("cat", "Cat Ears", 9),
        ("flower", "Flower", 8),
        ("party", "Party", 7),
        ("halo", "Halo", 6),
        ("wizard", "Wizard", 5),
        ("crown", "Crown", 4),
    ],
    "wrap": [
        ("none", "None", 34),
        ("chain", "Chain", 16),
        ("scarf", "Scarf", 14),
        ("bowtie", "Bowtie", 12),
        ("pearls", "Pearls", 10),
        ("collar", "Collar", 8),
        ("cape", "Cape", 6),
    ],
    "charm": [
        ("none", "None", 32),
        ("pumpkin", "Pumpkin", 14),
        ("candy", "Candy", 13),
        ("bat", "Bat", 11),
        ("corn", "Candy Corn", 10),
        ("broom", "Broom", 8),
        ("potion", "Potion", 7),
        ("moon", "Moon", 5),
    ],
}

PAINTERS = {
    "night": {k: (lambda kind: (lambda frame, k=kind: paint_night(k, frame)))(k) for k in NIGHTS},
    "sheet": {k: (lambda kind: (lambda frame, k=kind: paint_sheet(k, frame)))(k) for k in SHEETS},
    "mug": {k: (lambda kind: (lambda frame, k=kind: paint_mug(k, frame)))(k) for k in MUGS},
    "hat": {k: (lambda kind: (lambda frame, k=kind: paint_hat(k, frame)))(k) for k in HATS},
    "wrap": {k: (lambda kind: (lambda frame, k=kind: paint_wrap(k, frame)))(k) for k in WRAPS},
    "charm": {k: (lambda kind: (lambda frame, k=kind: paint_charm(k, frame)))(k) for k in CHARMS},
}

STACK = ("night", "sheet", "mug", "hat", "wrap", "charm")

SIGNATURES = [
    {"night": "parchment", "sheet": "classic", "mug": "blink", "hat": "none", "wrap": "none", "charm": "none"},
    {"night": "pumpkin", "sheet": "blush", "mug": "heart", "hat": "bow", "wrap": "chain", "charm": "none"},
    {"night": "midnight", "sheet": "classic", "mug": "spooked", "hat": "witch", "wrap": "none", "charm": "pumpkin"},
    {"night": "candy", "sheet": "blush", "mug": "spark", "hat": "flower", "wrap": "scarf", "charm": "candy"},
    {"night": "dusk", "sheet": "void", "mug": "starry", "hat": "halo", "wrap": "none", "charm": "bat"},
    {"night": "fog", "sheet": "classic", "mug": "sleepy", "hat": "none", "wrap": "pearls", "charm": "none"},
    {"night": "bloodmoon", "sheet": "void", "mug": "wink", "hat": "pumpkin", "wrap": "chain", "charm": "broom"},
    {"night": "moss", "sheet": "classic", "mug": "blep", "hat": "cat", "wrap": "bowtie", "charm": "corn"},
    {"night": "void", "sheet": "void", "mug": "angry", "hat": "wizard", "wrap": "cape", "charm": "moon"},
    {"night": "blush", "sheet": "blush", "mug": "blink", "hat": "party", "wrap": "none", "charm": "potion"},
    {"night": "parchment", "sheet": "classic", "mug": "sad", "hat": "crown", "wrap": "collar", "charm": "none"},
    {"night": "pumpkin", "sheet": "classic", "mug": "spark", "hat": "witch", "wrap": "scarf", "charm": "bat"},
    {"night": "candy", "sheet": "blush", "mug": "wink", "hat": "bow", "wrap": "pearls", "charm": "candy"},
    {"night": "midnight", "sheet": "void", "mug": "spooked", "hat": "cat", "wrap": "chain", "charm": "pumpkin"},
    {"night": "dusk", "sheet": "classic", "mug": "heart", "hat": "flower", "wrap": "none", "charm": "moon"},
    {"night": "bloodmoon", "sheet": "blush", "mug": "blep", "hat": "pumpkin", "wrap": "cape", "charm": "broom"},
]

TRAIT_LABELS = (
    ("night", "Night"),
    ("sheet", "Sheet"),
    ("mug", "Mug"),
    ("hat", "Hat"),
    ("wrap", "Wrap"),
    ("charm", "Charm"),
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


def build_traits(only: str | None = None) -> None:
    TRAIT_DIR.mkdir(parents=True, exist_ok=True)
    for category, traits in TRAIT_SPEC.items():
        if only and category != only:
            continue
        for trait_id, _name, _rarity in traits:
            if trait_id == "none":
                continue
            print(f"  {category}/{trait_id}")
            save_apng(render_trait_frames(category, trait_id), trait_path(category, trait_id))
    manifest = {
        "name": "Halloween Shook'ums",
        "size": SIZE,
        "frames": FRAMES,
        "durationMs": DURATION_MS,
        "format": "apng",
        "loop": 0,
        "order": list(STACK),
        "note": "Each trait is a looping APNG. Studio stacks them live. Minted tokens flatten to GIF. Three sheet bodies share one skeleton; hats, wraps, and charms never edit the sheet.",
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
                "name": f"Shook'um #{index}",
                "image": f"/shookums-preview/{index}.gif",
                "attributes": [
                    {"trait_type": label, "value": name_of(key, selection[key])} for key, label in TRAIT_LABELS
                ],
            }
        )
    (PREVIEW_DIR / "samples.json").write_text(json.dumps(samples, indent=2) + "\n", encoding="utf-8")


COLLECTION_DESCRIPTION = (
    "Halloween Shook'ums is a 5,555-piece collection of looping sheet-ghost PFP GIFs. "
    "Each Shook'um is stacked from six layers — night, sheet, mug, hat, wrap, and charm — then flattened onto one 12-frame GIF. "
    "Three bodies. One locked skeleton. Hats sit on the crown. The sheet never changes shape."
)

COLLECTION_STORY = (
    "Halloween Shook'ums.\n\n"
    "A 5,555-piece collection of looping sheet-ghost PFP GIFs. "
    "Each Shook'um is stacked from six layers — night, sheet, mug, hat, wrap, and charm — then flattened onto one 12-frame GIF. "
    "Three sheets only: classic, blush, and void. The silhouette never gets a special cutout. "
    "Witch hats, pumpkin buckets, gold chains, and the occasional bat sit on the same crown, neck, and hands.\n\n"
    "Painted 3D clay — canvas grain, wrap shade, a warm key from the left. "
    "Spooked, sleepy, sparkly. One hem. One shared clock.\n\n"
    "Minting on Abstract (chain ID 2741). Gas is ETH."
)


def panoramic_wash(width: int, height: int) -> Image.Image:
    colors = [NIGHTS["midnight"], NIGHTS["dusk"], NIGHTS["pumpkin"], NIGHTS["blush"]]
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
    ImageDraw.Draw(shadow).rounded_rectangle((8, 14, size + 8, size + 18), radius=radius, fill=(28, 18, 40, 80))
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
    (META_DIR / "shookums-description.txt").write_text(COLLECTION_STORY + "\n", encoding="utf-8")
    (META_DIR / "shookums.json").write_text(
        json.dumps(
            {
                "name": "Halloween Shook'ums",
                "symbol": "SHOOK",
                "description": COLLECTION_DESCRIPTION,
                "image": "/brand/collection-shookums.gif",
                "featured_image": "/brand/featured-shookums.jpg",
                "banner_image": "/brand/banner-shookums.png",
                "opensea_banner_image": "/brand/banner-shookums-opensea.jpg",
                "external_link": "/shookums",
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
    logo_frames = compose_selection(SIGNATURES[2])

    logo = logo_frames[0].copy()
    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).ellipse((18, 18, SIZE - 18, SIZE - 18), fill=255)
    logo.putalpha(Image.composite(logo.split()[-1], Image.new("L", (SIZE, SIZE), 0), mask))
    ring = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse((10, 10, SIZE - 10, SIZE - 10), outline=(224, 112, 58, 230), width=10)
    logo = Image.alpha_composite(logo, ring)
    save_image(logo.resize((512, 512), Image.Resampling.LANCZOS), BRAND_DIR / "logo-shookums.png")
    save_apng(
        [frame.resize((512, 512), Image.Resampling.LANCZOS) for frame in logo_frames],
        BRAND_DIR / "logo-shookums-loop.png",
    )

    save_image(lineup_banner(1500, 560, portraits[:5]).convert("RGB"), BRAND_DIR / "banner-shookums.png", quality=94)
    save_image(lineup_banner(2800, 700, portraits).convert("RGB"), BRAND_DIR / "banner-shookums-opensea.jpg", quality=90)

    featured = panoramic_wash(1200, 800)
    place_portrait(featured, portraits[2], 90, 110, 560, radius=64)
    place_portrait(featured, portraits[1], 540, 130, 560, radius=64)
    save_image(featured.convert("RGB"), BRAND_DIR / "featured-shookums.jpg", quality=90)

    gif_frames = [frame.resize((1000, 1000), Image.Resampling.LANCZOS) for frame in logo_frames]
    save_loop_gif(gif_frames, BRAND_DIR / "collection-shookums.gif", DURATION_MS, colors=180)
    write_collection_meta()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--brand-only", action="store_true", help="Rebuild logo, banners, and listing copy")
    parser.add_argument("--hats-only", action="store_true", help="Rebuild hat layers, then samples and brand")
    args = parser.parse_args()
    if args.brand_only:
        print("Writing Halloween Shook'ums brand kit…")
        build_brand()
        print("Done.")
        return
    if args.hats_only:
        print("Rebuilding Halloween Shook'ums hat layers…")
        build_traits(only="hat")
        print("Compositing sample GIF tokens…")
        build_samples()
        print("Writing brand…")
        build_brand()
        print("Done.")
        return
    print("Building Halloween Shook'ums trait loops…")
    build_traits()
    print("Compositing sample GIF tokens…")
    build_samples()
    print("Writing brand…")
    build_brand()
    print("Done.")


if __name__ == "__main__":
    main()
