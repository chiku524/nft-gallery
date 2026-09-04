# Scribblins OpenSea kit

16 flattened doodle-critter loops at 512×512, 12 frames, 90ms (sample pack — bake all 5,555 with `--all`).

## Collection fields

- Name: `Scribblins`
- Symbol: `SCRIB`
- Category: PFPs
- Chain: Base (`8453`)
- Supply: `5555`
- Creator fee: `5%` (set your wallet — `public/metadata/scribblins.json` still has a zero address)

## Paste this as the collection description

Same file: `public/metadata/scribblins-description.txt`

```
Scribblins never try that hard.

A 5,555-piece collection of looping doodle-critter PFP GIFs on Base. Each Scribblin is stacked from six layers — field, body, mug, hat, wrap, and charm — then flattened onto one 12-frame GIF. Four bodies only: bunny, bear, pup, and frog. The drawing stays friendly — thick charcoal outline, big oval eyes, a little blush, warm paper instead of rainbow ink.

Hats sit on one crown. Scarves sit on the neck. Charms float beside the paws. One shared clock.

Minting on Base (chain ID 8453). Gas is ETH.
```

## Listing images

No type on the marketplace images.

| Use | File | Size |
|---|---|---|
| Logo | `public/brand/logo-scribblins.png` | 512×512, 1:1 |
| Featured | `public/brand/featured-scribblins.jpg` | 1200×800, 3:2 |
| OpenSea banner | `public/brand/banner-scribblins-opensea.jpg` | 2800×700, 4:1 |
| Collection GIF | `public/brand/collection-scribblins.gif` | 1000×1000, 12-frame loop |
| Site hero (not the OpenSea banner) | `public/brand/banner-scribblins.png` | 1500×560 |

## Drop upload

1. In OpenSea Studio, create a Drop on Base (chain ID 8453).
2. Upload every file in `gifs/` (`1.gif`–`16.gif`).
3. Upload `SCRIBBLINS-opensea-drop.csv` (or `opensea-metadata.csv`). The CSV uses OpenSea Studio headers: `tokenID`, `name`, `description`, `file_name`, and `attributes[Trait]`.
4. Preview the loops, then publish.

OpenSea Drops play GIF, not APNG. Studio trait layers stay in `public/scribblins-traits/` and are not the upload pack.
