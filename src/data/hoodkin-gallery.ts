export type HoodkinSample = {
  id: number;
  name: string;
  image: string;
  attributes: { trait_type: string; value: string }[];
};

export const hoodkinSamples: HoodkinSample[] = [
  {
    id: 1,
    name: "Hoodkin #1",
    image: "/hoodkins-preview/1.gif",
    attributes: [
      { trait_type: "Pad", value: "Ledger" },
      { trait_type: "Glow", value: "Lime Halo" },
      { trait_type: "Pelt", value: "Silver" },
      { trait_type: "Fit", value: "Forest Hoodie" },
      { trait_type: "Mug", value: "Blink" },
      { trait_type: "Gear", value: "Headphones" },
    ],
  },
  {
    id: 2,
    name: "Hoodkin #2",
    image: "/hoodkins-preview/2.gif",
    attributes: [
      { trait_type: "Pad", value: "Blush" },
      { trait_type: "Glow", value: "Sparkle" },
      { trait_type: "Pelt", value: "Rust" },
      { trait_type: "Fit", value: "Blue Tee" },
      { trait_type: "Mug", value: "Wink" },
      { trait_type: "Gear", value: "Back Cap" },
    ],
  },
  {
    id: 3,
    name: "Hoodkin #3",
    image: "/hoodkins-preview/3.gif",
    attributes: [
      { trait_type: "Pad", value: "Mist" },
      { trait_type: "Glow", value: "Blush Bloom" },
      { trait_type: "Pelt", value: "Snow" },
      { trait_type: "Fit", value: "Clay Cardigan" },
      { trait_type: "Mug", value: "Heart" },
      { trait_type: "Gear", value: "Bucket Hat" },
    ],
  },
  {
    id: 4,
    name: "Hoodkin #4",
    image: "/hoodkins-preview/4.gif",
    attributes: [
      { trait_type: "Pad", value: "Mint" },
      { trait_type: "Glow", value: "Gold Dust" },
      { trait_type: "Pelt", value: "Moss" },
      { trait_type: "Fit", value: "Cream Polo" },
      { trait_type: "Mug", value: "Spark" },
      { trait_type: "Gear", value: "Coffee" },
    ],
  },
  {
    id: 5,
    name: "Hoodkin #5",
    image: "/hoodkins-preview/5.gif",
    attributes: [
      { trait_type: "Pad", value: "Night Tape" },
      { trait_type: "Glow", value: "Lime Halo" },
      { trait_type: "Pelt", value: "Ink" },
      { trait_type: "Fit", value: "Ink Jacket" },
      { trait_type: "Mug", value: "Smirk" },
      { trait_type: "Gear", value: "Shades" },
    ],
  },
  {
    id: 6,
    name: "Hoodkin #6",
    image: "/hoodkins-preview/6.gif",
    attributes: [
      { trait_type: "Pad", value: "Blotter" },
      { trait_type: "Glow", value: "No glow" },
      { trait_type: "Pelt", value: "Honey" },
      { trait_type: "Fit", value: "No fit" },
      { trait_type: "Mug", value: "Sleepy" },
      { trait_type: "Gear", value: "Beanie" },
    ],
  },
  {
    id: 7,
    name: "Hoodkin #7",
    image: "/hoodkins-preview/7.gif",
    attributes: [
      { trait_type: "Pad", value: "Amber" },
      { trait_type: "Glow", value: "Sparkle" },
      { trait_type: "Pelt", value: "Silver" },
      { trait_type: "Fit", value: "Forest Hoodie" },
      { trait_type: "Mug", value: "Wide" },
      { trait_type: "Gear", value: "Phone" },
    ],
  },
  {
    id: 8,
    name: "Hoodkin #8",
    image: "/hoodkins-preview/8.gif",
    attributes: [
      { trait_type: "Pad", value: "Slate" },
      { trait_type: "Glow", value: "Gold Dust" },
      { trait_type: "Pelt", value: "Rust" },
      { trait_type: "Fit", value: "Ink Jacket" },
      { trait_type: "Mug", value: "Coin" },
      { trait_type: "Gear", value: "None" },
    ],
  },
];
