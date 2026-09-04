import strangerWorks from "./stranger-works.json";

export const strangers = {
  name: "Strangers",
  symbol: "STRNGR",
  tagline: "24 open editions. No two share a medium.",
  description:
    "Strangers is a salon of 24 unique looping paintings on Base. Each work invents its own medium, palette, and motion. The composition is 1:1. The mint is an open edition.",
  story:
    "Strangers do not match.\n\nA salon of 24 unique looping paintings on Base. Each work invents its own medium, palette, silhouette, and motion. Neighboring tokens are not siblings. There is no trait stack and no shared character.\n\nEvery artwork is an open edition. The composition is 1:1. The mint is not.\n\nTwelve frames, ninety milliseconds, 512×512. Minting on Base (chain ID 8453). Gas is ETH.",
  supply: 24,
  mintPriceEth: "0.008",
  frames: 12,
  frameDurationMs: 90,
  canvas: 512,
  edition: "Open Edition" as const,
  chain: {
    name: "Base",
    chainId: 8453,
    chainIdHex: "0x2105",
    currency: "ETH",
    rpcUrl: "https://mainnet.base.org",
    explorer: "https://basescan.org",
    docs: "https://docs.base.org/docs/network-information",
  },
  opensea: {
    chainSlug: "base",
    collection: "https://opensea.io/collection/strangers-on-base",
    blog: "https://opensea.io/learn/blockchain/blockchains-compatible-with-opensea",
    explore: "https://opensea.io/collection/strangers-on-base",
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type StrangersCollection = typeof strangers;

export type StrangerWork = {
  id: number;
  slug: string;
  title: string;
  image: string;
  description: string;
  attributes: { trait_type: string; value: string }[];
};

export const strangerWorksList = strangerWorks as StrangerWork[];

export function getStrangerWork(id: number): StrangerWork | undefined {
  return strangerWorksList.find((work) => work.id === id);
}
