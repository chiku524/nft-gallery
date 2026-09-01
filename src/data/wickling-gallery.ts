export type WicklingSample = {
  id: number;
  name: string;
  image: string;
  attributes: { trait_type: string; value: string }[];
};

export const wicklingSamples: WicklingSample[] = [
  {
    id: 1,
    name: "Wickling #1",
    image: "/wicklings-preview/1.gif",
    attributes: [
      { trait_type: "Night", value: "Lantern Alley" },
      { trait_type: "Halo", value: "Gold Bloom" },
      { trait_type: "Vessel", value: "Round Paper" },
      { trait_type: "Wick", value: "Blink" },
      { trait_type: "Wrap", value: "Twine Tassel" },
      { trait_type: "Drift", value: "Orbit Moth" },
    ],
  },
  {
    id: 2,
    name: "Wickling #2",
    image: "/wicklings-preview/2.gif",
    attributes: [
      { trait_type: "Night", value: "Festival Street" },
      { trait_type: "Halo", value: "Heat Shimmer" },
      { trait_type: "Vessel", value: "Temple Hang" },
      { trait_type: "Wick", value: "Grin" },
      { trait_type: "Wrap", value: "Red Stamp" },
      { trait_type: "Drift", value: "Falling Petal" },
    ],
  },
  {
    id: 3,
    name: "Wickling #3",
    image: "/wicklings-preview/3.gif",
    attributes: [
      { trait_type: "Night", value: "Full Moon" },
      { trait_type: "Halo", value: "Moth Dust" },
      { trait_type: "Vessel", value: "Andon" },
      { trait_type: "Wick", value: "Sleepy" },
      { trait_type: "Wrap", value: "Ink Stripe" },
      { trait_type: "Drift", value: "None" },
    ],
  },
  {
    id: 4,
    name: "Wickling #4",
    image: "/wicklings-preview/4.gif",
    attributes: [
      { trait_type: "Night", value: "Shrine Path" },
      { trait_type: "Halo", value: "Firefly Ring" },
      { trait_type: "Vessel", value: "Teapot" },
      { trait_type: "Wick", value: "Wink" },
      { trait_type: "Wrap", value: "Floral" },
      { trait_type: "Drift", value: "Incense Curl" },
    ],
  },
  {
    id: 5,
    name: "Wickling #5",
    image: "/wicklings-preview/5.gif",
    attributes: [
      { trait_type: "Night", value: "Rooftop Night" },
      { trait_type: "Halo", value: "No halo" },
      { trait_type: "Vessel", value: "Sky Lantern" },
      { trait_type: "Wick", value: "Spark" },
      { trait_type: "Wrap", value: "Moon Tarot" },
      { trait_type: "Drift", value: "Spark Trail" },
    ],
  },
  {
    id: 6,
    name: "Wickling #6",
    image: "/wicklings-preview/6.gif",
    attributes: [
      { trait_type: "Night", value: "Ember Void" },
      { trait_type: "Halo", value: "Heat Shimmer" },
      { trait_type: "Vessel", value: "Glow Jar" },
      { trait_type: "Wick", value: "Wide" },
      { trait_type: "Wrap", value: "Bare paper" },
      { trait_type: "Drift", value: "Wax Drip" },
    ],
  },
  {
    id: 7,
    name: "Wickling #7",
    image: "/wicklings-preview/7.gif",
    attributes: [
      { trait_type: "Night", value: "Soft Fog" },
      { trait_type: "Halo", value: "Incense Smoke" },
      { trait_type: "Vessel", value: "Round Paper" },
      { trait_type: "Wick", value: "Blink" },
      { trait_type: "Wrap", value: "Hairline Cracks" },
      { trait_type: "Drift", value: "Orbit Moth" },
    ],
  },
  {
    id: 8,
    name: "Wickling #8",
    image: "/wicklings-preview/8.gif",
    attributes: [
      { trait_type: "Night", value: "Paper Rain" },
      { trait_type: "Halo", value: "Gold Bloom" },
      { trait_type: "Vessel", value: "Andon" },
      { trait_type: "Wick", value: "Grin" },
      { trait_type: "Wrap", value: "Twine Tassel" },
      { trait_type: "Drift", value: "Falling Petal" },
    ],
  },
];
