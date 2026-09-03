export type FoxkinTrait = {
  id: string;
  name: string;
  image?: string;
  rarity: number;
};

export type FoxkinTraitCategory = {
  id: "field" | "pelt" | "mug" | "hat" | "wrap" | "charm";
  label: string;
  blurb: string;
  noneLabel?: string;
  traits: FoxkinTrait[];
};

/** Bump when APNG layers change so the studio does not keep a stale loop. */
export const FOXKIN_ART_VERSION = "foxkins-v2";

export const FOXKIN_FRAMES = 12;
export const FOXKIN_DURATION_MS = 90;

export function foxkinTraitSrc(path?: string) {
  if (!path) return "";
  return `${path}?v=${FOXKIN_ART_VERSION}`;
}

export const foxkinTraitCategories: FoxkinTraitCategory[] = [
  {
    id: "field",
    label: "Field",
    blurb: "A flat paper wash — peach, snow, dusk, hearth. The halo stays put.",
    traits: [
      { id: "peach", name: "Peach", image: "/foxkins-traits/field/peach.png", rarity: 32 },
      { id: "snow", name: "Snow", image: "/foxkins-traits/field/snow.png", rarity: 26 },
      { id: "dusk", name: "Dusk", image: "/foxkins-traits/field/dusk.png", rarity: 24 },
      { id: "hearth", name: "Hearth", image: "/foxkins-traits/field/hearth.png", rarity: 18 },
    ],
  },
  {
    id: "pelt",
    label: "Pelt",
    blurb: "The skeleton — three bodies only. Maple, snow, dusk. The sticker never changes.",
    traits: [
      { id: "maple", name: "Maple", image: "/foxkins-traits/pelt/maple.png", rarity: 55 },
      { id: "snow", name: "Snow", image: "/foxkins-traits/pelt/snow.png", rarity: 28 },
      { id: "dusk", name: "Dusk", image: "/foxkins-traits/pelt/dusk.png", rarity: 17 },
    ],
  },
  {
    id: "mug",
    label: "Mug",
    blurb: "Big graphic eyes on the same face points. Grin, sleepy, a pink blep.",
    traits: [
      { id: "blink", name: "Normal", image: "/foxkins-traits/mug/blink.png", rarity: 20 },
      { id: "grin", name: "Grin", image: "/foxkins-traits/mug/grin.png", rarity: 16 },
      { id: "sleepy", name: "Sleepy", image: "/foxkins-traits/mug/sleepy.png", rarity: 14 },
      { id: "blep", name: "Blep", image: "/foxkins-traits/mug/blep.png", rarity: 12 },
      { id: "wink", name: "Wink", image: "/foxkins-traits/mug/wink.png", rarity: 12 },
      { id: "spark", name: "Sparkly", image: "/foxkins-traits/mug/spark.png", rarity: 10 },
      { id: "pout", name: "Pout", image: "/foxkins-traits/mug/pout.png", rarity: 9 },
      { id: "heart", name: "Heart", image: "/foxkins-traits/mug/heart.png", rarity: 7 },
    ],
  },
  {
    id: "hat",
    label: "Hat",
    blurb: "Sits between the ears. Leaf, beret, flower, beanie. The pelt is not cut.",
    noneLabel: "None",
    traits: [
      { id: "leaf", name: "Leaf", image: "/foxkins-traits/hat/leaf.png", rarity: 16 },
      { id: "beret", name: "Beret", image: "/foxkins-traits/hat/beret.png", rarity: 14 },
      { id: "flower", name: "Flower", image: "/foxkins-traits/hat/flower.png", rarity: 12 },
      { id: "beanie", name: "Beanie", image: "/foxkins-traits/hat/beanie.png", rarity: 12 },
      { id: "cap", name: "Cap", image: "/foxkins-traits/hat/cap.png", rarity: 10 },
      { id: "bow", name: "Bow", image: "/foxkins-traits/hat/bow.png", rarity: 8 },
    ],
  },
  {
    id: "wrap",
    label: "Wrap",
    blurb: "Neck extras on the same collar line — scarf, bandana, bell.",
    noneLabel: "None",
    traits: [
      { id: "scarf", name: "Scarf", image: "/foxkins-traits/wrap/scarf.png", rarity: 24 },
      { id: "bandana", name: "Bandana", image: "/foxkins-traits/wrap/bandana.png", rarity: 20 },
      { id: "bell", name: "Bell", image: "/foxkins-traits/wrap/bell.png", rarity: 16 },
    ],
  },
  {
    id: "charm",
    label: "Charm",
    blurb: "A held extra — acorn, leaf, lantern. Floats beside the same tucked paws.",
    noneLabel: "None",
    traits: [
      { id: "acorn", name: "Acorn", image: "/foxkins-traits/charm/acorn.png", rarity: 24 },
      { id: "leaf", name: "Leaf", image: "/foxkins-traits/charm/leaf.png", rarity: 20 },
      { id: "lantern", name: "Lantern", image: "/foxkins-traits/charm/lantern.png", rarity: 16 },
    ],
  },
];

export const noneFoxkinTrait: FoxkinTrait = { id: "none", name: "None", rarity: 0 };

export function foxkinCategoryById(id: FoxkinTraitCategory["id"]) {
  const category = foxkinTraitCategories.find((item) => item.id === id);
  if (!category) throw new Error(`Unknown Foxkin trait category: ${id}`);
  return category;
}

export function findFoxkinTrait(categoryId: FoxkinTraitCategory["id"], traitId: string) {
  if (traitId === "none") return noneFoxkinTrait;
  return foxkinCategoryById(categoryId).traits.find((trait) => trait.id === traitId);
}

export const defaultFoxkinSelection = {
  field: "peach",
  pelt: "maple",
  mug: "blink",
  hat: "none",
  wrap: "none",
  charm: "none",
} as const;

export type FoxkinSelection = Record<FoxkinTraitCategory["id"], string>;

export function randomFoxkinSelection(): FoxkinSelection {
  const pick = (category: FoxkinTraitCategory) => {
    const pool: FoxkinTrait[] = category.noneLabel
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
    field: pick(foxkinCategoryById("field")),
    pelt: pick(foxkinCategoryById("pelt")),
    mug: pick(foxkinCategoryById("mug")),
    hat: pick(foxkinCategoryById("hat")),
    wrap: pick(foxkinCategoryById("wrap")),
    charm: pick(foxkinCategoryById("charm")),
  };
}

export function foxkinCombinationCount() {
  return foxkinTraitCategories.reduce((product, category) => {
    const extra = category.noneLabel ? 1 : 0;
    return product * (category.traits.length + extra);
  }, 1);
}

export function foxkinSelectionToLayers(selection: FoxkinSelection) {
  return (["field", "pelt", "mug", "hat", "wrap", "charm"] as const)
    .map((id) => findFoxkinTrait(id, selection[id]))
    .filter((trait): trait is FoxkinTrait => Boolean(trait?.image))
    .map((trait) => foxkinTraitSrc(trait.image));
}
