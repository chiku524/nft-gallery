# Opaline

Looping **smoked-glass PFP GIFs** — eight crystal reef fish, dichroic film, editorial studio light. A **5,555-piece** collection built to mint on **Base** (chain ID `8453`) and list on **OpenSea**.

This collection lives inside **NFT Gallery** at `/opaline`.

The look is cut-glass reef fish on a seated clock: parrotfish, blue marlin, queen angelfish, lionfish, triggerfish, seahorse, green moray, manta. Not doodle ink. Not sticker cutouts. Not an oval-egg body. OpenSea does **not** assemble collections from trait layers. For a Drop you upload finished GIFs (max 10,000) plus a CSV. The generator flattens the live stack onto one 12-frame clock, then bakes those APNGs to GIF.

## What’s in the drop

- Trait art at `public/opaline-traits/` — each file is an APNG on a shared 512×512, 12-frame, 90ms loop
- Sample tokens at `public/opaline-preview/` (GIFs)
- Collection logo, featured image, OpenSea banner, site banner, and 1000×1000 collection GIF in `public/brand/`
- Paste-ready project description at `public/metadata/opaline-description.txt`
- Trait studio at `/opaline/studio` — a live CSS stack of APNG `<img>` layers
- `contracts/Opaline.sol` — ERC-721 named Opaline with a 5,555 supply cap

## Generate traits and tokens

```bash
python3 scripts/build_opaline.py
python3 scripts/generate_opaline.py        # 16 samples
python3 scripts/generate_opaline.py --all  # full 5,555 GIFs + OpenSea kit
```

Requires Python 3 with Pillow and NumPy. The marketplace pack lives in `generated/opaline/`: `gifs/` (`1.gif`–`5555.gif`), `OPALINE-opensea-drop.csv`, `opensea-metadata.csv`, and the kit README. GIFs stay off git; the CSV and sidecar files are committed.

## Trait stack

Every layer is already seated on the 512 canvas. Studio and the generator only stack:

1. Atelier
2. Vapor
3. Cast
4. Sheen
5. Regard
6. Crest
7. Clasp

Eight reef fish share one eye line. Vapor hangs behind the animal. Crests and clasps never edit the cast file — they composite on the same crown and throat. Light walks the facets. Film shifts hue. Minted tokens composite frame *n* of every layer so the marketplace file stays in sync.

Token 1 is the signature look — dusk chamber, pale disc, parrotfish, oil film, quiet regard, platinum band, glass drop.

## Why APNG in the studio, GIF on OpenSea

APNG keeps per-pixel alpha, so transparent layers can stack in the browser. GIF cannot. OpenSea Drops play GIF, not APNG — upload `generated/opaline/gifs` plus `generated/opaline/OPALINE-opensea-drop.csv`.
