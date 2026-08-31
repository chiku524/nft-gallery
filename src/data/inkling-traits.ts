export type InklingTrait = {
  id: string;
  name: string;
  image?: string;
  rarity: number;
};

export type InklingTraitCategory = {
  id: "paper" | "bloom" | "visage" | "gaze" | "mark" | "adorn";
  label: string;
  blurb: string;
  noneLabel?: string;
  traits: InklingTrait[];
};

/** Bump when APNG layers change so the studio does not keep a stale loop. */
export const INKLING_ART_VERSION = "ink-wash-v1";

export const INKLING_FRAMES = 16;
export const INKLING_DURATION_MS = 90;

export function inklingTraitSrc(path?: string) {
  if (!path) return "";
  return `${path}?v=${INKLING_ART_VERSION}`;
}

export const inklingTraitCategories: InklingTraitCategory[] = [
  {
    id: "paper",
    label: "Paper",
    blurb: "Full-canvas ink washes — slow drifts of dye on handmade paper.",
    traits: [
      { id: "indigo", name: "Indigo Night", image: "/inklings-traits/paper/indigo.png", rarity: 16 },
      { id: "peach", name: "Peach Dusk", image: "/inklings-traits/paper/peach.png", rarity: 14 },
      { id: "celadon", name: "Celadon Garden", image: "/inklings-traits/paper/celadon.png", rarity: 14 },
      { id: "charcoal", name: "Charcoal Wash", image: "/inklings-traits/paper/charcoal.png", rarity: 12 },
      { id: "rose", name: "Rose Gold", image: "/inklings-traits/paper/rose.png", rarity: 12 },
      { id: "storm", name: "Storm Grey", image: "/inklings-traits/paper/storm.png", rarity: 12 },
      { id: "wine", name: "Wine Paper", image: "/inklings-traits/paper/wine.png", rarity: 10 },
      { id: "cream", name: "Cream Rice", image: "/inklings-traits/paper/cream.png", rarity: 10 },
    ],
  },
  {
    id: "bloom",
    label: "Bloom",
    blurb: "A soft aura that sits behind the portrait and breathes.",
    noneLabel: "No bloom",
    traits: [
      { id: "violet", name: "Violet Haze", image: "/inklings-traits/bloom/violet.png", rarity: 16 },
      { id: "gold", name: "Gold Wash", image: "/inklings-traits/bloom/gold.png", rarity: 14 },
      { id: "teal", name: "Teal Mist", image: "/inklings-traits/bloom/teal.png", rarity: 14 },
      { id: "coral", name: "Coral Glow", image: "/inklings-traits/bloom/coral.png", rarity: 12 },
      { id: "silver", name: "Silver Veil", image: "/inklings-traits/bloom/silver.png", rarity: 12 },
    ],
  },
  {
    id: "visage",
    label: "Visage",
    blurb: "Eight illustrated faces. Soft edges, ink-wash fur, one shared breathe.",
    traits: [
      { id: "fox", name: "Fox", image: "/inklings-traits/visage/fox.png", rarity: 16 },
      { id: "crane", name: "Crane", image: "/inklings-traits/visage/crane.png", rarity: 14 },
      { id: "koi", name: "Koi", image: "/inklings-traits/visage/koi.png", rarity: 14 },
      { id: "cat", name: "Cat", image: "/inklings-traits/visage/cat.png", rarity: 14 },
      { id: "moth", name: "Moth", image: "/inklings-traits/visage/moth.png", rarity: 12 },
      { id: "moon", name: "Moon", image: "/inklings-traits/visage/moon.png", rarity: 12 },
      { id: "otter", name: "Otter", image: "/inklings-traits/visage/otter.png", rarity: 10 },
      { id: "hare", name: "Hare", image: "/inklings-traits/visage/hare.png", rarity: 8 },
    ],
  },
  {
    id: "gaze",
    label: "Gaze",
    blurb: "Eyes locked to the visage bob, with their own blinks and shine.",
    traits: [
      { id: "bright", name: "Bright", image: "/inklings-traits/gaze/bright.png", rarity: 22 },
      { id: "lidded", name: "Lidded", image: "/inklings-traits/gaze/lidded.png", rarity: 18 },
      { id: "sleepy", name: "Sleepy", image: "/inklings-traits/gaze/sleepy.png", rarity: 16 },
      { id: "wink", name: "Wink", image: "/inklings-traits/gaze/wink.png", rarity: 16 },
      { id: "ember", name: "Ember", image: "/inklings-traits/gaze/ember.png", rarity: 14 },
      { id: "dew", name: "Dew", image: "/inklings-traits/gaze/dew.png", rarity: 14 },
    ],
  },
  {
    id: "mark",
    label: "Mark",
    blurb: "Wet ink on the portrait — splashes, drips, and seals.",
    noneLabel: "Clean face",
    traits: [
      { id: "splash", name: "Ink Splash", image: "/inklings-traits/mark/splash.png", rarity: 16 },
      { id: "drip", name: "Slow Drip", image: "/inklings-traits/mark/drip.png", rarity: 14 },
      { id: "seal", name: "Red Seal", image: "/inklings-traits/mark/seal.png", rarity: 12 },
      { id: "streak", name: "Brush Streak", image: "/inklings-traits/mark/streak.png", rarity: 12 },
    ],
  },
  {
    id: "adorn",
    label: "Adorn",
    blurb: "Hair and ornaments that ride the same bob so they stay glued on.",
    noneLabel: "Bare head",
    traits: [
      { id: "flow", name: "Flow Hair", image: "/inklings-traits/adorn/flow.png", rarity: 16 },
      { id: "bun", name: "Silk Bun", image: "/inklings-traits/adorn/bun.png", rarity: 14 },
      { id: "ribbon", name: "Ink Ribbon", image: "/inklings-traits/adorn/ribbon.png", rarity: 14 },
      { id: "crown", name: "Soft Crown", image: "/inklings-traits/adorn/crown.png", rarity: 12 },
      { id: "hood", name: "Wash Hood", image: "/inklings-traits/adorn/hood.png", rarity: 10 },
    ],
  },
];

