#!/usr/bin/env python3
"""Generate deterministic Street Heirs static tokens and marketplace sidecars."""

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

from build_street_heirs import (  # noqa: E402
    ART_VERSION,
    BACK_SIGNAL_TRAITS,
    CHAIN,
    CHAIN_ID,
    COLLECTION_STORY,
    INCOMPATIBLE,
    MINT,
    NAME,
    SIGNATURES,
    SIZE,
    SLUG,
    SUPPLY,
    SYMBOL,
    TOKEN,
    TRAIT_LABELS,
    TRAIT_ORDER,
    TRAIT_SPEC,
    combo_from_signature,
    compatible,
    compose,
    name_of,
    trait_path,
)
from paint_kit import save_image  # noqa: E402

OUT = ROOT / "generated" / SLUG
IMAGE_DIR = OUT / "images"
JSON_DIR = OUT / "json"
ROSTER_SEED = 4663_5555
DEFAULT_COUNT = 16

_CACHE: dict[tuple[str, str], Image.Image] | None = None


def load_cache() -> dict[tuple[str, str], Image.Image]:
    cache = {}
    for category, traits in TRAIT_SPEC.items():
        for trait_id, _name, _weight in traits:
            with Image.open(trait_path(category, trait_id)) as image:
                cache[(category, trait_id)] = image.convert("RGBA").copy()
    return cache


def init_worker() -> None:
    global _CACHE
    _CACHE = load_cache()


def weighted_pick(category: str, rng: random.Random) -> str:
    traits = TRAIT_SPEC[category]
    total = sum(weight for _trait_id, _name, weight in traits)
    roll = rng.uniform(0, total)
    for trait_id, _name, weight in traits:
        roll -= weight
        if roll <= 0:
            return trait_id
    return traits[-1][0]


def fingerprint(selection: dict[str, str]) -> str:
    return "|".join(f"{category}:{selection[category]}" for category in TRAIT_ORDER)


def pixel_hash(image: Image.Image) -> str:
    return hashlib.sha256(image.tobytes()).hexdigest()


def build_roster(
    count: int,
) -> tuple[list[dict[str, str]], list[str], dict[str, int]]:
    rng = random.Random(ROSTER_SEED)
    cache = load_cache()
    roster: list[dict[str, str]] = []
    hashes: list[str] = []
    fingerprints: set[str] = set()
    pixels: set[str] = set()
    rejected = {"compatibility": 0, "fingerprint": 0, "pixel": 0}

    def accept(selection: dict[str, str]) -> bool:
        if not compatible(selection):
            rejected["compatibility"] += 1
            return False
        combo = fingerprint(selection)
        if combo in fingerprints:
            rejected["fingerprint"] += 1
            return False
        digest = pixel_hash(compose(selection, cache))
        if digest in pixels:
            rejected["pixel"] += 1
            return False
        fingerprints.add(combo)
        pixels.add(digest)
        roster.append(dict(selection))
        hashes.append(digest)
        return True

    for signature in SIGNATURES[:count]:
        selection = combo_from_signature(signature)
        if not accept(selection):
            raise RuntimeError(f"Signature is invalid or duplicated: {fingerprint(selection)}")

    attempts = 0
    max_attempts = max(100_000, count * 500)
    while len(roster) < count and attempts < max_attempts:
        attempts += 1
        selection = {
            category: weighted_pick(category, rng)
            for category in TRAIT_ORDER
        }
        accept(selection)
    if len(roster) != count:
        raise RuntimeError(
            f"Could only create {len(roster):,} unique tokens after {attempts:,} attempts"
        )
    rejected["attempts"] = attempts
    return roster, hashes, rejected


