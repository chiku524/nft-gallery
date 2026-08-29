#!/usr/bin/env python3
"""Bake overlay traits so studio/generator match gallery layering.

Gallery stack (back to front):
  background → clothes → hat → pug → hat brim → wall → hanging straps →
  stoop props → paws

The pug sheets ship with a baked concrete wall. This script knocks that
wall out, extracts paws, aligns every ledge to the same rim, and places
hats/clothes at gallery scale instead of squashing them onto the wall.
"""

from __future__ import annotations

import shutil
import time
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
TRAITS = ROOT / "public" / "traits"
SRC = ROOT / "public" / "traits-source"
GALLERY = ROOT / "public" / "gallery"
SIZE = 1024
WALL_TOP = 629
# Snout / mouth stay clear. Clothes may sit on the jowls under the chin.
SNOUT_TOP_Y = 505
SNOUT_BOTTOM_Y = 586
SNOUT_X0, SNOUT_X1 = 445, 590


def load_src(rel: str) -> Image.Image:
    path = SRC / rel
    if not path.exists():
        path = TRAITS / rel
    return Image.fromarray(clear_transparent(np.array(Image.open(path).convert("RGBA"))))


def load_trait(rel: str) -> Image.Image:
    return Image.open(TRAITS / rel).convert("RGBA")


def arr(im: Image.Image) -> np.ndarray:
    return np.array(im)


def save(rel: str, im: Image.Image) -> None:
    path = TRAITS / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp.png")
    im.save(tmp)
    last_err: OSError | None = None
    for _ in range(8):
        try:
            tmp.replace(path)
            last_err = None
            break
        except OSError as err:
            last_err = err
            time.sleep(0.15)
    if last_err is not None:
        raise last_err
    a = arr(im)
    ys, xs = np.where(a[:, :, 3] > 20)
    bbox = (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())) if xs.size else None
    print(f"wrote {rel:36} opaque={(a[:,:,3]>20).mean()*100:5.1f}% bbox={bbox}")


def blank() -> Image.Image:
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))


def clear_transparent(a: np.ndarray) -> np.ndarray:
    trans = a[..., 3] == 0
    a[trans, 0] = 0
    a[trans, 1] = 0
    a[trans, 2] = 0
    return a


def neighbors8(mask: np.ndarray) -> np.ndarray:
    out = np.zeros_like(mask)
    out[1:, :] |= mask[:-1, :]
    out[:-1, :] |= mask[1:, :]
    out[:, 1:] |= mask[:, :-1]
    out[:, :-1] |= mask[:, 1:]
    out[1:, 1:] |= mask[:-1, :-1]
    out[1:, :-1] |= mask[:-1, 1:]
    out[:-1, 1:] |= mask[1:, :-1]
    out[:-1, :-1] |= mask[1:, 1:]
    return out


def flood_from_edges(open_mask: np.ndarray) -> np.ndarray:
    h, w = open_mask.shape
    visited = np.zeros((h, w), dtype=bool)
    q: deque[tuple[int, int]] = deque()

    def push(y: int, x: int) -> None:
        if 0 <= y < h and 0 <= x < w and open_mask[y, x] and not visited[y, x]:
            visited[y, x] = True
            q.append((y, x))

    for x in range(w):
        push(0, x)
        push(h - 1, x)
    for y in range(h):
        push(y, 0)
        push(y, w - 1)
    while q:
        y, x = q.popleft()
        push(y - 1, x)
        push(y + 1, x)
        push(y, x - 1)
        push(y, x + 1)
    return visited


def seal_interior(im: Image.Image, hole_thresh: int = 96, knock_backdrop: bool = False) -> Image.Image:
    a = arr(im).copy()
    alpha = a[:, :, 3]
    openp = alpha < hole_thresh
    backdrop = flood_from_edges(openp)
    enclosed = openp & ~backdrop
    interior = ~backdrop
    near_bg = np.array(Image.fromarray((backdrop.astype(np.uint8) * 255)).filter(ImageFilter.MaxFilter(3))) > 0
    body = interior & ~near_bg
    if knock_backdrop:
        a[backdrop & openp, 3] = 0
    a[enclosed, 3] = 255
    mid = body & (a[:, :, 3] > 0) & (a[:, :, 3] < 255)
    a[mid, 3] = 255
    return Image.fromarray(a)


def seal_alpha(im: Image.Image) -> Image.Image:
    a = arr(im).astype(np.uint8)
    a[a[:, :, 3] > 90, 3] = 255
    return Image.fromarray(a)


GHOST_ALPHA = 32


def _neighbor_count(mask: np.ndarray) -> np.ndarray:
    count = np.zeros(mask.shape, dtype=np.uint8)
    count[1:, :] += mask[:-1, :]
    count[:-1, :] += mask[1:, :]
    count[:, 1:] += mask[:, :-1]
    count[:, :-1] += mask[:, 1:]
    count[1:, 1:] += mask[:-1, :-1]
    count[1:, :-1] += mask[:-1, 1:]
    count[:-1, 1:] += mask[1:, :-1]
    count[:-1, :-1] += mask[1:, 1:]
    return count


def inpaint_enclosed(a: np.ndarray) -> np.ndarray:
    """Fill pinholes that are trapped inside fabric, not openings that reach the canvas edge."""
    openp = a[:, :, 3] < GHOST_ALPHA
    holes = openp & ~flood_from_edges(openp)
    if not holes.any():
        return a
    out = a.copy()
    todo = holes.copy()
    for _ in range(16):
        if not todo.any():
            break
        solid = out[:, :, 3] >= 200
        painted = np.zeros_like(todo)
        for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            src_solid = np.roll(solid, (dy, dx), axis=(0, 1))
            src = np.roll(out, (dy, dx), axis=(0, 1))
            take = todo & src_solid
            out[take] = src[take]
            painted |= take
        todo &= ~painted
    out[holes, 3] = 255
    return out


def strip_edge_fringe(a: np.ndarray, *, keep_light: bool = False) -> np.ndarray:
    """Drop pale sticker-white sitting on the silhouette edge."""
    rgb = a[:, :, :3].astype(np.int16)
    lum = rgb.mean(axis=2)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    op = a[:, :, 3] > GHOST_ALPHA
    edge = op & neighbors8(~op)
    pale = edge & (lum > 200) & (chroma < 55)
    if keep_light:
        ys = np.where(op)[0]
        if ys.size:
            pale &= np.arange(SIZE)[:, None] >= int(ys.max()) - 18
    a[pale, 3] = 0
    return a


def drop_islands(a: np.ndarray, min_px: int = 18) -> np.ndarray:
    """Delete leftover specks that are not attached to the main silhouette."""
    op = a[:, :, 3] > GHOST_ALPHA
    if not op.any():
        return a
    visited = np.zeros(op.shape, dtype=bool)
    keep = np.zeros_like(op)
    h, w = op.shape
    ys, xs = np.where(op)
    for y, x in zip(ys.tolist(), xs.tolist()):
        if visited[y, x]:
            continue
        q = deque([(y, x)])
        visited[y, x] = True
        cells: list[tuple[int, int]] = []
        while q:
            cy, cx = q.popleft()
            cells.append((cy, cx))
            for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                if 0 <= ny < h and 0 <= nx < w and op[ny, nx] and not visited[ny, nx]:
                    visited[ny, nx] = True
                    q.append((ny, nx))
        if len(cells) >= min_px:
            for cy, cx in cells:
                keep[cy, cx] = True
    a[~keep, 3] = 0
    return a


def harden_overlay(
    im: Image.Image,
    *,
    fill_holes: bool = True,
    keep_light: bool = False,
    drop_specks: bool = False,
) -> Image.Image:
    """Make overlay traits solid: no ghost fringe, no salt-and-pepper holes."""
    a = arr(im).copy()
    a[a[:, :, 3] <= GHOST_ALPHA] = 0
    if fill_holes:
        a = inpaint_enclosed(a)
    if drop_specks:
        a = drop_islands(a)
    body = a[:, :, 3] > GHOST_ALPHA
    lonely = body & (_neighbor_count(body) < 2)
    a[lonely, 3] = 0
    a = strip_edge_fringe(a, keep_light=keep_light)
    a[a[:, :, 3] <= GHOST_ALPHA] = 0
    a[a[:, :, 3] > GHOST_ALPHA, 3] = 255
    return Image.fromarray(clear_transparent(a))


