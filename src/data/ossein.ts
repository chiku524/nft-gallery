export const ossein = {
  name: "Ossein",
  symbol: "OSSN",
  tagline: "Ivory bone. Hairline ink. A step on the grid.",
  description:
    "Ossein is a 10,000-piece collection of looping anatomical-chart PFP GIFs. Ivory bone. Hairline ink. A step on the grid.",
  story:
    "Ossein.\n\nA 10,000-piece collection of looping anatomical-chart PFP GIFs on Robinhood Chain. Each plate is stacked from seven plates — sheet, rule, specimen, joint, leader, stain, and chalk — then flattened onto one 12-frame GIF. Eight dancing specimens: cortical, avian, feline, equine, frog, ape, fish, and serpent. Ivory bone. Hairline ink. The step is the loop.\n\nA medical chart, not a leather puppet. Not neon tubing. Not soy-ink blots. The specimen stays seated on one sheet. The dance is in the joints. One shared clock.\n\nMinting free on Robinhood Chain (chain ID 4663). Gas is ETH.",
  supply: 10000,
  mintPriceEth: "0",
  frames: 12,
  frameDurationMs: 90,
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
    collection: "https://opensea.io/collection/ossein/overview",
    listings: [{ label: "Robinhood Chain", href: "https://opensea.io/collection/ossein/overview" }],
    blog: "https://opensea.io/blog/articles/robinhood-chain-is-live-on-opensea",
    explore: "https://opensea.io/collection/ossein/overview",
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type OsseinCollection = typeof ossein;
