export const hoodkins = {
  name: "Hoodkins",
  symbol: "HOOD",
  tagline: "Chibi raccoons in streetwear. They never sit still.",
  description:
    "Hoodkins is a 10,000-piece collection of looping chibi-raccoon PFP GIFs on Robinhood Chain. Each raccoon is stacked from six layers — pad, glow, pelt, fit, mug, and gear — then flattened onto one 12-frame GIF. Thick outlines. Flat fills. Bandit masks. Streetwear. Ears twitch. Eyes blink. Soft bob.",
  story:
    "Hoodkins never sit still.\n\nA 10,000-piece collection of looping chibi-raccoon PFP GIFs on Robinhood Chain. Each Hoodkin is stacked from six layers — pad, glow, pelt, fit, mug, and gear — then flattened onto one 12-frame GIF. Ledger desks behind them. Hoodies and beanies on top. Bandit masks. Ears twitch. Eyes blink. Soft bob.\n\nKawaii bust-crop raccoons with thick outlines, flat cel fills, and streetwear. One shared clock.\n\nMinting on Robinhood Chain (chain ID 4663). Gas is ETH.",
  supply: 10000,
  mintPriceEth: "0.005",
  frames: 12,
  frameDurationMs: 80,
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
    collection: "https://opensea.io/collection/hoodkins/overview",
    blog: "https://opensea.io/blog/articles/robinhood-chain-is-live-on-opensea",
    explore: "https://opensea.io/collection/hoodkins/overview",
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type HoodkinsCollection = typeof hoodkins;