def grow(mask: np.ndarray, px: int = 3) -> np.ndarray:
    img = Image.fromarray((mask.astype(np.uint8) * 255))
    img = img.filter(ImageFilter.MaxFilter(px * 2 + 1))
    return np.array(img) > 0


def content_bbox(a: np.ndarray, thresh: int = 18) -> tuple[int, int, int, int]:
    ys, xs = np.where(a[:, :, 3] > thresh)
    if xs.size == 0:
        raise ValueError("empty layer")
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def crop_content(im: Image.Image, pad: int = 2) -> Image.Image:
    a = arr(im)
    x0, y0, x1, y1 = content_bbox(a)
    x0 = max(0, x0 - pad)
    y0 = max(0, y0 - pad)
    x1 = min(a.shape[1], x1 + pad)
    y1 = min(a.shape[0], y1 + pad)
    return Image.fromarray(a[y0:y1, x0:x1])


def paste_centered(canvas: Image.Image, overlay: Image.Image, cx: float, cy: float) -> None:
    x = int(cx - overlay.width / 2)
    y = int(cy - overlay.height / 2)
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ox, oy = overlay.size
    src_x, src_y = max(0, -x), max(0, -y)
    dst_x, dst_y = max(0, x), max(0, y)
    width = min(ox - src_x, canvas.width - dst_x)
    height = min(oy - src_y, canvas.height - dst_y)
    if width <= 0 or height <= 0:
        return
    cropped = overlay.crop((src_x, src_y, src_x + width, src_y + height))
    layer.paste(cropped, (dst_x, dst_y), cropped)
    canvas.alpha_composite(layer)


def paste_box(
    src: Image.Image,
    box: tuple[int, int, int, int],
    anchor: str = "center",
    mode: str = "contain",
) -> Image.Image:
    x, y, w, h = box
    cropped = crop_content(src)
    if mode == "fill":
        fitted = cropped.resize((w, h), Image.Resampling.LANCZOS)
        nw, nh = w, h
    else:
        scale = min(w / cropped.width, h / cropped.height)
        nw = max(1, int(cropped.width * scale))
        nh = max(1, int(cropped.height * scale))
        fitted = cropped.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = blank()
    if anchor == "bottom":
        px = x + (w - nw) // 2
        py = y + h - nh
    elif anchor == "top":
        px = x + (w - nw) // 2
        py = y
    else:
        px = x + (w - nw) // 2
        py = y + (h - nh) // 2
    canvas.paste(fitted, (px, py), fitted)
    return seal_alpha(canvas)


def fit_width(im: Image.Image, width: int, max_height: int | None = None) -> Image.Image:
    cropped = Image.fromarray(clear_transparent(arr(crop_content(im))))
    height = max(1, round(cropped.height * (width / cropped.width)))
    if max_height is not None and height > max_height:
        height = max_height
        width = max(1, round(cropped.width * (height / cropped.height)))
    return resize_rgba(cropped, (width, height))


