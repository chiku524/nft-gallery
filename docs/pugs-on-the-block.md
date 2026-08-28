# Pugs On The Block

Neighborhood pugs peeking over the stoop. A **10,000-piece** PFP collection of layered chibi pugs, built to mint on **Robinhood Chain** (chain ID `4663`) and list on **OpenSea**.

This collection lives inside **NFT Gallery** at `/pugs-on-the-block`.

OpenSea does **not** generate collections from trait layers. For a Drop you upload finished images (max 10,000) plus a CSV. This repo already composited those files.

## What’s in the drop

- Trait art at `public/traits/` — background, base, block, hat, body, accessory
- 10,000 shuffled PFPs at `generated/images/` plus `generated/opensea-metadata.csv`
- Eight hand-dressed samples in `public/gallery/`
- Collection logo and banner in `public/brand/`
- Trait studio at `/pugs-on-the-block/studio`
- `contracts/PugsOnTheBlock.sol` — ERC-721 with a 10,000 supply cap

## Generate the 10,000

```bash
python3 scripts/fit_traits_1024.py   # optional: re-place hats/clothes/toys on the 1024 canvas
python3 scripts/generate_collection.py
```

Requires Python 3 with Pillow. Output lands in `generated/`. See `generated/README.md` for the OpenSea Drop upload steps.

## Trait stack

Draw order, back to front:

1. Background
2. Block (the ledge)
3. Base pug
4. Body (bandana, collar, hoodie, chain)
5. Hat
6. Accessory (shades, monocle, or a treat on the ledge)

Hats, clothes, and stoop props are painted onto the same 1024×1024 canvas as the pug, then stacked 1:1. Tokens 1–8 of the generated drop are the eight gallery paintings themselves, so those looks match the site gallery exactly.

## Robinhood Chain + OpenSea

| | |
| --- | --- |
| Network | Robinhood Chain |
| Chain ID | 4663 (`0x1237`) |
| RPC | `https://rpc.mainnet.chain.robinhood.com` |
| Explorer | https://robinhoodchain.blockscout.com |
| Gas token | ETH |
| Marketplace | OpenSea Drop (bulk images + CSV) |
