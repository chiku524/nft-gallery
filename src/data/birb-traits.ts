export type BirbTrait = {
  id: string;
  name: string;
  image?: string;
  rarity: number;
};

export type BirbTraitCategory = {
  id: "field" | "plumage" | "mug" | "accent";
  label: string;
  blurb: string;
  noneLabel?: string;
  traits: BirbTrait[];
};

/** Bump when APNG layers change so the studio does not keep a stale loop. */
export const BIRB_ART_VERSION = "birbnation-v1";

export const BIRB_FRAMES = 12;
export const BIRB_DURATION_MS = 90;

export function birbTraitSrc(path?: string) {
  if (!path) return "";
  return `${path}?v=${BIRB_ART_VERSION}`;
}

export const birbTraitCategories: BirbTraitCategory[] = [
  {
    id: "field",
    label: "Field",
    blurb: "A flat sticker ground — white, sky, forest, space. No desks.",
    traits: [
      { id: "white", name: "White", image: "/birbs-traits/field/white.png", rarity: 16 },
      { id: "cream", name: "Cream", image: "/birbs-traits/field/cream.png", rarity: 14 },
      { id: "blush", name: "Blush", image: "/birbs-traits/field/blush.png", rarity: 13 },
      { id: "mint", name: "Mint", image: "/birbs-traits/field/mint.png", rarity: 13 },
      { id: "sky", name: "Sky", image: "/birbs-traits/field/sky.png", rarity: 14 },
      { id: "peach", name: "Peach", image: "/birbs-traits/field/peach.png", rarity: 12 },
      { id: "dusk", name: "Dusk", image: "/birbs-traits/field/dusk.png", rarity: 10 },
      { id: "clover", name: "Forest", image: "/birbs-traits/field/clover.png", rarity: 10 },
      { id: "space", name: "Space", image: "/birbs-traits/field/space.png", rarity: 5 },
    ],
  },
  {
    id: "plumage",
    label: "Plumage",
    blurb: "The sphere — brown, blue, pink, gold, rainbow. Wings and beak stay tiny.",
    traits: [
      { id: "classic", name: "Brown", image: "/birbs-traits/plumage/classic.png", rarity: 25 },
      { id: "blue", name: "Blue", image: "/birbs-traits/plumage/blue.png", rarity: 18 },
      { id: "berry", name: "Pink", image: "/birbs-traits/plumage/berry.png", rarity: 14 },
      { id: "moss", name: "Green", image: "/birbs-traits/plumage/moss.png", rarity: 14 },
      { id: "gold", name: "Gold", image: "/birbs-traits/plumage/gold.png", rarity: 10 },
      { id: "snow", name: "Snow", image: "/birbs-traits/plumage/snow.png", rarity: 8 },
      { id: "dusk", name: "Dusk", image: "/birbs-traits/plumage/dusk.png", rarity: 6 },
      { id: "frost", name: "Frost", image: "/birbs-traits/plumage/frost.png", rarity: 5 },
      { id: "rainbow", name: "Rainbow", image: "/birbs-traits/plumage/rainbow.png", rarity: 4 },
      { id: "ink", name: "Void", image: "/birbs-traits/plumage/ink.png", rarity: 3 },
    ],
  },
  {
    id: "mug",
    label: "Mug",
    blurb: "Solid glossy black eyes — two catchlights, cream brow tufts, a pink blep.",
    traits: [
      { id: "blep", name: "Blep", image: "/birbs-traits/mug/blep.png", rarity: 22 },
      { id: "blink", name: "Normal", image: "/birbs-traits/mug/blink.png", rarity: 16 },
      { id: "spark", name: "Sparkly", image: "/birbs-traits/mug/spark.png", rarity: 14 },
      { id: "sleepy", name: "Sleepy", image: "/birbs-traits/mug/sleepy.png", rarity: 12 },
      { id: "wink", name: "Wink", image: "/birbs-traits/mug/wink.png", rarity: 10 },
      { id: "wide", name: "Wide", image: "/birbs-traits/mug/wide.png", rarity: 8 },
      { id: "angry", name: "Angry", image: "/birbs-traits/mug/angry.png", rarity: 7 },
      { id: "sad", name: "Sad", image: "/birbs-traits/mug/sad.png", rarity: 5 },
      { id: "starry", name: "Starry", image: "/birbs-traits/mug/starry.png", rarity: 4 },
      { id: "heart", name: "Heart", image: "/birbs-traits/mug/heart.png", rarity: 3 },
    ],
  },
  {
    id: "accent",
    label: "Accent",
    blurb: "A tiny extra — hat, crown, flower, worm. Companions live here too.",
    noneLabel: "None",
    traits: [
      { id: "bandana", name: "Bandana", image: "/birbs-traits/accent/bandana.png", rarity: 12 },
      { id: "flower", name: "Flower", image: "/birbs-traits/accent/flower.png", rarity: 10 },
      { id: "leaf", name: "Leaf", image: "/birbs-traits/accent/leaf.png", rarity: 9 },
      { id: "berry", name: "Berry", image: "/birbs-traits/accent/berry.png", rarity: 8 },
      { id: "hat", name: "Hat", image: "/birbs-traits/accent/hat.png", rarity: 7 },
      { id: "worm", name: "Worm", image: "/birbs-traits/accent/worm.png", rarity: 6 },
      { id: "bow", name: "Bow", image: "/birbs-traits/accent/bow.png", rarity: 5 },
      { id: "crown", name: "Crown", image: "/birbs-traits/accent/crown.png", rarity: 4 },
    ],
  },
];

export const noneBirbTrait: BirbTrait = { id: "none", name: "None", rarity: 0 };

export function birbCategoryById(id: BirbTraitCategory["id"]) {
  const category = birbTraitCategories.find((item) => item.id === id);
  if (!category) throw new Error(`Unknown Birb trait category: ${id}`);
  return category;
}

export function findBirbTrait(categoryId: BirbTraitCategory["id"], traitId: string) {
  if (traitId === "none") return noneBirbTrait;
  return birbCategoryById(categoryId).traits.find((trait) => trait.id === traitId);
}

export const defaultBirbSelection = {
  field: "white",
  plumage: "classic",
  mug: "blep",
  accent: "none",
} as const;

export type BirbSelection = Record<BirbTraitCategory["id"], string>;

export function randomBirbSelection(): BirbSelection {
  const pick = (category: BirbTraitCategory) => {
    const pool: BirbTrait[] = category.noneLabel
      ? [{ id: "none", name: category.noneLabel, rarity: 36 }, ...category.traits]
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
    field: pick(birbCategoryById("field")),
    plumage: pick(birbCategoryById("plumage")),
    mug: pick(birbCategoryById("mug")),
    accent: pick(birbCategoryById("accent")),
  };
}

export function birbCombinationCount() {
  return birbTraitCategories.reduce((product, category) => {
    const extra = category.noneLabel ? 1 : 0;
    return product * (category.traits.length + extra);
  }, 1);
}

export function birbSelectionToLayers(selection: BirbSelection) {
  return (["field", "plumage", "mug", "accent"] as const)
    .map((id) => findBirbTrait(id, selection[id]))
    .filter((trait): trait is BirbTrait => Boolean(trait?.image))
    .map((trait) => birbTraitSrc(trait.image));
}
