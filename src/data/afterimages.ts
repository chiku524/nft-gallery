export const afterimages = {
  name: "Afterimages",
  symbol: "AFTER",
  tagline: "One-of-one APNG paintings that never freeze.",
  description:
    "Afterimages is a 12-piece OpenSea drop of unique looping paintings. Each token is a finished APNG — not stacked traits, not a generative shuffle. One canvas, one clock, one artwork.",
  supply: 12,
  mintPriceEth: "0.08",
  frames: 16,
  frameDurationMs: 100,
  canvas: 640,
  edition: "1/1" as const,
  chain: {
    name: "Robinhood Chain",
    chainId: 4663,
    chainIdHex: "0x1237",
    currency: "ETH",
    rpcUrl: "https://rpc.mainnet.chain.robinhood.com",
    explorer: "https://robinhoodchain.blockscout.com",
    docs: "https://docs.robinhood.com/chain/connecting/",
  },
  opensea: {
    chainSlug: "robinhood",
    blog: "https://opensea.io/blog/articles/robinhood-chain-is-live-on-opensea",
    explore: "https://opensea.io",
    metadataGuide: "https://support.opensea.io/en/articles/8867060-preparing-metadata-for-your-drop",
  },
} as const;

export type AfterimagesCollection = typeof afterimages;

export type AfterimageWork = {
  id: number;
  slug: string;
  title: string;
  image: string;
  description: string;
  attributes: { trait_type: string; value: string }[];
};

