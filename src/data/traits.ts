export type Overlay = {
  x: number;
  y: number;
  scale: number;
};

export type Trait = {
  id: string;
  name: string;
  image?: string;
  /** Foreground slice: body strap over the wall, or hat brim on the crown. */
  front?: string;
  /** Floppy ears (debug extract; compositor draws the full pug over the hat). */
  ears?: string;
  /** Paws redrawn over clothes and the ledge. */
  paws?: string;
  rarity: number;
  overlay?: Overlay;
};

export type TraitCategory = {
  id: "background" | "base" | "block" | "hat" | "body" | "accessory";
  label: string;
  blurb: string;
  noneLabel?: string;
  traits: Trait[];
};

const none: Overlay = { x: 0, y: 0, scale: 1 };

/** Bump when trait PNGs change so the studio canvas does not keep a stale bitmap. */
export const TRAIT_ART_VERSION = "11";

export function traitSrc(path?: string) {
  if (!path) return "";
  return `${path}?v=${TRAIT_ART_VERSION}`;
}

export const traitCategories: TraitCategory[] = [
  {
    id: "background",
    label: "Background",
    blurb: "The block behind the pug — stoops, rooftops, and neon corners.",
    traits: [
      {
        id: "brownstone",
        name: "Brownstone",
        image: "/traits/background/bg-brownstone.png",
        rarity: 22,
      },
      {
        id: "stoop-day",
        name: "Sunny Stoop",
        image: "/traits/background/bg-stoop-day.png",
        rarity: 18,
      },
      {
        id: "cream-brick",
        name: "Cream Paper",
        image: "/traits/background/bg-cream-brick.png",
        rarity: 16,
      },
      {
        id: "rooftop",
        name: "Golden Rooftop",
        image: "/traits/background/bg-rooftop-sunset.png",
        rarity: 14,
      },
      {
        id: "subway",
        name: "Subway Platform",
        image: "/traits/background/bg-subway.png",
        rarity: 10,
      },
      {
        id: "court",
        name: "Dusk Court",
        image: "/traits/background/bg-court-dusk.png",
        rarity: 8,
      },
      {
        id: "neon",
        name: "Neon Alley",
        image: "/traits/background/bg-neon-night.png",
        rarity: 7,
      },
      {
        id: "chain-green",
        name: "Grid Green",
        image: "/traits/background/bg-chain-green.png",
        rarity: 5,
      },
    ],
  },
  {
    id: "base",
    label: "Base",
    blurb: "Three coat colors, one signature peek over the ledge.",
    traits: [
      {
        id: "fawn",
        name: "Fawn Peek",
        image: "/traits/base/base-fawn-peek.png",
        ears: "/traits/base/front-ears-fawn.png",
        paws: "/traits/base/front-paws-fawn.png",
        rarity: 50,
        overlay: none,
      },
      {
        id: "cream",
        name: "Apricot Peek",
        image: "/traits/base/base-cream-peek.png",
        ears: "/traits/base/front-ears-cream.png",
        paws: "/traits/base/front-paws-cream.png",
        rarity: 30,
        overlay: none,
      },
      {
        id: "black",
        name: "Black Peek",
        image: "/traits/base/base-black-peek.png",
        ears: "/traits/base/front-ears-black.png",
        paws: "/traits/base/front-paws-black.png",
        rarity: 20,
        overlay: none,
      },
    ],
  },
  {
    id: "block",
    label: "Block",
    blurb: "The ledge they lean on — concrete, brownstone, crate, or gold. Swaps the wall under the paws.",
    traits: [
      {
        id: "concrete",
        name: "Cinder Block",
        image: "/traits/block/block-concrete.png",
        rarity: 40,
        overlay: none,
      },
      {
        id: "brownstone-ledge",
        name: "Brownstone Ledge",
        image: "/traits/block/block-brownstone.png",
        rarity: 28,
        overlay: none,
      },
      {
        id: "crate",
        name: "Crate Stack",
        image: "/traits/block/block-crate.png",
        rarity: 20,
        overlay: none,
      },
      {
        id: "gold",
        name: "Gold Bars",
        image: "/traits/block/block-gold.png",
        rarity: 12,
        overlay: none,
      },
    ],
  },
  {
    id: "hat",
    label: "Hat",
    blurb: "Beanies, newsie caps, hard hats, and the occasional crown — brim on the forehead, ears in front.",
    noneLabel: "Bare head",
    traits: [
      {
        id: "beanie",
        name: "Forest Beanie",
        image: "/traits/hat/hat-beanie.png",
        front: "/traits/hat/hat-beanie-crown.png",
        rarity: 18,
        overlay: none,
      },
      {
        id: "newsie",
        name: "Newsie Cap",
        image: "/traits/hat/hat-newsie.png",
        front: "/traits/hat/hat-newsie-crown.png",
        rarity: 16,
        overlay: none,
      },
      {
        id: "snapback",
        name: "Stoop Snapback",
        image: "/traits/hat/hat-snapback.png",
        front: "/traits/hat/hat-snapback-crown.png",
        rarity: 14,
        overlay: none,
      },
      {
        id: "hardhat",
        name: "Block Hard Hat",
        image: "/traits/hat/hat-hardhat.png",
        front: "/traits/hat/hat-hardhat-crown.png",
        rarity: 12,
        overlay: none,
      },
      {
        id: "crown",
        name: "Stoop Crown",
        image: "/traits/hat/hat-crown.png",
        front: "/traits/hat/hat-crown-crown.png",
        rarity: 12,
        overlay: none,
      },
    ],
  },
  {
    id: "body",
    label: "Body",
    blurb: "Neckerchiefs, collars, hoodies, and a heavy gold chain — split so they wrap the neck, not sit in front of the face.",
    noneLabel: "No clothes",
    traits: [
      {
        id: "bandana",
        name: "Forest Bandana",
        image: "/traits/body/body-bandana.png",
        front: "/traits/body/body-bandana-front.png",
        rarity: 22,
        overlay: none,
      },
      {
        id: "collar",
        name: "Red Collar",
        image: "/traits/body/body-collar.png",
        front: "/traits/body/body-collar-front.png",
        rarity: 18,
        overlay: none,
      },
      {
        id: "hoodie",
        name: "Cream Hoodie",
        image: "/traits/body/body-hoodie.png",
        front: "/traits/body/body-hoodie-front.png",
        rarity: 16,
        overlay: none,
      },
      {
        id: "gold-chain",
        name: "Gold Chain",
        image: "/traits/body/body-gold-chain.png",
        front: "/traits/body/body-gold-chain-front.png",
        rarity: 12,
        overlay: none,
      },
    ],
  },
  {
    id: "accessory",
    label: "Accessory",
    blurb: "Shades on the snout, or a treat parked on the ledge.",
    noneLabel: "Empty paws",
    traits: [
      {
        id: "bone",
        name: "Chewed Bone",
        image: "/traits/accessory/acc-bone.png",
        rarity: 18,
        overlay: none,
      },
      {
        id: "coffee",
        name: "Stoop Coffee",
        image: "/traits/accessory/acc-coffee.png",
        rarity: 16,
        overlay: none,
      },
      {
        id: "sunglasses",
        name: "Round Shades",
        image: "/traits/accessory/acc-sunglasses.png",
        rarity: 14,
        overlay: none,
      },
      {
        id: "blocks",
        name: "Toy Blocks",
        image: "/traits/accessory/acc-blocks.png",
        rarity: 12,
        overlay: none,
      },
      {
        id: "monocle",
        name: "Gold Monocle",
        image: "/traits/accessory/acc-monocle.png",
        rarity: 10,
        overlay: none,
      },
    ],
  },
];

