#!/usr/bin/env python3
"""Compose Loopkins tokens from layered APNG traits.

Default: 16 signature samples.
Pass --all to shuffle the full 10,000 on the shared 12-frame clock.

Drop files are 384×384 APNGs so a 10,000 pack can fit OpenSea's 5GB media cap.
Studio traits stay 512×512 in public/traits/.
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

from build_loopkins import (  # noqa: E402
    DURATION_MS,
    FRAMES,
    PREVIEW_DIR,
    SIGNATURES,
    SIZE,
    STACK,
    TRAIT_SPEC,
    name_of,
    trait_path,
    write_opensea_kit_readme,
)
from gif_bake import load_apng_frames, save_loop_gif  # noqa: E402

OUT = ROOT / "generated"
IMAGE_DIR = OUT / "images"
GIF_DIR = OUT / "gifs"
JSON_DIR = OUT / "json"
TOTAL = 10_000
SEED = 4663_10000
DROP_SIZE = 256

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


def save_drop_apng(frames: list[Image.Image], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=[DURATION_MS] * len(frames),
        loop=0,
        format="PNG",
        disposal=1,
        blend=0,
        compress_level=9,
    )


TRAIT_LABELS = (
    ("sky", "Sky"),
    ("aura", "Aura"),
    ("body", "Body"),
    ("face", "Face"),
    ("wear", "Wear"),
    ("charm", "Charm"),
)

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
    description = "A looping PFP stacked from APNG trait layers."
    return {
        "name": f"Loopkin #{token_id}",
        "description": description,
        "image": f"{token_id}.gif",
        "attributes": attributes,
        "animation_loop": True,
        "compiler": "Loopkins APNG stack",
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


def bake_one(job: tuple[int, dict[str, str]]) -> tuple[int, dict, int]:
    token_id, selection = job
    dest = IMAGE_DIR / f"{token_id}.png"
    gif_dest = GIF_DIR / f"{token_id}.gif"
    meta = token_meta(token_id, selection)
    frames = None
    if not dest.exists() or dest.stat().st_size == 0:
        frames = compose_cached(selection)
        save_drop_apng(frames, dest)
    if not gif_dest.exists() or gif_dest.stat().st_size == 0:
        if frames is None:
            frames, _duration = load_apng_frames(dest)
        save_loop_gif(frames, gif_dest, DURATION_MS)
    (JSON_DIR / f"{token_id}.json").write_text(json.dumps(meta) + "\n", encoding="utf-8")
    return token_id, meta, dest.stat().st_size


def write_sidecar(count: int, rows: list[dict], stats: Counter[str], total_bytes: int) -> None:
    with (OUT / "opensea-metadata.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    digest = hashlib.sha256()
    for i in range(1, count + 1):
        digest.update((IMAGE_DIR / f"{i}.png").read_bytes())
    (OUT / "provenance.json").write_text(
        json.dumps(
            {
                "hash": digest.hexdigest(),
                "count": count,
                "frames": FRAMES,
                "durationMs": DURATION_MS,
                "size": DROP_SIZE,
                "bytes": total_bytes,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (OUT / "stats.json").write_text(json.dumps(dict(stats), indent=2) + "\n", encoding="utf-8")
    write_opensea_kit_readme(OUT / "README.md", count)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help=f"Bake all {TOTAL} tokens")
    parser.add_argument("--count", type=int, default=16)
    parser.add_argument("--workers", type=int, default=max(1, min(6, cpu_count() or 1)))
    args = parser.parse_args()
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

    print(f"Baking {count} Loopkins at {DROP_SIZE}px with {args.workers} workers…")
    with Pool(processes=args.workers, initializer=init_worker) as pool:
        for token_id, meta, nbytes in pool.imap_unordered(bake_one, jobs, chunksize=4):
            done += 1
            total_bytes += nbytes
            rows_by_id[token_id] = drop_csv_row(token_id, meta)
            for attr in meta["attributes"]:
                stats[f"{attr['trait_type']}:{attr['value']}"] += 1
            if done % 50 == 0 or done == count:
                print(f"  {done}/{count}  {total_bytes / 1_000_000:.1f} MB")

    rows = [rows_by_id[i] for i in range(1, count + 1)]
    for token_id in range(1, min(16, count) + 1):
        (PREVIEW_DIR / f"{token_id}.png").write_bytes((IMAGE_DIR / f"{token_id}.png").read_bytes())

    write_sidecar(count, rows, stats, total_bytes)
    print(f"Wrote {count} Loopkins to generated/images ({total_bytes / 1_000_000:.1f} MB)")


if __name__ == "__main__":
    main()
