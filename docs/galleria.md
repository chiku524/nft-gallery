# Galleria On Ink

**500 unique looping paintings. Each artwork is an open edition.** An OpenSea collection on **Ink** (chain ID `57073`). Symbol **GOI**.

This collection lives inside **NFT Gallery** at `/galleria`.

Galleria On Ink is not assembled from trait layers and does not share a house painter. Each token is painted by its own engine in `scripts/atelier/works/`. Neighboring works do not share a medium, palette, silhouette, or motion.

The composition is 1:1. The mint is an open edition. 512×512, 12 frames, 90ms.

## What’s in the drop

- Site loops at `public/galleria/1.png`–`500.png`
- Salon stills at `public/galleria/thumbs/` so the 500-work grid stays light
- Collection logo, featured image, site banner, OpenSea banner, and collection GIF in `public/brand/`
- Collection description at `public/metadata/galleria-description.txt`
- Salon at `/galleria/gallery` and a page per work at `/galleria/[id]`
- OpenSea pack at `generated/galleria/` (GIFs in `gifs/`)

## Generate the paintings

```bash
python3 scripts/build_galleria.py
```

Adding a work means adding a new file under `scripts/atelier/works/` that exports `WORK` and `paint(frame)`. Do not import sibling painters. Works 51–500 were emitted by `scripts/atelier/expand_salon.py` (thirty interleaved drawing families, unique media names).

## OpenSea Open Editions

OpenSea plays GIF, PNG, JPG, and SVG — not APNG. Upload `generated/galleria/gifs` (1.gif–500.gif) plus `generated/galleria/opensea-metadata.csv`. Create 500 open-edition items on Ink (chain ID `57073`), one per artwork. Mint price is 0.008 ETH.
