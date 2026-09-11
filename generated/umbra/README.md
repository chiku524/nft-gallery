# Umbra OpenSea kit

8,888 flattened shadow-puppet loops at 512×512, 12 frames, 90ms.

## Collection fields

- Name: `Umbra`
- Symbol: `UMBR`
- Token name: `Shade #{id}`
- Category: PFPs
- Chain: Robinhood Chain (`4663`)
- Supply: `8888`
- Mint: free (`0 ETH`)
- Creator fee: `5%` (set your wallet — `public/metadata/umbra.json` still has a zero address)

## Paste this as the collection description

Same file: `public/metadata/umbra-description.txt`

```
Umbra.

An 8,888-piece collection of looping shadow-puppet PFP GIFs on Robinhood Chain. Each shade is stacked from seven plates — cloth, ember, cast, hinge, cutwork, leaf, and soot — then flattened onto one 12-frame GIF. Eight dancing casts: clown, knight, bride, ogre, sage, harper, bird, and demon. Hinges swing the step. Cutwork lets the lamp through. Gold leaf rides the hide.

Leather on a woven screen. Not risograph blots. Not origami facets. Not an engraved bust. The cast stays seated in one envelope. The dance is in the joints. One shared clock.

Minting free on Robinhood Chain (chain ID 4663). Gas is ETH.
```

## Listing images

No type on the marketplace images.

| Use | File | Size |
|---|---|---|
| Logo | `public/brand/logo-umbra.png` | 512×512, 1:1 |
| Featured | `public/brand/featured-umbra.jpg` | 1200×800, 3:2 |
| OpenSea banner | `public/brand/banner-umbra-opensea.jpg` | 2800×700, 4:1 |
| Collection GIF | `public/brand/collection-umbra.gif` | 1000×1000, 12-frame loop |
| Site hero (not the OpenSea banner) | `public/brand/banner-umbra.png` | 1500×560 |

## Drop upload

1. In OpenSea Studio, create a Drop on Robinhood Chain (chain ID 4663).
2. Upload every file in `gifs/` (`1.gif`–`8888.gif`).
3. Upload `UMBRA-opensea-drop.csv` (or `opensea-metadata.csv`). The CSV uses OpenSea Studio headers: `tokenID`, `name`, `description`, `file_name`, and `attributes[Trait]`.
4. Set mint price to free.
5. Preview the loops, then publish.

OpenSea Drops play GIF, not APNG. Studio trait layers stay in `public/umbra-traits/` and are not the upload pack.
