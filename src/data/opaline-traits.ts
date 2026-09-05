export type OpalineTrait = {
  id: string;
  name: string;
  image?: string;
  rarity: number;
};

export type OpalineTraitCategory = {
  id: "atelier" | "cast" | "sheen" | "regard" | "crest" | "clasp";
  label: string;
  blurb: string;
  noneLabel?: string;
  traits: OpalineTrait[];
};

/** Bump when APNG layers change so the studio does not keep a stale loop. */
export const OPALINE_ART_VERSION = "opaline-v1";

export const OPALINE_FRAMES = 12;
export const OPALINE_DURATION_MS = 90;

export function opalineTraitSrc(path?: string) {
  if (!path) return "";
  return `${path}?v=${OPALINE_ART_VERSION}`;
}

export const opalineTraitCategories: OpalineTraitCategory[] = [
  {
    id: "atelier",
    label: "Atelier",
    blurb: "The studio — obsidian, slate, dusk, ivory gallery, mercury, wine, brine, quartz.",
    traits: [
      { id: "obsidian", name: "Obsidian Room", image: "/opaline-traits/atelier/obsidian.png", rarity: 16 },
      { id: "slate", name: "Slate Studio", image: "/opaline-traits/atelier/slate.png", rarity: 16 },
      { id: "dusk", name: "Dusk Chamber", image: "/opaline-traits/atelier/dusk.png", rarity: 14 },
      { id: "ivory", name: "Ivory Gallery", image: "/opaline-traits/atelier/ivory.png", rarity: 14 },
      { id: "mercury", name: "Mercury Wall", image: "/opaline-traits/atelier/mercury.png", rarity: 12 },
      { id: "wine", name: "Wine Vault", image: "/opaline-traits/atelier/wine.png", rarity: 10 },
      { id: "brine", name: "Brine Hall", image: "/opaline-traits/atelier/brine.png", rarity: 10 },
      { id: "quartz", name: "Quartz Court", image: "/opaline-traits/atelier/quartz.png", rarity: 8 },
    ],
  },
  {
    id: "cast",
    label: "Cast",
    blurb: "The seated crystal bust — eight smoked-glass recipes. Flat crown, angular jaw, column neck.",
    traits: [
      { id: "smoke", name: "Smoke Glass", image: "/opaline-traits/cast/smoke.png", rarity: 18 },
      { id: "champagne", name: "Champagne Glass", image: "/opaline-traits/cast/champagne.png", rarity: 16 },
      { id: "amethyst", name: "Amethyst Glass", image: "/opaline-traits/cast/amethyst.png", rarity: 14 },
      { id: "tide", name: "Tide Glass", image: "/opaline-traits/cast/tide.png", rarity: 14 },
      { id: "ink", name: "Ink Glass", image: "/opaline-traits/cast/ink.png", rarity: 12 },
      { id: "frost", name: "Frost Glass", image: "/opaline-traits/cast/frost.png", rarity: 10 },
      { id: "ember", name: "Ember Glass", image: "/opaline-traits/cast/ember.png", rarity: 8 },
      { id: "jade", name: "Jade Glass", image: "/opaline-traits/cast/jade.png", rarity: 8 },
    ],
  },
  {
    id: "sheen",
    label: "Sheen",
    blurb: "Dichroic film on the same facets. Oil, aurora, rose, peacock, quicksilver, prism — or bare glass.",
    noneLabel: "Bare Glass",
    traits: [
      { id: "oil", name: "Oil Film", image: "/opaline-traits/sheen/oil.png", rarity: 18 },
      { id: "aurora", name: "Aurora Film", image: "/opaline-traits/sheen/aurora.png", rarity: 16 },
      { id: "rose", name: "Rose Film", image: "/opaline-traits/sheen/rose.png", rarity: 14 },
      { id: "peacock", name: "Peacock Film", image: "/opaline-traits/sheen/peacock.png", rarity: 12 },
      { id: "quicksilver", name: "Quicksilver Film", image: "/opaline-traits/sheen/quicksilver.png", rarity: 10 },
      { id: "prism", name: "Prism Film", image: "/opaline-traits/sheen/prism.png", rarity: 8 },
    ],
  },
  {
    id: "regard",
    label: "Regard",
    blurb: "Glass inclusions where the eyes sit. Quiet wells, bloom, slit, twin bubbles, void, gleam.",
    traits: [
      { id: "quiet", name: "Quiet", image: "/opaline-traits/regard/quiet.png", rarity: 24 },
      { id: "bloom", name: "Bloom", image: "/opaline-traits/regard/bloom.png", rarity: 18 },
      { id: "slit", name: "Slit", image: "/opaline-traits/regard/slit.png", rarity: 16 },
      { id: "twin", name: "Twin", image: "/opaline-traits/regard/twin.png", rarity: 14 },
      { id: "void", name: "Void", image: "/opaline-traits/regard/void.png", rarity: 14 },
      { id: "gleam", name: "Gleam", image: "/opaline-traits/regard/gleam.png", rarity: 14 },
    ],
  },
  {
    id: "crest",
    label: "Crest",
    blurb: "Seated on the flat crown — platinum band, prism shard, gold arc, glass spine, thin diadem.",
    noneLabel: "Bare Crown",
    traits: [
      { id: "band", name: "Platinum Band", image: "/opaline-traits/crest/band.png", rarity: 18 },
      { id: "shard", name: "Prism Shard", image: "/opaline-traits/crest/shard.png", rarity: 16 },
      { id: "arc", name: "Gold Arc", image: "/opaline-traits/crest/arc.png", rarity: 14 },
      { id: "spine", name: "Glass Spine", image: "/opaline-traits/crest/spine.png", rarity: 12 },
      { id: "diadem", name: "Thin Diadem", image: "/opaline-traits/crest/diadem.png", rarity: 12 },
    ],
  },
  {
    id: "clasp",
    label: "Clasp",
    blurb: "Neck and shoulder metal — bar, glass drop, gold torque, shoulder pin, coil.",
    noneLabel: "Bare Neck",
    traits: [
      { id: "bar", name: "Bar Clasp", image: "/opaline-traits/clasp/bar.png", rarity: 18 },
      { id: "drop", name: "Glass Drop", image: "/opaline-traits/clasp/drop.png", rarity: 16 },
      { id: "torque", name: "Gold Torque", image: "/opaline-traits/clasp/torque.png", rarity: 14 },
      { id: "pin", name: "Shoulder Pin", image: "/opaline-traits/clasp/pin.png", rarity: 12 },
      { id: "coil", name: "Coil", image: "/opaline-traits/clasp/coil.png", rarity: 12 },
    ],
  },
];

