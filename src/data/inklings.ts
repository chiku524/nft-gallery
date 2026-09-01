export const inklings = {
  name: "Inklings",
  symbol: "INKL",
  tagline: "Cartoon squid PFPs, painted in ink wash.",
  description:
    "Inklings is a 5,555-piece collection of looping cartoon-squid PFPs on Ink. Each squid is stacked from six painterly layers — paper, bloom, visage, gaze, mark, and adorn — then flattened onto one 16-frame GIF. Washes drift, eyes blink, tentacles sway. Nothing is pixelated.",
  story:
    "Inklings are painted cartoon squids, not pixel art.\n\nA 5,555-piece collection of looping ink-wash squid PFPs on Ink, Kraken’s Ethereum layer 2. Each Inkling is stacked from six painterly layers — paper, bloom, visage, gaze, mark, and adorn — then flattened onto one 16-frame GIF. Dye drifts. Eyes blink. Tentacles sway. Soft edges only.\n\nMinting on Ink (chain ID 57073). Gas is ETH.",
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
    collection: "https://opensea.io/collection/inklings-on-ink/overview",
    blog: "https://opensea.io/learn/blockchain/blockchains-compatible-with-opensea",
    explore: "https://opensea.io/collection/inklings-on-ink/overview",
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type InklingsCollection = typeof inklings;
