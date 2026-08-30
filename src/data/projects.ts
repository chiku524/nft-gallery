import { collection } from "@/data/collection";
import { POTB_BASE } from "@/lib/potb";

export const gallery = {
  name: "NFT Gallery",
  tagline: "Collections on the wall. One drop at a time.",
  description:
    "NFT Gallery is a house of on-chain collections — each drop keeps its own studio, traits, and launch path. Pugs On The Block is the first project on the wall.",
} as const;

export const projects = [
  {
    slug: "pugs-on-the-block",
    href: POTB_BASE,
    name: collection.name,
    symbol: collection.symbol,
    tagline: collection.tagline,
    description: collection.description,
    chain: collection.chain.name,
    chainId: collection.chain.chainId,
    supply: collection.supply,
    mintPriceEth: collection.mintPriceEth,
    cover: "/brand/banner-pugs-on-the-block.png",
    thumb: "/generated-preview/1.jpg",
    status: "on the wall" as const,
  },
] as const;

export type GalleryProject = (typeof projects)[number];
