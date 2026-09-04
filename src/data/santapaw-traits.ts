export type SantaPawTrait = {
  id: string;
  name: string;
  image?: string;
  rarity: number;
};

export type SantaPawTraitCategory = {
  id: "yard" | "glow" | "pelt" | "mug" | "hat" | "gear";
  label: string;
  blurb: string;
  noneLabel?: string;
  traits: SantaPawTrait[];
};

/** Bump when APNG layers change so the studio does not keep a stale loop. */
export const SANTAPAW_ART_VERSION = "santapaws-v1";

export const SANTAPAW_FRAMES = 12;
export const SANTAPAW_DURATION_MS = 90;

export function santapawTraitSrc(path?: string) {
  if (!path) return "";
  return `${path}?v=${SANTAPAW_ART_VERSION}`;
}

export const santapawTraitCategories: SantaPawTraitCategory[] = [
  {
    id: "yard",
    label: "Yard",
    blurb: "Full-canvas winter rooms — snowy nights, hearths, candy stripes, and cookie kitchens.",
    traits: [
      { id: "snowy", name: "Snowy Night", image: "/santapaws-traits/yard/snowy.png", rarity: 22 },
      { id: "hearth", name: "Cozy Hearth", image: "/santapaws-traits/yard/hearth.png", rarity: 20 },
      { id: "candy", name: "Candy Cane", image: "/santapaws-traits/yard/candy.png", rarity: 16 },
      { id: "wrap", name: "Gift Wrap", image: "/santapaws-traits/yard/wrap.png", rarity: 14 },
      { id: "kitchen", name: "Cookie Kitchen", image: "/santapaws-traits/yard/kitchen.png", rarity: 14 },
      { id: "aurora", name: "Aurora", image: "/santapaws-traits/yard/aurora.png", rarity: 14 },
    ],
  },
  {
    id: "glow",
    label: "Glow",
    blurb: "A halo around the cat — gold dust, snow glitter, and hearth ember sit outside the pelt.",
    noneLabel: "No glow",
    traits: [
      { id: "halo", name: "Soft Halo", image: "/santapaws-traits/glow/halo.png", rarity: 20 },
      { id: "sparkle", name: "Sparkle", image: "/santapaws-traits/glow/sparkle.png", rarity: 18 },
      { id: "glitter", name: "Snow Glitter", image: "/santapaws-traits/glow/glitter.png", rarity: 18 },
      { id: "ember", name: "Ember", image: "/santapaws-traits/glow/ember.png", rarity: 16 },
    ],
  },
  {
    id: "pelt",
    label: "Pelt",
    blurb: "Seven winter coats — white fluff, ginger, tuxedo, gray tabby, calico, charcoal, cocoa.",
    traits: [
      { id: "fluff", name: "White Fluff", image: "/santapaws-traits/pelt/fluff.png", rarity: 20 },
      { id: "ginger", name: "Ginger", image: "/santapaws-traits/pelt/ginger.png", rarity: 18 },
      { id: "tuxedo", name: "Tuxedo", image: "/santapaws-traits/pelt/tuxedo.png", rarity: 16 },
      { id: "tabby", name: "Gray Tabby", image: "/santapaws-traits/pelt/tabby.png", rarity: 16 },
      { id: "calico", name: "Calico", image: "/santapaws-traits/pelt/calico.png", rarity: 12 },
      { id: "charcoal", name: "Charcoal", image: "/santapaws-traits/pelt/charcoal.png", rarity: 10 },
      { id: "cocoa", name: "Cocoa", image: "/santapaws-traits/pelt/cocoa.png", rarity: 8 },
    ],
  },
  {
    id: "mug",
    label: "Mug",
    blurb: "The face — cheerful, wink, sleepy — locked to the bob so the eyes stay glued on.",
    traits: [
      { id: "cheerful", name: "Cheerful", image: "/santapaws-traits/mug/cheerful.png", rarity: 20 },
      { id: "wink", name: "Wink", image: "/santapaws-traits/mug/wink.png", rarity: 16 },
      { id: "sleepy", name: "Sleepy", image: "/santapaws-traits/mug/sleepy.png", rarity: 16 },
      { id: "blush", name: "Blush", image: "/santapaws-traits/mug/blush.png", rarity: 14 },
      { id: "surprise", name: "Surprised", image: "/santapaws-traits/mug/surprise.png", rarity: 12 },
      { id: "tongue", name: "Tongue Out", image: "/santapaws-traits/mug/tongue.png", rarity: 12 },
      { id: "heart", name: "Heart Eyes", image: "/santapaws-traits/mug/heart.png", rarity: 10 },
    ],
  },
  {
    id: "hat",
    label: "Hat",
    blurb: "Sits on the same crown — Santa, elf, antlers, pom beanie, holly. The pelt is not cut.",
    noneLabel: "None",
    traits: [
      { id: "santa", name: "Santa Hat", image: "/santapaws-traits/hat/santa.png", rarity: 22 },
      { id: "elf", name: "Elf Cap", image: "/santapaws-traits/hat/elf.png", rarity: 16 },
      { id: "beanie", name: "Pom Beanie", image: "/santapaws-traits/hat/beanie.png", rarity: 14 },
      { id: "antlers", name: "Antlers", image: "/santapaws-traits/hat/antlers.png", rarity: 14 },
      { id: "holly", name: "Holly Crown", image: "/santapaws-traits/hat/holly.png", rarity: 12 },
    ],
  },
  {
    id: "gear",
    label: "Gear",
    blurb: "Scarves, sweaters, bells, cocoa, presents, stockings, and a sprig of mistletoe.",
    noneLabel: "None",
    traits: [
      { id: "scarf", name: "Scarf", image: "/santapaws-traits/gear/scarf.png", rarity: 16 },
      { id: "sweater", name: "Sweater", image: "/santapaws-traits/gear/sweater.png", rarity: 14 },
      { id: "bells", name: "Bells", image: "/santapaws-traits/gear/bells.png", rarity: 14 },
      { id: "cocoa", name: "Cocoa", image: "/santapaws-traits/gear/cocoa.png", rarity: 12 },
      { id: "present", name: "Present", image: "/santapaws-traits/gear/present.png", rarity: 12 },
      { id: "stocking", name: "Stocking", image: "/santapaws-traits/gear/stocking.png", rarity: 8 },
      { id: "mistletoe", name: "Mistletoe", image: "/santapaws-traits/gear/mistletoe.png", rarity: 6 },
    ],
  },
];

