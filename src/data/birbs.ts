export const birbs = {
  name: "BirbNation",
  symbol: "BIRB",
  tagline: "One sphere. A whole nation of vibes.",
  description:
    "BirbNation is a 2,222-piece collection of looping round-borb robin PFP GIFs on Robinhood Chain. Each birb is stacked from four layers — field, plumage, mug, and accent — then flattened onto one 12-frame GIF. One fat sphere. Chocolate cap. Burnt-orange chest. Cream belly. Thick brown outline. Soft-cel shade. A pink blep.",
  story:
    "Welcome to BirbNation.\n\nA 2,222-piece collection of looping round-borb robin PFP GIFs on Robinhood Chain. Each birb is stacked from four layers — field, plumage, mug, and accent — then flattened onto one 12-frame GIF. Sticker fields behind them. Chocolate caps. Burnt-orange chests. Cream bellies. Hats, crowns, and the occasional worm. Eyes blink. Wings twitch. The body stays a sphere.\n\nEach birb is a vibe — explorers, dreamers, jokers, guardians — on one shared clock.\n\nMinting on Robinhood Chain (chain ID 4663). Gas is ETH.",
  supply: 2222,
  mintPriceEth: "0.002",
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
    collection: "https://opensea.io/collection/birbnation/overview",
    blog: "https://opensea.io/blog/articles/robinhood-chain-is-live-on-opensea",
    explore: "https://opensea.io/collection/birbnation/overview",
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type BirbsCollection = typeof birbs;
