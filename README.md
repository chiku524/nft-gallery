# NFT Gallery

A house of NFT collections. Each drop is its own sub-project — studio, traits, and launch path included.

**Loopkins** is the first collection on the wall: 10,000 looping PFP creatures built from layered APNG traits, for OpenSea on Robinhood Chain (chain ID `4663`).

**Afterimages** is the second: a 12-piece OpenSea drop of unique 1:1 APNG paintings. No trait stack — each token is a finished loop.

## What’s in this repo

| Path | What it is |
| --- | --- |
| `/` | NFT Gallery hub — every collection on the wall |
| `/loopkins` | Loopkins drop, trait loops, gallery, OpenSea notes |
| `/afterimages` | Afterimages 1:1 drop, viewing room, OpenSea notes |
| `/studio` | Live APNG layer mixer (Loopkins) |
| `public/traits/` | Loopkins APNG layers (sky, aura, body, face, wear, charm) |
| `public/afterimages/` | Afterimages 1:1 APNG paintings |
| `generated/` | Flattened Loopkins APNGs, OpenSea GIFs + CSV |
| `generated/afterimages/` | Afterimages OpenSea GIF pack |
| `contracts/Loopkins.sol` | ERC-721 with a 10,000 supply cap |
| `contracts/Afterimages.sol` | ERC-721 that mints a chosen 1:1 (IDs 1–12) |

## Run the site

```bash
npm install
npm run dev
```

The app listens on [http://127.0.0.1:43147](http://127.0.0.1:43147).

- Gallery home: `/`
- Loopkins: `/loopkins`
- Afterimages: `/afterimages`
- Trait studio: `/studio`

## Generate collections

```bash
python3 scripts/build_loopkins.py
python3 scripts/generate_collection.py
python3 scripts/build_afterimages.py
python3 scripts/gif_bake.py --afterimages
python3 scripts/gif_bake.py --loopkins --all
```

Requires Python 3 with Pillow and NumPy. See `docs/loopkins.md` and `docs/afterimages.md` for OpenSea Drop upload steps.

## Deploy

This is a single Next.js app (one Vercel project). Point Vercel at the GitHub repo `nft-gallery`, framework preset Next.js, root directory `.`.

## License

Art and site code in this repository are for the collections on the wall. Swap the zero-address fee recipient in `public/metadata/collection.json` and `public/metadata/afterimages.json` before you list.