def resize_rgba(im: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Premultiplied resize so transparent black cannot bleed into fabric."""
    a = arr(im).astype(np.float32)
    alpha = a[:, :, 3:4] / 255.0
    a[:, :, :3] *= alpha
    resized = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA").resize(
        size, Image.Resampling.LANCZOS
    )
    r = arr(resized).astype(np.float32)
    al = r[:, :, 3:4]
    r[:, :, :3] = np.where(al > 0, r[:, :, :3] * 255.0 / np.maximum(al, 1.0), 0)
    return Image.fromarray(np.clip(r, 0, 255).astype(np.uint8))


BASE_RELS = (
    "base/base-fawn-peek.png",
    "base/base-cream-peek.png",
    "base/base-black-peek.png",
)

BLOCK_RELS = (
    "block/block-concrete.png",
    "block/block-brownstone.png",
    "block/block-crate.png",
    "block/block-gold.png",
)

FACE_ACCESSORIES = {"sunglasses", "monocle"}
LEDGE_ACCESSORIES = {"coffee", "bone", "blocks"}


def cache_source(rel: str) -> None:
    dest = SRC / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        return
    shutil.copy(TRAITS / rel, dest)
    print("cached source", rel)


def ensure_sources() -> None:
    """Keep wall-baked pugs and original ledges so this script can rerun."""
    for rel in BASE_RELS + BLOCK_RELS:
        cache_source(rel)


def sealed_source_base(rel: str) -> Image.Image:
    return seal_interior(load_src(rel))


def seal_bases() -> None:
    ensure_sources()
    for rel in BASE_RELS:
        im = sealed_source_base(rel)
        a = arr(im)
        print("sealed", rel, "forehead", tuple(int(v) for v in a[280, 512]))


def extract_paws(pug: Image.Image) -> Image.Image:
    data = arr(pug)
    rgb = data[:, :, :3].astype(np.int16)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    lum = rgb.mean(axis=2)
    alpha = data[:, :, 3] > 12
    rows = np.arange(SIZE)[:, None]
    cols = np.arange(SIZE)[None, :]
    wallish = (chroma <= 24) & (lum >= 70) & (lum <= 220) & (rows >= WALL_TOP - 6)
    seed = np.zeros((SIZE, SIZE), dtype=bool)
    seed[604 : WALL_TOP + 10, 248:412] = alpha[604 : WALL_TOP + 10, 248:412]
    seed[604 : WALL_TOP + 10, 628:800] = alpha[604 : WALL_TOP + 10, 628:800]
    seed &= ~wallish
    walk = alpha & ~wallish
    walk[:, 430:605] = False
    filled = seed.copy()
    for _ in range(16):
        nxt = neighbors8(filled) & walk & ~filled
        nxt[:598] = False
        nxt[654:] = False
        if not nxt.any():
            break
        filled |= nxt
    outline = alpha & (lum < 60) & ~wallish & (rows >= 598) & (rows <= 652)
    filled |= neighbors8(filled) & outline
    filled &= ~((cols >= 430) & (cols <= 605))
    filled[:598] = False
    filled[654:] = False
    out = np.zeros_like(data)
    out[filled] = data[filled]
    return Image.fromarray(clear_transparent(out))


def wall_mask(pug: np.ndarray) -> np.ndarray:
    rgb = pug[:, :, :3].astype(np.int16)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    lum = rgb.mean(axis=2)
    rows = np.arange(SIZE)[:, None]
    return (
        (pug[:, :, 3] > 12)
        & (rows >= WALL_TOP)
        & (chroma <= 30)
        & (lum >= 70)
        & (lum <= 210)
    )


def knock_wall_and_paws(pug: Image.Image, paws: Image.Image) -> Image.Image:
    """Remove the baked ledge only. Keep chin and chest so clothes holes stay filled."""
    data = arr(pug).copy()
    paw = arr(paws)[:, :, 3] > 12
    wall = wall_mask(data)
    data[paw | wall, 3] = 0
    # Dark grout fails the gray wall mask and otherwise leaves a thick rim.
    data[WALL_TOP:, :, 3] = 0
    return Image.fromarray(clear_transparent(data))


def extract_default_wall(pug: Image.Image, paws: Image.Image) -> Image.Image:
    data = arr(pug).copy()
    keep = wall_mask(data)
    paw = arr(paws)[:, :, 3] > 12
    keep &= ~paw
    out = np.zeros_like(data)
    out[keep] = data[keep]
    return Image.fromarray(clear_transparent(out))


def align_top(im: Image.Image, top: int) -> Image.Image:
    data = arr(im)
    ys, _xs = np.where(data[:, :, 3] > 12)
    if ys.size == 0:
        return im
    shift = top - int(ys.min())
    if shift == 0:
        return im
    canvas = blank()
    paste_centered(canvas, im, im.width / 2, im.height / 2 + shift)
    return canvas


def punch_paws(block: Image.Image, paws: Image.Image) -> Image.Image:
    return punch_mask(block, paws, dilate=6)


def punch_mask(overlay: Image.Image, mask_src: Image.Image, dilate: int = 3) -> Image.Image:
    overlay_arr = arr(overlay.convert("RGBA"))
    mask = arr(mask_src.convert("RGBA"))[:, :, 3] > 12
    for _ in range(dilate):
        mask = mask | neighbors8(mask)
    overlay_arr[mask, 3] = 0
    return Image.fromarray(clear_transparent(overlay_arr))


def split_bases() -> Image.Image:
    """Knock the baked wall out of each pug and save paws + default ledge."""
    paw_union = blank()
    for rel, color in (
        ("base/base-fawn-peek.png", "fawn"),
        ("base/base-cream-peek.png", "cream"),
        ("base/base-black-peek.png", "black"),
    ):
        pug = sealed_source_base(rel)
        paws = extract_paws(pug)
        save(f"base/front-paws-{color}.png", paws)
        paw_union = Image.alpha_composite(paw_union, paws)
        if color == "fawn":
            save("base/wall-default.png", extract_default_wall(pug, paws))
        save(rel, knock_wall_and_paws(pug, paws))
    return paw_union


def fit_blocks(paws: Image.Image) -> None:
    """Keep the pug's natural cap so paws sit on a ledge, not a cut face."""
    del paws
    for rel in BLOCK_RELS:
        save(rel, darken_wall(align_top(load_src(rel), WALL_TOP)))
    save("base/wall-default.png", darken_wall(load_trait("base/wall-default.png")))


def darken_wall(im: Image.Image, factor: float = 0.80) -> Image.Image:
    """Gallery ledges are a darker, grittier gray than the baked pug sheet."""
    a = arr(im).copy()
    op = a[:, :, 3] > 20
    rgb = a[:, :, :3].astype(np.float32)
    rgb[op] = np.clip(rgb[op] * factor, 0, 255)
    lum = rgb.mean(axis=2)
    rows = np.arange(SIZE)[:, None]
    ys = np.where(op.any(axis=1))[0]
    if ys.size:
        cap = op & (rows < int(ys.min()) + 22) & (lum > 130)
        rgb[cap] = np.clip(rgb[cap] * 0.86, 0, 255)
    a[:, :, :3] = rgb
    return Image.fromarray(a)


def ledge_face_top(im: Image.Image) -> int:
    """First full-width row that is the vertical wall face, not the top-down cap."""
    a = arr(im)
    for y in range(SIZE):
        opaque = a[y, :, 3] > 20
        if opaque.mean() < 0.65:
            continue
        lum = float(a[y, opaque, :3].mean())
        if lum < 150:
            return y
    ys, _ = np.where(a[:, :, 3] > 20)
    return int(ys.min()) if ys.size else WALL_TOP


def flatten_ledge(im: Image.Image, top: int = WALL_TOP) -> Image.Image:
    """Drop the looking-down cap so paws grip a thin rim, like the gallery paintings."""
    face = ledge_face_top(im)
    data = arr(im).copy()
    if face > top:
        data[:face, :, 3] = 0
    return align_top(Image.fromarray(clear_transparent(data)), top)


def load_gallery(name: str) -> np.ndarray:
    return np.array(Image.open(GALLERY / name).convert("RGB"))


def layer_from_mask(rgb: np.ndarray, seed: np.ndarray, grow_px: int = 4) -> Image.Image:
    """Keep seed pixels plus touching ink outlines and sticker white."""
    lum = rgb.mean(axis=2)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    outline = (lum < 55) & (chroma < 50)
    white = (lum > 210) & (chroma < 40)
    filled = seed.copy()
    for _ in range(grow_px):
        filled |= neighbors8(filled) & (outline | white | seed)
    out = np.zeros((SIZE, SIZE, 4), np.uint8)
    out[filled, :3] = rgb[filled]
    out[filled, 3] = 255
    im = seal_interior(Image.fromarray(out), knock_backdrop=True)
    if (arr(im)[:, :, 3] > 20).mean() < 0.002:
        raise RuntimeError("gallery extract too thin")
    return im


def place_bottom(
    im: Image.Image,
    width: int,
    bottom_y: float,
    cx: float = 530,
    max_height: int | None = None,
) -> Image.Image:
    fitted = fit_width(im, width, max_height)
    canvas = blank()
    paste_centered(canvas, fitted, cx, bottom_y - fitted.height / 2)
    return seal_alpha(canvas)


def extract_dressed_hat(dressed_rel: str, kind: str, bottom: int) -> Image.Image:
    """Pull the on-head hat off the dressed sheet, including brim, ink, and sticker white."""
    dressed = arr(load_trait(dressed_rel))
    rgb = dressed[:, :, :3].astype(np.int16)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    y = np.arange(SIZE)[:, None]
    x = np.arange(SIZE)[None, :]
    above = y < bottom
    alpha = dressed[:, :, 3] > 24
    lum = rgb.mean(axis=2)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)

    fur = (r > 170) & (g > 140) & (b > 100) & (chroma < 90)
    cream_panel = (y < 310) & (x > 370) & (x < 690) & (r > 155) & (g > 130) & (b > 100)
    fur = fur & ~cream_panel
    if kind == "beanie":
        color = (g > r + 10) & (g > b + 4) & (g > 25) & (y < 400) & ~fur
    elif kind == "crown":
        gold = (r > 130) & (g > 90) & (b < 110) & (r + g > 2 * b + 10)
        gems = (r > 120) & (g < 110) & (b < 110) & (r > g + 30)
        color = (gold | gems) & (y < 320)
    elif kind == "hardhat":
        # Bright dome plus the darker orange brim. Keep y low so wall yellow stays out.
        color = (r > 120) & (g > 70) & (b < 120) & (r > b + 30) & (g > b) & (chroma > 45) & ~fur
    elif kind == "newsie":
        color = (
            (r > 80)
            & (g > 40)
            & (b < 70)
            & (r > b + 24)
            & (g > b + 10)
            & (r < 175)
            & (chroma > 40)
            & (y < 370)
            & ~fur
        )
    elif kind == "snapback":
        red = (r > 130) & (g < 110) & (b < 110) & (r > g + 30) & (y < 360)
        cream = (r > 160) & (g > 140) & (b > 110) & (chroma < 90) & (y < 300) & (x > 380) & (x < 680)
        panel = (r < 70) & (g < 70) & (b < 70) & (y > 120) & (y < 300) & (x > 360) & (x < 680)
        color = red | cream | panel
    else:
        raise ValueError(kind)

    seed = color & alpha & above
    filled = seed.copy()
    outline = (lum < 55) & (chroma < 50) & alpha & above
    white = (lum > 200) & (chroma < 40) & alpha & above
    for _ in range(6):
        filled |= neighbors8(filled) & (outline | white | (color & alpha & above))
    keep = grow(filled, 1) & alpha & above & ~fur
    keep[bottom:] = False
    layer = np.zeros_like(dressed)
    layer[keep] = dressed[keep]
    im = seal_interior(Image.fromarray(layer), knock_backdrop=True)
    if (layer[:, :, 3] > 20).mean() < 0.005:
        raise RuntimeError(f"{kind} extract too thin")
    return im


