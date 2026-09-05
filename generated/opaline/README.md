# Opaline OpenSea kit

16 flattened smoked-glass loops at 512×512, 12 frames, 90ms (sample pack — bake all 10,000 with `--all`).

## Collection fields

- Name: `Opaline`
- Symbol: `OPAL`
- Category: PFPs
- Chain: Base (`8453`)
- Supply: `10000`
- Creator fee: `5%` (set your wallet — `public/metadata/opaline.json` still has a zero address)

## Paste this as the collection description

Same file: `public/metadata/opaline-description.txt`

```
Opaline.

A 10,000-piece collection of looping smoked-glass PFP GIFs on Base. Each portrait is stacked from six layers — atelier, cast, sheen, regard, crest, and clasp — then flattened onto one 12-frame GIF. Eight beasts share one seated face: stag, serpent, moth, beetle, ram, ibis, wyrm, and mantis. Light walks the facets. Film shifts hue. Inclusions dim.

Crystal creatures. Seven films, including bare glass. No charcoal outline. No sticker cutout. The beast stays seated. One shared clock.

Minting on Base (chain ID 8453). Gas is ETH.
```

## Listing images

No type on the marketplace images.

| Use | File | Size |
|---|---|---|
| Logo | `public/brand/logo-opaline.png` | 512×512, 1:1 |
| Featured | `public/brand/featured-opaline.jpg` | 1200×800, 3:2 |
| OpenSea banner | `public/brand/banner-opaline-opensea.jpg` | 2800×700, 4:1 |
| Collection GIF | `public/brand/collection-opaline.gif` | 1000×1000, 12-frame loop |
| Site hero (not the OpenSea banner) | `public/brand/banner-opaline.png` | 1500×560 |

## Drop upload

1. In OpenSea Studio, create a Drop on Base (chain ID 8453).
2. Upload every file in `gifs/` (`1.gif`–`16.gif`).
3. Upload `OPALINE-opensea-drop.csv` (or `opensea-metadata.csv`). The CSV uses OpenSea Studio headers: `tokenID`, `name`, `description`, `file_name`, and `attributes[Trait]`.
4. Preview the loops, then publish.

OpenSea Drops play GIF, not APNG. Studio trait layers stay in `public/opaline-traits/` and are not the upload pack.
