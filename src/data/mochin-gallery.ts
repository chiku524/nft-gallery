export type MochinSample = {
  id: number;
  name: string;
  image: string;
  attributes: { trait_type: string; value: string }[];
};

export const mochinSamples: MochinSample[] = [
  {
    id: 1,
    name: "Mochin #1",
    image: "/mochins-preview/1.gif?v=2",
    attributes: [
      { trait_type: "Stage", value: "Cream Cove" },
      { trait_type: "Haze", value: "Warm Key" },
      { trait_type: "Dough", value: "Snow" },
      { trait_type: "Face", value: "Blink" },
      { trait_type: "Topping", value: "Leaf" },
      { trait_type: "Steam", value: "Wisps" },
    ],
  },
  {
    id: 2,
    name: "Mochin #2",
    image: "/mochins-preview/2.gif?v=2",
    attributes: [
      { trait_type: "Stage", value: "Blush Cove" },
      { trait_type: "Haze", value: "Sakura Dust" },
      { trait_type: "Dough", value: "Berry" },
      { trait_type: "Face", value: "Wink" },
      { trait_type: "Topping", value: "Bow" },
      { trait_type: "Steam", value: "Sparkle" },
    ],
  },
  {
    id: 3,
    name: "Mochin #3",
    image: "/mochins-preview/3.gif?v=2",
    attributes: [
      { trait_type: "Stage", value: "Matcha Cove" },
      { trait_type: "Haze", value: "Gold Motes" },
      { trait_type: "Dough", value: "Matcha" },
      { trait_type: "Face", value: "Grin" },
      { trait_type: "Topping", value: "Sesame Dust" },
      { trait_type: "Steam", value: "Puff" },
    ],
  },
  {
    id: 4,
    name: "Mochin #4",
    image: "/mochins-preview/4.gif?v=2",
    attributes: [
      { trait_type: "Stage", value: "Dusk Cove" },
      { trait_type: "Haze", value: "Cool Rim" },
      { trait_type: "Dough", value: "Taro" },
      { trait_type: "Face", value: "Heart" },
      { trait_type: "Topping", value: "Berry" },
      { trait_type: "Steam", value: "Wisps" },
    ],
  },
  {
    id: 5,
    name: "Mochin #5",
    image: "/mochins-preview/5.gif?v=2",
    attributes: [
      { trait_type: "Stage", value: "Night Cove" },
      { trait_type: "Haze", value: "Warm Key" },
      { trait_type: "Dough", value: "Sesame" },
      { trait_type: "Face", value: "Pout" },
      { trait_type: "Topping", value: "Drizzle" },
      { trait_type: "Steam", value: "Still" },
    ],
  },
  {
    id: 6,
    name: "Mochin #6",
    image: "/mochins-preview/6.gif?v=2",
    attributes: [
      { trait_type: "Stage", value: "Marble Cove" },
      { trait_type: "Haze", value: "No haze" },
      { trait_type: "Dough", value: "Yuzu" },
      { trait_type: "Face", value: "Sleepy" },
      { trait_type: "Topping", value: "Kinako" },
      { trait_type: "Steam", value: "Puff" },
    ],
  },
  {
    id: 7,
    name: "Mochin #7",
    image: "/mochins-preview/7.gif?v=2",
    attributes: [
      { trait_type: "Stage", value: "Amber Cove" },
      { trait_type: "Haze", value: "Gold Motes" },
      { trait_type: "Dough", value: "Cocoa" },
      { trait_type: "Face", value: "Wide" },
      { trait_type: "Topping", value: "Leaf" },
      { trait_type: "Steam", value: "Sparkle" },
    ],
  },
  {
    id: 8,
    name: "Mochin #8",
    image: "/mochins-preview/8.gif?v=2",
    attributes: [
      { trait_type: "Stage", value: "Fog Cove" },
      { trait_type: "Haze", value: "Cool Rim" },
      { trait_type: "Dough", value: "Snow" },
      { trait_type: "Face", value: "Spark" },
      { trait_type: "Topping", value: "Plain" },
      { trait_type: "Steam", value: "Wisps" },
    ],
  },
];
