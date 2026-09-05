export type OpalineTrait = {
  id: string;
  name: string;
  image?: string;
  rarity: number;
};

export type OpalineTraitCategory = {
  id: "atelier" | "vapor" | "cast" | "sheen" | "regard" | "crest" | "clasp";
  label: string;
  blurb: string;
  noneLabel?: string;
  traits: OpalineTrait[];
};

/** Bump when APNG layers change so the studio does not keep a stale loop. */
export const OPALINE_ART_VERSION = "opaline-v5";

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
    id: "vapor",
    label: "Vapor",
    blurb: "Atmosphere in the room — mist, motes, a caustic ribbon, a pale disc, a rising plume, a luminous well — or clear air.",
    noneLabel: "Clear Air",
    traits: [
      { id: "mist", name: "Soft Mist", image: "/opaline-traits/vapor/mist.png", rarity: 18 },
      { id: "mote", name: "Glass Motes", image: "/opaline-traits/vapor/mote.png", rarity: 16 },
      { id: "ribbon", name: "Caustic Ribbon", image: "/opaline-traits/vapor/ribbon.png", rarity: 14 },
      { id: "disc", name: "Pale Disc", image: "/opaline-traits/vapor/disc.png", rarity: 12 },
      { id: "plume", name: "Rising Plume", image: "/opaline-traits/vapor/plume.png", rarity: 10 },
      { id: "well", name: "Luminous Well", image: "/opaline-traits/vapor/well.png", rarity: 8 },
    ],
  },
  {
    id: "cast",
    label: "Cast",
    blurb: "The crystal animal — stag, serpent, moth, beetle, ram, ibis, wyrm, mantis. Same eye line, eight skulls.",
    traits: [
      { id: "stag", name: "Stag", image: "/opaline-traits/cast/stag.png", rarity: 18 },
      { id: "serpent", name: "Serpent", image: "/opaline-traits/cast/serpent.png", rarity: 16 },
      { id: "moth", name: "Moth", image: "/opaline-traits/cast/moth.png", rarity: 14 },
      { id: "beetle", name: "Beetle", image: "/opaline-traits/cast/beetle.png", rarity: 14 },
      { id: "ram", name: "Ram", image: "/opaline-traits/cast/ram.png", rarity: 12 },
      { id: "ibis", name: "Ibis", image: "/opaline-traits/cast/ibis.png", rarity: 10 },
      { id: "wyrm", name: "Wyrm", image: "/opaline-traits/cast/wyrm.png", rarity: 8 },
      { id: "mantis", name: "Mantis", image: "/opaline-traits/cast/mantis.png", rarity: 8 },
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
    blurb: "Seated on the shared crown — platinum band, prism shard, gold arc, glass spine, thin diadem.",
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
  vapor: "disc",
  cast: "stag",
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
    vapor: pick(opalineCategoryById("vapor")),
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
  return (["atelier", "vapor", "cast", "sheen", "regard", "crest", "clasp"] as const)
    .map((id) => findOpalineTrait(id, selection[id]))
    .filter((trait): trait is OpalineTrait => Boolean(trait?.image))
    .map((trait) => opalineTraitSrc(trait.image));
}
