export type PartyPandaTrait = {
  id: string;
  name: string;
  image?: string;
  rarity: number;
};

export type PartyPandaTraitCategory = {
  id: "venue" | "glow" | "panda" | "mood" | "fit" | "extra";
  label: string;
  blurb: string;
  noneLabel?: string;
  traits: PartyPandaTrait[];
};

/** Bump when APNG layers change so the studio does not keep a stale loop. */
export const PARTY_PANDA_ART_VERSION = "party-pandas-v1";

export const PARTY_PANDA_FRAMES = 12;
export const PARTY_PANDA_DURATION_MS = 80;

export function partyPandaTraitSrc(path?: string) {
  if (!path) return "";
  return `${path}?v=${PARTY_PANDA_ART_VERSION}`;
}

export const partyPandaTraitCategories: PartyPandaTraitCategory[] = [
  {
    id: "venue",
    label: "Venue",
    blurb: "Full-canvas party rooms — clubs, lounges, rooftops, and gardens behind the panda.",
    traits: [
      { id: "disco", name: "Disco Night", image: "/party-pandas-traits/venue/disco.png", rarity: 16 },
      { id: "neon", name: "Neon Club", image: "/party-pandas-traits/venue/neon.png", rarity: 14 },
      { id: "bamboo", name: "Bamboo Lounge", image: "/party-pandas-traits/venue/bamboo.png", rarity: 14 },
      { id: "rooftop", name: "Rooftop Glow", image: "/party-pandas-traits/venue/rooftop.png", rarity: 12 },
      { id: "candy", name: "Candy Rave", image: "/party-pandas-traits/venue/candy.png", rarity: 12 },
      { id: "moonlight", name: "Moonlight", image: "/party-pandas-traits/venue/moonlight.png", rarity: 12 },
      { id: "confetti", name: "Confetti Hall", image: "/party-pandas-traits/venue/confetti.png", rarity: 10 },
      { id: "garden", name: "Garden Party", image: "/party-pandas-traits/venue/garden.png", rarity: 10 },
    ],
  },
  {
    id: "glow",
    label: "Glow",
    blurb: "A pulse that sits behind the panda and rides the shared clock.",
    noneLabel: "No glow",
    traits: [
      { id: "disco", name: "Disco Pulse", image: "/party-pandas-traits/glow/disco.png", rarity: 16 },
      { id: "laser", name: "Laser Sweep", image: "/party-pandas-traits/glow/laser.png", rarity: 14 },
      { id: "sparkle", name: "Sparkle Burst", image: "/party-pandas-traits/glow/sparkle.png", rarity: 14 },
      { id: "neon", name: "Neon Ring", image: "/party-pandas-traits/glow/neon.png", rarity: 12 },
      { id: "champagne", name: "Champagne Haze", image: "/party-pandas-traits/glow/champagne.png", rarity: 12 },
    ],
  },
  {
    id: "panda",
    label: "Panda",
    blurb: "Six party pandas. Each one bobs on the same 12-frame breathe.",
    traits: [
      { id: "classic", name: "Classic", image: "/party-pandas-traits/panda/classic.png", rarity: 20 },
      { id: "chubby", name: "Chubby", image: "/party-pandas-traits/panda/chubby.png", rarity: 18 },
      { id: "cub", name: "Cub", image: "/party-pandas-traits/panda/cub.png", rarity: 16 },
      { id: "dancer", name: "Dancer", image: "/party-pandas-traits/panda/dancer.png", rarity: 16 },
      { id: "tuxedo", name: "Tuxedo", image: "/party-pandas-traits/panda/tuxedo.png", rarity: 16 },
      { id: "peach", name: "Peach", image: "/party-pandas-traits/panda/peach.png", rarity: 14 },
    ],
  },
  {
    id: "mood",
    label: "Mood",
    blurb: "Eyes and mouths locked to the panda bob, with their own blinks.",
    traits: [
      { id: "blink", name: "Blink", image: "/party-pandas-traits/mood/blink.png", rarity: 22 },
      { id: "wink", name: "Wink", image: "/party-pandas-traits/mood/wink.png", rarity: 18 },
      { id: "shades", name: "Shades", image: "/party-pandas-traits/mood/shades.png", rarity: 16 },
      { id: "heart", name: "Heart", image: "/party-pandas-traits/mood/heart.png", rarity: 16 },
      { id: "sleepy", name: "Sleepy", image: "/party-pandas-traits/mood/sleepy.png", rarity: 14 },
      { id: "spark", name: "Spark", image: "/party-pandas-traits/mood/spark.png", rarity: 14 },
    ],
  },
  {
    id: "fit",
    label: "Fit",
    blurb: "Hats and party wear that ride the same bob so they stay glued on.",
    noneLabel: "Bare head",
    traits: [
      { id: "cone", name: "Party Hat", image: "/party-pandas-traits/fit/cone.png", rarity: 16 },
      { id: "bow", name: "Bowtie", image: "/party-pandas-traits/fit/bow.png", rarity: 14 },
      { id: "phones", name: "Headphones", image: "/party-pandas-traits/fit/phones.png", rarity: 14 },
      { id: "lei", name: "Lei", image: "/party-pandas-traits/fit/lei.png", rarity: 12 },
      { id: "crown", name: "Tiny Crown", image: "/party-pandas-traits/fit/crown.png", rarity: 12 },
      { id: "afro", name: "Disco Afro", image: "/party-pandas-traits/fit/afro.png", rarity: 10 },
    ],
  },
  {
    id: "extra",
    label: "Extra",
    blurb: "Front-layer loops — confetti, balloons, and sparklers on their own path.",
    noneLabel: "None",
    traits: [
      { id: "confetti", name: "Confetti", image: "/party-pandas-traits/extra/confetti.png", rarity: 16 },
      { id: "balloon", name: "Balloon", image: "/party-pandas-traits/extra/balloon.png", rarity: 14 },
      { id: "cocktail", name: "Cocktail", image: "/party-pandas-traits/extra/cocktail.png", rarity: 14 },
      { id: "sparkler", name: "Sparkler", image: "/party-pandas-traits/extra/sparkler.png", rarity: 12 },
      { id: "boombox", name: "Boombox", image: "/party-pandas-traits/extra/boombox.png", rarity: 10 },
    ],
  },
];

