# Kamiori OpenSea kit

16 flattened origami loops at 512×512, 12 frames, 90ms (sample pack — bake all 8,888 with `--all`).

## Collection fields

- Name: `Kamiori`
- Symbol: `KMIO`
- Token name: `Fold #{id}`
- Category: PFPs
- Chain: Robinhood Chain (`4663`)
- Supply: `8888`
- Mint: free (`0 ETH`)
- Creator fee: `5%` (set your wallet — `public/metadata/kamiori.json` still has a zero address)

## Paste this as the collection description

Same file: `public/metadata/kamiori-description.txt`

```
Kamiori.

An 8,888-piece collection of looping origami PFP GIFs on Robinhood Chain. Each sheet is stacked from seven plates — pulp, fleck, fold, score, facet, seal, and draft — then flattened onto one 12-frame GIF. Eight folds, each its own washi dye: crane, frog, beetle, boat, hare, fan, kite, and lotus. A crease diagram sits on the paper. A draft lifts one corner.

Deckle washi. Angular facets. No engraved bust. No perforated stamp. No charcoal outline. No sticker cutout. The fold stays seated. One shared clock.

Minting free on Robinhood Chain (chain ID 4663). Gas is ETH.
```

## Listing images

No type on the marketplace images.

| Use | File | Size |
|---|---|---|
| Logo | `public/brand/logo-kamiori.png` | 512×512, 1:1 |
| Featured | `public/brand/featured-kamiori.jpg` | 1200×800, 3:2 |
| OpenSea banner | `public/brand/banner-kamiori-opensea.jpg` | 2800×700, 4:1 |
| Collection GIF | `public/brand/collection-kamiori.gif` | 1000×1000, 12-frame loop |
| Site hero (not the OpenSea banner) | `public/brand/banner-kamiori.png` | 1500×560 |

## Drop upload

1. In OpenSea Studio, create a Drop on Robinhood Chain (chain ID 4663).
2. Upload every file in `gifs/` (`1.gif`–`16.gif`).
3. Upload `KAMIORI-opensea-drop.csv` (or `opensea-metadata.csv`). The CSV uses OpenSea Studio headers: `tokenID`, `name`, `description`, `file_name`, and `attributes[Trait]`.
4. Set mint price to free.
5. Preview the loops, then publish.

OpenSea Drops play GIF, not APNG. Studio trait layers stay in `public/kamiori-traits/` and are not the upload pack.
