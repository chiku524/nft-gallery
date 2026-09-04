# Groovy Nation OpenSea kit

16 flattened musical-note loops at 512×512, 12 frames, 90ms (sample pack — bake all 8,888 with `--all`).

## Collection fields

- Name: `Groovy Nation`
- Symbol: `GROOVY`
- Category: PFPs
- Chain: Robinhood Chain (`4663`)
- Supply: `8888`
- Creator fee: `5%` (set your wallet — `public/metadata/groovy.json` still has a zero address)

## Paste this as the collection description

Same file: `public/metadata/groovy-description.txt`

```
Welcome to Groovy Nation.

An 8,888-piece collection of looping musical-note PFP GIFs on Robinhood Chain. Each citizen is stacked from six layers — venue, note, expression, topper, cable, and riff — then flattened onto one 12-frame GIF. The notehead is the face. A black stem goes up. Flags and beams sit at the top. Stick arms and legs dance on the beat.

Four notes only: quarter, eighth, whole, and beamed. Bold outline, flat fill, cartoon notation. Shades sit on the head. Chains hang on the chin. Riffs float beside the beat. One shared clock.

Minting on Robinhood Chain (chain ID 4663). Gas is ETH.
```

## Listing images

No type on the marketplace images.

| Use | File | Size |
|---|---|---|
| Logo | `public/brand/logo-groovy.png` | 512×512, 1:1 |
| Featured | `public/brand/featured-groovy.jpg` | 1200×800, 3:2 |
| OpenSea banner | `public/brand/banner-groovy-opensea.jpg` | 2800×700, 4:1 |
| Collection GIF | `public/brand/collection-groovy.gif` | 1000×1000, 12-frame loop |
| Site hero (not the OpenSea banner) | `public/brand/banner-groovy.png` | 1500×560 |

## Drop upload

1. In OpenSea Studio, create a Drop on Robinhood Chain (chain ID 4663).
2. Upload every file in `gifs/` (`1.gif`–`16.gif`).
3. Upload `GROOVY-opensea-drop.csv` (or `opensea-metadata.csv`). The CSV uses OpenSea Studio headers: `tokenID`, `name`, `description`, `file_name`, and `attributes[Trait]`.
4. Preview the loops, then publish.

OpenSea Drops play GIF, not APNG. Studio trait layers stay in `public/groovy-traits/` and are not the upload pack.
