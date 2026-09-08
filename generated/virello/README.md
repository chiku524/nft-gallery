# Virello OpenSea kit

16 flattened wind-up tin-toy loops at 512×512, 12 frames, 90ms (sample pack — bake all 10,000 with `--all`).

## Collection fields

- Name: `Virello`
- Symbol: `VIRL`
- Token name: `Toy #{id}`
- Category: PFPs
- Chain: Robinhood Chain (`4663`)
- Supply: `10000`
- Mint: `$0.25` (about `0.0001` ETH at listing; set the live ETH amount in OpenSea)
- Creator fee: `5%` (set your wallet — `public/metadata/virello.json` still has a zero address)

## Paste this as the collection description

Same file: `public/metadata/virello-description.txt`

```
Virello.

A 10,000-piece collection of looping wind-up tin-toy PFP GIFs on Robinhood Chain. Each toy is stacked from seven plates — bench, chassis, enamel, decal, key, spark, and wear — then flattened onto one 12-frame GIF. Eight chassis: robot, duck, racer, soldier, monkey, tank, copter, and frog. The print is lithographed. The key is the loop.

Stamped metal on a toy-shop bench, not a snow globe. Not neon tubing. No sticker edge. No egg. Not a shadow puppet. Not a fold. The toy stays seated on one envelope. The wind-up is the key. One shared clock.

Minting at $0.25 on Robinhood Chain (chain ID 4663). Gas is ETH.
```

## Listing images

No type on the marketplace images.

| Use | File | Size |
|---|---|---|
| Logo | `public/brand/logo-virello.png` | 512×512, 1:1 |
| Featured | `public/brand/featured-virello.jpg` | 1200×800, 3:2 |
| OpenSea banner | `public/brand/banner-virello-opensea.jpg` | 2800×700, 4:1 |
| Collection GIF | `public/brand/collection-virello.gif` | 1000×1000, 12-frame loop |
| Site hero (not the OpenSea banner) | `public/brand/banner-virello.png` | 1500×560 |

## Drop upload

1. In OpenSea Studio, create a Drop on Robinhood Chain (chain ID 4663).
2. Upload every file in `gifs/` (`1.gif`–`16.gif`).
3. Upload `VIRELLO-opensea-drop.csv` (or `opensea-metadata.csv`). The CSV uses OpenSea Studio headers: `tokenID`, `name`, `description`, `file_name`, and `attributes[Trait]`.
4. Set mint price to $0.25.
5. Preview the loops, then publish.

OpenSea Drops play GIF, not APNG. Studio trait layers stay in `public/virello-traits/` and are not the upload pack.
