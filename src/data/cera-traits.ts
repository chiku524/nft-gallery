export type CeraTrait = {
  id: string;
  name: string;
  image?: string;
  rarity: number;
};

export type CeraTraitCategory = {
  id: "sill" | "socket" | "flask" | "serum" | "melt" | "coil" | "lid";
  label: string;
  blurb: string;
  noneLabel?: string;
  traits: CeraTrait[];
};

/** Bump when APNG layers change so the studio does not keep a stale loop. */
export const CERA_ART_VERSION = "cera-v5";

export const CERA_FRAMES = 12;
export const CERA_DURATION_MS = 90;

export function ceraTraitSrc(path?: string) {
  if (!path) return "";
  return `${path}?v=${CERA_ART_VERSION}`;
}

export const ceraTraitCategories: CeraTraitCategory[] = [
  {
    id: "sill",
    label: "Sill",
    blurb: "The nightstand — wood, formica, velvet, tile, night.",
    traits: [
      { id: "wood", name: "Wood Sill", image: "/cera-traits/sill/wood.png", rarity: 22 },
      { id: "formica", name: "Formica Sill", image: "/cera-traits/sill/formica.png", rarity: 22 },
      { id: "velvet", name: "Velvet Sill", image: "/cera-traits/sill/velvet.png", rarity: 20 },
      { id: "tile", name: "Tile Sill", image: "/cera-traits/sill/tile.png", rarity: 18 },
      { id: "night", name: "Night Sill", image: "/cera-traits/sill/night.png", rarity: 18 },
    ],
  },
  {
    id: "socket",
    label: "Socket",
    blurb: "The lamp foot — rocket, saucer, cone, cube, mushroom, chrome, walnut, ceramic.",
    traits: [
      { id: "rocket", name: "Rocket Socket", image: "/cera-traits/socket/rocket.png", rarity: 16 },
      { id: "saucer", name: "Saucer Socket", image: "/cera-traits/socket/saucer.png", rarity: 14 },
      { id: "cone", name: "Cone Socket", image: "/cera-traits/socket/cone.png", rarity: 14 },
      { id: "cube", name: "Cube Socket", image: "/cera-traits/socket/cube.png", rarity: 12 },
      { id: "mushroom", name: "Mushroom Socket", image: "/cera-traits/socket/mushroom.png", rarity: 12 },
      { id: "chrome", name: "Chrome Socket", image: "/cera-traits/socket/chrome.png", rarity: 12 },
      { id: "walnut", name: "Walnut Socket", image: "/cera-traits/socket/walnut.png", rarity: 10 },
      { id: "ceramic", name: "Ceramic Socket", image: "/cera-traits/socket/ceramic.png", rarity: 10 },
    ],
  },
  {
    id: "flask",
    label: "Flask",
    blurb: "The glass — taper, cylinder, teardrop, bulb.",
    traits: [
      { id: "taper", name: "Taper Flask", image: "/cera-traits/flask/taper.png", rarity: 32 },
      { id: "cylinder", name: "Cylinder Flask", image: "/cera-traits/flask/cylinder.png", rarity: 26 },
      { id: "teardrop", name: "Teardrop Flask", image: "/cera-traits/flask/teardrop.png", rarity: 22 },
      { id: "bulb", name: "Bulb Flask", image: "/cera-traits/flask/bulb.png", rarity: 20 },
    ],
  },
  {
    id: "serum",
    label: "Serum",
    blurb: "The oil — clear, cyan, amber, violet, green.",
    traits: [
      { id: "clear", name: "Clear Serum", image: "/cera-traits/serum/clear.png", rarity: 24 },
      { id: "cyan", name: "Cyan Serum", image: "/cera-traits/serum/cyan.png", rarity: 22 },
      { id: "amber", name: "Amber Serum", image: "/cera-traits/serum/amber.png", rarity: 20 },
      { id: "violet", name: "Violet Serum", image: "/cera-traits/serum/violet.png", rarity: 18 },
      { id: "green", name: "Green Serum", image: "/cera-traits/serum/green.png", rarity: 16 },
    ],
  },
  {
    id: "melt",
    label: "Melt",
    blurb: "The paraffin — crimson, gold, white, magenta, black. The wax is the loop.",
    traits: [
      { id: "crimson", name: "Crimson Melt", image: "/cera-traits/melt/crimson.png", rarity: 24 },
      { id: "gold", name: "Gold Melt", image: "/cera-traits/melt/gold.png", rarity: 22 },
      { id: "white", name: "White Melt", image: "/cera-traits/melt/white.png", rarity: 20 },
      { id: "magenta", name: "Magenta Melt", image: "/cera-traits/melt/magenta.png", rarity: 18 },
      { id: "black", name: "Black Melt", image: "/cera-traits/melt/black.png", rarity: 16 },
    ],
  },
  {
    id: "coil",
    label: "Coil",
    blurb: "The heater — dim, orange, white-hot.",
    traits: [
      { id: "dim", name: "Dim Coil", image: "/cera-traits/coil/dim.png", rarity: 36 },
      { id: "orange", name: "Orange Coil", image: "/cera-traits/coil/orange.png", rarity: 34 },
      { id: "whitehot", name: "White-Hot Coil", image: "/cera-traits/coil/whitehot.png", rarity: 30 },
    ],
  },
  {
    id: "lid",
    label: "Lid",
    blurb: "A chrome, gold, or painted cap.",
    noneLabel: "No Lid",
    traits: [
      { id: "chrome", name: "Chrome Lid", image: "/cera-traits/lid/chrome.png", rarity: 26 },
      { id: "gold", name: "Gold Lid", image: "/cera-traits/lid/gold.png", rarity: 24 },
      { id: "painted", name: "Painted Lid", image: "/cera-traits/lid/painted.png", rarity: 22 },
    ],
  }
];

