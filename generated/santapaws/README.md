# Santa Paws OpenSea kit

Deterministic metadata for all 7,777 tokens. 7,777 flattened chibi-cat loops baked at 512×512, 12 frames, 90ms.

## Collection fields

- Name: `Santa Paws`
- Symbol: `PAWS`
- Category: PFPs
- Chain: Base (`8453`)
- Supply: `7777`
- Creator fee: `5%` (set your wallet — `public/metadata/santapaws.json` still has a zero address)

## Paste this as the collection description

Same file: `public/metadata/santapaws-description.txt`

```
Santa Paws is always in the mood of giving.

A 7,777-piece collection of looping chibi-cat PFP GIFs on Base. Each Santa Paw is stacked from six layers — yard, glow, pelt, mug, hat, and gear — then flattened onto one 12-frame GIF. Snowy nights and cookie kitchens behind them. Santa hats and cocoa on top. Ears twitch. Eyes blink. Soft bob.

Kawaii bust-crop cats with thick outlines, flat cel fills, and a Christmas wardrobe. One shared clock.

Minting on Base (chain ID 8453). Gas is ETH.
```

## Listing images

No type on the marketplace images.

| Use | File | Size |
|---|---|---|
| Logo | `public/brand/logo-santapaws.png` | 512×512, 1:1 |
| Featured | `public/brand/featured-santapaws.jpg` | 1200×800, 3:2 |
| OpenSea banner | `public/brand/banner-santapaws-opensea.jpg` | 2800×700, 4:1 |
| Collection GIF | `public/brand/collection-santapaws.gif` | 1000×1000, 12-frame loop |
| Site hero (not the OpenSea banner) | `public/brand/banner-santapaws.png` | 1500×560 |

## Generate / bake

```bash
python3 scripts/build_santapaws.py
python3 scripts/generate_santapaws.py        # full metadata + 16 preview GIFs
python3 scripts/generate_santapaws.py --all  # full 7,777 GIFs
python3 scripts/gif_bake.py --santapaws --all
```

## Drop upload

1. In OpenSea Studio, create a Drop on Base (chain ID 8453).
2. Upload every file in `gifs/` (`1.gif`–`7777.gif`).
3. Upload `SANTAPAWS-opensea-drop.csv` (or `opensea-metadata.csv`). The CSV uses OpenSea Studio headers: `tokenID`, `name`, `description`, `file_name`, and `attributes[Trait]`.
4. Preview the loops, then publish.

OpenSea Drops play GIF, not APNG. Studio trait layers stay in `public/santapaws-traits/` and are not the upload pack.