export const noneOpalineTrait: OpalineTrait = { id: "none", name: "None", rarity: 0 };

export function opalineCategoryById(id: OpalineTraitCategory["id"]) {
  const category = opalineTraitCategories.find((item) => item.id === id);
  if (!category) throw new Error(`Unknown Opaline trait category: ${id}`);
  return category;
}

export function findOpalineTrait(categoryId: OpalineTraitCategory["id"], traitId: string) {
  if (traitId === "none") return noneOpalineTrait;
  return opalineCategoryById(categoryId).traits.find((trait) => trait.id === traitId);
}

export const defaultOpalineSelection = {
  atelier: "dusk",
  cast: "smoke",
  sheen: "oil",
  regard: "quiet",
  crest: "band",
  clasp: "drop",
} as const;

export type OpalineSelection = Record<OpalineTraitCategory["id"], string>;

export function randomOpalineSelection(): OpalineSelection {
  const pick = (category: OpalineTraitCategory) => {
    const pool: OpalineTrait[] = category.noneLabel
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
    atelier: pick(opalineCategoryById("atelier")),
    cast: pick(opalineCategoryById("cast")),
    sheen: pick(opalineCategoryById("sheen")),
    regard: pick(opalineCategoryById("regard")),
    crest: pick(opalineCategoryById("crest")),
    clasp: pick(opalineCategoryById("clasp")),
  };
}

export function opalineCombinationCount() {
  return opalineTraitCategories.reduce((product, category) => {
    const extra = category.noneLabel ? 1 : 0;
    return product * (category.traits.length + extra);
  }, 1);
}

export function opalineSelectionToLayers(selection: OpalineSelection) {
  return (["atelier", "cast", "sheen", "regard", "crest", "clasp"] as const)
    .map((id) => findOpalineTrait(id, selection[id]))
    .filter((trait): trait is OpalineTrait => Boolean(trait?.image))
    .map((trait) => opalineTraitSrc(trait.image));
}
