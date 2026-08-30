#!/usr/bin/env python3
"""Turn painted magenta-key art into seated 1024 PNG trait layers."""

from __future__ import annotations

import shutil
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SIZE = 1024
WALL_TOP = 648
RAW = ROOT / "generated" / "art-raw"
TRAITS = ROOT / "public" / "traits"
CURSOR_ASSETS = Path.home() / ".cursor" / "projects" / "c-Users-chiku-Projects-nft-gallery" / "assets"

# Raw filename -> (dest relative, how to seat the opaque pixels)
# seat: "bg" | "head" | "hat" | "face" | "monocle" | "neck" | "wall" | "paws" | "ledge-left" | "ledge-right"
FILES: dict[str, tuple[str, str]] = {
    "potb-bg-brownstone.png": ("background/bg-brownstone.png", "bg"),
    "potb-bg-stoop-day.png": ("background/bg-stoop-day.png", "bg"),
    "potb-bg-cream-brick.png": ("background/bg-cream-brick.png", "bg"),
    "potb-bg-rooftop.png": ("background/bg-rooftop-sunset.png", "bg"),
    "potb-bg-subway.png": ("background/bg-subway.png", "bg"),
    "potb-bg-court.png": ("background/bg-court-dusk.png", "bg"),
    "potb-bg-neon.png": ("background/bg-neon-night.png", "bg"),
    "potb-bg-chain-green.png": ("background/bg-chain-green.png", "bg"),
    "potb-base-fawn.png": ("base/base-fawn-peek.png", "head"),
    "potb-base-cream.png": ("base/base-cream-peek.png", "head"),
    "potb-base-black.png": ("base/base-black-peek.png", "head"),
    "potb-paws-fawn.png": ("base/front-paws-fawn.png", "paws"),
    "potb-paws-cream.png": ("base/front-paws-cream.png", "paws"),
    "potb-paws-black.png": ("base/front-paws-black.png", "paws"),
    "potb-wall-default.png": ("base/wall-default.png", "wall"),
    "potb-wall-concrete.png": ("block/block-concrete.png", "wall"),
    "potb-wall-brownstone.png": ("block/block-brownstone.png", "wall"),
    "potb-wall-crate.png": ("block/block-crate.png", "wall"),
    "potb-wall-gold.png": ("block/block-gold.png", "wall"),
    "potb-hat-beanie.png": ("hat/hat-beanie.png", "hat"),
    "potb-hat-newsie.png": ("hat/hat-newsie.png", "hat"),
    "potb-hat-snapback.png": ("hat/hat-snapback.png", "hat"),
    "potb-hat-hardhat.png": ("hat/hat-hardhat.png", "hat"),
    "potb-hat-crown.png": ("hat/hat-crown.png", "hat"),
    "potb-body-bandana.png": ("body/body-bandana.png", "neck"),
    "potb-body-collar.png": ("body/body-collar.png", "neck"),
    "potb-body-hoodie.png": ("body/body-hoodie.png", "neck"),
    "potb-body-gold-chain.png": ("body/body-gold-chain.png", "neck"),
    "potb-acc-sunglasses.png": ("accessory/acc-sunglasses.png", "face"),
    "potb-acc-monocle.png": ("accessory/acc-monocle.png", "monocle"),
    "potb-acc-coffee.png": ("accessory/acc-coffee.png", "ledge-right"),
    "potb-acc-bone.png": ("accessory/acc-bone.png", "ledge-right"),
    "potb-acc-blocks.png": ("accessory/acc-blocks.png", "ledge-left"),
}


def collect_raw() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    sources = []
    if CURSOR_ASSETS.exists():
        sources.append(CURSOR_ASSETS)
    sources.append(ROOT / "assets")
    for name in FILES:
        dest = RAW / name
        if dest.exists():
            continue
        for folder in sources:
            src = folder / name
            if src.exists():
                shutil.copy2(src, dest)
                break
        if not dest.exists():
            raise FileNotFoundError(f"Missing painted source {name}")


def knock_magenta(im: Image.Image) -> Image.Image:
    im = im.convert("RGBA").resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    arr = np.asarray(im).astype(np.int16)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    magenta = (r > 150) & (b > 150) & (g < 150) & ((r + b) / 2 - g > 40)
    # also knock leftover neon pink fringes
    pink = (r > 200) & (b > 120) & (g < 90)
    alpha = np.where(magenta | pink, 0, arr[:, :, 3])
    # soften the matte one pixel so painted edges do not keep a magenta halo
    solid = alpha > 8
    from numpy.lib.stride_tricks import sliding_window_view

    pad = np.pad(solid.astype(np.uint8), 1)
    neigh = sliding_window_view(pad, (3, 3)).sum(axis=(-1, -2))
    edge = solid & (neigh < 9)
    alpha = np.where(edge, np.minimum(alpha, 180), alpha)
    out = arr.astype(np.uint8)
    out[:, :, 3] = alpha.astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def opaque_mask(im: Image.Image) -> np.ndarray:
    return np.asarray(im)[:, :, 3] > 12


