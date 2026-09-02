export const mochins = {
  name: "Mochins",
  symbol: "MOCHI",
  tagline: "Soft 3D mochi under studio light. They never sit still.",
  description:
    "Mochins is a 4,000-piece collection of looping soft-3D mochi PFP GIFs on Shape. Each mochi is stacked from six layers — stage, haze, dough, face, topping, and steam — then flattened onto one 16-frame GIF. Studio light. Volume. Specular. Contact shadow. No outlines. The dough squashes. Steam rises.",
  story:
    "Mochins never sit still.\n\nA 4,000-piece collection of looping soft-3D mochi PFP GIFs on Shape. Each Mochin is stacked from six layers — stage, haze, dough, face, topping, and steam — then flattened onto one 16-frame GIF. Ceramic plates. Matcha and sesame dough. Studio key light. Soft squash. Steam lifts off the crown.\n\nSculpted daifuku with volume, rim light, and contact shadow. No outlines. One shared clock.\n\nMinting on Shape (chain ID 360). Gas is ETH.",
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
