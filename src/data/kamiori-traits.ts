export type KamioriTrait = {
  id: string;
  name: string;
  image?: string;
  rarity: number;
};

export type KamioriTraitCategory = {
  id: "pulp" | "fleck" | "fold" | "score" | "facet" | "seal" | "draft";
  label: string;
  blurb: string;
  noneLabel?: string;
  traits: KamioriTrait[];
};

/** Bump when APNG layers change so the studio does not keep a stale loop. */
export const KAMIORI_ART_VERSION = "kamiori-v1";

export const KAMIORI_FRAMES = 12;
export const KAMIORI_DURATION_MS = 90;

export function kamioriTraitSrc(path?: string) {
  if (!path) return "";
  return `${path}?v=${KAMIORI_ART_VERSION}`;
}

export const kamioriTraitCategories: KamioriTraitCategory[] = [
  {
    id: "pulp",
    label: "Pulp",
    blurb: "Deckle washi — cream, indigo, vermilion, moss, peach, gold, ink, frost.",
    traits: [
      { id: "cream", name: "Cream Washi", image: "/kamiori-traits/pulp/cream.png", rarity: 18 },
      { id: "indigo", name: "Indigo Washi", image: "/kamiori-traits/pulp/indigo.png", rarity: 14 },
      { id: "vermilion", name: "Vermilion Washi", image: "/kamiori-traits/pulp/vermilion.png", rarity: 12 },
      { id: "moss", name: "Moss Washi", image: "/kamiori-traits/pulp/moss.png", rarity: 12 },
      { id: "peach", name: "Peach Washi", image: "/kamiori-traits/pulp/peach.png", rarity: 12 },
      { id: "gold", name: "Gold Washi", image: "/kamiori-traits/pulp/gold.png", rarity: 12 },
      { id: "ink", name: "Ink Washi", image: "/kamiori-traits/pulp/ink.png", rarity: 10 },
      { id: "frost", name: "Frost Washi", image: "/kamiori-traits/pulp/frost.png", rarity: 10 },
    ],
  },
  {
    id: "fleck",
    label: "Fleck",
    blurb: "Paper tooth — kozo fiber, gold dust, speckle, laid stripe, cloud wash — or a plain sheet.",
    noneLabel: "Plain Sheet",
    traits: [
      { id: "kozo", name: "Kozo Fiber", image: "/kamiori-traits/fleck/kozo.png", rarity: 18 },
      { id: "golddust", name: "Gold Dust", image: "/kamiori-traits/fleck/golddust.png", rarity: 16 },
      { id: "speckle", name: "Speckle", image: "/kamiori-traits/fleck/speckle.png", rarity: 16 },
      { id: "stripe", name: "Laid Stripe", image: "/kamiori-traits/fleck/stripe.png", rarity: 14 },
      { id: "cloud", name: "Cloud Wash", image: "/kamiori-traits/fleck/cloud.png", rarity: 12 },
    ],
  },
  {
    id: "fold",
    label: "Fold",
    blurb: "The seated origami. Eight folds: crane, frog, beetle, boat, hare, fan, kite, lotus.",
    traits: [
      { id: "crane", name: "Crane", image: "/kamiori-traits/fold/crane.png", rarity: 18 },
      { id: "frog", name: "Frog", image: "/kamiori-traits/fold/frog.png", rarity: 16 },
      { id: "beetle", name: "Beetle", image: "/kamiori-traits/fold/beetle.png", rarity: 14 },
      { id: "boat", name: "Boat", image: "/kamiori-traits/fold/boat.png", rarity: 14 },
      { id: "hare", name: "Hare", image: "/kamiori-traits/fold/hare.png", rarity: 12 },
      { id: "fan", name: "Fan", image: "/kamiori-traits/fold/fan.png", rarity: 10 },
      { id: "kite", name: "Kite", image: "/kamiori-traits/fold/kite.png", rarity: 8 },
      { id: "lotus", name: "Lotus", image: "/kamiori-traits/fold/lotus.png", rarity: 8 },
    ],
  },
  {
    id: "score",
    label: "Score",
    blurb: "Crease language — mountain, valley, diagram, radial, grid — or unmarked paper.",
    noneLabel: "No Score",
    traits: [
      { id: "mountain", name: "Mountain Fold", image: "/kamiori-traits/score/mountain.png", rarity: 18 },
      { id: "valley", name: "Valley Fold", image: "/kamiori-traits/score/valley.png", rarity: 18 },
      { id: "diagram", name: "Crease Diagram", image: "/kamiori-traits/score/diagram.png", rarity: 16 },
      { id: "radial", name: "Radial Score", image: "/kamiori-traits/score/radial.png", rarity: 14 },
      { id: "grid", name: "Grid Score", image: "/kamiori-traits/score/grid.png", rarity: 12 },
    ],
  },
  {
    id: "facet",
    label: "Facet",
    blurb: "A second dye on one plane — wing, body, tip, band, gore — or a bare facet.",
    noneLabel: "Bare Facet",
    traits: [
      { id: "wing", name: "Wing Wash", image: "/kamiori-traits/facet/wing.png", rarity: 18 },
      { id: "body", name: "Body Wash", image: "/kamiori-traits/facet/body.png", rarity: 16 },
      { id: "tip", name: "Tip Wash", image: "/kamiori-traits/facet/tip.png", rarity: 16 },
      { id: "band", name: "Band Wash", image: "/kamiori-traits/facet/band.png", rarity: 14 },
      { id: "gore", name: "Gore Wash", image: "/kamiori-traits/facet/gore.png", rarity: 12 },
    ],
  },
  {
    id: "seal",
    label: "Seal",
    blurb: "A mark that stays put — hanko, twin cord, mizuhiki loop, tassel — or no seal.",
    noneLabel: "No Seal",
    traits: [
      { id: "hanko", name: "Hanko", image: "/kamiori-traits/seal/hanko.png", rarity: 20 },
      { id: "twin", name: "Twin Cord", image: "/kamiori-traits/seal/twin.png", rarity: 18 },
      { id: "loop", name: "Mizuhiki Loop", image: "/kamiori-traits/seal/loop.png", rarity: 18 },
      { id: "tassel", name: "Tassel", image: "/kamiori-traits/seal/tassel.png", rarity: 18 },
    ],
  },
  {
    id: "draft",
    label: "Draft",
    blurb: "Air on the sheet — corner lift, flutter, loose scrap, gust — or still air.",
    noneLabel: "Still Air",
    traits: [
      { id: "lift", name: "Corner Lift", image: "/kamiori-traits/draft/lift.png", rarity: 22 },
      { id: "flutter", name: "Flutter", image: "/kamiori-traits/draft/flutter.png", rarity: 20 },
      { id: "scrap", name: "Loose Scrap", image: "/kamiori-traits/draft/scrap.png", rarity: 18 },
      { id: "gust", name: "Gust", image: "/kamiori-traits/draft/gust.png", rarity: 18 },
    ],
  }
];

