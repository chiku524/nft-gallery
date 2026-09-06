# Kamiori

Looping **origami PFP GIFs** — eight paper folds, polygonal facets, valley and mountain scores, a corner that lifts. An **8,888-piece** free-mint collection built to mint on **Robinhood Chain** (chain ID `4663`) and list on **OpenSea**.

This collection lives inside **NFT Gallery** at `/kamiori`.

The look is a deckle sheet on a seated clock: crane, frog, beetle, boat, hare, fan, kite, lotus. Crease scores. A draft that lifts one corner. Not engraved busts. Not perforated stamps. Not risograph blots. Not doodle ink. Not sticker cutouts. OpenSea does **not** assemble collections from trait layers. For a Drop you upload finished GIFs (max 10,000) plus a CSV. The generator flattens the live stack onto one 12-frame clock, then bakes those APNGs to GIF.

## What’s in the drop

- Trait art at `public/kamiori-traits/` — each file is an APNG on a shared 512×512, 12-frame, 90ms loop
- Sample tokens at `public/kamiori-preview/` (GIFs)
- Collection logo, featured image, OpenSea banner, site banner, and 1000×1000 collection GIF in `public/brand/`
- Paste-ready project description at `public/metadata/kamiori-description.txt`
- Trait studio at `/kamiori/studio` — a live CSS stack of APNG `<img>` layers
- `contracts/Kamiori.sol` — ERC-721 named Kamiori with an 8,888 supply cap and a free mint

## Generate traits and tokens

```bash
python3 scripts/build_kamiori.py
python3 scripts/generate_kamiori.py        # 16 samples
python3 scripts/generate_kamiori.py --all  # full 8,888 GIFs + OpenSea kit
```

Requires Python 3 with Pillow and NumPy. The marketplace pack lives in `generated/kamiori/`: `gifs/` (`1.gif`–`8888.gif`), `KAMIORI-opensea-drop.csv`, `opensea-metadata.csv`, and the kit README. Each token is named `Fold #{id}`. GIFs stay off git; the CSV and sidecar files are committed.

## Trait stack

Every layer is already seated on the 512 canvas. Studio and the generator only stack:

1. Pulp
2. Fleck
3. Fold
4. Score
5. Facet
6. Seal
7. Draft

Eight folds share one envelope. Drafts lift a corner. Seals never edit the fold file. Minted tokens composite frame *n* of every layer so the marketplace file stays in sync.

Token 1 is the signature look — cream washi, kozo fiber, crane, mountain fold, no facet, hanko, corner lift.

## Why APNG in the studio, GIF on OpenSea

APNG keeps per-pixel alpha, so transparent layers can stack in the browser. GIF cannot. OpenSea Drops play GIF, not APNG — upload `generated/kamiori/gifs` plus `generated/kamiori/KAMIORI-opensea-drop.csv`.
