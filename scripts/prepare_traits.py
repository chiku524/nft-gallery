#!/usr/bin/env python3
"""DO NOT RUN for the live drop.

This recrops hats and splits body/hat layers for a later worn-stack experiment.
The collection look is the original gallery paintings (commit 6b3ca8f overlays).
Regenerate with `python3 scripts/generate_collection.py` only.
"""

from __future__ import annotations

from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SRC = Path("/opt/cursor/artifacts/assets")
DST = ROOT / "public" / "traits"
SIZE = 1024
TEST_DIR = ROOT / "generated" / "placement-tests"

# Pug landmarks on the 1024 canvas (measured from the processed bases):
#   head silhouette top ≈ 197
#   eyes ≈ 360–430 (cy ≈ 398)
#   chin on the ledge ≈ 620–629
#   wall top rim ≈ 630–639
HEAD_TOP = 197
EYE_CY = 398
WALL_TOP = 629


def _neighbors4(mask: np.ndarray) -> np.ndarray:
    out = np.zeros_like(mask)
    out[1:, :] |= mask[:-1, :]
    out[:-1, :] |= mask[1:, :]
    out[:, 1:] |= mask[:, :-1]
    out[:, :-1] |= mask[:, 1:]
    return out


def _neighbors8(mask: np.ndarray) -> np.ndarray:
    out = _neighbors4(mask)
    out[1:, 1:] |= mask[:-1, :-1]
    out[1:, :-1] |= mask[:-1, 1:]
    out[:-1, 1:] |= mask[1:, :-1]
    out[:-1, :-1] |= mask[1:, 1:]
    return out


def clear_transparent(arr: np.ndarray) -> np.ndarray:
    """Zero RGB on transparent pixels so later resizes cannot bleed white."""
    trans = arr[..., 3] == 0
    arr[trans, 0] = 0
    arr[trans, 1] = 0
    arr[trans, 2] = 0
    return arr


def flood_white(im: Image.Image, thresh: int = 246) -> Image.Image:
    """Transparent only for near-white pixels connected to the canvas edge."""
    arr = np.array(im.convert("RGBA"))
    rgb = arr[..., :3].astype(np.int16)
    h, w = rgb.shape[:2]
    white = rgb.min(axis=2) >= thresh
    visited = np.zeros((h, w), dtype=bool)
    q: deque[tuple[int, int]] = deque()

    def push(y: int, x: int) -> None:
        if 0 <= y < h and 0 <= x < w and white[y, x] and not visited[y, x]:
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
        arr[y, x, 3] = 0
        push(y - 1, x)
        push(y + 1, x)
        push(y, x - 1)
        push(y, x + 1)

    return Image.fromarray(clear_transparent(arr), "RGBA")


def knock_all_white(im: Image.Image, thresh: int = 246) -> Image.Image:
    """Transparent for every near-white pixel (opens bandana/chain holes)."""
    arr = np.array(im.convert("RGBA"))
    white = arr[..., :3].min(axis=2) >= thresh
    arr[..., 3] = np.where(white, 0, arr[..., 3]).astype(np.uint8)
    return Image.fromarray(clear_transparent(arr), "RGBA")


def defringe(
    im: Image.Image,
    lum_cut: int = 150,
    chroma_cut: int = 36,
    passes: int = 3,
    connectivity: int = 4,
) -> Image.Image:
    """Remove the light halo left by knocking a white backdrop.

    Two artifacts show up at the silhouette:

      1. Leftover near-white pixels (lum >= lum_cut) — fully transparent.
      2. Gray anti-aliasing that was baked against white (lum 50–150,
         full opacity). Those look like a pale ring on any dark or
         colored background. Recover coverage as if the source was a
         black outline over white: alpha = 1 - lum/255, RGB = black.

    Only near-neutral pixels that touch transparency are touched, so
    cream fur, gold tags, eye highlights, and snapback panels stay put.
    """
    neigh = _neighbors8 if connectivity == 8 else _neighbors4
    arr = np.array(im.convert("RGBA"))
    for _ in range(passes):
        rgb = arr[..., :3].astype(np.int16)
        alpha = arr[..., 3]
        lum = rgb.mean(axis=2)
        chroma = rgb.max(axis=2) - rgb.min(axis=2)
        opaque = alpha > 8
        trans = ~opaque
        edge = opaque & neigh(trans) & (chroma <= chroma_cut)
        if not edge.any():
            break
        white = edge & (lum >= lum_cut)
        aa = edge & (lum >= 48) & (lum < lum_cut)
        if not white.any() and not aa.any():
            break
        arr[white, 3] = 0
        if aa.any():
            coverage = np.clip(1.0 - lum[aa] / 255.0, 0.0, 1.0)
            arr[aa, 0] = 0
            arr[aa, 1] = 0
            arr[aa, 2] = 0
            arr[aa, 3] = np.clip(coverage * 255.0, 0, 255).astype(np.uint8)
    return Image.fromarray(clear_transparent(arr), "RGBA")


