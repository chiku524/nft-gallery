import { afterimages, afterimageWorks } from "@/data/afterimages";
import { collection } from "@/data/collection";
import { inklingSamples } from "@/data/inkling-gallery";
import { inklings } from "@/data/inklings";
import { partyPandaSamples } from "@/data/party-panda-gallery";
import { partyPandas } from "@/data/party-pandas";
import { sampleMints } from "@/data/gallery";
import { wicklingSamples } from "@/data/wickling-gallery";
import { wicklings } from "@/data/wicklings";
import { AFTERIMAGES_BASE } from "@/lib/afterimages";
import { INKLINGS_BASE } from "@/lib/inklings";
import { LOOPKINS_BASE } from "@/lib/loopkins";
import { PARTY_PANDAS_BASE } from "@/lib/party-pandas";
import { WICKLINGS_BASE } from "@/lib/wicklings";

export const gallery = {
  name: "NFT Gallery",
  tagline: "Collections on the wall. One drop at a time.",
  description:
    "NFT Gallery is a house of on-chain collections — each drop keeps its own studio, traits, and launch path. Loopkins is the layered PFP. Afterimages is the 1:1 APNG drop. Inklings is the cartoon-squid PFP GIF drop on Ink. Party Pandas is the cartoon party-panda GIF drop on Base. Wicklings is the paper-lantern PFP GIF drop on Arbitrum.",
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
    status: "on the wall" as const,
    kind: "layered-pfp" as const,
    previews: inklingSamples.map((mint) => mint.image),
    studioHref: "/inklings/studio" as const,
    opensea: inklings.opensea.collection,
  },
  {
    slug: "party-pandas",
    href: PARTY_PANDAS_BASE,
    name: partyPandas.name,
    symbol: partyPandas.symbol,
    tagline: partyPandas.tagline,
    description: partyPandas.description,
    chain: partyPandas.chain.name,
    chainId: partyPandas.chain.chainId,
    supply: partyPandas.supply,
    cover: "/brand/banner-party-pandas.png",
    thumb: partyPandaSamples[0].image,
    status: "on the wall" as const,
    kind: "layered-pfp" as const,
    previews: partyPandaSamples.map((mint) => mint.image),
    studioHref: "/party-pandas/studio" as const,
    opensea: partyPandas.opensea.collection,
  },
  {
    slug: "wicklings",
    href: WICKLINGS_BASE,
    name: wicklings.name,
    symbol: wicklings.symbol,
    tagline: wicklings.tagline,
    description: wicklings.description,
    chain: wicklings.chain.name,
    chainId: wicklings.chain.chainId,
    supply: wicklings.supply,
    cover: "/brand/banner-wicklings.png",
    thumb: wicklingSamples[0].image,
    status: "new on the wall" as const,
    kind: "layered-pfp" as const,
    previews: wicklingSamples.map((mint) => mint.image),
    studioHref: "/wicklings/studio" as const,
    opensea: wicklings.opensea.collection,
  },
] as const;

export type GalleryProject = (typeof projects)[number];
