export const foxkins = {
  name: "Foxkins",
  symbol: "FOXK",
  tagline: "Three pelts. One loaf-orb. A grove of vibes.",
  description:
    "Foxkins is a 5,555-piece collection of looping clay fox PFP GIFs. Each Foxkin is stacked from six layers — field, pelt, mug, hat, wrap, and charm — then flattened onto one 12-frame GIF. Three bodies. One locked Mix 3 skeleton. Hats sit between the ears. The loaf never changes shape.",
  story:
    "Foxkins.\n\nA 5,555-piece collection of looping clay fox PFP GIFs. Each Foxkin is stacked from six layers — field, pelt, mug, hat, wrap, and charm — then flattened onto one 12-frame GIF. Three pelts only: maple, snow, and dusk. The silhouette never gets a special cutout. Hats sit between the ears. Scarves sit on the neck. Charms float by the tucked paws.\n\nPainted 3D clay — canvas grain, wrap shade, a warm key from the left. Mix 3 three-quarter pose. Croissant tail on the left. Cream muzzle facing right. One shared clock.\n\nMinting on Base (chain ID 8453). Gas is ETH.",
  supply: 5555,
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
    collection: "https://opensea.io/collection/foxkins/overview",
    blog: "https://opensea.io/learn/blockchain/blockchains-compatible-with-opensea",
    explore: "https://opensea.io/collection/foxkins/overview",
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type FoxkinsCollection = typeof foxkins;
