export type MochinTrait = {
  id: string;
  name: string;
  image?: string;
  rarity: number;
};

export type MochinTraitCategory = {
  id: "stage" | "haze" | "dough" | "face" | "topping" | "steam";
  label: string;
  blurb: string;
  noneLabel?: string;
  traits: MochinTrait[];
};

/** Bump when APNG layers change so the studio does not keep a stale loop. */
export const MOCHIN_ART_VERSION = "mochins-v5";

export const MOCHIN_FRAMES = 16;
export const MOCHIN_DURATION_MS = 100;

export function mochinTraitSrc(path?: string) {
  if (!path) return "";
  return `${path}?v=${MOCHIN_ART_VERSION}`;
}

export const mochinTraitCategories: MochinTraitCategory[] = [
  {
    id: "stage",
    label: "Stage",
    blurb: "A collector cove and a lacquered stand — cream, dusk, matcha, marble, night.",
    traits: [
      { id: "cream", name: "Cream Cove", image: "/mochins-traits/stage/cream.png", rarity: 14 },
      { id: "dusk", name: "Dusk Cove", image: "/mochins-traits/stage/dusk.png", rarity: 12 },
      { id: "matcha", name: "Matcha Cove", image: "/mochins-traits/stage/matcha.png", rarity: 14 },
      { id: "night", name: "Night Cove", image: "/mochins-traits/stage/night.png", rarity: 10 },
      { id: "blush", name: "Blush Cove", image: "/mochins-traits/stage/blush.png", rarity: 14 },
      { id: "marble", name: "Marble Cove", image: "/mochins-traits/stage/marble.png", rarity: 12 },
      { id: "amber", name: "Amber Cove", image: "/mochins-traits/stage/amber.png", rarity: 12 },
      { id: "fog", name: "Fog Cove", image: "/mochins-traits/stage/fog.png", rarity: 12 },
    ],
  },
  {
    id: "haze",
    label: "Haze",
    blurb: "Volumetric key and rim — motes sit in the air, not under the vinyl.",
    noneLabel: "No haze",
    traits: [
      { id: "warm", name: "Warm Key", image: "/mochins-traits/haze/warm.png", rarity: 20 },
      { id: "cool", name: "Cool Rim", image: "/mochins-traits/haze/cool.png", rarity: 20 },
      { id: "gold", name: "Gold Motes", image: "/mochins-traits/haze/gold.png", rarity: 18 },
      { id: "sakura", name: "Sakura Dust", image: "/mochins-traits/haze/sakura.png", rarity: 18 },
    ],
  },
  {
    id: "dough",
    label: "Vinyl",
    blurb: "The molded body — ivory, matcha, berry, black, yuzu, cocoa, taro plastic.",
    traits: [
      { id: "snow", name: "Snow", image: "/mochins-traits/dough/snow.png", rarity: 20 },
      { id: "matcha", name: "Matcha", image: "/mochins-traits/dough/matcha.png", rarity: 16 },
      { id: "berry", name: "Berry", image: "/mochins-traits/dough/berry.png", rarity: 16 },
      { id: "sesame", name: "Sesame", image: "/mochins-traits/dough/sesame.png", rarity: 14 },
      { id: "yuzu", name: "Yuzu", image: "/mochins-traits/dough/yuzu.png", rarity: 12 },
      { id: "cocoa", name: "Cocoa", image: "/mochins-traits/dough/cocoa.png", rarity: 12 },
      { id: "taro", name: "Taro", image: "/mochins-traits/dough/taro.png", rarity: 10 },
    ],
  },
  {
    id: "face",
    label: "Face",
    blurb: "Molded on the front of the volume — blink, wink, grin — locked to the idle bob.",
    traits: [
      { id: "blink", name: "Blink", image: "/mochins-traits/face/blink.png", rarity: 20 },
      { id: "wink", name: "Wink", image: "/mochins-traits/face/wink.png", rarity: 14 },
      { id: "sleepy", name: "Sleepy", image: "/mochins-traits/face/sleepy.png", rarity: 14 },
      { id: "grin", name: "Grin", image: "/mochins-traits/face/grin.png", rarity: 14 },
      { id: "pout", name: "Pout", image: "/mochins-traits/face/pout.png", rarity: 12 },
      { id: "spark", name: "Spark", image: "/mochins-traits/face/spark.png", rarity: 12 },
      { id: "heart", name: "Heart", image: "/mochins-traits/face/heart.png", rarity: 8 },
      { id: "wide", name: "Wide", image: "/mochins-traits/face/wide.png", rarity: 6 },
    ],
  },
  {
    id: "topping",
    label: "Topping",
    blurb: "Molded vinyl bits on the crown — leaf, drizzle, berry, bow.",
    noneLabel: "Plain",
    traits: [
      { id: "leaf", name: "Leaf", image: "/mochins-traits/topping/leaf.png", rarity: 16 },
      { id: "sesame", name: "Sesame Dust", image: "/mochins-traits/topping/sesame.png", rarity: 16 },
      { id: "drizzle", name: "Drizzle", image: "/mochins-traits/topping/drizzle.png", rarity: 14 },
      { id: "berry", name: "Berry", image: "/mochins-traits/topping/berry.png", rarity: 12 },
      { id: "kinako", name: "Kinako", image: "/mochins-traits/topping/kinako.png", rarity: 12 },
      { id: "bow", name: "Bow", image: "/mochins-traits/topping/bow.png", rarity: 8 },
    ],
  },
  {
    id: "steam",
    label: "Steam",
    blurb: "Shelf glitter in the air — wisps, puff, sparkle.",
    noneLabel: "Still",
    traits: [
      { id: "wisps", name: "Wisps", image: "/mochins-traits/steam/wisps.png", rarity: 26 },
      { id: "puff", name: "Puff", image: "/mochins-traits/steam/puff.png", rarity: 24 },
      { id: "sparkle", name: "Sparkle", image: "/mochins-traits/steam/sparkle.png", rarity: 22 },
    ],
  },
];

