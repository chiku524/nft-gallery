export const vinylon = {
  name: "Vinylon",
  symbol: "VNYL",
  tagline: "Inflated tubes. Knots. A shine on the latex.",
  description:
    "Vinylon is a 10,000-piece collection of looping balloon-animal PFP GIFs. Inflated tubes. Knots. A shine on the latex.",
  story:
    "Vinylon.\n\nA 10,000-piece collection of looping balloon-animal PFP GIFs on Robinhood Chain. Each twist is stacked from seven plates — booth, latex, twist, knot, valve, gleam, and confetti — then flattened onto one 12-frame GIF. Eight dancing twists: hound, hare, steed, swan, monkey, dino, poodle, and figure. Inflated tubes. Knots at the joints. The bob is the loop.\n\nLatex in a booth. Not neon tubing. Not a leather puppet. Not soy-ink blots. The twist stays seated in one envelope. The dance is the squeeze. One shared clock.\n\nMinting free on Robinhood Chain (chain ID 4663). Gas is ETH.",
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
    collection: "https://opensea.io/collection/vinylon/overview",
    listings: [{ label: "Robinhood Chain", href: "https://opensea.io/collection/vinylon/overview" }],
    blog: "https://opensea.io/blog/articles/robinhood-chain-is-live-on-opensea",
    explore: "https://opensea.io/collection/vinylon/overview",
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type VinylonCollection = typeof vinylon;
