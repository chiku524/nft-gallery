export type BirbSample = {
  id: number;
  name: string;
  image: string;
  attributes: { trait_type: string; value: string }[];
};

export const birbSamples: BirbSample[] = [
  {
    id: 1,
    name: "Birb #1",
    image: "/birbs-preview/1.gif?v=4",
    attributes: [
      { trait_type: "Field", value: "White" },
      { trait_type: "Plumage", value: "Brown" },
      { trait_type: "Mug", value: "Blep" },
      { trait_type: "Accent", value: "None" },
    ],
  },
  {
    id: 2,
    name: "Birb #2",
    image: "/birbs-preview/2.gif?v=4",
    attributes: [
      { trait_type: "Field", value: "Blush" },
      { trait_type: "Plumage", value: "Pink" },
      { trait_type: "Mug", value: "Heart" },
      { trait_type: "Accent", value: "Bow" },
    ],
  },
  {
    id: 3,
    name: "Birb #3",
    image: "/birbs-preview/3.gif?v=4",
    attributes: [
      { trait_type: "Field", value: "Mint" },
      { trait_type: "Plumage", value: "Green" },
      { trait_type: "Mug", value: "Normal" },
      { trait_type: "Accent", value: "Leaf" },
    ],
  },
  {
    id: 4,
    name: "Birb #4",
    image: "/birbs-preview/4.gif?v=4",
    attributes: [
      { trait_type: "Field", value: "Sky" },
      { trait_type: "Plumage", value: "Blue" },
      { trait_type: "Mug", value: "Wide" },
      { trait_type: "Accent", value: "Flower" },
    ],
  },
  {
    id: 5,
    name: "Birb #5",
    image: "/birbs-preview/5.gif?v=4",
    attributes: [
      { trait_type: "Field", value: "Cream" },
      { trait_type: "Plumage", value: "Snow" },
      { trait_type: "Mug", value: "Sleepy" },
      { trait_type: "Accent", value: "None" },
    ],
  },
  {
    id: 6,
    name: "Birb #6",
    image: "/birbs-preview/6.gif?v=4",
    attributes: [
      { trait_type: "Field", value: "Peach" },
      { trait_type: "Plumage", value: "Gold" },
      { trait_type: "Mug", value: "Sparkly" },
      { trait_type: "Accent", value: "Berry" },
    ],
  },
  {
    id: 7,
    name: "Birb #7",
    image: "/birbs-preview/7.gif?v=4",
    attributes: [
      { trait_type: "Field", value: "Dusk" },
      { trait_type: "Plumage", value: "Dusk" },
      { trait_type: "Mug", value: "Wink" },
      { trait_type: "Accent", value: "Worm" },
    ],
  },
  {
    id: 8,
    name: "Birb #8",
    image: "/birbs-preview/8.gif?v=4",
    attributes: [
      { trait_type: "Field", value: "Forest" },
      { trait_type: "Plumage", value: "Brown" },
      { trait_type: "Mug", value: "Sad" },
      { trait_type: "Accent", value: "Leaf" },
    ],
  },
];
