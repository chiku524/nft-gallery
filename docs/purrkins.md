# Purrkins

Looping **chibi-cat PFP GIFs** — thick outlines, flat cel fills, streetwear on pastel desks. A **4,000-piece** collection built to mint on **HyperEVM** (chain ID `999`) and list on **OpenSea**.

This collection lives inside **NFT Gallery** at `/purrkins`.

The look is in the same kawaii-vector neighborhood as Hypurr (bust crop, streetwear, clean outlines) but the cats, coats, and loops are original. OpenSea does **not** assemble collections from trait layers. For a Drop you upload finished GIFs (max 10,000) plus a CSV. The generator flattens the live stack onto one 12-frame clock — the same clock Loopkins uses — then bakes those APNGs to GIF.

## What’s in the drop

- Trait art at `public/purrkins-traits/` — each file is an APNG on a shared 512×512, 12-frame, 80ms loop
- Sample tokens at `public/purrkins-preview/` (GIFs)
- Collection logo, featured image, OpenSea banner, site banner, and 1000×1000 collection GIF in `public/brand/`
- Paste-ready project description at `public/metadata/purrkins-description.txt`
- Trait studio at `/purrkins/studio` — a live CSS stack of APNG `<img>` layers
- `contracts/Purrkins.sol` — ERC-721 with a 4,000 supply cap

## Generate traits and tokens

```bash
python3 scripts/build_purrkins.py
python3 scripts/generate_purrkins.py        # 16 samples
python3 scripts/generate_purrkins.py --all  # full 4,000
python3 scripts/gif_bake.py --purrkins --all
```

Requires Python 3 with Pillow and NumPy. Output lands in `generated/purrkins/`.

## Trait stack

Every layer is already seated on the 512 canvas. Studio and the generator only stack:

1. Pad
2. Glow
3. Pelt
4. Fit
5. Mug
6. Gear

Pelt, fit, mug, and gear share one bob so the cat stays locked. Pad and glow move on their own loops. Minted tokens composite frame *n* of every layer so the marketplace file stays in sync.

Tokens 1–8 of the generated drop are the eight signature looks.

## Why APNG in the studio, GIF on OpenSea

APNG keeps per-pixel alpha, so transparent layers can stack in the browser. GIF cannot. OpenSea Drops play GIF, not APNG — upload `generated/purrkins/gifs` plus `generated/purrkins/PURRKINS-opensea-drop.csv`.
