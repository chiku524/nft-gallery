# Cera

Looping **lava-lamp PFP GIFs** — paraffin in a glass flask on a nightstand, a heater coil, wax that rises. A **10,000-piece** collection built to mint on **Robinhood Chain** (chain ID `4663`) at **$0.25** and list on **OpenSea**.

This collection lives inside **NFT Gallery** at `/cera`.

The look is a 1970s lamp on a seated clock: rocket, saucer, cone, cube, mushroom, chrome, walnut, ceramic. The glass holds oil. The wax is the loop. Not a matchbook. Not a tin toy. Not a snow globe. Not neon tubing. Not leather puppets. Not origami. Not an engraved bust. Not doodle ink. Not sticker cutouts. Not oval-egg bodies. OpenSea does **not** assemble collections from trait layers. For a Drop you upload finished GIFs (max 10,000) plus a CSV. The generator flattens the live stack onto one 12-frame GIF, then bakes those APNGs to GIF.

## What’s in the drop

- Trait art at `public/cera-traits/` — each file is an APNG on a shared 512×512, 12-frame, 90ms loop
- Sample tokens at `public/cera-preview/` (GIFs)
- Collection logo, featured image, OpenSea banner, site banner, and 1000×1000 collection GIF in `public/brand/`
- Paste-ready project description at `public/metadata/cera-description.txt`
- Trait studio at `/cera/studio` — a live CSS stack of APNG `<img>` layers
- `contracts/Cera.sol` — ERC-721 named Cera with a 10,000 supply cap and a $0.25 mint (`0.0001` ETH starting price; owner can retune)

## Generate traits and tokens

```bash
python scripts/build_cera.py
python scripts/generate_cera.py        # 16 samples
python scripts/generate_cera.py --all  # full 10,000 GIFs + OpenSea kit
```

Requires Python 3 with Pillow and NumPy. The marketplace pack lives in `generated/cera/`: `gifs/` (`1.gif`–`10000.gif`), `CERA-opensea-drop.csv`, `opensea-metadata.csv`, and the kit README. Each token is named `Lamp #{id}`. GIFs stay off git; the CSV and sidecar files are committed.

## Trait stack

Every layer is already seated on the 512 canvas. Studio and the generator only stack:

1. Sill
2. Socket
3. Flask
4. Serum
5. Melt
6. Coil
7. Lid

Eight sockets share one inner liquid column. The paraffin rises on a shared clock. Minted tokens composite frame *n* of every layer so the marketplace file stays in sync.

Token 1 is the signature look — wood sill, rocket socket, taper flask, cyan serum, crimson melt, orange coil, chrome lid.

## Why APNG in the studio, GIF on OpenSea

APNG keeps per-pixel alpha, so transparent layers can stack in the browser. GIF cannot. OpenSea Drops play GIF, not APNG — upload `generated/cera/gifs` plus `generated/cera/CERA-opensea-drop.csv`.
