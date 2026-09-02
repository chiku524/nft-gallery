export type PurrkinTrait = {
  id: string;
  name: string;
  image?: string;
  rarity: number;
};

export type PurrkinTraitCategory = {
  id: "pad" | "glow" | "pelt" | "fit" | "mug" | "gear";
  label: string;
  blurb: string;
  noneLabel?: string;
  traits: PurrkinTrait[];
};

/** Bump when APNG layers change so the studio does not keep a stale loop. */
export const PURRKIN_ART_VERSION = "purrkins-v2";

export const PURRKIN_FRAMES = 12;
export const PURRKIN_DURATION_MS = 80;

export function purrkinTraitSrc(path?: string) {
  if (!path) return "";
  return `${path}?v=${PURRKIN_ART_VERSION}`;
}

export const purrkinTraitCategories: PurrkinTraitCategory[] = [
  {
    id: "pad",
    label: "Pad",
    blurb: "Full-canvas loops — pastel desks and night desks behind the cat.",
    traits: [
      { id: "blush", name: "Blush", image: "/purrkins-traits/pad/blush.png", rarity: 14 },
      { id: "lilac", name: "Lilac", image: "/purrkins-traits/pad/lilac.png", rarity: 14 },
      { id: "mint", name: "Mint", image: "/purrkins-traits/pad/mint.png", rarity: 14 },
      { id: "slate", name: "Slate", image: "/purrkins-traits/pad/slate.png", rarity: 12 },
      { id: "cream", name: "Cream", image: "/purrkins-traits/pad/cream.png", rarity: 12 },
      { id: "teal", name: "Teal Desk", image: "/purrkins-traits/pad/teal.png", rarity: 12 },
      { id: "peach", name: "Peach", image: "/purrkins-traits/pad/peach.png", rarity: 12 },
      { id: "night", name: "Night Desk", image: "/purrkins-traits/pad/night.png", rarity: 10 },
    ],
  },
  {
    id: "glow",
    label: "Glow",
    blurb: "Light that sits behind the cat and pulses on the shared clock.",
    noneLabel: "No glow",
    traits: [
      { id: "sparkle", name: "Sparkle", image: "/purrkins-traits/glow/sparkle.png", rarity: 18 },
      { id: "mint", name: "Mint Halo", image: "/purrkins-traits/glow/mint.png", rarity: 18 },
      { id: "gold", name: "Gold Dust", image: "/purrkins-traits/glow/gold.png", rarity: 18 },
      { id: "blush", name: "Blush Bloom", image: "/purrkins-traits/glow/blush.png", rarity: 18 },
    ],
  },
  {
    id: "pelt",
    label: "Pelt",
    blurb: "Six coats. Cream, ginger, soot, mist, calico, and matcha — ears twitch, eyes blink.",
    traits: [
      { id: "cream", name: "Cream", image: "/purrkins-traits/pelt/cream.png", rarity: 22 },
      { id: "ginger", name: "Ginger", image: "/purrkins-traits/pelt/ginger.png", rarity: 18 },
      { id: "soot", name: "Soot", image: "/purrkins-traits/pelt/soot.png", rarity: 16 },
      { id: "mist", name: "Mist", image: "/purrkins-traits/pelt/mist.png", rarity: 16 },
      { id: "calico", name: "Calico", image: "/purrkins-traits/pelt/calico.png", rarity: 14 },
      { id: "matcha", name: "Matcha", image: "/purrkins-traits/pelt/matcha.png", rarity: 14 },
    ],
  },
  {
    id: "fit",
    label: "Fit",
    blurb: "Streetwear as one cropped bust — no sleeves, no paws.",
    noneLabel: "No fit",
    traits: [
      { id: "hoodie", name: "Forest Hoodie", image: "/purrkins-traits/fit/hoodie.png", rarity: 18 },
      { id: "tee", name: "Blue Tee", image: "/purrkins-traits/fit/tee.png", rarity: 16 },
      { id: "jacket", name: "Ink Jacket", image: "/purrkins-traits/fit/jacket.png", rarity: 16 },
      { id: "polo", name: "Cream Polo", image: "/purrkins-traits/fit/polo.png", rarity: 16 },
      { id: "cardigan", name: "Clay Cardigan", image: "/purrkins-traits/fit/cardigan.png", rarity: 14 },
    ],
  },
  {
    id: "mug",
    label: "Mug",
    blurb: "The face — blink, wink, grin — locked to the bob so the eyes stay glued on.",
    traits: [
      { id: "blink", name: "Blink", image: "/purrkins-traits/mug/blink.png", rarity: 22 },
      { id: "wink", name: "Wink", image: "/purrkins-traits/mug/wink.png", rarity: 16 },
      { id: "sleepy", name: "Sleepy", image: "/purrkins-traits/mug/sleepy.png", rarity: 16 },
      { id: "grin", name: "Grin", image: "/purrkins-traits/mug/grin.png", rarity: 16 },
      { id: "spark", name: "Spark", image: "/purrkins-traits/mug/spark.png", rarity: 16 },
      { id: "heart", name: "Heart", image: "/purrkins-traits/mug/heart.png", rarity: 14 },
      { id: "wide", name: "Wide", image: "/purrkins-traits/mug/wide.png", rarity: 14 },
    ],
  },
  {
    id: "gear",
    label: "Gear",
    blurb: "Hats, shades, phones, and handhelds on the front of the stack.",
    noneLabel: "None",
    traits: [
      { id: "beanie", name: "Beanie", image: "/purrkins-traits/gear/beanie.png", rarity: 14 },
      { id: "cap", name: "Back Cap", image: "/purrkins-traits/gear/cap.png", rarity: 14 },
      { id: "bucket", name: "Bucket Hat", image: "/purrkins-traits/gear/bucket.png", rarity: 12 },
      { id: "shades", name: "Shades", image: "/purrkins-traits/gear/shades.png", rarity: 12 },
      { id: "phones", name: "Headphones", image: "/purrkins-traits/gear/phones.png", rarity: 12 },
      { id: "phone", name: "Phone", image: "/purrkins-traits/gear/phone.png", rarity: 10 },
      { id: "coffee", name: "Coffee", image: "/purrkins-traits/gear/coffee.png", rarity: 10 },
    ],
  },
];

