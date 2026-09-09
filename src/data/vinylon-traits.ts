export type VinylonTrait = {
  id: string;
  name: string;
  image?: string;
  rarity: number;
};

export type VinylonTraitCategory = {
  id: "booth" | "latex" | "twist" | "knot" | "valve" | "gleam" | "confetti";
  label: string;
  blurb: string;
  noneLabel?: string;
  traits: VinylonTrait[];
};

export const VNYL_ART_VERSION = "vinylon-v1";

export const VNYL_FRAMES = 12;
export const VNYL_DURATION_MS = 90;

export function vinylonTraitSrc(path?: string) {
  if (!path) return "";
  return `${path}?v=${VNYL_ART_VERSION}`;
}

export const vinylonTraitCategories: VinylonTraitCategory[] = [
  {
    id: "booth",
    label: "Booth",
    blurb: "The party wall — curtain, tile, night, circus, stripe, dusk, paper, plaid.",
    traits: [
      { id: "curtain", name: "Curtain Booth", image: "/vinylon-traits/booth/curtain.png", rarity: 16 },
      { id: "tile", name: "Tile Booth", image: "/vinylon-traits/booth/tile.png", rarity: 14 },
      { id: "night", name: "Night Booth", image: "/vinylon-traits/booth/night.png", rarity: 14 },
      { id: "circus", name: "Circus Booth", image: "/vinylon-traits/booth/circus.png", rarity: 14 },
      { id: "stripe", name: "Stripe Booth", image: "/vinylon-traits/booth/stripe.png", rarity: 12 },
      { id: "dusk", name: "Dusk Booth", image: "/vinylon-traits/booth/dusk.png", rarity: 12 },
      { id: "paper", name: "Paper Booth", image: "/vinylon-traits/booth/paper.png", rarity: 10 },
      { id: "plaid", name: "Plaid Booth", image: "/vinylon-traits/booth/plaid.png", rarity: 8 },
    ],
  },
  {
    id: "latex",
    label: "Latex",
    blurb: "The inflated body — red, yellow, blue, pink, green, orange, white, purple.",
    traits: [
      { id: "red", name: "Red Latex", image: "/vinylon-traits/latex/red.png", rarity: 16 },
      { id: "yellow", name: "Yellow Latex", image: "/vinylon-traits/latex/yellow.png", rarity: 14 },
      { id: "blue", name: "Blue Latex", image: "/vinylon-traits/latex/blue.png", rarity: 14 },
      { id: "pink", name: "Pink Latex", image: "/vinylon-traits/latex/pink.png", rarity: 14 },
      { id: "green", name: "Green Latex", image: "/vinylon-traits/latex/green.png", rarity: 12 },
      { id: "orange", name: "Orange Latex", image: "/vinylon-traits/latex/orange.png", rarity: 12 },
      { id: "white", name: "White Latex", image: "/vinylon-traits/latex/white.png", rarity: 10 },
      { id: "purple", name: "Purple Latex", image: "/vinylon-traits/latex/purple.png", rarity: 8 },
    ],
  },
  {
    id: "twist",
    label: "Twist",
    blurb: "The dancing balloon. Eight twists: hound, hare, steed, swan, monkey, dino, poodle, figure.",
    traits: [
      { id: "hound", name: "Hound Twist", image: "/vinylon-traits/twist/hound.png", rarity: 16 },
      { id: "hare", name: "Hare Twist", image: "/vinylon-traits/twist/hare.png", rarity: 14 },
      { id: "steed", name: "Steed Twist", image: "/vinylon-traits/twist/steed.png", rarity: 14 },
      { id: "swan", name: "Swan Twist", image: "/vinylon-traits/twist/swan.png", rarity: 12 },
      { id: "monkey", name: "Monkey Twist", image: "/vinylon-traits/twist/monkey.png", rarity: 12 },
      { id: "dino", name: "Dino Twist", image: "/vinylon-traits/twist/dino.png", rarity: 12 },
      { id: "poodle", name: "Poodle Twist", image: "/vinylon-traits/twist/poodle.png", rarity: 10 },
      { id: "figure", name: "Figure Twist", image: "/vinylon-traits/twist/figure.png", rarity: 10 },
    ],
  },
  {
    id: "knot",
    label: "Knot",
    blurb: "A tied pinch — ear, waist, nose — or an untied tube.",
    noneLabel: "No Knot",
    traits: [
      { id: "ear", name: "Ear Knot", image: "/vinylon-traits/knot/ear.png", rarity: 28 },
      { id: "waist", name: "Waist Knot", image: "/vinylon-traits/knot/waist.png", rarity: 26 },
      { id: "nose", name: "Nose Knot", image: "/vinylon-traits/knot/nose.png", rarity: 22 },
    ],
  },
  {
    id: "valve",
    label: "Valve",
    blurb: "The inflation nozzle — silver, gold, black — or a sealed end.",
    noneLabel: "No Valve",
    traits: [
      { id: "silver", name: "Silver Valve", image: "/vinylon-traits/valve/silver.png", rarity: 28 },
      { id: "gold", name: "Gold Valve", image: "/vinylon-traits/valve/gold.png", rarity: 24 },
      { id: "black", name: "Black Valve", image: "/vinylon-traits/valve/black.png", rarity: 20 },
    ],
  },
  {
    id: "gleam",
    label: "Gleam",
    blurb: "Specular shine on the latex — tight, wide — or matte.",
    noneLabel: "Matte",
    traits: [
      { id: "tight", name: "Tight Gleam", image: "/vinylon-traits/gleam/tight.png", rarity: 40 },
      { id: "wide", name: "Wide Gleam", image: "/vinylon-traits/gleam/wide.png", rarity: 32 },
    ],
  },
  {
    id: "confetti",
    label: "Confetti",
    blurb: "Air in the booth — dots, stream, mix — or clear air.",
    noneLabel: "Clear Air",
    traits: [
      { id: "dots", name: "Dot Confetti", image: "/vinylon-traits/confetti/dots.png", rarity: 26 },
      { id: "stream", name: "Stream Confetti", image: "/vinylon-traits/confetti/stream.png", rarity: 22 },
      { id: "mix", name: "Mix Confetti", image: "/vinylon-traits/confetti/mix.png", rarity: 18 },
    ],
  }
];

