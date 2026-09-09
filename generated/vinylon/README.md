# Vinylon OpenSea kit

16 flattened balloon-animal loops at 512×512, 12 frames, 90ms (sample pack — bake all 10,000 with `--all`).

## Collection fields

- Name: `Vinylon`
- Symbol: `VNYL`
- Token name: `Twist #{id}`
- Category: PFPs
- Chain: Robinhood Chain (`4663`)
- Supply: `10000`
- Mint: free (`0 ETH`)
- Creator fee: `5%` (set your wallet — `public/metadata/vinylon.json` still has a zero address)

## Paste this as the collection description

Same file: `public/metadata/vinylon-description.txt`

```
Vinylon.

A 10,000-piece collection of looping balloon-animal PFP GIFs on Robinhood Chain. Each twist is stacked from seven plates — booth, latex, twist, knot, valve, gleam, and confetti — then flattened onto one 12-frame GIF. Eight dancing twists: hound, hare, steed, swan, monkey, dino, poodle, and figure. Inflated tubes. Knots at the joints. The bob is the loop.

Latex in a booth. Not neon tubing. Not a leather puppet. Not soy-ink blots. The twist stays seated in one envelope. The dance is the squeeze. One shared clock.

Minting free on Robinhood Chain (chain ID 4663). Gas is ETH.
```

## Listing images

No type on the marketplace images.

| Use | File | Size |
|---|---|---|
| Logo | `public/brand/logo-vinylon.png` | 512×512, 1:1 |
| Featured | `public/brand/featured-vinylon.jpg` | 1200×800, 3:2 |
| OpenSea banner | `public/brand/banner-vinylon-opensea.jpg` | 2800×700, 4:1 |
| Collection GIF | `public/brand/collection-vinylon.gif` | 1000×1000, 12-frame loop |
| Site hero (not the OpenSea banner) | `public/brand/banner-vinylon.png` | 1500×560 |

## Drop upload

1. In OpenSea Studio, create a Drop on Robinhood Chain (chain ID 4663).
2. Upload every file in `gifs/` (`1.gif`–`16.gif`).
3. Upload `VNYL-opensea-drop.csv` (or `opensea-metadata.csv`).
4. Set mint price to free.
5. Preview the loops, then publish.

OpenSea Drops play GIF, not APNG. Studio trait layers stay in `public/vinylon-traits/` and are not the upload pack.
