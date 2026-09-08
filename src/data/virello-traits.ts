export type VirelloTrait = {
  id: string;
  name: string;
  image?: string;
  rarity: number;
};

export type VirelloTraitCategory = {
  id: "bench" | "chassis" | "enamel" | "decal" | "key" | "spark" | "wear";
  label: string;
  blurb: string;
  noneLabel?: string;
  traits: VirelloTrait[];
};

/** Bump when APNG layers change so the studio does not keep a stale loop. */
export const VIRELLO_ART_VERSION = "virello-v1";

export const VIRELLO_FRAMES = 12;
export const VIRELLO_DURATION_MS = 90;

export function virelloTraitSrc(path?: string) {
  if (!path) return "";
  return `${path}?v=${VIRELLO_ART_VERSION}`;
}

export const virelloTraitCategories: VirelloTraitCategory[] = [
  {
    id: "bench",
    label: "Bench",
    blurb: "The toy-shop counter — linoleum, felt, crate, enamel, pine.",
    traits: [
      { id: "linoleum", name: "Linoleum Bench", image: "/virello-traits/bench/linoleum.png", rarity: 22 },
      { id: "felt", name: "Felt Bench", image: "/virello-traits/bench/felt.png", rarity: 20 },
      { id: "crate", name: "Crate Bench", image: "/virello-traits/bench/crate.png", rarity: 20 },
      { id: "enamel", name: "Enamel Bench", image: "/virello-traits/bench/enamel.png", rarity: 20 },
      { id: "pine", name: "Pine Bench", image: "/virello-traits/bench/pine.png", rarity: 18 },
    ],
  },
  {
    id: "chassis",
    label: "Chassis",
    blurb: "The stamped body — robot, duck, racer, soldier, monkey, tank, copter, frog.",
    traits: [
      { id: "robot", name: "Robot Chassis", image: "/virello-traits/chassis/robot.png", rarity: 16 },
      { id: "duck", name: "Duck Chassis", image: "/virello-traits/chassis/duck.png", rarity: 14 },
      { id: "racer", name: "Racer Chassis", image: "/virello-traits/chassis/racer.png", rarity: 14 },
      { id: "soldier", name: "Soldier Chassis", image: "/virello-traits/chassis/soldier.png", rarity: 12 },
      { id: "monkey", name: "Monkey Chassis", image: "/virello-traits/chassis/monkey.png", rarity: 12 },
      { id: "tank", name: "Tank Chassis", image: "/virello-traits/chassis/tank.png", rarity: 12 },
      { id: "copter", name: "Copter Chassis", image: "/virello-traits/chassis/copter.png", rarity: 10 },
      { id: "frog", name: "Frog Chassis", image: "/virello-traits/chassis/frog.png", rarity: 10 },
    ],
  },
  {
    id: "enamel",
    label: "Enamel",
    blurb: "The litho ink — tomato, navy, mustard, chrome, mint, cream, cherry.",
    traits: [
      { id: "tomato", name: "Tomato Enamel", image: "/virello-traits/enamel/tomato.png", rarity: 18 },
      { id: "navy", name: "Navy Enamel", image: "/virello-traits/enamel/navy.png", rarity: 16 },
      { id: "mustard", name: "Mustard Enamel", image: "/virello-traits/enamel/mustard.png", rarity: 16 },
      { id: "chrome", name: "Chrome Enamel", image: "/virello-traits/enamel/chrome.png", rarity: 14 },
      { id: "mint", name: "Mint Enamel", image: "/virello-traits/enamel/mint.png", rarity: 14 },
      { id: "cream", name: "Cream Enamel", image: "/virello-traits/enamel/cream.png", rarity: 12 },
      { id: "cherry", name: "Cherry Enamel", image: "/virello-traits/enamel/cherry.png", rarity: 10 },
    ],
  },
  {
    id: "decal",
    label: "Decal",
    blurb: "The chest print — star, number 8, circus, lightning.",
    noneLabel: "Bare Tin",
    traits: [
      { id: "star", name: "Star Decal", image: "/virello-traits/decal/star.png", rarity: 20 },
      { id: "eight", name: "No. 8 Decal", image: "/virello-traits/decal/eight.png", rarity: 20 },
      { id: "circus", name: "Circus Decal", image: "/virello-traits/decal/circus.png", rarity: 20 },
      { id: "lightning", name: "Lightning Decal", image: "/virello-traits/decal/lightning.png", rarity: 18 },
    ],
  },
  {
    id: "key",
    label: "Key",
    blurb: "The wind-up — brass, nickel, painted. The key is the loop.",
    noneLabel: "No Key",
    traits: [
      { id: "brass", name: "Brass Key", image: "/virello-traits/key/brass.png", rarity: 28 },
      { id: "nickel", name: "Nickel Key", image: "/virello-traits/key/nickel.png", rarity: 28 },
      { id: "painted", name: "Painted Key", image: "/virello-traits/key/painted.png", rarity: 28 },
    ],
  },
  {
    id: "spark",
    label: "Spark",
    blurb: "What flies off the works — flint, steam.",
    noneLabel: "Quiet Works",
    traits: [
      { id: "flint", name: "Flint Spark", image: "/virello-traits/spark/flint.png", rarity: 36 },
      { id: "steam", name: "Steam Puff", image: "/virello-traits/spark/steam.png", rarity: 24 },
    ],
  },
  {
    id: "wear",
    label: "Wear",
    blurb: "How the tin has lived — factory gloss, playroom scuff, rust bloom.",
    noneLabel: "Shop Fresh",
    traits: [
      { id: "factory", name: "Factory Gloss", image: "/virello-traits/wear/factory.png", rarity: 28 },
      { id: "scuff", name: "Playroom Scuff", image: "/virello-traits/wear/scuff.png", rarity: 24 },
      { id: "rust", name: "Rust Bloom", image: "/virello-traits/wear/rust.png", rarity: 20 },
    ],
  }
];

