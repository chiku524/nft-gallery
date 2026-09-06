# Umbra

Looping **shadow-puppet PFP GIFs** — eight dancing casts, leather silhouettes, brass hinges, an oil lamp behind a woven screen. An **8,888-piece** free-mint collection built to mint on **Robinhood Chain** (chain ID `4663`) and list on **OpenSea**.

This collection lives inside **NFT Gallery** at `/umbra`.

The look is a leather hide on a seated clock: clown, knight, bride, ogre, sage, harper, bird, demon. Brass brads. Cutwork that lets the lamp through. Not risograph blots. Not origami facets. Not engraved busts. Not doodle ink. Not sticker cutouts. OpenSea does **not** assemble collections from trait layers. For a Drop you upload finished GIFs (max 10,000) plus a CSV. The generator flattens the live stack onto one 12-frame clock, then bakes those APNGs to GIF.

## What’s in the drop

- Trait art at `public/umbra-traits/` — each file is an APNG on a shared 512×512, 12-frame, 90ms loop
- Sample tokens at `public/umbra-preview/` (GIFs)
- Collection logo, featured image, OpenSea banner, site banner, and 1000×1000 collection GIF in `public/brand/`
- Paste-ready project description at `public/metadata/umbra-description.txt`
- Trait studio at `/umbra/studio` — a live CSS stack of APNG `<img>` layers
- `contracts/Umbra.sol` — ERC-721 named Umbra with an 8,888 supply cap and a free mint

## Generate traits and tokens

```bash
python3 scripts/build_umbra.py
python3 scripts/generate_umbra.py        # 16 samples
python3 scripts/generate_umbra.py --all  # full 8,888 GIFs + OpenSea kit
```

Requires Python 3 with Pillow and NumPy. The marketplace pack lives in `generated/umbra/`: `gifs/` (`1.gif`–`8888.gif`), `UMBRA-opensea-drop.csv`, `opensea-metadata.csv`, and the kit README. Each token is named `Shade #{id}`. GIFs stay off git; the CSV and sidecar files are committed.

## Trait stack

Every layer is already seated on the 512 canvas. Studio and the generator only stack:

1. Cloth
2. Ember
3. Cast
4. Hinge
5. Cutwork
6. Leaf
7. Soot

Eight casts share one envelope. Hinges swing the dance. Soot never edits the cast file. Minted tokens composite frame *n* of every layer so the marketplace file stays in sync.

Token 1 is the signature look — parchment cloth, oil ember, clown, brass hinge, dot cutwork, gold rim, soot motes.

## Why APNG in the studio, GIF on OpenSea

APNG keeps per-pixel alpha, so transparent layers can stack in the browser. GIF cannot. OpenSea Drops play GIF, not APNG — upload `generated/umbra/gifs` plus `generated/umbra/UMBRA-opensea-drop.csv`.
