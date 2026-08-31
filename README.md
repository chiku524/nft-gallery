# NFT Gallery

A house of NFT collections. Each drop is its own sub-project — studio, traits, and launch path included.

**Loopkins** is the first collection on the wall: 10,000 looping PFP creatures built from layered APNG traits, for OpenSea on Robinhood Chain (chain ID `4663`).

**Afterimages** is the second: a 50-piece OpenSea drop of unique 1:1 APNG paintings. No trait stack — each token is a finished loop.

**Inklings** is the third: 5,555 cartoon-squid PFP GIFs, for OpenSea on Ink (chain ID `57073`).

## What’s in this repo

| Path | What it is |
| --- | --- |
| `/` | NFT Gallery hub — every collection on the wall |
| `/loopkins` | Loopkins drop, trait loops, gallery, OpenSea notes |
| `/afterimages` | Afterimages 1:1 drop, viewing room, OpenSea notes |
| `/inklings` | Inklings drop, trait loops, gallery, OpenSea notes |
| `/studio` | Live APNG layer mixer (Loopkins) |
| `/inklings/studio` | Live ink-wash mixer (Inklings) |
| `public/traits/` | Loopkins APNG layers (sky, aura, body, face, wear, charm) |
| `public/afterimages/` | Afterimages 1:1 APNG paintings |
| `public/inklings-traits/` | Inklings APNG layers (paper, bloom, visage, gaze, mark, adorn) |
| `generated/` | Flattened Loopkins APNGs, OpenSea GIFs + CSV |
| `generated/afterimages/` | Afterimages OpenSea GIF pack |
| `generated/inklings/` | Inklings OpenSea GIF pack |
| `contracts/Loopkins.sol` | ERC-721 with a 10,000 supply cap |
| `contracts/Afterimages.sol` | ERC-721 that mints a chosen 1:1 (IDs 1–12) |
| `contracts/Inklings.sol` | ERC-721 with a 5,555 supply cap |

## Run the site

```bash
npm install
npm run dev
```

The app listens on [http://127.0.0.1:43147](http://127.0.0.1:43147).

- Gallery home: `/`
- Loopkins: `/loopkins`
- Afterimages: `/afterimages`
- Inklings: `/inklings`
- Trait studio: `/studio` (Loopkins) or `/inklings/studio`

## Generate collections

```bash
python3 scripts/build_loopkins.py
python3 scripts/generate_collection.py
python3 scripts/build_afterimages.py
python3 scripts/build_inklings.py
python3 scripts/generate_inklings.py
python3 scripts/gif_bake.py --afterimages
python3 scripts/gif_bake.py --loopkins --all
python3 scripts/gif_bake.py --inklings --all
```

Requires Python 3 with Pillow and NumPy. See `docs/loopkins.md`, `docs/afterimages.md`, and `docs/inklings.md` for OpenSea Drop upload steps.

## Deploy

This is a single Next.js app (one Vercel project). Point Vercel at the GitHub repo `nft-gallery`, framework preset Next.js, root directory `.`.

## License

Art and site code in this repository are for the collections on the wall. Swap the zero-address fee recipient in `public/metadata/collection.json`, `public/metadata/afterimages.json`, and `public/metadata/inklings.json` before you list.