export const noneTrait: Trait = { id: "none", name: "None", rarity: 0 };

export function categoryById(id: TraitCategory["id"]) {
  const category = traitCategories.find((item) => item.id === id);
  if (!category) throw new Error(`Unknown trait category: ${id}`);
  return category;
}

export function findTrait(categoryId: TraitCategory["id"], traitId: string) {
  if (traitId === "none") return noneTrait;
  return categoryById(categoryId).traits.find((trait) => trait.id === traitId);
}

export const defaultSelection = {
  background: "brownstone",
  base: "fawn",
  block: "concrete",
  hat: "beanie",
  body: "bandana",
  accessory: "none",
} as const;

export type Selection = Record<TraitCategory["id"], string>;

export function randomSelection(): Selection {
  const pick = (category: TraitCategory) => {
    const pool: Trait[] = category.noneLabel
      ? [{ id: "none", name: category.noneLabel, rarity: 28 }, ...category.traits]
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
    background: pick(categoryById("background")),
    base: pick(categoryById("base")),
    block: pick(categoryById("block")),
    hat: pick(categoryById("hat")),
    body: pick(categoryById("body")),
    accessory: pick(categoryById("accessory")),
  };
}

export function combinationCount() {
  return traitCategories.reduce((product, category) => {
    const extra = category.noneLabel ? 1 : 0;
    return product * (category.traits.length + extra);
  }, 1);
}
