export const wicklings = {
  name: "Wicklings",
  symbol: "WICK",
  tagline: "Paper lanterns. A little flame that never goes out.",
  description:
    "Wicklings is a 10,000-piece collection of looping paper-lantern PFP GIFs on Arbitrum. Each lantern is stacked from six layers — night, halo, vessel, wick, wrap, and drift — then flattened onto one 12-frame GIF. Paper glows. The wick blinks. Moths never land.",
  story:
    "Wicklings never go out.\n\nA 10,000-piece collection of looping paper-lantern PFP GIFs on Arbitrum. Each lantern is stacked from six layers — night, halo, vessel, wick, wrap, and drift — then flattened onto one 12-frame GIF. Paper glows. The wick blinks. Moths never land.\n\nSoft discs, translucent paper, a little flame with a face. One shared clock.\n\nMinting on Arbitrum (chain ID 42161). Gas is ETH.",
  supply: 10000,
  mintPriceEth: "0.003",
  frames: 12,
  frameDurationMs: 80,
  canvas: 512,
  chain: {
    name: "Arbitrum",
    chainId: 42161,
    chainIdHex: "0xa4b1",
    currency: "ETH",
    rpcUrl: "https://arb1.arbitrum.io/rpc",
    explorer: "https://arbiscan.io",
    docs: "https://docs.arbitrum.io",
  },
  opensea: {
    chainSlug: "arbitrum",
    collection: "https://opensea.io/collection/wicklings/overview",
    blog: "https://opensea.io/learn/blockchain/blockchains-compatible-with-opensea",
    explore: "https://opensea.io/collection/wicklings/overview",
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type WicklingsCollection = typeof wicklings;
