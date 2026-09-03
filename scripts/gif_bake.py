#!/usr/bin/env python3
"""Bake looping GIFs from Afterimages, Loopkins, Inklings, Party Pandas, Wicklings, Purrkins, Hoodkins, Mochins, Birbs, and Shook'ums APNGs for OpenSea Drops.

OpenSea Drops play GIF, not APNG. The site keeps the APNGs. This writes
quantized looping GIFs and points the Studio CSVs at those files.
"""

from __future__ import annotations

import argparse
import csv
import sys
from io import BytesIO
from multiprocessing import Pool, cpu_count
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

LOOPKINS_APNG = ROOT / "generated" / "images"
LOOPKINS_GIF = ROOT / "generated" / "gifs"
AFTER_APNG = ROOT / "generated" / "afterimages" / "images"
AFTER_GIF = ROOT / "generated" / "afterimages" / "gifs"
AFTER_PUBLIC = ROOT / "public" / "afterimages"
INKLINGS_APNG = ROOT / "generated" / "inklings" / "images"
INKLINGS_GIF = ROOT / "generated" / "inklings" / "gifs"
PANDAS_APNG = ROOT / "generated" / "party-pandas" / "images"
PANDAS_GIF = ROOT / "generated" / "party-pandas" / "gifs"
WICKLINGS_APNG = ROOT / "generated" / "wicklings" / "images"
WICKLINGS_GIF = ROOT / "generated" / "wicklings" / "gifs"
PURRKINS_APNG = ROOT / "generated" / "purrkins" / "images"
PURRKINS_GIF = ROOT / "generated" / "purrkins" / "gifs"
HOODKINS_APNG = ROOT / "generated" / "hoodkins" / "images"
HOODKINS_GIF = ROOT / "generated" / "hoodkins" / "gifs"
MOCHINS_APNG = ROOT / "generated" / "mochins" / "images"
MOCHINS_GIF = ROOT / "generated" / "mochins" / "gifs"
BIRBS_APNG = ROOT / "generated" / "birbs" / "images"
BIRBS_GIF = ROOT / "generated" / "birbs" / "gifs"
SHOOKUMS_APNG = ROOT / "generated" / "shookums" / "images"
SHOOKUMS_GIF = ROOT / "generated" / "shookums" / "gifs"

LOOPKINS_DURATION_MS = 80
AFTER_DURATION_MS = 100
INKLINGS_DURATION_MS = 90
PANDAS_DURATION_MS = 80
WICKLINGS_DURATION_MS = 80
PURRKINS_DURATION_MS = 80
HOODKINS_DURATION_MS = 80
MOCHINS_DURATION_MS = 100
BIRBS_DURATION_MS = 90
SHOOKUMS_DURATION_MS = 90
LOOPKINS_TOTAL = 10_000
AFTER_TOTAL = 3333
INKLINGS_TOTAL = 5555
PANDAS_TOTAL = 4444
WICKLINGS_TOTAL = 8888
PURRKINS_TOTAL = 10_000
HOODKINS_TOTAL = 10_000
MOCHINS_TOTAL = 4_000
BIRBS_TOTAL = 2_222
SHOOKUMS_TOTAL = 5_555


def load_apng_frames(path: Path) -> tuple[list[Image.Image], int]:
    with Image.open(path) as im:
        duration = im.info.get("duration", LOOPKINS_DURATION_MS)
        if isinstance(duration, (list, tuple)):
            duration = duration[0] if duration else LOOPKINS_DURATION_MS
        frames = []
        for index in range(getattr(im, "n_frames", 1)):
            im.seek(index)
            frames.append(im.convert("RGBA").copy())
        return frames, int(duration)


