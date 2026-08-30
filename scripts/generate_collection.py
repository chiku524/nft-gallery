#!/usr/bin/env python3
"""Compose Loopkins tokens from layered APNG traits.

Default: 16 signature samples already baked by build_loopkins.py.
Pass --all to shuffle the full 3,333 on the shared 12-frame clock.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import sys
from collections import Counter
from pathlib import Path

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
    compose_selection,
    name_of,
    save_apng,
)

OUT = ROOT / "generated"
IMAGE_DIR = OUT / "images"
JSON_DIR = OUT / "json"
TOTAL = 3333
SEED = 4663_3333


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


def write_token(token_id: int, selection: dict[str, str]) -> dict:
    frames = compose_selection(selection)
    save_apng(frames, IMAGE_DIR / f"{token_id}.png")
    attributes = [
        {"trait_type": label, "value": name_of(key, selection[key])}
        for key, label in (
            ("sky", "Sky"),
            ("aura", "Aura"),
            ("body", "Body"),
            ("face", "Face"),
            ("wear", "Wear"),
            ("charm", "Charm"),
        )
    ]
    meta = {
        "name": f"Loopkin #{token_id}",
        "description": "A looping PFP stacked from APNG trait layers.",
        "image": f"{token_id}.png",
        "attributes": attributes,
        "animation_loop": True,
        "compiler": "Loopkins APNG stack",
    }
    (JSON_DIR / f"{token_id}.json").write_text(json.dumps(meta) + "\n", encoding="utf-8")
    return meta


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help=f"Bake all {TOTAL} tokens")
    parser.add_argument("--count", type=int, default=16)
    args = parser.parse_args()
    count = TOTAL if args.all else min(args.count, TOTAL)

    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    JSON_DIR.mkdir(parents=True, exist_ok=True)
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    roster = build_roster(count)

    rows = []
    stats: Counter[str] = Counter()
    for token_id, selection in enumerate(roster, start=1):
        print(f"  token {token_id}/{count}")
        meta = write_token(token_id, selection)
        if token_id <= 16:
            (PREVIEW_DIR / f"{token_id}.png").write_bytes((IMAGE_DIR / f"{token_id}.png").read_bytes())
        rows.append({"tokenID": token_id, "name": meta["name"], "file": f"{token_id}.png", **{a["trait_type"]: a["value"] for a in meta["attributes"]}})
        for attr in meta["attributes"]:
            stats[f"{attr['trait_type']}:{attr['value']}"] += 1

    with (OUT / "opensea-metadata.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    blob = b"".join((IMAGE_DIR / f"{i}.png").read_bytes() for i in range(1, count + 1))
    (OUT / "provenance.json").write_text(
        json.dumps({"hash": hashlib.sha256(blob).hexdigest(), "count": count, "frames": FRAMES, "durationMs": DURATION_MS, "size": SIZE}, indent=2)
        + "\n",
        encoding="utf-8",
    )
    (OUT / "stats.json").write_text(json.dumps(dict(stats), indent=2) + "\n", encoding="utf-8")
    (OUT / "README.md").write_text(
        "# Loopkins drop files\n\n"
        "Each token is a flattened APNG. Traits themselves stay layered in `public/traits/`.\n"
        "Upload `images/*.png` plus `opensea-metadata.csv` to an OpenSea Drop.\n",
        encoding="utf-8",
    )
    print(f"Wrote {count} Loopkins to generated/")


if __name__ == "__main__":
    main()
