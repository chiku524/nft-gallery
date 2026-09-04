export type GroovyTrait = {
  id: string;
  name: string;
  image?: string;
  rarity: number;
};

export type GroovyTraitCategory = {
  id: "venue" | "note" | "expression" | "topper" | "cable" | "riff";
  label: string;
  blurb: string;
  noneLabel?: string;
  traits: GroovyTrait[];
};

/** Bump when APNG layers change so the studio does not keep a stale loop. */
export const GROOVY_ART_VERSION = "groovy-v8";

export const GROOVY_FRAMES = 12;
export const GROOVY_DURATION_MS = 90;

export function groovyTraitSrc(path?: string) {
  if (!path) return "";
  return `${path}?v=${GROOVY_ART_VERSION}`;
}

export const groovyTraitCategories: GroovyTraitCategory[] = [
  {
    id: "venue",
    label: "Venue",
    blurb: "The stage — sunset strip, lava lamp, disco floor, velvet night, blacklight, chrome wash.",
    traits: [
      { id: "sunset", name: "Sunset Strip", image: "/groovy-traits/venue/sunset.png", rarity: 24 },
      { id: "lava", name: "Lava Lamp", image: "/groovy-traits/venue/lava.png", rarity: 20 },
      { id: "checker", name: "Disco Floor", image: "/groovy-traits/venue/checker.png", rarity: 18 },
      { id: "velvet", name: "Velvet Night", image: "/groovy-traits/venue/velvet.png", rarity: 16 },
      { id: "blacklight", name: "Blacklight", image: "/groovy-traits/venue/blacklight.png", rarity: 12 },
      { id: "chrome", name: "Chrome Wash", image: "/groovy-traits/venue/chrome.png", rarity: 10 },
    ],
  },
  {
    id: "note",
    label: "Note",
    blurb: "The citizen — a cartoon quarter, eighth, whole, or beamed pair. Round head is the face. Black stem. Stick limbs on the beat.",
    traits: [
      { id: "quarter", name: "Quarter", image: "/groovy-traits/note/quarter.png", rarity: 34 },
      { id: "eighth", name: "Eighth", image: "/groovy-traits/note/eighth.png", rarity: 28 },
      { id: "whole", name: "Whole", image: "/groovy-traits/note/whole.png", rarity: 22 },
      { id: "beamed", name: "Beamed", image: "/groovy-traits/note/beamed.png", rarity: 16 },
    ],
  },
  {
    id: "expression",
    label: "Expression",
    blurb: "Painted on the note-head. Cool lids, a shout, a wink, a groove, starry pupils.",
    traits: [
      { id: "cool", name: "Cool", image: "/groovy-traits/expression/cool.png", rarity: 26 },
      { id: "shout", name: "Shout", image: "/groovy-traits/expression/shout.png", rarity: 20 },
      { id: "wink", name: "Wink", image: "/groovy-traits/expression/wink.png", rarity: 18 },
      { id: "groove", name: "Groove", image: "/groovy-traits/expression/groove.png", rarity: 20 },
      { id: "star", name: "Starry", image: "/groovy-traits/expression/star.png", rarity: 16 },
    ],
  },
  {
    id: "topper",
    label: "Topper",
    blurb: "Sits on the notehead. Afro, shades, a knit beanie, a disco halo.",
    noneLabel: "None",
    traits: [
      { id: "afro", name: "Afro", image: "/groovy-traits/topper/afro.png", rarity: 20 },
      { id: "shades", name: "Shades", image: "/groovy-traits/topper/shades.png", rarity: 22 },
      { id: "visor", name: "Beanie", image: "/groovy-traits/topper/visor.png", rarity: 16 },
      { id: "halo", name: "Halo", image: "/groovy-traits/topper/halo.png", rarity: 14 },
    ],
  },
  {
    id: "cable",
    label: "Cable",
    blurb: "Gold chain under the chin, cans on the ears, a mic in the left hand.",
    noneLabel: "None",
    traits: [
      { id: "chain", name: "Gold Chain", image: "/groovy-traits/cable/chain.png", rarity: 24 },
      { id: "cans", name: "Cans", image: "/groovy-traits/cable/cans.png", rarity: 22 },
      { id: "mic", name: "Mic", image: "/groovy-traits/cable/mic.png", rarity: 18 },
    ],
  },
  {
    id: "riff",
    label: "Riff",
    blurb: "A floating extra — treble, vinyl, stars, a lightning bolt. Pulses off the beat.",
    noneLabel: "None",
    traits: [
      { id: "treble", name: "Treble", image: "/groovy-traits/riff/treble.png", rarity: 20 },
      { id: "vinyl", name: "Vinyl", image: "/groovy-traits/riff/vinyl.png", rarity: 18 },
      { id: "stars", name: "Stars", image: "/groovy-traits/riff/stars.png", rarity: 16 },
      { id: "bolt", name: "Bolt", image: "/groovy-traits/riff/bolt.png", rarity: 14 },
    ],
  },
];

export const noneGroovyTrait: GroovyTrait = { id: "none", name: "None", rarity: 0 };

export function groovyCategoryById(id: GroovyTraitCategory["id"]) {
  const category = groovyTraitCategories.find((item) => item.id === id);
  if (!category) throw new Error(`Unknown Groovy Nation trait category: ${id}`);
  return category;
}

export function findGroovyTrait(categoryId: GroovyTraitCategory["id"], traitId: string) {
  if (traitId === "none") return noneGroovyTrait;
  return groovyCategoryById(categoryId).traits.find((trait) => trait.id === traitId);
}

export const defaultGroovySelection = {
  venue: "sunset",
  note: "eighth",
  expression: "cool",
  topper: "shades",
  cable: "chain",
  riff: "vinyl",
} as const;

export type GroovySelection = Record<GroovyTraitCategory["id"], string>;

export function randomGroovySelection(): GroovySelection {
  const pick = (category: GroovyTraitCategory) => {
    const pool: GroovyTrait[] = category.noneLabel
      ? [{ id: "none", name: category.noneLabel, rarity: 36 }, ...category.traits]
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
    venue: pick(groovyCategoryById("venue")),
    note: pick(groovyCategoryById("note")),
    expression: pick(groovyCategoryById("expression")),
    topper: pick(groovyCategoryById("topper")),
    cable: pick(groovyCategoryById("cable")),
    riff: pick(groovyCategoryById("riff")),
  };
}

export function groovyCombinationCount() {
  return groovyTraitCategories.reduce((product, category) => {
    const extra = category.noneLabel ? 1 : 0;
    return product * (category.traits.length + extra);
  }, 1);
}

export function groovySelectionToLayers(selection: GroovySelection) {
  return (["venue", "note", "expression", "topper", "cable", "riff"] as const)
    .map((id) => findGroovyTrait(id, selection[id]))
    .filter((trait): trait is GroovyTrait => Boolean(trait?.image))
    .map((trait) => groovyTraitSrc(trait.image));
}
