export type FoxinTrait = {
  id: string;
  name: string;
  image?: string;
  rarity: number;
};

export type FoxinTraitCategory = {
  id: "field" | "pelt" | "mug" | "hat" | "wrap" | "charm";
  label: string;
  blurb: string;
  noneLabel?: string;
  traits: FoxinTrait[];
};

/** Bump when APNG layers change so the studio does not keep a stale loop. */
export const FOXIN_ART_VERSION = "foxins-v2";

export const FOXIN_FRAMES = 12;
export const FOXIN_DURATION_MS = 90;

export function foxinTraitSrc(path?: string) {
  if (!path) return "";
  return `${path}?v=${FOXIN_ART_VERSION}`;
}

export const foxinTraitCategories: FoxinTraitCategory[] = [
  {
    id: "field",
    label: "Field",
    blurb: "A flat paper wash — peach, snow, dusk, hearth. The halo stays put.",
    traits: [
      { id: "peach", name: "Peach", image: "/foxins-traits/field/peach.png", rarity: 32 },
      { id: "snow", name: "Snow", image: "/foxins-traits/field/snow.png", rarity: 26 },
      { id: "dusk", name: "Dusk", image: "/foxins-traits/field/dusk.png", rarity: 24 },
      { id: "hearth", name: "Hearth", image: "/foxins-traits/field/hearth.png", rarity: 18 },
    ],
  },
  {
    id: "pelt",
    label: "Pelt",
    blurb: "The skeleton — three bodies only. Maple, snow, dusk. The sticker never changes.",
    traits: [
      { id: "maple", name: "Maple", image: "/foxins-traits/pelt/maple.png", rarity: 55 },
      { id: "snow", name: "Snow", image: "/foxins-traits/pelt/snow.png", rarity: 28 },
      { id: "dusk", name: "Dusk", image: "/foxins-traits/pelt/dusk.png", rarity: 17 },
    ],
  },
  {
    id: "mug",
    label: "Mug",
    blurb: "Big graphic eyes on the same face points. Grin, sleepy, a pink blep.",
    traits: [
      { id: "blink", name: "Normal", image: "/foxins-traits/mug/blink.png", rarity: 20 },
      { id: "grin", name: "Grin", image: "/foxins-traits/mug/grin.png", rarity: 16 },
      { id: "sleepy", name: "Sleepy", image: "/foxins-traits/mug/sleepy.png", rarity: 14 },
      { id: "blep", name: "Blep", image: "/foxins-traits/mug/blep.png", rarity: 12 },
      { id: "wink", name: "Wink", image: "/foxins-traits/mug/wink.png", rarity: 12 },
      { id: "spark", name: "Sparkly", image: "/foxins-traits/mug/spark.png", rarity: 10 },
      { id: "pout", name: "Pout", image: "/foxins-traits/mug/pout.png", rarity: 9 },
      { id: "heart", name: "Heart", image: "/foxins-traits/mug/heart.png", rarity: 7 },
    ],
  },
  {
    id: "hat",
    label: "Hat",
    blurb: "Sits between the ears. Leaf, beret, flower, beanie. The pelt is not cut.",
    noneLabel: "None",
    traits: [
      { id: "leaf", name: "Leaf", image: "/foxins-traits/hat/leaf.png", rarity: 16 },
      { id: "beret", name: "Beret", image: "/foxins-traits/hat/beret.png", rarity: 14 },
      { id: "flower", name: "Flower", image: "/foxins-traits/hat/flower.png", rarity: 12 },
      { id: "beanie", name: "Beanie", image: "/foxins-traits/hat/beanie.png", rarity: 12 },
      { id: "cap", name: "Cap", image: "/foxins-traits/hat/cap.png", rarity: 10 },
      { id: "bow", name: "Bow", image: "/foxins-traits/hat/bow.png", rarity: 8 },
    ],
  },
  {
    id: "wrap",
    label: "Wrap",
    blurb: "Neck extras on the same collar line — scarf, bandana, bell.",
    noneLabel: "None",
    traits: [
      { id: "scarf", name: "Scarf", image: "/foxins-traits/wrap/scarf.png", rarity: 24 },
      { id: "bandana", name: "Bandana", image: "/foxins-traits/wrap/bandana.png", rarity: 20 },
      { id: "bell", name: "Bell", image: "/foxins-traits/wrap/bell.png", rarity: 16 },
    ],
  },
  {
    id: "charm",
    label: "Charm",
    blurb: "A held extra — acorn, leaf, lantern. Floats beside the same tucked paws.",
    noneLabel: "None",
    traits: [
      { id: "acorn", name: "Acorn", image: "/foxins-traits/charm/acorn.png", rarity: 24 },
      { id: "leaf", name: "Leaf", image: "/foxins-traits/charm/leaf.png", rarity: 20 },
      { id: "lantern", name: "Lantern", image: "/foxins-traits/charm/lantern.png", rarity: 16 },
    ],
  },
];

export const noneFoxinTrait: FoxinTrait = { id: "none", name: "None", rarity: 0 };

export function foxinCategoryById(id: FoxinTraitCategory["id"]) {
  const category = foxinTraitCategories.find((item) => item.id === id);
  if (!category) throw new Error(`Unknown Foxin trait category: ${id}`);
  return category;
}

export function findFoxinTrait(categoryId: FoxinTraitCategory["id"], traitId: string) {
  if (traitId === "none") return noneFoxinTrait;
  return foxinCategoryById(categoryId).traits.find((trait) => trait.id === traitId);
}

export const defaultFoxinSelection = {
  field: "peach",
  pelt: "maple",
  mug: "blink",
  hat: "none",
  wrap: "none",
  charm: "none",
} as const;

export type FoxinSelection = Record<FoxinTraitCategory["id"], string>;

export function randomFoxinSelection(): FoxinSelection {
  const pick = (category: FoxinTraitCategory) => {
    const pool: FoxinTrait[] = category.noneLabel
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
    field: pick(foxinCategoryById("field")),
    pelt: pick(foxinCategoryById("pelt")),
    mug: pick(foxinCategoryById("mug")),
    hat: pick(foxinCategoryById("hat")),
    wrap: pick(foxinCategoryById("wrap")),
    charm: pick(foxinCategoryById("charm")),
  };
}

export function foxinCombinationCount() {
  return foxinTraitCategories.reduce((product, category) => {
    const extra = category.noneLabel ? 1 : 0;
    return product * (category.traits.length + extra);
  }, 1);
}

export function foxinSelectionToLayers(selection: FoxinSelection) {
  return (["field", "pelt", "mug", "hat", "wrap", "charm"] as const)
    .map((id) => findFoxinTrait(id, selection[id]))
    .filter((trait): trait is FoxinTrait => Boolean(trait?.image))
    .map((trait) => foxinTraitSrc(trait.image));
}
