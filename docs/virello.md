# Virello

Looping **wind-up tin-toy PFP GIFs** — lithographed enamel on stamped metal, a toy-shop bench, a key that turns. A **10,000-piece** collection built to mint on **Robinhood Chain** (chain ID `4663`) at **$0.25** and list on **OpenSea**.

This collection lives inside **NFT Gallery** at `/virello`.

The look is a stamped souvenir on a seated clock: robot, duck, racer, soldier, monkey, tank, copter, frog. Print misregistration is the litho. The winding key is the loop. Not a snow globe. Not neon tubing. Not leather puppets. Not origami. Not an engraved bust. Not doodle ink. Not sticker cutouts. Not oval-egg bodies. OpenSea does **not** assemble collections from trait layers. For a Drop you upload finished GIFs (max 10,000) plus a CSV. The generator flattens the live stack onto one 12-frame GIF, then bakes those APNGs to GIF.

## What’s in the drop

- Trait art at `public/virello-traits/` — each file is an APNG on a shared 512×512, 12-frame, 90ms loop
- Sample tokens at `public/virello-preview/` (GIFs)
- Collection logo, featured image, OpenSea banner, site banner, and 1000×1000 collection GIF in `public/brand/`
- Paste-ready project description at `public/metadata/virello-description.txt`
- Trait studio at `/virello/studio` — a live CSS stack of APNG `<img>` layers
- `contracts/Virello.sol` — ERC-721 named Virello with a 10,000 supply cap and a $0.25 mint (`0.0001` ETH starting price; owner can retune)

## Generate traits and tokens

```bash
python scripts/build_virello.py
python scripts/generate_virello.py        # 16 samples
python scripts/generate_virello.py --all  # full 10,000 GIFs + OpenSea kit
```

Requires Python 3 with Pillow and NumPy. The marketplace pack lives in `generated/virello/`: `gifs/` (`1.gif`–`10000.gif`), `VIRELLO-opensea-drop.csv`, `opensea-metadata.csv`, and the kit README. Each token is named `Toy #{id}`. GIFs stay off git; the CSV and sidecar files are committed.

## Trait stack

Every layer is already seated on the 512 canvas. Studio and the generator only stack:

1. Bench
2. Chassis
3. Enamel
4. Decal
5. Key
6. Spark
7. Wear

Eight chassis share one bench. The winding key turns on a shared axle. Minted tokens composite frame *n* of every layer so the marketplace file stays in sync.

Token 1 is the signature look — linoleum bench, robot chassis, tomato enamel, star decal, brass key, flint spark, factory gloss.

## Why APNG in the studio, GIF on OpenSea

APNG keeps per-pixel alpha, so transparent layers can stack in the browser. GIF cannot. OpenSea Drops play GIF, not APNG — upload `generated/virello/gifs` plus `generated/virello/VIRELLO-opensea-drop.csv`.
