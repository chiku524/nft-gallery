export const foxins = {
  name: "Foxins",
  symbol: "FOXI",
  tagline: "Three pelts. One sticker. A grove of vibes.",
  description:
    "Foxins is a 5,555-piece collection of looping bold-graphic fox PFP GIFs. Each Foxin is stacked from six layers — field, pelt, mug, hat, wrap, and charm — then flattened onto one 12-frame GIF. Three bodies. One locked front-facing sticker. Hats sit between the ears. The silhouette never changes shape.",
  story:
    "Foxins.\n\nA 5,555-piece collection of looping bold-graphic fox PFP GIFs. Each Foxin is stacked from six layers — field, pelt, mug, hat, wrap, and charm — then flattened onto one 12-frame GIF. Three pelts only: maple, snow, and dusk. The sticker never gets a special cutout. Hats sit between the ears. Scarves sit on the neck. Charms float by the paws.\n\nFlat graphic — thick charcoal outline, limited palette, a little paper grain. Front-facing. Big circular head. Egg body. Tail on the right. One shared clock.\n\nMinting on Base (chain ID 8453). Gas is ETH.",
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
    collection: "https://opensea.io/collection/foxins/overview",
    blog: "https://opensea.io/learn/blockchain/blockchains-compatible-with-opensea",
    explore: "https://opensea.io/collection/foxins/overview",
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type FoxinsCollection = typeof foxins;
