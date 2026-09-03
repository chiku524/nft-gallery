# Foxins OpenSea kit

16 flattened bold-graphic fox loops at 512×512, 12 frames, 90ms (sample pack — bake all 5,555 with `--all`).

## Collection fields

- Name: `Foxins`
- Symbol: `FOXI`
- Category: PFPs
- Chain: Base (`8453`)
- Supply: `5555`
- Creator fee: `5%` (set your wallet — `public/metadata/foxins.json` still has a zero address)

## Paste this as the collection description

Same file: `public/metadata/foxins-description.txt`

```
Foxins.

A 5,555-piece collection of looping bold-graphic fox PFP GIFs. Each Foxin is stacked from six layers — field, pelt, mug, hat, wrap, and charm — then flattened onto one 12-frame GIF. Three pelts only: maple, snow, and dusk. The sticker never gets a special cutout. Hats sit between the ears. Scarves sit on the neck. Charms float by the paws.

Flat graphic — thick charcoal outline, limited palette, a little paper grain. Front-facing. Big circular head. Egg body. Tail on the right. One shared clock.

Minting on Base (chain ID 8453). Gas is ETH.
```

## Listing images

No type on the marketplace images.

| Use | File | Size |
|---|---|---|
| Logo | `public/brand/logo-foxins.png` | 512×512, 1:1 |
| Featured | `public/brand/featured-foxins.jpg` | 1200×800, 3:2 |
| OpenSea banner | `public/brand/banner-foxins-opensea.jpg` | 2800×700, 4:1 |
| Collection GIF | `public/brand/collection-foxins.gif` | 1000×1000, 12-frame loop |
| Site hero (not the OpenSea banner) | `public/brand/banner-foxins.png` | 1500×560 |

## Drop upload

1. In OpenSea Studio, create a Drop on Base (chain ID 8453).
2. Upload every file in `gifs/` (`1.gif`–`16.gif`).
3. Upload `FOXINS-opensea-drop.csv` (or `opensea-metadata.csv`). The CSV uses OpenSea Studio headers: `tokenID`, `name`, `description`, `file_name`, and `attributes[Trait]`.
4. Preview the loops, then publish.

OpenSea Drops play GIF, not APNG. Studio trait layers stay in `public/foxins-traits/` and are not the upload pack.
