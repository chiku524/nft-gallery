# Nivora

Looping **snow-globe PFP GIFs** — a dome of liquor on a lathe-turned plinth, a miniature vista, flakes that fall. A **10,000-piece** collection built to mint on **Robinhood Chain** (chain ID `4663`) at **$0.25** and list on **OpenSea**.

This collection lives inside **NFT Gallery** at `/nivora`.

The look is a souvenir object on a seated clock: cabin, pine, lighthouse, deer, chapel, tram, bridge, moon. Glycerin holds the flake. A collar seats the dome. Not a dancer. Not neon tubing. Not leather puppets. Not origami. Not an engraved bust. Not doodle ink. Not sticker cutouts. Not oval-egg bodies. OpenSea does **not** assemble collections from trait layers. For a Drop you upload finished GIFs (max 10,000) plus a CSV. The generator flattens the live stack onto one 12-frame GIF, then bakes those APNGs to GIF.

## What’s in the drop

- Trait art at `public/nivora-traits/` — each file is an APNG on a shared 512×512, 12-frame, 90ms loop
- Sample tokens at `public/nivora-preview/` (GIFs)
- Collection logo, featured image, OpenSea banner, site banner, and 1000×1000 collection GIF in `public/brand/`
- Paste-ready project description at `public/metadata/nivora-description.txt`
- Trait studio at `/nivora/studio` — a live CSS stack of APNG `<img>` layers
- `contracts/Nivora.sol` — ERC-721 named Nivora with a 10,000 supply cap and a $0.25 mint (`0.0001` ETH starting price; owner can retune)

## Generate traits and tokens

```bash
python scripts/build_nivora.py
python scripts/generate_nivora.py        # 16 samples
python scripts/generate_nivora.py --all  # full 10,000 GIFs + OpenSea kit
```

Requires Python 3 with Pillow and NumPy. The marketplace pack lives in `generated/nivora/`: `gifs/` (`1.gif`–`10000.gif`), `NIVORA-opensea-drop.csv`, `opensea-metadata.csv`, and the kit README. Each token is named `Globe #{id}`. GIFs stay off git; the CSV and sidecar files are committed.

## Trait stack

Every layer is already seated on the 512 canvas. Studio and the generator only stack:

1. Plinth
2. Bath
3. Vista
4. Flurry
5. Lens
6. Collar
7. Plaque

Eight vistas share one dome. Collar and plaque never edit the vista file. Minted tokens composite frame *n* of every layer so the marketplace file stays in sync. Flurry sits in front of the vista so flakes fall through the liquor.

Token 1 is the signature look — walnut plinth, gin bath, cabin vista, snow flurry, clear lens, brass collar, year plaque.

## Why APNG in the studio, GIF on OpenSea

APNG keeps per-pixel alpha, so transparent layers can stack in the browser. GIF cannot. OpenSea Drops play GIF, not APNG — upload `generated/nivora/gifs` plus `generated/nivora/NIVORA-opensea-drop.csv`.
