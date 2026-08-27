export const collection = {
  name: "Pugs On The Block",
  symbol: "POTB",
  tagline: "Neighborhood pugs, peeking over the stoop.",
  description:
    "Pugs On The Block is a 2,222-piece PFP collection of chibi pugs caught mid-peek over the city block. Every pug is assembled from layered traits — background, base, the block, hat, body, and accessory — ready to mint as ERC-721s on Robinhood Chain and list on OpenSea.",
  supply: 2222,
  mintPriceEth: "0.004",
  chain: {
    name: "Robinhood Chain",
    chainId: 4663,
    chainIdHex: "0x1237",
    currency: "ETH",
    rpcUrl: "https://rpc.mainnet.chain.robinhood.com",
    explorer: "https://robinhoodchain.blockscout.com",
    docs: "https://docs.robinhood.com/chain/connecting/",
  },
  opensea: {
    chainSlug: "robinhood",
    blog: "https://opensea.io/blog/articles/robinhood-chain-is-live-on-opensea",
    explore: "https://opensea.io",
  },
} as const;

export type Collection = typeof collection;
