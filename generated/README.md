# Loopkins OpenSea kit

10,000 flattened looping PFP creatures at 256×256, 12 frames, 80ms.

## Collection fields

- Name: `Loopkins`
- Symbol: `LOOP`
- Category: PFPs
- Chain: Robinhood Chain (`4663`)
- Supply: `10000`
- Creator fee: `5%` (set your wallet — `public/metadata/collection.json` still has a zero address)

## Paste this as the collection description

Same file: `public/metadata/loopkins-description.txt`

```
Loopkins never sit still.

A 10,000-piece collection of looping PFP creatures on Robinhood Chain. Each Loopkin is stacked from six layers — sky, aura, body, face, wear, and charm — then flattened onto one 12-frame GIF. Skies pulse. Auras breathe. Faces blink. Charms orbit.

One shared clock. The studio stacks the layers live. OpenSea gets the flattened loop.

Minting on Robinhood Chain (chain ID 4663). Gas is ETH.
```

## Listing images

No type on the marketplace images.

| Use | File | Size |
|---|---|---|
| Logo | `public/brand/logo-loopkins.png` | 512×512, 1:1 |
| Featured | `public/brand/featured-loopkins.jpg` | 1200×800, 3:2 |
| OpenSea banner | `public/brand/banner-loopkins-opensea.jpg` | 2800×700, 4:1 |
| Collection GIF | `public/brand/collection-loopkins.gif` | 1000×1000, 12-frame loop |
| Site hero (not the OpenSea banner) | `public/brand/banner-loopkins.png` | 1500×560 |

## Drop upload

1. In OpenSea Studio, create a Drop on Robinhood Chain (chain ID 4663).
2. Upload every file in `gifs/` (`1.gif`–`10000.gif`).
3. Upload `LOOPKINS-opensea-drop.csv` (or `opensea-metadata.csv`). The CSV uses OpenSea Studio headers: `tokenID`, `name`, `description`, `file_name`, and `attributes[Trait]`.
4. Preview the loops, then publish.

OpenSea Drops play GIF, not APNG. Studio trait layers stay in `public/traits/` and are not the upload pack. Drop files are 256×256 so the 10,000 pack stays under the cap.
