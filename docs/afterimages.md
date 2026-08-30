# Afterimages

**12 unique 1:1 APNG paintings.** An **OpenSea Drop** on **Robinhood Chain** (chain ID `4663`).

This collection lives inside **NFT Gallery** at `/afterimages`.

Unlike Loopkins, Afterimages is not assembled from trait layers. Each token is a finished looping painting — 640×640, 16 frames, 100ms — uploaded as-is.

## What’s in the drop

- Site previews at `public/afterimages/1.png`–`12.png`
- Collection logo, banner, and 1000×1000 collection GIF in `public/brand/`
- Viewing room at `/afterimages/gallery` and a page per painting at `/afterimages/[id]`
- OpenSea pack at `generated/afterimages/`
- `contracts/Afterimages.sol` — ERC-721 that mints a chosen token ID 1–12

## Generate the paintings

```bash
python3 scripts/build_afterimages.py
```

Requires Python 3 with Pillow and NumPy.

## OpenSea Drop

Upload `generated/afterimages/images` (1.png–12.png) plus `generated/afterimages/opensea-metadata.csv`. The CSV uses OpenSea Studio headers: `tokenID`, `name`, `description`, `file_name`, and `attributes[Trait]`.

## Why APNG, not GIF or MP4

APNG keeps the loop inside a PNG marketplace can list. GIF loses color. A still would be a poster. The file is the painting.
