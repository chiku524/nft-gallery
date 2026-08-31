export const inklings = {
  name: "Inklings",
  symbol: "INKL",
  tagline: "Smooth ink-wash PFP GIFs that never sit still.",
  description:
    "Inklings is a 5,555-piece collection of looping ink-wash portraits on Ink. Each face is stacked from six painterly layers — paper, bloom, visage, gaze, mark, and adorn — then flattened onto one 16-frame GIF. Washes drift, eyes blink, edges stay soft. Nothing is pixelated.",
  story:
    "Inklings are painted, not pixelated.\n\nA 5,555-piece collection of looping ink-wash PFP portraits on Ink, Kraken’s Ethereum layer 2. Each Inkling is stacked from six painterly layers — paper, bloom, visage, gaze, mark, and adorn — then flattened onto one 16-frame GIF. Dye drifts. Eyes blink. Soft edges only.\n\nMinting on Ink (chain ID 57073). Gas is ETH. 0.006 ETH to mint.",
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
