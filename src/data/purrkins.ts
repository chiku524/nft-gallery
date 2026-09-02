export const purrkins = {
  name: "Purrkins",
  symbol: "PURR",
  tagline: "Chibi cats in streetwear. They never sit still.",
  description:
    "Purrkins is a 4,000-piece collection of looping chibi-cat PFP GIFs on HyperEVM. Each cat is stacked from six layers — pad, glow, pelt, fit, mug, and gear — then flattened onto one 12-frame GIF. Thick outlines. Flat fills. Streetwear. Ears twitch. Eyes blink. Soft bob.",
  story:
    "Purrkins never sit still.\n\nA 4,000-piece collection of looping chibi-cat PFP GIFs on HyperEVM. Each Purrkin is stacked from six layers — pad, glow, pelt, fit, mug, and gear — then flattened onto one 12-frame GIF. Pastel desks behind them. Hoodies and beanies on top. Ears twitch. Eyes blink. Soft bob.\n\nKawaii bust-crop cats with thick outlines, flat cel fills, and streetwear. One shared clock.\n\nMinting on HyperEVM (chain ID 999). Gas is HYPE.",
  supply: 4000,
  mintPriceEth: "1",
  frames: 12,
  frameDurationMs: 80,
  canvas: 512,
  chain: {
    name: "HyperEVM",
    chainId: 999,
    chainIdHex: "0x3e7",
    currency: "HYPE",
    rpcUrl: "https://rpc.hyperliquid.xyz/evm",
    explorer: "https://hyperevmscan.io",
    docs: "https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/hyperevm",
  },
  opensea: {
    chainSlug: "hyperevm",
    collection: "https://opensea.io/collection/purrkins/overview",
    blog: "https://opensea.io/learn/blockchain/blockchains-compatible-with-opensea",
    explore: "https://opensea.io/collection/purrkins/overview",
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type PurrkinsCollection = typeof purrkins;