# Bases: aggressive. Overlays: conservative so cream hoodies / gold stay intact.
DEFRINGE_BASE = dict(lum_cut=110, chroma_cut=40, passes=6, connectivity=8)
DEFRINGE_OVERLAY = dict(lum_cut=180, chroma_cut=16, passes=3, connectivity=4)


def seal_outline(im: Image.Image) -> Image.Image:
    """Fill a 1px black ring into transparency next to the ink line.

    After unbaking white-backdrop AA, the outer pixel is often partial-alpha
    black. JPEG chroma subsampling turns that into a light fringe. Sealing
    the matte with solid black also closes the 1px gap left on the wall rim.
    """
    arr = np.array(im.convert("RGBA"))
    rgb = arr[..., :3].astype(np.int16)
    alpha = arr[..., 3]
    lum = rgb.mean(axis=2)
    # Crush leftover partial-alpha ink to solid black so JPEG cannot ring.
    partial = (alpha > 24) & (alpha < 250) & (lum < 50)
    arr[partial, 0] = 0
    arr[partial, 1] = 0
    arr[partial, 2] = 0
    arr[partial, 3] = 255
    rgb = arr[..., :3].astype(np.int16)
    alpha = arr[..., 3]
    lum = rgb.mean(axis=2)
    dark = (alpha > 160) & (lum < 55)
    trans = alpha < 24
    ring = trans & _neighbors8(dark)
    arr[ring, 0] = 0
    arr[ring, 1] = 0
    arr[ring, 2] = 0
    arr[ring, 3] = 255
    # Second pass only along the wall rim, where knockout can leave a 2px gap.
    rgb = arr[..., :3].astype(np.int16)
    alpha = arr[..., 3]
    lum = rgb.mean(axis=2)
    dark = (alpha > 160) & (lum < 55)
    trans = alpha < 24
    ring = trans & _neighbors8(dark)
    ring[:620] = False
    arr[ring, 0] = 0
    arr[ring, 1] = 0
    arr[ring, 2] = 0
    arr[ring, 3] = 255
    return Image.fromarray(clear_transparent(arr), "RGBA")


def content_crop(im: Image.Image, pad: int = 1) -> Image.Image:
    arr = np.array(im)
    ys, xs = np.where(arr[..., 3] > 12)
    if len(xs) == 0:
        return im
    left, right = max(0, xs.min() - pad), min(im.width - 1, xs.max() + pad)
    top, bottom = max(0, ys.min() - pad), min(im.height - 1, ys.max() + pad)
    return im.crop((left, top, right + 1, bottom + 1))


def paste_centered(canvas: Image.Image, overlay: Image.Image, cx: int, cy: int) -> None:
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


def paste_bottom(canvas: Image.Image, overlay: Image.Image, cx: int, bottom: int) -> None:
    paste_centered(canvas, overlay, cx, bottom - overlay.height / 2)


def fit_width(im: Image.Image, width: int, max_height: int | None = None) -> Image.Image:
    if im.width == 0:
        return im
    height = max(1, round(im.height * (width / im.width)))
    if max_height is not None and height > max_height:
        height = max_height
    resized = im.resize((width, height), Image.Resampling.LANCZOS)
    # LANCZOS samples transparent neighbors and can reintroduce a light fringe.
    return defringe(resized, **DEFRINGE_OVERLAY)