def extract_gallery_hat(kind: str) -> Image.Image:
    """Hats from the eight paintings, isolated by color, then scaled onto this pug."""
    y = np.arange(SIZE)[:, None]
    x = np.arange(SIZE)[None, :]
    if kind == "beanie":
        rgb = load_gallery("mint-01-stoop-beanie.png")
        r, g, b = [rgb[:, :, i].astype(np.int16) for i in range(3)]
        seed = (g > r + 6) & (g > b) & (g > 18) & (r < 90) & (b < 80) & (y < 520)
        return layer_from_mask(rgb, seed)
    if kind == "crown":
        rgb = load_gallery("mint-02-neon-crown.png")
        r, g, b = [rgb[:, :, i].astype(np.int16) for i in range(3)]
        gold = (r > 170) & (g > 110) & (b < 140) & (r > b + 30) & (y < 420)
        gems = (r > 140) & (g < 90) & (b < 90) & (y < 420) & (x > 400) & (x < 700)
        return layer_from_mask(rgb, gold | gems)
    if kind == "newsie":
        rgb = load_gallery("mint-03-rooftop-newsie.png")
        r, g, b = [rgb[:, :, i].astype(np.int16) for i in range(3)]
        seed = (r > 60) & (g > 30) & (b < 70) & (r > b + 20) & (g > b + 8) & (r < 200) & (y < 420)
        return layer_from_mask(rgb, seed)
    if kind == "hardhat":
        rgb = load_gallery("mint-04-day-hardhat.png")
        r, g, b = [rgb[:, :, i].astype(np.int16) for i in range(3)]
        chroma = rgb.max(axis=2) - rgb.min(axis=2)
        seed = (r > 140) & (g > 90) & (b < 80) & (r > b + 40) & (chroma > 50) & (y < 480) & (x > 280) & (x < 820)
        return layer_from_mask(rgb, seed, grow_px=6)
    if kind == "snapback":
        rgb = load_gallery("mint-05-subway-snapback.png")
        r, g, b = [rgb[:, :, i].astype(np.int16) for i in range(3)]
        red = (r > 140) & (g < 90) & (b < 90) & (r > g + 40) & (y < 420)
        cream = (r > 170) & (g > 140) & (b > 110) & (r < 245) & (y < 320) & (x > 350) & (x < 720)
        panel = (r < 50) & (g < 50) & (b < 50) & (y > 80) & (y < 320) & (x > 360) & (x < 720)
        return layer_from_mask(rgb, red | cream | panel)
    raise ValueError(kind)


def recolor_to(im: Image.Image, target: tuple[int, int, int], *, chroma_min: int = 12) -> Image.Image:
    """Shift fabric toward a gallery mean, leaving ink outlines and gold hardware alone."""
    a = arr(im).copy()
    rgb = a[:, :, :3].astype(np.float32)
    op = a[:, :, 3] > 20
    lum = rgb.mean(axis=2)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gold = (r > 140) & (g > 100) & (b < 150) & (r + g > 2 * b + 10)
    fabric = op & (chroma >= chroma_min) & (lum > 24) & (lum < 230) & ~gold
    if not fabric.any():
        return im
    mean = rgb[fabric].mean(axis=0)
    scale = np.array(target, dtype=np.float32) / np.maximum(mean, 1.0)
    rgb[fabric] = np.clip(rgb[fabric] * scale, 0, 255)
    a[:, :, :3] = rgb
    return Image.fromarray(a)


def fawn_mask(a: np.ndarray) -> np.ndarray:
    """Pug-fur / sticker-beige leftover. Leaves gold, yellow hats, and ink alone."""
    rgb = a[:, :, :3].astype(np.int16)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    lum = rgb.mean(axis=2)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    op = a[:, :, 3] > 20
    gold = (r > 140) & (g > 100) & (b < 150) & (r + g > 2 * b + 10)
    yellow = (r > 180) & (g > 140) & (b < 115)
    return (
        op
        & ~gold
        & ~yellow
        & (r > 140)
        & (g > 110)
        & (b > 75)
        & (chroma < 95)
        & (lum > 130)
        & (r < g + 55)
        & (b > 65)
    )


def strip_fawn(im: Image.Image, *, protect: np.ndarray | None = None) -> Image.Image:
    a = arr(im).copy()
    drop = fawn_mask(a)
    if protect is not None:
        drop = drop & ~protect
    a[drop, 3] = 0
    return Image.fromarray(clear_transparent(a))


def strip_pug_fur(im: Image.Image) -> Image.Image:
    """Hats extracted from dressed sheets pick up forehead fur under the brim."""
    return strip_fawn(im)


def strip_hat_halo(im: Image.Image, *, keep_cream: bool = False, kind: str = "") -> Image.Image:
    """Knock sticker-white and leftover fur off the brim so hats sit flush."""
    a = arr(im).copy()
    rgb = a[:, :, :3].astype(np.int16)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    lum = rgb.mean(axis=2)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    op = a[:, :, 3] > 20
    ys = np.where(op)[0]
    if not ys.size:
        return im
    y = np.arange(SIZE)[:, None]
    x = np.arange(SIZE)[None, :]
    near = y >= int(ys.max()) - 40
    edge = neighbors8(~op)
    gold = (r > 140) & (g > 100) & (b < 150) & (r + g > 2 * b + 10)
    yellow = (r > 180) & (g > 140) & (b < 115)
    fur = fawn_mask(a)
    white = op & (lum > 190) & (chroma < 55)
    # Mid-tan leftover under brims. Skip newsie — that hat is brown fabric.
    tan = np.zeros_like(op)
    if kind != "newsie":
        tan = (
            op
            & ~gold
            & ~yellow
            & (r > 85)
            & (g > 40)
            & (b > 15)
            & (r < 180)
            & (g < 135)
            & (b < 105)
            & (chroma < 95)
            & (lum > 70)
            & (lum < 175)
        )
    halo = (fur | white | tan) & (near | edge)
    if keep_cream:
        cream = (r > 155) & (g > 135) & (b > 100) & (chroma < 95)
        panel = cream & (y < 310) & (x > 380) & (x < 690) & ~near
        halo = halo & ~panel
    a[halo, 3] = 0
    return Image.fromarray(clear_transparent(a))


def cream_snapback_panel(im: Image.Image) -> Image.Image:
    """Gallery snapbacks use a cream front panel; dressed sheets sometimes bake charcoal."""
    a = arr(im).copy()
    rgb = a[:, :, :3].astype(np.float32)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    lum = rgb.mean(axis=2)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    y = np.arange(SIZE)[:, None]
    x = np.arange(SIZE)[None, :]
    op = a[:, :, 3] > 20
    cream = op & (r > 155) & (g > 135) & (b > 100) & (chroma < 95) & (y < 320)
    dark = op & (lum < 90) & (chroma < 55) & (x > 390) & (x < 690) & (y > 130) & (y < 310)
    if cream.sum() >= 2500 or dark.sum() < 400:
        return im
    cream_rgb = np.array([222, 200, 172], dtype=np.float32)
    shadow = np.array([176, 154, 128], dtype=np.float32)
    t = np.clip(lum / 80.0, 0.0, 1.0)
    target = shadow[None, None, :] * (1.0 - t[:, :, None]) + cream_rgb[None, None, :] * t[:, :, None]
    a[dark, :3] = np.clip(target[dark], 0, 255)
    return Image.fromarray(clear_transparent(a))


def shift_layer(im: Image.Image, dy: int, dx: int = 0) -> Image.Image:
    canvas = blank()
    paste_centered(canvas, im, SIZE / 2 + dx, SIZE / 2 + dy)
    return canvas


def visual_bottom(im: Image.Image, min_count: int = 50) -> int:
    """Last row that still has a real brim, ignoring leftover fur specks."""
    a = arr(im)
    for y in range(SIZE - 1, -1, -1):
        if int((a[y, :, 3] > 20).sum()) >= min_count:
            return y
    ys, _ = np.where(a[:, :, 3] > 20)
    return int(ys.max()) if ys.size else 0


def sit_on(im: Image.Image, target_bottom: int, min_count: int = 50) -> Image.Image:
    return shift_layer(im, target_bottom - visual_bottom(im, min_count))


def choke_silhouette(im: Image.Image, px: int = 1) -> Image.Image:
    """Erode the outline by a pixel so leftover brim fur cannot show."""
    a = arr(im).copy()
    op = a[:, :, 3] > 20
    for _ in range(px):
        a[op & neighbors8(~op), 3] = 0
        op = a[:, :, 3] > 20
    return Image.fromarray(clear_transparent(a))


