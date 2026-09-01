# Party Pandas

Looping **cartoon party-panda PFP GIFs** with real panda markings — crisp outlines, cel shading, classic black-and-white patches. A **4,444-piece** collection built to mint on **Base** (chain ID `8453`) and list on **OpenSea**.

This collection lives inside **NFT Gallery** at `/party-pandas`.

OpenSea does **not** assemble collections from trait layers. For a Drop you upload finished GIFs (max 10,000) plus a CSV. The generator flattens the live stack onto one 12-frame clock — the same clock Loopkins uses — then bakes those APNGs to GIF.

## What’s in the drop

- Trait art at `public/party-pandas-traits/` — each file is an APNG on a shared 512×512, 12-frame, 80ms loop
- Sample tokens at `public/party-pandas-preview/` (GIFs)
- Collection logo, featured image, OpenSea banner, site banner, and 1000×1000 collection GIF in `public/brand/`
- Paste-ready project description at `public/metadata/party-pandas-description.txt`
- Trait studio at `/party-pandas/studio` — a live CSS stack of APNG `<img>` layers
- `contracts/PartyPandas.sol` — ERC-721 with a 4,444 supply cap

## Generate traits and tokens

```bash
python3 scripts/build_party_pandas.py
python3 scripts/generate_party_pandas.py        # 16 samples
python3 scripts/generate_party_pandas.py --all  # full 4,444
python3 scripts/gif_bake.py --party-pandas --all
```

Requires Python 3 with Pillow and NumPy. Output lands in `generated/party-pandas/`.

## Trait stack

Every layer is already seated on the 512 canvas. Studio and the generator only stack:

1. Venue
2. Glow
3. Panda
4. Mood
5. Fit
6. Extra

Panda, mood, fit, and extra share one bob so the panda stays locked. Venue and glow move on their own loops. Minted tokens composite frame *n* of every layer so the marketplace file stays in sync.

Tokens 1–8 of the generated drop are the eight signature looks.

## Why APNG in the studio, GIF on OpenSea

APNG keeps per-pixel alpha, so transparent layers can stack in the browser. GIF cannot. OpenSea Drops play GIF, not APNG — upload `generated/party-pandas/gifs` plus `generated/party-pandas/PARTY-PANDAS-opensea-drop.csv`.
