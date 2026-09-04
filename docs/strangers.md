# Strangers

**24 unique looping paintings. Each artwork is an open edition.** An OpenSea collection on **Base** (chain ID `8453`).

This collection lives inside **NFT Gallery** at `/strangers`.

Strangers is not assembled from trait layers and does not share a house painter. Each token is painted by its own engine in `scripts/atelier/works/`. Neighboring works do not share a medium, palette, silhouette, or motion.

The composition is 1:1. The mint is an open edition. 512×512, 12 frames, 90ms.

## What’s in the drop

- Site loops at `public/strangers/1.png`–`24.png`
- Collection logo, featured image, site banner, OpenSea banner, and collection GIF in `public/brand/`
- Collection description at `public/metadata/strangers-description.txt`
- Salon at `/strangers/gallery` and a page per work at `/strangers/[id]`
- OpenSea pack at `generated/strangers/` (GIFs in `gifs/`)

## Generate the paintings

```bash
python3 scripts/build_strangers.py
```

Adding a work means adding a new file under `scripts/atelier/works/` that exports `WORK` and `paint(frame)`. Do not import sibling painters.

## OpenSea Open Editions

OpenSea plays GIF, PNG, JPG, and SVG — not APNG. Upload `generated/strangers/gifs` (1.gif–24.gif) plus `generated/strangers/opensea-metadata.csv`. Create 24 open-edition items on Base (chain ID `8453`), one per artwork. Mint price is 0.008 ETH.
