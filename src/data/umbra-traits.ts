export type UmbraTrait = {
  id: string;
  name: string;
  image?: string;
  rarity: number;
};

export type UmbraTraitCategory = {
  id: "cloth" | "ember" | "cast" | "hinge" | "cutwork" | "leaf" | "soot";
  label: string;
  blurb: string;
  noneLabel?: string;
  traits: UmbraTrait[];
};

/** Bump when APNG layers change so the studio does not keep a stale loop. */
export const UMBRA_ART_VERSION = "umbra-v1";

export const UMBRA_FRAMES = 12;
export const UMBRA_DURATION_MS = 90;

export function umbraTraitSrc(path?: string) {
  if (!path) return "";
  return `${path}?v=${UMBRA_ART_VERSION}`;
}

export const umbraTraitCategories: UmbraTraitCategory[] = [
  {
    id: "cloth",
    label: "Cloth",
    blurb: "The lamp screen — parchment, saffron, dusk, smoke, indigo, rose, ash, brass.",
    traits: [
      { id: "parchment", name: "Parchment Screen", image: "/umbra-traits/cloth/parchment.png", rarity: 18 },
      { id: "saffron", name: "Saffron Screen", image: "/umbra-traits/cloth/saffron.png", rarity: 14 },
      { id: "dusk", name: "Dusk Screen", image: "/umbra-traits/cloth/dusk.png", rarity: 12 },
      { id: "smoke", name: "Smoke Screen", image: "/umbra-traits/cloth/smoke.png", rarity: 12 },
      { id: "indigo", name: "Indigo Screen", image: "/umbra-traits/cloth/indigo.png", rarity: 12 },
      { id: "rose", name: "Rose Screen", image: "/umbra-traits/cloth/rose.png", rarity: 12 },
      { id: "ash", name: "Ash Screen", image: "/umbra-traits/cloth/ash.png", rarity: 10 },
      { id: "brass", name: "Brass Screen", image: "/umbra-traits/cloth/brass.png", rarity: 10 },
    ],
  },
  {
    id: "ember",
    label: "Ember",
    blurb: "The light behind the hide — oil, coal, dawn, hearth, moon, forge.",
    traits: [
      { id: "oil", name: "Oil Lamp", image: "/umbra-traits/ember/oil.png", rarity: 20 },
      { id: "coal", name: "Coal Glow", image: "/umbra-traits/ember/coal.png", rarity: 16 },
      { id: "dawn", name: "Dawn Glow", image: "/umbra-traits/ember/dawn.png", rarity: 16 },
      { id: "hearth", name: "Hearth Glow", image: "/umbra-traits/ember/hearth.png", rarity: 16 },
      { id: "moon", name: "Moon Glow", image: "/umbra-traits/ember/moon.png", rarity: 16 },
      { id: "forge", name: "Forge Glow", image: "/umbra-traits/ember/forge.png", rarity: 16 },
    ],
  },
  {
    id: "cast",
    label: "Cast",
    blurb: "The dancing puppet. Eight casts: clown, knight, bride, ogre, sage, harper, bird, demon.",
    traits: [
      { id: "clown", name: "Clown", image: "/umbra-traits/cast/clown.png", rarity: 18 },
      { id: "knight", name: "Knight", image: "/umbra-traits/cast/knight.png", rarity: 16 },
      { id: "bride", name: "Bride", image: "/umbra-traits/cast/bride.png", rarity: 14 },
      { id: "ogre", name: "Ogre", image: "/umbra-traits/cast/ogre.png", rarity: 14 },
      { id: "sage", name: "Sage", image: "/umbra-traits/cast/sage.png", rarity: 12 },
      { id: "harper", name: "Harper", image: "/umbra-traits/cast/harper.png", rarity: 10 },
      { id: "bird", name: "Bird", image: "/umbra-traits/cast/bird.png", rarity: 8 },
      { id: "demon", name: "Demon", image: "/umbra-traits/cast/demon.png", rarity: 8 },
    ],
  },
  {
    id: "hinge",
    label: "Hinge",
    blurb: "Brads at the joints — brass, iron, pearl, rust — or a seamless hide.",
    noneLabel: "No Hinge",
    traits: [
      { id: "brass", name: "Brass Brad", image: "/umbra-traits/hinge/brass.png", rarity: 22 },
      { id: "iron", name: "Iron Brad", image: "/umbra-traits/hinge/iron.png", rarity: 20 },
      { id: "pearl", name: "Pearl Brad", image: "/umbra-traits/hinge/pearl.png", rarity: 18 },
      { id: "rust", name: "Rust Brad", image: "/umbra-traits/hinge/rust.png", rarity: 18 },
    ],
  },
  {
    id: "cutwork",
    label: "Cutwork",
    blurb: "Lace punched through the leather — dots, stars, diamonds, vine — or solid hide.",
    noneLabel: "Solid Hide",
    traits: [
      { id: "dots", name: "Dot Lace", image: "/umbra-traits/cutwork/dots.png", rarity: 20 },
      { id: "stars", name: "Star Lace", image: "/umbra-traits/cutwork/stars.png", rarity: 18 },
      { id: "diamonds", name: "Diamond Lace", image: "/umbra-traits/cutwork/diamonds.png", rarity: 18 },
      { id: "vine", name: "Vine Lace", image: "/umbra-traits/cutwork/vine.png", rarity: 18 },
    ],
  },
  {
    id: "leaf",
    label: "Leaf",
    blurb: "Gold on the edge — rim, tips, full leaf, dust — or bare hide.",
    noneLabel: "Bare Hide",
    traits: [
      { id: "rim", name: "Gold Rim", image: "/umbra-traits/leaf/rim.png", rarity: 20 },
      { id: "tips", name: "Gold Tips", image: "/umbra-traits/leaf/tips.png", rarity: 18 },
      { id: "full", name: "Full Leaf", image: "/umbra-traits/leaf/full.png", rarity: 18 },
      { id: "dust", name: "Gold Dust", image: "/umbra-traits/leaf/dust.png", rarity: 18 },
    ],
  },
  {
    id: "soot",
    label: "Soot",
    blurb: "Air in front of the screen — motes, ribbon, haze, spark — or clear air.",
    noneLabel: "Clear Air",
    traits: [
      { id: "motes", name: "Soot Motes", image: "/umbra-traits/soot/motes.png", rarity: 20 },
      { id: "ribbon", name: "Smoke Ribbon", image: "/umbra-traits/soot/ribbon.png", rarity: 20 },
      { id: "haze", name: "Lamp Haze", image: "/umbra-traits/soot/haze.png", rarity: 18 },
      { id: "spark", name: "Spark Rise", image: "/umbra-traits/soot/spark.png", rarity: 18 },
    ],
  }
];