export const noneInklingTrait: InklingTrait = { id: "none", name: "None", rarity: 0 };

export function inklingCategoryById(id: InklingTraitCategory["id"]) {
  const category = inklingTraitCategories.find((item) => item.id === id);
  if (!category) throw new Error(`Unknown Inkling trait category: ${id}`);
  return category;
}

export function findInklingTrait(categoryId: InklingTraitCategory["id"], traitId: string) {
  if (traitId === "none") return noneInklingTrait;
  return inklingCategoryById(categoryId).traits.find((trait) => trait.id === traitId);
}

export const defaultInklingSelection = {
  paper: "indigo",
  bloom: "violet",
  visage: "fox",
  gaze: "bright",
  mark: "none",
  adorn: "flow",
} as const;

export type InklingSelection = Record<InklingTraitCategory["id"], string>;

export function randomInklingSelection(): InklingSelection {
  const pick = (category: InklingTraitCategory) => {
    const pool: InklingTrait[] = category.noneLabel
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
    paper: pick(inklingCategoryById("paper")),
    bloom: pick(inklingCategoryById("bloom")),
    visage: pick(inklingCategoryById("visage")),
    gaze: pick(inklingCategoryById("gaze")),
    mark: pick(inklingCategoryById("mark")),
    adorn: pick(inklingCategoryById("adorn")),
  };
}

export function inklingCombinationCount() {
  return inklingTraitCategories.reduce((product, category) => {
    const extra = category.noneLabel ? 1 : 0;
    return product * (category.traits.length + extra);
  }, 1);
}

export function inklingSelectionToLayers(selection: InklingSelection) {
  return (["paper", "bloom", "visage", "gaze", "mark", "adorn"] as const)
    .map((id) => findInklingTrait(id, selection[id]))
    .filter((trait): trait is InklingTrait => Boolean(trait?.image))
    .map((trait) => inklingTraitSrc(trait.image));
}
