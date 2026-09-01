import { afterimages, afterimageWorks } from "@/data/afterimages";
import { collection } from "@/data/collection";
import { inklingSamples } from "@/data/inkling-gallery";
import { inklings } from "@/data/inklings";
import { sampleMints } from "@/data/gallery";
import { AFTERIMAGES_BASE } from "@/lib/afterimages";
import { INKLINGS_BASE } from "@/lib/inklings";
import { LOOPKINS_BASE } from "@/lib/loopkins";

export const gallery = {
  name: "NFT Gallery",
  tagline: "Collections on the wall. One drop at a time.",
  description:
    "NFT Gallery is a house of on-chain collections — each drop keeps its own studio, traits, and launch path. Loopkins is the layered PFP. Afterimages is the 1:1 APNG drop. Inklings is the cartoon-squid PFP GIF drop on Ink.",
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
    cover: "/brand/banner-loopkins.png",
    thumb: "/generated-preview/1.png",
    status: "on the wall" as const,
    kind: "layered-pfp" as const,
    previews: sampleMints.slice(0, 8).map((mint) => mint.image),
    studioHref: "/studio" as const,
    opensea: collection.opensea.collection,
  },
  {
    slug: "afterimages",
    href: AFTERIMAGES_BASE,
    name: afterimages.name,
    symbol: afterimages.symbol,
    tagline: afterimages.tagline,
    description: afterimages.description,
    chain: afterimages.chain.name,
    chainId: afterimages.chain.chainId,
    supply: afterimages.supply,
    cover: "/brand/banner-afterimages.png",
    thumb: afterimageWorks[0].image,
    status: "on the wall" as const,
    kind: "1of1" as const,
    previews: afterimageWorks.map((work) => work.image),
    studioHref: null,
    opensea: afterimages.opensea.collection,
  },
  {
    slug: "inklings",
    href: INKLINGS_BASE,
    name: inklings.name,
    symbol: inklings.symbol,
    tagline: inklings.tagline,
    description: inklings.description,
    chain: inklings.chain.name,
    chainId: inklings.chain.chainId,
    supply: inklings.supply,
    cover: "/brand/banner-inklings.png",
    thumb: inklingSamples[0].image,
    status: "new on the wall" as const,
    kind: "layered-pfp" as const,
    previews: inklingSamples.map((mint) => mint.image),
    studioHref: "/inklings/studio" as const,
    opensea: inklings.opensea.collection,
  },
] as const;

export type GalleryProject = (typeof projects)[number];
