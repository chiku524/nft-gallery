#!/usr/bin/env python3
"""Compose Feltro tokens from layered APNG traits.

Default: 16 signature samples.
Pass --all to shuffle the full 10,000 on the shared 12-frame clock.
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

from build_feltro import (  # noqa: E402
    COLLECTION_STORY,
    DURATION_MS,
    FRAMES,
    GIF_COLORS,
    GIF_DITHER,
    NAME,
    PREVIEW_DIR,
    SIGNATURES,
    SIZE,
    SLUG,
    STACK,
    SYMBOL,
    TOKEN,
    TRAIT_LABELS,
    TRAIT_SPEC,
    name_of,
    trait_path,
)
from gif_bake import save_loop_gif  # noqa: E402

OUT = ROOT / "generated" / SLUG
GIF_DIR = OUT / "gifs"
JSON_DIR = OUT / "json"
TOTAL = 10_000
SEED = 4663_10001
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
        out.append(canvas)
    return out


CSV_FIELDS = ["tokenID", "name", "description", "file_name", *(f"attributes[{label}]" for _key, label in TRAIT_LABELS)]


def token_meta(token_id: int, selection: dict[str, str]) -> dict:
    attributes = [{"trait_type": label, "value": name_of(key, selection[key])} for key, label in TRAIT_LABELS]
    return {
        "name": f"{TOKEN} #{token_id}",
        "description": f"A looping foam mascot from {NAME}. Mesh eyes. A seam down the cylinder. Free mint on Robinhood Chain.",
        "image": f"{token_id}.gif",
        "attributes": attributes,
        "animation_loop": True,
        "compiler": f"{NAME} layer stack",
    }


def drop_csv_row(token_id: int, meta: dict) -> dict:
    row = {"tokenID": token_id, "name": meta["name"], "description": meta["description"], "file_name": f"{token_id}.gif"}
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
    if _FORCE or traits_newer_than(gif_dest) or not gif_dest.exists() or gif_dest.stat().st_size == 0:
        save_loop_gif(compose_cached(selection), gif_dest, DURATION_MS, colors=GIF_COLORS, dither=GIF_DITHER, palette_picks=FRAMES)
    (JSON_DIR / f"{token_id}.json").write_text(json.dumps(meta) + "\n", encoding="utf-8")
    return token_id, meta, gif_dest.stat().st_size


def write_sidecar(count: int, rows: list[dict], stats: Counter[str]) -> None:
    for name in ("opensea-metadata.csv", f"{SYMBOL}-opensea-drop.csv"):
        with (OUT / name).open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
            writer.writeheader()
            writer.writerows(rows)
    digest = hashlib.sha256()
    gif_bytes = 0
    for i in range(1, count + 1):
        data = (GIF_DIR / f"{i}.gif").read_bytes()
        digest.update(data)
        gif_bytes += len(data)
    (OUT / "provenance.json").write_text(
        json.dumps(
            {
                "hash": digest.hexdigest(),
                "count": count,
                "frames": FRAMES,
                "durationMs": DURATION_MS,
                "size": SIZE,
                "gifColors": GIF_COLORS,
                "bytes": gif_bytes,
                "openseaLimitBytes": OPENSEA_LIMIT_BYTES,
                "underOpenseaLimit": gif_bytes < OPENSEA_LIMIT_BYTES,
                "chain": "robinhood",
                "chainId": 4663,
                "mintPriceEth": "0",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (OUT / "stats.json").write_text(json.dumps(dict(stats), indent=2) + "\n", encoding="utf-8")
    (OUT / "README.md").write_text(
        f"# {NAME} OpenSea kit\n\n"
        f"{count:,} flattened foam-mascot loops at {SIZE}×{SIZE}, {FRAMES} frames, {DURATION_MS}ms"
        + ("" if count >= TOTAL else f" (sample pack — bake all {TOTAL:,} with `--all`)")
        + ".\n\n"
        "## Collection fields\n\n"
        f"- Name: `{NAME}`\n"
        f"- Symbol: `{SYMBOL}`\n"
        f"- Token name: `{TOKEN} #{{id}}`\n"
        "- Category: PFPs\n"
        "- Chain: Robinhood Chain (`4663`)\n"
        f"- Supply: `{TOTAL}`\n"
        "- Mint: free (`0 ETH`)\n"
        f"- Creator fee: `5%` (set your wallet — `public/metadata/{SLUG}.json` still has a zero address)\n\n"
        "## Paste this as the collection description\n\n"
        f"Same file: `public/metadata/{SLUG}-description.txt`\n\n"
        "```\n" + COLLECTION_STORY + "\n```\n\n"
        "## Listing images\n\n"
        "No type on the marketplace images.\n\n"
        "| Use | File | Size |\n"
        "|---|---|---|\n"
        f"| Logo | `public/brand/logo-{SLUG}.png` | 512×512, 1:1 |\n"
        f"| Featured | `public/brand/featured-{SLUG}.jpg` | 1200×800, 3:2 |\n"
        f"| OpenSea banner | `public/brand/banner-{SLUG}-opensea.jpg` | 2800×700, 4:1 |\n"
        f"| Collection GIF | `public/brand/collection-{SLUG}.gif` | 1000×1000, 12-frame loop |\n"
        f"| Site hero (not the OpenSea banner) | `public/brand/banner-{SLUG}.png` | 1500×560 |\n\n"
        "## Drop upload\n\n"
        "1. In OpenSea Studio, create a Drop on Robinhood Chain (chain ID 4663).\n"
        f"2. Upload every file in `gifs/` (`1.gif`–`{count}.gif`).\n"
        f"3. Upload `{SYMBOL}-opensea-drop.csv` (or `opensea-metadata.csv`).\n"
        "4. Set mint price to free.\n"
        "5. Preview the loops, then publish.\n\n"
        f"OpenSea Drops play GIF, not APNG. Studio trait layers stay in `public/{SLUG}-traits/` and are not the upload pack.\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help=f"Bake all {TOTAL} tokens")
    parser.add_argument("--count", type=int, default=16)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--workers", type=int, default=max(1, min(6, cpu_count() or 1)))
    args = parser.parse_args()
    global _FORCE
    _FORCE = args.force
    count = TOTAL if args.all else min(args.count, TOTAL)
    GIF_DIR.mkdir(parents=True, exist_ok=True)
    JSON_DIR.mkdir(parents=True, exist_ok=True)
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    jobs = list(enumerate(build_roster(count), start=1))
    rows_by_id: dict[int, dict] = {}
    stats: Counter[str] = Counter()
    done = 0
    print(f"Baking {count} {NAME} tokens with {args.workers} workers…")
    with Pool(processes=args.workers, initializer=init_worker, initargs=(args.force,)) as pool:
        for token_id, meta, _nbytes in pool.imap_unordered(bake_one, jobs, chunksize=4):
            done += 1
            rows_by_id[token_id] = drop_csv_row(token_id, meta)
            for attr in meta["attributes"]:
                stats[f"{attr['trait_type']}:{attr['value']}"] += 1
            if done % 100 == 0 or done == count:
                print(f"  {done}/{count}")
    for token_id in range(1, min(16, count) + 1):
        src = GIF_DIR / f"{token_id}.gif"
        if src.exists():
            (PREVIEW_DIR / f"{token_id}.gif").write_bytes(src.read_bytes())
    write_sidecar(count, [rows_by_id[i] for i in range(1, count + 1)], stats)
    print(f"Wrote {count} {NAME} sample GIFs to generated/{SLUG}/gifs")


if __name__ == "__main__":
    main()
