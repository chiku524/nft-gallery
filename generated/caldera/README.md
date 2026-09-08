# Caldera OpenSea kit

16 flattened hotel-matchbook loops at 512×512, 12 frames, 90ms (sample pack — bake all 10,000 with `--all`).

## Collection fields

- Name: `Caldera`
- Symbol: `CALD`
- Token name: `Match #{id}`
- Category: PFPs
- Chain: Robinhood Chain (`4663`)
- Supply: `10000`
- Mint: `$0.25` (about `0.0001` ETH at listing; set the live ETH amount in OpenSea)
- Creator fee: `5%` (set your wallet — `public/metadata/caldera.json` still has a zero address)

## Paste this as the collection description

Same file: `public/metadata/caldera-description.txt`

```
Caldera.

A 10,000-piece collection of looping hotel-matchbook PFP GIFs on Robinhood Chain. Each book is stacked from seven plates — cloth, sleeve, inn, comb, strike, flame, and mark — then flattened onto one 12-frame GIF. Eight inns: cactus, lodge, diner, buoy, crown, shield, palm, and ticket. The print is cardboard. The flame is the loop.

A souvenir matchbook on a cafe cloth, not a tin toy. Not a snow globe. Not neon tubing. No sticker edge. No egg. Not a shadow puppet. Not a fold. The book stays seated on one envelope. The strike is the flame. One shared clock.

Minting at $0.25 on Robinhood Chain (chain ID 4663). Gas is ETH.
```

## Listing images

No type on the marketplace images.

| Use | File | Size |
|---|---|---|
| Logo | `public/brand/logo-caldera.png` | 512×512, 1:1 |
| Featured | `public/brand/featured-caldera.jpg` | 1200×800, 3:2 |
| OpenSea banner | `public/brand/banner-caldera-opensea.jpg` | 2800×700, 4:1 |
| Collection GIF | `public/brand/collection-caldera.gif` | 1000×1000, 12-frame loop |
| Site hero (not the OpenSea banner) | `public/brand/banner-caldera.png` | 1500×560 |

## Drop upload

1. In OpenSea Studio, create a Drop on Robinhood Chain (chain ID 4663).
2. Upload every file in `gifs/` (`1.gif`–`16.gif`).
3. Upload `CALDERA-opensea-drop.csv` (or `opensea-metadata.csv`). The CSV uses OpenSea Studio headers: `tokenID`, `name`, `description`, `file_name`, and `attributes[Trait]`.
4. Set mint price to $0.25.
5. Preview the loops, then publish.

OpenSea Drops play GIF, not APNG. Studio trait layers stay in `public/caldera-traits/` and are not the upload pack.
