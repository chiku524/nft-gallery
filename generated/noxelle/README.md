# Noxelle OpenSea kit

10,000 flattened neon-tube loops at 512×512, 12 frames, 90ms.

## Collection fields

- Name: `Noxelle`
- Symbol: `NOXL`
- Token name: `Tube #{id}`
- Category: PFPs
- Chain: Robinhood Chain (`4663`)
- Supply: `10000`
- Mint: `$0.25` (about `0.0001` ETH at listing; set the live ETH amount in OpenSea)
- Creator fee: `5%` (set your wallet — `public/metadata/noxelle.json` still has a zero address)

## Paste this as the collection description

Same file: `public/metadata/noxelle-description.txt`

```
Noxelle.

A 10,000-piece collection of looping neon-tube PFP GIFs on Robinhood Chain. Each sign is stacked from seven plates — wall, spill, gas, bend, clip, badge, and mote — then flattened onto one 12-frame GIF. Eight bends: sway, kick, wave, hop, point, dip, spin, and split. Argon, neon, krypton, mercury. Clips hold the glass. Spill stains the club wall.

Bent tubing, not a filled body. No sticker edge. No egg. Not a shadow puppet. Not a musical note. The dancer stays seated on one envelope. The dance is the bend. One shared clock.

Minting at $0.25 on Robinhood Chain (chain ID 4663). Gas is ETH.
```

## Listing images

No type on the marketplace images.

| Use | File | Size |
|---|---|---|
| Logo | `public/brand/logo-noxelle.png` | 512×512, 1:1 |
| Featured | `public/brand/featured-noxelle.jpg` | 1200×800, 3:2 |
| OpenSea banner | `public/brand/banner-noxelle-opensea.jpg` | 2800×700, 4:1 |
| Collection GIF | `public/brand/collection-noxelle.gif` | 1000×1000, 12-frame loop |
| Site hero (not the OpenSea banner) | `public/brand/banner-noxelle.png` | 1500×560 |

## Drop upload

1. In OpenSea Studio, create a Drop on Robinhood Chain (chain ID 4663).
2. Upload every file in `gifs/` (`1.gif`–`10000.gif`).
3. Upload `NOXELLE-opensea-drop.csv` (or `opensea-metadata.csv`). The CSV uses OpenSea Studio headers: `tokenID`, `name`, `description`, `file_name`, and `attributes[Trait]`.
4. Set mint price to $0.25.
5. Preview the loops, then publish.

OpenSea Drops play GIF, not APNG. Studio trait layers stay in `public/noxelle-traits/` and are not the upload pack.
