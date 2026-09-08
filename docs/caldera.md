# Caldera

Looping **hotel-matchbook PFP GIFs** — offset-printed cardboard on a cafe table, a phosphorous strike, a flame that flickers. A **10,000-piece** collection built to mint on **Robinhood Chain** (chain ID `4663`) at **$0.25** and list on **OpenSea**.

This collection lives inside **NFT Gallery** at `/caldera`.

The look is a souvenir matchbook on a seated clock: cactus, lodge, diner, buoy, crown, shield, palm, ticket. Paper tooth is the print. The flame is the loop. Not a tin toy. Not a snow globe. Not neon tubing. Not leather puppets. Not origami. Not an engraved bust. Not doodle ink. Not sticker cutouts. Not oval-egg bodies. OpenSea does **not** assemble collections from trait layers. For a Drop you upload finished GIFs (max 10,000) plus a CSV. The generator flattens the live stack onto one 12-frame GIF, then bakes those APNGs to GIF.

## What’s in the drop

- Trait art at `public/caldera-traits/` — each file is an APNG on a shared 512×512, 12-frame, 90ms loop
- Sample tokens at `public/caldera-preview/` (GIFs)
- Collection logo, featured image, OpenSea banner, site banner, and 1000×1000 collection GIF in `public/brand/`
- Paste-ready project description at `public/metadata/caldera-description.txt`
- Trait studio at `/caldera/studio` — a live CSS stack of APNG `<img>` layers
- `contracts/Caldera.sol` — ERC-721 named Caldera with a 10,000 supply cap and a $0.25 mint (`0.0001` ETH starting price; owner can retune)

## Generate traits and tokens

```bash
python scripts/build_caldera.py
python scripts/generate_caldera.py        # 16 samples
python scripts/generate_caldera.py --all  # full 10,000 GIFs + OpenSea kit
```

Requires Python 3 with Pillow and NumPy. The marketplace pack lives in `generated/caldera/`: `gifs/` (`1.gif`–`10000.gif`), `CALDERA-opensea-drop.csv`, `opensea-metadata.csv`, and the kit README. Each token is named `Match #{id}`. GIFs stay off git; the CSV and sidecar files are committed.

## Trait stack

Every layer is already seated on the 512 canvas. Studio and the generator only stack:

1. Cloth
2. Sleeve
3. Inn
4. Comb
5. Strike
6. Flame
7. Mark

Eight inns share one cafe cloth. The flame flickers on a shared clock. Minted tokens composite frame *n* of every layer so the marketplace file stays in sync.

Token 1 is the signature look — check cloth, kraft sleeve, cactus inn, white comb, grit strike, gold flame, room mark.

## Why APNG in the studio, GIF on OpenSea

APNG keeps per-pixel alpha, so transparent layers can stack in the browser. GIF cannot. OpenSea Drops play GIF, not APNG — upload `generated/caldera/gifs` plus `generated/caldera/CALDERA-opensea-drop.csv`.
