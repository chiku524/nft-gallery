# Pugs On The Block

Neighborhood pugs peeking over the stoop. A **10,000-piece** PFP collection of layered chibi pugs, built to mint on **Robinhood Chain** (chain ID `4663`) and list on **OpenSea**.

This collection lives inside **NFT Gallery** at `/pugs-on-the-block`.

OpenSea does **not** generate collections from trait layers. For a Drop you upload finished images (max 10,000) plus a CSV. This repo already composited those files.

## What’s in the drop

- Trait art at `public/traits/` — painted PNG layers, already seated on the 1024 canvas
- 10,000 shuffled PFPs at `generated/images/` plus `generated/opensea-metadata.csv`
- Collection logo and banner in `public/brand/`
- Trait studio is now the empty gallery studio at `/studio`
- `contracts/PugsOnTheBlock.sol` — ERC-721 with a 10,000 supply cap

## Generate the 10,000

```bash
python3 scripts/build_traits.py
python3 scripts/generate_collection.py
```

Requires Python 3 with Pillow and NumPy. `build_traits.py` seats the painted PNG sources. Output lands in `generated/`. See `generated/README.md` for the OpenSea Drop upload steps.

## Trait stack

Every layer is already seated on the 1024×1024 canvas. Studio and the generator only stack:

1. Background
2. Base pug
3. Face accessory (sunglasses, monocle)
4. Body (bandana, collar, hoodie, gold chain)
5. Hat
6. Block, or the default concrete ledge when Block is None
7. Ledge accessory (coffee, bone, toy blocks)
8. Paws on the ledge

Tokens 1–8 of the generated drop are the eight signature stoop looks.

## Robinhood Chain + OpenSea

| | |
| --- | --- |
| Network | Robinhood Chain |
| Chain ID | 4663 (`0x1237`) |
| RPC | `https://rpc.mainnet.chain.robinhood.com` |
| Explorer | https://robinhoodchain.blockscout.com |
| Gas token | ETH |
| Marketplace | OpenSea Drop (bulk images + CSV) |
