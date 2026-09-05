#!/usr/bin/env python3
"""Paint Galleria On Ink — 500 independent 1:1 loops, each an open edition.

This orchestrator does not draw. It loads one painter per artwork from
scripts/atelier/works/, then writes APNG, GIF, CSV, brand, and site catalog.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import sys
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from atelier.catalog import load_works
from gif_bake import save_loop_gif
from paint_kit import DURATION_MS, FRAMES, SIZE, save_apng, save_image

PUBLIC_DIR = ROOT / "public" / "galleria"
THUMB_DIR = PUBLIC_DIR / "thumbs"
BRAND_DIR = ROOT / "public" / "brand"
META_DIR = ROOT / "public" / "metadata"
SRC_DATA = ROOT / "src" / "data"
OUT = ROOT / "generated" / "galleria"
IMAGE_DIR = OUT / "images"
GIF_DIR = OUT / "gifs"
JSON_DIR = OUT / "json"

COLLECTION_STORY = (
    "Galleria On Ink.\n\n"
    "A salon of 500 unique looping paintings on Ink. Each work invents its own "
    "medium, palette, silhouette, and motion. Neighboring tokens are not siblings. "
    "There is no trait stack and no shared character.\n\n"
    "Every artwork is an open edition. The composition is 1:1. The mint is not.\n\n"
    "Twelve frames, ninety milliseconds, 512×512. Minting on Ink (chain ID 57073). Gas is ETH."
)

CSV_FIELDS = [
    "tokenID",
    "name",
    "description",
    "file_name",
    "attributes[Medium]",
    "attributes[Motion]",
    "attributes[Palette]",
    "attributes[Edition]",
]
BRAND_IDS = (1, 3, 8, 10, 16, 22, 31, 50)
OPENSEA_LIMIT_BYTES = 10 * 1024 * 1024 * 1024


def _font(size: int):
    for path in ("C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def render_work(painter) -> list[Image.Image]:
    frames = []
    for index in range(FRAMES):
        frame = painter(index).convert("RGBA").resize((SIZE, SIZE), Image.Resampling.LANCZOS)
        frames.append(frame)
    return frames


def write_catalog(works: list[dict]) -> None:
    SRC_DATA.mkdir(parents=True, exist_ok=True)
    payload = [
        {
            "id": work["id"],
            "slug": work["slug"],
            "title": work["title"],
            "image": f"/galleria/{work['id']}.png",
            "description": work["description"],
            "attributes": [
                {"trait_type": "Medium", "value": work["medium"]},
                {"trait_type": "Motion", "value": work["motion"]},
                {"trait_type": "Palette", "value": work["palette"]},
                {"trait_type": "Edition", "value": "Open"},
            ],
        }
        for work in works
    ]
    (SRC_DATA / "galleria-works.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_metadata(works: list[dict]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    JSON_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    stats: Counter[str] = Counter()
    for work in works:
        meta = {
            "name": work["title"],
            "description": work["description"],
            "image": f"{work['id']}.gif",
            "external_url": f"/galleria/{work['id']}",
            "attributes": [
                {"trait_type": "Medium", "value": work["medium"]},
                {"trait_type": "Motion", "value": work["motion"]},
                {"trait_type": "Palette", "value": work["palette"]},
                {"trait_type": "Edition", "value": "Open"},
            ],
            "animation_loop": True,
            "compiler": "Galleria On Ink atelier",
        }
        (JSON_DIR / f"{work['id']}.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
        rows.append(
            {
                "tokenID": work["id"],
                "name": work["title"],
                "description": work["description"],
                "file_name": f"{work['id']}.gif",
                "attributes[Medium]": work["medium"],
                "attributes[Motion]": work["motion"],
                "attributes[Palette]": work["palette"],
                "attributes[Edition]": "Open",
            }
        )
        stats[f"Medium:{work['medium']}"] += 1
        stats[f"Motion:{work['motion']}"] += 1
        stats[f"Palette:{work['palette']}"] += 1
        stats["Edition:Open"] += 1
    csv_path = OUT / "opensea-metadata.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    shutil.copyfile(csv_path, OUT / "GOI-opensea-drop.csv")
    gif_bytes = sum(path.stat().st_size for path in GIF_DIR.glob("*.gif")) if GIF_DIR.exists() else 0
    digest = hashlib.sha256(csv_path.read_bytes()).hexdigest()
    (OUT / "provenance.json").write_text(
        json.dumps(
            {
                "hash": digest,
                "count": len(works),
                "frames": FRAMES,
                "durationMs": DURATION_MS,
                "size": SIZE,
                "bytes": gif_bytes,
                "openseaLimitBytes": OPENSEA_LIMIT_BYTES,
                "underOpenseaLimit": gif_bytes < OPENSEA_LIMIT_BYTES,
                "chain": "ink",
                "chainId": 57073,
                "edition": "open",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (OUT / "stats.json").write_text(json.dumps(dict(stats), indent=2) + "\n", encoding="utf-8")
    (OUT / "README.md").write_text(
        "# Galleria On Ink OpenSea kit\n\n"
        f"{len(works)} unique looping paintings at {SIZE}×{SIZE}, {FRAMES} frames, "
        f"{DURATION_MS}ms. Each artwork is an open edition.\n\n"
        "## Collection fields\n\n"
        "- Name: `Galleria On Ink`\n"
        "- Symbol: `GOI`\n"
        "- Category: Art\n"
        "- Chain: Ink (`57073`)\n"
        f"- Works: `{len(works)}` open editions (one item per painting; do not set unique 1:1 supply)\n"
        "- Mint: `0.008 ETH`\n"
        "- Creator fee: `7.5%` (set your wallet — `public/metadata/galleria.json` still has a zero address)\n\n"
        "## Paste this as the collection description\n\n"
        "Same file: `public/metadata/galleria-description.txt`\n\n"
        "```\n"
        + COLLECTION_STORY
        + "\n```\n\n"
        "## Listing images\n\n"
        "No type on the marketplace images.\n\n"
        "| Use | File | Size |\n"
        "|---|---|---|\n"
        "| Logo | `public/brand/logo-galleria.png` | 512×512, 1:1 |\n"
        "| Featured | `public/brand/featured-galleria.jpg` | 1200×800, 3:2 |\n"
        "| OpenSea banner | `public/brand/banner-galleria-opensea.jpg` | 2800×700, 4:1 |\n"
        "| Collection GIF | `public/brand/collection-galleria.gif` | 1000×1000, 12-frame loop |\n"
        "| Site hero (not the OpenSea banner) | `public/brand/banner-galleria.png` | 1500×560 |\n\n"
        "## Open edition upload\n\n"
        "1. In OpenSea Studio, create an Open Edition collection on Ink (chain ID 57073).\n"
        f"2. Add {len(works)} open-edition items — one per artwork. Do not set unique 1:1 supply.\n"
        f"3. Upload every file in `gifs/` (`1.gif`–`{len(works)}.gif`).\n"
        "4. Upload `GOI-opensea-drop.csv` (or `opensea-metadata.csv`). "
        "The CSV uses OpenSea Studio headers: `tokenID`, `name`, `description`, "
        "`file_name`, and `attributes[Trait]`.\n"
        "5. Paste the collection description, upload the listing images, set mint to 0.008 ETH, then publish.\n\n"
        "OpenSea plays GIF, not APNG. The site keeps the APNGs in `public/galleria/`.\n",
        encoding="utf-8",
    )
    META_DIR.mkdir(parents=True, exist_ok=True)
    (META_DIR / "galleria-description.txt").write_text(COLLECTION_STORY + "\n", encoding="utf-8")
    (META_DIR / "galleria.json").write_text(
        json.dumps(
            {
                "name": "Galleria On Ink",
                "symbol": "GOI",
                "description": COLLECTION_STORY.replace("\n", " "),
                "image": "/brand/collection-galleria.gif",
                "featured_image": "/brand/featured-galleria.jpg",
                "banner_image": "/brand/banner-galleria.png",
                "opensea_banner_image": "/brand/banner-galleria-opensea.jpg",
                "external_link": "/galleria",
                "seller_fee_basis_points": 750,
                "fee_recipient": "0x0000000000000000000000000000000000000000",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def _rounded(portrait: Image.Image, size: int, radius: int) -> Image.Image:
    face = portrait.resize((size, size), Image.Resampling.LANCZOS).convert("RGBA")
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=255)
    face.putalpha(Image.composite(face.split()[-1], Image.new("L", (size, size), 0), mask))
    return face


def _place(canvas: Image.Image, portrait: Image.Image, x: int, y: int, size: int, radius: int) -> None:
    face = _rounded(portrait, size, radius)
    shadow = Image.new("RGBA", (size + 28, size + 28), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((10, 16, size + 10, size + 20), radius=radius, fill=(8, 8, 10, 120))
    canvas.alpha_composite(shadow, (x - 10, y - 8))
    canvas.alpha_composite(face, (x, y))


def load_apng_frames(path: Path) -> list[Image.Image]:
    apng = Image.open(path)
    frames = []
    index = 0
    while True:
        apng.seek(index)
        frames.append(apng.convert("RGBA"))
        index += 1
        if index >= getattr(apng, "n_frames", 1):
            break
    return frames or [apng.convert("RGBA")]


def build_brand(frames_by_id: dict[int, list[Image.Image]]) -> None:
    BRAND_DIR.mkdir(parents=True, exist_ok=True)
    grid = Image.new("RGBA", (SIZE, SIZE), (18, 18, 20, 255))
    picks = (1, 8, 10, 22)
    for i, work_id in enumerate(picks):
        tile = frames_by_id[work_id][0].resize((256, 256), Image.Resampling.LANCZOS)
        grid.paste(tile, ((i % 2) * 256, (i // 2) * 256))
    save_image(grid, BRAND_DIR / "logo-galleria.png")

    hero = Image.new("RGBA", (1500, 560), (16, 16, 18, 255))
    for i, work_id in enumerate((1, 3, 8, 16, 22)):
        face = frames_by_id[work_id][0].resize((260, 260), Image.Resampling.LANCZOS)
        hero.alpha_composite(face, (40 + i * 292, 170))
    draw = ImageDraw.Draw(hero)
    draw.text((48, 36), "GALLERIA ON INK", font=_font(56), fill=(244, 240, 232, 255))
    draw.text((52, 108), "500 open editions. No two share a medium.", font=_font(26), fill=(180, 176, 168, 255))
    hero.convert("RGB").save(BRAND_DIR / "banner-galleria.png", quality=94)

    portraits = [frames_by_id[work_id][0] for work_id in (1, 8, 22, 31, 50) if work_id in frames_by_id]
    wash = Image.new("RGBA", (2800, 700), (16, 16, 18, 255))
    size = 560
    overlap = 90
    total = size * len(portraits) - overlap * max(len(portraits) - 1, 0)
    start_x = (2800 - total) // 2
    y = (700 - size) // 2 + 18
    for index, portrait in enumerate(portraits):
        _place(wash, portrait, start_x + index * (size - overlap), y, size, 48)
    wash.convert("RGB").save(BRAND_DIR / "banner-galleria-opensea.jpg", quality=90)

    featured = Image.new("RGBA", (1200, 800), (16, 16, 18, 255))
    if portraits:
        _place(featured, portraits[0], 70, 120, 540, 56)
    if len(portraits) > 1:
        _place(featured, portraits[1], 560, 140, 540, 56)
    featured.convert("RGB").save(BRAND_DIR / "featured-galleria.jpg", quality=90)
    save_loop_gif(
        [frame.resize((1000, 1000), Image.Resampling.LANCZOS) for frame in frames_by_id[8]],
        BRAND_DIR / "collection-galleria.gif",
        DURATION_MS,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", type=int, nargs="*", help="Paint only these work ids")
    parser.add_argument("--from-id", type=int, help="Paint this id through the last work")
    parser.add_argument("--kit", action="store_true", help="Rebuild listing images and the OpenSea kit only")
    args = parser.parse_args()

    loaded = load_works()
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    THUMB_DIR.mkdir(parents=True, exist_ok=True)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    GIF_DIR.mkdir(parents=True, exist_ok=True)

    frames_by_id: dict[int, list[Image.Image]] = {}
    catalog: list[dict] = []
    for spec, painter in loaded:
        catalog.append(
            {
                "id": spec.id,
                "slug": spec.slug,
                "title": spec.title,
                "description": spec.description,
                "medium": spec.medium,
                "motion": spec.motion,
                "palette": spec.palette,
            }
        )
        skip = False
        if args.kit:
            skip = True
        if args.only and spec.id not in args.only:
            skip = True
        if args.from_id and spec.id < args.from_id:
            skip = True
        if skip:
            existing = PUBLIC_DIR / f"{spec.id}.png"
            thumb = THUMB_DIR / f"{spec.id}.jpg"
            if existing.exists() and not thumb.exists():
                Image.open(existing).convert("RGB").resize((320, 320), Image.Resampling.LANCZOS).save(
                    thumb, quality=86
                )
            continue
        print(f"painting {spec.id:03d}  {spec.title}  [{spec.medium}]")
        frames = render_work(painter)
        if spec.id in BRAND_IDS:
            frames_by_id[spec.id] = frames
        save_apng(frames, PUBLIC_DIR / f"{spec.id}.png")
        save_apng(frames, IMAGE_DIR / f"{spec.id}.png")
        save_loop_gif(frames, GIF_DIR / f"{spec.id}.gif", DURATION_MS)
        frames[0].convert("RGB").resize((320, 320), Image.Resampling.LANCZOS).save(
            THUMB_DIR / f"{spec.id}.jpg", quality=86
        )
        if spec.id not in frames_by_id:
            del frames

    write_catalog(catalog)
    write_metadata(catalog)
    for work_id in BRAND_IDS:
        if work_id in frames_by_id:
            continue
        path = PUBLIC_DIR / f"{work_id}.png"
        if path.exists():
            frames_by_id[work_id] = load_apng_frames(path)
    if all(work_id in frames_by_id for work_id in BRAND_IDS):
        build_brand(frames_by_id)
    print(f"wrote {len(catalog)} galleria works")


if __name__ == "__main__":
    main()