def boost_fill(im: Image.Image, tan: tuple[float, float, float], mix: float) -> Image.Image:
    """Pull pale fur toward a readable tan so heads don't vanish on busy backgrounds."""
    arr = np.array(im).astype(np.float32)
    rgb = arr[..., :3]
    alpha = arr[..., 3]
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    rows = np.arange(arr.shape[0])[:, None]
    fill = (alpha > 200) & (rows < 640) & (chroma > 15) & (rgb.min(axis=2) > 80)
    target = np.array(tan, dtype=np.float32)
    rgb[fill] = rgb[fill] * (1.0 - mix) + target * mix
    arr[..., :3] = np.clip(rgb, 0, 255)
    return Image.fromarray(arr.astype(np.uint8), "RGBA")


def align_top(im: Image.Image, top: int) -> Image.Image:
    """Shift a full-width wall so its visible top matches the pug ledge."""
    arr = np.array(im.convert("RGBA"))
    ys, xs = np.where(arr[..., 3] > 12)
    if len(ys) == 0:
        return im
    shift = top - int(ys.min())
    if shift == 0:
        return im
    canvas = blank()
    overlay = Image.fromarray(arr, "RGBA")
    paste_centered(canvas, overlay, overlay.width / 2, overlay.height / 2 + shift)
    return canvas


def punch_paws(block: Image.Image, pug: Image.Image) -> Image.Image:
    """Keep tan/cream paws visible when the ledge overlay sits on the base."""
    b = np.array(block.convert("RGBA"))
    p = np.array(pug.convert("RGBA"))
    rgb = p[..., :3].astype(np.int16)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    lum = rgb.mean(axis=2)
    rows = np.arange(p.shape[0])[:, None]
    fur = (p[..., 3] > 80) & (chroma > 25) & (lum > 90) & (rows >= 618) & (rows <= 648)
    # Same peeking pose on every base: punch the known paw boxes too.
    boxes = np.zeros(p.shape[:2], dtype=bool)
    boxes[618:645, 260:400] = True
    boxes[618:645, 640:780] = True
    paws = fur | (boxes & (p[..., 3] > 80) & (chroma > 18))
    paws = paws | _neighbors8(paws)
    b[paws, 3] = 0
    return Image.fromarray(clear_transparent(b), "RGBA")


def extract_ears(pug: Image.Image) -> Image.Image:
    """Floppy side lobes, redrawn over hats so the brim tucks under them.

    Stay outside the crown (x 385–640) and above the eyes (y ~330) so this
    overlay cannot paint fur over the hat's center or the pupils.
    """
    arr = np.array(pug.convert("RGBA"))
    mask = np.zeros(arr.shape[:2], dtype=bool)
    mask[208:328, 240:388] = arr[208:328, 240:388, 3] > 12
    mask[208:332, 638:840] = arr[208:332, 638:840, 3] > 12
    out = np.zeros_like(arr)
    out[mask] = arr[mask]
    return Image.fromarray(clear_transparent(out), "RGBA")


def hat_crown(hat: Image.Image, pug: Image.Image) -> Image.Image:
    """Forehead slice of a hat, drawn after the pug so the brim sits on the crown.

    The full hat is drawn behind the pug (ears stay in front). This overlay puts
    the hat back on the skull, stopping short of the floppy lobes.
    """
    arr = np.array(hat.convert("RGBA"))
    pug_a = np.array(pug.convert("RGBA"))[..., 3] > 12
    h, w = arr.shape[:2]
    yy = np.arange(h)[:, None]
    xx = np.arange(w)[None, :]
    # Concept art tucks the brim under the inner ear around x 320 / 700.
    ear = ((xx < 322) | (xx > 702)) & (yy >= 200) & (yy <= 332)
    crown = pug_a & ~ear & (yy <= 314)
    # Fade the last few rows so the brim doesn't stamp a hard cut on the brow.
    dist_y = np.clip((314 - yy) / 8.0, 0.0, 1.0)
    # Soften the ear junction so the hat doesn't end on a vertical line.
    left = np.clip((xx - 322) / 16.0, 0.0, 1.0)
    right = np.clip((702 - xx) / 16.0, 0.0, 1.0)
    out = arr.copy().astype(np.float32)
    out[..., 3] *= crown.astype(np.float32) * dist_y * left * right
    return Image.fromarray(clear_transparent(np.clip(out, 0, 255).astype(np.uint8)), "RGBA")