def strip_under_brim(im: Image.Image, keep: np.ndarray) -> Image.Image:
    a = arr(im).copy()
    op = a[:, :, 3] > 20
    ys = np.where(op)[0]
    if not ys.size:
        return im
    under = op & (np.arange(SIZE)[:, None] >= int(ys.max()) - 12) & ~keep
    a[under, 3] = 0
    return Image.fromarray(clear_transparent(a))


def crop_below(im: Image.Image, y: int) -> Image.Image:
    a = arr(im).copy()
    a[y:, :, 3] = 0
    return Image.fromarray(clear_transparent(a))


def crop_to_brim(im: Image.Image, pad: int = 8) -> Image.Image:
    """Source hat sheets include a hollow opening. Keep hat + visor; drop the hole."""
    a = arr(im).copy()
    widths = (a[:, :, 3] > 20).sum(axis=1)
    if not widths.any():
        return im
    ys = np.where(widths > 0)[0]
    y0, y1 = int(ys[0]), int(ys[-1])
    # Visor / brim is the last still-wide row. Ignore the deep opening below.
    peak = int(widths[y0 : y0 + max(1, int(0.70 * (y1 - y0)))].max())
    brim = y0
    for y in range(y0, y1 + 1):
        if widths[y] >= 0.42 * peak:
            brim = y
        elif y > y0 + 0.45 * (y1 - y0) and widths[y] < 0.28 * peak:
            break
    a[brim + pad :, :, 3] = 0
    return Image.fromarray(clear_transparent(a))


def crop_hat_top(im: Image.Image, keep_h: int) -> Image.Image:
    """Some hat sheets fill the head opening with more fabric. Keep the wearable crown only."""
    a = arr(im).copy()
    ys = np.where(a[:, :, 3] > 20)[0]
    if not ys.size:
        return im
    a[int(ys.min()) + keep_h :, :, 3] = 0
    return Image.fromarray(clear_transparent(a))


def seat_hat_brim(im: Image.Image, y_center: int, y_sides: int, x0: int = 280, x1: int = 744) -> Image.Image:
    """Drop a flat crop line: brim higher on the forehead, lower over the ears."""
    a = arr(im).copy()
    rows = np.arange(SIZE, dtype=np.float32)[:, None]
    cols = np.arange(SIZE, dtype=np.float32)[None, :]
    half = max((x1 - x0) / 2.0, 1.0)
    t = np.clip(np.abs(cols - 512.0) / half, 0.0, 1.0)
    bottom = y_center + (y_sides - y_center) * t
    a[rows > bottom, 3] = 0
    return Image.fromarray(clear_transparent(a))


def place_hat(
    rel: str,
    width: int,
    brim_y: int,
    max_h: int | None = None,
    *,
    keep_h: int | None = None,
    seat: tuple[int, int] | None = None,
) -> Image.Image:
    """Original hat art, brim on this pug's forehead."""
    src = crop_hat_top(load_src(rel), keep_h) if keep_h else crop_to_brim(load_src(rel))
    hat = harden_overlay(place_bottom(src, width, brim_y, 512, max_h), drop_specks=True)
    if seat:
        hat = harden_overlay(seat_hat_brim(hat, seat[0], seat[1]), drop_specks=True)
    return hat


def fit_hats() -> None:
    """Original hat sheets, seated on this pug the way the eight gallery paintings wear them."""
    # Crop the source crown (keep_h) instead of max_h — max_h shrinks width.
    save("hat/hat-beanie.png", place_hat("hat/hat-beanie.png", 410, 338, keep_h=210, seat=(324, 358)))
    save("hat/hat-newsie.png", place_hat("hat/hat-newsie.png", 440, 402, keep_h=175, seat=(388, 406)))
    save("hat/hat-hardhat.png", place_hat("hat/hat-hardhat.png", 300, 408, keep_h=125, seat=(400, 414)))
    save("hat/hat-snapback.png", place_hat("hat/hat-snapback.png", 400, 378, keep_h=265))
    save("hat/hat-crown.png", place_hat("hat/hat-crown.png", 240, 362, 148, seat=(352, 364)))


def prepare_hoodie(im: Image.Image) -> Image.Image:
    """Paint a smooth cream cowl. Source grain becomes stripes if we remap by luminance."""
    a = arr(im).copy()
    rgb = a[:, :, :3].astype(np.int16)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    lum = rgb.mean(axis=2)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    opaque = a[:, :, 3] > 20
    strings = opaque & (r > g + 8) & (g > b + 4) & (chroma >= 28) & (r > 70) & (lum < 170)
    ink = opaque & (lum < 48)
    fabric = opaque & ~strings & ~ink
    cream = np.array([226, 206, 176], dtype=np.float32)
    shadow = np.array([200, 178, 148], dtype=np.float32)
    yy = np.broadcast_to(np.arange(SIZE, dtype=np.float32)[:, None], (SIZE, SIZE))
    t = np.clip((yy - 555.0) / 74.0, 0.0, 1.0)
    target = shadow[None, None, :] * t[:, :, None] + cream[None, None, :] * (1.0 - t)[:, :, None]
    a[fabric, :3] = np.clip(target[fabric], 0, 255)
    return Image.fromarray(clear_transparent(a))


def paint_hoodie_cowl(placed: Image.Image) -> Image.Image:
    """Solid rolled cowl on the wall. Keep source ink and drawstrings only."""
    src = arr(placed)
    rgb = src[:, :, :3].astype(np.int16)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    lum = rgb.mean(axis=2)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    op = src[:, :, 3] > 20
    strings = op & (r > g + 8) & (g > b + 4) & (chroma >= 28) & (r > 70) & (lum < 170)
    ink = op & (lum < 48)
    cream = np.array([226, 206, 176], dtype=np.uint8)
    shadow = np.array([196, 174, 144], dtype=np.uint8)
    a = np.zeros_like(src)
    yy = np.arange(SIZE)[:, None]
    xx = np.arange(SIZE)[None, :]
    x0, x1 = 268, 756
    # Almost-flat band so side wings cannot read as floating shards.
    y_center, y_sides = 564, 560
    half = max((x1 - x0) / 2.0, 1.0)
    t = np.clip(np.abs(xx - 512.0) / half, 0.0, 1.0)
    top = y_center + (y_sides - y_center) * t
    band = (xx >= x0) & (xx <= x1) & (yy >= top) & (yy < WALL_TOP)
    a[band, :3] = cream
    a[band, 3] = 255
    a[band & (yy >= 610), :3] = shadow
    rim = band & (yy < top + 3)
    a[rim, :3] = np.array([32, 22, 16], dtype=np.uint8)
    a[ink] = src[ink]
    a[strings] = src[strings]
    return Image.fromarray(clear_transparent(a))


def choke_brim(im: Image.Image, px: int = 2) -> Image.Image:
    """Erode only the underside of a hat so leftover fur cannot hang off the brim."""
    a = arr(im).copy()
    op = a[:, :, 3] > 20
    ys = np.where(op)[0]
    if not ys.size:
        return im
    brim = np.arange(SIZE)[:, None] >= int(ys.max()) - 22
    for _ in range(px):
        a[op & brim & neighbors8(~op), 3] = 0
        op = a[:, :, 3] > 20
    return Image.fromarray(clear_transparent(a))


def feather_front(full: Image.Image, split_y: int, fade: int = 8) -> Image.Image:
    data = arr(full).astype(np.float32)
    rows = np.arange(SIZE, dtype=np.float32)[:, None]
    data[:, :, 3] *= np.clip((rows - (split_y - fade)) / fade, 0.0, 1.0)
    return Image.fromarray(np.clip(data, 0, 255).astype(np.uint8))


