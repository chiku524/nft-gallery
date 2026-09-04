export type ScribblinTrait = {
  id: string;
  name: string;
  image?: string;
  rarity: number;
};

export type ScribblinTraitCategory = {
  id: "field" | "body" | "mug" | "hat" | "wrap" | "charm";
  label: string;
  blurb: string;
  noneLabel?: string;
  traits: ScribblinTrait[];
};

/** Bump when APNG layers change so the studio does not keep a stale loop. */
export const SCRIBBLIN_ART_VERSION = "scribblins-v1";

export const SCRIBBLIN_FRAMES = 12;
export const SCRIBBLIN_DURATION_MS = 90;

export function scribblinTraitSrc(path?: string) {
  if (!path) return "";
  return `${path}?v=${SCRIBBLIN_ART_VERSION}`;
}

export const scribblinTraitCategories: ScribblinTraitCategory[] = [
  {
    id: "field",
    label: "Field",
    blurb: "A warm paper wash — cream, sky, clay, butter. The halo stays put.",
    traits: [
      { id: "cream", name: "Cream", image: "/scribblins-traits/field/cream.png", rarity: 32 },
      { id: "sky", name: "Sky", image: "/scribblins-traits/field/sky.png", rarity: 26 },
      { id: "clay", name: "Clay", image: "/scribblins-traits/field/clay.png", rarity: 24 },
      { id: "butter", name: "Butter", image: "/scribblins-traits/field/butter.png", rarity: 18 },
    ],
  },
  {
    id: "body",
    label: "Body",
    blurb: "The skeleton — four doodle critters. Bunny, bear, pup, frog. The drawing never changes shape.",
    traits: [
      { id: "bunny", name: "Bunny", image: "/scribblins-traits/body/bunny.png", rarity: 36 },
      { id: "bear", name: "Bear", image: "/scribblins-traits/body/bear.png", rarity: 28 },
      { id: "pup", name: "Pup", image: "/scribblins-traits/body/pup.png", rarity: 22 },
      { id: "frog", name: "Frog", image: "/scribblins-traits/body/frog.png", rarity: 14 },
    ],
  },
  {
    id: "mug",
    label: "Mug",
    blurb: "Big oval eyes and a little blush on the same face points. Grin, sleepy, a pink blep.",
    traits: [
      { id: "blink", name: "Normal", image: "/scribblins-traits/mug/blink.png", rarity: 20 },
      { id: "grin", name: "Grin", image: "/scribblins-traits/mug/grin.png", rarity: 16 },
      { id: "sleepy", name: "Sleepy", image: "/scribblins-traits/mug/sleepy.png", rarity: 14 },
      { id: "blep", name: "Blep", image: "/scribblins-traits/mug/blep.png", rarity: 12 },
      { id: "wink", name: "Wink", image: "/scribblins-traits/mug/wink.png", rarity: 12 },
      { id: "spark", name: "Sparkly", image: "/scribblins-traits/mug/spark.png", rarity: 10 },
      { id: "pout", name: "Pout", image: "/scribblins-traits/mug/pout.png", rarity: 9 },
      { id: "heart", name: "Heart", image: "/scribblins-traits/mug/heart.png", rarity: 7 },
    ],
  },
  {
    id: "hat",
    label: "Hat",
    blurb: "Sits on one crown. Beanie, bow, headphones, a leaf. The body is not cut.",
    noneLabel: "None",
    traits: [
      { id: "beanie", name: "Beanie", image: "/scribblins-traits/hat/beanie.png", rarity: 16 },
      { id: "bow", name: "Bow", image: "/scribblins-traits/hat/bow.png", rarity: 14 },
      { id: "flower", name: "Flower", image: "/scribblins-traits/hat/flower.png", rarity: 12 },
      { id: "cap", name: "Cap", image: "/scribblins-traits/hat/cap.png", rarity: 12 },
      { id: "headphones", name: "Headphones", image: "/scribblins-traits/hat/headphones.png", rarity: 12 },
      { id: "leaf", name: "Leaf", image: "/scribblins-traits/hat/leaf.png", rarity: 10 },
    ],
  },
  {
    id: "wrap",
    label: "Wrap",
    blurb: "Neck extras on the same collar line — scarf, bandana, bowtie.",
    noneLabel: "None",
    traits: [
      { id: "scarf", name: "Scarf", image: "/scribblins-traits/wrap/scarf.png", rarity: 24 },
      { id: "bandana", name: "Bandana", image: "/scribblins-traits/wrap/bandana.png", rarity: 20 },
      { id: "bowtie", name: "Bowtie", image: "/scribblins-traits/wrap/bowtie.png", rarity: 16 },
    ],
  },
  {
    id: "charm",
    label: "Charm",
    blurb: "A held extra — star, pencil, heart, balloon. Floats beside the same tucked paws.",
    noneLabel: "None",
    traits: [
      { id: "star", name: "Star", image: "/scribblins-traits/charm/star.png", rarity: 20 },
      { id: "pencil", name: "Pencil", image: "/scribblins-traits/charm/pencil.png", rarity: 18 },
      { id: "heart", name: "Heart", image: "/scribblins-traits/charm/heart.png", rarity: 14 },
      { id: "balloon", name: "Balloon", image: "/scribblins-traits/charm/balloon.png", rarity: 12 },
    ],
  },
];

export const noneScribblinTrait: ScribblinTrait = { id: "none", name: "None", rarity: 0 };

export function scribblinCategoryById(id: ScribblinTraitCategory["id"]) {
  const category = scribblinTraitCategories.find((item) => item.id === id);
  if (!category) throw new Error(`Unknown Scribblin trait category: ${id}`);
  return category;
}

export function findScribblinTrait(categoryId: ScribblinTraitCategory["id"], traitId: string) {
  if (traitId === "none") return noneScribblinTrait;
  return scribblinCategoryById(categoryId).traits.find((trait) => trait.id === traitId);
}

export const defaultScribblinSelection = {
  field: "cream",
  body: "bunny",
  mug: "grin",
  hat: "headphones",
  wrap: "none",
  charm: "star",
} as const;

export type ScribblinSelection = Record<ScribblinTraitCategory["id"], string>;

export function randomScribblinSelection(): ScribblinSelection {
  const pick = (category: ScribblinTraitCategory) => {
    const pool: ScribblinTrait[] = category.noneLabel
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
    field: pick(scribblinCategoryById("field")),
    body: pick(scribblinCategoryById("body")),
    mug: pick(scribblinCategoryById("mug")),
    hat: pick(scribblinCategoryById("hat")),
    wrap: pick(scribblinCategoryById("wrap")),
    charm: pick(scribblinCategoryById("charm")),
  };
}

export function scribblinCombinationCount() {
  return scribblinTraitCategories.reduce((product, category) => {
    const extra = category.noneLabel ? 1 : 0;
    return product * (category.traits.length + extra);
  }, 1);
}

export function scribblinSelectionToLayers(selection: ScribblinSelection) {
  return (["field", "body", "mug", "hat", "wrap", "charm"] as const)
    .map((id) => findScribblinTrait(id, selection[id]))
    .filter((trait): trait is ScribblinTrait => Boolean(trait?.image))
    .map((trait) => scribblinTraitSrc(trait.image));
}
