export type ShookumSample = {
  id: number;
  name: string;
  image: string;
  attributes: { trait_type: string; value: string }[];
};

export const shookumSamples: ShookumSample[] = [
  {
    id: 1,
    name: "Shook'um #1",
    image: "/shookums-preview/1.gif?v=4",
    attributes: [
      { trait_type: "Night", value: "Parchment" },
      { trait_type: "Sheet", value: "Classic" },
      { trait_type: "Mug", value: "Normal" },
      { trait_type: "Hat", value: "None" },
      { trait_type: "Wrap", value: "None" },
      { trait_type: "Charm", value: "None" },
    ],
  },
  {
    id: 2,
    name: "Shook'um #2",
    image: "/shookums-preview/2.gif?v=4",
    attributes: [
      { trait_type: "Night", value: "Pumpkin" },
      { trait_type: "Sheet", value: "Blush" },
      { trait_type: "Mug", value: "Heart" },
      { trait_type: "Hat", value: "Bow" },
      { trait_type: "Wrap", value: "Chain" },
      { trait_type: "Charm", value: "None" },
    ],
  },
  {
    id: 3,
    name: "Shook'um #3",
    image: "/shookums-preview/3.gif?v=4",
    attributes: [
      { trait_type: "Night", value: "Midnight" },
      { trait_type: "Sheet", value: "Classic" },
      { trait_type: "Mug", value: "Spooked" },
      { trait_type: "Hat", value: "Witch" },
      { trait_type: "Wrap", value: "None" },
      { trait_type: "Charm", value: "Pumpkin" },
    ],
  },
  {
    id: 4,
    name: "Shook'um #4",
    image: "/shookums-preview/4.gif?v=4",
    attributes: [
      { trait_type: "Night", value: "Candy" },
      { trait_type: "Sheet", value: "Blush" },
      { trait_type: "Mug", value: "Sparkly" },
      { trait_type: "Hat", value: "Flower" },
      { trait_type: "Wrap", value: "Scarf" },
      { trait_type: "Charm", value: "Candy" },
    ],
  },
  {
    id: 5,
    name: "Shook'um #5",
    image: "/shookums-preview/5.gif?v=4",
    attributes: [
      { trait_type: "Night", value: "Dusk" },
      { trait_type: "Sheet", value: "Void" },
      { trait_type: "Mug", value: "Starry" },
      { trait_type: "Hat", value: "Halo" },
      { trait_type: "Wrap", value: "None" },
      { trait_type: "Charm", value: "Bat" },
    ],
  },
  {
    id: 6,
    name: "Shook'um #6",
    image: "/shookums-preview/6.gif?v=4",
    attributes: [
      { trait_type: "Night", value: "Fog" },
      { trait_type: "Sheet", value: "Classic" },
      { trait_type: "Mug", value: "Sleepy" },
      { trait_type: "Hat", value: "None" },
      { trait_type: "Wrap", value: "Pearls" },
      { trait_type: "Charm", value: "None" },
    ],
  },
  {
    id: 7,
    name: "Shook'um #7",
    image: "/shookums-preview/7.gif?v=4",
    attributes: [
      { trait_type: "Night", value: "Blood Moon" },
      { trait_type: "Sheet", value: "Void" },
      { trait_type: "Mug", value: "Wink" },
      { trait_type: "Hat", value: "Pumpkin" },
      { trait_type: "Wrap", value: "Chain" },
      { trait_type: "Charm", value: "Broom" },
    ],
  },
  {
    id: 8,
    name: "Shook'um #8",
    image: "/shookums-preview/8.gif?v=4",
    attributes: [
      { trait_type: "Night", value: "Graveyard" },
      { trait_type: "Sheet", value: "Classic" },
      { trait_type: "Mug", value: "Blep" },
      { trait_type: "Hat", value: "Cat Ears" },
      { trait_type: "Wrap", value: "Bowtie" },
      { trait_type: "Charm", value: "Candy Corn" },
    ],
  },
];