export const nonePartyPandaTrait: PartyPandaTrait = { id: "none", name: "None", rarity: 0 };

export function partyPandaCategoryById(id: PartyPandaTraitCategory["id"]) {
  const category = partyPandaTraitCategories.find((item) => item.id === id);
  if (!category) throw new Error(`Unknown Party Panda trait category: ${id}`);
  return category;
}

export function findPartyPandaTrait(categoryId: PartyPandaTraitCategory["id"], traitId: string) {
  if (traitId === "none") return nonePartyPandaTrait;
  return partyPandaCategoryById(categoryId).traits.find((trait) => trait.id === traitId);
}

export const defaultPartyPandaSelection = {
  venue: "disco",
  glow: "disco",
  panda: "classic",
  mood: "blink",
  fit: "cone",
  extra: "confetti",
} as const;

export type PartyPandaSelection = Record<PartyPandaTraitCategory["id"], string>;

export function randomPartyPandaSelection(): PartyPandaSelection {
  const pick = (category: PartyPandaTraitCategory) => {
    const pool: PartyPandaTrait[] = category.noneLabel
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
    venue: pick(partyPandaCategoryById("venue")),
    glow: pick(partyPandaCategoryById("glow")),
    panda: pick(partyPandaCategoryById("panda")),
    mood: pick(partyPandaCategoryById("mood")),
    fit: pick(partyPandaCategoryById("fit")),
    extra: pick(partyPandaCategoryById("extra")),
  };
}

export function partyPandaCombinationCount() {
  return partyPandaTraitCategories.reduce((product, category) => {
    const extra = category.noneLabel ? 1 : 0;
    return product * (category.traits.length + extra);
  }, 1);
}

export function partyPandaSelectionToLayers(selection: PartyPandaSelection) {
  return (["venue", "glow", "panda", "mood", "fit", "extra"] as const)
    .map((id) => findPartyPandaTrait(id, selection[id]))
    .filter((trait): trait is PartyPandaTrait => Boolean(trait?.image))
    .map((trait) => partyPandaTraitSrc(trait.image));
}
