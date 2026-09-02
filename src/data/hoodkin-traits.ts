export type HoodkinTrait = {
  id: string;
  name: string;
  image?: string;
  rarity: number;
};

export type HoodkinTraitCategory = {
  id: "pad" | "glow" | "pelt" | "fit" | "mug" | "gear";
  label: string;
  blurb: string;
  noneLabel?: string;
  traits: HoodkinTrait[];
};

/** Bump when APNG layers change so the studio does not keep a stale loop. */
export const HOODKIN_ART_VERSION = "hoodkins-v1";

export const HOODKIN_FRAMES = 12;
export const HOODKIN_DURATION_MS = 80;

export function hoodkinTraitSrc(path?: string) {
  if (!path) return "";
  return `${path}?v=${HOODKIN_ART_VERSION}`;
}

export const hoodkinTraitCategories: HoodkinTraitCategory[] = [
  {
    id: "pad",
    label: "Pad",
    blurb: "Full-canvas loops — ledger desks, blotters, and night tape behind the raccoon.",
    traits: [
      { id: "blush", name: "Blush", image: "/hoodkins-traits/pad/blush.png", rarity: 14 },
      { id: "mist", name: "Mist", image: "/hoodkins-traits/pad/mist.png", rarity: 14 },
      { id: "mint", name: "Mint", image: "/hoodkins-traits/pad/mint.png", rarity: 14 },
      { id: "slate", name: "Slate", image: "/hoodkins-traits/pad/slate.png", rarity: 12 },
      { id: "blotter", name: "Blotter", image: "/hoodkins-traits/pad/blotter.png", rarity: 12 },
      { id: "ledger", name: "Ledger", image: "/hoodkins-traits/pad/ledger.png", rarity: 12 },
      { id: "amber", name: "Amber", image: "/hoodkins-traits/pad/amber.png", rarity: 12 },
      { id: "night", name: "Night Tape", image: "/hoodkins-traits/pad/night.png", rarity: 10 },
    ],
  },
  {
    id: "glow",
    label: "Glow",
    blurb: "A halo around the raccoon — sparkles and dust sit outside the pelt, not under it.",
    noneLabel: "No glow",
    traits: [
      { id: "sparkle", name: "Sparkle", image: "/hoodkins-traits/glow/sparkle.png", rarity: 18 },
      { id: "lime", name: "Lime Halo", image: "/hoodkins-traits/glow/lime.png", rarity: 18 },
      { id: "gold", name: "Gold Dust", image: "/hoodkins-traits/glow/gold.png", rarity: 18 },
      { id: "blush", name: "Blush Bloom", image: "/hoodkins-traits/glow/blush.png", rarity: 18 },
    ],
  },
  {
    id: "pelt",
    label: "Pelt",
    blurb: "Six coats, each with its own bandit mask — silver, rust, ink, snow, honey, moss.",
    traits: [
      { id: "silver", name: "Silver", image: "/hoodkins-traits/pelt/silver.png", rarity: 22 },
      { id: "rust", name: "Rust", image: "/hoodkins-traits/pelt/rust.png", rarity: 18 },
      { id: "ink", name: "Ink", image: "/hoodkins-traits/pelt/ink.png", rarity: 16 },
      { id: "snow", name: "Snow", image: "/hoodkins-traits/pelt/snow.png", rarity: 16 },
      { id: "honey", name: "Honey", image: "/hoodkins-traits/pelt/honey.png", rarity: 14 },
      { id: "moss", name: "Moss", image: "/hoodkins-traits/pelt/moss.png", rarity: 14 },
    ],
  },
  {
    id: "fit",
    label: "Fit",
    blurb: "A tiny cropped bust under a huge head — no sleeves, no paws.",
    noneLabel: "No fit",
    traits: [
      { id: "hoodie", name: "Forest Hoodie", image: "/hoodkins-traits/fit/hoodie.png", rarity: 18 },
      { id: "tee", name: "Blue Tee", image: "/hoodkins-traits/fit/tee.png", rarity: 16 },
      { id: "jacket", name: "Ink Jacket", image: "/hoodkins-traits/fit/jacket.png", rarity: 16 },
      { id: "polo", name: "Cream Polo", image: "/hoodkins-traits/fit/polo.png", rarity: 16 },
      { id: "cardigan", name: "Clay Cardigan", image: "/hoodkins-traits/fit/cardigan.png", rarity: 14 },
    ],
  },
  {
    id: "mug",
    label: "Mug",
    blurb: "The face — blink, wink, smirk — locked to the bob so the eyes stay glued on.",
    traits: [
      { id: "blink", name: "Blink", image: "/hoodkins-traits/mug/blink.png", rarity: 22 },
      { id: "wink", name: "Wink", image: "/hoodkins-traits/mug/wink.png", rarity: 16 },
      { id: "sleepy", name: "Sleepy", image: "/hoodkins-traits/mug/sleepy.png", rarity: 16 },
      { id: "smirk", name: "Smirk", image: "/hoodkins-traits/mug/smirk.png", rarity: 16 },
      { id: "spark", name: "Spark", image: "/hoodkins-traits/mug/spark.png", rarity: 16 },
      { id: "heart", name: "Heart", image: "/hoodkins-traits/mug/heart.png", rarity: 14 },
      { id: "coin", name: "Coin", image: "/hoodkins-traits/mug/coin.png", rarity: 14 },
      { id: "wide", name: "Wide", image: "/hoodkins-traits/mug/wide.png", rarity: 14 },
    ],
  },
  {
    id: "gear",
    label: "Gear",
    blurb: "Hats, shades, phones, and handhelds on the front of the stack.",
    noneLabel: "None",
    traits: [
      { id: "beanie", name: "Beanie", image: "/hoodkins-traits/gear/beanie.png", rarity: 14 },
      { id: "cap", name: "Back Cap", image: "/hoodkins-traits/gear/cap.png", rarity: 14 },
      { id: "bucket", name: "Bucket Hat", image: "/hoodkins-traits/gear/bucket.png", rarity: 12 },
      { id: "shades", name: "Shades", image: "/hoodkins-traits/gear/shades.png", rarity: 12 },
      { id: "phones", name: "Headphones", image: "/hoodkins-traits/gear/phones.png", rarity: 12 },
      { id: "phone", name: "Phone", image: "/hoodkins-traits/gear/phone.png", rarity: 10 },
      { id: "coffee", name: "Coffee", image: "/hoodkins-traits/gear/coffee.png", rarity: 10 },
    ],
  },
];

