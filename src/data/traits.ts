export type Trait = {
  id: string;
  name: string;
  image?: string;
  rarity: number;
};

export type TraitCategory = {
  id: "sky" | "aura" | "body" | "face" | "wear" | "charm";
  label: string;
  blurb: string;
  noneLabel?: string;
  traits: Trait[];
};

/** Bump when APNG layers change so the studio does not keep a stale loop. */
export const TRAIT_ART_VERSION = "apng-stack-v1";

export const TRAIT_FRAMES = 12;
export const TRAIT_DURATION_MS = 80;

export function traitSrc(path?: string) {
  if (!path) return "";
  return `${path}?v=${TRAIT_ART_VERSION}`;
}

export const traitCategories: TraitCategory[] = [
  {
    id: "sky",
    label: "Sky",
    blurb: "Full-canvas loops — drift, flicker, wash, and flash behind the body.",
    traits: [
      { id: "midnight", name: "Midnight Drift", image: "/traits/sky/midnight.png", rarity: 18 },
      { id: "neon", name: "Neon Grid", image: "/traits/sky/neon.png", rarity: 14 },
      { id: "dawn", name: "Soft Dawn", image: "/traits/sky/dawn.png", rarity: 14 },
      { id: "forest", name: "Firefly Grove", image: "/traits/sky/forest.png", rarity: 12 },
      { id: "coral", name: "Coral Dusk", image: "/traits/sky/coral.png", rarity: 12 },
      { id: "void", name: "Void Speckles", image: "/traits/sky/void.png", rarity: 12 },
      { id: "candy", name: "Candy Wash", image: "/traits/sky/candy.png", rarity: 10 },
      { id: "storm", name: "Storm Flicker", image: "/traits/sky/storm.png", rarity: 8 },
    ],
  },
  {
    id: "aura",
    label: "Aura",
    blurb: "A glow that sits behind the creature and pulses on the shared clock.",
    noneLabel: "No aura",
    traits: [
      { id: "mint", name: "Mint Pulse", image: "/traits/aura/mint.png", rarity: 16 },
      { id: "gold", name: "Gold Ring", image: "/traits/aura/gold.png", rarity: 14 },
      { id: "magenta", name: "Magenta Haze", image: "/traits/aura/magenta.png", rarity: 14 },
      { id: "ice", name: "Ice Shimmer", image: "/traits/aura/ice.png", rarity: 12 },
      { id: "ember", name: "Ember Glow", image: "/traits/aura/ember.png", rarity: 12 },
      { id: "pixel", name: "Pixel Spark", image: "/traits/aura/pixel.png", rarity: 10 },
    ],
  },
  {
    id: "body",
    label: "Body",
    blurb: "Six silhouettes. Each one bobs on the same 12-frame breathe.",
    traits: [
      { id: "pudding", name: "Pudding", image: "/traits/body/pudding.png", rarity: 22 },
      { id: "fox", name: "Fox", image: "/traits/body/fox.png", rarity: 18 },
      { id: "owl", name: "Owl", image: "/traits/body/owl.png", rarity: 16 },
      { id: "frog", name: "Frog", image: "/traits/body/frog.png", rarity: 16 },
      { id: "cat", name: "Cat", image: "/traits/body/cat.png", rarity: 16 },
      { id: "beetle", name: "Beetle", image: "/traits/body/beetle.png", rarity: 12 },
    ],
  },
  {
    id: "face",
    label: "Face",
    blurb: "Eyes and mouths locked to the body bob, with their own blinks.",
    traits: [
      { id: "blink", name: "Blink", image: "/traits/face/blink.png", rarity: 24 },
      { id: "sleepy", name: "Sleepy", image: "/traits/face/sleepy.png", rarity: 18 },
      { id: "spark", name: "Spark", image: "/traits/face/spark.png", rarity: 16 },
      { id: "wink", name: "Wink", image: "/traits/face/wink.png", rarity: 16 },
      { id: "glow", name: "Glow", image: "/traits/face/glow.png", rarity: 14 },
      { id: "specs", name: "Specs", image: "/traits/face/specs.png", rarity: 12 },
    ],
  },
  {
    id: "wear",
    label: "Wear",
    blurb: "Hats and signals that ride the same bob so they stay glued on.",
    noneLabel: "Bare head",
    traits: [
      { id: "cap", name: "Mint Cap", image: "/traits/wear/cap.png", rarity: 16 },
      { id: "antenna", name: "Signal Antenna", image: "/traits/wear/antenna.png", rarity: 14 },
      { id: "sprout", name: "Sprout", image: "/traits/wear/sprout.png", rarity: 14 },
      { id: "crown", name: "Tiny Crown", image: "/traits/wear/crown.png", rarity: 12 },
      { id: "hood", name: "Night Hood", image: "/traits/wear/hood.png", rarity: 12 },
      { id: "halo", name: "Soft Halo", image: "/traits/wear/halo.png", rarity: 10 },
    ],
  },
  {
    id: "charm",
    label: "Charm",
    blurb: "Front-layer loops — orbits, floats, and spins on their own path.",
    noneLabel: "None",
    traits: [
      { id: "star", name: "Orbit Star", image: "/traits/charm/star.png", rarity: 16 },
      { id: "heart", name: "Float Heart", image: "/traits/charm/heart.png", rarity: 14 },
      { id: "bubble", name: "Bubble", image: "/traits/charm/bubble.png", rarity: 14 },
      { id: "leaf", name: "Leaf", image: "/traits/charm/leaf.png", rarity: 12 },
      { id: "coin", name: "Spin Coin", image: "/traits/charm/coin.png", rarity: 12 },
      { id: "spark", name: "Spark Trail", image: "/traits/charm/spark.png", rarity: 8 },
    ],
  },
];

export const noneTrait: Trait = { id: "none", name: "None", rarity: 0 };

export function categoryById(id: TraitCategory["id"]) {
  const category = traitCategories.find((item) => item.id === id);
  if (!category) throw new Error(`Unknown trait category: ${id}`);
  return category;
}

export function findTrait(categoryId: TraitCategory["id"], traitId: string) {
  if (traitId === "none") return noneTrait;
  return categoryById(categoryId).traits.find((trait) => trait.id === traitId);
}

export const defaultSelection = {
  sky: "midnight",
  aura: "mint",
  body: "pudding",
  face: "blink",
  wear: "cap",
  charm: "star",
} as const;

export type Selection = Record<TraitCategory["id"], string>;

export function randomSelection(): Selection {
  const pick = (category: TraitCategory) => {
    const pool: Trait[] = category.noneLabel
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
    sky: pick(categoryById("sky")),
    aura: pick(categoryById("aura")),
    body: pick(categoryById("body")),
    face: pick(categoryById("face")),
    wear: pick(categoryById("wear")),
    charm: pick(categoryById("charm")),
  };
}

export function combinationCount() {
  return traitCategories.reduce((product, category) => {
    const extra = category.noneLabel ? 1 : 0;
    return product * (category.traits.length + extra);
  }, 1);
}

export function selectionToLayers(selection: Selection) {
  return (["sky", "aura", "body", "face", "wear", "charm"] as const)
    .map((id) => findTrait(id, selection[id]))
    .filter((trait): trait is Trait => Boolean(trait?.image))
    .map((trait) => traitSrc(trait.image));
}
