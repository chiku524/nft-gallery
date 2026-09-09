export type FeltroTrait = {
  id: string;
  name: string;
  image?: string;
  rarity: number;
};

export type FeltroTraitCategory = {
  id: "gym" | "suit" | "nap" | "mesh" | "seam" | "crest" | "fuzz";
  label: string;
  blurb: string;
  noneLabel?: string;
  traits: FeltroTrait[];
};

export const FLTR_ART_VERSION = "feltro-v1";

export const FLTR_FRAMES = 12;
export const FLTR_DURATION_MS = 90;

export function feltroTraitSrc(path?: string) {
  if (!path) return "";
  return `${path}?v=${FLTR_ART_VERSION}`;
}

export const feltroTraitCategories: FeltroTraitCategory[] = [
  {
    id: "gym",
    label: "Gym",
    blurb: "The floor under the suit — maple, linoleum, turf, court, night, mat, clay, vinyl.",
    traits: [
      { id: "maple", name: "Maple Court", image: "/feltro-traits/gym/maple.png", rarity: 18 },
      { id: "linoleum", name: "Linoleum Court", image: "/feltro-traits/gym/linoleum.png", rarity: 16 },
      { id: "turf", name: "Turf Court", image: "/feltro-traits/gym/turf.png", rarity: 14 },
      { id: "court", name: "Wood Court", image: "/feltro-traits/gym/court.png", rarity: 14 },
      { id: "night", name: "Night Court", image: "/feltro-traits/gym/night.png", rarity: 12 },
      { id: "mat", name: "Mat Court", image: "/feltro-traits/gym/mat.png", rarity: 10 },
      { id: "clay", name: "Clay Court", image: "/feltro-traits/gym/clay.png", rarity: 8 },
      { id: "vinyl", name: "Vinyl Court", image: "/feltro-traits/gym/vinyl.png", rarity: 8 },
    ],
  },
  {
    id: "suit",
    label: "Suit",
    blurb: "The dancing mascot. Eight foam suits: bear, lion, frog, bunny, dino, wolf, octopus, shark.",
    traits: [
      { id: "bear", name: "Bear Suit", image: "/feltro-traits/suit/bear.png", rarity: 16 },
      { id: "lion", name: "Lion Suit", image: "/feltro-traits/suit/lion.png", rarity: 14 },
      { id: "frog", name: "Frog Suit", image: "/feltro-traits/suit/frog.png", rarity: 14 },
      { id: "bunny", name: "Bunny Suit", image: "/feltro-traits/suit/bunny.png", rarity: 14 },
      { id: "dino", name: "Dino Suit", image: "/feltro-traits/suit/dino.png", rarity: 12 },
      { id: "wolf", name: "Wolf Suit", image: "/feltro-traits/suit/wolf.png", rarity: 12 },
      { id: "octopus", name: "Octopus Suit", image: "/feltro-traits/suit/octopus.png", rarity: 10 },
      { id: "shark", name: "Shark Suit", image: "/feltro-traits/suit/shark.png", rarity: 8 },
    ],
  },
  {
    id: "nap",
    label: "Nap",
    blurb: "Felt pile on the cylinder — down, cross, tight, swirl.",
    traits: [
      { id: "down", name: "Down Nap", image: "/feltro-traits/nap/down.png", rarity: 30 },
      { id: "cross", name: "Cross Nap", image: "/feltro-traits/nap/cross.png", rarity: 26 },
      { id: "tight", name: "Tight Nap", image: "/feltro-traits/nap/tight.png", rarity: 24 },
      { id: "swirl", name: "Swirl Nap", image: "/feltro-traits/nap/swirl.png", rarity: 20 },
    ],
  },
  {
    id: "mesh",
    label: "Mesh",
    blurb: "The eye screen — round, visor, button, slit.",
    traits: [
      { id: "round", name: "Round Mesh", image: "/feltro-traits/mesh/round.png", rarity: 32 },
      { id: "visor", name: "Visor Mesh", image: "/feltro-traits/mesh/visor.png", rarity: 28 },
      { id: "button", name: "Button Eyes", image: "/feltro-traits/mesh/button.png", rarity: 22 },
      { id: "slit", name: "Slit Mesh", image: "/feltro-traits/mesh/slit.png", rarity: 18 },
    ],
  },
  {
    id: "seam",
    label: "Seam",
    blurb: "Stitch down the foam — white, black, gold, contrast.",
    traits: [
      { id: "white", name: "White Seam", image: "/feltro-traits/seam/white.png", rarity: 32 },
      { id: "black", name: "Black Seam", image: "/feltro-traits/seam/black.png", rarity: 28 },
      { id: "gold", name: "Gold Seam", image: "/feltro-traits/seam/gold.png", rarity: 22 },
      { id: "contrast", name: "Contrast Seam", image: "/feltro-traits/seam/contrast.png", rarity: 18 },
    ],
  },
  {
    id: "crest",
    label: "Crest",
    blurb: "A badge on the chest — star, patch, letter, badge — or bare foam.",
    noneLabel: "No Crest",
    traits: [
      { id: "star", name: "Star Crest", image: "/feltro-traits/crest/star.png", rarity: 22 },
      { id: "patch", name: "Patch Crest", image: "/feltro-traits/crest/patch.png", rarity: 20 },
      { id: "letter", name: "Letter Crest", image: "/feltro-traits/crest/letter.png", rarity: 16 },
      { id: "badge", name: "Badge Crest", image: "/feltro-traits/crest/badge.png", rarity: 14 },
    ],
  },
  {
    id: "fuzz",
    label: "Fuzz",
    blurb: "Loose fibers in the air — loose, halo, drift — or clean air.",
    noneLabel: "Clean Air",
    traits: [
      { id: "loose", name: "Loose Fuzz", image: "/feltro-traits/fuzz/loose.png", rarity: 26 },
      { id: "halo", name: "Halo Fuzz", image: "/feltro-traits/fuzz/halo.png", rarity: 22 },
      { id: "drift", name: "Drift Fuzz", image: "/feltro-traits/fuzz/drift.png", rarity: 18 },
    ],
  }
];

