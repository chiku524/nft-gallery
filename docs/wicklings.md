# Wicklings

Looping **paper-lantern PFP GIFs** — soft discs, translucent paper, a little flame with a face. A **3,333-piece** collection built to mint on **Arbitrum** (chain ID `42161`) and list on **OpenSea**.

This collection lives inside **NFT Gallery** at `/wicklings`.

OpenSea does **not** assemble collections from trait layers. For a Drop you upload finished GIFs (max 10,000) plus a CSV. The generator flattens the live stack onto one 12-frame clock — the same clock Loopkins uses — then bakes those APNGs to GIF.

## What’s in the drop

- Trait art at `public/wicklings-traits/` — each file is an APNG on a shared 512×512, 12-frame, 80ms loop
- Sample tokens at `public/wicklings-preview/` (GIFs)
- Collection logo, featured image, OpenSea banner, site banner, and 1000×1000 collection GIF in `public/brand/`
- Paste-ready project description at `public/metadata/wicklings-description.txt`
- Trait studio at `/wicklings/studio` — a live CSS stack of APNG `<img>` layers
- `contracts/Wicklings.sol` — ERC-721 with a 3,333 supply cap

## Generate traits and tokens

```bash
python3 scripts/build_wicklings.py
python3 scripts/generate_wicklings.py        # 16 samples
python3 scripts/generate_wicklings.py --all  # full 3,333
python3 scripts/gif_bake.py --wicklings --all
```

Requires Python 3 with Pillow and NumPy. Output lands in `generated/wicklings/`.

## Trait stack

Every layer is already seated on the 512 canvas. Studio and the generator only stack:

1. Night
2. Halo
3. Vessel
4. Wick
5. Wrap
6. Drift

Vessel, wick, and wrap share one hang so the lantern stays locked. Night, halo, and drift move on their own loops. Minted tokens composite frame *n* of every layer so the marketplace file stays in sync.

Tokens 1–8 of the generated drop are the eight signature hangs.

## Why APNG in the studio, GIF on OpenSea

APNG keeps per-pixel alpha, so transparent layers can stack in the browser. GIF cannot. OpenSea Drops play GIF, not APNG — upload `generated/wicklings/gifs` plus `generated/wicklings/WICKLINGS-opensea-drop.csv`.