def extract_paws(pug: Image.Image) -> Image.Image:
    """The two paws on the ledge — drawn last so clothes wrap behind them.

    Do not walk onto the baked-in wall or across the muzzle between the paws;
    those pixels would punch holes in collars and redraw the ledge on top.
    """
    arr = np.array(pug.convert("RGBA"))
    rgb = arr[..., :3].astype(np.int16)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    lum = rgb.mean(axis=2)
    alpha = arr[..., 3] > 12
    rows = np.arange(arr.shape[0])[:, None]
    cols = np.arange(arr.shape[1])[None, :]
    wallish = (chroma <= 24) & (lum >= 70) & (lum <= 220) & (rows >= WALL_TOP - 6)
    seed = np.zeros(arr.shape[:2], dtype=bool)
    seed[604:WALL_TOP + 10, 248:412] = alpha[604:WALL_TOP + 10, 248:412]
    seed[604:WALL_TOP + 10, 628:800] = alpha[604:WALL_TOP + 10, 628:800]
    seed &= ~wallish
    walk = alpha & ~wallish
    walk[:, 430:605] = False
    filled = seed.copy()
    for _ in range(16):
        grow = _neighbors8(filled) & walk & ~filled
        grow[:598] = False
        grow[654:] = False
        if not grow.any():
            break
        filled |= grow
    outline = alpha & (lum < 60) & ~wallish & (rows >= 598) & (rows <= 652)
    filled |= _neighbors8(filled) & outline
    filled &= ~((cols >= 430) & (cols <= 605))
    filled[:598] = False
    filled[654:] = False
    out = np.zeros_like(arr)
    out[filled] = arr[filled]
    return Image.fromarray(clear_transparent(out), "RGBA")


def feather_front(full: Image.Image, split_y: int, fade: int = 14) -> Image.Image:
    """Lower half of a neck loop, with a soft top so it doesn't look sliced."""
    arr = np.array(full.convert("RGBA")).astype(np.float32)
    rows = np.arange(arr.shape[0], dtype=np.float32)[:, None]
    ramp = np.clip((rows - (split_y - fade)) / fade, 0.0, 1.0)
    arr[..., 3] *= ramp
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")


def body_front_strap(
    full: Image.Image,
    pug: Image.Image,
    paws: Image.Image,
    split_y: int,
) -> Image.Image:
    """Hangings over the wall, with paws punched out.

    The full loop stays behind the pug. This overlay is only the lower strap
    so the buckle / knot / pendant can drape the ledge without covering the face.
    """
    del pug
    lower = feather_front(full, split_y, fade=5)
    return punch_mask(lower, paws, dilate=10)


def punch_mask(overlay: Image.Image, mask_src: Image.Image, dilate: int = 3) -> Image.Image:
    """Knock a silhouette (paws, etc.) out of an overlay."""
    overlay_arr = np.array(overlay.convert("RGBA"))
    mask = np.array(mask_src.convert("RGBA"))[..., 3] > 12
    for _ in range(dilate):
        mask = mask | _neighbors8(mask)
    overlay_arr[mask, 3] = 0
    return Image.fromarray(clear_transparent(overlay_arr), "RGBA")


def blank() -> Image.Image:
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))


def fringe_count(im: Image.Image) -> int:
    arr = np.array(im.convert("RGBA"))
    rgb = arr[..., :3].astype(np.int16)
    lum = rgb.mean(axis=2)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    opaque = arr[..., 3] > 8
    edge = opaque & _neighbors4(~opaque) & (chroma <= 36) & (lum >= 80)
    return int(edge.sum())


def save(im: Image.Image, rel: str) -> None:
    path = DST / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path)
    arr = np.array(im)
    print(
        f"  {rel} opaque={((arr[..., 3] > 12).mean()*100):.1f}% "
        f"halo={fringe_count(im)}"
    )


def sticker_from(src_name: str) -> Image.Image:
    return content_crop(defringe(knock_all_white(Image.open(SRC / src_name)), **DEFRINGE_OVERLAY))