def bbox(mask: np.ndarray) -> tuple[int, int, int, int]:
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return 0, 0, SIZE, SIZE
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def centroid(mask: np.ndarray) -> tuple[float, float]:
    ys, xs = np.where(mask)
    return float(xs.mean()), float(ys.mean())


def translate(im: Image.Image, dx: int, dy: int) -> Image.Image:
    canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    canvas.paste(im, (dx, dy), im)
    return canvas


def scale_about(im: Image.Image, factor: float) -> Image.Image:
    if abs(factor - 1) < 0.02:
        return im
    w, h = im.size
    nw, nh = max(1, int(w * factor)), max(1, int(h * factor))
    scaled = im.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    canvas.paste(scaled, ((w - nw) // 2, (h - nh) // 2), scaled)
    return canvas


def seat(im: Image.Image, kind: str) -> Image.Image:
    if kind == "bg":
        return im.convert("RGBA").resize((SIZE, SIZE), Image.Resampling.LANCZOS)

    cut = knock_magenta(im)
    mask = opaque_mask(cut)
    x0, y0, x1, y1 = bbox(mask)
    cx, cy = centroid(mask)
    bw, bh = x1 - x0 + 1, y1 - y0 + 1

    targets = {
        "head": (512, 400, 520),
        "hat": (512, 235, 400),
        "face": (512, 400, 280),
        "monocle": (430, 400, 180),
        "neck": (512, 612, 380),
        "paws": (512, 640, 360),
        "ledge-left": (200, 620, 220),
        "ledge-right": (820, 620, 200),
        "wall": None,
    }

    if kind == "wall":
        # Stretch/place so the wall top sits on WALL_TOP and fills the bottom.
        crop = cut.crop((0, y0, SIZE, SIZE))
        new_h = SIZE - WALL_TOP
        crop = crop.resize((SIZE, max(new_h, 1)), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        canvas.paste(crop, (0, WALL_TOP), crop)
        return canvas

    tx, ty, max_span = targets[kind]
    span = max(bw, bh)
    factor = min(1.0, max_span / max(span, 1))
    if kind in {"hat", "face", "monocle", "neck", "paws", "ledge-left", "ledge-right"} and span > max_span:
        cut = scale_about(cut, factor)
        mask = opaque_mask(cut)
        cx, cy = centroid(mask)
    dx = int(round(tx - cx))
    dy = int(round(ty - cy))
    return translate(cut, dx, dy)


def write_all() -> None:
    collect_raw()
    for name, (rel, kind) in FILES.items():
        dest = TRAITS / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        seated = seat(Image.open(RAW / name), kind)
        seated.save(dest)
        print(f"wrote {rel}")


def compose(layers: list[str]) -> Image.Image:
    canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    for rel in layers:
        overlay = Image.open(TRAITS / rel).convert("RGBA")
        if overlay.size != (SIZE, SIZE):
            overlay = overlay.resize((SIZE, SIZE), Image.Resampling.LANCZOS)
        canvas = Image.alpha_composite(canvas, overlay)
    return canvas


SIGNATURES = [
    ["background/bg-brownstone.png", "base/base-fawn-peek.png", "body/body-bandana.png", "hat/hat-beanie.png", "base/wall-default.png", "base/front-paws-fawn.png"],
    ["background/bg-neon-night.png", "base/base-black-peek.png", "body/body-gold-chain.png", "hat/hat-crown.png", "base/wall-default.png", "base/front-paws-black.png"],
    ["background/bg-rooftop-sunset.png", "base/base-cream-peek.png", "hat/hat-newsie.png", "base/wall-default.png", "accessory/acc-coffee.png", "base/front-paws-cream.png"],
    ["background/bg-stoop-day.png", "base/base-fawn-peek.png", "hat/hat-hardhat.png", "base/wall-default.png", "accessory/acc-blocks.png", "base/front-paws-fawn.png"],
    ["background/bg-subway.png", "base/base-black-peek.png", "accessory/acc-sunglasses.png", "hat/hat-snapback.png", "base/wall-default.png", "base/front-paws-black.png"],
    ["background/bg-chain-green.png", "base/base-cream-peek.png", "accessory/acc-monocle.png", "body/body-collar.png", "base/wall-default.png", "base/front-paws-cream.png"],
    ["background/bg-cream-brick.png", "base/base-fawn-peek.png", "body/body-hoodie.png", "base/wall-default.png", "accessory/acc-bone.png", "base/front-paws-fawn.png"],
    ["background/bg-rooftop-sunset.png", "base/base-black-peek.png", "accessory/acc-sunglasses.png", "body/body-bandana.png", "base/wall-default.png", "base/front-paws-black.png"],
]


def write_previews() -> None:
    out = ROOT / "generated" / "placement-tests"
    out.mkdir(parents=True, exist_ok=True)
    for i, layers in enumerate(SIGNATURES, start=1):
        compose(layers).convert("RGB").save(out / f"sig-{i:02d}.jpg", quality=92)
        print(f"preview sig-{i:02d}.jpg")


def main() -> int:
    write_all()
    write_previews()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
