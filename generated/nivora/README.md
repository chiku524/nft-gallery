# Nivora OpenSea kit

16 flattened snow-globe loops at 512×512, 12 frames, 90ms (sample pack — bake all 10,000 with `--all`).

## Collection fields

- Name: `Nivora`
- Symbol: `NIVO`
- Token name: `Globe #{id}`
- Category: PFPs
- Chain: Robinhood Chain (`4663`)
- Supply: `10000`
- Mint: `$0.25` (about `0.0001` ETH at listing; set the live ETH amount in OpenSea)
- Creator fee: `5%` (set your wallet — `public/metadata/nivora.json` still has a zero address)

## Paste this as the collection description

Same file: `public/metadata/nivora-description.txt`

```
Nivora.

A 10,000-piece collection of looping snow-globe PFP GIFs on Robinhood Chain. Each souvenir is stacked from seven plates — plinth, bath, vista, flurry, lens, collar, and plaque — then flattened onto one 12-frame GIF. Eight vistas: cabin, pine, lighthouse, deer, chapel, tram, bridge, and moon. Glycerin holds the flake. A collar seats the dome.

A sphere on a turned plinth, not a dancer. Not neon tubing. No sticker edge. No egg. Not a shadow puppet. Not a fold. The globe stays seated on one envelope. The weather is the flurry. One shared clock.

Minting at $0.25 on Robinhood Chain (chain ID 4663). Gas is ETH.
```

## Listing images

No type on the marketplace images.

| Use | File | Size |
|---|---|---|
| Logo | `public/brand/logo-nivora.png` | 512×512, 1:1 |
| Featured | `public/brand/featured-nivora.jpg` | 1200×800, 3:2 |
| OpenSea banner | `public/brand/banner-nivora-opensea.jpg` | 2800×700, 4:1 |
| Collection GIF | `public/brand/collection-nivora.gif` | 1000×1000, 12-frame loop |
| Site hero (not the OpenSea banner) | `public/brand/banner-nivora.png` | 1500×560 |

## Drop upload

1. In OpenSea Studio, create a Drop on Robinhood Chain (chain ID 4663).
2. Upload every file in `gifs/` (`1.gif`–`16.gif`).
3. Upload `NIVORA-opensea-drop.csv` (or `opensea-metadata.csv`). The CSV uses OpenSea Studio headers: `tokenID`, `name`, `description`, `file_name`, and `attributes[Trait]`.
4. Set mint price to $0.25.
5. Preview the loops, then publish.

OpenSea Drops play GIF, not APNG. Studio trait layers stay in `public/nivora-traits/` and are not the upload pack.