# Hats sit on the crown: (source, width, brim-bottom-y, max-height).
# Eyes start ~330. Wide brims tuck under the floppy ears (x ~240–388 / 638–840).
HATS = {
    "hat/hat-beanie.png": ("hat-only-beanie.png", 450, 306, 285),
    "hat/hat-crown.png": ("hat-only-crown.png", 250, 272, None),
    "hat/hat-snapback.png": ("hat-only-snapback.png", 460, 308, 250),
    "hat/hat-newsie.png": ("hat-only-newsie.png", 450, 304, 210),
    "hat/hat-hardhat.png": ("hat-only-hardhat.png", 450, 306, 220),
}

# Neck loops: (source, width, center-y, front-split-y).
# Full item is drawn behind the pug; the lower front is redrawn over the
# wall so the buckle / knot / pendant drapes the ledge. Paws sit on top.
BODIES = {
    "body/body-bandana.png": ("body-bandana.png", 340, 588, 612),
    "body/body-collar.png": ("body-collar.png", 360, 592, 614),
    "body/body-hoodie.png": ("body-hoodie.png", 420, 590, 612),
    "body/body-gold-chain.png": ("body-gold-chain.png", 360, 585, 608),
}

ACCESSORIES = {
    "accessory/acc-sunglasses.png": ("acc-sunglasses.png", "eyes", 300, 412),
    "accessory/acc-monocle.png": ("acc-monocle.png", "eye", 118, 400),
    "accessory/acc-coffee.png": ("acc-coffee.png", "ledge", 128, 622),
    "accessory/acc-bone.png": ("acc-bone.png", "ledge", 170, 618),
    "accessory/acc-blocks.png": ("acc-blocks.png", "ledge", 168, 624),
}

LEDGE_X = 868

BASES = {
    "base/base-fawn-peek.png": "base-fawn-peek.png",
    "base/base-cream-peek.png": "base-cream-peek.png",
    "base/base-black-peek.png": "base-black-peek.png",
}

BLOCKS = {
    "block/block-concrete.png": "block-concrete.png",
    "block/block-brownstone.png": "block-brownstone.png",
    "block/block-crate.png": "block-crate.png",
    "block/block-gold.png": "block-gold.png",
}


def prepare() -> None:
    print("Bases (edge flood-fill + defringe)…")
    boosts = {
        "base/base-fawn-peek.png": ((214, 168, 128), 0.22),
        "base/base-cream-peek.png": ((228, 186, 142), 0.38),
        "base/base-black-peek.png": None,
    }
    for dest, src in BASES.items():
        prepared = seal_outline(defringe(flood_white(Image.open(SRC / src)), **DEFRINGE_BASE))
        extra = boosts[dest]
        if extra:
            prepared = boost_fill(prepared, extra[0], extra[1])
        save(prepared, dest)

    print("Blocks (edge flood-fill + defringe)…")
    pug_ref = Image.open(DST / "base/base-fawn-peek.png")
    for dest, src in BLOCKS.items():
        prepared = align_top(
            seal_outline(defringe(flood_white(Image.open(SRC / src)), **DEFRINGE_BASE)),
            WALL_TOP,
        )
        save(punch_paws(prepared, pug_ref), dest)

    print("Hats (crop + place on crown)…")
    pug_ref = Image.open(DST / "base/base-fawn-peek.png")
    for dest, (src, width, bottom, max_height) in HATS.items():
        fitted = fit_width(sticker_from(src), width, max_height)
        canvas = blank()
        paste_bottom(canvas, fitted, 512, bottom)
        full = seal_outline(canvas)
        save(full, dest)
        save(hat_crown(full, pug_ref), dest.replace(".png", "-crown.png"))

    print("Body (full loop + front strap)…")
    pug_ref = Image.open(DST / "base/base-fawn-peek.png")
    paw_union = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    for dest in BASES:
        pug = Image.open(DST / dest)
        paw_union = Image.alpha_composite(paw_union, extract_paws(pug))
    for dest, (src, width, cy, split_y) in BODIES.items():
        fitted = fit_width(sticker_from(src), width)
        canvas = blank()
        paste_centered(canvas, fitted, 512, cy)
        full = seal_outline(canvas)
        save(full, dest)
        front = body_front_strap(full, pug_ref, paw_union, split_y)
        front_rel = dest.replace(".png", "-front.png")
        save(front, front_rel)

    print("Pug foregrounds (ears over hats, paws over clothes)…")
    for dest in BASES:
        pug = Image.open(DST / dest)
        color = Path(dest).stem.split("-")[1]
        save(extract_ears(pug), f"base/front-ears-{color}.png")
        save(extract_paws(pug), f"base/front-paws-{color}.png")

    print("Accessories…")
    for dest, (src, kind, width, cy) in ACCESSORIES.items():
        fitted = fit_width(sticker_from(src), width)
        canvas = blank()
        if kind == "eye":
            cx = 430
        elif kind == "ledge":
            cx = LEDGE_X
            cy = 638
        else:
            cx = 516
        paste_centered(canvas, fitted, cx, cy)
        save(seal_outline(canvas), dest)


