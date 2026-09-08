export type NivoraTrait = {
  id: string;
  name: string;
  image?: string;
  rarity: number;
};

export type NivoraTraitCategory = {
  id: "plinth" | "bath" | "vista" | "flurry" | "lens" | "collar" | "plaque";
  label: string;
  blurb: string;
  noneLabel?: string;
  traits: NivoraTrait[];
};

/** Bump when APNG layers change so the studio does not keep a stale loop. */
export const NIVORA_ART_VERSION = "nivora-v3";

export const NIVORA_FRAMES = 12;
export const NIVORA_DURATION_MS = 90;

export function nivoraTraitSrc(path?: string) {
  if (!path) return "";
  return `${path}?v=${NIVORA_ART_VERSION}`;
}

export const nivoraTraitCategories: NivoraTraitCategory[] = [
  {
    id: "plinth",
    label: "Plinth",
    blurb: "The turned base — walnut, bakelite, brass, ceramic, ice plastic, ebon, cherry, marble.",
    traits: [
      { id: "walnut", name: "Walnut Plinth", image: "/nivora-traits/plinth/walnut.png", rarity: 18 },
      { id: "bakelite", name: "Bakelite Plinth", image: "/nivora-traits/plinth/bakelite.png", rarity: 14 },
      { id: "brass", name: "Brass Plinth", image: "/nivora-traits/plinth/brass.png", rarity: 12 },
      { id: "ceramic", name: "Ceramic Plinth", image: "/nivora-traits/plinth/ceramic.png", rarity: 12 },
      { id: "plastic", name: "Ice Plastic", image: "/nivora-traits/plinth/plastic.png", rarity: 12 },
      { id: "ebon", name: "Ebon Plinth", image: "/nivora-traits/plinth/ebon.png", rarity: 12 },
      { id: "cherry", name: "Cherry Plinth", image: "/nivora-traits/plinth/cherry.png", rarity: 10 },
      { id: "marble", name: "Marble Plinth", image: "/nivora-traits/plinth/marble.png", rarity: 10 },
    ],
  },
  {
    id: "bath",
    label: "Bath",
    blurb: "The liquor in the dome — clear, gin, pine, ink, rose, amber, cobalt.",
    traits: [
      { id: "clear", name: "Clear Bath", image: "/nivora-traits/bath/clear.png", rarity: 18 },
      { id: "gin", name: "Gin Bath", image: "/nivora-traits/bath/gin.png", rarity: 16 },
      { id: "pine", name: "Pine Bath", image: "/nivora-traits/bath/pine.png", rarity: 16 },
      { id: "ink", name: "Ink Bath", image: "/nivora-traits/bath/ink.png", rarity: 14 },
      { id: "rose", name: "Rose Bath", image: "/nivora-traits/bath/rose.png", rarity: 14 },
      { id: "amber", name: "Amber Bath", image: "/nivora-traits/bath/amber.png", rarity: 12 },
      { id: "cobalt", name: "Cobalt Bath", image: "/nivora-traits/bath/cobalt.png", rarity: 10 },
    ],
  },
  {
    id: "vista",
    label: "Vista",
    blurb: "The miniature inside — cabin, pine, lighthouse, deer, chapel, tram, bridge, moon.",
    traits: [
      { id: "cabin", name: "Cabin Vista", image: "/nivora-traits/vista/cabin.png", rarity: 18 },
      { id: "pine", name: "Pine Vista", image: "/nivora-traits/vista/pine.png", rarity: 16 },
      { id: "lighthouse", name: "Lighthouse Vista", image: "/nivora-traits/vista/lighthouse.png", rarity: 14 },
      { id: "deer", name: "Deer Vista", image: "/nivora-traits/vista/deer.png", rarity: 12 },
      { id: "chapel", name: "Chapel Vista", image: "/nivora-traits/vista/chapel.png", rarity: 12 },
      { id: "tram", name: "Tram Vista", image: "/nivora-traits/vista/tram.png", rarity: 10 },
      { id: "bridge", name: "Bridge Vista", image: "/nivora-traits/vista/bridge.png", rarity: 10 },
      { id: "moon", name: "Moon Vista", image: "/nivora-traits/vista/moon.png", rarity: 8 },
    ],
  },
  {
    id: "flurry",
    label: "Flurry",
    blurb: "What falls in the glycerin — snow, gold leaf, ash, confetti, mica, grit.",
    traits: [
      { id: "snow", name: "Snow Flurry", image: "/nivora-traits/flurry/snow.png", rarity: 22 },
      { id: "gold", name: "Gold Leaf", image: "/nivora-traits/flurry/gold.png", rarity: 16 },
      { id: "ash", name: "Ash Flurry", image: "/nivora-traits/flurry/ash.png", rarity: 16 },
      { id: "confetti", name: "Confetti Flurry", image: "/nivora-traits/flurry/confetti.png", rarity: 14 },
      { id: "mica", name: "Mica Flurry", image: "/nivora-traits/flurry/mica.png", rarity: 16 },
      { id: "grit", name: "Grit Flurry", image: "/nivora-traits/flurry/grit.png", rarity: 16 },
    ],
  },
  {
    id: "lens",
    label: "Lens",
    blurb: "The dome glass — clear, smoked, bubble, hairline crack, frost, tint.",
    traits: [
      { id: "clear", name: "Clear Lens", image: "/nivora-traits/lens/clear.png", rarity: 22 },
      { id: "smoked", name: "Smoked Lens", image: "/nivora-traits/lens/smoked.png", rarity: 16 },
      { id: "bubble", name: "Bubble Lens", image: "/nivora-traits/lens/bubble.png", rarity: 16 },
      { id: "crack", name: "Hairline Crack", image: "/nivora-traits/lens/crack.png", rarity: 14 },
      { id: "frost", name: "Frost Lens", image: "/nivora-traits/lens/frost.png", rarity: 16 },
      { id: "tint", name: "Tinted Lens", image: "/nivora-traits/lens/tint.png", rarity: 16 },
    ],
  },
  {
    id: "collar",
    label: "Collar",
    blurb: "The ring that seats the dome — brass, pewter, copper, black — or bare.",
    noneLabel: "Bare Neck",
    traits: [
      { id: "brass", name: "Brass Collar", image: "/nivora-traits/collar/brass.png", rarity: 22 },
      { id: "pewter", name: "Pewter Collar", image: "/nivora-traits/collar/pewter.png", rarity: 20 },
      { id: "copper", name: "Copper Collar", image: "/nivora-traits/collar/copper.png", rarity: 18 },
      { id: "black", name: "Black Collar", image: "/nivora-traits/collar/black.png", rarity: 16 },
    ],
  },
  {
    id: "plaque",
    label: "Plaque",
    blurb: "A plate on the plinth — year, crest, ribbon, stamp — or none.",
    noneLabel: "No Plaque",
    traits: [
      { id: "year", name: "Year Plaque", image: "/nivora-traits/plaque/year.png", rarity: 18 },
      { id: "crest", name: "Crest Plaque", image: "/nivora-traits/plaque/crest.png", rarity: 18 },
      { id: "ribbon", name: "Ribbon Plaque", image: "/nivora-traits/plaque/ribbon.png", rarity: 18 },
      { id: "stamp", name: "Stamp Plaque", image: "/nivora-traits/plaque/stamp.png", rarity: 18 },
    ],
  }
];

