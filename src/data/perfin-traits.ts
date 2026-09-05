export type PerfinTrait = {
  id: string;
  name: string;
  image?: string;
  rarity: number;
};

export type PerfinTraitCategory = {
  id: "wove" | "guilloche" | "bust" | "surcharge" | "aspect" | "device" | "cancel";
  label: string;
  blurb: string;
  noneLabel?: string;
  traits: PerfinTrait[];
};

/** Bump when APNG layers change so the studio does not keep a stale loop. */
export const PERFIN_ART_VERSION = "perfin-v1";

export const PERFIN_FRAMES = 12;
export const PERFIN_DURATION_MS = 90;

export function perfinTraitSrc(path?: string) {
  if (!path) return "";
  return `${path}?v=${PERFIN_ART_VERSION}`;
}

export const perfinTraitCategories: PerfinTraitCategory[] = [
  {
    id: "wove",
    label: "Wove",
    blurb: "Stamp paper — ivory, rose, azure, buff, lilac, sage, pearl, grey.",
    traits: [
      { id: "ivory", name: "Ivory Wove", image: "/perfin-traits/wove/ivory.png", rarity: 18 },
      { id: "rose", name: "Rose Wove", image: "/perfin-traits/wove/rose.png", rarity: 14 },
      { id: "azure", name: "Azure Wove", image: "/perfin-traits/wove/azure.png", rarity: 12 },
      { id: "buff", name: "Buff Wove", image: "/perfin-traits/wove/buff.png", rarity: 12 },
      { id: "lilac", name: "Lilac Wove", image: "/perfin-traits/wove/lilac.png", rarity: 12 },
      { id: "sage", name: "Sage Wove", image: "/perfin-traits/wove/sage.png", rarity: 12 },
      { id: "pearl", name: "Pearl Wove", image: "/perfin-traits/wove/pearl.png", rarity: 10 },
      { id: "grey", name: "Grey Wove", image: "/perfin-traits/wove/grey.png", rarity: 10 },
    ],
  },
  {
    id: "guilloche",
    label: "Guilloche",
    blurb: "Security engraving behind the vignette — rose, engine, lattice, sunburst, wave, tablet.",
    traits: [
      { id: "rose", name: "Rose Engine", image: "/perfin-traits/guilloche/rose.png", rarity: 18 },
      { id: "engine", name: "Geometric Engine", image: "/perfin-traits/guilloche/engine.png", rarity: 16 },
      { id: "lattice", name: "Lattice", image: "/perfin-traits/guilloche/lattice.png", rarity: 16 },
      { id: "sunburst", name: "Sunburst", image: "/perfin-traits/guilloche/sunburst.png", rarity: 14 },
      { id: "wave", name: "Wave Engine", image: "/perfin-traits/guilloche/wave.png", rarity: 14 },
      { id: "tablet", name: "Value Tablet", image: "/perfin-traits/guilloche/tablet.png", rarity: 12 },
    ],
  },
  {
    id: "bust",
    label: "Bust",
    blurb: "The franked portrait. Eight engraved busts: pilot, keeper, clerk, captain, botanist, mapper, signal, warden.",
    traits: [
      { id: "pilot", name: "Pilot", image: "/perfin-traits/bust/pilot.png", rarity: 18 },
      { id: "keeper", name: "Keeper", image: "/perfin-traits/bust/keeper.png", rarity: 16 },
      { id: "clerk", name: "Clerk", image: "/perfin-traits/bust/clerk.png", rarity: 14 },
      { id: "captain", name: "Captain", image: "/perfin-traits/bust/captain.png", rarity: 14 },
      { id: "botanist", name: "Botanist", image: "/perfin-traits/bust/botanist.png", rarity: 12 },
      { id: "mapper", name: "Mapper", image: "/perfin-traits/bust/mapper.png", rarity: 10 },
      { id: "signal", name: "Signal", image: "/perfin-traits/bust/signal.png", rarity: 8 },
      { id: "warden", name: "Warden", image: "/perfin-traits/bust/warden.png", rarity: 8 },
    ],
  },
  {
    id: "surcharge",
    label: "Surcharge",
    blurb: "A second ink overprint — carmine bar, Prussian band, orange triangle, violet oval — or none.",
    noneLabel: "No Surcharge",
    traits: [
      { id: "bar", name: "Carmine Bar", image: "/perfin-traits/surcharge/bar.png", rarity: 18 },
      { id: "band", name: "Prussian Band", image: "/perfin-traits/surcharge/band.png", rarity: 16 },
      { id: "triangle", name: "Orange Triangle", image: "/perfin-traits/surcharge/triangle.png", rarity: 14 },
      { id: "oval", name: "Violet Oval", image: "/perfin-traits/surcharge/oval.png", rarity: 12 },
    ],
  },
  {
    id: "aspect",
    label: "Aspect",
    blurb: "The face cut — calm, stern, wink, shout, glance, smile.",
    traits: [
      { id: "calm", name: "Calm", image: "/perfin-traits/aspect/calm.png", rarity: 22 },
      { id: "stern", name: "Stern", image: "/perfin-traits/aspect/stern.png", rarity: 18 },
      { id: "wink", name: "Wink", image: "/perfin-traits/aspect/wink.png", rarity: 16 },
      { id: "shout", name: "Shout", image: "/perfin-traits/aspect/shout.png", rarity: 16 },
      { id: "glance", name: "Glance", image: "/perfin-traits/aspect/glance.png", rarity: 14 },
      { id: "smile", name: "Smile", image: "/perfin-traits/aspect/smile.png", rarity: 14 },
    ],
  },
  {
    id: "device",
    label: "Device",
    blurb: "An engraved extra on the crown or chest — goggles, spectacles, medal, pipe, cockade — or a bare device.",
    noneLabel: "Bare Device",
    traits: [
      { id: "goggles", name: "Goggles", image: "/perfin-traits/device/goggles.png", rarity: 18 },
      { id: "specs", name: "Spectacles", image: "/perfin-traits/device/specs.png", rarity: 16 },
      { id: "medal", name: "Medal", image: "/perfin-traits/device/medal.png", rarity: 14 },
      { id: "pipe", name: "Pipe", image: "/perfin-traits/device/pipe.png", rarity: 12 },
      { id: "cockade", name: "Cockade", image: "/perfin-traits/device/cockade.png", rarity: 12 },
    ],
  },
  {
    id: "cancel",
    label: "Cancel",
    blurb: "The killer that walks — circular date, wavy lines, mute, bars — or mint uncancelled.",
    noneLabel: "Mint Uncancelled",
    traits: [
      { id: "cds", name: "Circular Date", image: "/perfin-traits/cancel/cds.png", rarity: 20 },
      { id: "waves", name: "Wavy Lines", image: "/perfin-traits/cancel/waves.png", rarity: 18 },
      { id: "mute", name: "Mute Killer", image: "/perfin-traits/cancel/mute.png", rarity: 14 },
      { id: "bars", name: "Killer Bars", image: "/perfin-traits/cancel/bars.png", rarity: 12 },
    ],
  }
];