def tongue_mask(pug: Image.Image) -> np.ndarray:
    pug_a = arr(pug)
    rgb = pug_a[:, :, :3].astype(np.int16)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    alpha = pug_a[:, :, 3] > 20
    rows = np.arange(SIZE)[:, None]
    cols = np.arange(SIZE)[None, :]
    # Actual pink tongue pixels only — neck layer sits in front of the pug.
    return (
        alpha
        & (r > 160)
        & (g > 80)
        & (g < 180)
        & (b > 80)
        & (b < 160)
        & (r > g + 20)
        & (rows >= 528)
        & (rows < WALL_TOP)
        & (cols >= 445)
        & (cols <= 585)
    )


def clothes_face_punch(pug: Image.Image, kind: str) -> np.ndarray:
    """Clear leftover loop pixels over the eyes only. Do not carve the under-chin wrap."""
    pug_a = arr(pug)
    alpha = pug_a[:, :, 3] > 20
    rows = np.arange(SIZE)[:, None]
    cols = np.arange(SIZE)[None, :]
    eyes = alpha & (rows > 350) & (rows < 495) & (cols >= 330) & (cols <= 700)
    if kind == "gold-chain":
        eyes = alpha & (rows > 350) & (rows < 490) & (cols >= 350) & (cols <= 680)
    return eyes


def hoodie_charcoal_color(im: Image.Image) -> tuple[int, int, int]:
    """Exterior charcoal, not the cream lining that disappears on fawn fur."""
    a = arr(im)
    rgb = a[:, :, :3].astype(np.int16)
    lum = rgb.mean(axis=2)
    dark = (a[:, :, 3] > 200) & (lum > 12) & (lum < 85)
    if dark.any():
        return tuple(int(v) for v in np.median(rgb[dark], axis=0))
    return (42, 44, 50)


def drop_hoodie_lining(im: Image.Image, charcoal: tuple[int, int, int]) -> Image.Image:
    """Keep the charcoal wrap readable: swap leftover cream lining for exterior fabric."""
    a = arr(im).copy()
    lum = a[:, :, :3].astype(np.int16).mean(axis=2)
    cream = (a[:, :, 3] > 20) & (lum >= 120)
    a[cream, :3] = np.array(charcoal, dtype=np.uint8)
    a[cream, 3] = 255
    return Image.fromarray(clear_transparent(a))


