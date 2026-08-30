# NFT Gallery

A house of NFT collections. Each drop is its own sub-project — studio, traits, and launch path included.

**Loopkins** is the first collection on the wall: 10,000 looping PFP creatures built from layered APNG traits, for OpenSea on Robinhood Chain (chain ID `4663`).

## What’s in this repo

| Path | What it is |
| --- | --- |
| `/` | NFT Gallery hub — every collection on the wall |
| `/loopkins` | Loopkins drop, trait loops, gallery, OpenSea notes |
| `/studio` | Live APNG layer mixer |
| `public/traits/` | Loopkins APNG layers (sky, aura, body, face, wear, charm) |
| `generated/` | Flattened Loopkins APNGs + OpenSea CSV |
| `contracts/Loopkins.sol` | ERC-721 with a 10,000 supply cap |

## Run the site

```bash
npm install
npm run dev
```

The app listens on [http://127.0.0.1:43147](http://127.0.0.1:43147).

- Gallery home: `/`
- Loopkins: `/loopkins`
- Trait studio: `/studio`

## Generate Loopkins

```bash
python3 scripts/build_loopkins.py
python3 scripts/generate_collection.py
```

Requires Python 3 with Pillow and NumPy. Output lands in `generated/`. See `docs/loopkins.md` for OpenSea Drop upload steps.

## Deploy

This is a single Next.js app (one Vercel project). Point Vercel at the GitHub repo `nft-gallery`, framework preset Next.js, root directory `.`.

## License

Art and site code in this repository are for the collections on the wall. Swap the zero-address fee recipient in `public/metadata/collection.json` before you list Loopkins.
