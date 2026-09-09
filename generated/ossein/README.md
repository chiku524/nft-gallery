# Ossein OpenSea kit

16 flattened anatomical-chart loops at 512×512, 12 frames, 90ms (sample pack — bake all 10,000 with `--all`).

## Collection fields

- Name: `Ossein`
- Symbol: `OSSN`
- Token name: `Chart #{id}`
- Category: PFPs
- Chain: Robinhood Chain (`4663`)
- Supply: `10000`
- Mint: free (`0 ETH`)
- Creator fee: `5%` (set your wallet — `public/metadata/ossein.json` still has a zero address)

## Paste this as the collection description

Same file: `public/metadata/ossein-description.txt`

```
Ossein.

A 10,000-piece collection of looping anatomical-chart PFP GIFs on Robinhood Chain. Each plate is stacked from seven plates — sheet, rule, specimen, joint, leader, stain, and chalk — then flattened onto one 12-frame GIF. Eight dancing specimens: cortical, avian, feline, equine, frog, ape, fish, and serpent. Ivory bone. Hairline ink. The step is the loop.

A medical chart, not a leather puppet. Not neon tubing. Not soy-ink blots. The specimen stays seated on one sheet. The dance is in the joints. One shared clock.

Minting free on Robinhood Chain (chain ID 4663). Gas is ETH.
```

## Listing images

No type on the marketplace images.

| Use | File | Size |
|---|---|---|
| Logo | `public/brand/logo-ossein.png` | 512×512, 1:1 |
| Featured | `public/brand/featured-ossein.jpg` | 1200×800, 3:2 |
| OpenSea banner | `public/brand/banner-ossein-opensea.jpg` | 2800×700, 4:1 |
| Collection GIF | `public/brand/collection-ossein.gif` | 1000×1000, 12-frame loop |
| Site hero (not the OpenSea banner) | `public/brand/banner-ossein.png` | 1500×560 |

## Drop upload

1. In OpenSea Studio, create a Drop on Robinhood Chain (chain ID 4663).
2. Upload every file in `gifs/` (`1.gif`–`16.gif`).
3. Upload `OSSN-opensea-drop.csv` (or `opensea-metadata.csv`).
4. Set mint price to free.
5. Preview the loops, then publish.

OpenSea Drops play GIF, not APNG. Studio trait layers stay in `public/ossein-traits/` and are not the upload pack.
