export type WicklingTrait = {
  id: string;
  name: string;
  image?: string;
  rarity: number;
};

export type WicklingTraitCategory = {
  id: "night" | "halo" | "vessel" | "wick" | "wrap" | "drift";
  label: string;
  blurb: string;
  noneLabel?: string;
  traits: WicklingTrait[];
};

/** Bump when APNG layers change so the studio does not keep a stale loop. */
export const WICKLING_ART_VERSION = "wicklings-v1";

export const WICKLING_FRAMES = 12;
export const WICKLING_DURATION_MS = 80;

export function wicklingTraitSrc(path?: string) {
  if (!path) return "";
  return `${path}?v=${WICKLING_ART_VERSION}`;
}

export const wicklingTraitCategories: WicklingTraitCategory[] = [
  {
    id: "night",
    label: "Night",
    blurb: "Full-canvas loops — alleys, shrines, rooftops, and festival streets behind the lantern.",
    traits: [
      { id: "alley", name: "Lantern Alley", image: "/wicklings-traits/night/alley.png", rarity: 16 },
      { id: "shrine", name: "Shrine Path", image: "/wicklings-traits/night/shrine.png", rarity: 14 },
      { id: "rooftop", name: "Rooftop Night", image: "/wicklings-traits/night/rooftop.png", rarity: 14 },
      { id: "festival", name: "Festival Street", image: "/wicklings-traits/night/festival.png", rarity: 12 },
      { id: "fog", name: "Soft Fog", image: "/wicklings-traits/night/fog.png", rarity: 12 },
      { id: "moon", name: "Full Moon", image: "/wicklings-traits/night/moon.png", rarity: 12 },
      { id: "rain", name: "Paper Rain", image: "/wicklings-traits/night/rain.png", rarity: 10 },
      { id: "ember", name: "Ember Void", image: "/wicklings-traits/night/ember.png", rarity: 10 },
    ],
  },
  {
    id: "halo",
    label: "Halo",
    blurb: "Light that sits behind the paper and pulses on the shared clock.",
    noneLabel: "No halo",
    traits: [
      { id: "gold", name: "Gold Bloom", image: "/wicklings-traits/halo/gold.png", rarity: 16 },
      { id: "mothdust", name: "Moth Dust", image: "/wicklings-traits/halo/mothdust.png", rarity: 14 },
      { id: "firefly", name: "Firefly Ring", image: "/wicklings-traits/halo/firefly.png", rarity: 14 },
      { id: "smoke", name: "Incense Smoke", image: "/wicklings-traits/halo/smoke.png", rarity: 12 },
      { id: "heat", name: "Heat Shimmer", image: "/wicklings-traits/halo/heat.png", rarity: 12 },
    ],
  },
  {
    id: "vessel",
    label: "Vessel",
    blurb: "Six paper houses. Each one sways on the same hanging cord.",
    traits: [
      { id: "round", name: "Round Paper", image: "/wicklings-traits/vessel/round.png", rarity: 20 },
      { id: "andon", name: "Andon", image: "/wicklings-traits/vessel/andon.png", rarity: 18 },
      { id: "jar", name: "Glow Jar", image: "/wicklings-traits/vessel/jar.png", rarity: 16 },
      { id: "teapot", name: "Teapot", image: "/wicklings-traits/vessel/teapot.png", rarity: 16 },
      { id: "balloon", name: "Sky Lantern", image: "/wicklings-traits/vessel/balloon.png", rarity: 16 },
      { id: "temple", name: "Temple Hang", image: "/wicklings-traits/vessel/temple.png", rarity: 14 },
    ],
  },
  {
    id: "wick",
    label: "Wick",
    blurb: "The face is the flame — locked to the hang, with its own flicker and blink.",
    traits: [
      { id: "blink", name: "Blink", image: "/wicklings-traits/wick/blink.png", rarity: 22 },
      { id: "sleepy", name: "Sleepy", image: "/wicklings-traits/wick/sleepy.png", rarity: 18 },
      { id: "spark", name: "Spark", image: "/wicklings-traits/wick/spark.png", rarity: 16 },
      { id: "grin", name: "Grin", image: "/wicklings-traits/wick/grin.png", rarity: 16 },
      { id: "wink", name: "Wink", image: "/wicklings-traits/wick/wink.png", rarity: 14 },
      { id: "wide", name: "Wide", image: "/wicklings-traits/wick/wide.png", rarity: 14 },
    ],
  },
  {
    id: "wrap",
    label: "Wrap",
    blurb: "Marks on the paper that ride the same sway so they stay glued on.",
    noneLabel: "Bare paper",
    traits: [
      { id: "stripe", name: "Ink Stripe", image: "/wicklings-traits/wrap/stripe.png", rarity: 16 },
      { id: "floral", name: "Floral", image: "/wicklings-traits/wrap/floral.png", rarity: 14 },
      { id: "twine", name: "Twine Tassel", image: "/wicklings-traits/wrap/twine.png", rarity: 14 },
      { id: "stamp", name: "Red Stamp", image: "/wicklings-traits/wrap/stamp.png", rarity: 12 },
      { id: "cracks", name: "Hairline Cracks", image: "/wicklings-traits/wrap/cracks.png", rarity: 12 },
      { id: "tarot", name: "Moon Tarot", image: "/wicklings-traits/wrap/tarot.png", rarity: 10 },
    ],
  },
  {
    id: "drift",
    label: "Drift",
    blurb: "Front-layer loops — moths, petals, and incense on their own path.",
    noneLabel: "None",
    traits: [
      { id: "moth", name: "Orbit Moth", image: "/wicklings-traits/drift/moth.png", rarity: 16 },
      { id: "spark", name: "Spark Trail", image: "/wicklings-traits/drift/spark.png", rarity: 14 },
      { id: "incense", name: "Incense Curl", image: "/wicklings-traits/drift/incense.png", rarity: 14 },
      { id: "petal", name: "Falling Petal", image: "/wicklings-traits/drift/petal.png", rarity: 12 },
      { id: "wax", name: "Wax Drip", image: "/wicklings-traits/drift/wax.png", rarity: 10 },
    ],
  },
];