export const noneCeraTrait: CeraTrait = { id: "none", name: "None", rarity: 0 };

export function ceraCategoryById(id: CeraTraitCategory["id"]) {
  const category = ceraTraitCategories.find((item) => item.id === id);
  if (!category) throw new Error(`Unknown Cera trait category: ${id}`);
  return category;
}

export function findCeraTrait(categoryId: CeraTraitCategory["id"], traitId: string) {
  if (traitId === "none") return noneCeraTrait;
  return ceraCategoryById(categoryId).traits.find((trait) => trait.id === traitId);
}

export const defaultCeraSelection = {
  sill: "wood",
  socket: "rocket",
  flask: "taper",
  serum: "cyan",
  melt: "crimson",
  coil: "orange",
  lid: "chrome",
} as const;

export type CeraSelection = Record<CeraTraitCategory["id"], string>;

export function randomCeraSelection(): CeraSelection {
  const pick = (category: CeraTraitCategory) => {
    const pool: CeraTrait[] = category.noneLabel
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
    sill: pick(ceraCategoryById("sill")),
    socket: pick(ceraCategoryById("socket")),
    flask: pick(ceraCategoryById("flask")),
    serum: pick(ceraCategoryById("serum")),
    melt: pick(ceraCategoryById("melt")),
    coil: pick(ceraCategoryById("coil")),
    lid: pick(ceraCategoryById("lid")),
  };
}

export function ceraCombinationCount() {
  return ceraTraitCategories.reduce((product, category) => {
    const extra = category.noneLabel ? 1 : 0;
    return product * (category.traits.length + extra);
  }, 1);
}

export function ceraSelectionToLayers(selection: CeraSelection) {
  return (["sill", "socket", "flask", "serum", "melt", "coil", "lid"] as const)
    .map((id) => findCeraTrait(id, selection[id]))
    .filter((trait): trait is CeraTrait => Boolean(trait?.image))
    .map((trait) => ceraTraitSrc(trait.image));
}
