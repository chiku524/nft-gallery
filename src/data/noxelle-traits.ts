export type NoxelleTrait = {
  id: string;
  name: string;
  image?: string;
  rarity: number;
};

export type NoxelleTraitCategory = {
  id: "wall" | "spill" | "gas" | "bend" | "clip" | "badge" | "mote";
  label: string;
  blurb: string;
  noneLabel?: string;
  traits: NoxelleTrait[];
};

/** Bump when APNG layers change so the studio does not keep a stale loop. */
export const NOXELLE_ART_VERSION = "noxelle-v2";

export const NOXELLE_FRAMES = 12;
export const NOXELLE_DURATION_MS = 90;

export function noxelleTraitSrc(path?: string) {
  if (!path) return "";
  return `${path}?v=${NOXELLE_ART_VERSION}`;
}

export const noxelleTraitCategories: NoxelleTraitCategory[] = [
  {
    id: "wall",
    label: "Wall",
    blurb: "The club surface — velvet, tile, brick, chrome, alley, booth, parking, glass.",
    traits: [
      { id: "velvet", name: "Velvet Wall", image: "/noxelle-traits/wall/velvet.png", rarity: 16 },
      { id: "tile", name: "Tile Wall", image: "/noxelle-traits/wall/tile.png", rarity: 14 },
      { id: "brick", name: "Brick Wall", image: "/noxelle-traits/wall/brick.png", rarity: 14 },
      { id: "chrome", name: "Chrome Wall", image: "/noxelle-traits/wall/chrome.png", rarity: 12 },
      { id: "alley", name: "Alley Wall", image: "/noxelle-traits/wall/alley.png", rarity: 12 },
      { id: "booth", name: "Booth Wall", image: "/noxelle-traits/wall/booth.png", rarity: 12 },
      { id: "parking", name: "Parking Wall", image: "/noxelle-traits/wall/parking.png", rarity: 10 },
      { id: "glass", name: "Glass Wall", image: "/noxelle-traits/wall/glass.png", rarity: 10 },
    ],
  },
  {
    id: "spill",
    label: "Spill",
    blurb: "Color on the floor and ceiling — grape, lagoon, cherry, honey, mint, ice.",
    traits: [
      { id: "grape", name: "Grape Spill", image: "/noxelle-traits/spill/grape.png", rarity: 18 },
      { id: "lagoon", name: "Lagoon Spill", image: "/noxelle-traits/spill/lagoon.png", rarity: 17 },
      { id: "cherry", name: "Cherry Spill", image: "/noxelle-traits/spill/cherry.png", rarity: 17 },
      { id: "honey", name: "Honey Spill", image: "/noxelle-traits/spill/honey.png", rarity: 16 },
      { id: "mint", name: "Mint Spill", image: "/noxelle-traits/spill/mint.png", rarity: 16 },
      { id: "ice", name: "Ice Spill", image: "/noxelle-traits/spill/ice.png", rarity: 16 },
    ],
  },
  {
    id: "gas",
    label: "Gas",
    blurb: "The noble fill behind the glass — argon, neon, krypton, mercury, helium, xenon, sodium, shop mix.",
    traits: [
      { id: "argon", name: "Argon", image: "/noxelle-traits/gas/argon.png", rarity: 16 },
      { id: "neon", name: "Neon", image: "/noxelle-traits/gas/neon.png", rarity: 16 },
      { id: "krypton", name: "Krypton", image: "/noxelle-traits/gas/krypton.png", rarity: 14 },
      { id: "mercury", name: "Mercury", image: "/noxelle-traits/gas/mercury.png", rarity: 14 },
      { id: "helium", name: "Helium", image: "/noxelle-traits/gas/helium.png", rarity: 12 },
      { id: "xenon", name: "Xenon", image: "/noxelle-traits/gas/xenon.png", rarity: 12 },
      { id: "sodium", name: "Sodium", image: "/noxelle-traits/gas/sodium.png", rarity: 8 },
      { id: "mix", name: "Shop Mix", image: "/noxelle-traits/gas/mix.png", rarity: 8 },
    ],
  },
  {
    id: "bend",
    label: "Bend",
    blurb: "The dancer is the tube. Eight bends: sway, kick, wave, hop, point, dip, spin, split.",
    traits: [
      { id: "sway", name: "Sway Bend", image: "/noxelle-traits/bend/sway.png", rarity: 18 },
      { id: "kick", name: "Kick Bend", image: "/noxelle-traits/bend/kick.png", rarity: 16 },
      { id: "wave", name: "Wave Bend", image: "/noxelle-traits/bend/wave.png", rarity: 14 },
      { id: "hop", name: "Hop Bend", image: "/noxelle-traits/bend/hop.png", rarity: 14 },
      { id: "point", name: "Point Bend", image: "/noxelle-traits/bend/point.png", rarity: 12 },
      { id: "dip", name: "Dip Bend", image: "/noxelle-traits/bend/dip.png", rarity: 10 },
      { id: "spin", name: "Spin Bend", image: "/noxelle-traits/bend/spin.png", rarity: 8 },
      { id: "split", name: "Split Bend", image: "/noxelle-traits/bend/split.png", rarity: 8 },
    ],
  },
  {
    id: "clip",
    label: "Clip",
    blurb: "Hardware that holds the glass — transformer, conduit, clips, daisy chain — or bare wall.",
    noneLabel: "No Clip",
    traits: [
      { id: "brick", name: "Transformer Brick", image: "/noxelle-traits/clip/brick.png", rarity: 22 },
      { id: "conduit", name: "Conduit Run", image: "/noxelle-traits/clip/conduit.png", rarity: 20 },
      { id: "clips", name: "Wall Clips", image: "/noxelle-traits/clip/clips.png", rarity: 18 },
      { id: "daisy", name: "Daisy Chain", image: "/noxelle-traits/clip/daisy.png", rarity: 16 },
    ],
  },
  {
    id: "badge",
    label: "Badge",
    blurb: "A second small sign — moon, bolt, heart, star, disc — or none.",
    noneLabel: "No Badge",
    traits: [
      { id: "moon", name: "Moon Badge", image: "/noxelle-traits/badge/moon.png", rarity: 16 },
      { id: "bolt", name: "Bolt Badge", image: "/noxelle-traits/badge/bolt.png", rarity: 16 },
      { id: "heart", name: "Heart Badge", image: "/noxelle-traits/badge/heart.png", rarity: 14 },
      { id: "star", name: "Star Badge", image: "/noxelle-traits/badge/star.png", rarity: 14 },
      { id: "disc", name: "Disc Badge", image: "/noxelle-traits/badge/disc.png", rarity: 12 },
    ],
  },
  {
    id: "mote",
    label: "Mote",
    blurb: "Air in front of the tube — spark, moth, dust, tick — or clear air.",
    noneLabel: "Clear Air",
    traits: [
      { id: "spark", name: "Spark Motes", image: "/noxelle-traits/mote/spark.png", rarity: 20 },
      { id: "moth", name: "Night Moths", image: "/noxelle-traits/mote/moth.png", rarity: 18 },
      { id: "dust", name: "Dust Drift", image: "/noxelle-traits/mote/dust.png", rarity: 18 },
      { id: "tick", name: "Tick Flicker", image: "/noxelle-traits/mote/tick.png", rarity: 18 },
    ],
  }
];

