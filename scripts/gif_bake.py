#!/usr/bin/env python3
"""Bake looping GIFs from Afterimages, Loopkins, Inklings, Wicklings, Purrkins, Hoodkins, Birbs, Shook'ums, Foxins, Santa Paws, Scribblins, Groovy Nation, and Opaline APNGs for OpenSea Drops.

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
WICKLINGS_APNG = ROOT / "generated" / "wicklings" / "images"
WICKLINGS_GIF = ROOT / "generated" / "wicklings" / "gifs"
PURRKINS_APNG = ROOT / "generated" / "purrkins" / "images"
PURRKINS_GIF = ROOT / "generated" / "purrkins" / "gifs"
HOODKINS_APNG = ROOT / "generated" / "hoodkins" / "images"
HOODKINS_GIF = ROOT / "generated" / "hoodkins" / "gifs"
BIRBS_APNG = ROOT / "generated" / "birbs" / "images"
BIRBS_GIF = ROOT / "generated" / "birbs" / "gifs"
SHOOKUMS_APNG = ROOT / "generated" / "shookums" / "images"
SHOOKUMS_GIF = ROOT / "generated" / "shookums" / "gifs"
FOXINS_APNG = ROOT / "generated" / "foxins" / "images"
FOXINS_GIF = ROOT / "generated" / "foxins" / "gifs"
SANTAPAWS_APNG = ROOT / "generated" / "santapaws" / "images"
SANTAPAWS_GIF = ROOT / "generated" / "santapaws" / "gifs"
SCRIBBLINS_APNG = ROOT / "generated" / "scribblins" / "images"
SCRIBBLINS_GIF = ROOT / "generated" / "scribblins" / "gifs"
GROOVY_APNG = ROOT / "generated" / "groovy" / "images"
GROOVY_GIF = ROOT / "generated" / "groovy" / "gifs"
OPALINE_APNG = ROOT / "generated" / "opaline" / "images"
OPALINE_GIF = ROOT / "generated" / "opaline" / "gifs"

LOOPKINS_DURATION_MS = 80
AFTER_DURATION_MS = 100
INKLINGS_DURATION_MS = 90
WICKLINGS_DURATION_MS = 80
PURRKINS_DURATION_MS = 80
HOODKINS_DURATION_MS = 80
BIRBS_DURATION_MS = 90
SHOOKUMS_DURATION_MS = 90
FOXINS_DURATION_MS = 90
SANTAPAWS_DURATION_MS = 90
SCRIBBLINS_DURATION_MS = 90
GROOVY_DURATION_MS = 90
OPALINE_DURATION_MS = 90
LOOPKINS_TOTAL = 10_000
AFTER_TOTAL = 3333
INKLINGS_TOTAL = 5555
WICKLINGS_TOTAL = 8888
PURRKINS_TOTAL = 10_000
HOODKINS_TOTAL = 10_000
BIRBS_TOTAL = 2_222
SHOOKUMS_TOTAL = 5_555
FOXINS_TOTAL = 5_555
SANTAPAWS_TOTAL = 7_777
SCRIBBLINS_TOTAL = 5_555
GROOVY_TOTAL = 8_888
OPALINE_TOTAL = 5_555


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


def palette_source(frames: list[Image.Image], picks: int = 4) -> Image.Image:
    if picks >= len(frames):
        chosen = frames
    else:
        step = max(1, len(frames) // picks)
        chosen = frames[::step][:picks]
    width, height = chosen[0].size
    mosaic = Image.new("RGB", (width * len(chosen), height))
    for index, frame in enumerate(chosen):
        mosaic.paste(frame, (index * width, 0))
    return mosaic


def save_loop_gif(
    frames: list[Image.Image],
    path: Path,
    duration_ms: int,
    colors: int = 240,
    dither: int = Image.Dither.FLOYDSTEINBERG,
    palette_picks: int = 4,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rgb_frames = [frame.convert("RGB") for frame in frames]
    palette = palette_source(rgb_frames, picks=palette_picks).quantize(
        colors=colors,
        method=Image.Quantize.MEDIANCUT,
        dither=Image.Dither.NONE,
    )
    quantized = [frame.quantize(palette=palette, dither=dither) for frame in rgb_frames]
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
    parser.add_argument("--wicklings", action="store_true", help="Bake Wicklings GIFs only")
    parser.add_argument("--purrkins", action="store_true", help="Bake Purrkins GIFs only")
    parser.add_argument("--hoodkins", action="store_true", help="Bake Hoodkins GIFs only")
    parser.add_argument("--birbs", action="store_true", help="Bake Birbs GIFs only")
    parser.add_argument("--shookums", action="store_true", help="Bake Halloween Shook'ums GIFs only")
    parser.add_argument("--foxins", action="store_true", help="Bake Foxins GIFs only")
    parser.add_argument("--santapaws", action="store_true", help="Bake Santa Paws GIFs only")
    parser.add_argument("--scribblins", action="store_true", help="Bake Scribblins GIFs only")
    parser.add_argument("--groovy", action="store_true", help="Bake Groovy Nation GIFs only")
    parser.add_argument("--opaline", action="store_true", help="Bake Opaline GIFs only")
    parser.add_argument("--all", action="store_true", help="Bake the full collection supply")
    parser.add_argument("--count", type=int, default=16, help="Count when not using --all")
    parser.add_argument("--workers", type=int, default=max(1, min(6, cpu_count() or 1)))
    args = parser.parse_args()
    selected = args.afterimages or args.loopkins or args.inklings or args.wicklings or args.purrkins or args.hoodkins or args.birbs or args.shookums or args.foxins or args.santapaws or args.scribblins or args.groovy or args.opaline
    do_after = args.afterimages or not selected
    do_loopkins = args.loopkins or not selected
    do_inklings = args.inklings or not selected
    do_wicklings = args.wicklings or not selected
    do_purrkins = args.purrkins or not selected
    do_hoodkins = args.hoodkins or not selected
    do_birbs = args.birbs or not selected
    do_shookums = args.shookums or not selected
    do_foxins = args.foxins or not selected
    do_santapaws = args.santapaws or not selected
    do_scribblins = args.scribblins or not selected
    do_groovy = args.groovy or not selected
    do_opaline = args.opaline or not selected

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
        from build_loopkins import write_opensea_kit_readme  # noqa: E402

        write_opensea_kit_readme(ROOT / "generated" / "README.md", count)

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

    if do_foxins:
        count = FOXINS_TOTAL if args.all else min(args.count, FOXINS_TOTAL)
        fox_jobs = jobs_for(FOXINS_APNG, FOXINS_GIF, count, FOXINS_DURATION_MS)
        bake("Foxins", fox_jobs, args.workers)
        rewrite_csv_filenames(ROOT / "generated" / "foxins" / "opensea-metadata.csv")
        rewrite_csv_filenames(ROOT / "generated" / "foxins" / "FOXINS-opensea-drop.csv")
        (ROOT / "generated" / "foxins" / "README.md").write_text(
            "# Foxins OpenSea pack\n\n"
            f"{count:,} flattened bold-graphic fox loops at 512×512, 12 frames, 90ms.\n\n"
            f"Upload every file in `gifs/` (1.gif–{count}.gif) plus `FOXINS-opensea-drop.csv` "
            "or `opensea-metadata.csv` to an OpenSea Drop on Base.\n"
            "OpenSea Drops play GIF, not APNG. APNGs stay in `images/` for the site and restacks.\n"
            "The CSV uses OpenSea Studio headers: tokenID, name, description, file_name, and attributes[Trait].\n",
            encoding="utf-8",
        )

    if do_santapaws:
        count = SANTAPAWS_TOTAL if args.all else min(args.count, SANTAPAWS_TOTAL)
        paw_jobs = jobs_for(SANTAPAWS_APNG, SANTAPAWS_GIF, count, SANTAPAWS_DURATION_MS)
        bake("Santa Paws", paw_jobs, args.workers)
        rewrite_csv_filenames(ROOT / "generated" / "santapaws" / "opensea-metadata.csv")
        rewrite_csv_filenames(ROOT / "generated" / "santapaws" / "SANTAPAWS-opensea-drop.csv")
        (ROOT / "generated" / "santapaws" / "README.md").write_text(
            "# Santa Paws OpenSea pack\n\n"
            f"{count:,} flattened chibi-cat loops at 512×512, 12 frames, 90ms.\n\n"
            f"Upload every file in `gifs/` (1.gif–{count}.gif) plus `SANTAPAWS-opensea-drop.csv` "
            "or `opensea-metadata.csv` to an OpenSea Drop on Base.\n"
            "OpenSea Drops play GIF, not APNG. APNGs stay in `images/` for the site and restacks.\n"
            "The CSV uses OpenSea Studio headers: tokenID, name, description, file_name, and attributes[Trait].\n"
            "Full metadata for all 7,777 lives in `json/` after `generate_santapaws.py`. "
            "Bake every GIF with `python3 scripts/generate_santapaws.py --all`.\n",
            encoding="utf-8",
        )

    if do_scribblins:
        count = SCRIBBLINS_TOTAL if args.all else min(args.count, SCRIBBLINS_TOTAL)
        scrib_jobs = jobs_for(SCRIBBLINS_APNG, SCRIBBLINS_GIF, count, SCRIBBLINS_DURATION_MS)
        bake("Scribblins", scrib_jobs, args.workers)
        rewrite_csv_filenames(ROOT / "generated" / "scribblins" / "opensea-metadata.csv")
        rewrite_csv_filenames(ROOT / "generated" / "scribblins" / "SCRIBBLINS-opensea-drop.csv")
        (ROOT / "generated" / "scribblins" / "README.md").write_text(
            "# Scribblins OpenSea pack\n\n"
            f"{count:,} flattened doodle-critter loops at 512×512, 12 frames, 90ms.\n\n"
            f"Upload every file in `gifs/` (1.gif–{count}.gif) plus `SCRIBBLINS-opensea-drop.csv` "
            "or `opensea-metadata.csv` to an OpenSea Drop on Base.\n"
            "OpenSea Drops play GIF, not APNG. APNGs stay in `images/` for the site and restacks.\n"
            "The CSV uses OpenSea Studio headers: tokenID, name, description, file_name, and attributes[Trait].\n",
            encoding="utf-8",
        )

    if do_groovy:
        count = GROOVY_TOTAL if args.all else min(args.count, GROOVY_TOTAL)
        groovy_jobs = jobs_for(GROOVY_APNG, GROOVY_GIF, count, GROOVY_DURATION_MS)
        bake("Groovy Nation", groovy_jobs, args.workers)
        rewrite_csv_filenames(ROOT / "generated" / "groovy" / "opensea-metadata.csv")
        rewrite_csv_filenames(ROOT / "generated" / "groovy" / "GROOVY-opensea-drop.csv")
        (ROOT / "generated" / "groovy" / "README.md").write_text(
            "# Groovy Nation OpenSea pack\n\n"
            f"{count:,} flattened musical-note loops at 512×512, 12 frames, 90ms.\n\n"
            f"Upload every file in `gifs/` (1.gif–{count}.gif) plus `GROOVY-opensea-drop.csv` "
            "or `opensea-metadata.csv` to an OpenSea Drop on Robinhood Chain.\n"
            "OpenSea Drops play GIF, not APNG. APNGs stay in `images/` for the site and restacks.\n"
            "The CSV uses OpenSea Studio headers: tokenID, name, description, file_name, and attributes[Trait].\n",
            encoding="utf-8",
        )

    if do_opaline:
        count = OPALINE_TOTAL if args.all else min(args.count, OPALINE_TOTAL)
        opaline_jobs = jobs_for(OPALINE_APNG, OPALINE_GIF, count, OPALINE_DURATION_MS)
        bake("Opaline", opaline_jobs, args.workers)
        rewrite_csv_filenames(ROOT / "generated" / "opaline" / "opensea-metadata.csv")
        rewrite_csv_filenames(ROOT / "generated" / "opaline" / "OPALINE-opensea-drop.csv")
        (ROOT / "generated" / "opaline" / "README.md").write_text(
            "# Opaline OpenSea pack\n\n"
            f"{count:,} flattened smoked-glass loops at 512×512, 12 frames, 90ms.\n\n"
            f"Upload every file in `gifs/` (1.gif–{count}.gif) plus `OPALINE-opensea-drop.csv` "
            "or `opensea-metadata.csv` to an OpenSea Drop on Base.\n"
            "OpenSea Drops play GIF, not APNG. APNGs stay in `images/` for the site and restacks.\n"
            "The CSV uses OpenSea Studio headers: tokenID, name, description, file_name, and attributes[Trait].\n",
            encoding="utf-8",
        )

    print("Done.")


if __name__ == "__main__":
    main()
