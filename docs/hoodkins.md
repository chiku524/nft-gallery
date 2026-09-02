# Hoodkins

Looping **chibi-raccoon PFP GIFs** — thick outlines, flat cel fills, bandit masks, streetwear on ledger desks. A **10,000-piece** collection built to mint on **Robinhood Chain** (chain ID `4663`) and list on **OpenSea**.

This collection lives inside **NFT Gallery** at `/hoodkins`.

The look is kawaii bust-crop raccoons with a shared 12-frame clock. OpenSea does **not** assemble collections from trait layers. For a Drop you upload finished GIFs (max 10,000) plus a CSV. The generator flattens the live stack onto one 12-frame clock — the same clock Loopkins uses — then bakes those APNGs to GIF.

## What’s in the drop

- Trait art at `public/hoodkins-traits/` — each file is an APNG on a shared 512×512, 12-frame, 80ms loop
- Sample tokens at `public/hoodkins-preview/` (GIFs)
- Collection logo, featured image, OpenSea banner, site banner, and 1000×1000 collection GIF in `public/brand/`
- Paste-ready project description at `public/metadata/hoodkins-description.txt`
- Trait studio at `/hoodkins/studio` — a live CSS stack of APNG `<img>` layers
- `contracts/Hoodkins.sol` — ERC-721 with a 10,000 supply cap

## Generate traits and tokens

```bash
python3 scripts/build_hoodkins.py
python3 scripts/generate_hoodkins.py        # 16 samples
python3 scripts/generate_hoodkins.py --all  # full 10,000 GIFs (stays under OpenSea's 10 GB cap)
python3 scripts/gif_bake.py --hoodkins --all
```

Requires Python 3 with Pillow and NumPy. Output lands in `generated/hoodkins/`.

## Trait stack

Every layer is already seated on the 512 canvas. Studio and the generator only stack:

1. Pad
2. Glow
3. Pelt
4. Fit
5. Mug
6. Gear

Pelt, fit, mug, and gear share one bob so the raccoon stays locked. Pad and glow move on their own loops. Minted tokens composite frame *n* of every layer so the marketplace file stays in sync.

Tokens 1–8 of the generated drop are the eight signature looks.

## Why APNG in the studio, GIF on OpenSea

APNG keeps per-pixel alpha, so transparent layers can stack in the browser. GIF cannot. OpenSea Drops play GIF, not APNG — upload `generated/hoodkins/gifs` plus `generated/hoodkins/HOODKINS-opensea-drop.csv`.
