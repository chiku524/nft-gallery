#!/usr/bin/env python3
"""Paint Galleria On Ink — 24 independent 1:1 loops, each an open edition.

This orchestrator does not draw. It loads one painter per artwork from
scripts/atelier/works/, then writes APNG, GIF, CSV, brand, and site catalog.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from atelier.catalog import load_works
from gif_bake import save_loop_gif
from paint_kit import DURATION_MS, FRAMES, SIZE, save_apng, save_image

PUBLIC_DIR = ROOT / "public" / "galleria"
BRAND_DIR = ROOT / "public" / "brand"
META_DIR = ROOT / "public" / "metadata"
SRC_DATA = ROOT / "src" / "data"
OUT = ROOT / "generated" / "galleria"
IMAGE_DIR = OUT / "images"
GIF_DIR = OUT / "gifs"
JSON_DIR = OUT / "json"

COLLECTION_STORY = (
    "Galleria On Ink.\n\n"
    "A salon of 24 unique looping paintings on Ink. Each work invents its own "
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
    with (OUT / "opensea-metadata.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    (OUT / "README.md").write_text(
        "# Galleria On Ink OpenSea pack\n\n"
        "24 unique looping paintings at 512×512, 12 frames, 90ms. Each artwork is an open edition.\n\n"
        "Create an OpenSea Open Edition collection on Ink. Upload every file in `gifs/` plus "
        "`opensea-metadata.csv`. OpenSea plays GIF, not APNG. The site keeps the APNGs in "
        "`public/galleria/`.\n",
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


def build_brand(frames_by_id: dict[int, list[Image.Image]]) -> None:
    BRAND_DIR.mkdir(parents=True, exist_ok=True)
    grid = Image.new("RGBA", (SIZE, SIZE), (18, 18, 20, 255))
    picks = (1, 8, 10, 22)
    for i, work_id in enumerate(picks):
        tile = frames_by_id[work_id][0].resize((256, 256), Image.Resampling.LANCZOS)
        grid.paste(tile, ((i % 2) * 256, (i // 2) * 256))
    save_image(grid, BRAND_DIR / "logo-galleria.png")

    banner = Image.new("RGBA", (1500, 560), (16, 16, 18, 255))
    strip = (1, 3, 8, 16, 22)
    for i, work_id in enumerate(strip):
        face = frames_by_id[work_id][0].resize((260, 260), Image.Resampling.LANCZOS)
        banner.alpha_composite(face, (40 + i * 292, 170))
    draw = ImageDraw.Draw(banner)
    draw.text((48, 36), "GALLERIA ON INK", font=_font(56), fill=(244, 240, 232, 255))
    draw.text((52, 108), "24 open editions. No two share a medium.", font=_font(26), fill=(180, 176, 168, 255))
    banner.convert("RGB").save(BRAND_DIR / "banner-galleria.png", quality=94)
    banner.resize((1500, 500), Image.Resampling.LANCZOS).convert("RGB").save(
        BRAND_DIR / "banner-galleria-opensea.jpg", quality=92
    )
    featured = Image.new("RGB", (1000, 1000), (16, 16, 18))
    featured.paste(frames_by_id[8][0].resize((1000, 1000), Image.Resampling.LANCZOS).convert("RGB"))
    featured.save(BRAND_DIR / "featured-galleria.jpg", quality=92)
    save_loop_gif(
        [frame.resize((1000, 1000), Image.Resampling.LANCZOS) for frame in frames_by_id[8]],
        BRAND_DIR / "collection-galleria.gif",
        DURATION_MS,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", type=int, nargs="*", help="Paint only these work ids")
    args = parser.parse_args()

    loaded = load_works()
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    GIF_DIR.mkdir(parents=True, exist_ok=True)

    frames_by_id: dict[int, list[Image.Image]] = {}
    catalog: list[dict] = []
    for spec, painter in loaded:
        if args.only and spec.id not in args.only:
            continue
        print(f"painting {spec.id:02d}  {spec.title}  [{spec.medium}]")
        frames = render_work(painter)
        frames_by_id[spec.id] = frames
        save_apng(frames, PUBLIC_DIR / f"{spec.id}.png")
        save_apng(frames, IMAGE_DIR / f"{spec.id}.png")
        save_loop_gif(frames, GIF_DIR / f"{spec.id}.gif", DURATION_MS)
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

    if args.only:
        return
    write_catalog(catalog)
    write_metadata(catalog)
    build_brand(frames_by_id)
    print(f"wrote {len(catalog)} galleria works")


if __name__ == "__main__":
    main()
