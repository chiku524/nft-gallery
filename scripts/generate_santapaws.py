#!/usr/bin/env python3
"""Compose Santa Paws tokens from layered APNG traits.

Always writes deterministic metadata for the full 7,777.
Default: bake 16 signature-preview GIFs.
Pass --all to flatten every token onto the shared 12-frame clock.

OpenSea gets GIFs only (max 10 GB). Studio traits stay 512×512 APNGs in public/santapaws-traits/.
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

from build_santapaws import (  # noqa: E402
    COLLECTION_STORY,
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

OUT = ROOT / "generated" / "santapaws"
IMAGE_DIR = OUT / "images"
GIF_DIR = OUT / "gifs"
JSON_DIR = OUT / "json"
TOTAL = 7_777
SEED = 8453_7777
DROP_SIZE = 512
GIF_COLORS = 160
OPENSEA_LIMIT_BYTES = 10 * 1024 * 1024 * 1024

_CACHE: dict[tuple[str, str], list[Image.Image]] | None = None


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


def init_worker() -> None:
    global _CACHE
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
        "name": f"Santa Paw #{token_id}",
        "description": "A looping chibi-cat PFP, always in the mood of giving. Minted on Base.",
        "image": f"{token_id}.gif",
        "attributes": attributes,
        "animation_loop": True,
        "compiler": "Santa Paws layer stack",
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


def bake_one(job: tuple[int, dict[str, str]]) -> tuple[int, int]:
    token_id, selection = job
    gif_dest = GIF_DIR / f"{token_id}.gif"
    if not gif_dest.exists() or gif_dest.stat().st_size == 0:
        frames = compose_cached(selection)
        save_loop_gif(frames, gif_dest, DURATION_MS, colors=GIF_COLORS)
    return token_id, gif_dest.stat().st_size


def write_sidecar(baked: int, rows: list[dict], stats: Counter[str], total_bytes: int) -> None:
    for name in ("opensea-metadata.csv", "SANTAPAWS-opensea-drop.csv"):
        with (OUT / name).open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
            writer.writeheader()
            writer.writerows(rows)

    digest = hashlib.sha256()
    gif_bytes = 0
    for i in range(1, baked + 1):
        path = GIF_DIR / f"{i}.gif"
        if path.exists():
            digest.update(path.read_bytes())
            gif_bytes += path.stat().st_size
    roster_digest = hashlib.sha256()
    for row in rows:
        roster_digest.update(json.dumps(row, sort_keys=True).encode("utf-8"))
    (OUT / "provenance.json").write_text(
        json.dumps(
            {
                "hash": digest.hexdigest() if baked else None,
                "rosterHash": roster_digest.hexdigest(),
                "count": TOTAL,
                "baked": baked,
                "frames": FRAMES,
                "durationMs": DURATION_MS,
                "size": DROP_SIZE,
                "gifColors": GIF_COLORS,
                "bytes": gif_bytes,
                "openseaLimitBytes": OPENSEA_LIMIT_BYTES,
                "underOpenseaLimit": gif_bytes < OPENSEA_LIMIT_BYTES,
                "seed": SEED,
                "chain": "base",
                "chainId": 8453,
                "note": (
                    None
                    if baked >= TOTAL
                    else f"Preview GIF bake of {baked}. Run `python3 scripts/generate_santapaws.py --all` for all {TOTAL:,} GIFs."
                ),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (OUT / "stats.json").write_text(json.dumps(dict(stats), indent=2) + "\n", encoding="utf-8")
    (OUT / "README.md").write_text(
        "# Santa Paws OpenSea kit\n\n"
        f"Deterministic metadata for all {TOTAL:,} tokens. "
        f"{baked:,} flattened chibi-cat loops baked at {DROP_SIZE}×{DROP_SIZE}, "
        f"{FRAMES} frames, {DURATION_MS}ms"
        + ("" if baked >= TOTAL else f" (preview subset — bake all {TOTAL:,} GIFs with `--all`)")
        + ".\n\n"
        "## Collection fields\n\n"
        "- Name: `Santa Paws`\n"
        "- Symbol: `PAWS`\n"
        "- Category: PFPs\n"
        "- Chain: Base (`8453`)\n"
        f"- Supply: `{TOTAL}`\n"
        "- Creator fee: `5%` (set your wallet — `public/metadata/santapaws.json` still has a zero address)\n\n"
        "## Paste this as the collection description\n\n"
        "Same file: `public/metadata/santapaws-description.txt`\n\n"
        "```\n"
        + COLLECTION_STORY
        + "\n```\n\n"
        "## Listing images\n\n"
        "No type on the marketplace images.\n\n"
        "| Use | File | Size |\n"
        "|---|---|---|\n"
        "| Logo | `public/brand/logo-santapaws.png` | 512×512, 1:1 |\n"
        "| Featured | `public/brand/featured-santapaws.jpg` | 1200×800, 3:2 |\n"
        "| OpenSea banner | `public/brand/banner-santapaws-opensea.jpg` | 2800×700, 4:1 |\n"
        "| Collection GIF | `public/brand/collection-santapaws.gif` | 1000×1000, 12-frame loop |\n"
        "| Site hero (not the OpenSea banner) | `public/brand/banner-santapaws.png` | 1500×560 |\n\n"
        "## Generate / bake\n\n"
        "```bash\n"
        "python3 scripts/build_santapaws.py\n"
        "python3 scripts/generate_santapaws.py        # full metadata + 16 preview GIFs\n"
        "python3 scripts/generate_santapaws.py --all  # full 7,777 GIFs\n"
        "python3 scripts/gif_bake.py --santapaws --all\n"
        "```\n\n"
        "## Drop upload\n\n"
        "1. In OpenSea Studio, create a Drop on Base (chain ID 8453).\n"
        f"2. Upload every file in `gifs/` (`1.gif`–`{baked}.gif`"
        + ("" if baked >= TOTAL else f"; bake the rest with `--all` before listing all {TOTAL:,}")
        + ").\n"
        "3. Upload `SANTAPAWS-opensea-drop.csv` (or `opensea-metadata.csv`). "
        "The CSV uses OpenSea Studio headers: `tokenID`, `name`, `description`, "
        "`file_name`, and `attributes[Trait]`.\n"
        "4. Preview the loops, then publish.\n\n"
        "OpenSea Drops play GIF, not APNG. Studio trait layers stay in "
        "`public/santapaws-traits/` and are not the upload pack.\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help=f"Bake all {TOTAL} token GIFs")
    parser.add_argument("--count", type=int, default=16, help="GIF preview count when not using --all")
    parser.add_argument("--workers", type=int, default=max(1, min(6, cpu_count() or 1)))
    args = parser.parse_args()
    bake_count = TOTAL if args.all else min(args.count, TOTAL)

    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    GIF_DIR.mkdir(parents=True, exist_ok=True)
    JSON_DIR.mkdir(parents=True, exist_ok=True)
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)

    roster = build_roster(TOTAL)
    rows: list[dict] = []
    stats: Counter[str] = Counter()
    print(f"Writing metadata for all {TOTAL} Santa Paws…")
    for token_id, selection in enumerate(roster, start=1):
        meta = token_meta(token_id, selection)
        (JSON_DIR / f"{token_id}.json").write_text(json.dumps(meta) + "\n", encoding="utf-8")
        rows.append(drop_csv_row(token_id, meta))
        for attr in meta["attributes"]:
            stats[f"{attr['trait_type']}:{attr['value']}"] += 1
        if token_id % 1000 == 0 or token_id == TOTAL:
            print(f"  metadata {token_id}/{TOTAL}")

    jobs = list(enumerate(roster[:bake_count], start=1))
    total_bytes = 0
    done = 0
    print(f"Baking {bake_count} Santa Paws GIFs at {DROP_SIZE}px with {args.workers} workers…")
    with Pool(processes=args.workers, initializer=init_worker) as pool:
        for _token_id, nbytes in pool.imap_unordered(bake_one, jobs, chunksize=4):
            done += 1
            total_bytes += nbytes
            if done % 100 == 0 or done == bake_count:
                print(f"  {done}/{bake_count}  {total_bytes / (1024 ** 3):.2f} GiB")

    for token_id in range(1, min(16, bake_count) + 1):
        src_gif = GIF_DIR / f"{token_id}.gif"
        if src_gif.exists():
            try:
                (PREVIEW_DIR / f"{token_id}.gif").write_bytes(src_gif.read_bytes())
            except OSError:
                pass

    write_sidecar(bake_count, rows, stats, total_bytes)
    gib = total_bytes / (1024 ** 3)
    print(f"Wrote {TOTAL} Santa Paws metadata files and {bake_count} GIFs to generated/santapaws/ ({gib:.2f} GiB baked)")
    if bake_count < TOTAL:
        print(f"Preview pack only. Bake the rest with: python3 scripts/generate_santapaws.py --all")
    if total_bytes >= OPENSEA_LIMIT_BYTES:
        print(f"WARNING: pack is {gib:.2f} GiB — over OpenSea's 10 GiB upload cap.")
        raise SystemExit(1)
    if bake_count >= TOTAL:
        print(f"Under OpenSea's 10 GiB cap ({(OPENSEA_LIMIT_BYTES - total_bytes) / (1024 ** 3):.2f} GiB headroom).")


if __name__ == "__main__":
    main()