export const noneKamioriTrait: KamioriTrait = { id: "none", name: "None", rarity: 0 };

export function kamioriCategoryById(id: KamioriTraitCategory["id"]) {
  const category = kamioriTraitCategories.find((item) => item.id === id);
  if (!category) throw new Error(`Unknown Kamiori trait category: ${id}`);
  return category;
}

export function findKamioriTrait(categoryId: KamioriTraitCategory["id"], traitId: string) {
  if (traitId === "none") return noneKamioriTrait;
  return kamioriCategoryById(categoryId).traits.find((trait) => trait.id === traitId);
}

export const defaultKamioriSelection = {
  pulp: "cream",
  fleck: "kozo",
  fold: "crane",
  score: "mountain",
  facet: "none",
  seal: "hanko",
  draft: "lift",
} as const;

export type KamioriSelection = Record<KamioriTraitCategory["id"], string>;

export function randomKamioriSelection(): KamioriSelection {
  const pick = (category: KamioriTraitCategory) => {
    const pool: KamioriTrait[] = category.noneLabel
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
    pulp: pick(kamioriCategoryById("pulp")),
    fleck: pick(kamioriCategoryById("fleck")),
    fold: pick(kamioriCategoryById("fold")),
    score: pick(kamioriCategoryById("score")),
    facet: pick(kamioriCategoryById("facet")),
    seal: pick(kamioriCategoryById("seal")),
    draft: pick(kamioriCategoryById("draft")),
  };
}

export function kamioriCombinationCount() {
  return kamioriTraitCategories.reduce((product, category) => {
    const extra = category.noneLabel ? 1 : 0;
    return product * (category.traits.length + extra);
  }, 1);
}

export function kamioriSelectionToLayers(selection: KamioriSelection) {
  return (["pulp", "fleck", "fold", "score", "facet", "seal", "draft"] as const)
    .map((id) => findKamioriTrait(id, selection[id]))
    .filter((trait): trait is KamioriTrait => Boolean(trait?.image))
    .map((trait) => kamioriTraitSrc(trait.image));
}
