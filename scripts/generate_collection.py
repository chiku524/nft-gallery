#!/usr/bin/env python3
"""Generate 10,000 unique Pugs On The Block PFPs + OpenSea Drop metadata.

OpenSea does not build generative collections from trait layers. A Drop accepts
up to 10,000 finished JPG/PNG files and a CSV of names, descriptions, and string
traits. This script composites those files from the layered trait sheets.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import random
import sys
from collections import Counter
from multiprocessing import Pool, cpu_count
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
TRAITS = ROOT / "public" / "traits"
OUT = ROOT / "generated"
IMAGE_DIR = OUT / "images"
JSON_DIR = OUT / "json"
PREVIEW_DIR = ROOT / "public" / "generated-preview"

SIZE = 1024
TOTAL = 10_000
SEED = 4663_10000  # Robinhood chain ID + supply
JPEG_QUALITY = 92

NONE = {"id": "none", "name": None, "file": None, "rarity": 28}

# Tokens 1–8 are the eight gallery paintings, copied exactly so the drop
# opens with the same images as /pugs-on-the-block/gallery.
GALLERY_SEEDS = [
    {
        "file": ROOT / "public" / "gallery" / "mint-01-stoop-beanie.png",
        "combo": {
            "background": "brownstone",
            "base": "fawn",
            "block": "none",
            "hat": "beanie",
            "body": "bandana",
            "accessory": "none",
        },
    },
    {
        "file": ROOT / "public" / "gallery" / "mint-02-neon-crown.png",
        "combo": {
            "background": "neon",
            "base": "black",
            "block": "none",
            "hat": "crown",
            "body": "gold-chain",
            "accessory": "none",
        },
    },
    {
        "file": ROOT / "public" / "gallery" / "mint-03-rooftop-newsie.png",
        "combo": {
            "background": "rooftop",
            "base": "cream",
            "block": "none",
            "hat": "newsie",
            "body": "none",
            "accessory": "coffee",
        },
    },
    {
        "file": ROOT / "public" / "gallery" / "mint-04-day-hardhat.png",
        "combo": {
            "background": "stoop-day",
            "base": "fawn",
            "block": "none",
            "hat": "hardhat",
            "body": "none",
            "accessory": "blocks",
        },
    },
    {
        "file": ROOT / "public" / "gallery" / "mint-05-subway-snapback.png",
        "combo": {
            "background": "subway",
            "base": "black",
            "block": "none",
            "hat": "snapback",
            "body": "none",
            "accessory": "sunglasses",
        },
    },
    {
        "file": ROOT / "public" / "gallery" / "mint-06-green-monocle.png",
        "combo": {
            "background": "chain-green",
            "base": "cream",
            "block": "none",
            "hat": "none",
            "body": "collar",
            "accessory": "monocle",
        },
    },
    {
        "file": ROOT / "public" / "gallery" / "mint-07-cream-hoodie.png",
        "combo": {
            "background": "cream-brick",
            "base": "fawn",
            "block": "none",
            "hat": "none",
            "body": "hoodie",
            "accessory": "bone",
        },
    },
    {
        "file": ROOT / "public" / "gallery" / "mint-08-sunset-bandana.png",
        "combo": {
            "background": "rooftop",
            "base": "black",
            "block": "none",
            "hat": "none",
            "body": "bandana",
            "accessory": "sunglasses",
        },
    },
]

CATEGORIES = [
    {
        "id": "background",
        "label": "Background",
        "none_name": None,
        "traits": [
            {"id": "brownstone", "name": "Brownstone", "file": "background/bg-brownstone.png", "rarity": 22},
            {"id": "stoop-day", "name": "Sunny Stoop", "file": "background/bg-stoop-day.png", "rarity": 18},
            {"id": "cream-brick", "name": "Cream Paper", "file": "background/bg-cream-brick.png", "rarity": 16},
            {"id": "rooftop", "name": "Golden Rooftop", "file": "background/bg-rooftop-sunset.png", "rarity": 14},
            {"id": "subway", "name": "Subway Platform", "file": "background/bg-subway.png", "rarity": 10},
            {"id": "court", "name": "Dusk Court", "file": "background/bg-court-dusk.png", "rarity": 8},
            {"id": "neon", "name": "Neon Alley", "file": "background/bg-neon-night.png", "rarity": 7},
            {"id": "chain-green", "name": "Grid Green", "file": "background/bg-chain-green.png", "rarity": 5},
        ],
    },
    {
        "id": "base",
        "label": "Base",
        "none_name": None,
        "traits": [
            {"id": "fawn", "name": "Fawn Peek", "file": "base/base-fawn-peek.png", "rarity": 50},
            {"id": "cream", "name": "Apricot Peek", "file": "base/base-cream-peek.png", "rarity": 30},
            {"id": "black", "name": "Black Peek", "file": "base/base-black-peek.png", "rarity": 20},
        ],
    },
    {
        "id": "block",
        "label": "Block",
        "none_name": "Default concrete",
        "traits": [
            {"id": "concrete", "name": "Cinder Block", "file": "block/block-concrete.png", "rarity": 40},
            {"id": "brownstone-ledge", "name": "Brownstone Ledge", "file": "block/block-brownstone.png", "rarity": 28},
            {"id": "crate", "name": "Crate Stack", "file": "block/block-crate.png", "rarity": 20},
            {"id": "gold", "name": "Gold Bars", "file": "block/block-gold.png", "rarity": 12},
        ],
    },
    {
        "id": "hat",
        "label": "Hat",
        "none_name": "Bare head",
        "traits": [
            {"id": "beanie", "name": "Forest Beanie", "file": "hat/hat-beanie.png", "rarity": 18},
            {"id": "newsie", "name": "Newsie Cap", "file": "hat/hat-newsie.png", "rarity": 16},
            {"id": "snapback", "name": "Stoop Snapback", "file": "hat/hat-snapback.png", "rarity": 14},
            {"id": "hardhat", "name": "Block Hard Hat", "file": "hat/hat-hardhat.png", "rarity": 12},
            {"id": "crown", "name": "Stoop Crown", "file": "hat/hat-crown.png", "rarity": 12},
        ],
    },
    {
        "id": "body",
        "label": "Body",
        "none_name": "No clothes",
        "traits": [
            {"id": "bandana", "name": "Forest Bandana", "file": "body/body-bandana.png", "rarity": 22},
            {"id": "collar", "name": "Red Collar", "file": "body/body-collar.png", "rarity": 18},
            {"id": "hoodie", "name": "Cream Hoodie", "file": "body/body-hoodie.png", "rarity": 16},
            {"id": "gold-chain", "name": "Gold Chain", "file": "body/body-gold-chain.png", "rarity": 12},
        ],
    },
    {
        "id": "accessory",
        "label": "Accessory",
        "none_name": "Empty paws",
        "traits": [
            {"id": "bone", "name": "Chewed Bone", "file": "accessory/acc-bone.png", "rarity": 18},
            {"id": "coffee", "name": "Stoop Coffee", "file": "accessory/acc-coffee.png", "rarity": 16},
            {"id": "sunglasses", "name": "Round Shades", "file": "accessory/acc-sunglasses.png", "rarity": 14},
            {"id": "blocks", "name": "Toy Blocks", "file": "accessory/acc-blocks.png", "rarity": 12},
            {"id": "monocle", "name": "Gold Monocle", "file": "accessory/acc-monocle.png", "rarity": 10},
        ],
    },
]

DESCRIPTION = (
    "A neighborhood pug peeking over the block. Pugs On The Block is a 10,000-piece "
    "PFP collection on Robinhood Chain."
)

CACHE: dict[str, Image.Image] = {}


def pool_for(category: dict) -> list[dict]:
    traits = []
    if category["none_name"]:
        traits.append({**NONE, "name": category["none_name"]})
    for trait in category["traits"]:
        traits.append(
            {
                "id": trait["id"],
                "name": trait["name"],
                "file": trait["file"],
                "rarity": trait["rarity"],
            }
        )
    return traits


def pick(rng: random.Random, traits: list[dict]) -> dict:
    total = sum(max(t["rarity"], 1) for t in traits)
    roll = rng.random() * total
    for trait in traits:
        roll -= max(trait["rarity"], 1)
        if roll <= 0:
            return trait
    return traits[0]


def dna_key(combo: dict[str, dict]) -> str:
    return "|".join(f"{cat['id']}:{combo[cat['id']]['id']}" for cat in CATEGORIES)


def trait_by_id(category_id: str, trait_id: str) -> dict:
    category = next(cat for cat in CATEGORIES if cat["id"] == category_id)
    if trait_id == "none":
        return {**NONE, "name": category["none_name"]}
    trait = next(t for t in category["traits"] if t["id"] == trait_id)
    return {"id": trait["id"], "name": trait["name"], "file": trait["file"], "rarity": trait["rarity"]}


def gallery_combo(spec: dict) -> dict[str, dict]:
    return {cat_id: trait_by_id(cat_id, trait_id) for cat_id, trait_id in spec["combo"].items()}


def unique_combos(count: int) -> list[dict[str, dict]]:
    rng = random.Random(SEED)
    pools = {cat["id"]: pool_for(cat) for cat in CATEGORIES}
    seen: set[str] = set()
    combos: list[dict[str, dict]] = []

    for spec in GALLERY_SEEDS:
        if len(combos) >= count:
            break
        combo = gallery_combo(spec)
        seen.add(dna_key(combo))
        combos.append(combo)

    attempts = 0
    while len(combos) < count:
        attempts += 1
        if attempts > count * 50:
            raise RuntimeError(f"Could not find {count} unique combinations")
        combo = {cat["id"]: pick(rng, pools[cat["id"]]) for cat in CATEGORIES}
        key = dna_key(combo)
        if key in seen:
            continue
        seen.add(key)
        combos.append(combo)
    return combos


def load_trait(file_name: str) -> Image.Image:
    if file_name not in CACHE:
        path = TRAITS / file_name
        CACHE[file_name] = Image.open(path).convert("RGBA")
    return CACHE[file_name]


# Match the studio stack: wrap behind, pug, hat, neck front, wall, hanging, toys, paws.
FACE_ACCESSORIES = {"sunglasses", "monocle"}
LEDGE_ACCESSORIES = {"coffee", "bone", "blocks"}


def gallery_image_for(combo: dict[str, dict]) -> Image.Image | None:
    key = {cat_id: combo[cat_id]["id"] for cat_id in ("background", "base", "block", "hat", "body", "accessory")}
    for spec in GALLERY_SEEDS:
        if spec["combo"] == key:
            return Image.open(spec["file"]).convert("RGB")
    return None


def render(combo: dict[str, dict]) -> Image.Image:
    pinned = gallery_image_for(combo)
    if pinned is not None:
        if pinned.size != (SIZE, SIZE):
            pinned = pinned.resize((SIZE, SIZE), Image.Resampling.LANCZOS)
        return pinned
    canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))

    def comp(file_name: str | None) -> None:
        nonlocal canvas
        if not file_name:
            return
        overlay = load_trait(file_name)
        if overlay.size != (SIZE, SIZE):
            overlay = overlay.resize((SIZE, SIZE), Image.Resampling.LANCZOS)
        canvas = Image.alpha_composite(canvas, overlay)

    acc_id = combo["accessory"]["id"]
    body_file = combo["body"]["file"]
    comp(combo["background"]["file"])
    comp(body_file)
    comp(combo["base"]["file"])
    if acc_id in FACE_ACCESSORIES:
        comp(combo["accessory"]["file"])
    comp(combo["hat"]["file"])
    if body_file:
        comp(body_file.replace(".png", "-neck.png"))
    comp(combo["block"]["file"] or "base/wall-default.png")
    if body_file:
        comp(body_file.replace(".png", "-front.png"))
    if acc_id in LEDGE_ACCESSORIES:
        comp(combo["accessory"]["file"])
    comp(f"base/front-paws-{combo['base']['id']}.png")
    return canvas.convert("RGB")


def token_record(token_id: int, combo: dict[str, dict]) -> dict:
    attributes = [{"trait_type": cat["label"], "value": combo[cat["id"]]["name"]} for cat in CATEGORIES]
    filename = f"{token_id}.jpg"
    return {
        "tokenID": token_id,
        "name": f"Pugs On The Block #{token_id}",
        "description": DESCRIPTION,
        "image": filename,
        "attributes": attributes,
        "dna": dna_key(combo),
    }


def write_outputs(token_id: int, combo: dict[str, dict], image: Image.Image) -> str:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    JSON_DIR.mkdir(parents=True, exist_ok=True)
    image_path = IMAGE_DIR / f"{token_id}.jpg"
    image.save(image_path, "JPEG", quality=JPEG_QUALITY, optimize=False, subsampling=0)
    record = token_record(token_id, combo)
    json_path = JSON_DIR / f"{token_id}.json"
    json.dump(
        {
            "name": record["name"],
            "description": record["description"],
            "image": filename_for_json(token_id),
            "attributes": record["attributes"],
        },
        json_path.open("w"),
        indent=2,
    )
    return str(image_path)


def filename_for_json(token_id: int) -> str:
    return f"{token_id}.jpg"


def render_token(payload: tuple[int, dict[str, dict]]) -> tuple[int, str, str]:
    token_id, combo = payload
    image = render(combo)
    write_outputs(token_id, combo, image)
    return token_id, dna_key(combo), f"{token_id}.jpg"


def warmup() -> None:
    for cat in CATEGORIES:
        for trait in cat["traits"]:
            load_trait(trait["file"])
    extras = [
        "base/wall-default.png",
        "base/front-paws-fawn.png",
        "base/front-paws-cream.png",
        "base/front-paws-black.png",
        "body/body-bandana-neck.png",
        "body/body-collar-neck.png",
        "body/body-hoodie-neck.png",
        "body/body-gold-chain-neck.png",
        "body/body-bandana-front.png",
        "body/body-collar-front.png",
        "body/body-hoodie-front.png",
        "body/body-gold-chain-front.png",
    ]
    for rel in extras:
        load_trait(rel)


def write_csv(records: list[dict]) -> None:
    fieldnames = ["tokenID", "name", "description", "image"] + [cat["label"] for cat in CATEGORIES]
    path = OUT / "opensea-metadata.csv"
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            row = {
                "tokenID": record["tokenID"],
                "name": record["name"],
                "description": record["description"],
                "image": record["image"],
            }
            for attr in record["attributes"]:
                row[attr["trait_type"]] = attr["value"]
            writer.writerow(row)


def write_stats(records: list[dict]) -> None:
    counts = {cat["label"]: Counter() for cat in CATEGORIES}
    for record in records:
        for attr in record["attributes"]:
            counts[attr["trait_type"]][attr["value"]] += 1
    stats = {
        "supply": len(records),
        "seed": SEED,
        "unique": len({record["dna"] for record in records}),
        "traits": {
            label: {
                name: {"count": count, "percent": round(100 * count / len(records), 2)}
                for name, count in sorted(counter.items(), key=lambda item: (-item[1], item[0]))
            }
            for label, counter in counts.items()
        },
    }
    (OUT / "stats.json").write_text(json.dumps(stats, indent=2) + "\n")


def provenance(records: list[dict]) -> None:
    hashes = []
    for record in records:
        digest = hashlib.sha256((IMAGE_DIR / record["image"]).read_bytes()).hexdigest()
        hashes.append(f"{record['tokenID']}:{digest}")
        record["hash"] = digest
    concatenated = "".join(item.split(":", 1)[1] for item in hashes)
    final = hashlib.sha256(concatenated.encode("ascii")).hexdigest()
    (OUT / "provenance.json").write_text(
        json.dumps({"concatenatedHash": final, "hashFunction": "sha256", "tokens": hashes}, indent=2)
        + "\n"
    )


def copy_previews(records: list[dict]) -> None:
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    for path in PREVIEW_DIR.glob("*.jpg"):
        path.unlink()
    picks = records[:8] + records[111::1250][:8]
    seen = set()
    for record in picks:
        if record["tokenID"] in seen:
            continue
        seen.add(record["tokenID"])
        src = IMAGE_DIR / record["image"]
        dest = PREVIEW_DIR / record["image"]
        dest.write_bytes(src.read_bytes())


def main() -> int:
    count = TOTAL
    if len(sys.argv) > 1:
        count = int(sys.argv[1])

    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    JSON_DIR.mkdir(parents=True, exist_ok=True)
    warmup()
    combos = unique_combos(count)
    records = [token_record(i, combo) for i, combo in enumerate(combos, start=1)]

    workers = max(1, cpu_count())
    print(f"Rendering {count} unique pugs with {workers} workers…", flush=True)

    payloads = list(enumerate(combos, start=1))
    done = 0
    with Pool(processes=workers, initializer=warmup) as pool:
        for token_id, _dna, _name in pool.imap_unordered(render_token, payloads, chunksize=8):
            done += 1
            if done % 250 == 0 or done == count:
                print(f"  {done}/{count}  (last #{token_id})", flush=True)

    write_csv(records)
    write_stats(records)
    provenance(records)
    copy_previews(records)
    (OUT / "metadata.jsonl").write_text("".join(json.dumps(record) + "\n" for record in records))
    print(f"Wrote {count} images to {IMAGE_DIR}")
    print(f"OpenSea CSV: {OUT / 'opensea-metadata.csv'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
