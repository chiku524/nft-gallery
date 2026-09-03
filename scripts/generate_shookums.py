#!/usr/bin/env python3
"""Compose Halloween Shook'ums tokens from layered APNG traits.

Default: 16 signature samples.
Pass --all to shuffle the full 5,555 on the shared 12-frame clock.

OpenSea gets GIFs only (max 10 GB). Studio traits stay 512×512 APNGs in public/shookums-traits/.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import sys
from collections import Counter
from multiprocessing import Pool, cpu_count
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_shookums import (  # noqa: E402
    DURATION_MS,
    FRAMES,
    PREVIEW_DIR,
    SIGNATURES,
    SIZE,
    STACK,
    TRAIT_LABELS,
    TRAIT_SPEC,
    name_of,
    trait_path,
)
from gif_bake import save_loop_gif  # noqa: E402

OUT = ROOT / "generated" / "shookums"
IMAGE_DIR = OUT / "images"
GIF_DIR = OUT / "gifs"
JSON_DIR = OUT / "json"
TOTAL = 5_555
SEED = 2741_5555
DROP_SIZE = 512
GIF_COLORS = 160
OPENSEA_LIMIT_BYTES = 10 * 1024 * 1024 * 1024

_CACHE: dict[tuple[str, str], list[Image.Image]] | None = None
_FORCE = False


def pick(category: str, rng: random.Random) -> str:
    pool = TRAIT_SPEC[category]
    total = sum(max(rarity, 1) for _id, _name, rarity in pool)
    roll = rng.random() * total
    for trait_id, _name, rarity in pool:
        roll -= max(rarity, 1)
        if roll <= 0:
            return trait_id
    return pool[0][0]


def fingerprint(selection: dict[str, str]) -> str:
    return "|".join(f"{key}:{selection[key]}" for key in STACK)


def build_roster(count: int) -> list[dict[str, str]]:
    rng = random.Random(SEED)
    roster = [dict(item) for item in SIGNATURES[: min(len(SIGNATURES), count)]]
    seen = {fingerprint(item) for item in roster}
    while len(roster) < count:
        selection = {category: pick(category, rng) for category in STACK}
        key = fingerprint(selection)
        if key in seen:
            continue
        seen.add(key)
        roster.append(selection)
    return roster


def load_trait_frames(path: Path) -> list[Image.Image]:
    with Image.open(path) as im:
        im.load()
        frames = []
        for i in range(getattr(im, "n_frames", 1)):
            im.seek(i)
            frames.append(im.convert("RGBA").copy())
        return frames


def load_cache() -> dict[tuple[str, str], list[Image.Image]]:
    cache: dict[tuple[str, str], list[Image.Image]] = {}
    for category, traits in TRAIT_SPEC.items():
        for trait_id, _name, _rarity in traits:
            if trait_id == "none":
                continue
            cache[(category, trait_id)] = load_trait_frames(trait_path(category, trait_id))
    return cache


def init_worker(force: bool = False) -> None:
    global _CACHE, _FORCE
    _FORCE = force
    _CACHE = load_cache()


def compose_cached(selection: dict[str, str]) -> list[Image.Image]:
    assert _CACHE is not None
    layers = []
    for category in STACK:
        trait_id = selection[category]
        if trait_id == "none":
            continue
        layers.append(_CACHE[(category, trait_id)])
    out = []
    for i in range(FRAMES):
        canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        for frames in layers:
            canvas = Image.alpha_composite(canvas, frames[i % len(frames)])
        if DROP_SIZE != SIZE:
            canvas = canvas.resize((DROP_SIZE, DROP_SIZE), Image.Resampling.LANCZOS)
        out.append(canvas)
    return out


CSV_FIELDS = [
    "tokenID",
    "name",
    "description",
    "file_name",
    *(f"attributes[{label}]" for _key, label in TRAIT_LABELS),
]


def token_meta(token_id: int, selection: dict[str, str]) -> dict:
    attributes = [
        {"trait_type": label, "value": name_of(key, selection[key])}
        for key, label in TRAIT_LABELS
    ]
    return {
        "name": f"Shook'um #{token_id}",
        "description": "A looping sheet ghost from Halloween Shook'ums. Three bodies. One skeleton. One clock. Minted on Abstract.",
        "image": f"{token_id}.gif",
        "attributes": attributes,
        "animation_loop": True,
        "compiler": "Halloween Shook'ums layer stack",
    }


def drop_csv_row(token_id: int, meta: dict) -> dict:
    row = {
        "tokenID": token_id,
        "name": meta["name"],
        "description": meta["description"],
        "file_name": f"{token_id}.gif",
    }
    for attr in meta["attributes"]:
        row[f"attributes[{attr['trait_type']}]"] = attr["value"]
    return row


def traits_newer_than(gif_path: Path) -> bool:
    if not gif_path.exists() or gif_path.stat().st_size == 0:
        return True
    gif_mtime = gif_path.stat().st_mtime
    for category, traits in TRAIT_SPEC.items():
        for trait_id, _name, _rarity in traits:
            if trait_id == "none":
                continue
            path = trait_path(category, trait_id)
            if path.exists() and path.stat().st_mtime > gif_mtime:
                return True
    return False


def bake_one(job: tuple[int, dict[str, str]]) -> tuple[int, dict, int]:
    token_id, selection = job
    gif_dest = GIF_DIR / f"{token_id}.gif"
    meta = token_meta(token_id, selection)
    if _FORCE or traits_newer_than(gif_dest):
        frames = compose_cached(selection)
        save_loop_gif(frames, gif_dest, DURATION_MS, colors=GIF_COLORS)
    (JSON_DIR / f"{token_id}.json").write_text(json.dumps(meta) + "\n", encoding="utf-8")
    return token_id, meta, gif_dest.stat().st_size


def write_sidecar(count: int, rows: list[dict], stats: Counter[str], total_bytes: int) -> None:
    for name in ("opensea-metadata.csv", "SHOOKUMS-opensea-drop.csv"):
        with (OUT / name).open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
            writer.writeheader()
            writer.writerows(rows)

    digest = hashlib.sha256()
    for i in range(1, count + 1):
        digest.update((GIF_DIR / f"{i}.gif").read_bytes())
    gif_bytes = sum((GIF_DIR / f"{i}.gif").stat().st_size for i in range(1, count + 1))
    (OUT / "provenance.json").write_text(
        json.dumps(
            {
                "hash": digest.hexdigest(),
                "count": count,
                "frames": FRAMES,
                "durationMs": DURATION_MS,
                "size": DROP_SIZE,
                "gifColors": GIF_COLORS,
                "bytes": gif_bytes,
                "openseaLimitBytes": OPENSEA_LIMIT_BYTES,
                "underOpenseaLimit": gif_bytes < OPENSEA_LIMIT_BYTES,
                "chain": "abstract",
                "chainId": 2741,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (OUT / "stats.json").write_text(json.dumps(dict(stats), indent=2) + "\n", encoding="utf-8")
    (OUT / "README.md").write_text(
        "# Halloween Shook'ums OpenSea pack\n\n"
        f"{count:,} flattened Halloween Shook'ums loops at {DROP_SIZE}×{DROP_SIZE}, {FRAMES} frames, {DURATION_MS}ms.\n\n"
        "Listing kit (OpenSea collection page):\n"
        "- Name: Halloween Shook'ums · Symbol: SHOOK · Category: PFPs · Chain: Abstract (2741)\n"
        "- Description: `public/metadata/shookums-description.txt`\n"
        "- Logo: `public/brand/logo-shookums.png` (512×512)\n"
        "- Featured: `public/brand/featured-shookums.jpg` (1200×800)\n"
        "- Banner: `public/brand/banner-shookums-opensea.jpg` (2800×700)\n"
        "- Collection GIF: `public/brand/collection-shookums.gif` (1000×1000)\n\n"
        f"Drop upload: every file in `gifs/` (1.gif–{count}.gif) plus `SHOOKUMS-opensea-drop.csv` "
        "or `opensea-metadata.csv`.\n"
        "OpenSea Drops play GIF, not APNG, and cap a Drop upload at 10 GB / 10,000 files.\n"
        "The CSV uses OpenSea Studio headers: tokenID, name, description, file_name, and attributes[Trait].\n"
        "Studio trait layers stay in `public/shookums-traits/` and are not the upload pack.\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help=f"Bake all {TOTAL} tokens")
    parser.add_argument("--count", type=int, default=16)
    parser.add_argument("--force", action="store_true", help="Rebuild GIFs even if they already exist")
    parser.add_argument("--workers", type=int, default=max(1, min(6, cpu_count() or 1)))
    args = parser.parse_args()
    global _FORCE
    _FORCE = args.force
    count = TOTAL if args.all else min(args.count, TOTAL)

    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    GIF_DIR.mkdir(parents=True, exist_ok=True)
    JSON_DIR.mkdir(parents=True, exist_ok=True)
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    roster = build_roster(count)
    jobs = list(enumerate(roster, start=1))

    rows_by_id: dict[int, dict] = {}
    stats: Counter[str] = Counter()
    total_bytes = 0
    done = 0

    print(f"Baking {count} Halloween Shook'ums tokens at {DROP_SIZE}px with {args.workers} workers…")
    with Pool(processes=args.workers, initializer=init_worker, initargs=(args.force,)) as pool:
        for token_id, meta, nbytes in pool.imap_unordered(bake_one, jobs, chunksize=4):
            done += 1
            total_bytes += nbytes
            rows_by_id[token_id] = drop_csv_row(token_id, meta)
            for attr in meta["attributes"]:
                stats[f"{attr['trait_type']}:{attr['value']}"] += 1
            if done % 100 == 0 or done == count:
                print(f"  {done}/{count}  {total_bytes / (1024 ** 3):.2f} GiB")

    rows = [rows_by_id[i] for i in range(1, count + 1)]
    for token_id in range(1, min(16, count) + 1):
        src_gif = GIF_DIR / f"{token_id}.gif"
        if src_gif.exists():
            try:
                (PREVIEW_DIR / f"{token_id}.gif").write_bytes(src_gif.read_bytes())
            except OSError:
                pass

    write_sidecar(count, rows, stats, total_bytes)
    gib = total_bytes / (1024 ** 3)
    print(f"Wrote {count} Halloween Shook'ums GIFs to generated/shookums/gifs ({gib:.2f} GiB)")
    if total_bytes >= OPENSEA_LIMIT_BYTES:
        print(f"WARNING: pack is {gib:.2f} GiB — over OpenSea's 10 GiB upload cap.")
        raise SystemExit(1)
    print(f"Under OpenSea's 10 GiB cap ({(OPENSEA_LIMIT_BYTES - total_bytes) / (1024 ** 3):.2f} GiB headroom).")


if __name__ == "__main__":
    main()
