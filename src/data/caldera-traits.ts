export type CalderaTrait = {
  id: string;
  name: string;
  image?: string;
  rarity: number;
};

export type CalderaTraitCategory = {
  id: "cloth" | "sleeve" | "inn" | "comb" | "strike" | "flame" | "mark";
  label: string;
  blurb: string;
  noneLabel?: string;
  traits: CalderaTrait[];
};

/** Bump when APNG layers change so the studio does not keep a stale loop. */
export const CALDERA_ART_VERSION = "caldera-v1";

export const CALDERA_FRAMES = 12;
export const CALDERA_DURATION_MS = 90;

export function calderaTraitSrc(path?: string) {
  if (!path) return "";
  return `${path}?v=${CALDERA_ART_VERSION}`;
}

export const calderaTraitCategories: CalderaTraitCategory[] = [
  {
    id: "cloth",
    label: "Cloth",
    blurb: "The cafe table — check, linen, vinyl, bar, stone.",
    traits: [
      { id: "check", name: "Check Cloth", image: "/caldera-traits/cloth/check.png", rarity: 22 },
      { id: "linen", name: "Linen Cloth", image: "/caldera-traits/cloth/linen.png", rarity: 22 },
      { id: "vinyl", name: "Vinyl Cloth", image: "/caldera-traits/cloth/vinyl.png", rarity: 20 },
      { id: "bar", name: "Bar Cloth", image: "/caldera-traits/cloth/bar.png", rarity: 18 },
      { id: "stone", name: "Stone Cloth", image: "/caldera-traits/cloth/stone.png", rarity: 18 },
    ],
  },
  {
    id: "sleeve",
    label: "Sleeve",
    blurb: "The cardboard stock — kraft, ivory, crimson, navy, black, mint.",
    traits: [
      { id: "kraft", name: "Kraft Sleeve", image: "/caldera-traits/sleeve/kraft.png", rarity: 20 },
      { id: "ivory", name: "Ivory Sleeve", image: "/caldera-traits/sleeve/ivory.png", rarity: 18 },
      { id: "crimson", name: "Crimson Sleeve", image: "/caldera-traits/sleeve/crimson.png", rarity: 16 },
      { id: "navy", name: "Navy Sleeve", image: "/caldera-traits/sleeve/navy.png", rarity: 16 },
      { id: "black", name: "Black Sleeve", image: "/caldera-traits/sleeve/black.png", rarity: 16 },
      { id: "mint", name: "Mint Sleeve", image: "/caldera-traits/sleeve/mint.png", rarity: 14 },
    ],
  },
  {
    id: "inn",
    label: "Inn",
    blurb: "The printed hotel — cactus, lodge, diner, buoy, crown, shield, palm, ticket.",
    traits: [
      { id: "cactus", name: "Cactus Inn", image: "/caldera-traits/inn/cactus.png", rarity: 16 },
      { id: "lodge", name: "Lodge Inn", image: "/caldera-traits/inn/lodge.png", rarity: 14 },
      { id: "diner", name: "Diner Inn", image: "/caldera-traits/inn/diner.png", rarity: 14 },
      { id: "buoy", name: "Buoy Inn", image: "/caldera-traits/inn/buoy.png", rarity: 12 },
      { id: "crown", name: "Crown Inn", image: "/caldera-traits/inn/crown.png", rarity: 12 },
      { id: "shield", name: "Shield Inn", image: "/caldera-traits/inn/shield.png", rarity: 12 },
      { id: "palm", name: "Palm Inn", image: "/caldera-traits/inn/palm.png", rarity: 10 },
      { id: "ticket", name: "Ticket Inn", image: "/caldera-traits/inn/ticket.png", rarity: 10 },
    ],
  },
  {
    id: "comb",
    label: "Comb",
    blurb: "The matches in the book — white, kraft, ebony, candy.",
    traits: [
      { id: "white", name: "White Comb", image: "/caldera-traits/comb/white.png", rarity: 28 },
      { id: "kraft", name: "Kraft Comb", image: "/caldera-traits/comb/kraft.png", rarity: 26 },
      { id: "ebony", name: "Ebony Comb", image: "/caldera-traits/comb/ebony.png", rarity: 24 },
      { id: "candy", name: "Candy Comb", image: "/caldera-traits/comb/candy.png", rarity: 22 },
    ],
  },
  {
    id: "strike",
    label: "Strike",
    blurb: "The phosphor strip — grit, red phosphor, black.",
    traits: [
      { id: "grit", name: "Grit Strike", image: "/caldera-traits/strike/grit.png", rarity: 36 },
      { id: "redphos", name: "Red Phosphor", image: "/caldera-traits/strike/redphos.png", rarity: 34 },
      { id: "black", name: "Black Strike", image: "/caldera-traits/strike/black.png", rarity: 30 },
    ],
  },
  {
    id: "flame",
    label: "Flame",
    blurb: "What burns — gold, blue, tall, ember. The flame is the loop.",
    traits: [
      { id: "gold", name: "Gold Flame", image: "/caldera-traits/flame/gold.png", rarity: 32 },
      { id: "blue", name: "Blue Flame", image: "/caldera-traits/flame/blue.png", rarity: 24 },
      { id: "tall", name: "Tall Flame", image: "/caldera-traits/flame/tall.png", rarity: 24 },
      { id: "ember", name: "Ember Flame", image: "/caldera-traits/flame/ember.png", rarity: 20 },
    ],
  },
  {
    id: "mark",
    label: "Mark",
    blurb: "A room stamp, foil seal, or crest.",
    noneLabel: "No Mark",
    traits: [
      { id: "room", name: "Room Mark", image: "/caldera-traits/mark/room.png", rarity: 26 },
      { id: "foil", name: "Foil Mark", image: "/caldera-traits/mark/foil.png", rarity: 24 },
      { id: "crest", name: "Crest Mark", image: "/caldera-traits/mark/crest.png", rarity: 22 },
    ],
  }
];