def token_metadata(
    token_id: int,
    selection: dict[str, str],
    digest: str,
) -> dict:
    labels = dict(TRAIT_LABELS)
    return {
        "name": f"{TOKEN} #{token_id}",
        "description": COLLECTION_STORY,
        "image": f"{token_id}.png",
        "attributes": [
            {
                "trait_type": labels[category],
                "value": name_of(category, selection[category]),
            }
            for category in TRAIT_ORDER
        ],
        "compiler": f"{NAME} static portrait compositor",
        "art_version": ART_VERSION,
        "chain": CHAIN,
        "chain_id": CHAIN_ID,
        "signal_placement": (
            "behind-character"
            if selection["signal"] in BACK_SIGNAL_TRAITS
            else "foreground"
        ),
        "pixel_hash": digest,
    }


CSV_FIELDS = [
    "tokenID",
    "name",
    "description",
    "file_name",
    *(f"attributes[{label}]" for _category, label in TRAIT_LABELS),
]


def csv_row(token_id: int, metadata: dict) -> dict:
    row = {
        "tokenID": token_id,
        "name": metadata["name"],
        "description": metadata["description"],
        "file_name": f"{token_id}.png",
    }
    for attribute in metadata["attributes"]:
        row[f"attributes[{attribute['trait_type']}]"] = attribute["value"]
    return row


def render_one(job: tuple[int, dict[str, str], bool]) -> tuple[int, str, int]:
    token_id, selection, force = job
    assert _CACHE is not None
    destination = IMAGE_DIR / f"{token_id}.png"
    image = compose(selection, _CACHE)
    digest = pixel_hash(image)
    if force or not destination.exists() or destination.stat().st_size == 0:
        save_image(image, destination, compress_level=7)
    return token_id, digest, destination.stat().st_size


def write_csv(rows: list[dict]) -> None:
    for filename in ("opensea-metadata.csv", f"{SYMBOL}-opensea-drop.csv"):
        with (OUT / filename).open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
            writer.writeheader()
            writer.writerows(rows)


