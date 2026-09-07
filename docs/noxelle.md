# Noxelle

Looping **neon-tube PFP GIFs** — eight dancing bends of glass, noble-gas fill, wall clips, a club spill on the brick. A **10,000-piece** collection built to mint on **Robinhood Chain** (chain ID `4663`) at **$0.25** and list on **OpenSea**.

This collection lives inside **NFT Gallery** at `/noxelle`.

The look is bent tubing on a seated clock: sway, kick, wave, hop, point, dip, spin, split. Argon, neon, krypton, mercury. Hardware that holds the glass. Not leather puppets. Not risograph blots. Not doodle ink. Not sticker cutouts. Not oval-egg bodies. Not musical notes. OpenSea does **not** assemble collections from trait layers. For a Drop you upload finished GIFs (max 10,000) plus a CSV. The generator flattens the live stack onto one 12-frame clock, then bakes those APNGs to GIF.

## What’s in the drop

- Trait art at `public/noxelle-traits/` — each file is an APNG on a shared 512×512, 12-frame, 90ms loop
- Sample tokens at `public/noxelle-preview/` (GIFs)
- Collection logo, featured image, OpenSea banner, site banner, and 1000×1000 collection GIF in `public/brand/`
- Paste-ready project description at `public/metadata/noxelle-description.txt`
- Trait studio at `/noxelle/studio` — a live CSS stack of APNG `<img>` layers
- `contracts/Noxelle.sol` — ERC-721 named Noxelle with a 10,000 supply cap and a $0.25 mint (`0.0001` ETH starting price; owner can retune)

## Generate traits and tokens

```bash
python3 scripts/build_noxelle.py
python3 scripts/generate_noxelle.py        # 16 samples
python3 scripts/generate_noxelle.py --all  # full 10,000 GIFs + OpenSea kit
```

Requires Python 3 with Pillow and NumPy. The marketplace pack lives in `generated/noxelle/`: `gifs/` (`1.gif`–`10000.gif`), `NOXELLE-opensea-drop.csv`, `opensea-metadata.csv`, and the kit README. Each token is named `Tube #{id}`. GIFs stay off git; the CSV and sidecar files are committed.

## Trait stack

Every layer is already seated on the 512 canvas. Studio and the generator only stack:

1. Wall
2. Spill
3. Gas
4. Bend
5. Clip
6. Badge
7. Mote

Eight bends share one envelope. Clips and motes never edit the bend file. Minted tokens composite frame *n* of every layer so the marketplace file stays in sync.

Token 1 is the signature look — velvet wall, grape spill, argon gas, sway bend, transformer brick, moon badge, spark motes.

## Why APNG in the studio, GIF on OpenSea

APNG keeps per-pixel alpha, so transparent layers can stack in the browser. GIF cannot. OpenSea Drops play GIF, not APNG — upload `generated/noxelle/gifs` plus `generated/noxelle/NOXELLE-opensea-drop.csv`.
