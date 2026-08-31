# Inklings

Looping **ink-wash PFP GIFs**. A **5,555-piece** illustrated portrait collection built to mint on **Ink** (chain ID `57073`) and list on **OpenSea**.

This collection lives inside **NFT Gallery** at `/inklings`.

Nothing is pixelated. Every layer is a soft, anti-aliased wash — paper grain, painterly visages, blinking eyes — composited onto one 16-frame clock. OpenSea Drops play GIF, so the marketplace pack is the GIF bake.

## What’s in the drop

- Trait art at `public/inklings-traits/` — each file is an APNG on a shared 640×640, 16-frame, 90ms loop
- Sample tokens at `public/inklings-preview/` (GIFs)
- Collection logo, featured image, OpenSea banner, site banner, and 1000×1000 collection GIF in `public/brand/`
- Paste-ready project description at `public/metadata/inklings-description.txt`
- Trait studio at `/inklings/studio` — a live CSS stack of APNG `<img>` layers
- `contracts/Inklings.sol` — ERC-721 with a 5,555 supply cap

## Generate traits and tokens

```bash
python3 scripts/build_inklings.py
python3 scripts/generate_inklings.py        # 16 samples
python3 scripts/generate_inklings.py --all  # full 5,555
python3 scripts/gif_bake.py --inklings --all
```

Requires Python 3 with Pillow and NumPy. Output lands in `generated/inklings/`.

## Trait stack

Every layer is already seated on the 640 canvas. Studio and the generator only stack:

1. Paper
2. Bloom
3. Visage
4. Gaze
5. Mark
6. Adorn

Visage, gaze, mark, and adorn share one breathe so the portrait stays locked. Paper and bloom move on their own washes. Minted tokens composite frame *n* of every layer so the marketplace file stays in sync.

Tokens 1–8 of the generated drop are the eight signature looks.

## Why APNG in the studio, GIF on OpenSea

APNG keeps per-pixel alpha, so transparent layers can stack in the browser. GIF cannot. OpenSea Drops play GIF, not APNG — upload `generated/inklings/gifs` plus `generated/inklings/INKLINGS-opensea-drop.csv`.
