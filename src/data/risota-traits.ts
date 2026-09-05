export type RisotaTrait = {
  id: string;
  name: string;
  image?: string;
  rarity: number;
};

export type RisotaTraitCategory = {
  id: "stock" | "screen" | "figure" | "pass" | "knockout" | "slug" | "mark";
  label: string;
  blurb: string;
  noneLabel?: string;
  traits: RisotaTrait[];
};

/** Bump when APNG layers change so the studio does not keep a stale loop. */
export const RISOTA_ART_VERSION = "risota-v1";

export const RISOTA_FRAMES = 12;
export const RISOTA_DURATION_MS = 90;

export function risotaTraitSrc(path?: string) {
  if (!path) return "";
  return `${path}?v=${RISOTA_ART_VERSION}`;
}

export const risotaTraitCategories: RisotaTraitCategory[] = [
  {
    id: "stock",
    label: "Stock",
    blurb: "Uncoated paper — cream, blush, mint, kraft, ice, lemon, fog, recycled.",
    traits: [
      { id: "cream", name: "Cream Sheet", image: "/risota-traits/stock/cream.png", rarity: 18 },
      { id: "blush", name: "Blush Sheet", image: "/risota-traits/stock/blush.png", rarity: 14 },
      { id: "mint", name: "Mint Sheet", image: "/risota-traits/stock/mint.png", rarity: 12 },
      { id: "kraft", name: "Kraft Sheet", image: "/risota-traits/stock/kraft.png", rarity: 12 },
      { id: "ice", name: "Ice Sheet", image: "/risota-traits/stock/ice.png", rarity: 12 },
      { id: "lemon", name: "Lemon Sheet", image: "/risota-traits/stock/lemon.png", rarity: 12 },
      { id: "fog", name: "Fog Sheet", image: "/risota-traits/stock/fog.png", rarity: 10 },
      { id: "recyc", name: "Recycled Sheet", image: "/risota-traits/stock/recyc.png", rarity: 10 },
    ],
  },
  {
    id: "screen",
    label: "Screen",
    blurb: "Halftone hanging on the sheet — rosa, aqua, gild, navy, ember — or bare stock.",
    noneLabel: "Bare Stock",
    traits: [
      { id: "rosa", name: "Rosa Mesh", image: "/risota-traits/screen/rosa.png", rarity: 18 },
      { id: "aqua", name: "Aqua Mesh", image: "/risota-traits/screen/aqua.png", rarity: 16 },
      { id: "gild", name: "Gild Mist", image: "/risota-traits/screen/gild.png", rarity: 14 },
      { id: "navy", name: "Navy Mesh", image: "/risota-traits/screen/navy.png", rarity: 12 },
      { id: "ember", name: "Ember Dust", image: "/risota-traits/screen/ember.png", rarity: 10 },
    ],
  },
  {
    id: "figure",
    label: "Figure",
    blurb: "The dancer. Eight spot-ink bodies: kick, twirl, pop, sway, hop, glide, stomp, reach.",
    traits: [
      { id: "kick", name: "Kick", image: "/risota-traits/figure/kick.png", rarity: 18 },
      { id: "twirl", name: "Twirl", image: "/risota-traits/figure/twirl.png", rarity: 16 },
      { id: "pop", name: "Pop", image: "/risota-traits/figure/pop.png", rarity: 14 },
      { id: "sway", name: "Sway", image: "/risota-traits/figure/sway.png", rarity: 14 },
      { id: "hop", name: "Hop", image: "/risota-traits/figure/hop.png", rarity: 12 },
      { id: "glide", name: "Glide", image: "/risota-traits/figure/glide.png", rarity: 10 },
      { id: "stomp", name: "Stomp", image: "/risota-traits/figure/stomp.png", rarity: 8 },
      { id: "reach", name: "Reach", image: "/risota-traits/figure/reach.png", rarity: 8 },
    ],
  },
  {
    id: "pass",
    label: "Pass",
    blurb: "Second ink drum — smock, bib, sash, cuff, flare, wrap — sliding out of register.",
    noneLabel: "Open Plate",
    traits: [
      { id: "smock", name: "Smock Pass", image: "/risota-traits/pass/smock.png", rarity: 16 },
      { id: "bib", name: "Bib Pass", image: "/risota-traits/pass/bib.png", rarity: 14 },
      { id: "sash", name: "Sash Pass", image: "/risota-traits/pass/sash.png", rarity: 14 },
      { id: "cuff", name: "Cuff Pass", image: "/risota-traits/pass/cuff.png", rarity: 12 },
      { id: "flare", name: "Flare Pass", image: "/risota-traits/pass/flare.png", rarity: 12 },
      { id: "wrap", name: "Wrap Pass", image: "/risota-traits/pass/wrap.png", rarity: 10 },
    ],
  },
  {
    id: "knockout",
    label: "Knockout",
    blurb: "Face plate punched as a dark drum — dots, grin, wink, shout, focus, calm.",
    traits: [
      { id: "dots", name: "Dots", image: "/risota-traits/knockout/dots.png", rarity: 22 },
      { id: "grin", name: "Grin", image: "/risota-traits/knockout/grin.png", rarity: 18 },
      { id: "wink", name: "Wink", image: "/risota-traits/knockout/wink.png", rarity: 16 },
      { id: "shout", name: "Shout", image: "/risota-traits/knockout/shout.png", rarity: 16 },
      { id: "focus", name: "Focus", image: "/risota-traits/knockout/focus.png", rarity: 14 },
      { id: "calm", name: "Calm", image: "/risota-traits/knockout/calm.png", rarity: 14 },
    ],
  },
  {
    id: "slug",
    label: "Slug",
    blurb: "A third blot on the crown or throat — kerchief, bow, burst, brim — or a clear slug.",
    noneLabel: "Clear Slug",
    traits: [
      { id: "kerchief", name: "Kerchief", image: "/risota-traits/slug/kerchief.png", rarity: 18 },
      { id: "bow", name: "Bow", image: "/risota-traits/slug/bow.png", rarity: 16 },
      { id: "burst", name: "Burst", image: "/risota-traits/slug/burst.png", rarity: 14 },
      { id: "brim", name: "Brim", image: "/risota-traits/slug/brim.png", rarity: 12 },
    ],
  },
  {
    id: "mark",
    label: "Mark",
    blurb: "Press ephemera — registration ticks, splash, stars, crop marks — or a clean gripper.",
    noneLabel: "Clean Grip",
    traits: [
      { id: "ticks", name: "Reg Ticks", image: "/risota-traits/mark/ticks.png", rarity: 18 },
      { id: "splash", name: "Ink Splash", image: "/risota-traits/mark/splash.png", rarity: 16 },
      { id: "stars", name: "Star Burst", image: "/risota-traits/mark/stars.png", rarity: 14 },
      { id: "crop", name: "Crop Marks", image: "/risota-traits/mark/crop.png", rarity: 12 },
    ],
  }
];

