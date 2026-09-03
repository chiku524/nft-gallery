export type ShookumTrait = {
  id: string;
  name: string;
  image?: string;
  rarity: number;
};

export type ShookumTraitCategory = {
  id: "night" | "sheet" | "mug" | "hat" | "wrap" | "charm";
  label: string;
  blurb: string;
  noneLabel?: string;
  traits: ShookumTrait[];
};

/** Bump when APNG layers change so the studio does not keep a stale loop. */
export const SHOOKUM_ART_VERSION = "shookums-v4";

export const SHOOKUM_FRAMES = 12;
export const SHOOKUM_DURATION_MS = 90;

export function shookumTraitSrc(path?: string) {
  if (!path) return "";
  return `${path}?v=${SHOOKUM_ART_VERSION}`;
}

export const shookumTraitCategories: ShookumTraitCategory[] = [
  {
    id: "night",
    label: "Night",
    blurb: "A flat haunt field — parchment, pumpkin, midnight, blood moon. No desks.",
    traits: [
      { id: "parchment", name: "Parchment", image: "/shookums-traits/night/parchment.png", rarity: 14 },
      { id: "pumpkin", name: "Pumpkin", image: "/shookums-traits/night/pumpkin.png", rarity: 13 },
      { id: "blush", name: "Blush", image: "/shookums-traits/night/blush.png", rarity: 12 },
      { id: "midnight", name: "Midnight", image: "/shookums-traits/night/midnight.png", rarity: 12 },
      { id: "candy", name: "Candy", image: "/shookums-traits/night/candy.png", rarity: 11 },
      { id: "fog", name: "Fog", image: "/shookums-traits/night/fog.png", rarity: 10 },
      { id: "moss", name: "Graveyard", image: "/shookums-traits/night/moss.png", rarity: 9 },
      { id: "dusk", name: "Dusk", image: "/shookums-traits/night/dusk.png", rarity: 8 },
      { id: "bloodmoon", name: "Blood Moon", image: "/shookums-traits/night/bloodmoon.png", rarity: 7 },
      { id: "void", name: "Void", image: "/shookums-traits/night/void.png", rarity: 4 },
    ],
  },
  {
    id: "sheet",
    label: "Sheet",
    blurb: "The skeleton — three bodies only. Classic, blush, void. The hem never changes.",
    traits: [
      { id: "classic", name: "Classic", image: "/shookums-traits/sheet/classic.png", rarity: 55 },
      { id: "blush", name: "Blush", image: "/shookums-traits/sheet/blush.png", rarity: 28 },
      { id: "void", name: "Void", image: "/shookums-traits/sheet/void.png", rarity: 17 },
    ],
  },
  {
    id: "mug",
    label: "Mug",
    blurb: "Cutout-style glossy eyes on the same face points. Spooked, sleepy, a pink blep.",
    traits: [
      { id: "blink", name: "Normal", image: "/shookums-traits/mug/blink.png", rarity: 18 },
      { id: "spooked", name: "Spooked", image: "/shookums-traits/mug/spooked.png", rarity: 16 },
      { id: "blep", name: "Blep", image: "/shookums-traits/mug/blep.png", rarity: 14 },
      { id: "sleepy", name: "Sleepy", image: "/shookums-traits/mug/sleepy.png", rarity: 12 },
      { id: "wink", name: "Wink", image: "/shookums-traits/mug/wink.png", rarity: 10 },
      { id: "spark", name: "Sparkly", image: "/shookums-traits/mug/spark.png", rarity: 9 },
      { id: "angry", name: "Angry", image: "/shookums-traits/mug/angry.png", rarity: 7 },
      { id: "sad", name: "Sad", image: "/shookums-traits/mug/sad.png", rarity: 6 },
      { id: "starry", name: "Starry", image: "/shookums-traits/mug/starry.png", rarity: 5 },
      { id: "heart", name: "Heart", image: "/shookums-traits/mug/heart.png", rarity: 3 },
    ],
  },
  {
    id: "hat",
    label: "Hat",
    blurb: "Sits on the crown. Witch, pumpkin, cat ears, halo. The sheet is not cut.",
    noneLabel: "None",
    traits: [
      { id: "witch", name: "Witch", image: "/shookums-traits/hat/witch.png", rarity: 12 },
      { id: "bow", name: "Bow", image: "/shookums-traits/hat/bow.png", rarity: 11 },
      { id: "pumpkin", name: "Pumpkin", image: "/shookums-traits/hat/pumpkin.png", rarity: 10 },
      { id: "cat", name: "Cat Ears", image: "/shookums-traits/hat/cat.png", rarity: 9 },
      { id: "flower", name: "Flower", image: "/shookums-traits/hat/flower.png", rarity: 8 },
      { id: "party", name: "Party", image: "/shookums-traits/hat/party.png", rarity: 7 },
      { id: "halo", name: "Halo", image: "/shookums-traits/hat/halo.png", rarity: 6 },
      { id: "wizard", name: "Wizard", image: "/shookums-traits/hat/wizard.png", rarity: 5 },
      { id: "crown", name: "Crown", image: "/shookums-traits/hat/crown.png", rarity: 4 },
    ],
  },
  {
    id: "wrap",
    label: "Wrap",
    blurb: "Neck extras on the same collar line — chain, scarf, bowtie, cape.",
    noneLabel: "None",
    traits: [
      { id: "chain", name: "Chain", image: "/shookums-traits/wrap/chain.png", rarity: 16 },
      { id: "scarf", name: "Scarf", image: "/shookums-traits/wrap/scarf.png", rarity: 14 },
      { id: "bowtie", name: "Bowtie", image: "/shookums-traits/wrap/bowtie.png", rarity: 12 },
      { id: "pearls", name: "Pearls", image: "/shookums-traits/wrap/pearls.png", rarity: 10 },
      { id: "collar", name: "Collar", image: "/shookums-traits/wrap/collar.png", rarity: 8 },
      { id: "cape", name: "Cape", image: "/shookums-traits/wrap/cape.png", rarity: 6 },
    ],
  },
  {
    id: "charm",
    label: "Charm",
    blurb: "A held extra — pumpkin, candy, bat, broom. Floats beside the same hands.",
    noneLabel: "None",
    traits: [
      { id: "pumpkin", name: "Pumpkin", image: "/shookums-traits/charm/pumpkin.png", rarity: 14 },
      { id: "candy", name: "Candy", image: "/shookums-traits/charm/candy.png", rarity: 13 },
      { id: "bat", name: "Bat", image: "/shookums-traits/charm/bat.png", rarity: 11 },
      { id: "corn", name: "Candy Corn", image: "/shookums-traits/charm/corn.png", rarity: 10 },
      { id: "broom", name: "Broom", image: "/shookums-traits/charm/broom.png", rarity: 8 },
      { id: "potion", name: "Potion", image: "/shookums-traits/charm/potion.png", rarity: 7 },
      { id: "moon", name: "Moon", image: "/shookums-traits/charm/moon.png", rarity: 5 },
    ],
  },
];