export const noneVinylonTrait: VinylonTrait = { id: "none", name: "None", rarity: 0 };

export function vinylonCategoryById(id: VinylonTraitCategory["id"]) {
  const category = vinylonTraitCategories.find((item) => item.id === id);
  if (!category) throw new Error(`Unknown Vinylon trait category: ${id}`);
  return category;
}

export function findVinylonTrait(categoryId: VinylonTraitCategory["id"], traitId: string) {
  if (traitId === "none") return noneVinylonTrait;
  return vinylonCategoryById(categoryId).traits.find((trait) => trait.id === traitId);
}

export const defaultVinylonSelection = {
  booth: "curtain",
  latex: "red",
  twist: "hound",
  knot: "ear",
  valve: "silver",
  gleam: "tight",
  confetti: "dots",
} as const;

export type VinylonSelection = Record<VinylonTraitCategory["id"], string>;

export function randomVinylonSelection(): VinylonSelection {
  const pick = (category: VinylonTraitCategory) => {
    const pool: VinylonTrait[] = category.noneLabel ? [{ id: "none", name: category.noneLabel, rarity: 22 }, ...category.traits] : category.traits;
    const total = pool.reduce((sum, trait) => sum + Math.max(trait.rarity, 1), 0);
    let roll = Math.random() * total;
    for (const trait of pool) {
      roll -= Math.max(trait.rarity, 1);
      if (roll <= 0) return trait.id;
    }
    return pool[0].id;
  };
  return {
    booth: pick(vinylonCategoryById("booth")),
    latex: pick(vinylonCategoryById("latex")),
    twist: pick(vinylonCategoryById("twist")),
    knot: pick(vinylonCategoryById("knot")),
    valve: pick(vinylonCategoryById("valve")),
    gleam: pick(vinylonCategoryById("gleam")),
    confetti: pick(vinylonCategoryById("confetti")),
  };
}

export function vinylonCombinationCount() {
  return vinylonTraitCategories.reduce((product, category) => {
    const extra = category.noneLabel ? 1 : 0;
    return product * (category.traits.length + extra);
  }, 1);
}

export function vinylonSelectionToLayers(selection: VinylonSelection) {
  return (["booth", "latex", "twist", "knot", "valve", "gleam", "confetti"] as const)
    .map((id) => findVinylonTrait(id, selection[id]))
    .filter((trait): trait is VinylonTrait => Boolean(trait?.image))
    .map((trait) => vinylonTraitSrc(trait.image));
}
