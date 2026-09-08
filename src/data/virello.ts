export const virello = {
  name: "Virello",
  symbol: "VIRL",
  tagline: "Lithographed enamel. Stamped metal. The winding key is the loop.",
  description:
    "Virello is a 10,000-piece collection of looping wind-up tin-toy PFP GIFs. Each toy is stacked from seven plates — bench, chassis, enamel, decal, key, spark, and wear — then flattened onto one 12-frame GIF. Lithographed enamel on stamped metal. The winding key is the loop.",
  story:
    "Virello.\n\nA 10,000-piece collection of looping wind-up tin-toy PFP GIFs on Robinhood Chain. Each toy is stacked from seven plates — bench, chassis, enamel, decal, key, spark, and wear — then flattened onto one 12-frame GIF. Eight chassis: robot, duck, racer, soldier, monkey, tank, copter, and frog. The print is lithographed. The key is the loop.\n\nStamped metal on a toy-shop bench, not a snow globe. Not neon tubing. No sticker edge. No egg. Not a shadow puppet. Not a fold. The toy stays seated on one envelope. The wind-up is the key. One shared clock.\n\nMinting at $0.25 on Robinhood Chain (chain ID 4663). Gas is ETH.",
  supply: 10000,
  mintPriceUsd: "0.25",
  mintPriceEth: "0.0001",
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
    collection: "https://opensea.io/collection/virello/overview",
    listings: [{ label: "Robinhood Chain", href: "https://opensea.io/collection/virello/overview" }],
    blog: "https://opensea.io/blog/articles/robinhood-chain-is-live-on-opensea",
    explore: "https://opensea.io/collection/virello/overview",
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type VirelloCollection = typeof virello;