export const noneNoxelleTrait: NoxelleTrait = { id: "none", name: "None", rarity: 0 };

export function noxelleCategoryById(id: NoxelleTraitCategory["id"]) {
  const category = noxelleTraitCategories.find((item) => item.id === id);
  if (!category) throw new Error(`Unknown Noxelle trait category: ${id}`);
  return category;
}

export function findNoxelleTrait(categoryId: NoxelleTraitCategory["id"], traitId: string) {
  if (traitId === "none") return noneNoxelleTrait;
  return noxelleCategoryById(categoryId).traits.find((trait) => trait.id === traitId);
}

export const defaultNoxelleSelection = {
  wall: "velvet",
  spill: "grape",
  gas: "argon",
  bend: "sway",
  clip: "brick",
  badge: "moon",
  mote: "spark",
} as const;

export type NoxelleSelection = Record<NoxelleTraitCategory["id"], string>;

export function randomNoxelleSelection(): NoxelleSelection {
  const pick = (category: NoxelleTraitCategory) => {
    const pool: NoxelleTrait[] = category.noneLabel
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
    wall: pick(noxelleCategoryById("wall")),
    spill: pick(noxelleCategoryById("spill")),
    gas: pick(noxelleCategoryById("gas")),
    bend: pick(noxelleCategoryById("bend")),
    clip: pick(noxelleCategoryById("clip")),
    badge: pick(noxelleCategoryById("badge")),
    mote: pick(noxelleCategoryById("mote")),
  };
}

export function noxelleCombinationCount() {
  return noxelleTraitCategories.reduce((product, category) => {
    const extra = category.noneLabel ? 1 : 0;
    return product * (category.traits.length + extra);
  }, 1);
}

export function noxelleSelectionToLayers(selection: NoxelleSelection) {
  return (["wall", "spill", "gas", "bend", "clip", "badge", "mote"] as const)
    .map((id) => findNoxelleTrait(id, selection[id]))
    .filter((trait): trait is NoxelleTrait => Boolean(trait?.image))
    .map((trait) => noxelleTraitSrc(trait.image));
}
