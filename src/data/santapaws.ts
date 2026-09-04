export const santapaws = {
  name: "Santa Paws",
  symbol: "PAWS",
  tagline: "Always in the mood of giving.",
  description:
    "Santa Paws is a 7,777-piece collection of looping chibi-cat PFP GIFs on Base. Each cat is stacked from six layers — yard, glow, pelt, mug, hat, and gear — then flattened onto one 12-frame GIF. Thick outlines. Cozy winter yards. Always in the mood of giving.",
  story:
    "Santa Paws is always in the mood of giving.\n\nA 7,777-piece collection of looping chibi-cat PFP GIFs on Base. Each Santa Paw is stacked from six layers — yard, glow, pelt, mug, hat, and gear — then flattened onto one 12-frame GIF. Snowy nights and cookie kitchens behind them. Santa hats and cocoa on top. Ears twitch. Eyes blink. Soft bob.\n\nKawaii bust-crop cats with thick outlines, flat cel fills, and a Christmas wardrobe. One shared clock.\n\nMinting on Base (chain ID 8453). Gas is ETH.",
  supply: 7777,
  mintPriceEth: "0.004",
  frames: 12,
  frameDurationMs: 90,
  canvas: 512,
  chain: {
    name: "Base",
    chainId: 8453,
    chainIdHex: "0x2105",
    currency: "ETH",
    rpcUrl: "https://mainnet.base.org",
    explorer: "https://basescan.org",
    docs: "https://docs.base.org",
  },
  opensea: {
    chainSlug: "base",
    collection: "https://opensea.io/collection/santa-paws-123/overview",
    blog: "https://opensea.io/learn/blockchain/blockchains-compatible-with-opensea",
    explore: "https://opensea.io/collection/santa-paws-123/overview",
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type SantaPawsCollection = typeof santapaws;
