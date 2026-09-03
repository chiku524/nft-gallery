# Foxins

Looping **bold-graphic fox PFP GIFs** — one front-facing sticker, circular head, egg body, tail on the right, thick charcoal outline, limited palette. A **5,555-piece** collection built to mint on **Base** (chain ID `8453`) and list on **OpenSea**.

This collection lives inside **NFT Gallery** at `/foxins`.

The look is sticker foxes on a flat peach field with a shared 12-frame clock. OpenSea does **not** assemble collections from trait layers. For a Drop you upload finished GIFs (max 10,000) plus a CSV. The generator flattens the live stack onto one 12-frame clock, then bakes those APNGs to GIF.

## What’s in the drop

- Trait art at `public/foxins-traits/` — each file is an APNG on a shared 512×512, 12-frame, 90ms loop
- Sample tokens at `public/foxins-preview/` (GIFs)
- Collection logo, featured image, OpenSea banner, site banner, and 1000×1000 collection GIF in `public/brand/`
- Paste-ready project description at `public/metadata/foxins-description.txt`
- Trait studio at `/foxins/studio` — a live CSS stack of APNG `<img>` layers
- `contracts/Foxins.sol` — ERC-721 named Foxins with a 5,555 supply cap

## Generate traits and tokens

```bash
python3 scripts/build_foxins.py
python3 scripts/generate_foxins.py        # 16 samples
python3 scripts/generate_foxins.py --all  # full 5,555 GIFs (stays under OpenSea's 10 GB cap)
python3 scripts/gif_bake.py --foxins --all
```

Requires Python 3 with Pillow and NumPy. Output lands in `generated/foxins/`.

## Trait stack

Every layer is already seated on the 512 canvas. Studio and the generator only stack:

1. Field
2. Pelt
3. Mug
4. Hat
5. Wrap
6. Charm

Three pelt bodies share one Style 5 graphic skeleton. Hats, wraps, and charms never edit the pelt file — they composite on the same crown, collar, and paws. Eyes blink. The sticker hovers. Minted tokens composite frame *n* of every layer so the marketplace file stays in sync.

Token 1 is the common base — peach field, maple pelt, normal mug, no extras. Tokens 1–8 of the generated drop are the eight signature looks.

## Why APNG in the studio, GIF on OpenSea

APNG keeps per-pixel alpha, so transparent layers can stack in the browser. GIF cannot. OpenSea Drops play GIF, not APNG — upload `generated/foxins/gifs` plus `generated/foxins/FOXINS-opensea-drop.csv`.
