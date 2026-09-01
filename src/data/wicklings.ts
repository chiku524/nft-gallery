export const wicklings = {
  name: "Wicklings",
  symbol: "WICK",
  tagline: "Paper lanterns. A little flame that never goes out.",
  description:
    "Wicklings is an 8,888-piece collection of looping paper-lantern PFP GIFs on Arbitrum. Each one is a little flame living in a paper house — stacked from night, halo, vessel, wick, wrap, and drift, then flattened onto one 12-frame GIF. The lantern sways. The wick blinks. Moths never land.",
  story:
    "Wicklings never go out.\n\nAn 8,888-piece collection of looping paper-lantern PFP GIFs on Arbitrum. Each Wickling is a little flame that moved into a paper house. The lantern sways. The wick is the face — it blinks, it flickers, it never cools. Nights hang behind them. Halos breathe. Moths orbit and never land.\n\nSix layers on one 12-frame clock: night, halo, vessel, wick, wrap, and drift. Soft discs. Translucent paper. Warm amber on night indigo.\n\nMinting on Arbitrum (chain ID 42161). Gas is ETH.",
  supply: 8888,
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
