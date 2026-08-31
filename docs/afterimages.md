# Afterimages

**50 unique 1:1 APNG paintings.** An **OpenSea Drop** on **Robinhood Chain** (chain ID `4663`).

This collection lives inside **NFT Gallery** at `/afterimages`.

Unlike Loopkins, Afterimages is not assembled from trait layers. Each token is a finished looping painting — 640×640, 16 frames, 100ms. The site serves APNG. The OpenSea Drop is a GIF bake of the same loop.

## What’s in the drop

- Site previews at `public/afterimages/1.png`–`50.png`
- Collection logo, banner, and 1000×1000 collection GIF in `public/brand/`
- Viewing room at `/afterimages/gallery` and a page per painting at `/afterimages/[id]`
- OpenSea pack at `generated/afterimages/` (GIFs in `gifs/`)
- `contracts/Afterimages.sol` — ERC-721 that mints a chosen token ID 1–50

## Generate the paintings

```bash
python3 scripts/build_afterimages.py
python3 scripts/gif_bake.py --afterimages
```

Requires Python 3 with Pillow and NumPy.

## OpenSea Drop

OpenSea Drops play GIF, PNG, JPG, and SVG — not APNG. Upload `generated/afterimages/gifs` (1.gif–50.gif) plus `generated/afterimages/opensea-metadata.csv`. The CSV uses OpenSea Studio headers: `tokenID`, `name`, `description`, `file_name`, and `attributes[Trait]`.

## Why APNG on the site, GIF on OpenSea

APNG keeps the loop and color on this site. OpenSea’s pipeline treats `.png` as a still, so the Drop pack is a looping GIF of the same 16 frames.