export const noneVirelloTrait: VirelloTrait = { id: "none", name: "None", rarity: 0 };

export function virelloCategoryById(id: VirelloTraitCategory["id"]) {
  const category = virelloTraitCategories.find((item) => item.id === id);
  if (!category) throw new Error(`Unknown Virello trait category: ${id}`);
  return category;
}

export function findVirelloTrait(categoryId: VirelloTraitCategory["id"], traitId: string) {
  if (traitId === "none") return noneVirelloTrait;
  return virelloCategoryById(categoryId).traits.find((trait) => trait.id === traitId);
}

export const defaultVirelloSelection = {
  bench: "linoleum",
  chassis: "robot",
  enamel: "tomato",
  decal: "star",
  key: "brass",
  spark: "flint",
  wear: "factory",
} as const;

export type VirelloSelection = Record<VirelloTraitCategory["id"], string>;

export function randomVirelloSelection(): VirelloSelection {
  const pick = (category: VirelloTraitCategory) => {
    const pool: VirelloTrait[] = category.noneLabel
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
    bench: pick(virelloCategoryById("bench")),
    chassis: pick(virelloCategoryById("chassis")),
    enamel: pick(virelloCategoryById("enamel")),
    decal: pick(virelloCategoryById("decal")),
    key: pick(virelloCategoryById("key")),
    spark: pick(virelloCategoryById("spark")),
    wear: pick(virelloCategoryById("wear")),
  };
}

export function virelloCombinationCount() {
  return virelloTraitCategories.reduce((product, category) => {
    const extra = category.noneLabel ? 1 : 0;
    return product * (category.traits.length + extra);
  }, 1);
}

export function virelloSelectionToLayers(selection: VirelloSelection) {
  return (["bench", "chassis", "enamel", "decal", "key", "spark", "wear"] as const)
    .map((id) => findVirelloTrait(id, selection[id]))
    .filter((trait): trait is VirelloTrait => Boolean(trait?.image))
    .map((trait) => virelloTraitSrc(trait.image));
}