export const noneMochinTrait: MochinTrait = { id: "none", name: "None", rarity: 0 };

export function mochinCategoryById(id: MochinTraitCategory["id"]) {
  const category = mochinTraitCategories.find((item) => item.id === id);
  if (!category) throw new Error(`Unknown Mochin trait category: ${id}`);
  return category;
}

export function findMochinTrait(categoryId: MochinTraitCategory["id"], traitId: string) {
  if (traitId === "none") return noneMochinTrait;
  return mochinCategoryById(categoryId).traits.find((trait) => trait.id === traitId);
}

export const defaultMochinSelection = {
  stage: "cream",
  haze: "warm",
  dough: "snow",
  face: "blink",
  topping: "leaf",
  steam: "wisps",
} as const;

export type MochinSelection = Record<MochinTraitCategory["id"], string>;

export function randomMochinSelection(): MochinSelection {
  const pick = (category: MochinTraitCategory) => {
    const pool: MochinTrait[] = category.noneLabel
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
    stage: pick(mochinCategoryById("stage")),
    haze: pick(mochinCategoryById("haze")),
    dough: pick(mochinCategoryById("dough")),
    face: pick(mochinCategoryById("face")),
    topping: pick(mochinCategoryById("topping")),
    steam: pick(mochinCategoryById("steam")),
  };
}

export function mochinCombinationCount() {
  return mochinTraitCategories.reduce((product, category) => {
    const extra = category.noneLabel ? 1 : 0;
    return product * (category.traits.length + extra);
  }, 1);
}

export function mochinSelectionToLayers(selection: MochinSelection) {
  return (["stage", "haze", "dough", "face", "topping", "steam"] as const)
    .map((id) => findMochinTrait(id, selection[id]))
    .filter((trait): trait is MochinTrait => Boolean(trait?.image))
    .map((trait) => mochinTraitSrc(trait.image));
}
