# NFT Gallery

A house of NFT collections. Each drop is its own sub-project — studio, traits, and launch path included.

**Loopkins** is the first collection on the wall: 10,000 looping PFP creatures built from layered APNG traits, for OpenSea on Robinhood Chain (chain ID `4663`).

**Afterimages** is the second: a 50-piece OpenSea drop of unique 1:1 APNG paintings. No trait stack — each token is a finished loop.

**Inklings** is the third: 5,555 cartoon-squid PFP GIFs, for OpenSea on Ink (chain ID `57073`).

**Party Pandas** is the fourth: 4,444 looping cartoon party-panda PFP GIFs with real panda markings, for OpenSea on Base (chain ID `8453`). Same 12-frame GIF clock as Loopkins.

**Wicklings** is the fifth: 8,888 looping paper-lantern PFP GIFs, for OpenSea on Arbitrum (chain ID `42161`). Same 12-frame GIF clock as Loopkins.

## What’s in this repo

| Path | What it is |
| --- | --- |
| `/` | NFT Gallery hub — every collection on the wall |
| `/loopkins` | Loopkins drop, trait loops, gallery, OpenSea notes |
| `/afterimages` | Afterimages 1:1 drop, viewing room, OpenSea notes |
| `/inklings` | Inklings drop, trait loops, gallery, OpenSea notes |
| `/party-pandas` | Party Pandas drop, trait loops, gallery, OpenSea notes |
| `/wicklings` | Wicklings drop, trait loops, gallery, OpenSea notes |
| `/studio` | Live APNG layer mixer (Loopkins) |
| `/inklings/studio` | Live ink-wash mixer (Inklings) |
| `/party-pandas/studio` | Live party-panda mixer (Party Pandas) |
| `/wicklings/studio` | Live paper-lantern mixer (Wicklings) |
| `public/traits/` | Loopkins APNG layers (sky, aura, body, face, wear, charm) |
| `public/afterimages/` | Afterimages 1:1 APNG paintings |
| `public/inklings-traits/` | Inklings APNG layers (paper, bloom, visage, gaze, mark, adorn) |
| `public/party-pandas-traits/` | Party Pandas APNG layers (venue, glow, panda, mood, fit, extra) |
| `public/wicklings-traits/` | Wicklings APNG layers (night, halo, vessel, wick, wrap, drift) |
| `generated/` | Flattened Loopkins APNGs, OpenSea GIFs + CSV |
| `generated/afterimages/` | Afterimages OpenSea GIF pack |
| `generated/inklings/` | Inklings OpenSea GIF pack |
| `generated/party-pandas/` | Party Pandas OpenSea GIF pack |
| `generated/wicklings/` | Wicklings OpenSea GIF pack |
| `contracts/Loopkins.sol` | ERC-721 with a 10,000 supply cap |
| `contracts/Afterimages.sol` | ERC-721 that mints a chosen 1:1 (IDs 1–12) |
| `contracts/Inklings.sol` | ERC-721 with a 5,555 supply cap |
| `contracts/PartyPandas.sol` | ERC-721 with a 4,444 supply cap |
| `contracts/Wicklings.sol` | ERC-721 with an 8,888 supply cap |

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
- Party Pandas: `/party-pandas`
- Wicklings: `/wicklings`
- Trait studio: `/studio` (Loopkins), `/inklings/studio`, `/party-pandas/studio`, or `/wicklings/studio`

## Generate collections

```bash
python3 scripts/build_loopkins.py
python3 scripts/generate_collection.py
python3 scripts/build_afterimages.py
python3 scripts/build_inklings.py
python3 scripts/generate_inklings.py
python3 scripts/build_party_pandas.py
python3 scripts/generate_party_pandas.py
python3 scripts/build_wicklings.py
python3 scripts/generate_wicklings.py
python3 scripts/gif_bake.py --afterimages
python3 scripts/gif_bake.py --loopkins --all
python3 scripts/gif_bake.py --inklings --all
python3 scripts/gif_bake.py --party-pandas --all
python3 scripts/gif_bake.py --wicklings --all
```

Requires Python 3 with Pillow and NumPy. See `docs/loopkins.md`, `docs/afterimages.md`, `docs/inklings.md`, `docs/party-pandas.md`, and `docs/wicklings.md` for OpenSea Drop upload steps.

## Deploy

This is a single Next.js app (one Vercel project). Point Vercel at the GitHub repo `nft-gallery`, framework preset Next.js, root directory `.`.

## License

Art and site code in this repository are for the collections on the wall. Swap the zero-address fee recipient in `public/metadata/collection.json`, `public/metadata/afterimages.json`, `public/metadata/inklings.json`, `public/metadata/party-pandas.json`, and `public/metadata/wicklings.json` before you list.
