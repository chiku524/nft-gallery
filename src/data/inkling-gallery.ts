export type InklingSample = {
  id: number;
  name: string;
  image: string;
  attributes: { trait_type: string; value: string }[];
};

export const inklingSamples: InklingSample[] = [
  {
    id: 1,
    name: "Inkling #1",
    image: "/inklings-preview/1.gif",
    attributes: [
      { trait_type: "Paper", value: "Indigo Night" },
      { trait_type: "Bloom", value: "Violet Haze" },
      { trait_type: "Visage", value: "Fox" },
      { trait_type: "Gaze", value: "Bright" },
      { trait_type: "Mark", value: "Clean face" },
      { trait_type: "Adorn", value: "Flow Hair" },
    ],
  },
  {
    id: 2,
    name: "Inkling #2",
    image: "/inklings-preview/2.gif",
    attributes: [
      { trait_type: "Paper", value: "Peach Dusk" },
      { trait_type: "Bloom", value: "Gold Wash" },
      { trait_type: "Visage", value: "Crane" },
      { trait_type: "Gaze", value: "Lidded" },
      { trait_type: "Mark", value: "Red Seal" },
      { trait_type: "Adorn", value: "Silk Bun" },
    ],
  },
  {
    id: 3,
    name: "Inkling #3",
    image: "/inklings-preview/3.gif",
    attributes: [
      { trait_type: "Paper", value: "Celadon Garden" },
      { trait_type: "Bloom", value: "Teal Mist" },
      { trait_type: "Visage", value: "Koi" },
      { trait_type: "Gaze", value: "Dew" },
      { trait_type: "Mark", value: "Ink Splash" },
      { trait_type: "Adorn", value: "Bare head" },
    ],
  },
  {
    id: 4,
    name: "Inkling #4",
    image: "/inklings-preview/4.gif",
    attributes: [
      { trait_type: "Paper", value: "Charcoal Wash" },
      { trait_type: "Bloom", value: "No bloom" },
      { trait_type: "Visage", value: "Cat" },
      { trait_type: "Gaze", value: "Wink" },
      { trait_type: "Mark", value: "Slow Drip" },
      { trait_type: "Adorn", value: "Ink Ribbon" },
    ],
  },
  {
    id: 5,
    name: "Inkling #5",
    image: "/inklings-preview/5.gif",
    attributes: [
      { trait_type: "Paper", value: "Rose Gold" },
      { trait_type: "Bloom", value: "Coral Glow" },
      { trait_type: "Visage", value: "Moth" },
      { trait_type: "Gaze", value: "Ember" },
      { trait_type: "Mark", value: "Clean face" },
      { trait_type: "Adorn", value: "Wash Hood" },
    ],
  },
  {
    id: 6,
    name: "Inkling #6",
    image: "/inklings-preview/6.gif",
    attributes: [
      { trait_type: "Paper", value: "Storm Grey" },
      { trait_type: "Bloom", value: "Silver Veil" },
      { trait_type: "Visage", value: "Moon" },
      { trait_type: "Gaze", value: "Sleepy" },
      { trait_type: "Mark", value: "Brush Streak" },
      { trait_type: "Adorn", value: "Soft Crown" },
    ],
  },
  {
    id: 7,
    name: "Inkling #7",
    image: "/inklings-preview/7.gif",
    attributes: [
      { trait_type: "Paper", value: "Wine Paper" },
      { trait_type: "Bloom", value: "Gold Wash" },
      { trait_type: "Visage", value: "Otter" },
      { trait_type: "Gaze", value: "Bright" },
      { trait_type: "Mark", value: "Red Seal" },
      { trait_type: "Adorn", value: "Flow Hair" },
    ],
  },
  {
    id: 8,
    name: "Inkling #8",
    image: "/inklings-preview/8.gif",
    attributes: [
      { trait_type: "Paper", value: "Cream Rice" },
      { trait_type: "Bloom", value: "Violet Haze" },
      { trait_type: "Visage", value: "Hare" },
      { trait_type: "Gaze", value: "Dew" },
      { trait_type: "Mark", value: "Clean face" },
      { trait_type: "Adorn", value: "Silk Bun" },
    ],
  },
];