export const noneShookumTrait: ShookumTrait = { id: "none", name: "None", rarity: 0 };

export function shookumCategoryById(id: ShookumTraitCategory["id"]) {
  const category = shookumTraitCategories.find((item) => item.id === id);
  if (!category) throw new Error(`Unknown Shook'um trait category: ${id}`);
  return category;
}

export function findShookumTrait(categoryId: ShookumTraitCategory["id"], traitId: string) {
  if (traitId === "none") return noneShookumTrait;
  return shookumCategoryById(categoryId).traits.find((trait) => trait.id === traitId);
}

export const defaultShookumSelection = {
  night: "parchment",
  sheet: "classic",
  mug: "blink",
  hat: "none",
  wrap: "none",
  charm: "none",
} as const;

export type ShookumSelection = Record<ShookumTraitCategory["id"], string>;

export function randomShookumSelection(): ShookumSelection {
  const pick = (category: ShookumTraitCategory) => {
    const pool: ShookumTrait[] = category.noneLabel
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
    night: pick(shookumCategoryById("night")),
    sheet: pick(shookumCategoryById("sheet")),
    mug: pick(shookumCategoryById("mug")),
    hat: pick(shookumCategoryById("hat")),
    wrap: pick(shookumCategoryById("wrap")),
    charm: pick(shookumCategoryById("charm")),
  };
}

export function shookumCombinationCount() {
  return shookumTraitCategories.reduce((product, category) => {
    const extra = category.noneLabel ? 1 : 0;
    return product * (category.traits.length + extra);
  }, 1);
}

export function shookumSelectionToLayers(selection: ShookumSelection) {
  return (["night", "sheet", "mug", "hat", "wrap", "charm"] as const)
    .map((id) => findShookumTrait(id, selection[id]))
    .filter((trait): trait is ShookumTrait => Boolean(trait?.image))
    .map((trait) => shookumTraitSrc(trait.image));
}