export const afterimageWorks: AfterimageWork[] = [
  {
    id: 1,
    slug: "moonrise",
    title: "Moonrise Over Still Water",
    image: "/afterimages/1.png",
    description: "A silver moon climbs a indigo inlet. The water holds the climb a beat later.",
    attributes: [
      { trait_type: "Series", value: "Afterimages" },
      { trait_type: "Palette", value: "Indigo Silver" },
      { trait_type: "Motion", value: "Rise" },
      { trait_type: "Season", value: "Night" },
      { trait_type: "Medium", value: "APNG" },
    ],
  },
  {
    id: 2,
    slug: "stained-glass",
    title: "Stained Glass Breath",
    image: "/afterimages/2.png",
    description: "Jewel panes inhale gold. Lead lines hold while the colors keep changing their mind.",
    attributes: [
      { trait_type: "Series", value: "Afterimages" },
      { trait_type: "Palette", value: "Jewel Gold" },
      { trait_type: "Motion", value: "Pulse" },
      { trait_type: "Season", value: "Dusk" },
      { trait_type: "Medium", value: "APNG" },
    ],
  },
  {
    id: 3,
    slug: "petal-storm",
    title: "Petal Storm",
    image: "/afterimages/3.png",
    description: "Blush petals fall through cream light and never quite land.",
    attributes: [
      { trait_type: "Series", value: "Afterimages" },
      { trait_type: "Palette", value: "Blush Cream" },
      { trait_type: "Motion", value: "Fall" },
      { trait_type: "Season", value: "Spring" },
      { trait_type: "Medium", value: "APNG" },
    ],
  },
  {
    id: 4,
    slug: "lighthouse",
    title: "Lighthouse Sweep",
    image: "/afterimages/4.png",
    description: "An amber beam turns over navy water. Foam remembers the last pass.",
    attributes: [
      { trait_type: "Series", value: "Afterimages" },
      { trait_type: "Palette", value: "Navy Amber" },
      { trait_type: "Motion", value: "Sweep" },
      { trait_type: "Season", value: "Night" },
      { trait_type: "Medium", value: "APNG" },
    ],
  },
  {
    id: 5,
    slug: "coral-bloom",
    title: "Coral Bloom",
    image: "/afterimages/5.png",
    description: "Anemones open under teal water. A gold fish threads the bloom.",
    attributes: [
      { trait_type: "Series", value: "Afterimages" },
      { trait_type: "Palette", value: "Teal Salmon" },
      { trait_type: "Motion", value: "Bloom" },
      { trait_type: "Season", value: "Tide" },
      { trait_type: "Medium", value: "APNG" },
    ],
  },
  {
    id: 6,
    slug: "neon-dusk",
    title: "Neon Dusk",
    image: "/afterimages/6.png",
    description: "A city silhouette holds still while magenta and cyan signs keep arguing.",
    attributes: [
      { trait_type: "Series", value: "Afterimages" },
      { trait_type: "Palette", value: "Magenta Cyan" },
      { trait_type: "Motion", value: "Flicker" },
      { trait_type: "Season", value: "Dusk" },
      { trait_type: "Medium", value: "APNG" },
    ],
  },
  {
    id: 7,
    slug: "firefly-grove",
    title: "Firefly Grove",
    image: "/afterimages/7.png",
    description: "Dark pines, a wet floor, and gold specks that refuse a single path.",
    attributes: [
      { trait_type: "Series", value: "Afterimages" },
      { trait_type: "Palette", value: "Forest Gold" },
      { trait_type: "Motion", value: "Drift" },
      { trait_type: "Season", value: "Night" },
      { trait_type: "Medium", value: "APNG" },
    ],
  },
  {
    id: 8,
    slug: "corona",
    title: "Corona",
    image: "/afterimages/8.png",
    description: "A black disc covers the sun. The flare keeps finding new edges.",
    attributes: [
      { trait_type: "Series", value: "Afterimages" },
      { trait_type: "Palette", value: "Black Gold" },
      { trait_type: "Motion", value: "Flare" },
      { trait_type: "Season", value: "Eclipse" },
      { trait_type: "Medium", value: "APNG" },
    ],
  },
  {
    id: 9,
    slug: "koi-mirror",
    title: "Koi Mirror",
    image: "/afterimages/9.png",
    description: "Orange and white koi turn under a jade surface. The pond is the painting.",
    attributes: [
      { trait_type: "Series", value: "Afterimages" },
      { trait_type: "Palette", value: "Jade Orange" },
      { trait_type: "Motion", value: "Orbit" },
      { trait_type: "Season", value: "Garden" },
      { trait_type: "Medium", value: "APNG" },
    ],
  },
  {
    id: 10,
    slug: "heat-shimmer",
    title: "Heat Shimmer",
    image: "/afterimages/10.png",
    description: "Dunes wait. The air above them will not.",
    attributes: [
      { trait_type: "Series", value: "Afterimages" },
      { trait_type: "Palette", value: "Ochre Sky" },
      { trait_type: "Motion", value: "Shimmer" },
      { trait_type: "Season", value: "Noon" },
      { trait_type: "Medium", value: "APNG" },
    ],
  },
  {
    id: 11,
    slug: "ice-fracture",
    title: "Ice Fracture",
    image: "/afterimages/11.png",
    description: "A frozen lake splits. Light travels the crack before the ice does.",
    attributes: [
      { trait_type: "Series", value: "Afterimages" },
      { trait_type: "Palette", value: "Ice Navy" },
      { trait_type: "Motion", value: "Crack" },
      { trait_type: "Season", value: "Winter" },
      { trait_type: "Medium", value: "APNG" },
    ],
  },
  {
    id: 12,
    slug: "nave-light",
    title: "Nave Light",
    image: "/afterimages/12.png",
    description: "Stone holds. A honey shaft of dust keeps rewriting the aisle.",
    attributes: [
      { trait_type: "Series", value: "Afterimages" },
      { trait_type: "Palette", value: "Stone Honey" },
      { trait_type: "Motion", value: "Motes" },
      { trait_type: "Season", value: "Afternoon" },
      { trait_type: "Medium", value: "APNG" },
    ],
  },
];

export function getAfterimageWork(id: number): AfterimageWork | undefined {
  return afterimageWorks.find((work) => work.id === id);
}
