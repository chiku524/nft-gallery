# Perfin

Looping **engraved postage-stamp PFP GIFs** — eight postal busts, intaglio hatch, perforated edges, a cancellation that walks. An **8,888-piece** free-mint collection built to mint on **Robinhood Chain** (chain ID `4663`) and list on **OpenSea**.

This collection lives inside **NFT Gallery** at `/perfin`.

The look is a franked rectangle on a seated clock: pilot, keeper, clerk, captain, botanist, mapper, signal, warden. Fine hatch. Guilloche. A killer that walks the face. Not risograph blots. Not doodle ink. Not sticker cutouts. Not an oval-egg body. Not musical notes. OpenSea does **not** assemble collections from trait layers. For a Drop you upload finished GIFs (max 10,000) plus a CSV. The generator flattens the live stack onto one 12-frame clock, then bakes those APNGs to GIF.

## What’s in the drop

- Trait art at `public/perfin-traits/` — each file is an APNG on a shared 512×512, 12-frame, 90ms loop
- Sample tokens at `public/perfin-preview/` (GIFs)
- Collection logo, featured image, OpenSea banner, site banner, and 1000×1000 collection GIF in `public/brand/`
- Paste-ready project description at `public/metadata/perfin-description.txt`
- Trait studio at `/perfin/studio` — a live CSS stack of APNG `<img>` layers
- `contracts/Perfin.sol` — ERC-721 named Perfin with an 8,888 supply cap and a free mint

## Generate traits and tokens

```bash
python3 scripts/build_perfin.py
python3 scripts/generate_perfin.py        # 16 samples
python3 scripts/generate_perfin.py --all  # full 8,888 GIFs + OpenSea kit
```

Requires Python 3 with Pillow and NumPy. The marketplace pack lives in `generated/perfin/`: `gifs/` (`1.gif`–`8888.gif`), `PERFIN-opensea-drop.csv`, `opensea-metadata.csv`, and the kit README. Each token is named `Perfin #{id}`. GIFs stay off git; the CSV and sidecar files are committed.

## Trait stack

Every layer is already seated on the 512 canvas. Studio and the generator only stack:

1. Wove
2. Guilloche
3. Bust
4. Surcharge
5. Aspect
6. Device
7. Cancel

Eight busts share one vignette. Cancels walk. Devices never edit the bust file. Minted tokens composite frame *n* of every layer so the marketplace file stays in sync.

Token 1 is the signature look — ivory wove, rose engine, pilot, no surcharge, calm, goggles, circular date.

## Why APNG in the studio, GIF on OpenSea

APNG keeps per-pixel alpha, so transparent layers can stack in the browser. GIF cannot. OpenSea Drops play GIF, not APNG — upload `generated/perfin/gifs` plus `generated/perfin/PERFIN-opensea-drop.csv`.
