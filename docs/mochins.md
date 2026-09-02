# Mochins

Looping **vinyl-toy mochi PFP GIFs** — gloss plastic, tight spec, clear coat, contact shadow, no outlines. A **4,000-piece** collection built to mint on **Shape** (chain ID `360`) and list on **OpenSea**.

This collection lives inside **NFT Gallery** at `/mochins`.

The look is designer-toy daifuku on a lacquered stand with a shared 16-frame clock. OpenSea does **not** assemble collections from trait layers. For a Drop you upload finished GIFs (max 10,000) plus a CSV. The generator flattens the live stack onto one 16-frame clock, then bakes those APNGs to GIF.

## What’s in the drop

- Trait art at `public/mochins-traits/` — each file is an APNG on a shared 512×512, 16-frame, 100ms loop
- Sample tokens at `public/mochins-preview/` (GIFs)
- Collection logo, featured image, OpenSea banner, site banner, and 1000×1000 collection GIF in `public/brand/`
- Paste-ready project description at `public/metadata/mochins-description.txt`
- Trait studio at `/mochins/studio` — a live CSS stack of APNG `<img>` layers
- `contracts/Mochins.sol` — ERC-721 with a 4,000 supply cap

## Generate traits and tokens

```bash
python3 scripts/build_mochins.py
python3 scripts/generate_mochins.py        # 16 samples
python3 scripts/generate_mochins.py --all  # full 4,000 GIFs (stays under OpenSea's 10 GB cap)
python3 scripts/gif_bake.py --mochins --all
```

Requires Python 3 with Pillow and NumPy. Output lands in `generated/mochins/`.

## Trait stack

Every layer is already seated on the 512 canvas. Studio and the generator only stack:

1. Stage
2. Haze
3. Vinyl
4. Face
5. Topping
6. Steam

Vinyl, face, and topping share one idle bob so the figure stays locked. Stage, haze, and steam move on their own loops. Minted tokens composite frame *n* of every layer so the marketplace file stays in sync.

Tokens 1–8 of the generated drop are the eight signature looks.

## Why APNG in the studio, GIF on OpenSea

APNG keeps per-pixel alpha, so transparent layers can stack in the browser. GIF cannot. OpenSea Drops play GIF, not APNG — upload `generated/mochins/gifs` plus `generated/mochins/MOCHINS-opensea-drop.csv`.