export const nonePurrkinTrait: PurrkinTrait = { id: "none", name: "None", rarity: 0 };

export function purrkinCategoryById(id: PurrkinTraitCategory["id"]) {
  const category = purrkinTraitCategories.find((item) => item.id === id);
  if (!category) throw new Error(`Unknown Purrkin trait category: ${id}`);
  return category;
}

export function findPurrkinTrait(categoryId: PurrkinTraitCategory["id"], traitId: string) {
  if (traitId === "none") return nonePurrkinTrait;
  return purrkinCategoryById(categoryId).traits.find((trait) => trait.id === traitId);
}

export const defaultPurrkinSelection = {
  pad: "teal",
  glow: "mint",
  pelt: "cream",
  fit: "hoodie",
  mug: "blink",
  gear: "phones",
} as const;

export type PurrkinSelection = Record<PurrkinTraitCategory["id"], string>;

export function randomPurrkinSelection(): PurrkinSelection {
  const pick = (category: PurrkinTraitCategory) => {
    const pool: PurrkinTrait[] = category.noneLabel
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
    pad: pick(purrkinCategoryById("pad")),
    glow: pick(purrkinCategoryById("glow")),
    pelt: pick(purrkinCategoryById("pelt")),
    fit: pick(purrkinCategoryById("fit")),
    mug: pick(purrkinCategoryById("mug")),
    gear: pick(purrkinCategoryById("gear")),
  };
}

export function purrkinCombinationCount() {
  return purrkinTraitCategories.reduce((product, category) => {
    const extra = category.noneLabel ? 1 : 0;
    return product * (category.traits.length + extra);
  }, 1);
}

export function purrkinSelectionToLayers(selection: PurrkinSelection) {
  return (["pad", "glow", "pelt", "fit", "mug", "gear"] as const)
    .map((id) => findPurrkinTrait(id, selection[id]))
    .filter((trait): trait is PurrkinTrait => Boolean(trait?.image))
    .map((trait) => purrkinTraitSrc(trait.image));
}