def composite(layers: list[str], bg: tuple[int, int, int] | None = None) -> Image.Image:
    if bg is None:
        canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    else:
        canvas = Image.new("RGBA", (SIZE, SIZE), (*bg, 255))
    for rel in layers:
        layer = Image.open(DST / rel).convert("RGBA")
        if layer.size != (SIZE, SIZE):
            layer = layer.resize((SIZE, SIZE), Image.Resampling.LANCZOS)
        canvas = Image.alpha_composite(canvas, layer)
    return canvas


def worn_stack(
    background: str,
    base: str,
    *,
    block: str | None = None,
    body: str | None = None,
    hat: str | None = None,
    accessory: str | None = None,
) -> Image.Image:
    """Studio/generator draw order: clothes wrap the neck, hats tuck behind ears."""
    color = Path(base).stem.split("-")[1]
    layers = [background]
    if body:
        layers.append(body)
    if hat:
        layers.append(hat)
    layers.append(base)
    if block:
        layers.append(block)
    if body:
        front = body.replace(".png", "-front.png")
        if (DST / front).exists():
            layers.append(front)
    if hat:
        crown = hat.replace(".png", "-crown.png")
        if (DST / crown).exists():
            layers.append(crown)
    if accessory:
        layers.append(accessory)
    layers.append(f"base/front-paws-{color}.png")
    return composite(layers)


def _font(size: int) -> ImageFont.ImageFont:
    for path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def labeled_tile(image: Image.Image, label: str, tile: int = 320) -> Image.Image:
    thumb = image.resize((tile, tile), Image.Resampling.LANCZOS).convert("RGB")
    draw = ImageDraw.Draw(thumb)
    font = _font(16)
    draw.rectangle((0, tile - 28, tile, tile), fill=(8, 8, 8))
    draw.text((8, tile - 24), label, fill=(255, 255, 255), font=font)
    return thumb


def grid(tiles: list[Image.Image], columns: int, path: Path) -> None:
    if not tiles:
        return
    tile_w, tile_h = tiles[0].size
    rows = (len(tiles) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * tile_w, rows * tile_h), (12, 12, 12))
    for i, tile in enumerate(tiles):
        x = (i % columns) * tile_w
        y = (i // columns) * tile_h
        sheet.paste(tile, (x, y))
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path, "PNG")
    print("sheet", path)


