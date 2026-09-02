# Hoodkins OpenSea kit

10,000 flattened chibi-raccoon loops at 512×512, 12 frames, 80ms. Pack is **8.81 GiB** — under OpenSea's 10 GiB / 10,000-file Drop cap.

## Collection fields

- Name: `Hoodkins`
- Symbol: `HOOD`
- Category: PFPs
- Chain: Robinhood Chain (`4663`)
- Supply: `10000`
- Creator fee: `5%` (set your wallet — `public/metadata/hoodkins.json` still has a zero address)

## Paste this as the collection description

Same file: `public/metadata/hoodkins-description.txt`

```
Hoodkins never sit still.

A 10,000-piece collection of looping chibi-raccoon PFP GIFs on Robinhood Chain. Each Hoodkin is stacked from six layers — pad, glow, pelt, fit, mug, and gear — then flattened onto one 12-frame GIF. Ledger desks behind them. Hoodies and beanies on top. Bandit masks. Ears twitch. Eyes blink. Soft bob.

Kawaii bust-crop raccoons with thick outlines, flat cel fills, and streetwear. One shared clock.

Minting on Robinhood Chain (chain ID 4663). Gas is ETH.
```

## Listing images

No type on the marketplace images.

| Use | File | Size |
|---|---|---|
| Logo | `public/brand/logo-hoodkins.png` | 512×512, 1:1 |
| Featured | `public/brand/featured-hoodkins.jpg` | 1200×800, 3:2 |
| OpenSea banner | `public/brand/banner-hoodkins-opensea.jpg` | 2800×700, 4:1 |
| Collection GIF | `public/brand/collection-hoodkins.gif` | 1000×1000, 12-frame loop |
| Site hero (not the OpenSea banner) | `public/brand/banner-hoodkins.png` | 1500×560 |

## Drop upload

1. In OpenSea Studio, create a Drop on Robinhood Chain (chain ID 4663).
2. Upload every file in `gifs/` (`1.gif`–`10000.gif`).
3. Upload `HOODKINS-opensea-drop.csv` (or `opensea-metadata.csv`). The CSV uses OpenSea Studio headers: `tokenID`, `name`, `description`, `file_name`, and `attributes[Trait]`.
4. Preview the loops, then publish.

OpenSea Drops play GIF, not APNG. Studio trait layers stay in `public/hoodkins-traits/` and are not the upload pack.
