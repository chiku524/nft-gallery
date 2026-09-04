import { afterimages, afterimageWorks } from "@/data/afterimages";
import { collection } from "@/data/collection";
import { inklingSamples } from "@/data/inkling-gallery";
import { inklings } from "@/data/inklings";
import { hoodkinSamples } from "@/data/hoodkin-gallery";
import { hoodkins } from "@/data/hoodkins";
import { birbSamples } from "@/data/birb-gallery";
import { birbs } from "@/data/birbs";
import { shookumSamples } from "@/data/shookum-gallery";
import { shookums } from "@/data/shookums";
import { foxinSamples } from "@/data/foxin-gallery";
import { foxins } from "@/data/foxins";
import { purrkinSamples } from "@/data/purrkin-gallery";
import { purrkins } from "@/data/purrkins";
import { santapawSamples } from "@/data/santapaw-gallery";
import { santapaws } from "@/data/santapaws";
import { scribblinSamples } from "@/data/scribblin-gallery";
import { scribblins } from "@/data/scribblins";
import { groovySamples } from "@/data/groovy-gallery";
import { groovy } from "@/data/groovy";
import { galleria, galleriaWorks } from "@/data/galleria";
import { sampleMints } from "@/data/gallery";
import { wicklingSamples } from "@/data/wickling-gallery";
import { wicklings } from "@/data/wicklings";
import { AFTERIMAGES_BASE } from "@/lib/afterimages";
import { BIRBS_BASE } from "@/lib/birbs";
import { SHOOKUMS_BASE } from "@/lib/shookums";
import { FOXINS_BASE } from "@/lib/foxins";
import { SANTAPAWS_BASE } from "@/lib/santapaws";
import { SCRIBBLINS_BASE } from "@/lib/scribblins";
import { GROOVY_BASE } from "@/lib/groovy";
import { GALLERIA_BASE } from "@/lib/galleria";
import { HOODKINS_BASE } from "@/lib/hoodkins";
import { INKLINGS_BASE } from "@/lib/inklings";
import { LOOPKINS_BASE } from "@/lib/loopkins";
import { PURRKINS_BASE } from "@/lib/purrkins";
import { WICKLINGS_BASE } from "@/lib/wicklings";
import { openSeaListings } from "@/lib/opensea";