export const noneWicklingTrait: WicklingTrait = { id: "none", name: "None", rarity: 0 };

export function wicklingCategoryById(id: WicklingTraitCategory["id"]) {
  const category = wicklingTraitCategories.find((item) => item.id === id);
  if (!category) throw new Error(`Unknown Wickling trait category: ${id}`);
  return category;
}

export function findWicklingTrait(categoryId: WicklingTraitCategory["id"], traitId: string) {
  if (traitId === "none") return noneWicklingTrait;
  return wicklingCategoryById(categoryId).traits.find((trait) => trait.id === traitId);
}

export const defaultWicklingSelection = {
  night: "alley",
  halo: "gold",
  vessel: "round",
  wick: "blink",
  wrap: "twine",
  drift: "moth",
} as const;

export type WicklingSelection = Record<WicklingTraitCategory["id"], string>;

export function randomWicklingSelection(): WicklingSelection {
  const pick = (category: WicklingTraitCategory) => {
    const pool: WicklingTrait[] = category.noneLabel
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
    night: pick(wicklingCategoryById("night")),
    halo: pick(wicklingCategoryById("halo")),
    vessel: pick(wicklingCategoryById("vessel")),
    wick: pick(wicklingCategoryById("wick")),
    wrap: pick(wicklingCategoryById("wrap")),
    drift: pick(wicklingCategoryById("drift")),
  };
}

export function wicklingCombinationCount() {
  return wicklingTraitCategories.reduce((product, category) => {
    const extra = category.noneLabel ? 1 : 0;
    return product * (category.traits.length + extra);
  }, 1);
}

export function wicklingSelectionToLayers(selection: WicklingSelection) {
  return (["night", "halo", "vessel", "wick", "wrap", "drift"] as const)
    .map((id) => findWicklingTrait(id, selection[id]))
    .filter((trait): trait is WicklingTrait => Boolean(trait?.image))
    .map((trait) => wicklingTraitSrc(trait.image));
}