export const noneUmbraTrait: UmbraTrait = { id: "none", name: "None", rarity: 0 };

export function umbraCategoryById(id: UmbraTraitCategory["id"]) {
  const category = umbraTraitCategories.find((item) => item.id === id);
  if (!category) throw new Error(`Unknown Umbra trait category: ${id}`);
  return category;
}

export function findUmbraTrait(categoryId: UmbraTraitCategory["id"], traitId: string) {
  if (traitId === "none") return noneUmbraTrait;
  return umbraCategoryById(categoryId).traits.find((trait) => trait.id === traitId);
}

export const defaultUmbraSelection = {
  cloth: "parchment",
  ember: "oil",
  cast: "clown",
  hinge: "brass",
  cutwork: "dots",
  leaf: "rim",
  soot: "motes",
} as const;

export type UmbraSelection = Record<UmbraTraitCategory["id"], string>;

export function randomUmbraSelection(): UmbraSelection {
  const pick = (category: UmbraTraitCategory) => {
    const pool: UmbraTrait[] = category.noneLabel
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
    cloth: pick(umbraCategoryById("cloth")),
    ember: pick(umbraCategoryById("ember")),
    cast: pick(umbraCategoryById("cast")),
    hinge: pick(umbraCategoryById("hinge")),
    cutwork: pick(umbraCategoryById("cutwork")),
    leaf: pick(umbraCategoryById("leaf")),
    soot: pick(umbraCategoryById("soot")),
  };
}

export function umbraCombinationCount() {
  return umbraTraitCategories.reduce((product, category) => {
    const extra = category.noneLabel ? 1 : 0;
    return product * (category.traits.length + extra);
  }, 1);
}

export function umbraSelectionToLayers(selection: UmbraSelection) {
  return (["cloth", "ember", "cast", "hinge", "cutwork", "leaf", "soot"] as const)
    .map((id) => findUmbraTrait(id, selection[id]))
    .filter((trait): trait is UmbraTrait => Boolean(trait?.image))
    .map((trait) => umbraTraitSrc(trait.image));
}
