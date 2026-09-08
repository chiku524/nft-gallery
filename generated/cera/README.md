# Cera OpenSea kit

16 flattened lava-lamp loops at 512×512, 12 frames, 90ms (sample pack — bake all 10,000 with `--all`).

## Collection fields

- Name: `Cera`
- Symbol: `CERA`
- Token name: `Lamp #{id}`
- Category: PFPs
- Chain: Robinhood Chain (`4663`)
- Supply: `10000`
- Mint: `$0.25` (about `0.0001` ETH at listing; set the live ETH amount in OpenSea)
- Creator fee: `5%` (set your wallet — `public/metadata/cera.json` still has a zero address)

## Paste this as the collection description

Same file: `public/metadata/cera-description.txt`

```
Cera.

A 10,000-piece collection of looping lava-lamp PFP GIFs on Robinhood Chain. Each lamp is stacked from seven plates — sill, socket, flask, serum, melt, coil, and lid — then flattened onto one 12-frame GIF. Eight sockets: rocket, saucer, cone, cube, mushroom, chrome, walnut, and ceramic. The glass holds oil. The wax is the loop.

A paraffin lamp on a nightstand, not a matchbook. Not a tin toy. Not a snow globe. Not neon tubing. No sticker edge. No egg. Not a shadow puppet. Not a fold. The flask stays seated on one envelope. The melt is the wax. One shared clock.

Minting at $0.25 on Robinhood Chain (chain ID 4663). Gas is ETH.
```

## Listing images

No type on the marketplace images.

| Use | File | Size |
|---|---|---|
| Logo | `public/brand/logo-cera.png` | 512×512, 1:1 |
| Featured | `public/brand/featured-cera.jpg` | 1200×800, 3:2 |
| OpenSea banner | `public/brand/banner-cera-opensea.jpg` | 2800×700, 4:1 |
| Collection GIF | `public/brand/collection-cera.gif` | 1000×1000, 12-frame loop |
| Site hero (not the OpenSea banner) | `public/brand/banner-cera.png` | 1500×560 |

## Drop upload

1. In OpenSea Studio, create a Drop on Robinhood Chain (chain ID 4663).
2. Upload every file in `gifs/` (`1.gif`–`16.gif`).
3. Upload `CERA-opensea-drop.csv` (or `opensea-metadata.csv`). The CSV uses OpenSea Studio headers: `tokenID`, `name`, `description`, `file_name`, and `attributes[Trait]`.
4. Set mint price to $0.25.
5. Preview the loops, then publish.

OpenSea Drops play GIF, not APNG. Studio trait layers stay in `public/cera-traits/` and are not the upload pack.
