# Loopkins

Looping creatures stacked from **APNG trait layers**. A **10,000-piece** PFP collection built to mint on **Robinhood Chain** (chain ID `4663`) and list on **OpenSea**.

This collection lives inside **NFT Gallery** at `/loopkins`.

OpenSea does **not** assemble collections from trait layers. For a Drop you upload finished GIFs (max 10,000) plus a CSV. The generator flattens the live stack onto one 12-frame clock, then bakes those APNGs to GIF.

## What’s in the drop

- Trait art at `public/traits/` — each file is an APNG on a shared 512×512, 12-frame, 80ms loop
- Sample tokens at `public/generated-preview/`
- Collection logo, featured image, OpenSea banner, site banner, and 1000×1000 collection GIF in `public/brand/`
- Paste-ready project description at `public/metadata/loopkins-description.txt`
- Trait studio at `/studio` — a live CSS stack of APNG `<img>` layers (not a flattened canvas)
- `contracts/Loopkins.sol` — ERC-721 with a 10,000 supply cap

## Generate traits and tokens

```bash
python3 scripts/build_loopkins.py
python3 scripts/generate_collection.py        # 16 samples
python3 scripts/generate_collection.py --all  # full 10,000
python3 scripts/gif_bake.py --loopkins --all  # OpenSea GIFs
```

Requires Python 3 with Pillow and NumPy. Output lands in `generated/`.

## Trait stack

Every layer is already seated on the 512 canvas. Studio and the generator only stack:

1. Sky
2. Aura
3. Body
4. Face
5. Wear
6. Charm

Body, face, and wear share one bob so the creature stays locked. Sky, aura, and charm move on their own loops. Minted tokens composite frame *n* of every layer so the marketplace file stays in sync.

Tokens 1–8 of the generated drop are the eight signature looks.

## Why APNG in the studio, GIF on OpenSea

APNG keeps per-pixel alpha, so transparent layers can stack in the browser. GIF cannot. OpenSea Drops play GIF, not APNG — upload `generated/gifs` plus `generated/LOOPKINS-opensea-drop.csv`.
