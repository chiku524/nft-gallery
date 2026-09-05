# Risota OpenSea kit

16 flattened risograph loops at 512×512, 12 frames, 90ms (sample pack — bake all 8,888 with `--all`).

## Collection fields

- Name: `Risota`
- Symbol: `RISO`
- Token name: `Print #{id}`
- Category: PFPs
- Chain: Robinhood Chain (`4663`)
- Supply: `8888`
- Creator fee: `5%` (set your wallet — `public/metadata/risota.json` still has a zero address)

## Paste this as the collection description

Same file: `public/metadata/risota-description.txt`

```
Risota.

An 8,888-piece collection of looping risograph PFP GIFs on Robinhood Chain. Each print is stacked from seven plates — stock, screen, figure, pass, knockout, slug, and mark — then flattened onto one 12-frame GIF. Eight dancers, each its own spot ink: kick, twirl, pop, sway, hop, glide, stomp, and reach. A second plate slides out of register. Halftone hangs on the sheet. Faces knock through as a dark drum.

Soy ink on uncoated paper. Fat blots, not outlines. No sticker edge. No egg body. The dancer stays seated on one envelope. One shared clock.

Minting on Robinhood Chain (chain ID 4663). Gas is ETH.
```

## Listing images

No type on the marketplace images.

| Use | File | Size |
|---|---|---|
| Logo | `public/brand/logo-risota.png` | 512×512, 1:1 |
| Featured | `public/brand/featured-risota.jpg` | 1200×800, 3:2 |
| OpenSea banner | `public/brand/banner-risota-opensea.jpg` | 2800×700, 4:1 |
| Collection GIF | `public/brand/collection-risota.gif` | 1000×1000, 12-frame loop |
| Site hero (not the OpenSea banner) | `public/brand/banner-risota.png` | 1500×560 |

## Drop upload

1. In OpenSea Studio, create a Drop on Robinhood Chain (chain ID 4663).
2. Upload every file in `gifs/` (`1.gif`–`16.gif`).
3. Upload `RISOTA-opensea-drop.csv` (or `opensea-metadata.csv`). The CSV uses OpenSea Studio headers: `tokenID`, `name`, `description`, `file_name`, and `attributes[Trait]`.
4. Preview the loops, then publish.

OpenSea Drops play GIF, not APNG. Studio trait layers stay in `public/risota-traits/` and are not the upload pack.