export const noneHoodkinTrait: HoodkinTrait = { id: "none", name: "None", rarity: 0 };

export function hoodkinCategoryById(id: HoodkinTraitCategory["id"]) {
  const category = hoodkinTraitCategories.find((item) => item.id === id);
  if (!category) throw new Error(`Unknown Hoodkin trait category: ${id}`);
  return category;
}

export function findHoodkinTrait(categoryId: HoodkinTraitCategory["id"], traitId: string) {
  if (traitId === "none") return noneHoodkinTrait;
  return hoodkinCategoryById(categoryId).traits.find((trait) => trait.id === traitId);
}

export const defaultHoodkinSelection = {
  pad: "ledger",
  glow: "lime",
  pelt: "silver",
  fit: "hoodie",
  mug: "blink",
  gear: "phones",
} as const;

export type HoodkinSelection = Record<HoodkinTraitCategory["id"], string>;

export function randomHoodkinSelection(): HoodkinSelection {
  const pick = (category: HoodkinTraitCategory) => {
    const pool: HoodkinTrait[] = category.noneLabel
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
    pad: pick(hoodkinCategoryById("pad")),
    glow: pick(hoodkinCategoryById("glow")),
    pelt: pick(hoodkinCategoryById("pelt")),
    fit: pick(hoodkinCategoryById("fit")),
    mug: pick(hoodkinCategoryById("mug")),
    gear: pick(hoodkinCategoryById("gear")),
  };
}

export function hoodkinCombinationCount() {
  return hoodkinTraitCategories.reduce((product, category) => {
    const extra = category.noneLabel ? 1 : 0;
    return product * (category.traits.length + extra);
  }, 1);
}

export function hoodkinSelectionToLayers(selection: HoodkinSelection) {
  return (["pad", "glow", "pelt", "fit", "mug", "gear"] as const)
    .map((id) => findHoodkinTrait(id, selection[id]))
    .filter((trait): trait is HoodkinTrait => Boolean(trait?.image))
    .map((trait) => hoodkinTraitSrc(trait.image));
}
