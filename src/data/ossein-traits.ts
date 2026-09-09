export type OsseinTrait = {
  id: string;
  name: string;
  image?: string;
  rarity: number;
};

export type OsseinTraitCategory = {
  id: "sheet" | "rule" | "specimen" | "joint" | "leader" | "stain" | "chalk";
  label: string;
  blurb: string;
  noneLabel?: string;
  traits: OsseinTrait[];
};

export const OSSN_ART_VERSION = "ossein-v1";

export const OSSN_FRAMES = 12;
export const OSSN_DURATION_MS = 90;

export function osseinTraitSrc(path?: string) {
  if (!path) return "";
  return `${path}?v=${OSSN_ART_VERSION}`;
}

export const osseinTraitCategories: OsseinTraitCategory[] = [
  {
    id: "sheet",
    label: "Sheet",
    blurb: "The chart paper — cream, ledger, night, slate, aged, blush, vellum, mint.",
    traits: [
      { id: "cream", name: "Cream Sheet", image: "/ossein-traits/sheet/cream.png", rarity: 18 },
      { id: "ledger", name: "Ledger Sheet", image: "/ossein-traits/sheet/ledger.png", rarity: 16 },
      { id: "night", name: "Night Sheet", image: "/ossein-traits/sheet/night.png", rarity: 14 },
      { id: "slate", name: "Slate Sheet", image: "/ossein-traits/sheet/slate.png", rarity: 14 },
      { id: "aged", name: "Aged Sheet", image: "/ossein-traits/sheet/aged.png", rarity: 12 },
      { id: "blush", name: "Blush Sheet", image: "/ossein-traits/sheet/blush.png", rarity: 10 },
      { id: "vellum", name: "Vellum Sheet", image: "/ossein-traits/sheet/vellum.png", rarity: 8 },
      { id: "mint", name: "Mint Sheet", image: "/ossein-traits/sheet/mint.png", rarity: 8 },
    ],
  },
  {
    id: "rule",
    label: "Rule",
    blurb: "The printed grid — hair, dot, cross, double.",
    traits: [
      { id: "hair", name: "Hair Rule", image: "/ossein-traits/rule/hair.png", rarity: 32 },
      { id: "dot", name: "Dot Rule", image: "/ossein-traits/rule/dot.png", rarity: 26 },
      { id: "cross", name: "Cross Rule", image: "/ossein-traits/rule/cross.png", rarity: 22 },
      { id: "double", name: "Double Rule", image: "/ossein-traits/rule/double.png", rarity: 20 },
    ],
  },
  {
    id: "specimen",
    label: "Specimen",
    blurb: "The dancing skeleton. Eight specimens: cortical, avian, feline, equine, frog, ape, fish, serpent.",
    traits: [
      { id: "cortical", name: "Cortical", image: "/ossein-traits/specimen/cortical.png", rarity: 16 },
      { id: "avian", name: "Avian", image: "/ossein-traits/specimen/avian.png", rarity: 14 },
      { id: "feline", name: "Feline", image: "/ossein-traits/specimen/feline.png", rarity: 14 },
      { id: "equine", name: "Equine", image: "/ossein-traits/specimen/equine.png", rarity: 12 },
      { id: "frog", name: "Frog", image: "/ossein-traits/specimen/frog.png", rarity: 12 },
      { id: "ape", name: "Ape", image: "/ossein-traits/specimen/ape.png", rarity: 12 },
      { id: "fish", name: "Fish", image: "/ossein-traits/specimen/fish.png", rarity: 10 },
      { id: "serpent", name: "Serpent", image: "/ossein-traits/specimen/serpent.png", rarity: 10 },
    ],
  },
  {
    id: "joint",
    label: "Joint",
    blurb: "Marks at the articulations — ring, dot, cross, tick.",
    traits: [
      { id: "ring", name: "Ring Joint", image: "/ossein-traits/joint/ring.png", rarity: 30 },
      { id: "dot", name: "Dot Joint", image: "/ossein-traits/joint/dot.png", rarity: 28 },
      { id: "cross", name: "Cross Joint", image: "/ossein-traits/joint/cross.png", rarity: 22 },
      { id: "tick", name: "Tick Joint", image: "/ossein-traits/joint/tick.png", rarity: 20 },
    ],
  },
  {
    id: "leader",
    label: "Leader",
    blurb: "Callout ticks — one, pair — or an unlabeled plate.",
    noneLabel: "No Leader",
    traits: [
      { id: "one", name: "One Leader", image: "/ossein-traits/leader/one.png", rarity: 36 },
      { id: "pair", name: "Pair Leader", image: "/ossein-traits/leader/pair.png", rarity: 28 },
    ],
  },
  {
    id: "stain",
    label: "Stain",
    blurb: "Age on the sheet — tea, foxing, coffee — or a clean sheet.",
    noneLabel: "Clean Sheet",
    traits: [
      { id: "tea", name: "Tea Stain", image: "/ossein-traits/stain/tea.png", rarity: 26 },
      { id: "foxing", name: "Foxing", image: "/ossein-traits/stain/foxing.png", rarity: 22 },
      { id: "coffee", name: "Coffee Stain", image: "/ossein-traits/stain/coffee.png", rarity: 18 },
    ],
  },
  {
    id: "chalk",
    label: "Chalk",
    blurb: "Dust over the plate — mote, smear, dust — or clear air.",
    noneLabel: "Clear Air",
    traits: [
      { id: "mote", name: "Chalk Motes", image: "/ossein-traits/chalk/mote.png", rarity: 26 },
      { id: "smear", name: "Chalk Smear", image: "/ossein-traits/chalk/smear.png", rarity: 20 },
      { id: "dust", name: "Chalk Dust", image: "/ossein-traits/chalk/dust.png", rarity: 18 },
    ],
  }
];

