export const caldera = {
  name: "Caldera",
  symbol: "CALD",
  tagline: "Offset-printed cardboard. A cafe table. The flame is the loop.",
  description:
    "Caldera is a 10,000-piece collection of looping hotel-matchbook PFP GIFs. Each book is stacked from seven plates — cloth, sleeve, inn, comb, strike, flame, and mark — then flattened onto one 12-frame GIF. Offset-printed cardboard on a cafe table. The flame is the loop.",
  story:
    "Caldera.\n\nA 10,000-piece collection of looping hotel-matchbook PFP GIFs on Robinhood Chain. Each book is stacked from seven plates — cloth, sleeve, inn, comb, strike, flame, and mark — then flattened onto one 12-frame GIF. Eight inns: cactus, lodge, diner, buoy, crown, shield, palm, and ticket. The print is cardboard. The flame is the loop.\n\nA souvenir matchbook on a cafe cloth, not a tin toy. Not a snow globe. Not neon tubing. No sticker edge. No egg. Not a shadow puppet. Not a fold. The book stays seated on one envelope. The strike is the flame. One shared clock.\n\nMinting at $0.25 on Robinhood Chain (chain ID 4663). Gas is ETH.",
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
    collection: "https://opensea.io/collection/caldera/overview",
    listings: [{ label: "Robinhood Chain", href: "https://opensea.io/collection/caldera/overview" }],
    blog: "https://opensea.io/blog/articles/robinhood-chain-is-live-on-opensea",
    explore: "https://opensea.io/collection/caldera/overview",
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type CalderaCollection = typeof caldera;
