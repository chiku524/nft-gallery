export const scribblins = {
  name: "Scribblins",
  symbol: "SCRIB",
  tagline: "Four doodle critters. Thick ink. Warm paper.",
  description:
    "Scribblins is a 5,555-piece collection of looping doodle-critter PFP GIFs. Each Scribblin is stacked from six layers — field, body, mug, hat, wrap, and charm — then flattened onto one 12-frame GIF. Four bodies. One locked friendly cartoon. Thick ink, warm paper, no rainbow.",
  story:
    "Scribblins never try that hard.\n\nA 5,555-piece collection of looping doodle-critter PFP GIFs on Base. Each Scribblin is stacked from six layers — field, body, mug, hat, wrap, and charm — then flattened onto one 12-frame GIF. Four bodies only: bunny, bear, pup, and frog. The drawing stays friendly — thick charcoal outline, big oval eyes, a little blush, warm paper instead of rainbow ink.\n\nHats sit on one crown. Scarves sit on the neck. Charms float beside the paws. One shared clock.\n\nMinting on Base (chain ID 8453). Gas is ETH.",
  supply: 5555,
  mintPriceEth: "0.004",
  frames: 12,
  frameDurationMs: 90,
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
  opensea: {
    chainSlug: "base",
    collection: "https://opensea.io/collection/scribblins-5555/overview",
    blog: "https://opensea.io/learn/blockchain/blockchains-compatible-with-opensea",
    explore: "https://opensea.io/collection/scribblins-5555/overview",
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type ScribblinsCollection = typeof scribblins;
