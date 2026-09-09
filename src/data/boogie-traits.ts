export type BoogieTrait = {
  id: string;
  name: string;
  image?: string;
  rarity: number;
};

export type BoogieTraitCategory = {
  id: "stage" | "lights" | "cast" | "face" | "fit" | "prop";
  label: string;
  blurb: string;
  noneLabel?: string;
  traits: BoogieTrait[];
};

export const BOOGIE_ART_VERSION = "boogiesquad-v1";
export const BOOGIE_FRAMES = 12;
export const BOOGIE_DURATION_MS = 90;

export function boogieTraitSrc(path?: string) {
  if (!path) return "";
  return `${path}?v=${BOOGIE_ART_VERSION}`;
}

export const boogieTraitCategories: BoogieTraitCategory[] = [
  {
    id: "stage",
    label: "Stage",
    blurb: "The room — dance floor, disco, rooftop, alley, booth, backyard, warehouse.",
    traits: [
      { id: "floor", name: "Dance Floor", image: "/boogiesquad-traits/stage/floor.png", rarity: 22 },
      { id: "disco", name: "Disco Hall", image: "/boogiesquad-traits/stage/disco.png", rarity: 16 },
      { id: "rooftop", name: "Rooftop Party", image: "/boogiesquad-traits/stage/rooftop.png", rarity: 14 },
      { id: "alley", name: "Neon Alley", image: "/boogiesquad-traits/stage/alley.png", rarity: 14 },
      { id: "booth", name: "Club Booth", image: "/boogiesquad-traits/stage/booth.png", rarity: 12 },
      { id: "backyard", name: "Backyard Jam", image: "/boogiesquad-traits/stage/backyard.png", rarity: 12 },
      { id: "warehouse", name: "Warehouse Rave", image: "/boogiesquad-traits/stage/warehouse.png", rarity: 10 },
    ],
  },
  {
    id: "lights",
    label: "Lights",
    blurb: "Beat FX — spots, glints, neon, confetti, rings. Or none.",
    noneLabel: "None",
    traits: [
      { id: "spots", name: "Spotlights", image: "/boogiesquad-traits/lights/spots.png", rarity: 18 },
      { id: "glitter", name: "Disco Glints", image: "/boogiesquad-traits/lights/glitter.png", rarity: 16 },
      { id: "neon", name: "Neon Glow", image: "/boogiesquad-traits/lights/neon.png", rarity: 14 },
      { id: "confetti", name: "Confetti Burst", image: "/boogiesquad-traits/lights/confetti.png", rarity: 14 },
      { id: "rings", name: "Beat Rings", image: "/boogiesquad-traits/lights/rings.png", rarity: 10 },
    ],
  },
  {
    id: "cast",
    label: "Cast",
    blurb: "Who is dancing — cats, frogs, blobs, birds, robots, and more colorways.",
    traits: [
      { id: "cat-peach", name: "Peach Cat", image: "/boogiesquad-traits/cast/cat-peach.png", rarity: 14 },
      { id: "cat-midnight", name: "Midnight Cat", image: "/boogiesquad-traits/cast/cat-midnight.png", rarity: 10 },
      { id: "frog-lime", name: "Lime Frog", image: "/boogiesquad-traits/cast/frog-lime.png", rarity: 12 },
      { id: "frog-teal", name: "Teal Frog", image: "/boogiesquad-traits/cast/frog-teal.png", rarity: 9 },
      { id: "blob-grape", name: "Grape Blob", image: "/boogiesquad-traits/cast/blob-grape.png", rarity: 10 },
      { id: "blob-mango", name: "Mango Blob", image: "/boogiesquad-traits/cast/blob-mango.png", rarity: 8 },
      { id: "bird-canary", name: "Canary Bird", image: "/boogiesquad-traits/cast/bird-canary.png", rarity: 10 },
      { id: "bird-indigo", name: "Indigo Bird", image: "/boogiesquad-traits/cast/bird-indigo.png", rarity: 7 },
      { id: "robot-chrome", name: "Chrome Robot", image: "/boogiesquad-traits/cast/robot-chrome.png", rarity: 8 },
      { id: "robot-candy", name: "Candy Robot", image: "/boogiesquad-traits/cast/robot-candy.png", rarity: 5 },
      { id: "bunny-cream", name: "Cream Bunny", image: "/boogiesquad-traits/cast/bunny-cream.png", rarity: 4 },
      { id: "pig-blush", name: "Blush Pig", image: "/boogiesquad-traits/cast/pig-blush.png", rarity: 3 },
    ],
  },
  {
    id: "face",
    label: "Face",
    blurb: "The mug on the same head points — hype, cool, wink, scream.",
    traits: [
      { id: "hype", name: "Hype", image: "/boogiesquad-traits/face/hype.png", rarity: 18 },
      { id: "cool", name: "Cool", image: "/boogiesquad-traits/face/cool.png", rarity: 16 },
      { id: "wink", name: "Wink", image: "/boogiesquad-traits/face/wink.png", rarity: 14 },
      { id: "blep", name: "Tongue Out", image: "/boogiesquad-traits/face/blep.png", rarity: 12 },
      { id: "grin", name: "Grin", image: "/boogiesquad-traits/face/grin.png", rarity: 12 },
      { id: "focus", name: "Focused", image: "/boogiesquad-traits/face/focus.png", rarity: 10 },
      { id: "scream", name: "Party Scream", image: "/boogiesquad-traits/face/scream.png", rarity: 10 },
      { id: "heart", name: "Heart Eyes", image: "/boogiesquad-traits/face/heart.png", rarity: 8 },
    ],
  },
  {
    id: "fit",
    label: "Fit",
    blurb: "Wear on the same groove — hoodie, shades, jacket, headphones, chain.",
    noneLabel: "None",
    traits: [
      { id: "hoodie", name: "Hoodie", image: "/boogiesquad-traits/fit/hoodie.png", rarity: 16 },
      { id: "shades", name: "Shades", image: "/boogiesquad-traits/fit/shades.png", rarity: 14 },
      { id: "jacket", name: "Jacket", image: "/boogiesquad-traits/fit/jacket.png", rarity: 14 },
      { id: "phones", name: "Headphones", image: "/boogiesquad-traits/fit/phones.png", rarity: 12 },
      { id: "chain", name: "Chain", image: "/boogiesquad-traits/fit/chain.png", rarity: 10 },
      { id: "visor", name: "Visor", image: "/boogiesquad-traits/fit/visor.png", rarity: 8 },
    ],
  },
  {
    id: "prop",
    label: "Prop",
    blurb: "A held extra that rides the right hand — mic, boombox, vinyl, trophy.",
    noneLabel: "None",
    traits: [
      { id: "mic", name: "Mic", image: "/boogiesquad-traits/prop/mic.png", rarity: 16 },
      { id: "boombox", name: "Boombox", image: "/boogiesquad-traits/prop/boombox.png", rarity: 14 },
      { id: "sticks", name: "Glow Sticks", image: "/boogiesquad-traits/prop/sticks.png", rarity: 14 },
      { id: "vinyl", name: "Vinyl", image: "/boogiesquad-traits/prop/vinyl.png", rarity: 12 },
      { id: "drink", name: "Drink", image: "/boogiesquad-traits/prop/drink.png", rarity: 10 },
      { id: "trophy", name: "Trophy", image: "/boogiesquad-traits/prop/trophy.png", rarity: 6 },
    ],
  }
];

