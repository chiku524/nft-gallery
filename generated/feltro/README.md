# Feltro OpenSea kit

16 flattened foam-mascot loops at 512×512, 12 frames, 90ms (sample pack — bake all 10,000 with `--all`).

## Collection fields

- Name: `Feltro`
- Symbol: `FLTR`
- Token name: `Suit #{id}`
- Category: PFPs
- Chain: Robinhood Chain (`4663`)
- Supply: `10000`
- Mint: free (`0 ETH`)
- Creator fee: `5%` (set your wallet — `public/metadata/feltro.json` still has a zero address)

## Paste this as the collection description

Same file: `public/metadata/feltro-description.txt`

```
Feltro.

A 10,000-piece collection of looping foam-mascot PFP GIFs on Robinhood Chain. Each suit is stacked from seven plates — gym, suit, nap, mesh, seam, crest, and fuzz — then flattened onto one 12-frame GIF. Eight dancing suits: bear, lion, frog, bunny, dino, wolf, octopus, and shark. Mesh covers the eyes. A seam runs the cylinder. The bounce is the loop.

Plush foam on a court. Not a leather puppet. Not neon tubing. Not soy-ink blots. The suit stays seated in one envelope. The dance is the squash. One shared clock.

Minting free on Robinhood Chain (chain ID 4663). Gas is ETH.
```

## Listing images

No type on the marketplace images.

| Use | File | Size |
|---|---|---|
| Logo | `public/brand/logo-feltro.png` | 512×512, 1:1 |
| Featured | `public/brand/featured-feltro.jpg` | 1200×800, 3:2 |
| OpenSea banner | `public/brand/banner-feltro-opensea.jpg` | 2800×700, 4:1 |
| Collection GIF | `public/brand/collection-feltro.gif` | 1000×1000, 12-frame loop |
| Site hero (not the OpenSea banner) | `public/brand/banner-feltro.png` | 1500×560 |

## Drop upload

1. In OpenSea Studio, create a Drop on Robinhood Chain (chain ID 4663).
2. Upload every file in `gifs/` (`1.gif`–`16.gif`).
3. Upload `FLTR-opensea-drop.csv` (or `opensea-metadata.csv`).
4. Set mint price to free.
5. Preview the loops, then publish.

OpenSea Drops play GIF, not APNG. Studio trait layers stay in `public/feltro-traits/` and are not the upload pack.