export const noneNivoraTrait: NivoraTrait = { id: "none", name: "None", rarity: 0 };

export function nivoraCategoryById(id: NivoraTraitCategory["id"]) {
  const category = nivoraTraitCategories.find((item) => item.id === id);
  if (!category) throw new Error(`Unknown Nivora trait category: ${id}`);
  return category;
}

export function findNivoraTrait(categoryId: NivoraTraitCategory["id"], traitId: string) {
  if (traitId === "none") return noneNivoraTrait;
  return nivoraCategoryById(categoryId).traits.find((trait) => trait.id === traitId);
}

export const defaultNivoraSelection = {
  plinth: "walnut",
  bath: "gin",
  vista: "cabin",
  flurry: "snow",
  lens: "clear",
  collar: "brass",
  plaque: "year",
} as const;

export type NivoraSelection = Record<NivoraTraitCategory["id"], string>;

export function randomNivoraSelection(): NivoraSelection {
  const pick = (category: NivoraTraitCategory) => {
    const pool: NivoraTrait[] = category.noneLabel
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
    plinth: pick(nivoraCategoryById("plinth")),
    bath: pick(nivoraCategoryById("bath")),
    vista: pick(nivoraCategoryById("vista")),
    flurry: pick(nivoraCategoryById("flurry")),
    lens: pick(nivoraCategoryById("lens")),
    collar: pick(nivoraCategoryById("collar")),
    plaque: pick(nivoraCategoryById("plaque")),
  };
}

export function nivoraCombinationCount() {
  return nivoraTraitCategories.reduce((product, category) => {
    const extra = category.noneLabel ? 1 : 0;
    return product * (category.traits.length + extra);
  }, 1);
}

export function nivoraSelectionToLayers(selection: NivoraSelection) {
  return (["plinth", "bath", "vista", "flurry", "lens", "collar", "plaque"] as const)
    .map((id) => findNivoraTrait(id, selection[id]))
    .filter((trait): trait is NivoraTrait => Boolean(trait?.image))
    .map((trait) => nivoraTraitSrc(trait.image));
}
