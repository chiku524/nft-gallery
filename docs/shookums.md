# Halloween Shook'ums

Looping **sheet-ghost PFP GIFs** — one plump sheet, two arm nubs, a scalloped hem, painted 3D volume, thick drawn outline, huge glossy eyes. A **5,555-piece** collection built to mint on **Abstract** (chain ID `2741`) and list on **OpenSea**.

This collection lives inside **NFT Gallery** at `/shookums`.

The look is sticker ghosts on a flat haunt field with a shared 12-frame clock. OpenSea does **not** assemble collections from trait layers. For a Drop you upload finished GIFs (max 10,000) plus a CSV. The generator flattens the live stack onto one 12-frame clock, then bakes those APNGs to GIF.

## What’s in the drop

- Trait art at `public/shookums-traits/` — each file is an APNG on a shared 512×512, 12-frame, 90ms loop
- Sample tokens at `public/shookums-preview/` (GIFs)
- Collection logo, featured image, OpenSea banner, site banner, and 1000×1000 collection GIF in `public/brand/`
- Paste-ready project description at `public/metadata/shookums-description.txt`
- Trait studio at `/shookums/studio` — a live CSS stack of APNG `<img>` layers
- `contracts/Shookums.sol` — ERC-721 named Halloween Shook'ums with a 5,555 supply cap

## Generate traits and tokens

```bash
python3 scripts/build_shookums.py
python3 scripts/generate_shookums.py        # 16 samples
python3 scripts/generate_shookums.py --all  # full 5,555 GIFs (stays under OpenSea's 10 GB cap)
python3 scripts/gif_bake.py --shookums --all
```

Requires Python 3 with Pillow and NumPy. Output lands in `generated/shookums/`.

## Trait stack

Every layer is already seated on the 512 canvas. Studio and the generator only stack:

1. Night
2. Sheet
3. Mug
4. Hat
5. Wrap
6. Charm

Three sheet bodies share one skeleton. Hats, wraps, and charms never edit the sheet file — they composite on the same crown, collar, and hands. Eyes blink. The sheet hovers. Minted tokens composite frame *n* of every layer so the marketplace file stays in sync.

Token 1 is the common base — parchment night, classic sheet, normal mug, no extras. Tokens 1–8 of the generated drop are the eight signature looks.

## Why APNG in the studio, GIF on OpenSea

APNG keeps per-pixel alpha, so transparent layers can stack in the browser. GIF cannot. OpenSea Drops play GIF, not APNG — upload `generated/shookums/gifs` plus `generated/shookums/SHOOKUMS-opensea-drop.csv`.
