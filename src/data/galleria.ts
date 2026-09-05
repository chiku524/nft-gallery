import galleriaWorksJson from "./galleria-works.json";

export const galleria = {
  name: "Galleria On Ink",
  symbol: "GOI",
  tagline: "500 open editions. No two share a medium.",
  description:
    "Galleria On Ink is a salon of 500 unique looping paintings on Ink. Each work invents its own medium, palette, and motion. The composition is 1:1. The mint is an open edition.",
  story:
    "Galleria On Ink.\n\nA salon of 500 unique looping paintings on Ink. Each work invents its own medium, palette, silhouette, and motion. Neighboring tokens are not siblings. There is no trait stack and no shared character.\n\nEvery artwork is an open edition. The composition is 1:1. The mint is not.\n\nTwelve frames, ninety milliseconds, 512×512. Minting on Ink (chain ID 57073). Gas is ETH.",
  supply: 500,
  mintPriceEth: "0.008",
  frames: 12,
  frameDurationMs: 90,
  canvas: 512,
  edition: "Open Edition" as const,
  chain: {
    name: "Ink",
    chainId: 57073,
    chainIdHex: "0xdef1",
    currency: "ETH",
    rpcUrl: "https://rpc-gel.inkonchain.com",
    explorer: "https://explorer.inkonchain.com",
    docs: "https://docs.inkonchain.com/general/network-information",
  },
  opensea: {
    chainSlug: "ink",
    collection: "https://opensea.io/collection/galleria-on-ink",
    blog: "https://opensea.io/learn/blockchain/blockchains-compatible-with-opensea",
    explore: "https://opensea.io/collection/galleria-on-ink",
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type GalleriaCollection = typeof galleria;

export type GalleriaWork = {
  id: number;
  slug: string;
  title: string;
  image: string;
  description: string;
  attributes: { trait_type: string; value: string }[];
};

export const galleriaWorks = galleriaWorksJson as GalleriaWork[];

export function getGalleriaWork(id: number): GalleriaWork | undefined {
  return galleriaWorks.find((work) => work.id === id);
}
