# Galleria On Ink OpenSea kit

500 unique looping paintings at 512×512, 12 frames, 90ms. Each artwork is an open edition.

## Collection fields

- Name: `Galleria On Ink`
- Symbol: `GOI`
- Category: Art
- Chain: Ink (`57073`)
- Works: `500` open editions (one item per painting; do not set unique 1:1 supply)
- Mint: `0.008 ETH`
- Creator fee: `7.5%` (set your wallet — `public/metadata/galleria.json` still has a zero address)

## Paste this as the collection description

Same file: `public/metadata/galleria-description.txt`

```
Galleria On Ink.

A salon of 500 unique looping paintings on Ink. Each work invents its own medium, palette, silhouette, and motion. Neighboring tokens are not siblings. There is no trait stack and no shared character.

Every artwork is an open edition. The composition is 1:1. The mint is not.

Twelve frames, ninety milliseconds, 512×512. Minting on Ink (chain ID 57073). Gas is ETH.
```

## Listing images

No type on the marketplace images.

| Use | File | Size |
|---|---|---|
| Logo | `public/brand/logo-galleria.png` | 512×512, 1:1 |
| Featured | `public/brand/featured-galleria.jpg` | 1200×800, 3:2 |
| OpenSea banner | `public/brand/banner-galleria-opensea.jpg` | 2800×700, 4:1 |
| Collection GIF | `public/brand/collection-galleria.gif` | 1000×1000, 12-frame loop |
| Site hero (not the OpenSea banner) | `public/brand/banner-galleria.png` | 1500×560 |

## Open edition upload

1. In OpenSea Studio, create an Open Edition collection on Ink (chain ID 57073).
2. Add 500 open-edition items — one per artwork. Do not set unique 1:1 supply.
3. Upload every file in `gifs/` (`1.gif`–`500.gif`).
4. Upload `GOI-opensea-drop.csv` (or `opensea-metadata.csv`). The CSV uses OpenSea Studio headers: `tokenID`, `name`, `description`, `file_name`, and `attributes[Trait]`.
5. Paste the collection description, upload the listing images, set mint to 0.008 ETH, then publish.

OpenSea plays GIF, not APNG. The site keeps the APNGs in `public/galleria/`.