export const noneSantaPawTrait: SantaPawTrait = { id: "none", name: "None", rarity: 0 };

export function santapawCategoryById(id: SantaPawTraitCategory["id"]) {
  const category = santapawTraitCategories.find((item) => item.id === id);
  if (!category) throw new Error(`Unknown Santa Paw trait category: ${id}`);
  return category;
}

export function findSantaPawTrait(categoryId: SantaPawTraitCategory["id"], traitId: string) {
  if (traitId === "none") return noneSantaPawTrait;
  return santapawCategoryById(categoryId).traits.find((trait) => trait.id === traitId);
}

export const defaultSantaPawSelection = {
  yard: "snowy",
  glow: "halo",
  pelt: "fluff",
  mug: "cheerful",
  hat: "santa",
  gear: "scarf",
} as const;

export type SantaPawSelection = Record<SantaPawTraitCategory["id"], string>;

export function randomSantaPawSelection(): SantaPawSelection {
  const pick = (category: SantaPawTraitCategory) => {
    const pool: SantaPawTrait[] = category.noneLabel
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
    yard: pick(santapawCategoryById("yard")),
    glow: pick(santapawCategoryById("glow")),
    pelt: pick(santapawCategoryById("pelt")),
    mug: pick(santapawCategoryById("mug")),
    hat: pick(santapawCategoryById("hat")),
    gear: pick(santapawCategoryById("gear")),
  };
}

export function santapawCombinationCount() {
  return santapawTraitCategories.reduce((product, category) => {
    const extra = category.noneLabel ? 1 : 0;
    return product * (category.traits.length + extra);
  }, 1);
}

export function santapawSelectionToLayers(selection: SantaPawSelection) {
  return (["yard", "glow", "pelt", "mug", "hat", "gear"] as const)
    .map((id) => findSantaPawTrait(id, selection[id]))
    .filter((trait): trait is SantaPawTrait => Boolean(trait?.image))
    .map((trait) => santapawTraitSrc(trait.image));
}
