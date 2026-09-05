# Perfin OpenSea kit

16 flattened engraved-stamp loops at 512×512, 12 frames, 90ms (sample pack — bake all 8,888 with `--all`).

## Collection fields

- Name: `Perfin`
- Symbol: `PRFN`
- Token name: `Perfin #{id}`
- Category: PFPs
- Chain: Robinhood Chain (`4663`)
- Supply: `8888`
- Mint: free (`0 ETH`)
- Creator fee: `5%` (set your wallet — `public/metadata/perfin.json` still has a zero address)

## Paste this as the collection description

Same file: `public/metadata/perfin-description.txt`

```
Perfin.

An 8,888-piece collection of looping engraved postage-stamp PFP GIFs on Robinhood Chain. Each frank is stacked from seven plates — wove, guilloche, bust, surcharge, aspect, device, and cancel — then flattened onto one 12-frame GIF. Eight busts, each its own stamp ink: pilot, keeper, clerk, captain, botanist, mapper, signal, and warden. Guilloche turns behind the vignette. A cancellation walks the face.

Intaglio lines on wove paper. Perforated rectangle. No charcoal outline. No sticker cutout. No dancing blot. The bust stays seated. One shared clock.

Minting free on Robinhood Chain (chain ID 4663). Gas is ETH.
```

## Listing images

No type on the marketplace images.

| Use | File | Size |
|---|---|---|
| Logo | `public/brand/logo-perfin.png` | 512×512, 1:1 |
| Featured | `public/brand/featured-perfin.jpg` | 1200×800, 3:2 |
| OpenSea banner | `public/brand/banner-perfin-opensea.jpg` | 2800×700, 4:1 |
| Collection GIF | `public/brand/collection-perfin.gif` | 1000×1000, 12-frame loop |
| Site hero (not the OpenSea banner) | `public/brand/banner-perfin.png` | 1500×560 |

## Drop upload

1. In OpenSea Studio, create a Drop on Robinhood Chain (chain ID 4663).
2. Upload every file in `gifs/` (`1.gif`–`16.gif`).
3. Upload `PERFIN-opensea-drop.csv` (or `opensea-metadata.csv`). The CSV uses OpenSea Studio headers: `tokenID`, `name`, `description`, `file_name`, and `attributes[Trait]`.
4. Set mint price to free.
5. Preview the loops, then publish.

OpenSea Drops play GIF, not APNG. Studio trait layers stay in `public/perfin-traits/` and are not the upload pack.