def palette_source(frames: list[Image.Image]) -> Image.Image:
    step = max(1, len(frames) // 4)
    picks = frames[::step][:4]
    width, height = picks[0].size
    mosaic = Image.new("RGB", (width * len(picks), height))
    for index, frame in enumerate(picks):
        mosaic.paste(frame, (index * width, 0))
    return mosaic


def save_loop_gif(
    frames: list[Image.Image],
    path: Path,
    duration_ms: int,
    colors: int = 240,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rgb_frames = [frame.convert("RGB") for frame in frames]
    palette = palette_source(rgb_frames).quantize(
        colors=colors,
        method=Image.Quantize.MEDIANCUT,
        dither=Image.Dither.NONE,
    )
    quantized = [frame.quantize(palette=palette, dither=Image.Dither.FLOYDSTEINBERG) for frame in rgb_frames]
    buffer = BytesIO()
    quantized[0].save(
        buffer,
        save_all=True,
        append_images=quantized[1:],
        duration=duration_ms,
        loop=0,
        optimize=True,
        disposal=2,
        format="GIF",
    )
    data = buffer.getvalue()
    last_error: OSError | None = None
    for attempt in range(8):
        try:
            path.write_bytes(data)
            last_error = None
            break
        except OSError as error:
            last_error = error
            import time

            time.sleep(0.15 * (attempt + 1))
    if last_error is not None:
        raise last_error


def rewrite_csv_filenames(csv_path: Path, extension: str = ".gif") -> None:
    if not csv_path.exists():
        return
    with csv_path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    if "file_name" not in fieldnames:
        return
    for row in rows:
        name = row.get("file_name") or ""
        stem = Path(name).stem or name
        row["file_name"] = f"{stem}{extension}"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def convert_one(job: tuple[str, str, int]) -> tuple[int, int]:
    src_text, dest_text, duration_ms = job
    src = Path(src_text)
    dest = Path(dest_text)
    token_id = int(src.stem)
    if dest.exists() and dest.stat().st_size > 0:
        return token_id, dest.stat().st_size
    frames, detected = load_apng_frames(src)
    save_loop_gif(frames, dest, duration_ms or detected)
    return token_id, dest.stat().st_size


def jobs_for(src_dir: Path, dest_dir: Path, count: int, duration_ms: int) -> list[tuple[str, str, int]]:
    dest_dir.mkdir(parents=True, exist_ok=True)
    jobs: list[tuple[str, str, int]] = []
    for token_id in range(1, count + 1):
        src = src_dir / f"{token_id}.png"
        if not src.exists() and src_dir == AFTER_APNG:
            src = AFTER_PUBLIC / f"{token_id}.png"
        if not src.exists():
            continue
        jobs.append((str(src), str(dest_dir / f"{token_id}.gif"), duration_ms))
    return jobs


def bake(label: str, jobs: list[tuple[str, str, int]], workers: int) -> int:
    if not jobs:
        print(f"No {label} APNGs found to convert.")
        return 0
    dest_dir = Path(jobs[0][1]).parent
    print(f"Baking {len(jobs)} {label} GIFs into {dest_dir.relative_to(ROOT)} with {workers} workers…")
    done = 0
    total_bytes = 0
    with Pool(processes=workers) as pool:
        for _token_id, nbytes in pool.imap_unordered(convert_one, jobs, chunksize=8):
            done += 1
            total_bytes += nbytes
            if done % 50 == 0 or done == len(jobs):
                print(f"  {done}/{len(jobs)}  {total_bytes / 1_000_000:.1f} MB")
    return total_bytes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--afterimages", action="store_true", help="Bake Afterimages GIFs only")
    parser.add_argument("--loopkins", action="store_true", help="Bake Loopkins GIFs only")
    parser.add_argument("--inklings", action="store_true", help="Bake Inklings GIFs only")
    parser.add_argument("--party-pandas", action="store_true", help="Bake Party Pandas GIFs only")
    parser.add_argument("--wicklings", action="store_true", help="Bake Wicklings GIFs only")
    parser.add_argument("--purrkins", action="store_true", help="Bake Purrkins GIFs only")
    parser.add_argument("--hoodkins", action="store_true", help="Bake Hoodkins GIFs only")
    parser.add_argument("--mochins", action="store_true", help="Bake Mochins GIFs only")
    parser.add_argument("--birbs", action="store_true", help="Bake Birbs GIFs only")
    parser.add_argument("--shookums", action="store_true", help="Bake Halloween Shook'ums GIFs only")
    parser.add_argument("--all", action="store_true", help="Bake the full collection supply")
    parser.add_argument("--count", type=int, default=16, help="Count when not using --all")
    parser.add_argument("--workers", type=int, default=max(1, min(6, cpu_count() or 1)))
    args = parser.parse_args()
    selected = args.afterimages or args.loopkins or args.inklings or args.party_pandas or args.wicklings or args.purrkins or args.hoodkins or args.mochins or args.birbs or args.shookums
    do_after = args.afterimages or not selected
    do_loopkins = args.loopkins or not selected
    do_inklings = args.inklings or not selected
    do_pandas = args.party_pandas or not selected
    do_wicklings = args.wicklings or not selected
    do_purrkins = args.purrkins or not selected
    do_hoodkins = args.hoodkins or not selected
    do_mochins = args.mochins or not selected
    do_birbs = args.birbs or not selected
    do_shookums = args.shookums or not selected

    if do_after:
        after_jobs = jobs_for(AFTER_APNG, AFTER_GIF, AFTER_TOTAL, AFTER_DURATION_MS)
        bake("Afterimages", after_jobs, args.workers)
        rewrite_csv_filenames(ROOT / "generated" / "afterimages" / "opensea-metadata.csv")
        (ROOT / "generated" / "afterimages" / "README.md").write_text(
            "# Afterimages OpenSea pack\n\n"
            f"{AFTER_TOTAL} unique 1:1 loops. Site files stay APNG. OpenSea Drop files are GIFs.\n\n"
            f"Upload every file in `gifs/` (1.gif–{AFTER_TOTAL}.gif) plus `opensea-metadata.csv`.\n"
            "OpenSea Drops play GIF, PNG, JPG, and SVG — not APNG.\n"
            "The CSV uses OpenSea Studio headers: `tokenID`, `name`, `description`, `file_name`, and `attributes[Trait]`.\n",
            encoding="utf-8",
        )

    if do_loopkins:
        count = LOOPKINS_TOTAL if args.all else min(args.count, LOOPKINS_TOTAL)
        loop_jobs = jobs_for(LOOPKINS_APNG, LOOPKINS_GIF, count, LOOPKINS_DURATION_MS)
        bake("Loopkins", loop_jobs, args.workers)
        rewrite_csv_filenames(ROOT / "generated" / "opensea-metadata.csv")
        rewrite_csv_filenames(ROOT / "generated" / "LOOPKINS-opensea-drop.csv")
        (ROOT / "generated" / "README.md").write_text(
            "# Loopkins OpenSea pack\n\n"
            f"{count:,} flattened loops at 256×256, 12 frames, 80ms.\n\n"
            "Upload every file in `gifs/` (1.gif–10000.gif) plus `LOOPKINS-opensea-drop.csv` "
            "or `opensea-metadata.csv` to an OpenSea Drop.\n"
            "OpenSea Drops play GIF, not APNG. APNGs stay in `images/` for the site and restacks.\n"
            "The CSV uses OpenSea Studio headers: tokenID, name, description, file_name, and attributes[Trait].\n",
            encoding="utf-8",
        )

    if do_inklings:
        count = INKLINGS_TOTAL if args.all else min(args.count, INKLINGS_TOTAL)
        ink_jobs = jobs_for(INKLINGS_APNG, INKLINGS_GIF, count, INKLINGS_DURATION_MS)
        bake("Inklings", ink_jobs, args.workers)
        rewrite_csv_filenames(ROOT / "generated" / "inklings" / "opensea-metadata.csv")
        rewrite_csv_filenames(ROOT / "generated" / "inklings" / "INKLINGS-opensea-drop.csv")
        (ROOT / "generated" / "inklings" / "README.md").write_text(
            "# Inklings OpenSea pack\n\n"
            f"{count:,} flattened cartoon-squid loops at 512×512, 16 frames, 90ms.\n\n"
            "Upload every file in `gifs/` (1.gif–5555.gif) plus `INKLINGS-opensea-drop.csv` "
            "or `opensea-metadata.csv` to an OpenSea Drop on Ink.\n"
            "OpenSea Drops play GIF, not APNG. APNGs stay in `images/` for the site and restacks.\n"
            "The CSV uses OpenSea Studio headers: tokenID, name, description, file_name, and attributes[Trait].\n",
            encoding="utf-8",
        )

    if do_pandas:
        count = PANDAS_TOTAL if args.all else min(args.count, PANDAS_TOTAL)
        panda_jobs = jobs_for(PANDAS_APNG, PANDAS_GIF, count, PANDAS_DURATION_MS)
        bake("Party Pandas", panda_jobs, args.workers)
        rewrite_csv_filenames(ROOT / "generated" / "party-pandas" / "opensea-metadata.csv")
        rewrite_csv_filenames(ROOT / "generated" / "party-pandas" / "PARTY-PANDAS-opensea-drop.csv")
        (ROOT / "generated" / "party-pandas" / "README.md").write_text(
            "# Party Pandas OpenSea pack\n\n"
            f"{count:,} flattened party-panda loops at 512×512, 12 frames, 80ms.\n\n"
            "Upload every file in `gifs/` (1.gif–4444.gif) plus `PARTY-PANDAS-opensea-drop.csv` "
            "or `opensea-metadata.csv` to an OpenSea Drop on Base.\n"
            "OpenSea Drops play GIF, not APNG. APNGs stay in `images/` for the site and restacks.\n"
            "The CSV uses OpenSea Studio headers: tokenID, name, description, file_name, and attributes[Trait].\n",
            encoding="utf-8",
        )

    if do_wicklings:
        count = WICKLINGS_TOTAL if args.all else min(args.count, WICKLINGS_TOTAL)
        wick_jobs = jobs_for(WICKLINGS_APNG, WICKLINGS_GIF, count, WICKLINGS_DURATION_MS)
        bake("Wicklings", wick_jobs, args.workers)
        rewrite_csv_filenames(ROOT / "generated" / "wicklings" / "opensea-metadata.csv")
        rewrite_csv_filenames(ROOT / "generated" / "wicklings" / "WICKLINGS-opensea-drop.csv")
        (ROOT / "generated" / "wicklings" / "README.md").write_text(
            "# Wicklings OpenSea pack\n\n"
            f"{count:,} flattened lantern loops at 512×512, 12 frames, 80ms.\n\n"
            f"Upload every file in `gifs/` (1.gif–{count}.gif) plus `WICKLINGS-opensea-drop.csv` "
            "or `opensea-metadata.csv` to an OpenSea Drop on Arbitrum.\n"
            "OpenSea Drops play GIF, not APNG. APNGs stay in `images/` for the site and restacks.\n"
            "The CSV uses OpenSea Studio headers: tokenID, name, description, file_name, and attributes[Trait].\n",
            encoding="utf-8",
        )

    if do_purrkins:
        count = PURRKINS_TOTAL if args.all else min(args.count, PURRKINS_TOTAL)
        purr_jobs = jobs_for(PURRKINS_APNG, PURRKINS_GIF, count, PURRKINS_DURATION_MS)
        bake("Purrkins", purr_jobs, args.workers)
        rewrite_csv_filenames(ROOT / "generated" / "purrkins" / "opensea-metadata.csv")
        rewrite_csv_filenames(ROOT / "generated" / "purrkins" / "PURRKINS-opensea-drop.csv")
        (ROOT / "generated" / "purrkins" / "README.md").write_text(
            "# Purrkins OpenSea pack\n\n"
            f"{count:,} flattened chibi-cat loops at 512×512, 12 frames, 80ms.\n\n"
            f"Upload every file in `gifs/` (1.gif–{count}.gif) plus `PURRKINS-opensea-drop.csv` "
            "or `opensea-metadata.csv` to an OpenSea Drop on HyperEVM.\n"
            "OpenSea Drops play GIF, not APNG. APNGs stay in `images/` for the site and restacks.\n"
            "The CSV uses OpenSea Studio headers: tokenID, name, description, file_name, and attributes[Trait].\n",
            encoding="utf-8",
        )

    if do_hoodkins:
        count = HOODKINS_TOTAL if args.all else min(args.count, HOODKINS_TOTAL)
        hood_jobs = jobs_for(HOODKINS_APNG, HOODKINS_GIF, count, HOODKINS_DURATION_MS)
        bake("Hoodkins", hood_jobs, args.workers)
        rewrite_csv_filenames(ROOT / "generated" / "hoodkins" / "opensea-metadata.csv")
        rewrite_csv_filenames(ROOT / "generated" / "hoodkins" / "HOODKINS-opensea-drop.csv")
        (ROOT / "generated" / "hoodkins" / "README.md").write_text(
            "# Hoodkins OpenSea pack\n\n"
            f"{count:,} flattened chibi-raccoon loops at 512×512, 12 frames, 80ms.\n\n"
            f"Upload every file in `gifs/` (1.gif–{count}.gif) plus `HOODKINS-opensea-drop.csv` "
            "or `opensea-metadata.csv` to an OpenSea Drop on Robinhood Chain.\n"
            "OpenSea Drops play GIF, not APNG. APNGs stay in `images/` for the site and restacks.\n"
            "The CSV uses OpenSea Studio headers: tokenID, name, description, file_name, and attributes[Trait].\n",
            encoding="utf-8",
        )

    if do_mochins:
        count = MOCHINS_TOTAL if args.all else min(args.count, MOCHINS_TOTAL)
        mochi_jobs = jobs_for(MOCHINS_APNG, MOCHINS_GIF, count, MOCHINS_DURATION_MS)
        bake("Mochins", mochi_jobs, args.workers)
        rewrite_csv_filenames(ROOT / "generated" / "mochins" / "opensea-metadata.csv")
        rewrite_csv_filenames(ROOT / "generated" / "mochins" / "MOCHINS-opensea-drop.csv")
        (ROOT / "generated" / "mochins" / "README.md").write_text(
            "# Mochins OpenSea pack\n\n"
            f"{count:,} flattened cartoon vinyl-toy mochi loops at 512×512, 16 frames, 100ms.\n\n"
            f"Upload every file in `gifs/` (1.gif–{count}.gif) plus `MOCHINS-opensea-drop.csv` "
            "or `opensea-metadata.csv` to an OpenSea Drop on Shape.\n"
            "OpenSea Drops play GIF, not APNG. APNGs stay in `images/` for the site and restacks.\n"
            "The CSV uses OpenSea Studio headers: tokenID, name, description, file_name, and attributes[Trait].\n",
            encoding="utf-8",
        )

    if do_birbs:
        count = BIRBS_TOTAL if args.all else min(args.count, BIRBS_TOTAL)
        birb_jobs = jobs_for(BIRBS_APNG, BIRBS_GIF, count, BIRBS_DURATION_MS)
        bake("BirbNation", birb_jobs, args.workers)
        rewrite_csv_filenames(ROOT / "generated" / "birbs" / "opensea-metadata.csv")
        rewrite_csv_filenames(ROOT / "generated" / "birbs" / "BIRBS-opensea-drop.csv")
        (ROOT / "generated" / "birbs" / "README.md").write_text(
            "# BirbNation OpenSea pack\n\n"
            f"{count:,} flattened round-borb robin loops at 512×512, 12 frames, 90ms.\n\n"
            f"Upload every file in `gifs/` (1.gif–{count}.gif) plus `BIRBS-opensea-drop.csv` "
            "or `opensea-metadata.csv` to an OpenSea Drop on Robinhood Chain.\n"
            "OpenSea Drops play GIF, not APNG. APNGs stay in `images/` for the site and restacks.\n"
            "The CSV uses OpenSea Studio headers: tokenID, name, description, file_name, and attributes[Trait].\n",
            encoding="utf-8",
        )

    if do_shookums:
        count = SHOOKUMS_TOTAL if args.all else min(args.count, SHOOKUMS_TOTAL)
        shook_jobs = jobs_for(SHOOKUMS_APNG, SHOOKUMS_GIF, count, SHOOKUMS_DURATION_MS)
        bake("Halloween Shook'ums", shook_jobs, args.workers)
        rewrite_csv_filenames(ROOT / "generated" / "shookums" / "opensea-metadata.csv")
        rewrite_csv_filenames(ROOT / "generated" / "shookums" / "SHOOKUMS-opensea-drop.csv")
        (ROOT / "generated" / "shookums" / "README.md").write_text(
            "# Halloween Shook'ums OpenSea pack\n\n"
            f"{count:,} flattened sheet-ghost loops at 512×512, 12 frames, 90ms.\n\n"
            f"Upload every file in `gifs/` (1.gif–{count}.gif) plus `SHOOKUMS-opensea-drop.csv` "
            "or `opensea-metadata.csv` to an OpenSea Drop on Abstract.\n"
            "OpenSea Drops play GIF, not APNG. APNGs stay in `images/` for the site and restacks.\n"
            "The CSV uses OpenSea Studio headers: tokenID, name, description, file_name, and attributes[Trait].\n",
            encoding="utf-8",
        )

    print("Done.")


if __name__ == "__main__":
    main()
