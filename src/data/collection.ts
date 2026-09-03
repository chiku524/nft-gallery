export const collection = {
  name: "Loopkins",
  symbol: "LOOP",
  tagline: "Layered APNG PFPs that never sit still.",
  description:
    "Loopkins is a 10,000-piece collection of looping PFP creatures. Each Loopkin is stacked from six APNG layers — sky, aura, body, face, wear, and charm — then flattened onto one 12-frame GIF. Skies pulse. Auras breathe. Faces blink. Charms orbit. One shared clock. Minting on Robinhood Chain.",
  story:
    "Loopkins never sit still.\n\nA 10,000-piece collection of looping PFP creatures on Robinhood Chain. Each Loopkin is stacked from six layers — sky, aura, body, face, wear, and charm — then flattened onto one 12-frame GIF. Skies pulse. Auras breathe. Faces blink. Charms orbit.\n\nOne shared clock. The studio stacks the layers live. OpenSea gets the flattened loop.\n\nMinting on Robinhood Chain (chain ID 4663). Gas is ETH.",
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
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type Collection = typeof collection;