export const noneBoogieTrait: BoogieTrait = { id: "none", name: "None", rarity: 0 };

export function boogieCategoryById(id: BoogieTraitCategory["id"]) {
  const category = boogieTraitCategories.find((item) => item.id === id);
  if (!category) throw new Error(`Unknown Boogie Squad trait category: ${id}`);
  return category;
}

export function findBoogieTrait(categoryId: BoogieTraitCategory["id"], traitId: string) {
  if (traitId === "none") return noneBoogieTrait;
  return boogieCategoryById(categoryId).traits.find((trait) => trait.id === traitId);
}

export const defaultBoogieSelection = {
  stage: "floor", lights: "none", cast: "cat-peach", face: "hype", fit: "none", prop: "none",
} as const;

export type BoogieSelection = Record<BoogieTraitCategory["id"], string>;

export function randomBoogieSelection(): BoogieSelection {
  const pick = (category: BoogieTraitCategory) => {
    const pool: BoogieTrait[] = category.noneLabel
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
    stage: pick(boogieCategoryById("stage")),
    lights: pick(boogieCategoryById("lights")),
    cast: pick(boogieCategoryById("cast")),
    face: pick(boogieCategoryById("face")),
    fit: pick(boogieCategoryById("fit")),
    prop: pick(boogieCategoryById("prop")),
  };
}

export function boogieCombinationCount() {
  return boogieTraitCategories.reduce((product, category) => {
    const extra = category.noneLabel ? 1 : 0;
    return product * (category.traits.length + extra);
  }, 1);
}

export function boogieSelectionToLayers(selection: BoogieSelection) {
  return (["stage", "lights", "cast", "face", "fit", "prop"] as const)
    .map((id) => findBoogieTrait(id, selection[id]))
    .filter((trait): trait is BoogieTrait => Boolean(trait?.image))
    .map((trait) => boogieTraitSrc(trait.image));
}
