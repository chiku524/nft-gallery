# Pugs On The Block

Neighborhood pugs peeking over the stoop. A **10,000-piece** PFP collection of layered chibi pugs, built to mint on **Robinhood Chain** (chain ID `4663`) and list on **OpenSea**.

OpenSea does **not** generate collections from trait layers. For a Drop you upload finished images (max 10,000) plus a CSV. This repo already composited those files.

## What’s in this repo

- Trait art at `public/traits/` — background, base, block, hat, body, accessory
- 10,000 shuffled PFPs at `generated/images/` plus `generated/opensea-metadata.csv`
- Eight hand-dressed samples in `public/gallery/`
- Collection logo and banner in `public/brand/`
- Trait studio at `/studio`
- `contracts/PugsOnTheBlock.sol` — ERC-721 with a 10,000 supply cap

## Run the site

```bash
npm install
npm run dev
```

The app listens on [http://127.0.0.1:43147](http://127.0.0.1:43147).

## Generate the 10,000

```bash
python3 scripts/generate_collection.py
```

Requires Python 3 with Pillow. Output lands in `generated/`. See `generated/README.md` for the OpenSea Drop upload steps.

## Trait stack

Draw order, back to front: background → base pug → block (ledge) → body → hat → accessory.

## Robinhood Chain + OpenSea

| | |
| --- | --- |
| Network | Robinhood Chain |
| Chain ID | 4663 (`0x1237`) |
| RPC | `https://rpc.mainnet.chain.robinhood.com` |
| Explorer | https://robinhoodchain.blockscout.com |
| Gas token | ETH |
| Marketplace | OpenSea Drop (bulk images + CSV) |

## License

Art and site code in this repository are for the Pugs On The Block drop. Swap the zero-address fee recipient in `public/metadata/collection.json` before you list.