export const gallery = {
  name: "NFT Gallery",
  tagline: "Collections on the wall. One drop at a time.",
  description:
    "NFT Gallery is a house of on-chain collections — each drop keeps its own studio, traits, and launch path. Loopkins is the layered PFP. Afterimages is the 1:1 APNG drop. Inklings is the cartoon-squid PFP GIF drop on Ink. Wicklings is the paper-lantern PFP GIF drop on Arbitrum. Purrkins is the chibi-cat PFP GIF drop on HyperEVM. Hoodkins is the chibi-raccoon PFP GIF drop on Robinhood Chain. BirbNation is the round-borb robin PFP GIF drop on Robinhood Chain. Halloween Shook'ums is the sheet-ghost PFP GIF drop on Abstract. Foxins is the bold-graphic fox PFP GIF drop on Base. Santa Paws is the giving chibi-cat PFP GIF drop on Base. Scribblins is the doodle-critter PFP GIF drop on Base. Groovy Nation is the cartoon musical-note PFP GIF drop on Robinhood Chain. Galleria On Ink is the salon of 50 open-edition 1:1 looping paintings on Ink.",
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
    openseaListings: openSeaListings(collection.opensea, collection.chain.name),
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
    previews: afterimageWorks.slice(0, 6).map((work) => work.image),
    studioHref: null,
    opensea: afterimages.opensea.collection,
    openseaListings: openSeaListings(afterimages.opensea, afterimages.chain.name),
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
    openseaListings: openSeaListings(inklings.opensea, inklings.chain.name),
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
    status: "on the wall" as const,
    kind: "layered-pfp" as const,
    previews: wicklingSamples.map((mint) => mint.image),
    studioHref: "/wicklings/studio" as const,
    opensea: wicklings.opensea.collection,
    openseaListings: openSeaListings(wicklings.opensea, wicklings.chain.name),
  },
  {
    slug: "purrkins",
    href: PURRKINS_BASE,
    name: purrkins.name,
    symbol: purrkins.symbol,
    tagline: purrkins.tagline,
    description: purrkins.description,
    chain: purrkins.chain.name,
    chainId: purrkins.chain.chainId,
    supply: purrkins.supply,
    cover: "/brand/banner-purrkins.png",
    thumb: purrkinSamples[0].image,
    status: "on the wall" as const,
    kind: "layered-pfp" as const,
    previews: purrkinSamples.map((mint) => mint.image),
    studioHref: "/purrkins/studio" as const,
    opensea: purrkins.opensea.collection,
    openseaListings: openSeaListings(purrkins.opensea, purrkins.chain.name),
  },
  {
    slug: "hoodkins",
    href: HOODKINS_BASE,
    name: hoodkins.name,
    symbol: hoodkins.symbol,
    tagline: hoodkins.tagline,
    description: hoodkins.description,
    chain: hoodkins.chain.name,
    chainId: hoodkins.chain.chainId,
    supply: hoodkins.supply,
    cover: "/brand/banner-hoodkins.png",
    thumb: hoodkinSamples[0].image,
    status: "on the wall" as const,
    kind: "layered-pfp" as const,
    previews: hoodkinSamples.map((mint) => mint.image),
    studioHref: "/hoodkins/studio" as const,
    opensea: hoodkins.opensea.collection,
    openseaListings: openSeaListings(hoodkins.opensea, hoodkins.chain.name),
  },
  {
    slug: "birbs",
    href: BIRBS_BASE,
    name: birbs.name,
    symbol: birbs.symbol,
    tagline: birbs.tagline,
    description: birbs.description,
    chain: birbs.chain.name,
    chainId: birbs.chain.chainId,
    supply: birbs.supply,
    cover: "/brand/banner-birbs.png",
    thumb: birbSamples[0].image,
    status: "on the wall" as const,
    kind: "layered-pfp" as const,
    previews: birbSamples.map((mint) => mint.image),
    studioHref: "/birbs/studio" as const,
    opensea: birbs.opensea.collection,
    openseaListings: openSeaListings(birbs.opensea, birbs.chain.name),
  },
  {
    slug: "shookums",
    href: SHOOKUMS_BASE,
    name: shookums.name,
    symbol: shookums.symbol,
    tagline: shookums.tagline,
    description: shookums.description,
    chain: shookums.chain.name,
    chainId: shookums.chain.chainId,
    supply: shookums.supply,
    cover: "/brand/banner-shookums.png",
    thumb: shookumSamples[0].image,
    status: "on the wall" as const,
    kind: "layered-pfp" as const,
    previews: shookumSamples.map((mint) => mint.image),
    studioHref: "/shookums/studio" as const,
    opensea: shookums.opensea.collection,
    openseaListings: openSeaListings(shookums.opensea, shookums.chain.name),
  },
  {
    slug: "foxins",
    href: FOXINS_BASE,
    name: foxins.name,
    symbol: foxins.symbol,
    tagline: foxins.tagline,
    description: foxins.description,
    chain: foxins.chain.name,
    chainId: foxins.chain.chainId,
    supply: foxins.supply,
    cover: "/brand/banner-foxins.png",
    thumb: foxinSamples[0].image,
    status: "on the wall" as const,
    kind: "layered-pfp" as const,
    previews: foxinSamples.map((mint) => mint.image),
    studioHref: "/foxins/studio" as const,
    opensea: foxins.opensea.collection,
    openseaListings: openSeaListings(foxins.opensea, foxins.chain.name),
  },
  {
    slug: "santapaws",
    href: SANTAPAWS_BASE,
    name: santapaws.name,
    symbol: santapaws.symbol,
    tagline: santapaws.tagline,
    description: santapaws.description,
    chain: santapaws.chain.name,
    chainId: santapaws.chain.chainId,
    supply: santapaws.supply,
    cover: "/brand/banner-santapaws.png",
    thumb: santapawSamples[0].image,
    status: "on the wall" as const,
    kind: "layered-pfp" as const,
    previews: santapawSamples.map((mint) => mint.image),
    studioHref: "/santapaws/studio" as const,
    opensea: santapaws.opensea.collection,
    openseaListings: openSeaListings(santapaws.opensea, santapaws.chain.name),
  },
  {
    slug: "scribblins",
    href: SCRIBBLINS_BASE,
    name: scribblins.name,
    symbol: scribblins.symbol,
    tagline: scribblins.tagline,
    description: scribblins.description,
    chain: scribblins.chain.name,
    chainId: scribblins.chain.chainId,
    supply: scribblins.supply,
    cover: "/brand/banner-scribblins.png",
    thumb: scribblinSamples[0].image,
    status: "on the wall" as const,
    kind: "layered-pfp" as const,
    previews: scribblinSamples.map((mint) => mint.image),
    studioHref: "/scribblins/studio" as const,
    opensea: scribblins.opensea.collection,
    openseaListings: openSeaListings(scribblins.opensea, scribblins.chain.name),
  },
  {
    slug: "groovy",
    href: GROOVY_BASE,
    name: groovy.name,
    symbol: groovy.symbol,
    tagline: groovy.tagline,
    description: groovy.description,
    chain: groovy.chain.name,
    chainId: groovy.chain.chainId,
    supply: groovy.supply,
    cover: "/brand/banner-groovy.png",
    thumb: groovySamples[0].image,
    status: "on the wall" as const,
    kind: "layered-pfp" as const,
    previews: groovySamples.map((mint) => mint.image),
    studioHref: "/groovy/studio" as const,
    opensea: groovy.opensea.collection,
    openseaListings: openSeaListings(groovy.opensea, groovy.chain.name),
  },
  {
    slug: "galleria",
    href: GALLERIA_BASE,
    name: galleria.name,
    symbol: galleria.symbol,
    tagline: galleria.tagline,
    description: galleria.description,
    chain: galleria.chain.name,
    chainId: galleria.chain.chainId,
    supply: galleria.supply,
    cover: "/brand/banner-galleria.png",
    thumb: galleriaWorks[0].image,
    status: "new on the wall" as const,
    kind: "open-edition" as const,
    previews: galleriaWorks.slice(0, 6).map((work) => work.image),
    studioHref: null,
    opensea: galleria.opensea.collection,
    openseaListings: openSeaListings(galleria.opensea, galleria.chain.name),
  },
] as const;

export type GalleryProject = (typeof projects)[number];
