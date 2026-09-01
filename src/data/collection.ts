export const collection = {
  name: "Loopkins",
  symbol: "LOOP",
  tagline: "Layered APNG PFPs that never sit still.",
  description:
    "Loopkins is a 10,000-piece collection of looping PFP creatures. Each Loopkin is stacked from animated APNG trait layers — skies pulse, auras breathe, faces blink, and charms orbit — then flattened onto one shared 12-frame clock. Minting on Robinhood Chain.",
  supply: 10000,
  mintPriceEth: "0.005",
  frames: 12,
  frameDurationMs: 80,
  canvas: 512,
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
    collection: "https://opensea.io/collection/loopkins/overview",
    blog: "https://opensea.io/blog/articles/robinhood-chain-is-live-on-opensea",
    explore: "https://opensea.io/collection/loopkins/overview",
  },
} as const;

export type Collection = typeof collection;