export const noneRisotaTrait: RisotaTrait = { id: "none", name: "None", rarity: 0 };

export function risotaCategoryById(id: RisotaTraitCategory["id"]) {
  const category = risotaTraitCategories.find((item) => item.id === id);
  if (!category) throw new Error(`Unknown Risota trait category: ${id}`);
  return category;
}

export function findRisotaTrait(categoryId: RisotaTraitCategory["id"], traitId: string) {
  if (traitId === "none") return noneRisotaTrait;
  return risotaCategoryById(categoryId).traits.find((trait) => trait.id === traitId);
}

export const defaultRisotaSelection = {
  stock: "cream",
  screen: "rosa",
  figure: "kick",
  pass: "smock",
  knockout: "grin",
  slug: "kerchief",
  mark: "ticks",
} as const;

export type RisotaSelection = Record<RisotaTraitCategory["id"], string>;

export function randomRisotaSelection(): RisotaSelection {
  const pick = (category: RisotaTraitCategory) => {
    const pool: RisotaTrait[] = category.noneLabel
      ? [{ id: "none", name: category.noneLabel, rarity: 22 }, ...category.traits]
      : category.traits;
    const total = pool.reduce((sum, trait) => sum + Math.max(trait.rarity, 1), 0);
    let roll = Math.random() * total;
    for (const trait of pool) {
      roll -= Math.max(trait.rarity, 1);
      if (roll <= 0) return trait.id;
    }
    return pool[0].id;
  };

  return {
    stock: pick(risotaCategoryById("stock")),
    screen: pick(risotaCategoryById("screen")),
    figure: pick(risotaCategoryById("figure")),
    pass: pick(risotaCategoryById("pass")),
    knockout: pick(risotaCategoryById("knockout")),
    slug: pick(risotaCategoryById("slug")),
    mark: pick(risotaCategoryById("mark")),
  };
}

export function risotaCombinationCount() {
  return risotaTraitCategories.reduce((product, category) => {
    const extra = category.noneLabel ? 1 : 0;
    return product * (category.traits.length + extra);
  }, 1);
}

export function risotaSelectionToLayers(selection: RisotaSelection) {
  return (["stock", "screen", "figure", "pass", "knockout", "slug", "mark"] as const)
    .map((id) => findRisotaTrait(id, selection[id]))
    .filter((trait): trait is RisotaTrait => Boolean(trait?.image))
    .map((trait) => risotaTraitSrc(trait.image));
}
