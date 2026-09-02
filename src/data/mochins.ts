export const mochins = {
  name: "Mochins",
  symbol: "MOCHI",
  tagline: "Gloss vinyl toys on a collector shelf. They never sit still.",
  description:
    "Mochins is a 4,000-piece collection of looping vinyl-toy mochi PFP GIFs on Shape. Each figure is stacked from six layers — stage, haze, vinyl, face, topping, and steam — then flattened onto one 16-frame GIF. Gloss plastic. Tight spec. Clear coat. No outlines. Collector-shelf light. The vinyl idles.",
  story:
    "Mochins never sit still.\n\nA 4,000-piece collection of looping vinyl-toy mochi PFP GIFs on Shape. Each Mochin is stacked from six layers — stage, haze, vinyl, face, topping, and steam — then flattened onto one 16-frame GIF. Lacquered stands. Ivory, matcha, and black vinyl. Studio key light. A hard highlight. Shelf glitter in the air.\n\nDesigner-toy daifuku with volume, rim light, and a planted contact shadow. No outlines. One shared clock.\n\nMinting on Shape (chain ID 360). Gas is ETH.",
  supply: 4000,
  mintPriceEth: "0.004",
  frames: 16,
  frameDurationMs: 100,
  canvas: 512,
  chain: {
    name: "Shape",
    chainId: 360,
    chainIdHex: "0x168",
    currency: "ETH",
    rpcUrl: "https://mainnet.shape.network",
    explorer: "https://shapescan.xyz",
    docs: "https://docs.shape.network/",
  },
  opensea: {
    chainSlug: "shape",
    collection: "https://opensea.io/collection/mochins/overview",
    blog: "https://opensea.io/learn/blockchain/blockchains-compatible-with-opensea",
    explore: "https://opensea.io/collection/mochins/overview",
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type MochinsCollection = typeof mochins;
