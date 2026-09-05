# Risota

Looping **risograph PFP GIFs** — eight dancing characters printed as overlapping spot-ink plates on uncoated paper. An **8,888-piece** collection built to mint on **Robinhood Chain** (chain ID `4663`) and list on **OpenSea**.

This collection lives inside **NFT Gallery** at `/risota`.

The look is soy ink on a seated clock: kick, twirl, pop, sway, hop, glide, stomp, reach. Fat blots. Halftone mesh. A second plate that misses the register. Not doodle ink. Not sticker cutouts. Not an oval-egg body. Not musical notes. OpenSea does **not** assemble collections from trait layers. For a Drop you upload finished GIFs (max 10,000) plus a CSV. The generator flattens the live stack onto one 12-frame clock, then bakes those APNGs to GIF.

## What’s in the drop

- Trait art at `public/risota-traits/` — each file is an APNG on a shared 512×512, 12-frame, 90ms loop
- Sample tokens at `public/risota-preview/` (GIFs)
- Collection logo, featured image, OpenSea banner, site banner, and 1000×1000 collection GIF in `public/brand/`
- Paste-ready project description at `public/metadata/risota-description.txt`
- Trait studio at `/risota/studio` — a live CSS stack of APNG `<img>` layers
- `contracts/Risota.sol` — ERC-721 named Risota with an 8,888 supply cap

## Generate traits and tokens

```bash
python3 scripts/build_risota.py
python3 scripts/generate_risota.py        # 16 samples
python3 scripts/generate_risota.py --all  # full 8,888 GIFs + OpenSea kit
```

Requires Python 3 with Pillow and NumPy. The marketplace pack lives in `generated/risota/`: `gifs/` (`1.gif`–`8888.gif`), `RISOTA-opensea-drop.csv`, `opensea-metadata.csv`, and the kit README. Each token is named `Print #{id}`. GIFs stay off git; the CSV and sidecar files are committed.

## Trait stack

Every layer is already seated on the 512 canvas. Studio and the generator only stack:

1. Stock
2. Screen
3. Figure
4. Pass
5. Knockout
6. Slug
7. Mark

Eight dancers share one envelope. Pass plates slide out of register. Slugs and marks never edit the figure file. Minted tokens composite frame *n* of every layer so the marketplace file stays in sync.

Token 1 is the signature look — cream sheet, rosa mesh, kick, smock pass, grin, kerchief, reg ticks.

## Why APNG in the studio, GIF on OpenSea

APNG keeps per-pixel alpha, so transparent layers can stack in the browser. GIF cannot. OpenSea Drops play GIF, not APNG — upload `generated/risota/gifs` plus `generated/risota/RISOTA-opensea-drop.csv`.
