# Vinylon

Looping **balloon-animal PFP GIFs**. A **10,000-piece** free-mint collection built to mint on **Robinhood Chain** (chain ID `4663`) and list on **OpenSea**.

This collection lives inside **NFT Gallery** at `/vinylon`.

Inflated tubes. Knots. A shine on the latex. Not a leather puppet. Not neon tubing. Not soy-ink blots. Not doodle ink. Not sticker cutouts. Not oval-egg bodies. OpenSea does **not** assemble collections from trait layers. For a Drop you upload finished GIFs (max 10,000) plus a CSV. The generator flattens the live stack onto one 12-frame GIF, then bakes those APNGs to GIF.

## What’s in the drop

- Trait art at `public/vinylon-traits/` — each file is an APNG on a shared 512×512, 12-frame, 90ms loop
- Sample tokens at `public/vinylon-preview/` (GIFs)
- Collection logo, featured image, OpenSea banner, site banner, and 1000×1000 collection GIF in `public/brand/`
- Paste-ready project description at `public/metadata/vinylon-description.txt`
- Trait studio at `/vinylon/studio` — a live CSS stack of APNG `<img>` layers
- `contracts/Vinylon.sol` — ERC-721 named Vinylon with a 10,000 supply cap and a free mint

## Generate traits and tokens

```bash
python scripts/build_vinylon.py
python scripts/generate_vinylon.py        # 16 samples
python scripts/generate_vinylon.py --all  # full 10,000 GIFs + OpenSea kit
```

Requires Python 3 with Pillow and NumPy. The marketplace pack lives in `generated/vinylon/`. Each token is named `Twist #{id}`. GIFs stay off git; the CSV and sidecar files are committed. Gallery samples only were baked for this drop.

## Trait stack

Studio and the generator stack: booth → latex → twist → knot → valve → gleam → confetti.