export const noneFeltroTrait: FeltroTrait = { id: "none", name: "None", rarity: 0 };

export function feltroCategoryById(id: FeltroTraitCategory["id"]) {
  const category = feltroTraitCategories.find((item) => item.id === id);
  if (!category) throw new Error(`Unknown Feltro trait category: ${id}`);
  return category;
}

export function findFeltroTrait(categoryId: FeltroTraitCategory["id"], traitId: string) {
  if (traitId === "none") return noneFeltroTrait;
  return feltroCategoryById(categoryId).traits.find((trait) => trait.id === traitId);
}

export const defaultFeltroSelection = {
  gym: "maple",
  suit: "bear",
  nap: "down",
  mesh: "round",
  seam: "white",
  crest: "star",
  fuzz: "loose",
} as const;

export type FeltroSelection = Record<FeltroTraitCategory["id"], string>;

export function randomFeltroSelection(): FeltroSelection {
  const pick = (category: FeltroTraitCategory) => {
    const pool: FeltroTrait[] = category.noneLabel
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
    gym: pick(feltroCategoryById("gym")),
    suit: pick(feltroCategoryById("suit")),
    nap: pick(feltroCategoryById("nap")),
    mesh: pick(feltroCategoryById("mesh")),
    seam: pick(feltroCategoryById("seam")),
    crest: pick(feltroCategoryById("crest")),
    fuzz: pick(feltroCategoryById("fuzz")),
  };
}

export function feltroCombinationCount() {
  return feltroTraitCategories.reduce((product, category) => {
    const extra = category.noneLabel ? 1 : 0;
    return product * (category.traits.length + extra);
  }, 1);
}

export function feltroSelectionToLayers(selection: FeltroSelection) {
  return (["gym", "suit", "nap", "mesh", "seam", "crest", "fuzz"] as const)
    .map((id) => findFeltroTrait(id, selection[id]))
    .filter((trait): trait is FeltroTrait => Boolean(trait?.image))
    .map((trait) => feltroTraitSrc(trait.image));
}
