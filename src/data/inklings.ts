export const inklings = {
  name: "Inklings",
  symbol: "INKL",
  tagline: "Smooth ink-wash PFP GIFs that never sit still.",
  description:
    "Inklings is a 5,555-piece collection of illustrated PFP portraits. Each face is stacked from painterly GIF layers — paper washes drift, blooms breathe, visages bob, eyes blink — then flattened onto one shared 16-frame clock. Soft edges only. Minting on Ink.",
  supply: 5555,
  mintPriceEth: "0.006",
  frames: 16,
  frameDurationMs: 90,
  canvas: 640,
  chain: {
    name: "Ink",
    chainId: 57073,
    chainIdHex: "0xdef1",
    currency: "ETH",
    rpcUrl: "https://rpc-gel.inkonchain.com",
    explorer: "https://explorer.inkonchain.com",
    docs: "https://docs.inkonchain.com/general/network-information",
  },
  opensea: {
    chainSlug: "ink",
    blog: "https://opensea.io/learn/blockchain/blockchains-compatible-with-opensea",
    explore: "https://opensea.io",
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type InklingsCollection = typeof inklings;
