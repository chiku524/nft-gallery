#!/usr/bin/env python3
"""Paint Mochins — looping vinyl-toy mochi PFP layers for an OpenSea Drop on Shape.

Every trait is a 16-frame APNG on a shared 512 canvas and 100ms clock.
Vinyl, face, and topping share one idle bob so a stacked preview stays locked.
Stage, haze, and steam move on their own loops.

Look: gloss vinyl designer toys. Hard plastic. Tight spec. Clear coat. No outlines.
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

TRAIT_DIR = ROOT / "public" / "mochins-traits"
PREVIEW_DIR = ROOT / "public" / "mochins-preview"
BRAND_DIR = ROOT / "public" / "brand"
META_DIR = ROOT / "public" / "metadata"

SIZE = 512
FRAMES = 16
DURATION_MS = 100
H, W = SIZE, SIZE

YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)

KEY = np.array([-0.46, -0.64, 0.62], dtype=np.float32)
KEY /= float(np.linalg.norm(KEY))
FILL = np.array([0.58, 0.10, 0.38], dtype=np.float32)
FILL /= float(np.linalg.norm(FILL))
RIM = np.array([0.84, 0.16, 0.18], dtype=np.float32)
RIM /= float(np.linalg.norm(RIM))
VIEW = np.array([0.04, 0.06, 0.997], dtype=np.float32)
VIEW /= float(np.linalg.norm(VIEW))
HALF = KEY + VIEW
HALF /= float(np.linalg.norm(HALF))
WINDOW = np.array([0.62, -0.38, 0.69], dtype=np.float32)
WINDOW /= float(np.linalg.norm(WINDOW))
WINDOW_H = WINDOW + VIEW
WINDOW_H /= float(np.linalg.norm(WINDOW_H))


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
    if t.ndim == 2 and a.ndim == 3:
        t = t[..., None]
    return a * (1.0 - t) + b * t


def blank() -> np.ndarray:
    return np.zeros((H, W, 4), dtype=np.float32)


def over(dst: np.ndarray, src: np.ndarray) -> None:
    sa = src[..., 3:4]
    da = dst[..., 3:4]
    out_a = sa + da * (1.0 - sa)
    rgb_out = src[..., :3] * sa + dst[..., :3] * da * (1.0 - sa)
    dst[..., :3] = np.divide(rgb_out, out_a, out=np.zeros_like(rgb_out), where=out_a > 1e-6)
    dst[..., 3:4] = out_a


def shade(color: np.ndarray, t: float = 0.22) -> np.ndarray:
    return mix(color, rgb("120e0c"), t)


def lite(color: np.ndarray, t: float = 0.32) -> np.ndarray:
    return mix(color, rgb("ffffff"), t)


_GRAIN: dict[tuple[int, int], np.ndarray] = {}


def grain(seed: int, amp: float = 0.03) -> np.ndarray:
    key = (seed, int(amp * 1000))
    cached = _GRAIN.get(key)
    if cached is not None:
        return cached
    rng = np.random.default_rng(seed)
    small = (rng.random((SIZE // 14, SIZE // 14)) * 2 - 1).astype(np.float32)
    im = Image.fromarray(((small + 1) * 127.5).astype(np.uint8), "L")
    big = np.asarray(im.resize((W, H), Image.Resampling.BICUBIC), dtype=np.float32) / 127.5 - 1.0
    out = big * amp
    _GRAIN[key] = out
    return out


def ellipsoid(cx: float, cy: float, rx: float, ry: float, soft: float = 2.6) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    nx = (XX - cx) / max(rx, 1.0)
    ny = (YY - cy) / max(ry, 1.0)
    r2 = nx * nx + ny * ny
    nz = np.sqrt(np.maximum(0.0, 1.0 - r2))
    length = np.maximum(np.sqrt(nx * nx + ny * ny + nz * nz), 1e-6)
    nnx, nny, nnz = nx / length, ny / length, nz / length
    rad = np.sqrt(r2)
    edge = soft / max(min(rx, ry), 1.0)
    alpha = smoothstep(1.0 + edge, 1.0 - edge * 0.28, rad)
    return nnx, nny, nnz, alpha


def bump_normals(nx: np.ndarray, ny: np.ndarray, nz: np.ndarray, seed: int, amount: float = 0.07) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    bx = grain(seed, amount)
    by = grain(seed + 17, amount)
    nx = nx + bx
    ny = ny + by
    length = np.maximum(np.sqrt(nx * nx + ny * ny + nz * nz), 1e-6)
    return nx / length, ny / length, nz / length


def shade_rgb(
    albedo: np.ndarray,
    nx: np.ndarray,
    ny: np.ndarray,
    nz: np.ndarray,
    *,
    key_col: np.ndarray | None = None,
    fill_col: np.ndarray | None = None,
    rim_col: np.ndarray | None = None,
    ambient: float = 0.20,
    wrap: float = 0.20,
    spec: float = 0.48,
    shininess: float = 40.0,
    sss: float = 0.16,
    bounce: np.ndarray | None = None,
) -> np.ndarray:
    albedo = np.asarray(albedo, dtype=np.float32)
    if albedo.ndim == 1:
        albedo = np.broadcast_to(albedo, (H, W, 3)).copy()
    key_col = rgb("fff3e2") if key_col is None else key_col
    fill_col = rgb("6d7ea6") * 0.32 if fill_col is None else fill_col
    rim_col = rgb("ffe4bc") * 0.52 if rim_col is None else rim_col

    ndotk = nx * KEY[0] + ny * KEY[1] + nz * KEY[2]
    wrap_l = clamp01((ndotk + wrap) / (1.0 + wrap))
    ndotf = clamp01(nx * FILL[0] + ny * FILL[1] + nz * FILL[2])
    ndotr = clamp01(nx * RIM[0] + ny * RIM[1] + nz * RIM[2])
    ndotv = clamp01(nx * VIEW[0] + ny * VIEW[1] + nz * VIEW[2])
    ndoth = clamp01(nx * HALF[0] + ny * HALF[1] + nz * HALF[2])
    ndotw = clamp01(nx * WINDOW_H[0] + ny * WINDOW_H[1] + nz * WINDOW_H[2])
    spec_tight = np.power(ndoth, shininess * 1.45)
    spec_broad = np.power(ndoth, max(shininess * 0.20, 14.0))
    window = np.power(ndotw, max(shininess * 0.62, 22.0))
    fresnel = np.power(np.clip(1.0 - ndotv, 0.0, 1.0), 3.1)
    ao = clamp01(0.42 + 0.58 * nz - 0.22 * ny)
    sss_term = clamp01(-ndotk) * fresnel * sss
    coat = spec_tight * spec * 1.35 + spec_broad * spec * 0.18 + window * spec * 0.72 + fresnel * spec * 0.16
    # Gloss plastic: less diffuse so the clear coat can punch through light vinyl.
    kd = 1.0 - min(float(spec), 1.0) * 0.22

    lit = albedo * (ambient * ao)[..., None] * kd
    lit = lit + albedo * wrap_l[..., None] * key_col * kd
    lit = lit + albedo * ndotf[..., None] * fill_col * kd
    lit = lit + coat[..., None] * rgb("fffdf8")
    lit = lit + (fresnel * ndotr)[..., None] * rim_col
    lit = lit + sss_term[..., None] * mix(albedo, rgb("ffe0d0"), 0.18)
    if bounce is not None:
        lit = lit + albedo * clamp01(-ny)[..., None] * bounce * kd
    return np.clip(lit, 0.0, 1.0)


def blit_volume(dst: np.ndarray, albedo: np.ndarray, nx: np.ndarray, ny: np.ndarray, nz: np.ndarray, alpha: np.ndarray, **kwargs) -> None:
    layer = blank()
    layer[..., :3] = shade_rgb(albedo, nx, ny, nz, **kwargs)
    layer[..., 3] = np.clip(alpha, 0.0, 1.0)
    over(dst, layer)


def blit_soft(dst: np.ndarray, color: np.ndarray, alpha: np.ndarray) -> None:
    layer = blank()
    layer[..., :3] = color
    layer[..., 3] = np.clip(alpha, 0.0, 1.0)
    over(dst, layer)


def body_geo(frame: int) -> tuple[float, float, float, float]:
    t = 2.0 * math.pi * frame / FRAMES
    # Rigid vinyl — a shelf bob, no squash.
    lift = 3.2 * math.sin(t)
    return 256.0, 268.0 - lift, 176.0, 150.0


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

STAGES = {
    "cream": {
        "wall_top": rgb("f6eedc"),
        "wall_bot": rgb("e5d4ba"),
        "floor": rgb("d8c4a4"),
        "splash": rgb("fff6e6") * 0.22,
        "plate": rgb("f4eee4"),
        "plate_spec": 0.78,
        "plate_shiny": 72.0,
        "seed": 101,
    },
    "dusk": {
        "wall_top": rgb("3c3854"),
        "wall_bot": rgb("2a263c"),
        "floor": rgb("1e1b2c"),
        "splash": rgb("c8b4ff") * 0.16,
        "plate": rgb("8a8498"),
        "plate_spec": 0.68,
        "plate_shiny": 56.0,
        "seed": 202,
    },
    "matcha": {
        "wall_top": rgb("dce6c4"),
        "wall_bot": rgb("c4d2a4"),
        "floor": rgb("aeb888"),
        "splash": rgb("f0ffd4") * 0.16,
        "plate": rgb("c4a06a"),
        "plate_spec": 0.42,
        "plate_shiny": 28.0,
        "seed": 303,
    },
    "night": {
        "wall_top": rgb("1a1c26"),
        "wall_bot": rgb("12141c"),
        "floor": rgb("0c0d12"),
        "splash": rgb("8ab4ff") * 0.12,
        "plate": rgb("2c3038"),
        "plate_spec": 0.74,
        "plate_shiny": 80.0,
        "seed": 404,
    },
    "blush": {
        "wall_top": rgb("f4d4d0"),
        "wall_bot": rgb("e6b8b4"),
        "floor": rgb("d4a098"),
        "splash": rgb("ffe4e0") * 0.20,
        "plate": rgb("f6d8d2"),
        "plate_spec": 0.80,
        "plate_shiny": 76.0,
        "seed": 505,
    },
    "marble": {
        "wall_top": rgb("eceae6"),
        "wall_bot": rgb("d8d4ce"),
        "floor": rgb("c8c2ba"),
        "splash": rgb("ffffff") * 0.14,
        "plate": rgb("f2f0ec"),
        "plate_spec": 0.86,
        "plate_shiny": 90.0,
        "seed": 606,
    },
    "amber": {
        "wall_top": rgb("f0d8b0"),
        "wall_bot": rgb("d8b078"),
        "floor": rgb("c09458"),
        "splash": rgb("ffe8b0") * 0.20,
        "plate": rgb("c9a24a"),
        "plate_spec": 0.92,
        "plate_shiny": 110.0,
        "seed": 707,
    },
    "fog": {
        "wall_top": rgb("dce2ea"),
        "wall_bot": rgb("c4ccd6"),
        "floor": rgb("aeb6c2"),
        "splash": rgb("f0f6ff") * 0.16,
        "plate": rgb("e8eef4"),
        "plate_spec": 0.70,
        "plate_shiny": 64.0,
        "seed": 808,
    },
}

DOUGHS = {
    "snow": {"albedo": rgb("f3ece3"), "sss": 0.0, "spec": 1.06, "shininess": 200.0, "seed": 11},
    "matcha": {"albedo": rgb("4f9a32"), "sss": 0.0, "spec": 1.16, "shininess": 220.0, "seed": 22},
    "berry": {"albedo": rgb("e03a62"), "sss": 0.0, "spec": 1.18, "shininess": 216.0, "seed": 33},
    "sesame": {"albedo": rgb("1c1816"), "sss": 0.0, "spec": 1.28, "shininess": 240.0, "seed": 44},
    "yuzu": {"albedo": rgb("e8b428"), "sss": 0.0, "spec": 1.14, "shininess": 200.0, "seed": 55},
    "cocoa": {"albedo": rgb("6e3224"), "sss": 0.0, "spec": 1.18, "shininess": 224.0, "seed": 66},
    "taro": {"albedo": rgb("b46ac8"), "sss": 0.0, "spec": 1.20, "shininess": 212.0, "seed": 77},
}

HAZES = ("warm", "cool", "gold", "sakura")
FACES = ("blink", "wink", "sleepy", "grin", "pout", "spark", "heart", "wide")
TOPPINGS = ("leaf", "sesame", "drizzle", "berry", "kinako", "bow")
STEAMS = ("wisps", "puff", "sparkle")


def paint_stage(kind: str, frame: int) -> np.ndarray:
    spec = STAGES[kind]
    dst = blank()
    y = YY / float(H)
    wall = mix(spec["wall_top"], spec["wall_bot"], smoothstep(0.0, 0.64, y))
    floor_t = smoothstep(0.56, 0.78, y)
    color = mix(wall, spec["floor"], floor_t)
    cx = (XX - 256.0) / 290.0
    cy = (YY - 230.0) / 310.0
    vig = 1.0 - 0.24 * clamp01(cx * cx + cy * cy)
    color = color * vig[..., None]
    splash = np.exp(-((XX - 132.0) ** 2 + (YY - 88.0) ** 2) / (2.0 * 150.0**2))
    color = color + splash[..., None] * spec["splash"]
    color = color * (1.0 + grain(spec["seed"], 0.008)[..., None])
    dst[..., :3] = np.clip(color, 0.0, 1.0)
    dst[..., 3] = 1.0

    pulse = 0.94 + 0.06 * math.sin(2.0 * math.pi * frame / FRAMES)
    plate_n = grain(spec["seed"] + 3, 0.016)
    plate_alb = spec["plate"] * (1.0 + plate_n[..., None])
    if kind == "marble":
        veins = np.abs(grain(909, 0.9))
        plate_alb = mix(plate_alb, rgb("c8c4bc"), smoothstep(0.62, 0.86, veins))
    elif kind == "matcha":
        plate_alb = mix(plate_alb, rgb("8a6840"), clamp01(grain(310, 0.8) * 2.2 + 0.45))
    nx, ny, nz, a = ellipsoid(256.0, 406.0, 198.0, 40.0, soft=1.8)
    blit_volume(
        dst,
        plate_alb,
        nx,
        ny,
        nz,
        a,
        spec=spec["plate_spec"] * pulse,
        shininess=spec["plate_shiny"] * 1.25,
        sss=0.0,
        ambient=0.14,
        wrap=0.06,
    )
    nx2, ny2, nz2, a2 = ellipsoid(256.0, 400.0, 148.0, 22.0, soft=1.6)
    blit_volume(
        dst,
        shade(spec["plate"], 0.16),
        nx2,
        ny2,
        nz2,
        a2 * 0.90,
        spec=0.55,
        shininess=48.0,
        sss=0.0,
        ambient=0.12,
        wrap=0.04,
    )
    return dst


def paint_haze(kind: str, frame: int) -> np.ndarray:
    dst = blank()
    t = 2.0 * math.pi * frame / FRAMES
    drift = 10.0 * math.sin(t)
    if kind == "warm":
        color = rgb("ffd2a0")
        cx, cy, rx, ry = 150.0 + drift, 150.0, 210.0, 180.0
    elif kind == "cool":
        color = rgb("a8c8ff")
        cx, cy, rx, ry = 360.0 - drift, 140.0, 200.0, 170.0
    elif kind == "gold":
        color = rgb("ffd878")
        cx, cy, rx, ry = 256.0, 120.0 + drift * 0.4, 230.0, 150.0
    else:
        color = rgb("ffb8c8")
        cx, cy, rx, ry = 256.0 + drift, 160.0, 220.0, 190.0
    d = ((XX - cx) / rx) ** 2 + ((YY - cy) / ry) ** 2
    wash = np.exp(-d * 1.15) * (0.16 + 0.04 * math.sin(t + 0.6))
    blit_soft(dst, color, wash)

    rng = np.random.default_rng({"warm": 1, "cool": 2, "gold": 3, "sakura": 4}[kind])
    count = 18 if kind != "sakura" else 22
    for i in range(count):
        px = float(rng.uniform(40, 470))
        py = float(rng.uniform(30, 300)) + 8.0 * math.sin(t + i * 0.7)
        pr = float(rng.uniform(1.4, 3.6))
        op = float(rng.uniform(0.18, 0.55)) * (0.75 + 0.25 * math.sin(t + i))
        dist = np.sqrt((XX - px) ** 2 + (YY - py) ** 2)
        mote = smoothstep(pr + 1.6, pr - 0.4, dist) * op
        blit_soft(dst, lite(color, 0.45), mote)
    return dst


def paint_dough(kind: str, frame: int) -> np.ndarray:
    mat = DOUGHS[kind]
    dst = blank()
    cx, cy, rx, ry = body_geo(frame)
    # Hard contact shadow — the figure sits on the stand, it does not sink.
    shadow_y = cy + ry * 0.82
    _sx, sy, _sz, sa = ellipsoid(cx + 2.0, shadow_y, rx * 0.78, ry * 0.13, soft=5.0)
    blit_soft(dst, rgb("0c0a0a"), sa * (0.62 + 0.10 * (1.0 - sy)))

    nx, ny, nz, a = ellipsoid(cx, cy, rx, ry, soft=1.05)
    nx, ny, nz = bump_normals(nx, ny, nz, mat["seed"], 0.004)
    albedo = mat["albedo"] * (1.0 + grain(mat["seed"], 0.004)[..., None])
    blit_volume(
        dst,
        albedo,
        nx,
        ny,
        nz,
        a,
        spec=mat["spec"],
        shininess=mat["shininess"],
        sss=mat["sss"],
        bounce=rgb("d4cfc8") * 0.08,
        ambient=0.18,
        wrap=0.04,
    )
    # Molded equator seam — the two-part vinyl toy join.
    seam = smoothstep(0.055, 0.0, np.abs((YY - cy) / ry)) * a * 0.22
    blit_soft(dst, shade(mat["albedo"], 0.28), seam)
    # Key catchlight + elongated window reflection.
    hx = cx - rx * 0.28
    hy = cy - ry * 0.36
    _nx, _ny, _nz, ha = ellipsoid(hx, hy, rx * 0.13, ry * 0.08, soft=1.2)
    blit_soft(dst, rgb("ffffff"), ha * 0.78)
    wx = cx + rx * 0.22
    wy = cy - ry * 0.18
    _nx, _ny, _nz, wa = ellipsoid(wx, wy, rx * 0.20, ry * 0.055, soft=1.6)
    blit_soft(dst, rgb("eef4ff"), wa * 0.38)
    return dst


def add_eye(
    dst: np.ndarray,
    ex: float,
    ey: float,
    *,
    closed: bool = False,
    heart: bool = False,
    spark: bool = False,
    wide: bool = False,
) -> None:
    if closed:
        nx, ny, nz, a = ellipsoid(ex, ey + 2.0, 17.0, 3.4, soft=1.1)
        blit_volume(dst, rgb("2a2018"), nx, ny, nz, a, spec=0.12, shininess=16.0, sss=0.04, ambient=0.14)
        return
    erx, ery = (18.5, 19.5) if wide else (15.2, 16.4)
    nx, ny, nz, a = ellipsoid(ex, ey, erx, ery, soft=1.3)
    iris = rgb("3a1020") if heart else rgb("1a1410")
    blit_volume(dst, iris, nx, ny, nz, a, spec=0.98, shininess=160.0, sss=0.01, ambient=0.08, wrap=0.06)
    if heart:
        hx, hy, hz, ha = ellipsoid(ex, ey + 1.0, 7.4, 6.6, soft=1.0)
        blit_volume(dst, rgb("e24b6a"), hx, hy, hz, ha * 0.92, spec=0.6, shininess=40.0, sss=0.2)
    nxh, nyh, nzh, ah = ellipsoid(ex - 4.6, ey - 5.2, 4.8, 5.4, soft=0.7)
    blit_soft(dst, rgb("ffffff"), ah * 0.94)
    if spark or wide:
        nxs, nys, nzs, as_ = ellipsoid(ex + 4.2, ey + 3.4, 2.1, 2.3, soft=0.5)
        blit_soft(dst, rgb("fff6e8"), as_ * 0.8)


def paint_face(kind: str, frame: int) -> np.ndarray:
    dst = blank()
    cx, cy, rx, ry = body_geo(frame)
    t = 2.0 * math.pi * frame / FRAMES
    blink_shut = kind == "blink" and frame % FRAMES in (11, 12)
    wink_shut = kind == "wink" and frame % FRAMES in (8, 9, 10)
    sleepy = kind == "sleepy"
    wide = kind == "wide"
    heart = kind == "heart"
    spark = kind == "spark"

    # Cheeks sit on the front of the volume.
    for ox in (-58.0, 58.0):
        nx, ny, nz, a = ellipsoid(cx + ox, cy + 24.0, 24.0, 14.0, soft=9.0)
        blit_volume(dst, rgb("e87880"), nx, ny, nz, a * 0.34, spec=0.82, shininess=110.0, sss=0.0, ambient=0.12, wrap=0.04)

    ly = cy - 10.0 + (2.0 if sleepy else 0.0)
    add_eye(
        dst,
        cx - 40.0,
        ly,
        closed=blink_shut or sleepy or wink_shut,
        heart=heart,
        spark=spark,
        wide=wide,
    )
    add_eye(
        dst,
        cx + 40.0,
        ly,
        closed=blink_shut or sleepy,
        heart=heart,
        spark=spark,
        wide=wide,
    )

    if kind == "grin":
        nx, ny, nz, a = ellipsoid(cx, cy + 38.0, 28.0, 8.0, soft=1.6)
        blit_volume(dst, rgb("2a1c18"), nx, ny, nz, a, spec=0.2, shininess=18.0, sss=0.06)
        nx2, ny2, nz2, a2 = ellipsoid(cx, cy + 35.5, 22.0, 4.2, soft=1.2)
        blit_volume(dst, rgb("e87880"), nx2, ny2, nz2, a2 * 0.7, spec=0.35, shininess=24.0, sss=0.2)
    elif kind == "pout":
        nx, ny, nz, a = ellipsoid(cx, cy + 40.0, 11.0, 8.5, soft=1.4)
        blit_volume(dst, rgb("c45a62"), nx, ny, nz, a, spec=0.4, shininess=28.0, sss=0.22)
    elif kind == "wide":
        nx, ny, nz, a = ellipsoid(cx, cy + 40.0, 10.0, 11.0, soft=1.3)
        blit_volume(dst, rgb("2a1c18"), nx, ny, nz, a, spec=0.15, shininess=16.0)
    else:
        nx, ny, nz, a = ellipsoid(cx, cy + 38.0, 9.5 if sleepy else 12.0, 4.6, soft=1.3)
        blit_volume(dst, rgb("2a1c18"), nx, ny, nz, a, spec=0.16, shininess=16.0)

    if spark:
        star = blank()
        ang = t
        px = cx + 72.0 * math.cos(ang)
        py = cy - 48.0 + 10.0 * math.sin(ang * 2)
        dist = np.sqrt((XX - px) ** 2 + (YY - py) ** 2)
        blit_soft(star, rgb("fff2b0"), smoothstep(7.0, 1.5, dist) * 0.85)
        over(dst, star)
    return dst


def paint_topping(kind: str, frame: int) -> np.ndarray:
    dst = blank()
    cx, cy, rx, ry = body_geo(frame)
    crown_x = cx + 6.0
    crown_y = cy - ry * 0.78

    if kind == "leaf":
        nx, ny, nz, a = ellipsoid(crown_x + 18.0, crown_y + 4.0, 38.0, 16.0, soft=1.8)
        nx, ny, nz = bump_normals(nx, ny, nz, 81, 0.012)
        blit_volume(dst, rgb("4f9a32"), nx, ny, nz, a, spec=0.88, shininess=110.0, sss=0.03)
        nx2, ny2, nz2, a2 = ellipsoid(crown_x - 8.0, crown_y + 10.0, 28.0, 12.0, soft=1.6)
        blit_volume(dst, rgb("62b044"), nx2, ny2, nz2, a2, spec=0.86, shininess=100.0, sss=0.03)
        vein, _, _, va = ellipsoid(crown_x + 10.0, crown_y + 6.0, 24.0, 2.2, soft=0.8)
        blit_soft(dst, rgb("3e6428"), va * 0.45)
    elif kind == "sesame":
        rng = np.random.default_rng(19)
        for i in range(26):
            ang = float(rng.uniform(-2.2, 2.2))
            rad = float(rng.uniform(0.15, 0.78))
            px = cx + math.cos(ang) * rx * rad * 0.72
            py = cy - ry * (0.15 + 0.72 * math.cos(rad)) + float(rng.uniform(-6, 6))
            pr = float(rng.uniform(3.2, 5.4))
            tone = rgb("2a221c") if rng.random() > 0.22 else rgb("ebe2d2")
            nx, ny, nz, a = ellipsoid(px, py, pr, pr * 0.86, soft=0.8)
            blit_volume(dst, tone, nx, ny, nz, a, spec=0.92, shininess=140.0, sss=0.02, ambient=0.12)
    elif kind == "drizzle":
        for i, ox in enumerate((-36.0, -8.0, 22.0, 46.0)):
            nx, ny, nz, a = ellipsoid(cx + ox, cy - ry * 0.42 + i * 10.0, 16.0 - i, 46.0, soft=2.2)
            blit_volume(dst, rgb("5a2e1c"), nx, ny, nz, a * 0.88, spec=0.94, shininess=150.0, sss=0.02, ambient=0.10)
    elif kind == "berry":
        nx, ny, nz, a = ellipsoid(crown_x, crown_y + 2.0, 28.0, 26.0, soft=1.6)
        nx, ny, nz = bump_normals(nx, ny, nz, 44, 0.02)
        blit_volume(dst, rgb("e23a4a"), nx, ny, nz, a, spec=0.94, shininess=140.0, sss=0.03)
        nx2, ny2, nz2, a2 = ellipsoid(crown_x + 2.0, crown_y - 20.0, 6.0, 10.0, soft=1.0)
        blit_volume(dst, rgb("3e7a32"), nx2, ny2, nz2, a2, spec=0.82, shininess=90.0, sss=0.02)
    elif kind == "kinako":
        rng = np.random.default_rng(27)
        dust = blank()
        for i in range(40):
            px = cx + float(rng.uniform(-rx * 0.7, rx * 0.7))
            py = cy + float(rng.uniform(-ry * 0.7, ry * 0.15))
            pr = float(rng.uniform(2.0, 5.5))
            dist = np.sqrt((XX - px) ** 2 + (YY - py) ** 2)
            blit_soft(dust, rgb("e0c078"), smoothstep(pr + 1.8, pr - 0.6, dist) * float(rng.uniform(0.22, 0.55)))
        over(dst, dust)
    else:  # bow
        nx, ny, nz, a = ellipsoid(crown_x - 22.0, crown_y + 6.0, 24.0, 16.0, soft=1.5)
        blit_volume(dst, rgb("e85a6e"), nx, ny, nz, a, spec=0.90, shininess=120.0, sss=0.03)
        nx2, ny2, nz2, a2 = ellipsoid(crown_x + 22.0, crown_y + 6.0, 24.0, 16.0, soft=1.5)
        blit_volume(dst, rgb("e85a6e"), nx2, ny2, nz2, a2, spec=0.90, shininess=120.0, sss=0.03)
        nx3, ny3, nz3, a3 = ellipsoid(crown_x, crown_y + 8.0, 10.0, 10.0, soft=1.2)
        blit_volume(dst, rgb("c43a52"), nx3, ny3, nz3, a3, spec=0.92, shininess=130.0, sss=0.02)
    return dst


def paint_steam(kind: str, frame: int) -> np.ndarray:
    dst = blank()
    t = 2.0 * math.pi * frame / FRAMES
    rise = (frame / FRAMES) * 36.0
    if kind == "wisps":
        for i, ox in enumerate((-28.0, 0.0, 30.0)):
            px = 256.0 + ox + 10.0 * math.sin(t + i)
            py = 150.0 - rise * 0.55 + 8.0 * math.cos(t + i * 1.3)
            nx, ny, nz, a = ellipsoid(px, py, 18.0 + i * 2, 36.0, soft=10.0)
            blit_soft(dst, rgb("f6f2ea"), a * (0.16 + 0.05 * math.sin(t + i)))
    elif kind == "puff":
        px = 256.0 + 6.0 * math.sin(t)
        py = 128.0 - rise * 0.4
        nx, ny, nz, a = ellipsoid(px, py, 42.0, 28.0, soft=12.0)
        blit_volume(dst, rgb("f3efe6"), nx, ny, nz, a * 0.28, spec=0.2, shininess=18.0, sss=0.08, ambient=0.3)
        nx2, ny2, nz2, a2 = ellipsoid(px + 24.0, py - 18.0, 22.0, 16.0, soft=8.0)
        blit_volume(dst, rgb("f7f4ee"), nx2, ny2, nz2, a2 * 0.22, spec=0.18, shininess=16.0, ambient=0.3)
    else:
        rng = np.random.default_rng(5)
        for i in range(14):
            px = float(rng.uniform(90, 420))
            py = float(rng.uniform(40, 220)) - 12.0 * math.sin(t + i)
            pr = float(rng.uniform(1.6, 3.8))
            dist = np.sqrt((XX - px) ** 2 + (YY - py) ** 2)
            blit_soft(dst, rgb("fff4c8"), smoothstep(pr + 2.2, pr - 0.4, dist) * (0.35 + 0.25 * math.sin(t + i)))
    return dst


TRAIT_SPEC = {
    "stage": [
        ("cream", "Cream Cove", 14),
        ("dusk", "Dusk Cove", 12),
        ("matcha", "Matcha Cove", 14),
        ("night", "Night Cove", 10),
        ("blush", "Blush Cove", 14),
        ("marble", "Marble Cove", 12),
        ("amber", "Amber Cove", 12),
        ("fog", "Fog Cove", 12),
    ],
    "haze": [
        ("none", "No haze", 24),
        ("warm", "Warm Key", 20),
        ("cool", "Cool Rim", 20),
        ("gold", "Gold Motes", 18),
        ("sakura", "Sakura Dust", 18),
    ],
    "dough": [
        ("snow", "Snow", 20),
        ("matcha", "Matcha", 16),
        ("berry", "Berry", 16),
        ("sesame", "Sesame", 14),
        ("yuzu", "Yuzu", 12),
        ("cocoa", "Cocoa", 12),
        ("taro", "Taro", 10),
    ],
    "face": [
        ("blink", "Blink", 20),
        ("wink", "Wink", 14),
        ("sleepy", "Sleepy", 14),
        ("grin", "Grin", 14),
        ("pout", "Pout", 12),
        ("spark", "Spark", 12),
        ("heart", "Heart", 8),
        ("wide", "Wide", 6),
    ],
    "topping": [
        ("none", "Plain", 22),
        ("leaf", "Leaf", 16),
        ("sesame", "Sesame Dust", 16),
        ("drizzle", "Drizzle", 14),
        ("berry", "Berry", 12),
        ("kinako", "Kinako", 12),
        ("bow", "Bow", 8),
    ],
    "steam": [
        ("none", "Still", 28),
        ("wisps", "Wisps", 26),
        ("puff", "Puff", 24),
        ("sparkle", "Sparkle", 22),
    ],
}

PAINTERS = {
    "stage": {k: (lambda kind: (lambda frame, k=kind: paint_stage(k, frame)))(k) for k in STAGES},
    "haze": {k: (lambda kind: (lambda frame, k=kind: paint_haze(k, frame)))(k) for k in HAZES},
    "dough": {k: (lambda kind: (lambda frame, k=kind: paint_dough(k, frame)))(k) for k in DOUGHS},
    "face": {k: (lambda kind: (lambda frame, k=kind: paint_face(k, frame)))(k) for k in FACES},
    "topping": {k: (lambda kind: (lambda frame, k=kind: paint_topping(k, frame)))(k) for k in TOPPINGS},
    "steam": {k: (lambda kind: (lambda frame, k=kind: paint_steam(k, frame)))(k) for k in STEAMS},
}

STACK = ("stage", "haze", "dough", "face", "topping", "steam")

SIGNATURES = [
    {"stage": "cream", "haze": "warm", "dough": "snow", "face": "blink", "topping": "leaf", "steam": "wisps"},
    {"stage": "blush", "haze": "sakura", "dough": "berry", "face": "wink", "topping": "bow", "steam": "sparkle"},
    {"stage": "matcha", "haze": "gold", "dough": "matcha", "face": "grin", "topping": "sesame", "steam": "puff"},
    {"stage": "dusk", "haze": "cool", "dough": "taro", "face": "heart", "topping": "berry", "steam": "wisps"},
    {"stage": "night", "haze": "warm", "dough": "sesame", "face": "pout", "topping": "drizzle", "steam": "none"},
    {"stage": "marble", "haze": "none", "dough": "yuzu", "face": "sleepy", "topping": "kinako", "steam": "puff"},
    {"stage": "amber", "haze": "gold", "dough": "cocoa", "face": "wide", "topping": "leaf", "steam": "sparkle"},
    {"stage": "fog", "haze": "cool", "dough": "snow", "face": "spark", "topping": "none", "steam": "wisps"},
    {"stage": "cream", "haze": "none", "dough": "matcha", "face": "wink", "topping": "drizzle", "steam": "none"},
    {"stage": "blush", "haze": "warm", "dough": "cocoa", "face": "sleepy", "topping": "bow", "steam": "puff"},
    {"stage": "matcha", "haze": "sakura", "dough": "berry", "face": "pout", "topping": "sesame", "steam": "none"},
    {"stage": "dusk", "haze": "gold", "dough": "snow", "face": "spark", "topping": "leaf", "steam": "sparkle"},
    {"stage": "night", "haze": "cool", "dough": "taro", "face": "heart", "topping": "none", "steam": "wisps"},
    {"stage": "marble", "haze": "warm", "dough": "sesame", "face": "wide", "topping": "berry", "steam": "none"},
    {"stage": "amber", "haze": "none", "dough": "yuzu", "face": "blink", "topping": "kinako", "steam": "puff"},
    {"stage": "fog", "haze": "sakura", "dough": "matcha", "face": "grin", "topping": "bow", "steam": "sparkle"},
]

TRAIT_LABELS = (
    ("stage", "Stage"),
    ("haze", "Haze"),
    ("dough", "Vinyl"),
    ("face", "Face"),
    ("topping", "Topping"),
    ("steam", "Steam"),
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
        "name": "Mochins",
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
        save_loop_gif(frames, PREVIEW_DIR / f"{index}.gif", DURATION_MS, colors=180)
        samples.append(
            {
                "id": index,
                "name": f"Mochin #{index}",
                "image": f"/mochins-preview/{index}.gif",
                "attributes": [
                    {"trait_type": label, "value": name_of(key, selection[key])} for key, label in TRAIT_LABELS
                ],
            }
        )
    (PREVIEW_DIR / "samples.json").write_text(json.dumps(samples, indent=2) + "\n", encoding="utf-8")


COLLECTION_DESCRIPTION = (
    "Mochins is a 4,000-piece collection of looping vinyl-toy mochi PFP GIFs on Shape. "
    "Each figure is stacked from six layers — stage, haze, vinyl, face, topping, and steam — "
    "then flattened onto one 16-frame GIF. Gloss plastic. Tight spec. Clear coat. "
    "No outlines. Collector-shelf light. The vinyl idles."
)

COLLECTION_STORY = (
    "Mochins never sit still.\n\n"
    "A 4,000-piece collection of looping vinyl-toy mochi PFP GIFs on Shape. "
    "Each Mochin is stacked from six layers — stage, haze, vinyl, face, topping, and steam — "
    "then flattened onto one 16-frame GIF. Lacquered stands. Ivory, matcha, and black vinyl. "
    "Studio key light. A hard highlight. Shelf glitter in the air.\n\n"
    "Designer-toy daifuku with volume, rim light, and a planted contact shadow. No outlines. One shared clock.\n\n"
    "Minting on Shape (chain ID 360). Gas is ETH."
)


def panoramic_wash(width: int, height: int, frame: int = 0) -> Image.Image:
    left = np.asarray(to_image(paint_stage("night", frame)).resize((width, height), Image.Resampling.LANCZOS), dtype=np.float32)
    mid = np.asarray(to_image(paint_stage("cream", frame)).resize((width, height), Image.Resampling.LANCZOS), dtype=np.float32)
    right = np.asarray(to_image(paint_stage("matcha", frame)).resize((width, height), Image.Resampling.LANCZOS), dtype=np.float32)
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
    ImageDraw.Draw(shadow).rounded_rectangle((8, 14, size + 8, size + 18), radius=radius, fill=(28, 18, 12, 90))
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
    (META_DIR / "mochins-description.txt").write_text(COLLECTION_STORY + "\n", encoding="utf-8")
    (META_DIR / "mochins.json").write_text(
        json.dumps(
            {
                "name": "Mochins",
                "symbol": "MOCHI",
                "description": COLLECTION_DESCRIPTION,
                "image": "/brand/collection-mochins.gif",
                "featured_image": "/brand/featured-mochins.jpg",
                "banner_image": "/brand/banner-mochins.png",
                "opensea_banner_image": "/brand/banner-mochins-opensea.jpg",
                "external_link": "/mochins",
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
    ImageDraw.Draw(ring).ellipse((10, 10, SIZE - 10, SIZE - 10), outline=(196, 120, 74, 230), width=10)
    logo = Image.alpha_composite(logo, ring)
    save_image(logo.resize((512, 512), Image.Resampling.LANCZOS), BRAND_DIR / "logo-mochins.png")
    save_apng(
        [frame.resize((512, 512), Image.Resampling.LANCZOS) for frame in logo_frames],
        BRAND_DIR / "logo-mochins-loop.png",
    )

    site_banner = lineup_banner(1500, 560, portraits[:5])
    save_image(site_banner.convert("RGB"), BRAND_DIR / "banner-mochins.png", quality=94)

    opensea_banner = lineup_banner(2800, 700, portraits)
    save_image(opensea_banner.convert("RGB"), BRAND_DIR / "banner-mochins-opensea.jpg", quality=90)

    featured = panoramic_wash(1200, 800, frame=8)
    place_portrait(featured, portraits[0], 90, 110, 560, radius=64)
    place_portrait(featured, portraits[2], 540, 130, 560, radius=64)
    save_image(featured.convert("RGB"), BRAND_DIR / "featured-mochins.jpg", quality=90)

    gif_frames = [frame.resize((1000, 1000), Image.Resampling.LANCZOS) for frame in logo_frames]
    save_loop_gif(gif_frames, BRAND_DIR / "collection-mochins.gif", DURATION_MS, colors=180)
    write_collection_meta()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--brand-only", action="store_true", help="Rebuild logo, banners, and listing copy")
    args = parser.parse_args()
    if args.brand_only:
        print("Writing Mochins brand kit…")
        build_brand()
        print("Done.")
        return
    print("Building Mochins trait loops…")
    build_traits()
    print("Compositing sample GIF tokens…")
    build_samples()
    print("Writing brand…")
    build_brand()
    print("Done.")


if __name__ == "__main__":
    main()