export const noneOsseinTrait: OsseinTrait = { id: "none", name: "None", rarity: 0 };

export function osseinCategoryById(id: OsseinTraitCategory["id"]) {
  const category = osseinTraitCategories.find((item) => item.id === id);
  if (!category) throw new Error(`Unknown Ossein trait category: ${id}`);
  return category;
}

export function findOsseinTrait(categoryId: OsseinTraitCategory["id"], traitId: string) {
  if (traitId === "none") return noneOsseinTrait;
  return osseinCategoryById(categoryId).traits.find((trait) => trait.id === traitId);
}

export const defaultOsseinSelection = {
  sheet: "cream",
  rule: "hair",
  specimen: "cortical",
  joint: "ring",
  leader: "one",
  stain: "none",
  chalk: "mote",
} as const;

export type OsseinSelection = Record<OsseinTraitCategory["id"], string>;

export function randomOsseinSelection(): OsseinSelection {
  const pick = (category: OsseinTraitCategory) => {
    const pool: OsseinTrait[] = category.noneLabel ? [{ id: "none", name: category.noneLabel, rarity: 22 }, ...category.traits] : category.traits;
    const total = pool.reduce((sum, trait) => sum + Math.max(trait.rarity, 1), 0);
    let roll = Math.random() * total;
    for (const trait of pool) {
      roll -= Math.max(trait.rarity, 1);
      if (roll <= 0) return trait.id;
    }
    return pool[0].id;
  };
  return {
    sheet: pick(osseinCategoryById("sheet")),
    rule: pick(osseinCategoryById("rule")),
    specimen: pick(osseinCategoryById("specimen")),
    joint: pick(osseinCategoryById("joint")),
    leader: pick(osseinCategoryById("leader")),
    stain: pick(osseinCategoryById("stain")),
    chalk: pick(osseinCategoryById("chalk")),
  };
}

export function osseinCombinationCount() {
  return osseinTraitCategories.reduce((product, category) => {
    const extra = category.noneLabel ? 1 : 0;
    return product * (category.traits.length + extra);
  }, 1);
}

export function osseinSelectionToLayers(selection: OsseinSelection) {
  return (["sheet", "rule", "specimen", "joint", "leader", "stain", "chalk"] as const)
    .map((id) => findOsseinTrait(id, selection[id]))
    .filter((trait): trait is OsseinTrait => Boolean(trait?.image))
    .map((trait) => osseinTraitSrc(trait.image));
}
