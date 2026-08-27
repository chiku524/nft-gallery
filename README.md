# Pugs On The Block

Neighborhood pugs peeking over the stoop. A 2,222-piece PFP collection of layered chibi pugs, built to mint as ERC-721s on **Robinhood Chain** (chain ID `4663`) and list on **OpenSea**.

## What’s in this repo

- Trait art at `public/traits/` — background, base, block, hat, body, accessory (1024×1024 PNGs with transparent layers where they overlay)
- Eight finished sample mints in `public/gallery/`
- Collection logo and banner in `public/brand/`
- OpenSea-shaped metadata in `public/metadata/`
- An interactive trait studio that composites layers in the browser
- `contracts/PugsOnTheBlock.sol` — ERC-721 with a 2,222 supply cap

## Run locally

```bash
npm install
npm run dev
```

The app listens on [http://127.0.0.1:43147](http://127.0.0.1:43147).

## Trait stack

Draw order, back to front:

1. Background
2. Block (the ledge)
3. Base pug
4. Body (bandana, collar, hoodie, chain)
5. Hat
6. Accessory (shades, monocle, or a treat on the ledge)

Mix them in `/studio`, browse the sheets on `/traits`, and inspect sample tokens on `/gallery`.

## Robinhood Chain + OpenSea

| | |
| --- | --- |
| Network | Robinhood Chain |
| Chain ID | 4663 (`0x1237`) |
| RPC | `https://rpc.mainnet.chain.robinhood.com` |
| Explorer | https://robinhoodchain.blockscout.com |
| Gas token | ETH |
| Marketplace | OpenSea (Robinhood Chain is a supported network) |

Launch checklist lives on `/launch`. After you pin images and metadata, deploy the contract, verify it, then import the collection on OpenSea.

## License

Art and site code in this repository are for the Pugs On The Block drop. Swap the zero-address fee recipient in `public/metadata/collection.json` before you list.
