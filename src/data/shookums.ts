export const shookums = {
  name: "Halloween Shook'ums",
  symbol: "SHOOK",
  tagline: "Three sheets. One skeleton. A whole haunt of vibes.",
  description:
    "Halloween Shook'ums is a 5,555-piece collection of looping sheet-ghost PFP GIFs. Each Shook'um is stacked from six layers — night, sheet, mug, hat, wrap, and charm — then flattened onto one 12-frame GIF. Three bodies. One locked skeleton. Hats sit on the crown. The sheet never changes shape.",
  story:
    "Halloween Shook'ums.\n\nA 5,555-piece collection of looping sheet-ghost PFP GIFs. Each Shook'um is stacked from six layers — night, sheet, mug, hat, wrap, and charm — then flattened onto one 12-frame GIF. Three sheets only: classic, blush, and void. The silhouette never gets a special cutout. Witch hats, pumpkin buckets, gold chains, and the occasional bat sit on the same crown, neck, and hands.\n\nPainted 3D clay — canvas grain, wrap shade, a warm key from the left. Spooked, sleepy, sparkly. One hem. One shared clock.\n\nMinting on Abstract (chain ID 2741). Gas is ETH.",
  supply: 5555,
  mintPriceEth: "0.004",
  frames: 12,
  frameDurationMs: 90,
  canvas: 512,
  chain: {
    name: "Abstract",
    chainId: 2741,
    chainIdHex: "0xab5",
    currency: "ETH",
    rpcUrl: "https://api.mainnet.abs.xyz",
    explorer: "https://abscan.org",
    docs: "https://docs.abs.xyz",
  },
  opensea: {
    chainSlug: "abstract",
    collection: "https://opensea.io/collection/halloween-shookums/overview",
    blog: "https://opensea.io/learn/blockchain/blockchains-compatible-with-opensea",
    explore: "https://opensea.io/collection/halloween-shookums/overview",
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type ShookumsCollection = typeof shookums;
