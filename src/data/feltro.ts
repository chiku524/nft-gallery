export const feltro = {
  name: "Feltro",
  symbol: "FLTR",
  tagline: "Plush foam. Mesh eyes. A bounce down the court.",
  description:
    "Feltro is a 10,000-piece collection of looping foam-mascot PFP GIFs. Plush foam. Mesh eyes. A bounce down the court.",
  story:
    "Feltro.\n\nA 10,000-piece collection of looping foam-mascot PFP GIFs on Robinhood Chain. Each suit is stacked from seven plates — gym, suit, nap, mesh, seam, crest, and fuzz — then flattened onto one 12-frame GIF. Eight dancing suits: bear, lion, frog, bunny, dino, wolf, octopus, and shark. Mesh covers the eyes. A seam runs the cylinder. The bounce is the loop.\n\nPlush foam on a court. Not a leather puppet. Not neon tubing. Not soy-ink blots. The suit stays seated in one envelope. The dance is the squash. One shared clock.\n\nMinting free on Robinhood Chain (chain ID 4663). Gas is ETH.",
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
    collection: "https://opensea.io/collection/feltro/overview",
    listings: [{ label: "Robinhood Chain", href: "https://opensea.io/collection/feltro/overview" }],
    blog: "https://opensea.io/blog/articles/robinhood-chain-is-live-on-opensea",
    explore: "https://opensea.io/collection/feltro/overview",
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type FeltroCollection = typeof feltro;