export const nonePerfinTrait: PerfinTrait = { id: "none", name: "None", rarity: 0 };

export function perfinCategoryById(id: PerfinTraitCategory["id"]) {
  const category = perfinTraitCategories.find((item) => item.id === id);
  if (!category) throw new Error(`Unknown Perfin trait category: ${id}`);
  return category;
}

export function findPerfinTrait(categoryId: PerfinTraitCategory["id"], traitId: string) {
  if (traitId === "none") return nonePerfinTrait;
  return perfinCategoryById(categoryId).traits.find((trait) => trait.id === traitId);
}

export const defaultPerfinSelection = {
  wove: "ivory",
  guilloche: "rose",
  bust: "pilot",
  surcharge: "none",
  aspect: "calm",
  device: "goggles",
  cancel: "cds",
} as const;

export type PerfinSelection = Record<PerfinTraitCategory["id"], string>;

export function randomPerfinSelection(): PerfinSelection {
  const pick = (category: PerfinTraitCategory) => {
    const pool: PerfinTrait[] = category.noneLabel
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
    wove: pick(perfinCategoryById("wove")),
    guilloche: pick(perfinCategoryById("guilloche")),
    bust: pick(perfinCategoryById("bust")),
    surcharge: pick(perfinCategoryById("surcharge")),
    aspect: pick(perfinCategoryById("aspect")),
    device: pick(perfinCategoryById("device")),
    cancel: pick(perfinCategoryById("cancel")),
  };
}

export function perfinCombinationCount() {
  return perfinTraitCategories.reduce((product, category) => {
    const extra = category.noneLabel ? 1 : 0;
    return product * (category.traits.length + extra);
  }, 1);
}

export function perfinSelectionToLayers(selection: PerfinSelection) {
  return (["wove", "guilloche", "bust", "surcharge", "aspect", "device", "cancel"] as const)
    .map((id) => findPerfinTrait(id, selection[id]))
    .filter((trait): trait is PerfinTrait => Boolean(trait?.image))
    .map((trait) => perfinTraitSrc(trait.image));
}
