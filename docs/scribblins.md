# Scribblins

Looping **doodle-critter PFP GIFs** — thick charcoal outline, warm paper fills, four friendly cartoon animals. A **5,555-piece** collection built to mint on **Base** (chain ID `8453`) and list on **OpenSea**.

This collection lives inside **NFT Gallery** at `/scribblins`.

The look is marker-on-paper cartoon friends (bunny, bear, pup, frog) on a cream field with a shared 12-frame clock. Not rainbow. OpenSea does **not** assemble collections from trait layers. For a Drop you upload finished GIFs (max 10,000) plus a CSV. The generator flattens the live stack onto one 12-frame clock, then bakes those APNGs to GIF.

## What’s in the drop

- Trait art at `public/scribblins-traits/` — each file is an APNG on a shared 512×512, 12-frame, 90ms loop
- Sample tokens at `public/scribblins-preview/` (GIFs)
- Collection logo, featured image, OpenSea banner, site banner, and 1000×1000 collection GIF in `public/brand/`
- Paste-ready project description at `public/metadata/scribblins-description.txt`
- Trait studio at `/scribblins/studio` — a live CSS stack of APNG `<img>` layers
- `contracts/Scribblins.sol` — ERC-721 named Scribblins with a 5,555 supply cap

## Generate traits and tokens

```bash
python3 scripts/build_scribblins.py
python3 scripts/generate_scribblins.py        # 16 samples
python3 scripts/generate_scribblins.py --all  # full 5,555 GIFs (stays under OpenSea's 10 GB cap)
python3 scripts/gif_bake.py --scribblins --all
```

Requires Python 3 with Pillow and NumPy. Output lands in `generated/scribblins/`.

## Trait stack

Every layer is already seated on the 512 canvas. Studio and the generator only stack:

1. Field
2. Body
3. Mug
4. Hat
5. Wrap
6. Charm

Four doodle bodies share one locked skeleton. Hats, wraps, and charms never edit the body file — they composite on the same crown, collar, and paws. Eyes blink. The doodle hovers. Minted tokens composite frame *n* of every layer so the marketplace file stays in sync.

Token 1 is the signature look — cream field, honey bunny, grin, headphones, star.

## Why APNG in the studio, GIF on OpenSea

APNG keeps per-pixel alpha, so transparent layers can stack in the browser. GIF cannot. OpenSea Drops play GIF, not APNG — upload `generated/scribblins/gifs` plus `generated/scribblins/SCRIBBLINS-opensea-drop.csv`.