def ensure_u_wrap(
    im: Image.Image,
    y_center: int,
    y_sides: int,
    x0: int,
    x1: int,
    color: tuple[int, int, int],
) -> Image.Image:
    """Solid strap under the chin; sides only above that, so the mouth stays open."""
    a = arr(im).copy()
    sample = np.array(color, dtype=np.uint8)
    mid = (x0 + x1) // 2
    for y in range(y_sides, WALL_TOP):
        if y < y_center:
            t = (y_center - y) / max(y_center - y_sides, 1)
            open_w = int((x1 - x0) * 0.42 * t)
            spans = ((x0, mid - open_w // 2), (mid + open_w // 2, x1))
        else:
            spans = ((x0, x1),)
        for left, right in spans:
            if right <= left:
                continue
            empty = a[y, left:right, 3] < 180
            if not empty.any():
                continue
            a[y, left:right, :3][empty] = sample
            a[y, left:right, 3][empty] = 255
    return Image.fromarray(clear_transparent(a))


def body_neck_layer(full: Image.Image, pug: Image.Image, kind: str) -> Image.Image:
    """Original fabric in front of the neck. No painted fill — placement does the wrap."""
    a = arr(full).copy()
    a[clothes_face_punch(pug, kind), 3] = 0
    a[tongue_mask(pug), 3] = 0
    a[WALL_TOP:, :, 3] = 0
    neck = Image.fromarray(clear_transparent(a))
    # Keep the source pixels under the chin. Do not paint a replacement strap.
    curve = {
        "bandana": (600, 538),
        "collar": (605, 548),
        "gold-chain": (598, 562),
    }.get(kind)
    if curve:
        neck = clip_above_curve(neck, curve[0], curve[1])
    return neck


def fabric_fill_color(im: Image.Image, kind: str | None = None) -> tuple[int, int, int] | None:
    a = arr(im)
    rgb = a[:, :, :3].astype(np.int16)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    lum = rgb.mean(axis=2)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    op = a[:, :, 3] > 200
    if kind == "hoodie":
        fabric = op & (lum > 12) & (lum < 85)
    elif kind == "bandana":
        fabric = op & (lum > 40) & (lum < 200) & (chroma >= 18)
    elif kind == "collar":
        fabric = op & (r > g + 20) & (r > b + 20) & (r > 80)
    else:
        fabric = op & (lum > 40) & (lum < 230) & (chroma >= 12)
    if not fabric.any():
        return None
    return tuple(int(v) for v in np.median(rgb[fabric], axis=0))


def fill_interior_gaps(
    im: Image.Image,
    y0: int,
    y1: int = WALL_TOP,
    color: tuple[int, int, int] | None = None,
) -> Image.Image:
    """Close the neck-loop hole under the chin with one fabric color."""
    a = arr(im).copy()
    fill = color or fabric_fill_color(im)
    if fill is None:
        return im
    mask = a[:, :, 3] > 20
    sample = np.array(fill, dtype=np.uint8)
    for y in range(y0, y1):
        xs = np.where(mask[y])[0]
        if xs.size < 8:
            continue
        left, right = int(xs.min()), int(xs.max())
        if right - left < 40:
            continue
        gap = slice(left, right + 1)
        empty = a[y, gap, 3] < 180
        if not empty.any():
            continue
        a[y, gap, :3][empty] = sample
        a[y, gap, 3][empty] = 255
    return Image.fromarray(clear_transparent(a))


def punch_chain_holes(im: Image.Image) -> Image.Image:
    """Knock gray/beige sheet-fill out of link openings. Leave gold and highlights."""
    a = arr(im).copy()
    rgb = a[:, :, :3].astype(np.int16)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    lum = rgb.mean(axis=2)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    op = a[:, :, 3] > 20
    gray_fill = (
        op
        & (chroma < 45)
        & (lum > 100)
        & (lum < 200)
        & (np.abs(r - g) < 28)
        & (np.abs(g - b) < 28)
    )
    a[gray_fill | fawn_mask(a), 3] = 0
    return Image.fromarray(clear_transparent(a))


def keep_metal_only(im: Image.Image, *, gems: bool = False) -> Image.Image:
    """Crown / chain: drop fur-colored leftover that is not metal, ink, or gems."""
    a = arr(im).copy()
    rgb = a[:, :, :3].astype(np.int16)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    lum = rgb.mean(axis=2)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    op = a[:, :, 3] > 20
    gold = (r > 130) & (g > 85) & (b < 140) & (chroma > 35) & (r + g > 2 * b + 8)
    shine = op & (lum > 220) & (chroma < 45)
    ink = op & (lum < 60)
    gem = (r > 120) & (g < 110) & (b < 110) & (r > g + 20) if gems else np.zeros_like(op)
    keep = grow(gold | shine | ink | gem, 1) & op
    a[~keep, 3] = 0
    return Image.fromarray(clear_transparent(a))


def close_row_gaps(
    im: Image.Image,
    y0: int,
    y1: int,
    color: tuple[int, int, int],
    max_gap: int = 140,
) -> Image.Image:
    """Bridge two fabric islands on the same row (bandana wrap → knot)."""
    a = arr(im).copy()
    mask = a[:, :, 3] > 20
    sample = np.array(color, dtype=np.uint8)
    for y in range(y0, y1):
        xs = np.where(mask[y])[0]
        if xs.size < 4:
            continue
        breaks = np.where(np.diff(xs) > 1)[0]
        starts = np.concatenate(([int(xs[0])], xs[breaks + 1].astype(int)))
        ends = np.concatenate((xs[breaks].astype(int), [int(xs[-1])]))
        for i in range(len(starts) - 1):
            gap = int(starts[i + 1] - ends[i])
            if 2 < gap <= max_gap:
                a[y, ends[i] + 1 : starts[i + 1], :3] = sample
                a[y, ends[i] + 1 : starts[i + 1], 3] = 255
    return Image.fromarray(clear_transparent(a))


def bandana_knot_layer(src: Image.Image) -> Image.Image:
    """The knot is drawn at the top of the source loop; park it on the right of the neck."""
    a = arr(src).copy()
    x0, y0, x1, y1 = content_bbox(a)
    a[:, : int(x0 + 0.66 * (x1 - x0)), 3] = 0
    a[int(y0 + 0.40 * (y1 - y0)) :, :, 3] = 0
    knot = Image.fromarray(clear_transparent(a))
    return paste_box(knot, (605, 565, 160, 110), "center")


def body_hang_layer(full: Image.Image, kind: str) -> Image.Image:
    """Strings, medallion, tag, and bib that hang in front of the wall."""
    a = arr(full).copy()
    rgb = a[:, :, :3].astype(np.int16)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    lum = rgb.mean(axis=2)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    rows = np.arange(SIZE)[:, None]
    alpha = a[:, :, 3] > 20
    below = np.broadcast_to(rows >= WALL_TOP - 18, alpha.shape)
    cols = np.arange(SIZE)[None, :]
    if kind == "bandana":
        # Gallery tucks the bib behind the wall; only the neck wrap should show.
        keep = np.zeros_like(alpha)
    elif kind == "hoodie":
        strings = (
            alpha
            & (rows >= WALL_TOP - 22)
            & (cols >= 430)
            & (cols <= 590)
            & (
                ((r > g + 4) & (g >= b - 4) & (r > 40) & (lum < 170) & (chroma >= 10))
                | ((lum < 70) & (cols >= 455) & (cols <= 565))
            )
        )
        keep = grow(strings, 2)
    elif kind == "gold-chain":
        gold = alpha & (r > 120) & (g > 80) & (b < 150) & (rows >= WALL_TOP - 36)
        keep = grow(gold, 2)
    elif kind == "collar":
        gold = (r > 140) & (g > 90) & (b < 150)
        center = (cols >= 420) & (cols <= 610)
        tag = alpha & (rows >= 580) & (gold | (center & (rows >= WALL_TOP - 28)))
        keep = grow(tag, 2)
    else:
        keep = alpha & below
    a[~keep, 3] = 0
    return Image.fromarray(clear_transparent(a))


def clip_above_curve(im: Image.Image, y_center: int, y_sides: int, x0: int = 260, x1: int = 764) -> Image.Image:
    """Keep a U-wrap: higher on the jowls, lower under the mouth. Avoids a hard crop line."""
    a = arr(im).copy()
    rows = np.arange(SIZE, dtype=np.float32)[:, None]
    cols = np.arange(SIZE, dtype=np.float32)[None, :]
    half = max((x1 - x0) / 2.0, 1.0)
    t = np.clip(np.abs(cols - 512.0) / half, 0.0, 1.0)
    top = y_center + (y_sides - y_center) * t
    a[rows < top, 3] = 0
    return Image.fromarray(clear_transparent(a))


def knock_out_hoodie_fill(im: Image.Image) -> Image.Image:
    """Source hoodie fills the head hole with lining. Drop the fill so the pug shows through."""
    a = arr(im).copy()
    rgb = a[:, :, :3].astype(np.int16)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    alpha = a[:, :, 3] > 20
    lining = alpha & (r > 140) & (g > 110) & (b > 70) & (r > b)
    fabric = alpha & ~lining
    rim = grow(fabric, 3)
    a[lining & ~rim, 3] = 0
    return Image.fromarray(clear_transparent(a))


def fit_body(paws: Image.Image) -> None:
    """Original clothes sheets, seated under this pug's chin the way the gallery paintings wear them."""
    pug = load_trait("base/base-fawn-peek.png")
    specs = [
        # Scale so the solid bottom of each source loop lands under the chin, not the hole.
        ("body/body-bandana.png", load_src("body/body-bandana.png"), "bandana", (180, 390, 660, 315)),
        ("body/body-collar.png", load_src("body/body-collar.png"), "collar", (210, 435, 580, 310)),
        ("body/body-hoodie.png", knock_out_hoodie_fill(load_src("body/body-hoodie.png")), "hoodie", (170, 400, 680, 280)),
        ("body/body-gold-chain.png", load_src("body/body-gold-chain.png"), "gold-chain", (190, 380, 644, 370)),
    ]
    for dest, src, kind, box in specs:
        # Never fill the neck opening — that painted the wraps into flat bars.
        full = harden_overlay(paste_box(src, box, "bottom"), fill_holes=False)
        if kind == "gold-chain":
            full = punch_chain_holes(full)
        save(dest, full)
        neck = harden_overlay(body_neck_layer(full, pug, kind), fill_holes=False)
        if kind == "bandana":
            knot = harden_overlay(bandana_knot_layer(src), fill_holes=False)
            knot_a = arr(knot)
            knot_a[WALL_TOP:, :, 3] = 0
            knot = Image.fromarray(clear_transparent(knot_a))
            neck = Image.alpha_composite(neck, knot)
        save(dest.replace(".png", "-neck.png"), neck)
        hang = body_hang_layer(full, kind)
        if (arr(hang)[:, :, 3] > 20).any():
            hang = harden_overlay(hang, fill_holes=False)
        else:
            hang = blank()
        save(dest.replace(".png", "-front.png"), hang)


def extract_gallery_accessory(kind: str) -> Image.Image:
    y = np.arange(SIZE)[:, None]
    x = np.arange(SIZE)[None, :]
    if kind == "blocks":
        rgb = load_gallery("mint-04-day-hardhat.png")
        r, g, b = [rgb[:, :, i].astype(np.int16) for i in range(3)]
        red = (r > 160) & (g < 90) & (b < 80) & (x < 480) & (y > 430) & (y < 820)
        blue = (b > 90) & (b > r + 20) & (b > g) & (x < 480) & (y > 430) & (y < 820)
        yellow = (r > 180) & (g > 140) & (b < 80) & (x < 520) & (y > 430) & (y < 820)
        return layer_from_mask(rgb, red | blue | yellow, grow_px=5)
    if kind == "coffee":
        rgb = load_gallery("mint-03-rooftop-newsie.png")
        r, g, b = [rgb[:, :, i].astype(np.int16) for i in range(3)]
        cup = (r > 80) & (g > 40) & (b < 70) & (r > b + 20) & (x > 560) & (y > 480) & (y < 860)
        lid = (r > 180) & (g > 180) & (b > 170) & (x > 600) & (y > 480) & (y < 700)
        return layer_from_mask(rgb, cup | lid, grow_px=4)
    if kind == "bone":
        rgb = load_gallery("mint-07-cream-hoodie.png")
        r, g, b = [rgb[:, :, i].astype(np.int16) for i in range(3)]
        bone = (r > 160) & (g > 130) & (b > 90) & (r < 250) & (x > 520) & (y > 520) & (y < 820)
        chew = (r > 90) & (r < 180) & (g > 60) & (g < 140) & (b < 100) & (x > 520) & (y > 540) & (y < 820)
        return layer_from_mask(rgb, bone | chew, grow_px=4)
    if kind == "sunglasses":
        rgb = load_gallery("mint-05-subway-snapback.png")
        r, g, b = [rgb[:, :, i].astype(np.int16) for i in range(3)]
        dark = (r < 70) & (g < 70) & (b < 70) & (y > 300) & (y < 520) & (x > 280) & (x < 780)
        return layer_from_mask(rgb, dark, grow_px=3)
    if kind == "monocle":
        rgb = load_gallery("mint-06-green-monocle.png")
        r, g, b = [rgb[:, :, i].astype(np.int16) for i in range(3)]
        gold = (r > 160) & (g > 110) & (b < 90) & (y > 280) & (y < 720) & (x < 560)
        glass = (b > g) & (g > 80) & (r < 200) & (y > 300) & (y < 520) & (x < 520)
        return layer_from_mask(rgb, gold | glass, grow_px=4)
    raise ValueError(kind)


def fit_accessories() -> None:
    """Source drawings at gallery scale, sitting on this pug's eyes / wall rim."""
    save(
        "accessory/acc-sunglasses.png",
        harden_overlay(paste_box(load_src("accessory/acc-sunglasses.png"), (300, 360, 420, 145), "center")),
    )
    monocle = ImageOps.mirror(load_src("accessory/acc-monocle.png"))
    save(
        "accessory/acc-monocle.png",
        harden_overlay(paste_box(monocle, (325, 355, 155, 230), "center"), fill_holes=False),
    )
    save(
        "accessory/acc-coffee.png",
        harden_overlay(paste_box(load_src("accessory/acc-coffee.png"), (790, 525, 170, 150), "bottom")),
    )
    save(
        "accessory/acc-bone.png",
        harden_overlay(paste_box(load_src("accessory/acc-bone.png"), (735, 540, 230, 120), "bottom")),
    )
    save(
        "accessory/acc-blocks.png",
        harden_overlay(paste_box(load_src("accessory/acc-blocks.png"), (12, 485, 215, 170), "bottom")),
    )


def composite_stack(
    *,
    background: str,
    base: str,
    block: str | None = None,
    body: str | None = None,
    hat: str | None = None,
    accessory: str | None = None,
) -> Image.Image:
    """Gallery order: wrap behind, pug, hat, neck in front, wall, hanging bits, toys, paws."""
    color = Path(base).stem.split("-")[1]
    canvas = blank()

    def comp(rel: str | None) -> None:
        nonlocal canvas
        if not rel:
            return
        path = TRAITS / rel
        if not path.exists():
            return
        overlay = Image.open(path).convert("RGBA")
        if overlay.size != (SIZE, SIZE):
            overlay = overlay.resize((SIZE, SIZE), Image.Resampling.LANCZOS)
        canvas = Image.alpha_composite(canvas, overlay)

    acc_id = Path(accessory).stem.replace("acc-", "") if accessory else None
    comp(background)
    comp(body)
    comp(base)
    if acc_id in FACE_ACCESSORIES:
        comp(accessory)
    comp(hat)
    if body:
        comp(body.replace(".png", "-neck.png"))
    comp(block or "base/wall-default.png")
    if body:
        comp(body.replace(".png", "-front.png"))
    if acc_id in LEDGE_ACCESSORIES:
        comp(accessory)
    comp(f"base/front-paws-{color}.png")
    return canvas


GALLERY_COMBOS = [
    ("compare-01.jpg", "mint-01-stoop-beanie.png", dict(background="background/bg-brownstone.png", base="base/base-fawn-peek.png", body="body/body-bandana.png", hat="hat/hat-beanie.png")),
    ("compare-02.jpg", "mint-02-neon-crown.png", dict(background="background/bg-neon-night.png", base="base/base-black-peek.png", body="body/body-gold-chain.png", hat="hat/hat-crown.png")),
    ("compare-03.jpg", "mint-03-rooftop-newsie.png", dict(background="background/bg-rooftop-sunset.png", base="base/base-cream-peek.png", hat="hat/hat-newsie.png", accessory="accessory/acc-coffee.png")),
    ("compare-04.jpg", "mint-04-day-hardhat.png", dict(background="background/bg-stoop-day.png", base="base/base-fawn-peek.png", hat="hat/hat-hardhat.png", accessory="accessory/acc-blocks.png")),
    ("compare-05.jpg", "mint-05-subway-snapback.png", dict(background="background/bg-subway.png", base="base/base-black-peek.png", hat="hat/hat-snapback.png", accessory="accessory/acc-sunglasses.png")),
    ("compare-06.jpg", "mint-06-green-monocle.png", dict(background="background/bg-chain-green.png", base="base/base-cream-peek.png", body="body/body-collar.png", accessory="accessory/acc-monocle.png")),
    ("compare-07.jpg", "mint-07-cream-hoodie.png", dict(background="background/bg-cream-brick.png", base="base/base-fawn-peek.png", body="body/body-hoodie.png", accessory="accessory/acc-bone.png")),
    ("compare-08.jpg", "mint-08-sunset-bandana.png", dict(background="background/bg-rooftop-sunset.png", base="base/base-black-peek.png", body="body/body-bandana.png", accessory="accessory/acc-sunglasses.png")),
]


def write_placement_tests() -> None:
    out = ROOT / "generated" / "placement-tests"
    out.mkdir(parents=True, exist_ok=True)
    combos = [
        ("stack-01-beanie-bandana.png", dict(background="background/bg-brownstone.png", base="base/base-fawn-peek.png", body="body/body-bandana.png", hat="hat/hat-beanie.png")),
        ("stack-02-crown-chain.png", dict(background="background/bg-neon-night.png", base="base/base-black-peek.png", body="body/body-gold-chain.png", hat="hat/hat-crown.png")),
        ("stack-03-newsie-coffee.png", dict(background="background/bg-rooftop-sunset.png", base="base/base-cream-peek.png", hat="hat/hat-newsie.png", accessory="accessory/acc-coffee.png")),
        ("stack-04-hardhat-blocks.png", dict(background="background/bg-stoop-day.png", base="base/base-fawn-peek.png", hat="hat/hat-hardhat.png", accessory="accessory/acc-blocks.png")),
        ("stack-05-snap-shades.png", dict(background="background/bg-subway.png", base="base/base-black-peek.png", hat="hat/hat-snapback.png", accessory="accessory/acc-sunglasses.png")),
        ("stack-06-collar-monocle.png", dict(background="background/bg-chain-green.png", base="base/base-cream-peek.png", body="body/body-collar.png", accessory="accessory/acc-monocle.png")),
        ("stack-07-hoodie-bone.png", dict(background="background/bg-cream-brick.png", base="base/base-fawn-peek.png", body="body/body-hoodie.png", accessory="accessory/acc-bone.png")),
        ("stack-08-bandana-shades.png", dict(background="background/bg-rooftop-sunset.png", base="base/base-black-peek.png", body="body/body-bandana.png", accessory="accessory/acc-sunglasses.png")),
        ("stack-gold-block.png", dict(background="background/bg-stoop-day.png", base="base/base-fawn-peek.png", block="block/block-gold.png", hat="hat/hat-beanie.png", body="body/body-hoodie.png")),
        ("stack-crate-block.png", dict(background="background/bg-brownstone.png", base="base/base-cream-peek.png", block="block/block-crate.png", hat="hat/hat-snapback.png", body="body/body-gold-chain.png")),
    ]
    for name, layers in combos:
        img = composite_stack(**layers)
        img.convert("RGB").save(out / name, "JPEG", quality=92)
        print("test", out / name)

    strips = []
    for name, gal_name, layers in GALLERY_COMBOS:
        stacked = composite_stack(**layers).convert("RGB")
        gallery = Image.open(GALLERY / gal_name).convert("RGB").resize((SIZE, SIZE), Image.Resampling.LANCZOS)
        pair = Image.new("RGB", (SIZE * 2, SIZE))
        pair.paste(gallery, (0, 0))
        pair.paste(stacked, (SIZE, 0))
        pair.save(out / name, "JPEG", quality=90)
        a = np.array(gallery).astype(np.int16)
        b = np.array(stacked).astype(np.int16)
        mae = float(np.abs(a - b).mean())
        print(f"compare {name} mae={mae:.1f} (gallery left, stack right)")
        strips.append(pair.resize((512, 256), Image.Resampling.LANCZOS))
    if strips:
        sheet = Image.new("RGB", (512, 256 * len(strips)))
        for i, strip in enumerate(strips):
            sheet.paste(strip, (0, i * 256))
        sheet.save(out / "compare-all.jpg", "JPEG", quality=90)


def main() -> int:
    seal_bases()
    paws = split_bases()
    fit_blocks(paws)
    fit_hats()
    fit_body(paws)
    fit_accessories()
    write_placement_tests()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