def write_contact_sheet() -> None:
    sheet = Image.new("RGB", (1024, 1024), "#f4efe5")
    for index in range(16):
        with Image.open(IMAGE_DIR / f"{index + 1}.png") as image:
            thumb = image.convert("RGB").resize((256, 256), Image.Resampling.LANCZOS)
            sheet.paste(thumb, ((index % 4) * 256, (index // 4) * 256))
    save_image(sheet, OUT / "contact-sheet.jpg", quality=92, optimize=True)


def write_sidecars(
    count: int,
    rows: list[dict],
    roster: list[dict[str, str]],
    hashes: list[str],
    rejected: dict[str, int],
    total_bytes: int,
) -> None:
    stat_counts: Counter[str] = Counter()
    for row in rows:
        for key, value in row.items():
            if key.startswith("attributes["):
                stat_counts[f"{key[11:-1]}:{value}"] += 1

    roster_hash = hashlib.sha256(
        json.dumps(roster, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    provenance_root = hashlib.sha256("".join(hashes).encode("ascii")).hexdigest()
    provenance = {
        "name": NAME,
        "symbol": SYMBOL,
        "seed": ROSTER_SEED,
        "requestedCount": count,
        "collectionSupply": SUPPLY,
        "fullSupply": count == SUPPLY,
        "size": SIZE,
        "format": "PNG",
        "static": True,
        "chain": CHAIN,
        "chainId": CHAIN_ID,
        "mint": MINT,
        "combinationFingerprintHash": roster_hash,
        "pixelHashRoot": provenance_root,
        "pixelHashes": {
            str(index): digest for index, digest in enumerate(hashes, 1)
        },
        "rejectedCandidates": rejected,
        "compatibilityRules": len(INCOMPATIBLE),
        "backSignalTraits": sorted(BACK_SIGNAL_TRAITS),
        "bytes": total_bytes,
        "artVersion": ART_VERSION,
    }
    (OUT / "provenance.json").write_text(
        json.dumps(provenance, indent=2) + "\n",
        encoding="utf-8",
    )
    stats = {
        "generated": count,
        "supply": SUPPLY,
        "uniqueCombinationFingerprints": len(
            {fingerprint(item) for item in roster}
        ),
        "uniqueRenderedPixelHashes": len(set(hashes)),
        "rejectedCandidates": rejected,
        "traitCounts": dict(sorted(stat_counts.items())),
    }
    (OUT / "stats.json").write_text(
        json.dumps(stats, indent=2) + "\n",
        encoding="utf-8",
    )
    layers = ", ".join(label for _category, label in TRAIT_LABELS)
    (OUT / "README.md").write_text(
        f"# {NAME} static generation pack\n\n"
        f"Deterministic {SIZE}×{SIZE} clean-cartoon portraits for {CHAIN} "
        f"(`{CHAIN_ID}`). This export contains {count:,} of the {SUPPLY:,} token supply.\n\n"
        "## Collection\n\n"
        f"- Symbol: `{SYMBOL}`\n"
        f"- Supply: `{SUPPLY:,}`\n"
        f"- Mint: `{MINT}`\n"
        f"- Roster seed: `{ROSTER_SEED}`\n"
        f"- Art version: `{ART_VERSION}`\n"
        f"- Layers: {layers}\n"
        f"- Compatibility exclusions: `{len(INCOMPATIBLE)}`\n\n"
        "## Contents\n\n"
        "- `images/`: flattened PNG art\n"
        "- `json/`: token metadata with exact rendered pixel hashes\n"
        f"- `{SYMBOL}-opensea-drop.csv`: OpenSea Studio import\n"
        "- `stats.json`: realized trait distribution and uniqueness totals\n"
        "- `provenance.json`: roster digest and per-token pixel hashes\n\n"
        "## Reproduce\n\n"
        "```bash\n"
        "python3 scripts/build_street_heirs.py\n"
        "python3 scripts/generate_street_heirs.py --count 16 --force\n"
        "python3 scripts/generate_street_heirs.py --all --workers 6\n"
        "```\n",
        encoding="utf-8",
    )
    write_contact_sheet()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--count",
        type=int,
        default=DEFAULT_COUNT,
        help="Number of tokens to export",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=max(1, min(6, cpu_count() or 1)),
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing rendered PNG files",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help=f"Export the full {SUPPLY:,} supply",
    )
    args = parser.parse_args()
    count = SUPPLY if args.all else args.count
    if not 1 <= count <= SUPPLY:
        parser.error(f"--count must be between 1 and {SUPPLY}")
    if args.workers < 1:
        parser.error("--workers must be at least 1")

    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    JSON_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Selecting {count:,} deterministic {NAME} portraits...")
    roster, expected_hashes, rejected = build_roster(count)

    jobs = [
        (token_id, selection, args.force)
        for token_id, selection in enumerate(roster, 1)
    ]
    rendered_hashes = [""] * count
    total_bytes = 0
    print(f"Rendering {count:,} PNGs with {args.workers} worker(s)...")
    with Pool(processes=args.workers, initializer=init_worker) as pool:
        for token_id, digest, byte_count in pool.imap_unordered(
            render_one,
            jobs,
            chunksize=8,
        ):
            rendered_hashes[token_id - 1] = digest
            total_bytes += byte_count
    if rendered_hashes != expected_hashes:
        raise RuntimeError("Rendered pixel hashes changed between selection and export")
    if len(set(rendered_hashes)) != count:
        raise RuntimeError("Rendered pixel-hash duplicate escaped roster filtering")

    rows = []
    for token_id, (selection, digest) in enumerate(
        zip(roster, rendered_hashes, strict=True),
        1,
    ):
        metadata = token_metadata(token_id, selection, digest)
        (JSON_DIR / f"{token_id}.json").write_text(
            json.dumps(metadata, indent=2) + "\n",
            encoding="utf-8",
        )
        rows.append(csv_row(token_id, metadata))

    write_csv(rows)
    write_sidecars(
        count,
        rows,
        roster,
        rendered_hashes,
        rejected,
        total_bytes,
    )
    print(
        f"Wrote {count:,} unique {NAME} PNGs, metadata, CSV, stats, and provenance "
        f"to generated/{SLUG}/ ({total_bytes / 1024**2:.1f} MiB)."
    )


if __name__ == "__main__":
    main()
