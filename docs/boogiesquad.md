# Boogie Squad

Looping **jelly-cel dance PFP GIFs** — mixed cartoon dancers (cats, frogs, blobs, birds, little robots, and more) on a party floor. A **10,000-piece** collection built to mint on **Robinhood Chain** (chain ID `4663`) and list on **OpenSea**.

This collection lives inside **NFT Gallery** at `/boogiesquad`.

The look is full-body chibi dancers with sausage limbs, cream outlines, and a shared 12-frame groove. OpenSea does **not** assemble collections from trait layers. For a Drop you upload finished GIFs (max 10,000) plus a CSV. The generator flattens the live stack onto one 12-frame clock, then bakes those APNGs to GIF.

## What’s in the drop

- Trait art at `public/boogiesquad-traits/` — each file is an APNG on a shared 512×512, 12-frame, 90ms loop
- Sample tokens at `public/boogiesquad-preview/` (GIFs)
- Collection logo, featured image, OpenSea banner, site banner, and 1000×1000 collection GIF in `public/brand/`
- Paste-ready project description at `public/metadata/boogiesquad-description.txt`
- Trait studio at `/boogiesquad/studio` — a live CSS stack of APNG `<img>` layers
- `contracts/BoogieSquad.sol` — ERC-721 named Boogie Squad with a 10,000 supply cap

## Generate traits and tokens

```bash
python3 scripts/build_boogiesquad.py
python3 scripts/generate_boogiesquad.py        # full 10,000 metadata + 16 preview GIFs
python3 scripts/generate_boogiesquad.py --all  # full 10,000 GIFs (stays under OpenSea's 10 GB cap)
python3 scripts/gif_bake.py --boogiesquad --all
```

Requires Python 3 with Pillow and NumPy. Output lands in `generated/boogiesquad/`.

`npm run generate:boogiesquad` runs the build + generate pair (preview GIF bake). Use `--all` on the generate script for the full OpenSea pack.

## Trait stack

Every layer is already seated on the 512 canvas. Studio and the generator only stack:

1. Stage
2. Lights
3. Cast
4. Face
5. Fit
6. Prop

Cast, face, fit, and prop share one side-step groove so the dancer stays locked. Stage and lights move on their own loops. Minted tokens composite frame *n* of every layer so the marketplace file stays in sync.

Token 1 is the common base — dance floor, peach cat, hype face, no extras. Tokens 1–8 of the generated drop are the eight signature looks.

## Why APNG in the studio, GIF on OpenSea

APNG keeps per-pixel alpha, so transparent layers can stack in the browser. GIF cannot. OpenSea Drops play GIF, not APNG — upload `generated/boogiesquad/gifs` plus `generated/boogiesquad/BOOG-opensea-drop.csv`.
