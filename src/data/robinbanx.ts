export const robinBanx = {
  name: "Robin Banx",
  symbol: "RBX",
  tagline: "Ten thousand masked operators. Every portrait leaves a paper trail.",
  description:
    "Robin Banx is a 10,000-piece static PNG PFP collection on Base. Angular noir portraits combine masked human crooks, halftone shadows, evidence stamps, and multichain-themed accessories.",
  story:
    "Robin Banx is an open case file: 10,000 masked human crooks assembled from hard-edged portrait plates, photocopied shadows, seized-property labels, and network contraband.\n\nEvery PFP reads like a page pulled from a security dossier. Faces stay hidden. Angles stay sharp. Chain references arrive as accessories and evidence, not endorsements.\n\nMinting is free on Base (chain ID 8453). Collectors pay only ETH gas.",
  supply: 10_000,
  mintPriceEth: "0",
  maxPerTransaction: 10,
  format: "Static PNG",
  canvas: 512,
  chain: {
    name: "Base",
    chainId: 8453,
    chainIdHex: "0x2105",
    currency: "ETH",
    rpcUrl: "https://mainnet.base.org",
    explorer: "https://basescan.org",
    docs: "https://docs.base.org",
  },
  marketplace: {
    status: "Not launched",
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type RobinBanxCollection = typeof robinBanx;