def test_sheet() -> None:
    TEST_DIR.mkdir(parents=True, exist_ok=True)
    teal = (18, 78, 92)
    crimson = (140, 28, 48)

    tiles: list[Image.Image] = []
    for name, rel in [
        ("fawn / teal", "base/base-fawn-peek.png"),
        ("cream / teal", "base/base-cream-peek.png"),
        ("black / teal", "base/base-black-peek.png"),
        ("fawn / crimson", "base/base-fawn-peek.png"),
        ("cream / crimson", "base/base-cream-peek.png"),
        ("black / crimson", "base/base-black-peek.png"),
    ]:
        bg = teal if "teal" in name else crimson
        tiles.append(labeled_tile(composite([rel], bg), name))
    grid(tiles, 3, TEST_DIR / "halo-check.png")

    hat_tiles = []
    for dest in HATS:
        label = Path(dest).stem
        img = worn_stack("background/bg-stoop-day.png", "base/base-fawn-peek.png", hat=dest)
        hat_tiles.append(labeled_tile(img, label))
        img.convert("RGB").save(TEST_DIR / f"{label}.jpg", "JPEG", quality=90)
    grid(hat_tiles, 5, TEST_DIR / "hats.png")

    block_tiles = []
    for dest in BLOCKS:
        label = Path(dest).stem
        img = worn_stack(
            "background/bg-stoop-day.png",
            "base/base-fawn-peek.png",
            block=dest,
            hat="hat/hat-beanie.png",
        )
        block_tiles.append(labeled_tile(img, label))
        img.convert("RGB").save(TEST_DIR / f"{label}.jpg", "JPEG", quality=90)
    grid(block_tiles, 4, TEST_DIR / "blocks.png")

    body_tiles = []
    for dest in BODIES:
        label = Path(dest).stem
        img = worn_stack(
            "background/bg-brownstone.png",
            "base/base-fawn-peek.png",
            body=dest,
        )
        body_tiles.append(labeled_tile(img, label))
        img.convert("RGB").save(TEST_DIR / f"{label}.jpg", "JPEG", quality=90)
    grid(body_tiles, 4, TEST_DIR / "bodies.png")

    acc_tiles = []
    for dest in ACCESSORIES:
        label = Path(dest).stem
        img = worn_stack(
            "background/bg-rooftop-sunset.png",
            "base/base-cream-peek.png",
            accessory=dest,
        )
        acc_tiles.append(labeled_tile(img, label))
        img.convert("RGB").save(TEST_DIR / f"{label}.jpg", "JPEG", quality=90)
    grid(acc_tiles, 5, TEST_DIR / "accessories.png")

    combos = [
        ("fawn-beanie-bandana.jpg", dict(background="background/bg-brownstone.png", base="base/base-fawn-peek.png", body="body/body-bandana.png", hat="hat/hat-beanie.png")),
        ("cream-newsie-coffee.jpg", dict(background="background/bg-rooftop-sunset.png", base="base/base-cream-peek.png", hat="hat/hat-newsie.png", accessory="accessory/acc-coffee.png")),
        ("black-crown-chain.jpg", dict(background="background/bg-neon-night.png", base="base/base-black-peek.png", body="body/body-gold-chain.png", hat="hat/hat-crown.png")),
        ("fawn-hardhat-blocks.jpg", dict(background="background/bg-stoop-day.png", base="base/base-fawn-peek.png", hat="hat/hat-hardhat.png", accessory="accessory/acc-blocks.png")),
        ("black-snap-shades.jpg", dict(background="background/bg-subway.png", base="base/base-black-peek.png", hat="hat/hat-snapback.png", accessory="accessory/acc-sunglasses.png")),
        ("cream-monocle-collar.jpg", dict(background="background/bg-chain-green.png", base="base/base-cream-peek.png", body="body/body-collar.png", accessory="accessory/acc-monocle.png")),
        ("fawn-hoodie-bone.jpg", dict(background="background/bg-cream-brick.png", base="base/base-fawn-peek.png", body="body/body-hoodie.png", accessory="accessory/acc-bone.png")),
        ("black-bandana-shades.jpg", dict(background="background/bg-rooftop-sunset.png", base="base/base-black-peek.png", body="body/body-bandana.png", accessory="accessory/acc-sunglasses.png")),
        ("fawn-snap-hoodie-coffee.jpg", dict(background="background/bg-brownstone.png", base="base/base-fawn-peek.png", body="body/body-hoodie.png", hat="hat/hat-snapback.png", accessory="accessory/acc-coffee.png")),
        ("cream-beanie-collar-shades.jpg", dict(background="background/bg-stoop-day.png", base="base/base-cream-peek.png", body="body/body-collar.png", hat="hat/hat-beanie.png", accessory="accessory/acc-sunglasses.png")),
    ]
    stack_tiles = []
    for name, layers in combos:
        canvas = worn_stack(layers["background"], layers["base"], block=None, body=layers.get("body"), hat=layers.get("hat"), accessory=layers.get("accessory"))
        out = TEST_DIR / name
        canvas.convert("RGB").save(out, "JPEG", quality=90)
        stack_tiles.append(labeled_tile(canvas, name.replace(".jpg", "")))
        print("test", out)
    grid(stack_tiles, 5, TEST_DIR / "stacks.png")


if __name__ == "__main__":
    import os

    if os.environ.get("FORCE_PREPARE") != "1":
        raise SystemExit(
            "Refusing to run: this recrops trait art away from the gallery mint look. "
            "Use python3 scripts/generate_collection.py. Set FORCE_PREPARE=1 only if you "
            "intentionally want the worn-stack experiment."
        )
    prepare()
    test_sheet()