export const noneCalderaTrait: CalderaTrait = { id: "none", name: "None", rarity: 0 };

export function calderaCategoryById(id: CalderaTraitCategory["id"]) {
  const category = calderaTraitCategories.find((item) => item.id === id);
  if (!category) throw new Error(`Unknown Caldera trait category: ${id}`);
  return category;
}

export function findCalderaTrait(categoryId: CalderaTraitCategory["id"], traitId: string) {
  if (traitId === "none") return noneCalderaTrait;
  return calderaCategoryById(categoryId).traits.find((trait) => trait.id === traitId);
}

export const defaultCalderaSelection = {
  cloth: "check",
  sleeve: "kraft",
  inn: "cactus",
  comb: "white",
  strike: "grit",
  flame: "gold",
  mark: "room",
} as const;

export type CalderaSelection = Record<CalderaTraitCategory["id"], string>;

export function randomCalderaSelection(): CalderaSelection {
  const pick = (category: CalderaTraitCategory) => {
    const pool: CalderaTrait[] = category.noneLabel
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
    cloth: pick(calderaCategoryById("cloth")),
    sleeve: pick(calderaCategoryById("sleeve")),
    inn: pick(calderaCategoryById("inn")),
    comb: pick(calderaCategoryById("comb")),
    strike: pick(calderaCategoryById("strike")),
    flame: pick(calderaCategoryById("flame")),
    mark: pick(calderaCategoryById("mark")),
  };
}

export function calderaCombinationCount() {
  return calderaTraitCategories.reduce((product, category) => {
    const extra = category.noneLabel ? 1 : 0;
    return product * (category.traits.length + extra);
  }, 1);
}

export function calderaSelectionToLayers(selection: CalderaSelection) {
  return (["cloth", "sleeve", "inn", "comb", "strike", "flame", "mark"] as const)
    .map((id) => findCalderaTrait(id, selection[id]))
    .filter((trait): trait is CalderaTrait => Boolean(trait?.image))
    .map((trait) => calderaTraitSrc(trait.image));
}
