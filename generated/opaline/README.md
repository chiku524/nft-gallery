# Opaline OpenSea kit

5,555 flattened smoked-glass loops at 512×512, 12 frames, 90ms.

## Collection fields

- Name: `Opaline`
- Symbol: `OPAL`
- Category: PFPs
- Chain: Base (`8453`)
- Supply: `5555`
- Creator fee: `5%` (set your wallet — `public/metadata/opaline.json` still has a zero address)

## Paste this as the collection description

Same file: `public/metadata/opaline-description.txt`

```
Opaline.

A 5,555-piece collection of looping smoked-glass PFP GIFs on Base. Each portrait is stacked from seven layers — atelier, vapor, cast, sheen, regard, crest, and clasp — then flattened onto one 12-frame GIF. Eight saltwater fish, each its own glass: parrotfish, blue marlin, queen angelfish, lionfish, triggerfish, seahorse, green moray, and manta. Vapor hangs in the room. Light walks the facets. Film shifts hue. Inclusions dim.

Crystal reef fish. Seven films, including bare glass. No charcoal outline. No sticker cutout. The fish stays seated. One shared clock.

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
2. Upload every file in `gifs/` (`1.gif`–`5555.gif`).
3. Upload `OPALINE-opensea-drop.csv` (or `opensea-metadata.csv`). The CSV uses OpenSea Studio headers: `tokenID`, `name`, `description`, `file_name`, and `attributes[Trait]`.
4. Preview the loops, then publish.

OpenSea Drops play GIF, not APNG. Studio trait layers stay in `public/opaline-traits/` and are not the upload pack.
