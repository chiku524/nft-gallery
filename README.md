# NFT Gallery

A house of NFT collections. Each drop is its own sub-project — studio, traits, and launch path included.

**Pugs On The Block** is the first collection on the wall: 10,000 chibi pug PFPs for OpenSea on Robinhood Chain (chain ID `4663`).

## What’s in this repo

| Path | What it is |
| --- | --- |
| `/` | NFT Gallery hub — every collection on the wall |
| `/pugs-on-the-block` | Pugs On The Block drop, studio, traits, gallery, OpenSea notes |
| `public/traits/` | POTB trait layers (background, base, block, hat, body, accessory) |
| `generated/` | 10,000 shuffled POTB PFPs + OpenSea CSV |
| `contracts/PugsOnTheBlock.sol` | ERC-721 with a 10,000 supply cap |

More collections land as sibling routes (same pattern as `/pugs-on-the-block`) and get a card on the hub.

## Run the site

```bash
npm install
npm run dev
```

The app listens on [http://127.0.0.1:43147](http://127.0.0.1:43147).

- Gallery home: `/`
- Pugs On The Block: `/pugs-on-the-block`
- Trait studio: `/pugs-on-the-block/studio`

## Generate the Pugs On The Block drop

```bash
python3 scripts/fit_traits_1024.py
python3 scripts/generate_collection.py
```

Requires Python 3 with Pillow. Output lands in `generated/`. See `generated/README.md` and `docs/pugs-on-the-block.md` for OpenSea Drop upload steps.

## Deploy

This is a single Next.js app (one Vercel project). Point Vercel at the GitHub repo `nft-gallery`, framework preset Next.js, root directory `.`.

## License

Art and site code in this repository are for the collections on the wall. Swap the zero-address fee recipient in `public/metadata/collection.json` before you list Pugs On The Block.
