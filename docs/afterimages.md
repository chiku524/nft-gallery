# Afterimages

**3,333 unique 1:1 looping paintings.** An **OpenSea Drop** on **Ink** (chain ID `57073`).

This collection lives inside **NFT Gallery** at `/afterimages`.

Unlike Loopkins, Afterimages is not assembled from trait layers. Each token is a finished looping painting — 640×640, 16 frames, 100ms. Tokens 1–50 are signature APNGs on the site. The OpenSea Drop is a GIF bake of the full 3,333.

## What’s in the drop

- Signature site previews at `public/afterimages/1.png`–`50.png`
- Series previews at `public/afterimages-preview/51.gif`–`66.gif`
- Collection logo, featured image, site banner, OpenSea banner, and 1000×1000 collection GIF in `public/brand/`
- Collection description at `public/metadata/afterimages-description.txt`
- Viewing room at `/afterimages/gallery` and a page per signature painting at `/afterimages/[id]`
- OpenSea pack at `generated/afterimages/` (GIFs in `gifs/`)
- `contracts/Afterimages.sol` — ERC-721 that mints a chosen token ID 1–3333 on Ink

## Generate the paintings

```bash
python3 scripts/build_afterimages.py
python3 scripts/gif_bake.py --afterimages
```

`build_afterimages.py` paints any missing loops through 3,333 and writes `opensea-metadata.csv`. Signature tokens 1–50 are skipped if their APNGs already exist. Requires Python 3 with Pillow and NumPy.

## OpenSea Drop

OpenSea Drops play GIF, PNG, JPG, and SVG — not APNG. Upload `generated/afterimages/gifs` (1.gif–3333.gif) plus `generated/afterimages/opensea-metadata.csv`. The CSV uses OpenSea Studio headers: `tokenID`, `name`, `description`, `file_name`, and `attributes[Trait]`. Create the Drop on Ink (chain ID `57073`).

## Why APNG on the site, GIF on OpenSea

APNG keeps the loop and color on this site for the signature fifty. OpenSea’s pipeline treats `.png` as a still, so the Drop pack is a looping GIF of every token.
