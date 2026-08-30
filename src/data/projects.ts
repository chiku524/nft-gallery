import { collection } from "@/data/collection";
import { LOOPKINS_BASE } from "@/lib/loopkins";

export const gallery = {
  name: "NFT Gallery",
  tagline: "Collections on the wall. One drop at a time.",
  description:
    "NFT Gallery is a house of on-chain collections — each drop keeps its own studio, traits, and launch path. Loopkins is the first project on the wall.",
} as const;

export const projects = [
  {
    slug: "loopkins",
    href: LOOPKINS_BASE,
    name: collection.name,
    symbol: collection.symbol,
    tagline: collection.tagline,
    description: collection.description,
    chain: collection.chain.name,
    chainId: collection.chain.chainId,
    supply: collection.supply,
    mintPriceEth: collection.mintPriceEth,
    cover: "/brand/banner-loopkins.png",
    thumb: "/generated-preview/1.png",
    status: "on the wall" as const,
  },
] as const;

export type GalleryProject = (typeof projects)[number];
