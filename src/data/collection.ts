export const collection = {
  name: "Loopkins",
  symbol: "LOOP",
  tagline: "Layered APNG PFPs that never sit still.",
  description:
    "Loopkins is a 3,333-piece PFP collection of looping creatures. Every token is stacked from APNG trait layers — skies pulse, auras breathe, faces blink, charms orbit — then flattened onto one shared 12-frame clock for mint.",
  supply: 3333,
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
    blog: "https://opensea.io/blog/articles/robinhood-chain-is-live-on-opensea",
    explore: "https://opensea.io",
  },
} as const;

export type Collection = typeof collection;
