# BirbNation

Looping **round-borb robin PFP GIFs** — one fat sphere, chocolate cap, burnt-orange chest, cream belly, painted 3D volume, thick drawn outline, huge glossy eyes. A **2,222-piece** collection built to mint on **Robinhood Chain** (chain ID `4663`) and list on **OpenSea**.

This collection lives inside **NFT Gallery** at `/birbs`.

The look is sticker robins on a flat field with a shared 12-frame clock. OpenSea does **not** assemble collections from trait layers. For a Drop you upload finished GIFs (max 10,000) plus a CSV. The generator flattens the live stack onto one 12-frame clock, then bakes those APNGs to GIF.

## What’s in the drop

- Trait art at `public/birbs-traits/` — each file is an APNG on a shared 512×512, 12-frame, 90ms loop
- Sample tokens at `public/birbs-preview/` (GIFs)
- Collection logo, featured image, OpenSea banner, site banner, and 1000×1000 collection GIF in `public/brand/`
- Paste-ready project description at `public/metadata/birbs-description.txt`
- Trait studio at `/birbs/studio` — a live CSS stack of APNG `<img>` layers
- `contracts/Birbs.sol` — ERC-721 named BirbNation with a 2,222 supply cap

## Generate traits and tokens

```bash
python3 scripts/build_birbs.py
python3 scripts/generate_birbs.py        # 16 samples
python3 scripts/generate_birbs.py --all  # full 2,222 GIFs (stays under OpenSea's 10 GB cap)
python3 scripts/gif_bake.py --birbs --all
```

Requires Python 3 with Pillow and NumPy. Output lands in `generated/birbs/`.

## Trait stack

Every layer is already seated on the 512 canvas. Studio and the generator only stack:

1. Field
2. Plumage
3. Mug
4. Accent

The sphere stays locked. Eyes blink. Wings twitch. Accents bob. Minted tokens composite frame *n* of every layer so the marketplace file stays in sync.

Token 1 is the common base — white field, brown plumage, blep, no accent. Tokens 1–8 of the generated drop are the eight signature looks.

## Why APNG in the studio, GIF on OpenSea

APNG keeps per-pixel alpha, so transparent layers can stack in the browser. GIF cannot. OpenSea Drops play GIF, not APNG — upload `generated/birbs/gifs` plus `generated/birbs/BIRBS-opensea-drop.csv`.
